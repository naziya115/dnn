import requests
from bs4 import BeautifulSoup as bsoup
import time
from urllib.parse import urljoin

url = "https://www.bbc.com/news/world"


def get_all_links(url: str):
    links = set()
    res = requests.get(url)
    doc = bsoup(res.text, 'html.parser')
    section = doc.find('div', {'data-testid': 'virginia-section-7'})
    if section:
        a_tags = section.find_all('a', href=True)
        for a_tag in a_tags:
            links.add('https://www.bbc.com' + a_tag['href'])
    return links


def get_article_text(link):
    res = requests.get(link)
    doc = bsoup(res.text, 'html.parser')
    text_blocks = doc.find_all('div', {'data-component': 'text-block'})
    article_text = ''
    for block in text_blocks:
        paragraphs = block.find_all('p')
        for p in paragraphs:
            article_text += p.get_text(strip=True)
    return article_text


def get_title(link):
    res = requests.get(link)
    doc = bsoup(res.text, 'html.parser')
    title = doc.find('h1', {'class': 'sc-518485e5-0 bWszMR'})
    if title:
        return title.text
    return None


def get_image(link):
    res = requests.get(link)
    doc = bsoup(res.text, 'html.parser')
    img_tag = doc.find('img', srcset=True)
    srcset = img_tag.get('srcset')
    if srcset:
        srcset_urls = [(url.split()[0], int(url.split()[1][:-1])) for url in srcset.split(',')]
        largest_image_url = max(srcset_urls, key=lambda x: x[1])[0]
        return urljoin(link, largest_image_url)
    else:
        print("No srcset found, using src.")
        return img_tag['src']

# links = get_all_links(url)
# for link in links:
#     print(f"Fetching article from {link}...")
#     article_text = get_article_text(link)
#     print(get_title(link))
#     print()
#     img = get_image(link)
#     print(img)
#     print()
#     if article_text:
#         print(article_text)
#     else:
#         print("Failed to fetch article text.")
#     time.sleep(2)