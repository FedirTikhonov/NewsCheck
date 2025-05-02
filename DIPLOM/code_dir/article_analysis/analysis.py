import openai
import voyageai
import os
import datetime
from typing import List
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.llm_requests import generate_metric
from utils.schemas import MetricSchema, SameIssueArticleResponseSchema
from utils.semantic_analysis import generate_recommendations, find_same_issue_articles_with_llm
from article_scraping.scraping import scrape_news
from postgres_db.models.Article import Article


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

    for scraped_article in articles_lst:
        article = Article(
            title=scraped_article['title'],
            href=scraped_article['href'],
            outlet=scraped_article['outlet'],
            published_at=scraped_article['published_at'],
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            status='processing',
        )
        for paragraph_num, paragraph in enumerate(scraped_article['paragraphs']):
            article.add_paragraph(paragraph, paragraph_num)
        for source_num, source in enumerate(scraped_article['sources']):
            article.add_paragraph(source, source_num)
        metric = generate_metric(article=article, client=openai_client, assistant=metric_assistant, verbose=verbose)
        article.add_metric(metric)
        recommended_articles = generate_recommendations(article=scraped_article, article_id=article.id, voyageai_client=voyageai_client)
        for recommended_article in recommended_articles:
            article.add_recommendation(recommended_article)
        same_issue_articles = find_same_issue_articles_with_llm(article=scraped_article,
                                                                article_id=article.id,
                                                                assistant=same_issue_article_assistant,
                                                                openai_client=openai_client,
                                                                voyageai_client=voyageai_client,
                                                                issue_span=48,
                                                                session=session)
        for same_issue_article in same_issue_articles:
            article.add_same_issue_article(same_issue_article)
        session.add(article)
        session.commit()
        session.close()
    openai_client.beta.assistants.delete(assistant_id=metric_assistant.id)
    openai_client.beta.assistants.delete(assistant_id=same_issue_article_assistant.id)


if __name__ == '__main__':
    articles = scrape_news(verbose=True)
