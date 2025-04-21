from typing import NamedTuple, Optional
import requests
from bs4 import BeautifulSoup

class Products(NamedTuple):
    name : str
    discount_price : str
    original_price: Optional[str]

class Scrape:
    def __init__ (self, url: str):
        self.url = url

    def get_soup(self, url) -> BeautifulSoup:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
        
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print (f"Error fetching page: {e}")
            return None 
    
    def scrape_tokped(self) -> None:
        results = []
        print(f"On searching...")

        soup = self.get_soup(self.url)

        if not soup:
            print("Failed to fetch data from Tokopedia.")
            return results
        
        name = soup.select_one("div.css-1nylpq2").get_text(strip=True)
        original_price = soup.select_one("div.original-price span:nth-of-type(2)")
        discount_price = soup.select_one("div.price")

        if original_price and discount_price:
            original_price = original_price.get_text(strip=True)
            discount_price = discount_price.get_text(strip=True)
        else:
            discount_price = discount_price.get_text(strip=True)
            original_price = discount_price

        product_result = Products(
            name=name,
            discount_price=discount_price,
            original_price=original_price,
        )

        results.append(product_result)

        if not results:
            raise Exception("Product not found.")

        return {
            "product_name": name if name else "Unknown",
            "original_price": original_price if original_price else "Unknown",
            "discount_price": discount_price if discount_price else "Unknown"
        }

def clean_price(price):
    """Clean price string from non-numeric characters"""
    if isinstance(price, str):
        cleaned = ''.join(c for c in price if c.isdigit())
        return int(cleaned) if cleaned else 0
    return price