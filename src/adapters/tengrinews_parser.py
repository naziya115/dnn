import requests
from bs4 import BeautifulSoup as bsoup

# requests and bs4 to requirmnts

url = 'https://tengrinews.kz'
links = set()
counter = 0

def get_all_todays_urls(url: str, links: set = set(), counter: int = 0):
    res = requests.get(url)
    doc = bsoup(res.text, 'html.parser')
    news = doc.find_all('div', {'class': 'main-news_top_item'})

    for i in news:
        part = str(i)
        doc_s = bsoup(part, 'html.parser')
        asd = doc_s.find('a', href=True)
        # print(asd)
        try:
            if 'kazakhstan_news' in asd['href']:
                link = 'https://tengrinews.kz' + asd['href']
                links.add(link)
                counter += 1
                get_all_todays_urls(link, links, counter)
        except:
            return
    return links


def get_article_text(link):
    res = requests.get(link)
    doc = bsoup(res.text, 'html.parser')
    article = doc.find('div', {'class': 'content_main_text'})
    # print(article)
    plain_text = ''

    doc = bsoup(str(article), 'html.parser')
    paragraphs = doc.find_all('p')
    for paragraph in paragraphs:
        for link in paragraph.find_all('a'):
            link.extract()

        for img in paragraph.find_all('img'):
            img.extract()

        plain_text += paragraph.get_text()

    text = plain_text.replace('\n', '')
    

    return text


def get_title(link):
    res = requests.get(link)
    doc = bsoup(res.text, 'html.parser')
    title = doc.find('h2', {'class': 'content_main_desc'})
    span = title.find('p')
    span.get_text()
    # print(span)
    text = title.get_text().replace('\n', '')
    return text

def parse_news_website():
    url = 'YOUR_NEWS_WEBSITE_URL'
    links = set()
    counter = 0
    get_all_todays_urls(url, links, counter)
    
    articles = []
    for link in links:
        title = get_title(link)
        content = get_article_text(link)
        theme_tags = ['TAG1', 'TAG2']
        article = {
            'title': title,
            'content': content,
            'theme_tags': theme_tags
        }
        articles.append(article)
    
    return articles

# print(get_all_todays_urls(url, links, counter))
# #
# print(links)
#
# text = get_article_text(next(iter(links)))
#
# print(text)

# print(get_title("https://tengrinews.kz/kazakhstan_news/prezident-prizval-biznesmenov-razvivat-selo-554161/"))
# print(get_article_text("https://tengrinews.kz/kazakhstan_news/prezident-prizval-biznesmenov-razvivat-selo-554161/"))
