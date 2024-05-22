import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Підключення до бази даних
conn = sqlite3.connect('fuel_records.db')
c = conn.cursor()

# Функції для роботи з базою даних
def add_record(date, vehicle_id, fuel_type, quantity, cost):
    c.execute('''INSERT INTO fuel_usage (date, vehicle_id, fuel_type, quantity, cost) 
                 VALUES (?, ?, ?, ?, ?)''', (date, vehicle_id, fuel_type, quantity, cost))
    conn.commit()
    messagebox.showinfo("Успіх", "Запис успішно додано")

def search_records(vehicle_id):
    c.execute('''SELECT * FROM fuel_usage WHERE vehicle_id=?''', (vehicle_id,))
    return c.fetchall()

def update_record(record_id, date, vehicle_id, fuel_type, quantity, cost):
    c.execute('''UPDATE fuel_usage 
                 SET date=?, vehicle_id=?, fuel_type=?, quantity=?, cost=? 
                 WHERE id=?''', (date, vehicle_id, fuel_type, quantity, cost, record_id))
    conn.commit()
    messagebox.showinfo("Успіх", "Запис успішно оновлено")

def delete_record(record_id):
    c.execute('''DELETE FROM fuel_usage WHERE id=?''', (record_id,))
    conn.commit()
    messagebox.showinfo("Успіх", "Запис успішно видалено")

def show_all_records():
    c.execute('''SELECT * FROM fuel_usage''')
    records = c.fetchall()
    return pd.DataFrame(records, columns=['ID', 'Date', 'Vehicle ID', 'Fuel Type', 'Quantity', 'Cost'])

def show_statistics():
    stats_window = Toplevel(root)
    stats_window.title("Статистика")

    df = show_all_records()
    summary = df.describe()

    text = Text(stats_window)
    text.pack()
    text.insert(END, summary.to_string())

    # Побудова графіків
    fig, ax = plt.subplots()
    df.groupby('Fuel Type')['Quantity'].sum().plot(kind='bar', ax=ax)
    plt.xlabel('Тип пального')
    plt.ylabel('Загальна кількість (л)')
    plt.title('Розподіл витрат пального за типами')

    canvas = FigureCanvasTkAgg(fig, master=stats_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Графічний інтерфейс користувача
root = Tk()
root.title("Система обліку витрат пального")

def add_record_gui():
    add_window = Toplevel(root)
    add_window.title("Додати запис")

    Label(add_window, text="Дата (YYYY-MM-DD):").grid(row=0, column=0)
    date_entry = Entry(add_window)
    date_entry.grid(row=0, column=1)

    Label(add_window, text="ID ТЗ:").grid(row=1, column=0)
    vehicle_id_entry = Entry(add_window)
    vehicle_id_entry.grid(row=1, column=1)

    Label(add_window, text="Тип пального:").grid(row=2, column=0)
    fuel_type_entry = Entry(add_window)
    fuel_type_entry.grid(row=2, column=1)

    Label(add_window, text="Кількість (л):").grid(row=3, column=0)
    quantity_entry = Entry(add_window)
    quantity_entry.grid(row=3, column=1)

    Label(add_window, text="Вартість (грн):").grid(row=4, column=0)
    cost_entry = Entry(add_window)
    cost_entry.grid(row=4, column=1)

    def save_record():
        add_record(date_entry.get(), vehicle_id_entry.get(), fuel_type_entry.get(), float(quantity_entry.get()), float(cost_entry.get()))
        add_window.destroy()

    Button(add_window, text="Зберегти", command=save_record).grid(row=5, column=0, columnspan=2)

Button(root, text="Додати запис", command=add_record_gui).pack()

def show_records_gui():
    records_window = Toplevel(root)
    records_window.title("Всі записи")

    records = show_all_records()
    text = Text(records_window)
    text.pack()
    text.insert(END, records.to_string())

Button(root, text="Показати всі записи", command=show_records_gui).pack()

def update_record_gui():
    update_window = Toplevel(root)
    update_window.title("Оновити запис")

    Label(update_window, text="ID запису:").grid(row=0, column=0)
    id_entry = Entry(update_window)
    id_entry.grid(row=0, column=1)

    Label(update_window, text="Нова дата (YYYY-MM-DD):").grid(row=1, column=0)
    date_entry = Entry(update_window)
    date_entry.grid(row=1, column=1)

    Label(update_window, text="Новий ID ТЗ:").grid(row=2, column=0)
    vehicle_id_entry = Entry(update_window)
    vehicle_id_entry.grid(row=2, column=1)

    Label(update_window, text="Новий тип пального:").grid(row=3, column=0)
    fuel_type_entry = Entry(update_window)
    fuel_type_entry.grid(row=3, column=1)

    Label(update_window, text="Нова кількість (л):").grid(row=4, column=0)
    quantity_entry = Entry(update_window)
    quantity_entry.grid(row=4, column=1)

    Label(update_window, text="Нова вартість (грн):").grid(row=5, column=0)
    cost_entry = Entry(update_window)
    cost_entry.grid(row=5, column=1)

    def save_updated_record():
        update_record(int(id_entry.get()), date_entry.get(), vehicle_id_entry.get(), fuel_type_entry.get(), float(quantity_entry.get()), float(cost_entry.get()))
        update_window.destroy()

    Button(update_window, text="Оновити", command=save_updated_record).grid(row=6, column=0, columnspan=2)

Button(root, text="Оновити запис", command=update_record_gui).pack()

def delete_record_gui():
    delete_window = Toplevel(root)
    delete_window.title("Видалити запис")

    Label(delete_window, text="ID запису:").grid(row=0, column=0)
    id_entry = Entry(delete_window)
    id_entry.grid(row=0, column=1)

    def delete_selected_record():
        delete_record(int(id_entry.get()))
        delete_window.destroy()

    Button(delete_window, text="Видалити", command=delete_selected_record).grid(row=1, column=0, columnspan=2)

Button(root, text="Видалити запис", command=delete_record_gui).pack()

def search_record_gui():
    search_window = Toplevel(root)
    search_window.title("Пошук запису")

    Label(search_window, text="ID ТЗ:").grid(row=0, column=0)
    vehicle_id_entry = Entry(search_window)
    vehicle_id_entry.grid(row=0, column=1)

    def search_and_display():
        records = search_records(vehicle_id_entry.get())
        text = Text(search_window)
        text.grid(row=2, column=0, columnspan=2)
        if records:
            df = pd.DataFrame(records, columns=['ID', 'Date', 'Vehicle ID', 'Fuel Type', 'Quantity', 'Cost'])
            text.insert(END, df.to_string())
        else:
            text.insert(END, "Записів не знайдено")

    Button(search_window, text="Пошук", command=search_and_display).grid(row=1, column=0, columnspan=2)

Button(root, text="Пошук запису", command=search_record_gui).pack()

Button(root, text="Показати статистику", command=show_statistics).pack()

root.mainloop()

conn.close()
