from celery_app import app

from analysis import (generate_analysis_for_news,
                      generate_analysis_for_fact_checkers,
                      update_recommendations,
                      create_weekly_stats,
                      create_weekly_report)
from article_scraping.scraping import scrape_news, scrape_fact_check_articles


@app.task
def news_analysis():
    print('Request for news analysis received')
    news_articles = [scrape_news(delay=0.25)]
    print('Scraping complete, beginning analysis')
    generate_analysis_for_news(news_articles)


@app.task
def fact_checkers_analysis():
    print('Request for fact check article analysis received')
    fact_checker_articles = [scrape_fact_check_articles(delay=48)]
    print('Scraping complete, beginning analysis')
    generate_analysis_for_fact_checkers(fact_checker_articles)


@app.task
def weekly_digest():
    print('Request for weekly digest analysis received')
    create_weekly_stats()
    create_weekly_report()

@app.task
def refresh_recommendations():
    print('Request for refresh recommendations analysis received')
    update_recommendations()

