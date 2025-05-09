from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import dateutil.parser
import time


def month_verbal_to_num(month: str):
    if month == 'січня':
        month = '01'
    elif month == 'лютого':
        month = '02'
    elif month == 'березня':
        month = '03'
    elif month == 'квітня':
        month = '04'
    elif month == 'травня':
        month = '05'
    elif month == 'червня':
        month = '06'
    elif month == 'липня':
        month = '07'
    elif month == 'серпня':
        month = '08'
    elif month == 'вересня':
        month = '09'
    elif month == 'жовтня':
        month = '10'
    elif month == 'листопада':
        month = '11'
    elif month == 'грудня':
        month = '12'
    return month


def espreso_to_ISO(date: str):
    date = date.split(sep=' ')
    date.remove(date[3])
    day = date[0].zfill(2)
    month = month_verbal_to_num(date[1])
    year = date[2]
    time = date[3]
    iso_format = f'{year}-{month}-{day}T{time}:00+03:00'
    return iso_format


def scrape_espreso(scraping_delay=0.25):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Recommended for headless
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size`
    os.environ['PATH'] += "/Users/ted/Documents/chrome-mac-arm64"
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://espreso.tv/news")
    feed_list = driver.find_element(by=webdriver.common.by.By.CLASS_NAME, value='news_page_similar_content__items')
    feed_list = feed_list.find_elements(By.CLASS_NAME, 'news_page_similar_content__item')
    article_hrefs = []
    for article_content_item in feed_list:
        wrapper = article_content_item.find_element(By.CLASS_NAME, 'news_page_similar_content_item__wrapper')
        title_tag = wrapper.find_element(By.CLASS_NAME, 'title')
        href = title_tag.find_element(By.TAG_NAME, 'a').get_attribute('href')
        article_hrefs.append(href)
    article_data = []
    for href in article_hrefs:
        driver.get(href)
        body = driver.find_element(By.TAG_NAME, 'body')
        header_section = body.find_element(By.CLASS_NAME, 'header_current_article')
        title = header_section.find_element(By.CLASS_NAME, 'text-title').text.replace('\xa0', ' ').strip()
        time_tag = header_section.find_element(By.CLASS_NAME, 'news__author_date')
        date = time_tag.find_element(By.CLASS_NAME, 'news__author_date__date').text
        time = time_tag.find_element(By.CLASS_NAME, 'news__author_date__time').text
        timestamp = date + ' ' + time
        timestamp = timestamp.replace(',', '')
        timestamp = espreso_to_ISO(timestamp)
        paragraphs_tags = []
        article_section = body.find_element(By.CLASS_NAME, 'content_current_article')
        paragraphs_tags.append(article_section.find_element(By.TAG_NAME, 'h2'))
        li_paragraphs = article_section.find_elements(By.TAG_NAME, 'li')
        paragraphs_tags.extend(li_paragraphs)
        news_content = article_section.find_element(By.CLASS_NAME, 'news-content')
        paragraphs = news_content.find_elements(By.TAG_NAME, 'p')
        paragraphs_tags.extend(paragraphs)
        sources = []
        paragraphs_text = []
        exception_texts = ["This is a modal window.",
                           "Beginning of dialog window. Escape will cancel and close the window.",
                           "End of dialog window.",
                           "Chapters",
                           "descriptions off, selected",
                           "subtitles settings, opens subtitles settings dialog",
                           "subtitles off, selected",
                           ]
        for paragraph in paragraphs_tags:
            html = paragraph.get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            text = text.replace(' ', ' ').strip()
            text = text.replace('\xa0', ' ')
            if text not in exception_texts and not text.startswith('Читайте також:') and len(text) != 0:
                paragraphs_text.append(text)
            try:
                links = paragraph.find_elements(By.TAG_NAME, 'a')
                for link in links:
                    source_url = link.get_attribute('href')
                    if source_url:
                        sources.append(source_url)
            except Exception as e:
                pass
        if href is not None and timestamp is not None and title is not None and paragraphs_text is not None and sources is not None:
            article_time = dateutil.parser.isoparse(timestamp)
            current_time = datetime.now(timezone.utc)
            one_hour_ago = current_time - timedelta(hours=scraping_delay)
            if article_time >= one_hour_ago:
                article_data.append({
                    'outlet': 'espreso',
                    'href': href,
                    'timestamp': timestamp,
                    'title': title,
                    'paragraphs': paragraphs_text,
                    'sources': sources
                })
            else:
                return article_data


if __name__ == "__main__":
    start = time.time()
    print(scrape_espreso(scraping_delay=0.25))
    end = time.time()
    print(end - start)
