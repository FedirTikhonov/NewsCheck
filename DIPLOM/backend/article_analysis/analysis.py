import openai
import voyageai
import os
import datetime
from typing import List
from dotenv import load_dotenv
from sqlalchemy import create_engine, and_, or_, func, asc
from sqlalchemy.orm import sessionmaker

from utils.llm_requests import message_llm
from utils.schemas import MetricSchema, CategoryResponseSchema, DigestTextResponseSchema
from utils.semantic_analysis import generate_recommendations, categorize_articles
from postgres_db.models.Article import Article
from postgres_db.models.Paragraph import Paragraph
from postgres_db.models.Category import Category
from postgres_db.models.FactCheckCategory import FactcheckCategory
from postgres_db.models.WeeklyStats import WeeklyStats
from postgres_db.models.WeeklyReport import WeeklyReport
from article_scraping.scraping import scrape_fact_check_articles


EMBEDDING_DIM = 1024


def generate_analysis_for_news(articles_lst: List, verbose=False, return_values=True):
    load_dotenv()
    engine = create_engine(os.environ["DATABASE_URL"])
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    openai_client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    voyageai_client = voyageai.Client(api_key=os.environ.get("VOYAGEAI_API_KEY"))

    with open('prompts/system_prompt_metrics.txt', 'r') as system_prompt_file:
        system_prompt_metric = system_prompt_file.read()

    metric_assistant = openai_client.beta.assistants.create(
        model='gpt-4.1-mini',
        instructions=system_prompt_metric,
        temperature=0.5,
        response_format={
            'type': 'json_schema',
            'json_schema':
                {
                    'name': 'MetricSchema',
                    'schema': MetricSchema.model_json_schema()
                }
        }
    )

    try:
        articles_lst = articles_lst[0]
    except IndexError:
        print('Articles list exception')

    for scraped_article in articles_lst:
        query = session.query(Article).filter(Article.href == scraped_article['href']).first()
        if query:
            continue
        article = Article(
            title=scraped_article['title'],
            href=scraped_article['href'],
            outlet=scraped_article['outlet'],
            published_at=scraped_article['timestamp'],
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            status='processing',
        )
        session.add(article)
        try:
            session.commit()
        except Exception as e:
            print('Failed to save changes to article')
        for paragraph_num, paragraph in enumerate(scraped_article['paragraphs']):
            article.add_paragraph(paragraph, paragraph_num)
        for source_num, source in enumerate(scraped_article['sources']):
            article.add_source(source, source_num)
        try:
            metric = message_llm(article=scraped_article, client=openai_client, assistant=metric_assistant, verbose=verbose)
            article.add_metric(metric)
        except Exception as e:
            print('Failed to save metrics to article')
        recommended_articles = generate_recommendations(article=scraped_article,
                                                        article_id=article.id,
                                                        voyageai_client=voyageai_client,
                                                        create_vector=True)
        for recommended_article in recommended_articles:
            article.add_recommendation(recommended_article)

        article.mark_processed()
        session.add(article)
        session.commit()
    session.close()

    openai_client.beta.assistants.delete(assistant_id=metric_assistant.id)


def generate_analysis_for_fact_checkers(articles_lst: List, verbose=False, return_values=True):
    load_dotenv()
    engine = create_engine(os.environ["DATABASE_URL"])
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    openai_client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    with open('prompts/system_prompt_categories.txt', 'r') as system_prompt_file:
        system_prompt_categories = system_prompt_file.read()

    category_article_assistant = openai_client.beta.assistants.create(
        model='gpt-4.1-mini',
        instructions=system_prompt_categories,
        temperature=0.1,
        response_format={
            'type': 'json_schema',
            'json_schema':
                {
                    'name': 'MetricSchema',
                    'schema': CategoryResponseSchema.model_json_schema()
                }
        }
    )
    try:
        articles_lst = articles_lst[0]
    except IndexError:
        print('Articles list exception')

    for scraped_article in articles_lst:
        query = session.query(Article).filter(Article.title == scraped_article['title']).first()
        if query:
            continue
        article = Article(
            title=scraped_article['title'],
            href=scraped_article['href'],
            outlet=scraped_article['outlet'],
            published_at=scraped_article['timestamp'],
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            status='processing',
        )
        session.add(article)
        session.commit()
        for paragraph_num, paragraph in enumerate(scraped_article['paragraphs']):
            article.add_paragraph(paragraph, paragraph_num)
        for source_num, source in enumerate(scraped_article['sources']):
            article.add_source(source, source_num)
        print(f'categorizing_article {article.title}')
        category_ids = categorize_articles(article=scraped_article, assistant=category_article_assistant,
                                           openai_client=openai_client)
        for category_id in category_ids:
            article.add_factcheck_category(category_id)

        article.mark_processed()
        session.add(article)
        session.commit()
    session.close()

    openai_client.beta.assistants.delete(assistant_id=category_article_assistant.id)


def update_recommendations():
    load_dotenv()
    engine = create_engine(os.environ["DATABASE_URL"])
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()

    try:
        voyageai_client = voyageai.Client(api_key=os.environ.get("VOYAGEAI_API_KEY"))

        # Find articles from last hour
        time_now = datetime.datetime.now(datetime.timezone.utc)
        time_one_hour_ago = time_now - datetime.timedelta(hours=1)

        articles_to_update = session.query(Article).filter(and_(
            Article.published_at >= time_one_hour_ago,
            Article.published_at < time_now
        )).all()

        print(f"Found {len(articles_to_update)} articles to update")

        for article in articles_to_update:
            try:
                print(f"Processing article ID: {article.id}, Title: {article.title}")

                article.mark_processing()
                session.commit()

                article.remove_recommendations()
                session.commit()

                article_dict = {
                    'title': article.title,
                    'href': article.href,
                    'outlet': article.outlet,
                    'timestamp': article.published_at,
                    'status': article.status,
                }

                recommended_articles = generate_recommendations(
                    article=article_dict,
                    article_id=article.id,
                    voyageai_client=voyageai_client,
                    create_vector=False
                )

                seen_ids = set()

                for recommended_article in recommended_articles:
                    if recommended_article['id'] in seen_ids:
                        continue

                    seen_ids.add(recommended_article['id'])

                    try:
                        article.add_recommendation(recommended_article_dict=recommended_article)
                    except Exception as e:
                        print(
                            f"Error adding recommendation {recommended_article['id']} to article {article.id}: {str(e)}")
                        continue

                try:
                    session.add(article)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(f"Error saving recommendations for article {article.id}: {str(e)}")

                article.mark_processed()

            except Exception as e:
                session.rollback()
                print(f"Error processing article {article.id}: {str(e)}")
                continue

    except Exception as e:
        print(f"General error in update function: {str(e)}")
    finally:
        session.close()
        print("Update process completed")


def create_weekly_stats(current_date=None):
    load_dotenv()
    engine = create_engine(os.environ["DATABASE_URL"])
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    categories = session.query(Category).all()
    if current_date:
        today = current_date
    else:
        today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    for category in categories:
        query = (
            session.query(func.count())
            .select_from(FactcheckCategory)
            .join(Article, Article.id == FactcheckCategory.article_id)
            .filter(Article.published_at <= today)
            .filter(Article.published_at >= seven_days_ago)
            .filter(FactcheckCategory.category_id == category.id)
        )
        formatted_date = today.strftime("%Y-%m-%d")
        session.add(WeeklyStats(
            category_id=category.id,
            category_num=query.scalar(),
            date=formatted_date,
        ))
        session.commit()
    session.close()


def create_weekly_report():
    load_dotenv()
    engine = create_engine(os.environ["DATABASE_URL"])
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    openai_client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    with open('prompts/system_prompt_digest.txt', 'r') as system_prompt_file:
        system_prompt_digest = system_prompt_file.read()

    digest_article_assistant = openai_client.beta.assistants.create(
        model='gpt-4.1-mini',
        instructions=system_prompt_digest,
        temperature=0.1,
        response_format={
            'type': 'json_schema',
            'json_schema':
                {
                    'name': 'MetricSchema',
                    'schema': DigestTextResponseSchema.model_json_schema()
                }
        }
    )

    articles = session.query(Article).filter(
        and_(
            Article.outlet == 'stopfake',
            Article.published_at <= today,
            Article.published_at >= seven_days_ago
        )
    ).limit(10).all()

    request_body = {'articles': []}
    for article in articles:
        article_text = []
        article_paragraphs = session.query(Paragraph
                                           ).filter(Paragraph.article_id == article.id
                                                    ).order_by(asc(Paragraph.paragraph_num)
                                                               ).all()
        for article_paragraph in article_paragraphs:
            article_text.append(article_paragraph.paragraph_text)

        article_text = ' '.join(article_text)

        request_body['articles'].append({
            'title': article.title,
            'text': article_text,
            'timestamp': str(article.published_at)
        })
    try:
        digest = message_llm(request_body, assistant=digest_article_assistant, client=openai_client, verbose=True)['digest_text']
        weekly_report = WeeklyReport(
            digest_date=today,
            digest_text=digest)
        session.add(weekly_report)
        session.commit()
        session.close()
    except Exception as e:
        print(f"Error adding weekly report")
        session.rollback()
        session.close()


if __name__ == '__main__':
    create_weekly_report()
