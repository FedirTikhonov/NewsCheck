import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import dateutil.parser


def scrape_hromadske():
    page = requests.get("https://hromadske.ua/news")
    soup = BeautifulSoup(page.content, "html.parser")
    feed_list = soup.find("ul", class_='l-feed-list')
    articles = feed_list.find_all("article", class_='c-feed-item')
    article_hrefs = []
    for article in articles:
        href = article.find('a', class_="c-feed-item__link")['href']
        timestamp = article.find('time', class_='c-feed-item__time')['datetime']
        article_hrefs.append((href, timestamp))
    article_data = []
    for (href, timestamp) in article_hrefs:
        print(href, timestamp)
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
            with open(f'hromadske_articles/{article["timestamp"]}.json', 'w', encoding='utf-8') as f:
                json.dump(article, f, ensure_ascii=False, indent=4)
        # Implement the mechanism to check if the atricle has already been scraped


if __name__ == "__main__":
    scrape_hromadske()
