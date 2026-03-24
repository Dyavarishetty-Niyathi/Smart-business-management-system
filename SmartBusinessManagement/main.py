import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import connect_db
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings
warnings.filterwarnings("ignore")

# ------------------- Main App -------------------

class SmartBusinessApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="morph")

        self.title("Smart Business Management System")
        self.geometry("1000x600")
        self.minsize(900, 550)

        self.current_frame = None
        self.show_frame(LoginPage)

    def show_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)


# ------------------- Login Page -------------------

class LoginPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        container = ttk.Frame(self, padding=40)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(container,
                  text="Smart Business Management",
                  font=("Segoe UI", 22, "bold")).pack(pady=10)

        ttk.Label(container, text="Login to Continue",
                  font=("Segoe UI", 12)).pack(pady=5)

        self.username = ttk.Entry(container, width=30)
        self.username.pack(pady=10)

        self.password = ttk.Entry(container, width=30, show="*")
        self.password.pack(pady=10)

        ttk.Button(container,
                   text="Login",
                   bootstyle="success",
                   width=25,
                   command=self.login).pack(pady=15)

        ttk.Button(container,
                   text="Register New Business",
                   bootstyle="secondary",
                   width=25,
                   command=lambda: master.show_frame(RegisterPage)).pack()

    def login(self):
        conn = connect_db()
        cursor = conn.cursor()

        sql = "SELECT * FROM business WHERE username=%s AND password=%s"
        cursor.execute(sql, (self.username.get(), self.password.get()))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", "Login Successful!")
            self.master.show_frame(Dashboard)
        else:
            messagebox.showerror("Error", "Invalid Username or Password")


# ------------------- Register Page -------------------

class RegisterPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        container = ttk.Frame(self, padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(container,
                  text="Register Your Business",
                  font=("Segoe UI", 20, "bold")).pack(pady=15)

        fields = ["Business Name", "Owner Name", "Email",
                  "Phone Number", "Username", "Password"]

        self.entries = {}

        for field in fields:
            ttk.Label(container, text=field).pack()
            entry = ttk.Entry(container, width=35)
            entry.pack(pady=5)
            self.entries[field] = entry

        ttk.Button(container,
                   text="Register",
                   bootstyle="primary",
                   width=25,
                   command=self.register_business).pack(pady=15)

        ttk.Button(container,
                   text="Back to Login",
                   bootstyle="secondary",
                   width=25,
                   command=lambda: master.show_frame(LoginPage)).pack()

    def register_business(self):
        conn = connect_db()
        cursor = conn.cursor()

        sql = """
        INSERT INTO business 
        (business_name, owner_name, email, phone, username, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            self.entries["Business Name"].get(),
            self.entries["Owner Name"].get(),
            self.entries["Email"].get(),
            self.entries["Phone Number"].get(),
            self.entries["Username"].get(),
            self.entries["Password"].get()
        )

        try:
            cursor.execute(sql, values)
            conn.commit()
            messagebox.showinfo("Success", "Business Registered Successfully!")
            self.master.show_frame(LoginPage)
        except:
            messagebox.showerror("Error", "Username already exists!")
        conn.close()


# ------------------- Dashboard -------------------

class Dashboard(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        sidebar = ttk.Frame(self, padding=20)
        sidebar.pack(side="left", fill="y")

        ttk.Label(sidebar,
                  text="Dashboard",
                  font=("Segoe UI", 16, "bold"),
                  foreground="white").pack(pady=20)

        buttons = [
            ("Project Info", ProjectInfo),
            ("Customer Info", CustomerInfo),
            ("Sales Entry", SalesEntry),
            ("Sales Analysis", SalesAnalysis),
            ("Product Management", ProductManagement),
            ("Logout", LoginPage)
        ]

        for text, page in buttons:
            ttk.Button(sidebar,
                       text=text,
                       bootstyle="light",
                       width=20,
                       command=lambda p=page: master.show_frame(p)).pack(pady=8)

        main_area = ttk.Frame(self, padding=40)
        main_area.pack(side="right", fill="both", expand=True)

        ttk.Label(main_area,
                  text="Welcome to Smart Business Dashboard",
                  font=("Segoe UI", 24, "bold")).pack(pady=20)

        card_frame = ttk.Frame(main_area)
        card_frame.pack(pady=30)

        self.create_card(card_frame, "Total Products", self.get_product_count())
        self.create_card(card_frame, "Total Sales", self.get_total_sales())

    def create_card(self, parent, title, value):
        card = ttk.Frame(parent, padding=20)
        card.pack(side="left", padx=20)

        ttk.Label(card, text=title,
                  font=("Segoe UI", 12)).pack()
        ttk.Label(card, text=value,
                  font=("Segoe UI", 18, "bold")).pack()

    def get_product_count(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_total_sales(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT IFNULL(SUM(total_amount),0) FROM sales")
        total = cursor.fetchone()[0]
        conn.close()
        return f"₹ {total}"


# ------------------- Project Info -------------------

class ProjectInfo(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        ttk.Label(self,
                  text="Project Information",
                  font=("Segoe UI", 20, "bold")).pack(pady=30)

        info = """
Smart Business Management System

This application is designed to help small businesses efficiently manage their operations.

Key Features:
• Business registration and secure login system
• Product management (add, view, update stock)
• Customer management system
• Sales entry with automatic bill calculation
• Automatic stock reduction after each sale
• Real-time data stored using MySQL database

Analytics Features:
• Total revenue calculation
• Product-wise sales analysis
• Tabular data representation
• Graphical visualization using charts

Advantages:
• Reduces manual errors
• Improves business tracking
• Provides data-driven insights
• Easy to use desktop application

This system demonstrates integration of:
Python + Tkinter + MySQL + Pandas + Matplotlib
        """

        ttk.Label(self,
                  text=info,
                  font=("Segoe UI", 11),
                  justify="left").pack(pady=20)

        ttk.Button(self,
                   text="Back",
                   command=lambda: master.show_frame(Dashboard)).pack()
        
# ------------------customer info--------------------        
class CustomerInfo(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        ttk.Label(self,
                  text="Customer Management",
                  font=("Segoe UI", 20, "bold")).pack(pady=20)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Customer Name").grid(row=0, column=0)
        self.name = ttk.Entry(form)
        self.name.grid(row=0, column=1)

        ttk.Label(form, text="Phone").grid(row=1, column=0)
        self.phone = ttk.Entry(form)
        self.phone.grid(row=1, column=1)

        ttk.Label(form, text="Email").grid(row=2, column=0)
        self.email = ttk.Entry(form)
        self.email.grid(row=2, column=1)

        ttk.Button(form,
                   text="Add Customer",
                   command=self.add_customer).grid(row=3, columnspan=2, pady=10)

        columns = ("ID", "Name", "Phone", "Email")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=20)

        self.load_customers()

        ttk.Button(self,
                   text="Back",
                   command=lambda: master.show_frame(Dashboard)).pack()

    def add_customer(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO customers (business_id, customer_name, phone, email)
            VALUES (1, %s, %s, %s)
        """, (self.name.get(), self.phone.get(), self.email.get()))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Customer Added")
        self.load_customers()

    def load_customers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, customer_name, phone, email FROM customers")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

# ---------------------sales entry-------------------------
class SalesEntry(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        ttk.Label(self,
                  text="Sales Entry",
                  font=("Segoe UI", 20, "bold")).pack(pady=20)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT customer_id, customer_name FROM customers")
        self.customers = cursor.fetchall()

        cursor.execute("SELECT product_id, product_name, price FROM products")
        self.products = cursor.fetchall()

        conn.close()

        # Dropdowns
        ttk.Label(self, text="Select Customer").pack()
        self.customer_combo = ttk.Combobox(self,
            values=[c[1] for c in self.customers])
        self.customer_combo.pack(pady=5)

        ttk.Label(self, text="Select Product").pack()
        self.product_combo = ttk.Combobox(self,
            values=[p[1] for p in self.products])
        self.product_combo.pack(pady=5)

        ttk.Label(self, text="Quantity").pack()
        self.quantity = ttk.Entry(self)
        self.quantity.pack(pady=5)

        ttk.Button(self,
                   text="Save Sale",
                   command=self.save_sale).pack(pady=10)

        ttk.Button(self,
                   text="Back",
                   command=lambda: master.show_frame(Dashboard)).pack()

    def save_sale(self):
        customer_name = self.customer_combo.get()
        product_name = self.product_combo.get()
        qty = int(self.quantity.get())

        customer_id = next(c[0] for c in self.customers if c[1] == customer_name)
        product = next(p for p in self.products if p[1] == product_name)
        product_id = product[0]
        price = float(product[2])

        total = qty * price

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sales (business_id, customer_id, product_id, quantity_sold, total_amount)
            VALUES (1, %s, %s, %s, %s)
        """, (customer_id, product_id, qty, total))

        # Reduce stock
        cursor.execute("""
            UPDATE products
            SET quantity = quantity - %s
            WHERE product_id = %s
        """, (qty, product_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Sale Recorded Successfully!")



# ------------------- Sales Analysis -------------------

class SalesAnalysis(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        ttk.Label(self,
                  text="Sales Analysis",
                  font=("Segoe UI", 20, "bold")).pack(pady=20)

        conn = connect_db()

        query = """
        SELECT p.product_name, s.quantity_sold, s.total_amount, s.sale_date
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        """

        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            ttk.Label(self, text="No Sales Data Available").pack()
            ttk.Button(self, text="Back",
                       command=lambda: master.show_frame(Dashboard)).pack()
            return

        total_sales = df["total_amount"].sum()
        total_transactions = len(df)

        ttk.Label(self, text=f"Total Revenue: ₹ {total_sales}",
                  font=("Segoe UI", 14)).pack()

        ttk.Label(self, text=f"Total Transactions: {total_transactions}",
                  font=("Segoe UI", 14)).pack()

        product_summary = df.groupby("product_name")["total_amount"].sum().reset_index()

        # graph code
        fig, ax = plt.subplots(figsize=(7, 4))

        ax.bar(product_summary["product_name"],
             product_summary["total_amount"])

        ax.set_title("Revenue by Product")
        ax.set_xlabel("Products")
        ax.set_ylabel("Revenue")

        plt.xticks(rotation=30)
        plt.tight_layout()

        canvas= FigureCanvasTkAgg(fig,master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

        ttk.Button(self,text="Back",command=lambda:master.show_frame(Dashboard)).pack(pady=10)

# ------------------product management----------------------------

class ProductManagement(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        ttk.Label(self,
                  text="Product Management",
                  font=("Segoe UI", 20, "bold")).pack(pady=20)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Product Name").grid(row=0, column=0)
        self.name = ttk.Entry(form_frame)
        self.name.grid(row=0, column=1)

        ttk.Label(form_frame, text="Price").grid(row=1, column=0)
        self.price = ttk.Entry(form_frame)
        self.price.grid(row=1, column=1)

        ttk.Label(form_frame, text="Quantity").grid(row=2, column=0)
        self.quantity = ttk.Entry(form_frame)
        self.quantity.grid(row=2, column=1)

        ttk.Button(form_frame,
                   text="Add Product",
                   command=self.add_product).grid(row=3, columnspan=2, pady=10)

        # Table
        columns = ("ID", "Name", "Price", "Quantity")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=20)

        self.load_products()

        ttk.Button(self,
                   text="Back",
                   command=lambda: master.show_frame(Dashboard)).pack()

    def add_product(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO products (business_id, product_name, price, quantity)
            VALUES (1, %s, %s, %s)
        """, (self.name.get(), self.price.get(), self.quantity.get()))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product Added")
        self.load_products()

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, product_name, price, quantity FROM products")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)



# ------------------- Run -------------------

if __name__ == "__main__":
    app = SmartBusinessApp()
    app.mainloop()