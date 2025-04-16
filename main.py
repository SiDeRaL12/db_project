import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from dotenv import load_dotenv
import csv
from tkinter import filedialog

import os

load_dotenv()



db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_database")
# Database Connection
conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = conn.cursor()

# Insert Item Function
def insert_item():
    name = entry_name.get()
    desc = entry_desc.get()
    qty = entry_qty.get()
    price = entry_price.get()
    cat = entry_cat.get()

    if name and qty and price:
        try:
            cursor.execute("INSERT INTO items (item_name, description, quantity, price, category) VALUES (%s, %s, %s, %s, %s)",
                           (name, desc, qty, price, cat))
            conn.commit()
            messagebox.showinfo("Success", "Item added successfully!")
            clear_entries()
            view_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill out all required fields (name, qty, price).")

# View Items Function
def view_items():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

# Delete Item Function
def delete_item():
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        item_id = values[0]
        cursor.execute("DELETE FROM items WHERE item_id = %s", (item_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Item deleted successfully!")
        view_items()
    else:
        messagebox.showwarning("No selection", "Please select an item to delete.")

def search_items():
    name_filter = search_name.get()
    cat_filter = search_cat.get()

    query = "SELECT * FROM items WHERE 1=1"
    params = []

    if name_filter:
        query += " AND item_name LIKE %s"
        params.append(f"%{name_filter}%")
    if cat_filter:
        query += " AND category LIKE %s"
        params.append(f"%{cat_filter}%")

    cursor.execute(query, params)
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", tk.END, values=row)

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            cursor.execute("SELECT * FROM items")
            rows = cursor.fetchall()
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                for row in rows:
                    writer.writerow(row)
            messagebox.showinfo("Exported", "Data exported to CSV successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")

# Clear Entry Fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_qty.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_cat.delete(0, tk.END)

def update_item():
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        item_id = values[0]
        name = entry_name.get()
        desc = entry_desc.get()
        qty = entry_qty.get()
        price = entry_price.get()
        cat = entry_cat.get()
        if name and qty and price:
            try:
                cursor.execute("""
                    UPDATE items 
                    SET item_name=%s, description=%s, quantity=%s, price=%s, category=%s 
                    WHERE item_id=%s
                """, (name, desc, qty, price, cat, item_id))
                conn.commit()
                messagebox.showinfo("Updated", "Item updated successfully!")
                clear_entries()
                view_items()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill out all required fields (name, qty, price).")
    else:
        messagebox.showwarning("No selection", "Please select an item to update.")


# GUI Setup
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("800x500")
root.configure(bg="#f0f4f8")
root.option_add("*Font", ("Segoe UI", 10))


# Labels and Entries
input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

ttk.Label(input_frame, text="Item Name*").grid(row=0, column=0, padx=5, pady=5)
entry_name = ttk.Entry(input_frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Description").grid(row=1, column=0, padx=5, pady=5)
entry_desc = ttk.Entry(input_frame)
entry_desc.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Quantity*").grid(row=0, column=2, padx=5, pady=5)
entry_qty = ttk.Entry(input_frame)
entry_qty.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(input_frame, text="Price*").grid(row=1, column=2, padx=5, pady=5)
entry_price = ttk.Entry(input_frame)
entry_price.grid(row=1, column=3, padx=5, pady=5)

ttk.Label(input_frame, text="Category").grid(row=2, column=0, padx=5, pady=5)
entry_cat = ttk.Entry(input_frame)
entry_cat.grid(row=2, column=1, padx=5, pady=5)


# Buttons
button_frame = ttk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=4, pady=10)

ttk.Button(button_frame, text="Add Item", command=insert_item).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Delete Item", command=delete_item).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="Update Item", command=update_item).grid(row=0, column=2, padx=10)
ttk.Label(button_frame, text="Search Name").grid(row=1, column=0, padx=5)
search_name = ttk.Entry(button_frame)
search_name.grid(row=1, column=1, padx=5)

ttk.Label(button_frame, text="Category").grid(row=1, column=2, padx=5)
search_cat = ttk.Entry(button_frame)
search_cat.grid(row=1, column=3, padx=5)

ttk.Button(button_frame, text="Search", command=search_items).grid(row=1, column=4, padx=10)
ttk.Button(button_frame, text="Export CSV", command=export_to_csv).grid(row=1, column=5, padx=10)

sort_orders = {}

def sort_column(col):
    reverse = sort_orders.get(col, False)
    query = f"SELECT * FROM items ORDER BY {col} {'DESC' if reverse else 'ASC'}"
    cursor.execute(query)
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", tk.END, values=row)
    sort_orders[col] = not reverse



# Treeview for Items
columns = ("item_id", "item_name", "description", "quantity", "price", "category", "added_at")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col, command=lambda _col=col: sort_column(_col))
    tree.column(col, width=100)


tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

view_items()
root.mainloop()

# Close connection when app ends
conn.close()