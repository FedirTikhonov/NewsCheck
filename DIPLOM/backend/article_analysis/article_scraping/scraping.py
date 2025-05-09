from DIPLOM.backend.article_analysis.article_scraping.espreso import scrape_espreso
from .hromadske import scrape_hromadske
from .radiosvoboda import scrape_radiosvoboda
from .voxukraine import scrape_voxukraine
from .stopfake import scrape_stopfake
from .ukrinform import scrape_ukrinform
import time


def scrape_news(verbose=False, return_values=True, delay=0.25):
    all_articles = []
    scraping_time_start = time.time()
    articles_ukrinform = scrape_ukrinform(scraping_delay=delay)
    articles_hromadske = scrape_hromadske(scraping_delay=delay)
    articles_radiosvoboda = scrape_radiosvoboda(scraping_delay=delay)
    articles_espreso = scrape_espreso(scraping_delay=delay)
    scraping_time_end = time.time()

    all_articles.extend(articles_ukrinform)
    all_articles.extend(articles_hromadske)
    all_articles.extend(articles_radiosvoboda)
    all_articles.extend(articles_espreso)

    time_taken = scraping_time_end - scraping_time_start
    if verbose:
        total_articles = len(all_articles)
        print(f'For the time span of 15 minutes found {total_articles} articles in {time_taken} seconds')
        print(f'Number of articles from hromadske: {len(articles_hromadske)}')
        print(f'Number of articles from radiosvoboda: {len(articles_radiosvoboda)}')
        print(f'Number of articles from espreso: {len(articles_espreso)}')
        print(f'Number of articles from ukrinform: {len(articles_ukrinform)}')
    if return_values:
        return all_articles
    else:
        return None


def scrape_fact_check_articles(verbose=False, return_values=True, delay=48):
    all_articles = []
    scraping_time_start = time.time()
    articles_voxukraine = scrape_voxukraine(scraping_delay=delay)
    articles_stopfake = scrape_stopfake(scraping_delay=delay)
    scraping_time_end = time.time()
    print(articles_voxukraine)
    print(articles_stopfake)

    all_articles.extend(articles_voxukraine)
    all_articles.extend(articles_stopfake)

    time_taken = scraping_time_end - scraping_time_start
    if verbose:
        total_articles = len(all_articles)
        print(f'For the time span of 15 minutes found {total_articles} articles in {time_taken} seconds')
        print(f'Number of articles from VoxUkraine: {len(articles_voxukraine)}')
        print(f'Number of articles from StopFake articles: {len(articles_stopfake)}')
    if return_values:
        return all_articles
    else:
        return None


if __name__ == "__main__":
    scrape_news(verbose=True, return_values=False)
