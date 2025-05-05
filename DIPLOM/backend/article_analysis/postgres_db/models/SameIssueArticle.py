from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


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
