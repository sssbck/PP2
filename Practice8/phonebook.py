import psycopg2
from connect import get_connection

import psycopg2
import os
from connect import get_connection

def create_table(conn):
    """Отдельная функция только для создания таблицы"""
    with conn.cursor() as cur:

        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL
            )
        """)
        conn.commit()

def setup_database():
    """Главная функция настройки базы при запуске"""
    conn = get_connection()
    try:
        create_table(conn)
        
        with conn.cursor() as cur:
            if os.path.exists('functions.sql'):
                with open('functions.sql', 'r', encoding='utf-8') as f:
                    cur.execute(f.read())

            if os.path.exists('procedures.sql'):
                with open('procedures.sql', 'r', encoding='utf-8') as f:
                    cur.execute(f.read())
                    
            conn.commit()
            print("--- База данных успешно инициализирована! ---")
            
    except Exception as e:
        print(f" Ошибка при инициализации базы: {e}")
    finally:
        conn.close()


def search_pattern(pattern):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
            results = cur.fetchall()
            print(f"\n--- Результаты поиска по запросу '{pattern}' ---")
            if not results:
                print("Ничего не найдено.")
            for row in results:
                print(f"Имя: {row[0]}, Телефон: {row[1]}")
    finally:
        conn.close()

def upsert_user(name, phone):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s::VARCHAR, %s::VARCHAR);", (name, phone))
            conn.commit()
            print(f"\n Контакт {name} успешно добавлен/обновлен.")
    finally:
        conn.close()

def bulk_insert_users(names_list, phones_list):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL bulk_insert_contacts(%s, %s, %s);", (names_list, phones_list, None))
            conn.commit()
            
            invalid_data = cur.fetchone()[0] 
            if invalid_data:
                print("\n Внимание: Найдены некорректные данные (они не были добавлены):")
                for item in invalid_data:
                    print(f" - Ошибка валидации телефона: {item}")
            else:
                print("\n Все контакты успешно добавлены (ошибок нет).")
    finally:
        conn.close()

def get_paginated_users(limit, offset):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
            results = cur.fetchall()
            print(f"\n--- Страница (Limit: {limit}, Offset: {offset}) ---")
            if not results:
                print("Записей нет.")
            for row in results:
                print(f"Имя: {row[0]}, Телефон: {row[1]}")
    finally:
        conn.close()

def delete_user(identifier):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s::VARCHAR);", (identifier,))
            conn.commit()
            print(f"\n Записи с идентификатором '{identifier}' удалены.")
    finally:
        conn.close()


if __name__ == '__main__':
    while True:
        print(" ТЕЛЕФОННАЯ КНИГА (PostgreSQL)")

        print("1. Добавить или обновить контакт (Upsert)")
        print("2. Массовое добавление контактов")
        print("3. Поиск по имени или телефону")
        print("4. Вывод контактов (Пагинация)")
        print("5. Удалить контакт")
        print("0. Выйти из программы")
        
        choice = input("\nВыберите действие (0-5): ")
        
        if choice == '1':
            name = input("Введите имя: ")
            phone = input("Введите телефон: ")
            upsert_user(name, phone)
            
        elif choice == '2':
            print("Введите данные через запятую.")
            names_input = input("Имена (напр. Анна, Борис): ")
            phones_input = input("Телефоны (напр. +123, +456): ")
            # Очищаем от лишних пробелов и создаем списки
            names = [n.strip() for n in names_input.split(',')]
            phones = [p.strip() for p in phones_input.split(',')]
            
            if len(names) == len(phones):
                bulk_insert_users(names, phones)
            else:
                print(" Ошибка: Количество имен не совпадает с количеством телефонов!")
                
        elif choice == '3':
            pattern = input("Введите текст для поиска: ")
            search_pattern(pattern)
            
        elif choice == '4':
            try:
                limit = int(input("Сколько записей показать (Limit)? "))
                offset = int(input("С какой записи начать (Offset)? "))
                get_paginated_users(limit, offset)
            except ValueError:
                print(" Ошибка: Пожалуйста, вводите только числа.")
                
        elif choice == '5':
            identifier = input("Введите имя или телефон для удаления: ")
            delete_user(identifier)
            
        elif choice == '0':
            print("Выход из программы. Пока!")
            break
            
        else:
            print(" Неверная команда, попробуйте снова.")