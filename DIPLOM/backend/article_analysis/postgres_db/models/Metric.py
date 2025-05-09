from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


class Metric(Base):
    __tablename__ = 'metric'

    id = Column(Integer, primary_key=True)
    emotionality_score = Column(String(255))
    emotionality_reason = Column(String(1023))
    factuality_score = Column(SmallInteger)
    factuality_reason = Column(String(1023))
    credibility_score = Column(SmallInteger)
    credibility_reason = Column(String(1023))
    clickbaitness_score = Column(SmallInteger)
    clickbaitness_reason = Column(String(1023))
    article_id = Column(Integer, ForeignKey('article.id'))

    # Relationships
    article = relationship("Article", back_populates="metric")
