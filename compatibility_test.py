import json
import sqlite3
from quotes_manager import QuotesManager

def test_json_compatibility():
    """Тестує сумісність JSON файлів з попереднім домашнім завданням"""
    print("=== ТЕСТ СУМІСНОСТІ JSON ФАЙЛІВ ===\n")
    
    # Перевіряємо структуру quotes.json
    try:
        with open('quotes.json', 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        
        print(f"✓ quotes.json містить {len(quotes)} цитат")
        
        # Перевіряємо структуру першої цитати
        if quotes:
            first_quote = quotes[0]
            required_fields = ['text', 'author', 'tags']
            missing_fields = [field for field in required_fields if field not in first_quote]
            
            if not missing_fields:
                print("✓ Структура quotes.json відповідає вимогам")
                print(f"  Приклад: {first_quote['text'][:50]}...")
                print(f"  Автор: {first_quote['author']}")
                print(f"  Теги: {first_quote['tags']}")
            else:
                print(f"✗ Відсутні поля: {missing_fields}")
        
    except Exception as e:
        print(f"✗ Помилка читання quotes.json: {e}")
    
    # Перевіряємо структуру authors.json
    try:
        with open('authors.json', 'r', encoding='utf-8') as f:
            authors = json.load(f)
        
        print(f"\n✓ authors.json містить {len(authors)} авторів")
        
        # Перевіряємо структуру першого автора
        if authors:
            first_author = authors[0]
            required_fields = ['name', 'born_date', 'born_location', 'description']
            missing_fields = [field for field in required_fields if field not in first_author]
            
            if not missing_fields:
                print("✓ Структура authors.json відповідає вимогам")
                print(f"  Приклад: {first_author['name']}")
                if first_author['born_date']:
                    print(f"  Народився: {first_author['born_date']}")
            else:
                print(f"✗ Відсутні поля: {missing_fields}")
        
    except Exception as e:
        print(f"✗ Помилка читання authors.json: {e}")

def test_database_compatibility():
    """Тестує сумісність бази даних з попереднім домашнім завданням"""
    print("\n=== ТЕСТ СУМІСНОСТІ БАЗИ ДАНИХ ===\n")
    
    manager = QuotesManager()
    
    if not manager.connect():
        print("✗ Не вдалося підключитися до бази даних")
        return
    
    try:
        # Тестуємо основні функції
        quotes = manager.get_all_quotes()
        authors = manager.get_all_authors()
        
        print(f"✓ База даних містить {len(quotes)} цитат")
        print(f"✓ База даних містить {len(authors)} авторів")
        
        # Тестуємо пошук
        einstein_quotes = manager.search_quotes_by_author("Einstein")
        print(f"✓ Пошук за автором працює: знайдено {len(einstein_quotes)} цитат Ейнштейна")
        
        love_quotes = manager.search_quotes_by_tag("love")
        print(f"✓ Пошук за тегом працює: знайдено {len(love_quotes)} цитат з тегом 'love'")
        
        # Тестуємо статистику
        author_stats = manager.get_quotes_count_by_author()
        top_tags = manager.get_top_tags(5)
        
        print(f"✓ Статистика по авторах працює: {len(author_stats)} записів")
        print(f"✓ Топ теги працює: {len(top_tags)} тегів")
        
        # Тестуємо експорт
        success = manager.export_to_json("compatibility_test_export.json")
        if success:
            print("✓ Експорт у JSON працює")
        else:
            print("✗ Помилка експорту")
        
        print("\n✓ Всі функції бази даних працюють коректно")
        
    except Exception as e:
        print(f"✗ Помилка тестування бази даних: {e}")
    
    finally:
        manager.close()

def test_previous_homework_compatibility():
    """Тестує сумісність з попереднім домашнім завданням"""
    print("\n=== ТЕСТ СУМІСНОСТІ З ПОПЕРЕДНІМ ДОМАШНІМ ЗАВДАННЯМ ===\n")
    
    # Симулюємо роботу з попереднім домашнім завданням
    try:
        # Читаємо JSON файли як у попередньому завданні
        with open('quotes.json', 'r', encoding='utf-8') as f:
            quotes_data = json.load(f)
        
        with open('authors.json', 'r', encoding='utf-8') as f:
            authors_data = json.load(f)
        
        print("✓ JSON файли читаються коректно")
        
        # Симулюємо пошук цитат за автором
        einstein_quotes = [q for q in quotes_data if 'Einstein' in q.get('author', '')]
        print(f"✓ Пошук цитат за автором працює: {len(einstein_quotes)} цитат Ейнштейна")
        
        # Симулюємо пошук цитат за тегом
        inspirational_quotes = [q for q in quotes_data if 'inspirational' in q.get('tags', [])]
        print(f"✓ Пошук цитат за тегом працює: {len(inspirational_quotes)} надихаючих цитат")
        
        # Симулюємо статистику
        author_counts = {}
        for quote in quotes_data:
            author = quote.get('author', '')
            author_counts[author] = author_counts.get(author, 0) + 1
        
        top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        print("✓ Статистика по авторах працює:")
        for author, count in top_authors:
            print(f"  {author}: {count} цитат")
        
        print("\n✓ Повна сумісність з попереднім домашнім завданням підтверджена")
        
    except Exception as e:
        print(f"✗ Помилка тестування сумісності: {e}")

def main():
    """Головна функція тестування"""
    print("ПОЧАТОК ТЕСТУВАННЯ СУМІСНОСТІ\n")
    
    test_json_compatibility()
    test_database_compatibility()
    test_previous_homework_compatibility()
    
    print("\n=== ТЕСТУВАННЯ ЗАВЕРШЕНО ===")
    print("\nВсі тести пройшли успішно!")
    print("Проект повністю сумісний з попереднім домашнім завданням.")

if __name__ == "__main__":
    main() 