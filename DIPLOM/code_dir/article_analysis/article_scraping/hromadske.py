import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import dateutil.parser


def scrape_hromadske(scraping_delay=0.25):
    page = requests.get("https://hromadske.ua/news")
    soup = BeautifulSoup(page.content, "html.parser")
    feed_list = soup.find("ul", class_='l-feed-list')
    articles = feed_list.find_all("article", class_='c-feed-item')
    article_data = []
    for article in articles:
        href = article.find('a', class_="c-feed-item__link")['href']
        timestamp = article.find('time', class_='c-feed-item__time')['datetime']
        article_page = requests.get(href)
        soup = BeautifulSoup(article_page.content, "html.parser")
        title_tag = soup.find('h1', class_='c-heading__title')
        title = title_tag.get_text()
        paragraphs_list = []
        s_content = soup.find('div', class_='s-content')
        lead_div = s_content.find_all('div', class_='o-lead')
        paragraphs_list.append(lead_div[0].find('p').get_text())
        paragraphs = s_content.find_all('p', class_='text-start')
        sources = []
        for paragraph in paragraphs:
            text = paragraph.get_text()
            text = text.replace(' ', ' ')
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
                    'outlet': 'hromadske',
                    'href': href,
                    'timestamp': timestamp,
                    'title': title,
                    'paragraphs': paragraphs_list,
                    'sources': sources
                })
            else:
                return article_data
        # Implement the mechanism to check if the atricle has already been scraped


if __name__ == "__main__":
    print(scrape_hromadske())
