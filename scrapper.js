const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

// Website to scrape (safe practice site)
const url = 'http://books.toscrape.com/';

async function scrapeBooks() {
    try {
        // Fetch the website HTML
        const { data } = await axios.get(url);
        
        // Load HTML into cheerio for parsing
        const $ = cheerio.load(data);
        
        // Array to store our scraped data
        const books = [];
        
        // Find all book articles
        $('article.product_pod').each((index, element) => {
            // Extract title (from the 'title' attribute of the <a> tag inside h3)
            const title = $(element).find('h3 a').attr('title');
            
            // Extract price
            const price = $(element).find('p.price_color').text();
            
            // Extract availability (bonus!)
            const availability = $(element).find('p.instock.availability').text().trim();
            
            books.push({
                title: title,
                price: price,
                availability: availability
            });
            
            console.log(`Found: ${title} - ${price}`);
        });
        
        // Save to JSON file (good for APIs)
        fs.writeFileSync('books.json', JSON.stringify(books, null, 2));
        console.log(`\n✅ Saved ${books.length} books to books.json`);
        
        // Also save to CSV (good for Excel)
        let csvContent = 'Title,Price,Availability\n';
        books.forEach(book => {
            csvContent += `"${book.title}","${book.price}","${book.availability}"\n`;
        });
        fs.writeFileSync('books.csv', csvContent);
        console.log(`✅ Saved ${books.length} books to books.csv`);
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
}

// Run the scraper
scrapeBooks();