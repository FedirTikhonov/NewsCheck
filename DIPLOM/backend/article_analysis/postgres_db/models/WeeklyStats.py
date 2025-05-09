from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


class WeeklyStats(Base):
    __tablename__ = 'weekly_stats'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category_num = Column(Integer)
    date = Column(Date)

    categories = relationship("Category", back_populates="weekly_stats")
