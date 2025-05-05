from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


class Paragraph(Base):
    __tablename__ = 'paragraph'

    id = Column(Integer, primary_key=True)
    paragraph_text = Column(String(1023))
    paragraph_num = Column(SmallInteger)
    article_id = Column(Integer, ForeignKey('article.id'))

    # Relationships
    article = relationship("Article", back_populates="paragraphs")