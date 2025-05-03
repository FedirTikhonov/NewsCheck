import openai
import voyageai
import os
import datetime
from typing import List
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from DIPLOM.code_dir.article_analysis.utils.llm_requests import message_llm
from DIPLOM.code_dir.article_analysis.utils.schemas import MetricSchema, SameIssueArticleResponseSchema, CategoryResponseSchema
from DIPLOM.code_dir.article_analysis.utils.semantic_analysis import generate_recommendations, find_same_issue_articles, \
    categorize_articles
from DIPLOM.code_dir.article_analysis.article_scraping.scraping import scrape_news
from DIPLOM.code_dir.article_analysis.postgres_db.models.Article import Article


EMBEDDING_DIM = 512


def generate_analysis(articles_lst: List, verbose=False, return_values=True):
    load_dotenv()
    engine = create_engine(os.environ["DATABASE_URL"])
    Session = sessionmaker(bind=engine)
    session = Session()
    openai_client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    voyageai_client = voyageai.Client(api_key=os.environ.get("VOYAGEAI_API_KEY"))

    with open('prompts/system_prompt_same_issue_article.txt', 'r') as system_prompt_file:
        system_prompt_same_issue_article = system_prompt_file.read()

    with open('prompts/system_prompt_metrics.txt', 'r') as system_prompt_file:
        system_prompt_metric = system_prompt_file.read()

    with open('prompts/system_prompt_categories.txt', 'r') as system_prompt_file:
        system_prompt_categories = system_prompt_file.read()

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

    same_issue_article_assistant = openai_client.beta.assistants.create(
        model='gpt-4.1-mini',
        instructions=system_prompt_same_issue_article,
        temperature=0.1,
        response_format={
            'type': 'json_schema',
            'json_schema':
                {
                    'name': 'MetricSchema',
                    'schema': SameIssueArticleResponseSchema.model_json_schema()
                }
        }
    )

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
            article.add_paragraph(source, source_num)
        metric = message_llm(article=scraped_article, client=openai_client, assistant=metric_assistant, verbose=verbose)
        article.add_metric(metric)
        recommended_articles = generate_recommendations(article=scraped_article, article_id=article.id, voyageai_client=voyageai_client)
        for recommended_article in recommended_articles:
            article.add_recommendation(recommended_article)
        same_issue_articles = find_same_issue_articles(article=scraped_article,
                                                       article_id=article.id,
                                                       assistant=same_issue_article_assistant,
                                                       openai_client=openai_client,
                                                       voyageai_client=voyageai_client,
                                                       session=session)
        for same_issue_article in same_issue_articles:
            article.add_same_issue_article(same_issue_article)

        if scraped_article['outlet'] in ['voxukraine', 'stopfake']:
            category_ids = categorize_articles(article=scraped_article, assistant=category_article_assistant, openai_client=openai_client)
            for category_id in category_ids:
                article.add_factcheck_category(category_id)
        article.mark_processed()
        session.add(article)
        session.commit()
        session.close()
    openai_client.beta.assistants.delete(assistant_id=metric_assistant.id)
    openai_client.beta.assistants.delete(assistant_id=same_issue_article_assistant.id)
    openai_client.beta.assistants.delete(assistant_id=category_article_assistant.id)


if __name__ == '__main__':
    articles = scrape_news()
    articles = [[article for article in articles if article['outlet'] in ['voxukraine', 'stopfake']]]
    print(len(articles[0]))
    generate_analysis(articles, verbose=True)

