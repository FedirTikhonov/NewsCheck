from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class ArticleSchema(BaseModel):
    href: str
    title: str
    timestamp: str
    paragraphs: List[str]
    sources: List[str]


class Factuality(BaseModel):
    rating: int = Field(ge=1, le=5)
    explanation: str


class Emotionality(BaseModel):
    rating: Literal['нейтральна', 'дещо емоційна', 'дуже емоційна']
    explanation: str


class Credibility(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    explanation: str


class Clickbbaitness(BaseModel):
    rating: int = Field(..., ge=1, le=3)
    explanation: str


class MetricSchema(BaseModel):
    credibility_rating: Credibility
    emotionality_rating: Emotionality
    factuality_rating: Factuality
    clickbaitness_rating: Clickbbaitness


class MainArticleSchema(BaseModel):
    article_text: str


class SimilarArticleSchema(BaseModel):
    article_id: int
    article_text: str


class SameIssueArticleSchema(BaseModel):
    main_article: MainArticleSchema
    similar_articles: List[SimilarArticleSchema]


class SameIssueArticleResponseSchema(BaseModel):
    ids: List[int]


class CategoryResponseSchema(BaseModel):
    ids: List[int]
