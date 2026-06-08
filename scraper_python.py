import requests
from bs4 import BeautifulSoup
import csv
import json
import time

base_url = "http://books.toscrape.com/catalogue/page-{}.html"
all_books = []

for page in range(1, 6):  # Pages 1-5
    url = base_url.format(page)
    print(f"\n📄 Scraping page {page}: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes
        
        soup = BeautifulSoup(response.content, "html.parser")
        books_on_page = soup.find_all("article", class_="product_pod")
        
        for book in books_on_page:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            all_books.append({"title": title, "price": price, "page": page})
            print(f"   Found: {title} - {price}")
        
        time.sleep(1)  # Be respectful to the server
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error scraping page {page}: {e}")
        continue

# Save results (same as before)
with open("books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "Page"])
    for book in all_books:
        writer.writerow([book["title"], book["price"], book["page"]])

with open("books.json", "w") as f:
    json.dump(all_books, f, indent=2)

print(f"\n✅ Success! Scraped {len(all_books)} books from {page} pages")