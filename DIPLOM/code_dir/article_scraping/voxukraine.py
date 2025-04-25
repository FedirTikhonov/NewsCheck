import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import dateutil.parser
from espreso import month_verbal_to_num


def voxukraine_to_ISO(date: str):
    date_lst = date.split(sep=' ')
    day = date_lst[0]
    month = month_verbal_to_num(date_lst[1])
    year = date_lst[2]
    iso_format = f'{year}-{month}-{day}T00:00:00+03:00'
    return iso_format


def scrape_voxukraine(scraping_delay=24):
    page = requests.get("https://voxukraine.org/category/voks-informue")
    soup = BeautifulSoup(page.content, "html.parser")
    feed_list = soup.find("div", class_="posts-wrapper d-flex flex-column flex-md-row justify-content-between justify-content-lg-start flex-md-wrap")
    articles = feed_list.find_all("article", class_='post-info')
    article_data = []
    for article in articles:
        href = article.find('a')['href']
        time_tag = article.find('div', class_='post-info__date')
        time_text = time_tag.get_text().strip()
        timestamp = voxukraine_to_ISO(time_text)
        article_page = requests.get(href)
        soup = BeautifulSoup(article_page.content, "html.parser")
        title_tag = soup.find('h1', class_='underline underline--large item-title base-color')
        title = title_tag.get_text()
        paragraphs_list = []
        paragraph_content = soup.find('div', class_='content-wrapper')
        paragraphs = paragraph_content.find_all('p')
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
            print(timestamp)
            article_time = dateutil.parser.isoparse(timestamp)
            current_time = datetime.now(timezone.utc)
            one_hour_ago = current_time - timedelta(hours=scraping_delay)
            if article_time >= one_hour_ago:
                article_data.append({
                    'outlet': 'voxukraine',
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
    print(scrape_voxukraine())
