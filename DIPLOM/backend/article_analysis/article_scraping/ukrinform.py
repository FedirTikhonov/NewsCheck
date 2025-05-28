import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import dateutil.parser
import time


def scrape_ukrinform(scraping_delay=0.25):
    article_hrefs = []
    page = requests.get('https://www.ukrinform.ua/block-lastnews')
    soup = BeautifulSoup(page.content, "html.parser")
    feed_list = soup.find_all("article")
    for article in feed_list:
        title_tag = article.find('h2')
        if title_tag is not None:
            href = title_tag.find('a')['href']
            timestamp = article.find('time')['datetime']
            title = article.find('h2').get_text()
            if not href.startswith('\thttp'):
                article_hrefs.append((f'https://www.ukrinform.ua{href}', timestamp, title))
    article_data = []
    for (href, timestamp, title) in article_hrefs:
        article_page = requests.get(href)
        if article_page.status_code == 404:
            continue
        soup = BeautifulSoup(article_page.content, "html.parser")
        paragraphs_list = []
        main_content = soup.find('div', class_='newsText')
        lead_div = soup.find_all('div', class_='newsHeading')
        if lead_div:
            paragraphs_list.append(lead_div[0].get_text().replace('\xa0', ' '))
        paragraphs = main_content.find_all('p', recursive=True)
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
                'outlet': 'ukrinform',
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
    print(scrape_ukrinform(scraping_delay=0.5))
