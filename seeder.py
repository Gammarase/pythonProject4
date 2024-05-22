from datetime import datetime, timedelta
import sqlite3
import random

conn = sqlite3.connect('fuel_records.db')
c = conn.cursor()

# Функції для роботи з базою даних
def add_record(date, vehicle_id, fuel_type, quantity, cost):
    c.execute('''INSERT INTO fuel_usage (date, vehicle_id, fuel_type, quantity, cost) 
                 VALUES (?, ?, ?, ?, ?)''', (date, vehicle_id, fuel_type, quantity, cost))
    conn.commit()
    return "Успіх", "Запис успішно додано"


def seed_database(num_records):
    fuel_types = ['Petrol', 'Diesel', 'Gas']
    start_date = datetime.now() - timedelta(days=365)
    for _ in range(num_records):
        date = start_date + timedelta(days=random.randint(0, 365))
        vehicle_id = f'VEH{random.randint(1, 10)}'
        fuel_type = random.choice(fuel_types)
        quantity = round(random.uniform(10, 100), 2)
        cost = round(quantity * random.uniform(1.5, 2.0), 2)
        add_record(date.strftime('%Y-%m-%d'), vehicle_id, fuel_type, quantity, cost)
    return "Успіх", f"{num_records} записів успішно додано"

if __name__ == '__main__':
    seed_database(100)

conn.close()
