import json

def convert_quotes_structure():
    """Конвертує структуру quotes.json під попереднє завдання"""
    try:
        with open('quotes.json', 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        
        # Конвертуємо структуру
        converted_quotes = []
        for quote in quotes:
            converted_quote = {
                "quote": quote["text"],  # text -> quote
                "author": quote["author"],
                "tags": quote["tags"]
            }
            converted_quotes.append(converted_quote)
        
        # Зберігаємо з новою структурою
        with open('quotes_converted.json', 'w', encoding='utf-8') as f:
            json.dump(converted_quotes, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Конвертовано {len(converted_quotes)} цитат")
        print("📁 Збережено як quotes_converted.json")
        
    except Exception as e:
        print(f"❌ Помилка конвертації quotes: {e}")

def convert_authors_structure():
    """Конвертує структуру authors.json під попереднє завдання"""
    try:
        with open('authors.json', 'r', encoding='utf-8') as f:
            authors = json.load(f)
        
        # Конвертуємо структуру
        converted_authors = []
        for author in authors:
            converted_author = {
                "fullname": author["name"],  # name -> fullname
                "born_date": author["born_date"],
                "born_location": author["born_location"],
                "description": author["description"]
            }
            converted_authors.append(converted_author)
        
        # Зберігаємо з новою структурою
        with open('authors_converted.json', 'w', encoding='utf-8') as f:
            json.dump(converted_authors, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Конвертовано {len(converted_authors)} авторів")
        print("📁 Збережено як authors_converted.json")
        
    except Exception as e:
        print(f"❌ Помилка конвертації authors: {e}")

def main():
    """Головна функція конвертації"""
    print("🔄 Конвертація структури JSON файлів...")
    print("=" * 50)
    
    convert_quotes_structure()
    print()
    convert_authors_structure()
    print()
    
    print("✅ Конвертація завершена!")
    print("\n📋 Створені файли:")
    print("  - quotes_converted.json (з полем 'quote' замість 'text')")
    print("  - authors_converted.json (з полем 'fullname' замість 'name')")
    print("\n💡 Тепер ви можете використовувати ці файли з попереднім домашнім завданням!")

if __name__ == "__main__":
    main() 