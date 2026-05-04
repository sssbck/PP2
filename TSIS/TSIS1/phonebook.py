import psycopg2, csv, json, os
from connect import get_connection

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (Работа на стороне Python) ---
def clean(val):
    """Очищает ввод от мусора. Если строка пустая - возвращает None (SQL превратит это в NULL)"""
    return str(val).strip() if val and str(val).strip() else None

def setup_db():
    """Синергия: Python сам загружает SQL-файлы в базу при первом запуске"""
    conn = get_connection()
    with conn.cursor() as cur:
        for f_name in ['schema.sql', 'procedures.sql']:
            if os.path.exists(f_name):
                with open(f_name, 'r', encoding='utf-8') as f:
                    cur.execute(f.read())
        conn.commit()
    conn.close()

# --- ЛОГИКА ВЗАИМОДЕЙСТВИЯ (Python + SQL) ---

def add_full_contact():
    name = clean(input("Введите имя: "))
    if not name: return

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # 1. Спрашиваем у базы (SQL делает проверку)
            cur.execute("SELECT is_contact_exists(%s)", (name,))
            
            # Если база ответила True (контакт есть), Python включает UI-логику
            if cur.fetchone()[0]:  
                if input(f"⚠️ Контакт '{name}' уже есть. Перезаписать? (y/n): ").lower() != 'y':
                    print("⏭️ Пропущено.")
                    return
            
            # 2. Собираем остальные данные (чистый UI)
            email = clean(input("Введите email: "))
            birthday = clean(input("Введите дату (ГГГГ-ММ-ДД): "))
            group = clean(input("Введите группу: "))
            phone = clean(input("Введите номер телефона: "))
            p_type = clean(input("Тип (home/work/mobile): "))

            # 3. Отдаем всю работу SQL-процедуре
            cur.execute("CALL upsert_full_contact(%s, %s, %s, %s, %s, %s)", 
                        (name, email, birthday, group, phone, p_type))
            conn.commit()
            print(f"✅ Данные для '{name}' сохранены.")
    finally:
        conn.close()

def check_exists(name):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def show_data(query, params=(), title="Результаты"):
    # Универсальная функция для вывода данных на экран (Поиск, Фильтр, Сортировка)
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()
        print(f"\n--- {title} ---")
        if not rows: print("Пусто.")
        for r in rows: print(" | ".join(str(item) for item in r if item is not None))
    conn.close()

def paginated_navigator():
    # Синергия: Python управляет состоянием (offset), SQL отдает строго кусок данных
    limit, offset = 5, 0
    conn = get_connection()
    while True:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            rows = cur.fetchall()
            print(f"\n--- Страница (Сдвиг: {offset}) ---")
            for r in rows: print(r)
            cmd = input("\n[n]ext (вперед), [p]rev (назад), [q]uit (выход): ").lower()
            if cmd == 'n' and len(rows) == limit: offset += limit
            elif cmd == 'p': offset = max(0, offset - limit)
            elif cmd == 'q': break
    conn.close()

def export_json():
    # Синергия: SQL собирает JSON, Python просто пишет его в файл
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT get_contacts_for_export()")
        data = cur.fetchone()[0]
        with open("contacts.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    conn.close()
    print("✅ Экспортировано в contacts.json")

def import_json():
    # Синергия: Python читает файл, цикл отдает данные в SQL-процедуру
    if not os.path.exists("contacts.json"): return print("❌ Файл не найден.")
    with open("contacts.json", "r", encoding="utf-8") as f: data = json.load(f)
    conn = get_connection()
    with conn.cursor() as cur:
        for c in data:
            phone, ptype = (c['phones'][0].split(':') if c.get('phones') else (None, None))
            cur.execute("CALL upsert_full_contact(%s, %s, %s, %s, %s, %s)", 
                        (clean(c.get('name')), clean(c.get('email')), clean(c.get('birthday')), clean(c.get('group')), phone, ptype))
        conn.commit()
    conn.close()
    print("✅ JSON импортирован.")

def import_csv():
    # Синергия: Python читает файл, цикл отдает данные в SQL-процедуру
    fn = input("Имя CSV файла: ")
    if not os.path.exists(fn): return print("❌ Файл не найден.")
    conn = get_connection()
    with open(fn, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        with conn.cursor() as cur:
            for r in reader:
                name = clean(r.get('name'))
                if name: cur.execute("CALL upsert_full_contact(%s, %s, %s, %s, %s, %s)", 
                                     (name, clean(r.get('email')), clean(r.get('birthday')), clean(r.get('group')), clean(r.get('phone')), clean(r.get('type'))))
            conn.commit()
    conn.close()
    print("✅ CSV импортирован.")

def manage_db(action):
    # Обертка для простых SQL-процедур
    conn = get_connection()
    with conn.cursor() as cur:
        if action == 'add_phone': cur.execute("CALL add_phone(%s, %s, %s)", (clean(input("Имя: ")), clean(input("Тел: ")), clean(input("Тип: "))))
        elif action == 'move': cur.execute("CALL move_to_group(%s, %s)", (clean(input("Имя: ")), clean(input("Группа: "))))
        elif action == 'delete': cur.execute("CALL delete_contact_smart(%s)", (clean(input("Имя или телефон: ")),))
        conn.commit()
    conn.close()
    print("✅ Выполнено.")

# --- ГЛАВНОЕ МЕНЮ ---
def main_menu():
    setup_db()
    while True:
        print("\n" + "="*30 + "\n   TSIS 1: PRO PHONEBOOK\n" + "="*30)
        print("1. Добавить контакт   2. Поиск             3. Фильтр по группе")
        print("4. Пагинация          5. Сортировка        6. Экспорт в JSON")
        print("7. Импорт из JSON     8. Импорт из CSV     9. Добавить телефон")
        print("10. Сменить группу    11. Удалить          0. Выход")
        
        c = input(">> ")
        if c == '1': add_full_contact()
        elif c == '2': show_data("SELECT * FROM search_contacts_extended(%s)", (input("Поиск: "),), "Поиск")
        elif c == '3': show_data("SELECT * FROM get_contacts_by_group(%s)", (input("Группа: "),), "Фильтр")
        elif c == '4': paginated_navigator()
        elif c == '5': show_data("SELECT * FROM get_sorted_contacts(%s)", (int(input("1-Имя, 2-ДР: ")),), "Сортировка")
        elif c == '6': export_json()
        elif c == '7': import_json()
        elif c == '8': import_csv()
        elif c == '9': manage_db('add_phone')
        elif c == '10': manage_db('move')
        elif c == '11': manage_db('delete')
        elif c == '0': break

if __name__ == "__main__":
    main_menu()