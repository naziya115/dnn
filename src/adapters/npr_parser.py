import requests
from bs4 import BeautifulSoup

url = "https://www.npr.org/"
    

def get_links(url: str) -> list:
    try:
        response = requests.get(url)
        response.raise_for_status()  
        html_content = response.text
        print(response)
        
        soup = BeautifulSoup(html_content, "html.parser")
        
        articles = []
        links = set()
        for article in soup.find_all("article"):
            # title_tag = article.find("h3")
            link_tag = article.find("a", href=True)
            # teaser_tag = article.find("p")

            # title = title_tag.text.strip() if title_tag else "No title available"
            link = f"{link_tag['href']}" if link_tag else "No URL available"
            # teaser = teaser_tag.text.strip() if teaser_tag else "No summary available"

            if link not in links: 
                articles.append(link)
                links.add(link)

        return articles

    except requests.RequestException as e:
        print(f"Error with links NPR: {e}")
        return []


def get_text(article_url: str) -> list:
    try:
        response = requests.get(article_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("h1", class_="title")
        title = title_tag.text.strip() if title_tag else "No title available"

        main_image = None
        temp = soup.find("div", class_='imagewrap has-source-dimensions')
        image_tag = temp.find("img", class_="img")  # Adjust class based on NPR's structure
        if image_tag and image_tag.get("src"):
            main_image = image_tag["src"]


        paragraphs = [p.text.strip() for p in soup.find_all("p") if p.text.strip()]
        lists = []
        for ul in soup.find_all("ul"):
            items = [li.text.strip() for li in ul.find_all("li") if li.text.strip()]
            if items:
                lists.append("\n".join(items))

        content = "\n\n".join(paragraphs + lists)

        marker = "Become an NPR sponsor"
        if marker in content:
            content = content.split(marker)[0].strip()
        return {"url": article_url, "title": title, "content": content, "image_url": main_image}

    except requests.RequestException as e:
        print(f"Error fetching article: {e}")
        return {"url": article_url, "title": "Error", "content": "Could not fetch article", "image_url": None}




# news_articles = get_links(url)
# print(news_articles)
# print()
# print()
# print("-" * 50)
# print(get_texts(news_articles[0]['url'])['image_url'])



# for idx, article in enumerate(news_articles, start=1):
#     print(f"Article {idx}:")
#     print(f"Title: {article['title']}")
#     print(f"URL: {article['url']}")
#     print(f"Teaser: {article['teaser']}")
#     print("-" * 40)
