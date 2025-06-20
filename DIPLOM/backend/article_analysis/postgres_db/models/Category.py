from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(511))

    articles = relationship("FactcheckCategory", back_populates="category")
    weekly_stats = relationship("WeeklyStats", back_populates="categories")
