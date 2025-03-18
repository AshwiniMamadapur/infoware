from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox
)
from database import Database

class BillingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing System")
        self.setGeometry(100, 100, 600, 400)
        self.db = Database()

        layout = QVBoxLayout()

        # Customer Fields
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Customer Name")
        layout.addWidget(self.name_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Phone")
        layout.addWidget(self.phone_input)

        # Add Customer Button
        self.add_customer_btn = QPushButton("Add Customer", self)
        self.add_customer_btn.clicked.connect(self.add_customer)
        layout.addWidget(self.add_customer_btn)

        # Bill Fields
        self.customer_dropdown = QComboBox(self)
        layout.addWidget(self.customer_dropdown)

        self.bill_amount_input = QLineEdit(self)
        self.bill_amount_input.setPlaceholderText("Bill Amount")
        layout.addWidget(self.bill_amount_input)

        self.add_bill_btn = QPushButton("Add Bill", self)
        self.add_bill_btn.clicked.connect(self.add_bill)
        layout.addWidget(self.add_bill_btn)

        # Display Customers
        self.customer_table = QTableWidget(self)
        self.customer_table.setColumnCount(3)
        self.customer_table.setHorizontalHeaderLabels(["ID", "Name", "Email"])
        layout.addWidget(self.customer_table)

        # Display Bills
        self.bill_table = QTableWidget(self)
        self.bill_table.setColumnCount(4)
        self.bill_table.setHorizontalHeaderLabels(["ID", "Customer", "Amount", "Date"])
        layout.addWidget(self.bill_table)

        self.setLayout(layout)
        self.load_data()

    def add_customer(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        if name and email and phone:
            customer_id = self.db.add_customer(name, email, phone)
            self.load_data()

    def add_bill(self):
        customer_id = self.customer_dropdown.currentData()
        amount = self.bill_amount_input.text()
        if customer_id and amount:
            self.db.add_bill(customer_id, float(amount))
            self.load_data()

    def load_data(self):
        # Load customers
        customers = self.db.get_customers()
        self.customer_table.setRowCount(len(customers))
        self.customer_dropdown.clear()
        for row, customer in enumerate(customers):
            self.customer_table.setItem(row, 0, QTableWidgetItem(str(customer[0])))
            self.customer_table.setItem(row, 1, QTableWidgetItem(customer[1]))
            self.customer_table.setItem(row, 2, QTableWidgetItem(customer[2]))
            self.customer_dropdown.addItem(customer[1], customer[0])  # Add to dropdown

        # Load bills
        bills = self.db.get_bills()
        self.bill_table.setRowCount(len(bills))
        for row, bill in enumerate(bills):
            for col, data in enumerate(bill):
                self.bill_table.setItem(row, col, QTableWidgetItem(str(data)))

if __name__ == "__main__":
    app = QApplication([])
    window = BillingApp()
    window.show()
    app.exec()
