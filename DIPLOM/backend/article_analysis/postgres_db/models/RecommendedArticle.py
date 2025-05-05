from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


class RecommendedArticle(Base):
    __tablename__ = 'recommended_article'

    id = Column(Integer, primary_key=True)
    source_article_id = Column(Integer, ForeignKey('article.id'))
    recommended_article_id = Column(Integer, ForeignKey('article.id'))
    similarity_score = Column(Float)
    last_updated = Column(DateTime(timezone=True))

    # Relationships
    source_article = relationship("Article", foreign_keys=[source_article_id], back_populates="recommendations")
    recommended_article = relationship("Article", foreign_keys=[recommended_article_id], back_populates="recommended_by")

    # Unique constraint
    __table_args__ = (UniqueConstraint('source_article_id', 'recommended_article_id'),)