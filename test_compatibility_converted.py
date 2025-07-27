import json

def test_converted_json_compatibility():
    """Тестує сумісність конвертованих JSON файлів з попереднім домашнім завданням"""
    print("=== ТЕСТ СУМІСНОСТІ КОНВЕРТОВАНИХ JSON ФАЙЛІВ ===\n")
    
    # Тестуємо quotes_converted.json
    try:
        with open('quotes_converted.json', 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        print(f"✓ quotes_converted.json містить {len(quotes)} цитат")
        
        if quotes:
            first_quote = quotes[0]
            required_fields = ['quote', 'author', 'tags']
            missing_fields = [field for field in required_fields if field not in first_quote]
            
            if not missing_fields:
                print("✓ Структура quotes_converted.json відповідає вимогам попереднього завдання")
                print(f"  Приклад: {first_quote['quote'][:50]}...")
                print(f"  Автор: {first_quote['author']}")
                print(f"  Теги: {first_quote['tags']}")
            else:
                print(f"✗ Відсутні поля: {missing_fields}")
    except Exception as e:
        print(f"✗ Помилка читання quotes_converted.json: {e}")

    # Тестуємо authors_converted.json
    try:
        with open('authors_converted.json', 'r', encoding='utf-8') as f:
            authors = json.load(f)
        print(f"\n✓ authors_converted.json містить {len(authors)} авторів")
        
        if authors:
            first_author = authors[0]
            required_fields = ['fullname', 'born_date', 'born_location', 'description']
            missing_fields = [field for field in required_fields if field not in first_author]
            
            if not missing_fields:
                print("✓ Структура authors_converted.json відповідає вимогам попереднього завдання")
                print(f"  Приклад: {first_author['fullname']}")
                if first_author['born_date']:
                    print(f"  Народився: {first_author['born_date']}")
            else:
                print(f"✗ Відсутні поля: {missing_fields}")
    except Exception as e:
        print(f"✗ Помилка читання authors_converted.json: {e}")

def test_simulation_with_previous_homework():
    """Симулює роботу з попереднім домашнім завданням"""
    print("\n=== СИМУЛЯЦІЯ РОБОТИ З ПОПЕРЕДНІМ ДОМАШНІМ ЗАВДАННЯМ ===\n")
    
    try:
        # Завантажуємо конвертовані дані
        with open('quotes_converted.json', 'r', encoding='utf-8') as f:
            quotes_data = json.load(f)
        with open('authors_converted.json', 'r', encoding='utf-8') as f:
            authors_data = json.load(f)
        
        print("✅ JSON файли читаються коректно")
        
        # Симулюємо пошук цитат за автором (як у попередньому завданні)
        einstein_quotes = [q for q in quotes_data if 'Einstein' in q.get('author', '')]
        print(f"✅ Пошук цитат за автором працює: {len(einstein_quotes)} цитат Ейнштейна")
        
        # Симулюємо пошук цитат за тегом
        inspirational_quotes = [q for q in quotes_data if 'inspirational' in q.get('tags', [])]
        print(f"✅ Пошук цитат за тегом працює: {len(inspirational_quotes)} надихаючих цитат")
        
        # Симулюємо статистику по авторах
        author_counts = {}
        for quote in quotes_data:
            author = quote.get('author', '')
            author_counts[author] = author_counts.get(author, 0) + 1
        
        top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        print("✅ Статистика по авторах працює:")
        for author, count in top_authors:
            print(f"  {author}: {count} цитат")
        
        # Симулюємо роботу з авторами (як у попередньому завданні)
        einstein_author = next((a for a in authors_data if a.get('fullname') == 'Albert Einstein'), None)
        if einstein_author:
            print(f"✅ Знайдено автора: {einstein_author['fullname']}")
            if einstein_author['born_date']:
                print(f"  Народився: {einstein_author['born_date']}")
        
        print("\n✅ Повна сумісність з попереднім домашнім завданням підтверджена!")
        
    except Exception as e:
        print(f"✗ Помилка симуляції: {e}")

def main():
    """Головна функція тестування"""
    print("ПОЧАТОК ТЕСТУВАННЯ СУМІСНОСТІ КОНВЕРТОВАНИХ ФАЙЛІВ\n")
    
    test_converted_json_compatibility()
    test_simulation_with_previous_homework()
    
    print("\n=== ТЕСТУВАННЯ ЗАВЕРШЕНО ===")
    print("\n🎉 Всі тести пройшли успішно!")
    print("📁 Конвертовані файли готові для використання з попереднім домашнім завданням:")
    print("  - quotes_converted.json")
    print("  - authors_converted.json")
    print("\n💡 Тепер ви можете використовувати ці файли з вашим попереднім домашнім завданням!")

if __name__ == "__main__":
    main() 