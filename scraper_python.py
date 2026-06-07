import requests
from bs4 import BeautifulSoup
import csv
import json

url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

books = []
for book in soup.find_all("article", class_="product_pod"):
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    books.append({"title": title, "price": price})
    print(f"{title} - {price}")

# Save to CSV
with open("books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price"])
    for b in books:
        writer.writerow([b["title"], b["price"]])

# Save to JSON
with open("books.json", "w") as f:
    json.dump(books, f, indent=2)

print(f"\n✅ Saved {len(books)} books")