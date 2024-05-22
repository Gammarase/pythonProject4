import sqlite3

# Підключення до бази даних (створює базу даних, якщо вона не існує)
conn = sqlite3.connect('fuel_records.db')
c = conn.cursor()

# Створення таблиці для зберігання даних про витрати пального
c.execute('''CREATE TABLE IF NOT EXISTS fuel_usage (
                id INTEGER PRIMARY KEY,
                date TEXT,
                vehicle_id TEXT,
                fuel_type TEXT,
                quantity REAL,
                cost REAL
            )''')

conn.commit()
conn.close()
