from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

# Import the shared Base
from DIPLOM.backend.article_analysis.postgres_db.models import Base


class SameIssueArticle(Base):
    __tablename__ = 'same_issue_article'

    id = Column(Integer, primary_key=True)
    main_article_id = Column(Integer, ForeignKey('article.id'))
    same_issue_article_id = Column(Integer, ForeignKey('article.id'))
    similarity_score = Column(Float)
    created_at = Column(DateTime(timezone=True))

    # Relationships
    main_article = relationship("Article", foreign_keys=[main_article_id], back_populates="main_articles")
    similar_article = relationship("Article", foreign_keys=[same_issue_article_id], back_populates="similar_to")

    # Unique constraint
    __table_args__ = (UniqueConstraint('main_article_id', 'same_issue_article_id'),)


def find_same_issue_articles(article: dict,
                             article_id: int,
                             voyageai_client: voyageai.Client,
                             openai_client: openai.OpenAI,
                             assistant,
                             session: sqlalchemy.orm.session.Session,
                             issue_span=datetime.timedelta(hours=48),
                             create_vector=True):

    article_text = [article['title']]
    for paragraph_num, paragraph in enumerate(article['paragraphs']):
        if paragraph_num in [0, 1]:
            article_text.append(paragraph)
    article_text = ' '.join(article_text).strip()

    if create_vector:
        article_text_embeddings = voyageai_client.embed(
            texts=[article_text],
            model='voyage-3',
            output_dimension=EMBEDDING_DIM,
        ).embeddings

        # Insert article into milvus collection
        insert_article(postgres_id=article_id, embedding=article_text_embeddings[0], embedding_type='same_issue')
    else:
        article_text_embeddings = [retrieve_vector_by_ids(article_id, 'same_issue')]

    # Find similar article beginnings
    found_articles = similarity_search(article_text_embeddings, embedding_type='same_issue', top_k=20, threshold=0.2)

    similar_articles = []
    for found_article in found_articles:
        already_existing_ids = []
        for tmp_article in found_articles:
            already_existing_ids.append(tmp_article['postgres_id'])
        if article_id == found_article['postgres_id'] or found_article['postgres_id'] in already_existing_ids:
            continue
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
        same_issue_article_from_db = session.query(Article).filter(Article.id == similar_article['id']).first()
        if not same_issue_article_from_db:
            continue
        if isinstance(article['timestamp'], str):
            published_timestamp = dateutil.parser.isoparse(article['timestamp'])
        else:
            published_timestamp = article['timestamp']
        earliest_limit = published_timestamp - issue_span
        latest_limit = published_timestamp + issue_span
        if not earliest_limit <= same_issue_article_from_db.published_at <= latest_limit:
            continue

        first_two_paragraphs = session.query(Paragraph).filter(
            Paragraph.article_id == similar_article['id'],
            Paragraph.paragraph_num.in_([0, 1])
        ).order_by(Paragraph.paragraph_num).all()

        same_issue_article_text = [same_issue_article_from_db.title]

        for paragraph in first_two_paragraphs:
            paragraph_text = paragraph.paragraph_text
            same_issue_article_text.append(paragraph_text)

        same_issue_article_text = ' '.join(same_issue_article_text).strip()
        request_body['similar_articles'].append({'id': same_issue_article_from_db.id, 'article_text': same_issue_article_text})

    if len(request_body['similar_articles']) > 0:
        print(request_body)
        same_issue_article_ids = message_llm(article=request_body, assistant=assistant, client=openai_client)['ids']
        print(same_issue_article_ids)
        result_same_issue_articles = []
        for similar_article in similar_articles:
            if similar_article['id'] in same_issue_article_ids:
                result_same_issue_articles.append(similar_article)
        return result_same_issue_articles
    return []