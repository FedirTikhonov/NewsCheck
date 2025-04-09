import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import dateutil.parser


def scrape_tsn():
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
        title = title_tag.get_text()
        paragraphs_list = []
        main_content = soup.find('div', class_='c-prose c-post__inner')
        lead_div = soup.find_all('div', class_='c-entry__lead c-prose__lead')
        paragraphs_list.append(lead_div[0].find('p').get_text())
        paragraphs = main_content.find_all('p', recursive=False)
        sources = []
        for paragraph in paragraphs:
            text = paragraph.get_text()
            text = text.replace(' ', ' ').strip()
            if len(text) != 0 and not text.startswith('Читайте також'):
                paragraphs_list.append(text)
            links = paragraph.find_all('a')
            for link in links:
                source_url = link['href']
                if source_url:
                    sources.append(source_url)
        if href is not None and timestamp is not None and title is not None and paragraphs_list is not None and sources is not None:
            article_data.append({
                'href': href,
                'timestamp': timestamp,
                'title': title,
                'paragraphs': paragraphs_list,
                'sources': sources
            })
    for article in article_data:
        timestamp = article['timestamp']
        article_time = dateutil.parser.isoparse(timestamp)
        current_time = datetime.now(timezone.utc)
        one_hour_ago = current_time - timedelta(hours=1)
        if article_time >= one_hour_ago:
            with open(f'tsn_articles/{article["timestamp"]}.json', 'w', encoding='utf-8') as f:
                json.dump(article, f, ensure_ascii=False, indent=4)
        # Implement the mechanism to check if the atricle has already been scraped


if __name__ == "__main__":
    scrape_tsn()
