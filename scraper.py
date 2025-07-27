import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

class QuotesScraper:
    def __init__(self):
        self.base_url = "http://quotes.toscrape.com"
        self.quotes = []
        self.authors = {}
        
    def get_page_content(self, url):
        """Отримує HTML контент сторінки"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Помилка при отриманні {url}: {e}")
            return None
    
    def parse_quotes_page(self, html_content):
        """Парсить сторінку з цитатами"""
        soup = BeautifulSoup(html_content, 'html.parser')
        quote_elements = soup.find_all('div', class_='quote')
        
        for quote_element in quote_elements:
            # Отримуємо текст цитати
            text_element = quote_element.find('span', class_='text')
            text = text_element.get_text(strip=True) if text_element else ""
            
            # Отримуємо автора
            author_element = quote_element.find('small', class_='author')
            author_name = author_element.get_text(strip=True) if author_element else ""
            
            # Отримуємо теги
            tags_elements = quote_element.find_all('a', class_='tag')
            tags = [tag.get_text(strip=True) for tag in tags_elements]
            
            # Створюємо об'єкт цитати
            quote = {
                "text": text,
                "author": author_name,
                "tags": tags
            }
            
            self.quotes.append(quote)
            
            # Зберігаємо інформацію про автора для подальшого отримання
            if author_name and author_name not in self.authors:
                self.authors[author_name] = None
    
    def get_author_info(self, author_name):
        """Отримує інформацію про автора з його сторінки"""
        # Знаходимо посилання на автора
        author_url = f"{self.base_url}/author/{author_name.replace(' ', '-')}/"
        
        html_content = self.get_page_content(author_url)
        if not html_content:
            return None
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Отримуємо інформацію про автора
        author_info = {
            "name": author_name,
            "born_date": "",
            "born_location": "",
            "description": ""
        }
        
        # Знаходимо блок з інформацією про автора
        author_details = soup.find('div', class_='author-details')
        if author_details:
            # Дата народження
            born_element = author_details.find('span', class_='author-born-date')
            if born_element:
                author_info["born_date"] = born_element.get_text(strip=True)
            
            # Місце народження
            location_element = author_details.find('span', class_='author-born-location')
            if location_element:
                author_info["born_location"] = location_element.get_text(strip=True)
            
            # Опис
            description_element = author_details.find('div', class_='author-description')
            if description_element:
                author_info["description"] = description_element.get_text(strip=True)
        
        return author_info
    
    def scrape_all_pages(self):
        """Скрапить всі сторінки з цитатами"""
        page_num = 1
        
        while True:
            page_url = f"{self.base_url}/page/{page_num}/"
            print(f"Скрапінг сторінки {page_num}...")
            
            html_content = self.get_page_content(page_url)
            if not html_content:
                break
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Перевіряємо чи є цитати на сторінці
            quotes_on_page = soup.find_all('div', class_='quote')
            if not quotes_on_page:
                print(f"На сторінці {page_num} немає цитат. Зупиняємо скрапінг.")
                break
            
            self.parse_quotes_page(html_content)
            
            # Невелика затримка між запитами
            time.sleep(1)
            page_num += 1
    
    def get_all_authors_info(self):
        """Отримує інформацію про всіх авторів"""
        print("Отримання інформації про авторів...")
        
        for author_name in self.authors.keys():
            print(f"Отримання інформації про автора: {author_name}")
            author_info = self.get_author_info(author_name)
            if author_info:
                self.authors[author_name] = author_info
            time.sleep(1)  # Затримка між запитами
    
    def save_to_json(self):
        """Зберігає дані у JSON файли"""
        # Зберігаємо цитати
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=2)
        
        # Зберігаємо авторів (тільки ті, для яких є інформація)
        authors_list = [author for author in self.authors.values() if author is not None]
        with open('authors.json', 'w', encoding='utf-8') as f:
            json.dump(authors_list, f, ensure_ascii=False, indent=2)
        
        print(f"Збережено {len(self.quotes)} цитат у quotes.json")
        print(f"Збережено {len(authors_list)} авторів у authors.json")
    
    def run(self):
        """Запускає повний процес скрапінгу"""
        print("Початок скрапінгу сайту quotes.toscrape.com...")
        
        # Скрапимо всі сторінки з цитатами
        self.scrape_all_pages()
        
        # Отримуємо інформацію про авторів
        self.get_all_authors_info()
        
        # Зберігаємо результати
        self.save_to_json()
        
        print("Скрапінг завершено!")

if __name__ == "__main__":
    scraper = QuotesScraper()
    scraper.run() 