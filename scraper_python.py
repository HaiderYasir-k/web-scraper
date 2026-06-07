import requests
from bs4 import BeautifulSoup
import csv
import json

# Scrape multiple pages (pagination)
base_url = "http://books.toscrape.com/catalogue/page-{}.html"
all_books = []

# Change range(1, 3) to scrape more pages (1-2 pages for now)
for page in range(1, 3):  # Pages 1-2
    url = base_url.format(page)
    print(f"\n📄 Scraping page {page}: {url}")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all books on this page
    books_on_page = soup.find_all("article", class_="product_pod")
    
    for book in books_on_page:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        all_books.append({"title": title, "price": price, "page": page})
        print(f"   Found: {title} - {price}")

# Save to CSV
with open("books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "Page"])
    for book in all_books:
        writer.writerow([book["title"], book["price"], book["page"]])

# Save to JSON
with open("books.json", "w") as f:
    json.dump(all_books, f, indent=2)

print(f"\n✅ Success! Scraped {len(all_books)} books from {all_books[-1]['page']} pages")
print(f"📁 Saved to books.csv and books.json")