from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .Article import Article
from .Category import Category
from .FactCheckCategory import FactcheckCategory
from .Metric import Metric
from .Paragraph import Paragraph
from .RecommendedArticle import RecommendedArticle
from .SameIssueArticle import SameIssueArticle
from .Source import Source

__all__ = [
    'Article',
    'Category',
    'FactcheckCategory',
    'Metric',
    'Paragraph',
    'RecommendedArticle',
    'SameIssueArticle',
    'Source'
]
