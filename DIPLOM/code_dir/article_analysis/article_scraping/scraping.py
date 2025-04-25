from .espreso import scrape_espreso
from .hromadske import scrape_hromadske
from .radiosvoboda import scrape_radiosvoboda
from .tsn import scrape_tsn
from .unian import scrape_unian
from .voxukraine import scrape_voxukraine
from .stopfake import scrape_stopfake
import time


def scrape_news(verbose=False, return_values=True):
    all_articles = []
    scraping_time_start = time.time()
    articles_tsn = scrape_tsn()
    articles_hromadske = scrape_hromadske()
    articles_radiosvoboda = scrape_radiosvoboda()
    articles_unian = scrape_unian()
    articles_espreso = scrape_espreso()
    scraping_time_end = time.time()
    all_articles.extend(articles_tsn)
    all_articles.extend(articles_hromadske)
    all_articles.extend(articles_radiosvoboda)
    all_articles.extend(articles_unian)
    all_articles.extend(articles_espreso)
    time_taken = scraping_time_end - scraping_time_start
    if verbose:
        total_articles = len(all_articles)
        print(f'For the time span of 15 minutes found {total_articles} articles in {time_taken} seconds')
        print(f'Number of articles from hromadske: {len(articles_hromadske)}')
        print(f'Number of articles from radiosvoboda: {len(articles_radiosvoboda)}')
        print(f'Number of articles from unian: {len(articles_unian)}')
        print(f'Number of articles from espreso: {len(articles_espreso)}')
        print(f'Number of articles from tsn: {len(articles_tsn)}')
    if return_values:
        return all_articles
    else:
        return None


def scrape_factcheckers(verbose=False, return_values=True):
    all_articles = []
    scraping_time_start = time.time()
    articles_voxukraine = scrape_voxukraine()
    articles_stopfake = scrape_stopfake()
    scraping_time_end = time.time()
    all_articles.extend(articles_voxukraine)
    all_articles.extend(articles_stopfake)
    time_taken = scraping_time_end - scraping_time_start
    if verbose:
        total_articles = len(all_articles)
        print(f'For the time span of 24 hours found {total_articles} articles in {time_taken} seconds')
        print(f'Number of articles from VoxUkraine: {len(articles_voxukraine)}')
        print(f'Number of articles from StopFake articles: {len(articles_stopfake)}')
    if return_values:
        return all_articles
    else:
        return None


if __name__ == "__main__":
    scrape_news(verbose=True, return_values=False)
