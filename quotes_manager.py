import sqlite3
import json
from datetime import datetime

class QuotesManager:
    def __init__(self, db_name="quotes.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Підключається до бази даних"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Помилка підключення до бази даних: {e}")
            return False
    
    def close(self):
        """Закриває з'єднання з базою даних"""
        if self.conn:
            self.conn.close()
    
    def get_all_quotes(self):
        """Отримує всі цитати з авторами та тегами"""
        try:
            query = '''
                SELECT 
                    q.id,
                    q.text,
                    a.name as author_name,
                    a.born_date,
                    a.born_location,
                    a.description,
                    GROUP_CONCAT(t.name) as tags
                FROM quotes q
                LEFT JOIN authors a ON q.author_id = a.id
                LEFT JOIN quote_tags qt ON q.id = qt.quote_id
                LEFT JOIN tags t ON qt.tag_id = t.id
                GROUP BY q.id
                ORDER BY q.id
            '''
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            quotes = []
            for row in results:
                quote = {
                    "id": row[0],
                    "text": row[1],
                    "author": {
                        "name": row[2],
                        "born_date": row[3],
                        "born_location": row[4],
                        "description": row[5]
                    },
                    "tags": row[6].split(',') if row[6] else []
                }
                quotes.append(quote)
            
            return quotes
            
        except Exception as e:
            print(f"Помилка отримання цитат: {e}")
            return []
    
    def get_all_authors(self):
        """Отримує всіх авторів"""
        try:
            query = '''
                SELECT 
                    id,
                    name,
                    born_date,
                    born_location,
                    description
                FROM authors
                ORDER BY name
            '''
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            authors = []
            for row in results:
                author = {
                    "id": row[0],
                    "name": row[1],
                    "born_date": row[2],
                    "born_location": row[3],
                    "description": row[4]
                }
                authors.append(author)
            
            return authors
            
        except Exception as e:
            print(f"Помилка отримання авторів: {e}")
            return []
    
    def search_quotes_by_author(self, author_name):
        """Пошук цитат за автором"""
        try:
            query = '''
                SELECT 
                    q.id,
                    q.text,
                    a.name as author_name,
                    a.born_date,
                    a.born_location,
                    a.description,
                    GROUP_CONCAT(t.name) as tags
                FROM quotes q
                LEFT JOIN authors a ON q.author_id = a.id
                LEFT JOIN quote_tags qt ON q.id = qt.quote_id
                LEFT JOIN tags t ON qt.tag_id = t.id
                WHERE a.name LIKE ?
                GROUP BY q.id
                ORDER BY q.id
            '''
            
            self.cursor.execute(query, (f'%{author_name}%',))
            results = self.cursor.fetchall()
            
            quotes = []
            for row in results:
                quote = {
                    "id": row[0],
                    "text": row[1],
                    "author": {
                        "name": row[2],
                        "born_date": row[3],
                        "born_location": row[4],
                        "description": row[5]
                    },
                    "tags": row[6].split(',') if row[6] else []
                }
                quotes.append(quote)
            
            return quotes
            
        except Exception as e:
            print(f"Помилка пошуку цитат за автором: {e}")
            return []
    
    def search_quotes_by_tag(self, tag_name):
        """Пошук цитат за тегом"""
        try:
            query = '''
                SELECT 
                    q.id,
                    q.text,
                    a.name as author_name,
                    a.born_date,
                    a.born_location,
                    a.description,
                    GROUP_CONCAT(t.name) as tags
                FROM quotes q
                LEFT JOIN authors a ON q.author_id = a.id
                LEFT JOIN quote_tags qt ON q.id = qt.quote_id
                LEFT JOIN tags t ON qt.tag_id = t.id
                WHERE t.name LIKE ?
                GROUP BY q.id
                ORDER BY q.id
            '''
            
            self.cursor.execute(query, (f'%{tag_name}%',))
            results = self.cursor.fetchall()
            
            quotes = []
            for row in results:
                quote = {
                    "id": row[0],
                    "text": row[1],
                    "author": {
                        "name": row[2],
                        "born_date": row[3],
                        "born_location": row[4],
                        "description": row[5]
                    },
                    "tags": row[6].split(',') if row[6] else []
                }
                quotes.append(quote)
            
            return quotes
            
        except Exception as e:
            print(f"Помилка пошуку цитат за тегом: {e}")
            return []
    
    def get_quotes_count_by_author(self):
        """Отримує кількість цитат для кожного автора"""
        try:
            query = '''
                SELECT 
                    a.name,
                    COUNT(q.id) as quotes_count
                FROM authors a
                LEFT JOIN quotes q ON a.id = q.author_id
                GROUP BY a.id, a.name
                ORDER BY quotes_count DESC
            '''
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            stats = []
            for row in results:
                stat = {
                    "author": row[0],
                    "quotes_count": row[1]
                }
                stats.append(stat)
            
            return stats
            
        except Exception as e:
            print(f"Помилка отримання статистики: {e}")
            return []
    
    def get_top_tags(self, limit=10):
        """Отримує топ тегів за кількістю цитат"""
        try:
            query = '''
                SELECT 
                    t.name,
                    COUNT(qt.quote_id) as usage_count
                FROM tags t
                LEFT JOIN quote_tags qt ON t.id = qt.tag_id
                GROUP BY t.id, t.name
                ORDER BY usage_count DESC
                LIMIT ?
            '''
            
            self.cursor.execute(query, (limit,))
            results = self.cursor.fetchall()
            
            tags = []
            for row in results:
                tag = {
                    "name": row[0],
                    "usage_count": row[1]
                }
                tags.append(tag)
            
            return tags
            
        except Exception as e:
            print(f"Помилка отримання топ тегів: {e}")
            return []
    
    def export_to_json(self, filename="exported_data.json"):
        """Експортує всі дані у JSON файл"""
        try:
            data = {
                "quotes": self.get_all_quotes(),
                "authors": self.get_all_authors(),
                "statistics": {
                    "quotes_by_author": self.get_quotes_count_by_author(),
                    "top_tags": self.get_top_tags()
                },
                "export_date": datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"Дані експортовано у файл: {filename}")
            return True
            
        except Exception as e:
            print(f"Помилка експорту: {e}")
            return False

def main():
    """Головна функція для демонстрації роботи з базою даних"""
    manager = QuotesManager()
    
    if not manager.connect():
        print("Не вдалося підключитися до бази даних")
        return
    
    print("=== ДЕМОНСТРАЦІЯ РОБОТИ З БАЗОЮ ДАНИХ ===\n")
    
    # Отримуємо всі цитати
    quotes = manager.get_all_quotes()
    print(f"Всього цитат: {len(quotes)}")
    
    # Показуємо перші 3 цитати
    print("\nПерші 3 цитати:")
    for i, quote in enumerate(quotes[:3]):
        print(f"{i+1}. {quote['text'][:100]}...")
        print(f"   Автор: {quote['author']['name']}")
        print(f"   Теги: {', '.join(quote['tags'])}")
        print()
    
    # Отримуємо всіх авторів
    authors = manager.get_all_authors()
    print(f"Всього авторів: {len(authors)}")
    
    # Показуємо перших 3 авторів
    print("\nПерші 3 автори:")
    for i, author in enumerate(authors[:3]):
        print(f"{i+1}. {author['name']}")
        if author['born_date']:
            print(f"   Народився: {author['born_date']}")
        print()
    
    # Пошук цитат за автором
    einstein_quotes = manager.search_quotes_by_author("Einstein")
    print(f"Цитат Альберта Ейнштейна: {len(einstein_quotes)}")
    
    # Пошук цитат за тегом
    inspirational_quotes = manager.search_quotes_by_tag("inspirational")
    print(f"Надихаючих цитат: {len(inspirational_quotes)}")
    
    # Статистика по авторах
    author_stats = manager.get_quotes_count_by_author()
    print("\nТоп 5 авторів за кількістю цитат:")
    for i, stat in enumerate(author_stats[:5]):
        print(f"{i+1}. {stat['author']}: {stat['quotes_count']} цитат")
    
    # Топ теги
    top_tags = manager.get_top_tags(5)
    print("\nТоп 5 тегів:")
    for i, tag in enumerate(top_tags):
        print(f"{i+1}. {tag['name']}: {tag['usage_count']} використань")
    
    # Експорт даних
    manager.export_to_json("exported_quotes_data.json")
    
    manager.close()
    print("\n=== ДЕМОНСТРАЦІЯ ЗАВЕРШЕНА ===")

if __name__ == "__main__":
    main() 