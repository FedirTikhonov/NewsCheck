import openai
import sqlalchemy.orm.session
import voyageai
import datetime
import dateutil.parser

from DIPLOM.backend.article_analysis.milvus_db.utils import similarity_search, insert_article, retrieve_vector_by_ids
from DIPLOM.backend.article_analysis.postgres_db.models.Article import Article
from DIPLOM.backend.article_analysis.postgres_db.models.Paragraph import Paragraph
from DIPLOM.backend.article_analysis.utils.llm_requests import message_llm

EMBEDDING_DIM = 1024


def generate_recommendations(article: dict, article_id: int, voyageai_client: voyageai.Client, create_vector=True):
    if create_vector:
        article_text = [article['title']]
        article_text.extend(article['paragraphs'])
        article_text = ' '.join(article_text)

        article_text_embeddings = voyageai_client.embed(
            texts=[article_text],
            model='voyage-3',
            output_dimension=EMBEDDING_DIM,
        ).embeddings

        insert_article(postgres_id=article_id, embedding=article_text_embeddings[0])

    else:
        article_text_embeddings = [retrieve_vector_by_ids(article_id)]

    found_articles = similarity_search(article_text_embeddings)
    recommended_articles = []
    for found_article in found_articles:
        if article_id == found_article['postgres_id']:
            continue
        recommended_article = {
            'last_updated': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            'id': found_article['postgres_id'],
            'similarity_score': found_article['similarity_score']
        }
        recommended_articles.append(recommended_article)

    return recommended_articles


def categorize_articles(article: dict, openai_client: openai.OpenAI, assistant):
    article_text = [article['title']]
    article_text.extend(article['paragraphs'])
    article_text = {'article': ' '.join(article_text).strip()}
    categories = message_llm({'article_text': article_text}, assistant=assistant, client=openai_client, verbose=True)['ids']
    return categories





