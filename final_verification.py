#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Фінальна перевірка виконання домашнього завдання #9
"""

import json
import os
import sqlite3

def check_requirements():
    """Перевіряє всі вимоги домашнього завдання #9"""
    print("🔍 ПЕРЕВІРКА ВИМОГ ДОМАШНЬОГО ЗАВДАННЯ #9")
    print("=" * 60)
    
    requirements = {
        "BeautifulSoup використання": False,
        "Скрапінг quotes.toscrape.com": False,
        "quotes.json файл": False,
        "authors.json файл": False,
        "Структура відповідає попередньому завданню": False,
        "База даних створена": False,
        "Попереднє завдання працює": False
    }
    
    # 1. Перевірка використання BeautifulSoup
    try:
        with open('scraper.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'BeautifulSoup' in content and 'bs4' in content:
                requirements["BeautifulSoup використання"] = True
                print("✅ BeautifulSoup використовується")
            else:
                print("❌ BeautifulSoup не знайдено")
    except Exception as e:
        print(f"❌ Помилка перевірки scraper.py: {e}")
    
    # 2. Перевірка скрапінгу
    if os.path.exists('quotes.json') and os.path.exists('authors.json'):
        requirements["Скрапінг quotes.toscrape.com"] = True
        print("✅ Скрапінг виконано")
    else:
        print("❌ Файли скрапінгу не знайдено")
    
    # 3. Перевірка quotes.json
    try:
        with open('quotes.json', 'r', encoding='utf-8') as f:
            quotes = json.load(f)
            if len(quotes) > 0:
                requirements["quotes.json файл"] = True
                print(f"✅ quotes.json містить {len(quotes)} цитат")
            else:
                print("❌ quotes.json порожній")
    except Exception as e:
        print(f"❌ Помилка читання quotes.json: {e}")
    
    # 4. Перевірка authors.json
    try:
        with open('authors.json', 'r', encoding='utf-8') as f:
            authors = json.load(f)
            if len(authors) > 0:
                requirements["authors.json файл"] = True
                print(f"✅ authors.json містить {len(authors)} авторів")
            else:
                print("❌ authors.json порожній")
    except Exception as e:
        print(f"❌ Помилка читання authors.json: {e}")
    
    # 5. Перевірка структури для попереднього завдання
    try:
        with open('quotes_converted.json', 'r', encoding='utf-8') as f:
            quotes_converted = json.load(f)
        with open('authors_converted.json', 'r', encoding='utf-8') as f:
            authors_converted = json.load(f)
        
        if quotes_converted and authors_converted:
            # Перевіряємо структуру
            first_quote = quotes_converted[0]
            first_author = authors_converted[0]
            
            if ('quote' in first_quote and 'author' in first_quote and 'tags' in first_quote and
                'fullname' in first_author and 'born_date' in first_author and 
                'born_location' in first_author and 'description' in first_author):
                requirements["Структура відповідає попередньому завданню"] = True
                print("✅ Структура JSON файлів відповідає попередньому завданню")
            else:
                print("❌ Структура JSON файлів не відповідає попередньому завданню")
    except Exception as e:
        print(f"❌ Помилка перевірки конвертованих файлів: {e}")
    
    # 6. Перевірка бази даних
    try:
        conn = sqlite3.connect('quotes.db')
        cursor = conn.cursor()
        
        # Перевіряємо таблиці
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['authors', 'quotes', 'tags', 'quote_tags']
        if all(table in tables for table in required_tables):
            requirements["База даних створена"] = True
            print("✅ База даних створена з усіма таблицями")
            
            # Перевіряємо дані
            cursor.execute("SELECT COUNT(*) FROM authors")
            authors_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM quotes")
            quotes_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tags")
            tags_count = cursor.fetchone()[0]
            
            print(f"   📊 Авторів: {authors_count}")
            print(f"   📊 Цитат: {quotes_count}")
            print(f"   📊 Тегів: {tags_count}")
        else:
            print("❌ База даних не містить всіх необхідних таблиць")
        
        conn.close()
    except Exception as e:
        print(f"❌ Помилка перевірки бази даних: {e}")
    
    # 7. Перевірка роботи з попереднім завданням
    try:
        # Симулюємо роботу з попереднім завданням
        with open('quotes_converted.json', 'r', encoding='utf-8') as f:
            quotes_data = json.load(f)
        
        # Тестуємо пошук за автором
        einstein_quotes = [q for q in quotes_data if 'Einstein' in q.get('author', '')]
        # Тестуємо пошук за тегом
        inspirational_quotes = [q for q in quotes_data if 'inspirational' in q.get('tags', [])]
        
        if len(einstein_quotes) > 0 and len(inspirational_quotes) > 0:
            requirements["Попереднє завдання працює"] = True
            print("✅ Попереднє домашнє завдання працює коректно")
        else:
            print("❌ Попереднє домашнє завдання не працює")
    except Exception as e:
        print(f"❌ Помилка тестування попереднього завдання: {e}")
    
    return requirements

def print_summary(requirements):
    """Виводить підсумок перевірки"""
    print("\n" + "=" * 60)
    print("📋 ПІДСУМОК ПЕРЕВІРКИ")
    print("=" * 60)
    
    passed = sum(requirements.values())
    total = len(requirements)
    
    for req, status in requirements.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {req}")
    
    print(f"\n📊 Результат: {passed}/{total} вимог виконано")
    
    if passed == total:
        print("\n🎉 ВСІ ВИМОГИ ДОМАШНЬОГО ЗАВДАННЯ #9 ВИКОНАНО!")
        print("✅ Проект готовий до здачі")
    else:
        print(f"\n⚠️  Не виконано {total - passed} вимог")
        print("❌ Потрібно доопрацювати проект")

def main():
    """Головна функція"""
    print("🚀 ФІНАЛЬНА ПЕРЕВІРКА ДОМАШНЬОГО ЗАВДАННЯ #9")
    print("=" * 60)
    
    requirements = check_requirements()
    print_summary(requirements)
    
    print("\n📁 Створені файли:")
    files = [
        'scraper.py', 'database_loader.py', 'quotes_manager.py',
        'quotes.json', 'authors.json', 'quotes_converted.json', 
        'authors_converted.json', 'quotes.db', 'README.md'
    ]
    
    for file in files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (відсутній)")

if __name__ == "__main__":
    main() 