from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

# Import the shared Base
from . import Base


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(511))
    href = Column(String(1023))
    outlet = Column(String(255))
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))
    status = Column(String(31))

    # Relationships
    categories = relationship("FactcheckCategory", back_populates="article")
    sources = relationship("Source", back_populates="article")
    paragraphs = relationship("Paragraph", back_populates="article")
    metric = relationship("Metric", back_populates="article", uselist=False)
    recommended_by = relationship("RecommendedArticle",
                                  foreign_keys="RecommendedArticle.recommended_article_id",
                                  back_populates="recommended_article")
    recommendations = relationship("RecommendedArticle",
                                   foreign_keys="RecommendedArticle.source_article_id",
                                   back_populates="source_article")
    similar_to = relationship("SameIssueArticle",
                              foreign_keys="SameIssueArticle.similar_article_id",
                              back_populates="similar_article")
    main_articles = relationship("SameIssueArticle",
                                 foreign_keys="SameIssueArticle.main_article_id",
                                 back_populates="main_article")

    def add_paragraph(self, paragraph_text, paragraph_num=None):
        from .Paragraph import Paragraph  # Import here to avoid circular imports

        if paragraph_num is None:
            existing_count = len(self.paragraphs)
            paragraph_num = existing_count + 1

        paragraph = Paragraph(paragraph_text=paragraph_text, paragraph_num=paragraph_num, article_id=self.id)
        self.paragraphs.append(paragraph)
        return paragraph

    def add_source(self, source_href, source_num=None):
        from .Source import Source  # Import here to avoid circular imports

        if source_num is None:
            existing_count = len(self.sources)
            source_num = existing_count + 1

        source = Source(source_href=source_href, source_num=source_num, article_id=self.id)
        self.sources.append(source)
        return source

    def add_metric(self, metric: dict):
        from .Metric import Metric  # Import here to avoid circular imports

        metric = Metric(
            credibility_score=metric['credibility_score'],
            credibility_reason=metric['credibility_reason'],
            clickbaitness_score=metric['clickbaitness_score'],
            clickbaitness_reason=metric['clickbaitness_reason'],
            factuality_score=metric['factuality_score'],
            factuality_reason=metric['factuality_reason'],
            emotionality_score=metric['emotionality_score'],
            emotionality_reason=metric['emotionality_reason'],
            article_id=self.id
        )
        self.metric = metric
        return metric

    def mark_processed(self):
        self.status = 'processed'

    def add_recommendation(self, recommended_article_dict):
        from .RecommendedArticle import RecommendedArticle  # Import here to avoid circular imports

        recommendation_for_article = RecommendedArticle(
            last_updated=recommended_article_dict['last_updated'],
            recommended_article_id=recommended_article_dict['id'],
            similarity_score=recommended_article_dict['similarity_score'],
            source_article_id=self.id,
        )
        self.recommendations.append(recommendation_for_article)
        return recommendation_for_article

    def add_same_issue_article(self, same_issue_article_dict):
        from .SameIssueArticle import SameIssueArticle  # Import here to avoid circular imports

        original_article = SameIssueArticle(
            created_at=same_issue_article_dict['last_updated'],
            same_issue_article_id=same_issue_article_dict['id'],
            similarity_score=same_issue_article_dict['similarity_score'],
            main_article_id=self.id,
        )
        self.main_articles.append(original_article)
        return original_article


