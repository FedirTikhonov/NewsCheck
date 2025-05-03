import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import dateutil.parser


def scrape_stopfake(scraping_delay=48):
    page = requests.get("https://www.stopfake.org/uk/category/context-ua/")
    soup = BeautifulSoup(page.content, "html.parser")
    feed_list = soup.find("div", class_='td-ss-main-content')
    articles = feed_list.find_all("div", class_='td_module_10 td_module_wrap td-animation-stack')
    article_data = []
    for article in articles:
        href = article.find('a')['href']
        timestamp = article.find('time', class_='entry-date updated td-module-date')['datetime']
        article_page = requests.get(href)
        soup = BeautifulSoup(article_page.content, "html.parser")
        title_tag = soup.find('h1', class_='entry-title')
        title = title_tag.get_text().replace('\xa0', ' ').strip()
        paragraphs_list = []
        paragraph_content = soup.find('div', class_='td-post-content tagdiv-type')
        paragraphs = paragraph_content.find_all('p')
        sources = []
        for paragraph in paragraphs:
            text = paragraph.get_text()
            text = text.replace(' ', ' ')
            text = text.replace('\xa0', ' ')
            paragraphs_list.append(text)
            links = paragraph.find_all('a')
            for link in links:
                source_url = link['href']
                if source_url:
                    sources.append(source_url)
        if href is not None and timestamp is not None and title is not None and paragraphs_list is not None and sources is not None:
            article_time = dateutil.parser.isoparse(timestamp)
            current_time = datetime.now(timezone.utc)
            one_hour_ago = current_time - timedelta(hours=scraping_delay)
            if article_time >= one_hour_ago:
                article_data.append({
                    'outlet': 'stopfake',
                    'href': href,
                    'timestamp': timestamp,
                    'title': title,
                    'paragraphs': paragraphs_list,
                    'sources': sources
                })
            else:
                return article_data


if __name__ == "__main__":
    articles = scrape_stopfake(scraping_delay=10000)
    with open('stopfake.json', 'w') as outfile:
        json.dump(articles, outfile)
