from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .Article import Article
from .Category import Category
from .FactCheckCategory import FactcheckCategory
from .Metric import Metric
from .Paragraph import Paragraph
from .RecommendedArticle import RecommendedArticle
from .Source import Source
from .WeeklyStats import WeeklyStats
from .WeeklyReport import WeeklyReport


__all__ = [
    'Article',
    'Category',
    'FactcheckCategory',
    'Metric',
    'Paragraph',
    'RecommendedArticle',
    'Source',
    'WeeklyReport',
    'WeeklyStats'
]
