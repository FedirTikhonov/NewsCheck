from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


class FactcheckCategory(Base):
    __tablename__ = 'factcheck_category'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    article_id = Column(Integer, ForeignKey('article.id'))

    # Relationships
    category = relationship("Category", back_populates="articles")
    article = relationship("Article", back_populates="categories")

    # Unique constraint
    __table_args__ = (UniqueConstraint('category_id', 'article_id'),)