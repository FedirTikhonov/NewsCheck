import openai
import sqlalchemy.orm.session
import voyageai
import datetime
import dateutil.parser

from DIPLOM.code_dir.article_analysis.milvus_db.utils import similarity_search, insert_article
from DIPLOM.code_dir.article_analysis.postgres_db.models.Article import Article
from DIPLOM.code_dir.article_analysis.postgres_db.models.Paragraph import Paragraph
from DIPLOM.code_dir.article_analysis.utils.llm_requests import message_llm

EMBEDDING_DIM = 1024


def generate_recommendations(article: dict, article_id: int, voyageai_client: voyageai.Client):
    article_text = [article['title']]
    article_text.extend(article['paragraphs'])
    article_text = ' '.join(article_text)

    article_text_embeddings = voyageai_client.embed(
        texts=[article_text],
        model='voyage-3',
        output_dimension=EMBEDDING_DIM,
    ).embeddings

    found_articles = similarity_search(article_text_embeddings, embedding_type='recommendations')
    recommended_articles = []
    for found_article in found_articles:
        recommended_article = {
            'last_updated': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            'id': found_article['postgres_id'],
            'similarity_score': found_article['similarity_score']
        }
        recommended_articles.append(recommended_article)

    insert_article(postgres_id=article_id, embedding=article_text_embeddings[0], embedding_type='recommendations')

    return recommended_articles


def find_same_issue_articles(article: dict,
                             article_id: int,
                             voyageai_client: voyageai.Client,
                             openai_client: openai.OpenAI,
                             assistant,
                             session: sqlalchemy.orm.session.Session,
                             issue_span=datetime.timedelta(hours=48)):
    article_text = [article['title']]
    for paragraph_num, paragraph in enumerate(article['paragraphs']):
        if paragraph_num in [0, 1]:
            article_text.append(paragraph)
    article_text = ' '.join(article_text).strip()

    # Create a main article's beginning text embedding
    article_text_embeddings = voyageai_client.embed(
        texts=[article_text],
        model='voyage-3',
        output_dimension=EMBEDDING_DIM,
    ).embeddings

    # Find similar article beginnings
    found_articles = similarity_search(article_text_embeddings, embedding_type='same_issue', top_k=20)

    # Insert article into milvus collection
    insert_article(postgres_id=article_id, embedding=article_text_embeddings[0], embedding_type='same_issue')

    similar_articles = []
    for found_article in found_articles:
        similar_article = {
            'last_updated': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            'id': found_article['postgres_id'],
            'similarity_score': found_article['similarity_score']
        }
        similar_articles.append(similar_article)

    request_body = {
        'main_article': article_text,
        'similar_articles': []
    }

    for similar_article in similar_articles:
        same_issue_article_from_db = session.query(Article).filter(Article.id == article_id).first()
        if not same_issue_article_from_db:
            continue
        published_timestamp = dateutil.parser.isoparse(article['timestamp'])
        earliest_limit = published_timestamp - issue_span
        latest_limit = published_timestamp + issue_span
        if not earliest_limit <= same_issue_article_from_db.published_at <= latest_limit:
            continue
        first_two_paragraphs = session.query(Paragraph).filter(Paragraph.article_id == similar_article['id'], Paragraph.paragraph_num in [0, 1]).order_by(Paragraph.paragraph_num).all()
        same_issue_article_text = list(same_issue_article_from_db.title)
        for paragraph in first_two_paragraphs:
            paragraph_text = paragraph.paragraph_text
            same_issue_article_text.append(paragraph_text)
        same_issue_article_text = ' '.join(same_issue_article_text).strip()
        request_body['similar_articles'].append({'id': same_issue_article_from_db.id, 'article_text': same_issue_article_text})
    same_issue_article_ids = message_llm(article=request_body, assistant=assistant, client=openai_client)['ids']

    # Leave in only ids which LLM approved of
    result_same_issue_articles = []
    for similar_article in similar_articles:
        if similar_article['id'] in same_issue_article_ids:
            result_same_issue_articles.append(similar_article)

    return result_same_issue_articles


def categorize_articles(article: dict, openai_client: openai.OpenAI, assistant):
    article_text = [article['title']]
    article_text.extend(article['paragraphs'])
    article_text = {'article': ' '.join(article_text).strip()}
    categories = message_llm({'article_text': article_text}, assistant=assistant, client=openai_client)['ids']
    return categories





