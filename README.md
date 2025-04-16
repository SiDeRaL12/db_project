#  Inventory Management System

This is a simple desktop-based Inventory Management System built with **Python (Tkinter)** and **MySQL**. It allows users to manage products efficiently, providing CRUD operations and some bonus features for a more realistic application.

---

##  Features

- **Add** new inventory items (name, description, quantity, price, category)
- **View** all items in a sortable table
- **Update** and **delete** selected items
- **Search/filter** items by name or category
- **Export** inventory data to CSV
- **User authentication** (basic login before accessing the app)
- **Environment variable support** for secure database configuration using `.env`

---

##  Technologies Used

- Python 3.x
- Tkinter (GUI)
- MySQL (Database)
- `dotenv` for environment variable loading
- `csv` for export functionality


---

##  How to Run

1. Set up the MySQL database using `create_tables.sql`.
2. Create a `.env` file with your DB credentials (see `.env.example`).
3. Install required Python packages:
   ```bash
   pip install mysql-connector-python python-dotenv

### `create_tables.sql`

```sql
CREATE DATABASE IF NOT EXISTS inventory_db;

USE inventory_db;

-- Items table
CREATE TABLE IF NOT EXISTS items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);