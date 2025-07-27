import json
import sqlite3
import os
from datetime import datetime

class DatabaseLoader:
    def __init__(self, db_name="quotes.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Підключається до бази даних"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Підключено до бази даних: {self.db_name}")
        except Exception as e:
            print(f"Помилка підключення до бази даних: {e}")
            return False
        return True
    
    def create_tables(self):
        """Створює таблиці в базі даних"""
        try:
            # Таблиця для авторів
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    born_date TEXT,
                    born_location TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблиця для цитат
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    author_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (author_id) REFERENCES authors (id)
                )
            ''')
            
            # Таблиця для тегів
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблиця для зв'язку цитат і тегів
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS quote_tags (
                    quote_id INTEGER,
                    tag_id INTEGER,
                    FOREIGN KEY (quote_id) REFERENCES quotes (id),
                    FOREIGN KEY (tag_id) REFERENCES tags (id),
                    PRIMARY KEY (quote_id, tag_id)
                )
            ''')
            
            self.conn.commit()
            print("Таблиці створено успішно")
            
        except Exception as e:
            print(f"Помилка створення таблиць: {e}")
            return False
        return True
    
    def load_authors(self, authors_file):
        """Завантажує авторів з JSON файлу"""
        try:
            with open(authors_file, 'r', encoding='utf-8') as f:
                authors = json.load(f)
            
            print(f"Завантаження {len(authors)} авторів...")
            
            for author in authors:
                try:
                    self.cursor.execute('''
                        INSERT OR REPLACE INTO authors (name, born_date, born_location, description)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        author.get('name', ''),
                        author.get('born_date', ''),
                        author.get('born_location', ''),
                        author.get('description', '')
                    ))
                except Exception as e:
                    print(f"Помилка додавання автора {author.get('name', 'Unknown')}: {e}")
            
            self.conn.commit()
            print("Автори завантажено успішно")
            
        except Exception as e:
            print(f"Помилка завантаження авторів: {e}")
            return False
        return True
    
    def load_quotes(self, quotes_file):
        """Завантажує цитати з JSON файлу"""
        try:
            with open(quotes_file, 'r', encoding='utf-8') as f:
                quotes = json.load(f)
            
            print(f"Завантаження {len(quotes)} цитат...")
            
            for quote in quotes:
                try:
                    # Отримуємо ID автора
                    author_name = quote.get('author', '')
                    self.cursor.execute('SELECT id FROM authors WHERE name = ?', (author_name,))
                    author_result = self.cursor.fetchone()
                    author_id = author_result[0] if author_result else None
                    
                    # Додаємо цитату
                    self.cursor.execute('''
                        INSERT INTO quotes (text, author_id)
                        VALUES (?, ?)
                    ''', (quote.get('text', ''), author_id))
                    
                    quote_id = self.cursor.lastrowid
                    
                    # Додаємо теги
                    tags = quote.get('tags', [])
                    for tag_name in tags:
                        # Додаємо тег, якщо його немає
                        self.cursor.execute('''
                            INSERT OR IGNORE INTO tags (name)
                            VALUES (?)
                        ''', (tag_name,))
                        
                        # Отримуємо ID тегу
                        self.cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
                        tag_result = self.cursor.fetchone()
                        tag_id = tag_result[0] if tag_result else None
                        
                        # Додаємо зв'язок цитата-тег
                        if tag_id:
                            self.cursor.execute('''
                                INSERT OR IGNORE INTO quote_tags (quote_id, tag_id)
                                VALUES (?, ?)
                            ''', (quote_id, tag_id))
                
                except Exception as e:
                    print(f"Помилка додавання цитати: {e}")
            
            self.conn.commit()
            print("Цитати завантажено успішно")
            
        except Exception as e:
            print(f"Помилка завантаження цитат: {e}")
            return False
        return True
    
    def get_statistics(self):
        """Показує статистику бази даних"""
        try:
            # Кількість авторів
            self.cursor.execute('SELECT COUNT(*) FROM authors')
            authors_count = self.cursor.fetchone()[0]
            
            # Кількість цитат
            self.cursor.execute('SELECT COUNT(*) FROM quotes')
            quotes_count = self.cursor.fetchone()[0]
            
            # Кількість тегів
            self.cursor.execute('SELECT COUNT(*) FROM tags')
            tags_count = self.cursor.fetchone()[0]
            
            print("\n=== СТАТИСТИКА БАЗИ ДАНИХ ===")
            print(f"Авторів: {authors_count}")
            print(f"Цитат: {quotes_count}")
            print(f"Тегів: {tags_count}")
            print("================================")
            
        except Exception as e:
            print(f"Помилка отримання статистики: {e}")
    
    def close(self):
        """Закриває з'єднання з базою даних"""
        if self.conn:
            self.conn.close()
            print("З'єднання з базою даних закрито")
    
    def run(self):
        """Запускає повний процес завантаження"""
        print("Початок завантаження даних у базу даних...")
        
        # Перевіряємо наявність файлів
        if not os.path.exists('authors.json'):
            print("Помилка: файл authors.json не знайдено")
            return False
        
        if not os.path.exists('quotes.json'):
            print("Помилка: файл quotes.json не знайдено")
            return False
        
        # Підключаємося до бази даних
        if not self.connect():
            return False
        
        # Створюємо таблиці
        if not self.create_tables():
            return False
        
        # Завантажуємо дані
        if not self.load_authors('authors.json'):
            return False
        
        if not self.load_quotes('quotes.json'):
            return False
        
        # Показуємо статистику
        self.get_statistics()
        
        # Закриваємо з'єднання
        self.close()
        
        print("Завантаження завершено успішно!")
        return True

if __name__ == "__main__":
    loader = DatabaseLoader()
    loader.run() 