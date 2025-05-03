import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import dateutil.parser
import time


def scrape_tsn(scraping_delay=0.25):
    links = ['https://tsn.ua/news', 'https://tsn.ua/news/page-2']
    article_hrefs = []
    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        feed_list = soup.find("ul", class_='l-entries l-entries--bordered')
        articles = feed_list.find_all("li", class_='l-entries__item')
        for article in articles:
            title_tag = article.find('h2')
            if title_tag is not None:
                href = title_tag.find('a')['href']
                timestamp = article.find('time', class_='text-current c-bar__link c-entry__time')['datetime']
                article_hrefs.append((href, timestamp))
    article_data = []
    for (href, timestamp) in article_hrefs:
        article_page = requests.get(href)
        soup = BeautifulSoup(article_page.content, "html.parser")
        title_tag = soup.find('h1', class_='c-entry__title c-title c-title--h1 font-bold')
        title = title_tag.get_text().replace('\xa0', ' ').strip()
        paragraphs_list = []
        main_content = soup.find('div', class_='c-prose c-post__inner')
        lead_div = soup.find_all('div', class_='c-entry__lead c-prose__lead')
        if lead_div:
            paragraphs_list.append(lead_div[0].find('p').get_text().replace('\xa0', ' '))
        paragraphs = main_content.find_all('p', recursive=False)
        sources = []
        for paragraph in paragraphs:
            text = paragraph.get_text()
            text = text.replace(' ', ' ').strip()
            text = text.replace('\xa0', ' ')
            if len(text) != 0 and not text.startswith('Читайте також'):
                paragraphs_list.append(text)
            links = paragraph.find_all('a')
            for link in links:
                source_url = link['href']
                if source_url:
                    sources.append(source_url)
        article_time = dateutil.parser.isoparse(timestamp)
        current_time = datetime.now(timezone.utc)
        one_hour_ago = current_time - timedelta(hours=scraping_delay)
        if article_time >= one_hour_ago:
            article_data.append({
                'outlet': 'tsn',
                'href': href,
                'timestamp': timestamp,
                'title': title,
                'paragraphs': paragraphs_list,
                'sources': sources
            })
        else:
            return article_data
    return article_data


if __name__ == "__main__":
    start = time.time()
    article_list = scrape_tsn(scraping_delay=0.25)
    for article in article_list:
        print(article['title'])
    end = time.time()
    print(end - start)
