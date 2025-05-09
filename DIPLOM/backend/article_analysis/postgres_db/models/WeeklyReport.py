from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, Date, Text
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


class WeeklyReport(Base):
    __tablename__ = 'weekly_report'

    id = Column(Integer, primary_key=True)
    digest_text = Column(Text)
    digest_date = Column(Date)

