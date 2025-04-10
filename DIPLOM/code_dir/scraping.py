from article_scraping.espreso import scrape_espreso
from article_scraping.hromadske import scrape_hromadske
from article_scraping.radiosvoboda import scrape_radiosvoboda
from article_scraping.tsn import scrape_tsn
from article_scraping.unian import scrape_unian
import time


def test_scraping():
    scraping_time_start = time.time()
    articles_tsn = scrape_tsn()
    articles_hromadske = scrape_hromadske()
    articles_radiosvoboda = scrape_radiosvoboda()
    articles_unian = scrape_unian()
    articles_espreso = scrape_espreso()
    scraping_time_end = time.time()
    time_taken = scraping_time_end - scraping_time_start
    total_articles = len(articles_tsn) + len(articles_hromadske) + len(articles_radiosvoboda) + len(articles_unian) + len(articles_espreso)
    print(f'For the time span of 15 minutes found {total_articles} articles in {time_taken} seconds')
    print(f'Number of articles from hromadske: {len(articles_hromadske)}')
    print(f'Number of articles from radiosvoboda: {len(articles_radiosvoboda)}')
    print(f'Number of articles from unian: {len(articles_unian)}')
    print(f'Number of articles from espreso: {len(articles_espreso)}')
    print(f'Number of articles from tsn: {len(articles_tsn)}')


if __name__ == "__main__":
    test_scraping()
