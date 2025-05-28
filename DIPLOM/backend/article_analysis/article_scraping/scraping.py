from .espreso import scrape_espreso
from .hromadske import scrape_hromadske
from .radiosvoboda import scrape_radiosvoboda
from .voxukraine import scrape_voxukraine
from .stopfake import scrape_stopfake
from .ukrinform import scrape_ukrinform
import time


def scrape_news(verbose=False, return_values=True, delay=0.25):
    all_articles = []
    scraping_time_start = time.time()
    try:
        articles_ukrinform = scrape_ukrinform(scraping_delay=delay)
        all_articles.extend(articles_ukrinform)
        if verbose:
            print(f'Number of articles from ukrinform: {len(articles_ukrinform)}')
    except Exception as e:
        print('Failed to execute ukrinform scraping function')
    try:
        articles_hromadske = scrape_hromadske(scraping_delay=delay)
        all_articles.extend(articles_hromadske)
        if verbose:
            print(f'Number of articles from hromadske {len(articles_hromadske)}')
    except Exception as e:
        print('Failed to execute hromadske scraping function')
    try:
        articles_radiosvoboda = scrape_radiosvoboda(scraping_delay=delay)
        all_articles.extend(articles_radiosvoboda)
        if verbose:
            print(f'Number of articles from radiosvoboda: {len(articles_radiosvoboda)}')
    except Exception as e:
        print('Failed to execute radiosvoboda scraping function')
    try:
        articles_espreso = scrape_espreso(scraping_delay=1)
        all_articles.extend(articles_espreso)
        if verbose:
            print(f'Number of articles from espreso: {len(articles_espreso)}')
    except Exception as e:
        print('Failed to execute espreso scraping function')
    scraping_time_end = time.time()
    time_taken = scraping_time_end - scraping_time_start
    if verbose:
        total_articles = len(all_articles)
        print(f'For the time span of 15 minutes found {total_articles} articles in {time_taken} seconds')
    if return_values:
        return all_articles
    else:
        return None


def scrape_fact_check_articles(verbose=False, return_values=True, delay=48):
    all_articles = []
    scraping_time_start = time.time()
    try:
        articles_voxukraine = scrape_voxukraine(scraping_delay=delay)
        all_articles.extend(articles_voxukraine)
        print(f'Number of articles from VoxUkraine: {len(articles_voxukraine)}')
    except Exception as e:
        print('Failed to execute a voxukraine scraping function')
    try:
        articles_stopfake = scrape_stopfake(scraping_delay=delay)
        all_articles.extend(articles_stopfake)
        if verbose:
            print(f'Number of articles from StopFake: {len(articles_stopfake)}')
    except Exception as e:
        print('Failed to execute a stopfake scraping function')
    scraping_time_end = time.time()

    time_taken = scraping_time_end - scraping_time_start
    if verbose:
        total_articles = len(all_articles)
        print(f'For the time span of 15 minutes found {total_articles} articles in {time_taken} seconds')
    if return_values:
        return all_articles
    else:
        return None


if __name__ == "__main__":
    print(len(scrape_fact_check_articles(delay=10000)))
