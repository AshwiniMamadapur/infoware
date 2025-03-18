import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ankutanu@32",
            database="NewBillingDB"  # Updated database name
        )
        self.cursor = self.conn.cursor()

    def add_customer(self, name, email, phone):
        sql = "INSERT INTO Customers (name, email, phone) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (name, email, phone))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_bill(self, customer_id, amount):
        sql = "INSERT INTO Bills (customer_id, amount) VALUES (%s, %s)"
        self.cursor.execute(sql, (customer_id, amount))
        self.conn.commit()

    def get_customers(self):
        self.cursor.execute("SELECT * FROM Customers")
        return self.cursor.fetchall()

    def get_bills(self):
        self.cursor.execute("""
            SELECT Bills.id, Customers.name, Bills.amount, Bills.date
            FROM Bills
            JOIN Customers ON Bills.customer_id = Customers.id
        """)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
