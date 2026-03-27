import csv
from connect import get_connection


def create_table(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)
    conn.commit()
    cur.close()


def insert_from_csv(conn, filename):
    cur = conn.cursor()
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur.execute(
                """
                INSERT INTO phonebook (username, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone) DO NOTHING
                """,
                (row["username"], row["phone"])
            )
    conn.commit()
    cur.close()
    print("CSV data imported.")


def insert_from_console(conn):
    username = input("Enter username: ").strip()
    phone = input("Enter phone: ").strip()

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
        (username, phone)
    )
    conn.commit()
    cur.close()
    print("Contact added.")


def update_contact(conn):
    username = input("Enter username to update: ").strip()
    field = input("Update name or phone? ").strip().lower()
    new_value = input("Enter new value: ").strip()

    cur = conn.cursor()

    if field == "name":
        cur.execute(
            "UPDATE phonebook SET username = %s WHERE username = %s",
            (new_value, username)
        )
    elif field == "phone":
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE username = %s",
            (new_value, username)
        )
    else:
        print("Invalid field.")
        cur.close()
        return

    conn.commit()
    cur.close()
    print("Contact updated.")


def query_contacts(conn):
    choice = input("Search by (all/name/prefix): ").strip().lower()
    cur = conn.cursor()

    if choice == "all":
        cur.execute("SELECT id, username, phone FROM phonebook ORDER BY username")
    elif choice == "name":
        name = input("Enter name: ").strip()
        cur.execute(
            "SELECT id, username, phone FROM phonebook WHERE username ILIKE %s",
            (f"%{name}%",)
        )
    elif choice == "prefix":
        prefix = input("Enter phone prefix: ").strip()
        cur.execute(
            "SELECT id, username, phone FROM phonebook WHERE phone LIKE %s",
            (f"{prefix}%",)
        )
    else:
        print("Invalid query type.")
        cur.close()
        return

    rows = cur.fetchall()
    cur.close()

    if not rows:
        print("No contacts found.")
    else:
        for row in rows:
            print(row)


def delete_contact(conn):
    choice = input("Delete by (name/phone): ").strip().lower()
    value = input("Enter value: ").strip()

    cur = conn.cursor()

    if choice == "name":
        cur.execute("DELETE FROM phonebook WHERE username = %s", (value,))
    elif choice == "phone":
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (value,))
    else:
        print("Invalid delete option.")
        cur.close()
        return

    conn.commit()
    cur.close()
    print("Contact deleted.")


def main():
    conn = None
    try:
        conn = get_connection()
        create_table(conn)

        while True:
            print("\n--- PHONEBOOK MENU ---")
            print("1. Import contacts from CSV")
            print("2. Add contact from console")
            print("3. Update contact")
            print("4. Query contacts")
            print("5. Delete contact")
            print("6. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                insert_from_csv(conn, "contacts.csv")
            elif choice == "2":
                insert_from_console(conn)
            elif choice == "3":
                update_contact(conn)
            elif choice == "4":
                query_contacts(conn)
            elif choice == "5":
                delete_contact(conn)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error:", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()