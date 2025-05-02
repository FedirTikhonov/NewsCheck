from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import dateutil.parser
import time


def scrape_radiosvoboda(scraping_delay=0.25):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Recommended for headless
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size`
    os.environ['PATH'] += "/Users/ted/Documents/chrome-mac-arm64"
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.radiosvoboda.org/z/630")
    feed_list = driver.find_element(by=By.CSS_SELECTOR, value='.archive-list')
    feed_list_html = feed_list.get_attribute('outerHTML')
    soup = BeautifulSoup(feed_list_html, 'html.parser')
    articles_previews = soup.find_all(class_='mb-grid archive-list__item')
    article_hrefs = []
    for article_content_item in articles_previews:
        href = article_content_item.find('a')['href']
        href = 'https://www.radiosvoboda.org' + href
        article_hrefs.append(href)
    article_data = []
    for href in article_hrefs:
        article_page = requests.get(href)
        soup = BeautifulSoup(article_page.content, 'html.parser')
        title = soup.find('h1', class_='title pg-title').get_text().replace('\xa0', ' ').strip()
        timestamp = soup.find('time')['datetime']
        paragraphs_tags = []
        article_section = soup.find('div', class_='wsw')
        paragraphs = article_section.find_all('p')
        paragraphs_tags.extend(paragraphs)
        sources = []
        paragraphs_text = []
        for paragraph in paragraphs_tags:
            text = paragraph.get_text()
            text = text.replace(' ', ' ').strip()
            text = text.replace('\xa0', ' ')
            if len(text) != 0:
                paragraphs_text.append(text)
            links = paragraph.find_all('a')
            for link in links:
                source_url = link['href']
                if source_url:
                    sources.append(source_url)
        if href is not None and timestamp is not None and title is not None and paragraphs_text is not None and sources is not None:
            article_time = dateutil.parser.isoparse(timestamp)
            current_time = datetime.now(timezone.utc)
            one_hour_ago = current_time - timedelta(hours=scraping_delay)
            if article_time >= one_hour_ago:
                article_data.append({
                    'outlet': 'radiosvoboda',
                    'href': href,
                    'timestamp': timestamp,
                    'title': title,
                    'paragraphs': paragraphs_text,
                    'sources': sources
                })
            else:
                return article_data
    # Implement the mechanism to check if the atricle has already been scraped


if __name__ == "__main__":
    start = time.time()
    article_list = scrape_radiosvoboda(scraping_delay=0.25)
    for article in article_list:
        print(article['timestamp'])
    end = time.time()
    print(end - start)
