from typing import NamedTuple, Optional
import requests
from bs4 import BeautifulSoup

class ProductScraper(NamedTuple):
    name : str
    discount_price : str
    original_price: Optional[str]
    seller : str
    image_url : str
    sold : str

class Scrape:
    def __init__ (self, product_name: str):
        self.product_name = product_name

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
        encoded_product_name = self.product_name.replace(" ", "%20")
        url = f"https://www.tokopedia.com/search?st=&q={encoded_product_name}"
        print(f"Searching for {self.product_name}")
        # print(f"URL: {url}")

        soup = self.get_soup(url)

        if not soup:
            print("Failed to fetch data from Tokopedia.")
            return results
        
        products = soup.select("div[data-testid='divSRPContentProducts']")

        get_url = soup.find("a", class_="oQ94Awb6LlTiGByQZo8Lyw== IM26HEnTb-krJayD-R0OHw==")
        product_url = get_url.get("href")

        if not products:
            print("No products found on the search page")
            return results

        for product in products:
            name = product.select_one("span[class='_0T8-iGxMpV6NEsYEhwkqEg==']").get_text()

            discount_price = product.select_one("div[class='_67d6E1xDKIzw+i2D2L0tjw== t4jWW3NandT5hvCFAiotYg==']")
            original_price = product.select_one("span[class='q6wH9+Ht7LxnxrEgD22BCQ==']")

            if discount_price and original_price:
                discount_price = discount_price.get_text(strip=True)
                original_price = original_price.get_text(strip=True)
            else:
                original_price = product.select_one("div[class='_67d6E1xDKIzw+i2D2L0tjw==']").get_text(strip=True)
                discount_price = original_price

            seller = product.select_one("span[class='T0rpy-LEwYNQifsgB-3SQw== pC8DMVkBZGW7-egObcWMFQ== flip']").get_text()
            image_url = product.select_one("div.css-bqlp8e.responsive img").get("src")
            sold = product.select_one("span[class='se8WAnkjbVXZNA8mT+Veuw==']").get_text()

            product_result = ProductScraper(
                name=name,
                discount_price=discount_price,
                original_price=original_price,
                seller=seller,
                image_url=image_url,
                sold=sold
            )

            results.append(product_result)

        if not results:
            raise Exception("Product not found.")
        
        for result in results:
            print(result)

        return {
            "product_name": name if name else "Unknown",
            "product_url": product_url,
            "original_price": original_price if original_price else "Unknown",
            "discount_price": discount_price if discount_price else "Unknown"
        }

def clean_price(price):
    """Clean price string from non-numeric characters"""
    if isinstance(price, str):
        cleaned = ''.join(c for c in price if c.isdigit())
        return int(cleaned) if cleaned else 0
    return price