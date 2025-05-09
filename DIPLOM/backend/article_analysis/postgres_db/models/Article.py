from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session

# Import the shared Base
from . import Base


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(511))
    href = Column(String(1023))
    outlet = Column(String(255))
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))
    status = Column(String(31))

    # Relationships
    categories = relationship("FactcheckCategory", back_populates="article")
    sources = relationship("Source", back_populates="article")
    paragraphs = relationship("Paragraph", back_populates="article")
    metric = relationship("Metric", back_populates="article", uselist=False)
    recommended_by = relationship("RecommendedArticle",
                                  foreign_keys="RecommendedArticle.recommended_article_id",
                                  back_populates="recommended_article")
    recommendations = relationship("RecommendedArticle",
                                   foreign_keys="RecommendedArticle.source_article_id",
                                   back_populates="source_article")

    def add_paragraph(self, paragraph_text, paragraph_num=None):
        from .Paragraph import Paragraph

        if paragraph_num is None:
            existing_count = len(self.paragraphs)
            paragraph_num = existing_count + 1
        if not paragraph_text.startswith('https'):
            paragraph = Paragraph(paragraph_text=paragraph_text, paragraph_num=paragraph_num, article_id=self.id)
            self.paragraphs.append(paragraph)
            return paragraph

    def add_source(self, source_href, source_num=None):
        from .Source import Source

        if source_num is None:
            existing_count = len(self.sources)
            source_num = existing_count + 1

        source = Source(source_href=source_href, source_num=source_num, article_id=self.id)
        self.sources.append(source)
        return source

    def add_metric(self, metric: dict):
        from .Metric import Metric  # Import here to avoid circular imports

        metric = Metric(
            credibility_score=metric['credibility_rating']['rating'],
            credibility_reason=metric['credibility_rating']['explanation'],
            clickbaitness_score=metric['clickbaitness_rating']['rating'],
            clickbaitness_reason=metric['clickbaitness_rating']['explanation'],
            factuality_score=metric['factuality_rating']['rating'],
            factuality_reason=metric['factuality_rating']['explanation'],
            emotionality_score=metric['emotionality_rating']['rating'],
            emotionality_reason=metric['emotionality_rating']['explanation'],
            article_id=self.id
        )
        self.metric = metric
        return metric

    def mark_processed(self):
        self.status = 'processed'

    def mark_processing(self):
        self.status = 'processing'

    def add_recommendation(self, recommended_article_dict):
        from .RecommendedArticle import RecommendedArticle
        session = Session.object_session(self)
        existing = session.query(RecommendedArticle).filter(
            RecommendedArticle.source_article_id == self.id,
            RecommendedArticle.recommended_article_id == recommended_article_dict['id']
        ).first()

        if existing:
            existing.similarity_score = recommended_article_dict['similarity_score']
            existing.last_updated = recommended_article_dict['last_updated']
            return existing

        recommendation_for_article = RecommendedArticle(
            last_updated=recommended_article_dict['last_updated'],
            recommended_article_id=recommended_article_dict['id'],
            similarity_score=recommended_article_dict['similarity_score'],
            source_article_id=self.id,
        )
        self.recommendations.append(recommendation_for_article)
        return recommendation_for_article

    def add_factcheck_category(self, category_id: int):
        from .FactCheckCategory import FactcheckCategory

        factcheck_category = FactcheckCategory(
            category_id=category_id,
            article_id=self.id,
        )

        self.categories.append(factcheck_category)

    def remove_recommendations(self):
        from sqlalchemy.orm import Session
        from .RecommendedArticle import RecommendedArticle

        session = Session.object_session(self)
        if session:
            session.query(RecommendedArticle).filter(RecommendedArticle.source_article_id == self.id).delete(synchronize_session='fetch')
            session.expire(self, ['recommendations'])
