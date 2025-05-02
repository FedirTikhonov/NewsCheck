from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(511))

    # Relationships
    articles = relationship("FactcheckCategory", back_populates="category")