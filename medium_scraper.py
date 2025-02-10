import requests
from bs4 import BeautifulSoup
import time

def get_articles(BASE_URL):
    """Scrapes Medium blog articles and extracts text from raw html."""
    response = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find article links
    links = list({a["href"] for a in soup.find_all("a", href=True) if "/gwc-solutions/" in a["href"]})
    
    articles = []
    for link in links:
        
        article_page = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
        article_soup = BeautifulSoup(article_page.text, "html.parser")
        paragraphs = [p.text for p in article_soup.find_all("p")]
        if paragraphs:
            articles.append("\n".join(paragraphs))
        time.sleep(1)  # Be polite to Medium
    
    return articles, links