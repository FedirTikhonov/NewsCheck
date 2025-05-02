from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


class Source(Base):
    __tablename__ = 'source'

    id = Column(Integer, primary_key=True)
    source_href = Column(String(1023))
    source_num = Column(SmallInteger)
    article_id = Column(Integer, ForeignKey('article.id'))

    # Relationships
    article = relationship("Article", back_populates="sources")