import requests
from bs4 import BeautifulSoup
import pandas as pd

# a function for scraping content from url
def scrape_url(url):
  response = requests.get(url)
  response = response.content
  soup = BeautifulSoup(response, 'html.parser')
  return soup


# show the URL instead of printing the full page HTML
url = 'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
print(f"Starting scrape. First URL: {url}")


# extracting data from the content
data1 = []
for i in range(1,51):
  url = f'https://books.toscrape.com/catalogue/page-{i}.html'
  print(f"Fetching page {i}/50: {url}")
  response = requests.get(url)
  response = response.content
  soup = BeautifulSoup(response, 'html.parser')
  ol = soup.find('ol')
  if not ol:
    print(f"Page {i}: no book list found (skipping)")
    continue
  articles = ol.find_all('article', class_='product_pod')

  for article in articles:
    title_element = article.find('h3')
    title = title_element.get_text(strip=True)
    price_element = article.find('p', class_='price_color')
    price = price_element.get_text(strip=True)
    star_element = article.find('p')
    star = star_element['class'][1] if star_element else None
    data1.append({"title":title ," Price":price,"Star":star})

  print(f"Page {i}: found {len(articles)} books, total scraped: {len(data1)}")
# data stored in DataFrame to easy manipulate and preprocess
df = pd.DataFrame(data1)