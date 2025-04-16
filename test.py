import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from dotenv import load_dotenv
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
category_map = {}  # name -> id

# Load categories from DB
def load_categories():
    cursor.execute("SELECT category_id, name FROM categories")
    results = cursor.fetchall()
    entry_cat['values'] = [row[1] for row in results]
    for cid, name in results:
        category_map[name] = cid

def add_category_popup():
    popup = tk.Toplevel(root)
    popup.title("Add New Category")
    popup.geometry("300x120")
    popup.resizable(False, False)

    ttk.Label(popup, text="New Category Name:").pack(pady=(10, 5))
    entry_new = ttk.Entry(popup)
    entry_new.pack(padx=20, fill="x")

    def submit_new_category():
        new_cat = entry_new.get().strip()
        if new_cat:
            try:
                cursor.execute("INSERT INTO categories (name) VALUES (%s)", (new_cat,))
                conn.commit()
                messagebox.showinfo("Success", f"Category '{new_cat}' added.")
                popup.destroy()
                load_categories()
            except mysql.connector.errors.IntegrityError:
                messagebox.showwarning("Exists", "This category already exists.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Category name cannot be empty.")

    ttk.Button(popup, text="Add Category", command=submit_new_category).pack(pady=10)


# Insert Item Function
def insert_item():
    name = entry_name.get()
    desc = entry_desc.get()
    qty = entry_qty.get()
    price = entry_price.get()
    cat_name = entry_cat.get()
    cat_id = category_map.get(cat_name)

    if name and qty and price and cat_id:
        try:
            cursor.execute("INSERT INTO items (item_name, description, quantity, price, category_id) VALUES (%s, %s, %s, %s, %s)",
                           (name, desc, qty, price, cat_id))
            conn.commit()
            messagebox.showinfo("Success", "Item added successfully!")
            clear_entries()
            view_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill out all required fields (name, qty, price, category).")

# View Items Function
def view_items():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("""
        SELECT i.item_id, i.item_name, i.description, i.quantity, i.price, c.name, i.added_at
        FROM items i
        LEFT JOIN categories c ON i.category_id = c.category_id
    """)
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

# Clear Entry Fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_qty.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_cat.set("")

def update_item():
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        item_id = values[0]
        name = entry_name.get()
        desc = entry_desc.get()
        qty = entry_qty.get()
        price = entry_price.get()
        cat_name = entry_cat.get()
        cat_id = category_map.get(cat_name)

        if name and qty and price and cat_id:
            try:
                cursor.execute("""
                    UPDATE items 
                    SET item_name=%s, description=%s, quantity=%s, price=%s, category_id=%s 
                    WHERE item_id=%s
                """, (name, desc, qty, price, cat_id, item_id))
                conn.commit()
                messagebox.showinfo("Updated", "Item updated successfully!")
                clear_entries()
                view_items()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill out all required fields.")
    else:
        messagebox.showwarning("No selection", "Please select an item to update.")

# GUI Setup
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("800x500")
root.minsize(500, 500)
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

ttk.Label(input_frame, text="Category*").grid(row=2, column=0, padx=5, pady=5)
entry_cat = ttk.Combobox(input_frame, state="readonly")
entry_cat.grid(row=2, column=1, padx=5, pady=5)

# Buttons
button_frame = ttk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=4, pady=10)

ttk.Button(button_frame, text="Add Item", command=insert_item).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Delete Item", command=delete_item).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="Update Item", command=update_item).grid(row=0, column=2, padx=10)
ttk.Button(button_frame, text="Add Category", command=add_category_popup).grid(row=0, column=3, padx=10)

sort_orders = {}

def sort_column(col):
    reverse = sort_orders.get(col, False)
    query = f"SELECT i.item_id, i.item_name, i.description, i.quantity, i.price, c.name, i.added_at FROM items i LEFT JOIN categories c ON i.category_id = c.category_id ORDER BY {col} {'DESC' if reverse else 'ASC'}"
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

load_categories()
view_items()
root.mainloop()
conn.close()
