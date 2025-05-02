import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import dateutil.parser
import time


def convert_to_iso(timestamp):
    time_part, date_part = timestamp.split(", ")
    hours, minutes = time_part.split(":")
    day, month, year = date_part.split(".")
    dt = datetime(
        int(year),
        int(month),
        int(day),
        int(hours),
        int(minutes)
    )
    return dt.strftime("%Y-%m-%dT%H:%M:00+03:00")


def scrape_unian(scraping_delay=0.25):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    os.environ['PATH'] += "/Users/ted/Documents/chrome-mac-arm64"
    driver = Chrome(options=chrome_options)
    driver.get('https://www.unian.ua/detail/all_news')
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(2)
    articles = driver.execute_script("""
        return document.querySelectorAll('.list-thumbs__item');
    """)
    article_hrefs = []
    for article in articles:
        soup = BeautifulSoup(article.get_attribute('outerHTML'), 'html.parser')
        article_info = soup.find('div', class_='list-thumbs__info')
        timestamp = convert_to_iso(article_info.find('div', class_='list-thumbs__time time').get_text())
        href = article_info.find('a')['href']
        article_hrefs.append((href, timestamp))
    article_data = []
    for (href, timestamp) in article_hrefs:
        driver.get(href)
        article = driver.find_element(by=By.CLASS_NAME, value='article')
        soup = BeautifulSoup(article.get_attribute('outerHTML'), 'html.parser')
        title_tag = soup.find('h1')
        title = title_tag.get_text().replace('\xa0', ' ').strip()
        paragraphs_list = []
        paragraphs = soup.find_all('p')
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
        if href is not None and timestamp is not None and title is not None and paragraphs_list is not None and sources is not None:
            paragraphs_list.remove(paragraphs_list[0])
            article_time = dateutil.parser.isoparse(timestamp)
            current_time = datetime.now(timezone.utc)
            one_hour_ago = current_time - timedelta(hours=scraping_delay)
            if article_time >= one_hour_ago:
                article_data.append({
                    'outlet': 'unian',
                    'href': href,
                    'timestamp': timestamp,
                    'title': title,
                    'paragraphs': paragraphs_list,
                    'sources': sources
                })
            else:
                return article_data


if __name__ == "__main__":
    start = time.time()
    article_list = scrape_unian()
    for article in article_list:
        print(article['timestamp'])
    end = time.time()
    print(end - start)

