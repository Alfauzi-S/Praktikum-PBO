import sys
import os

# Tambahkan path root ke sys.path agar import bekerja
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.person import Person
from models.customer import Customer
from models.staff import Staff
from models.product import Product
from models.store import Store
from models.sale import Sale
from menus import product_menu, customer_menu, sale_menu, testing_menu
from utils import clear_screen, pause

# INISIALISASI STORE (Agregasi: Induk)
my_store = Store("Alfauzi Computer Store", "Samarinda")

# INISIALISASI PRODUCT (Objek untuk Agregasi & Komposisi)
prod1 = Product("P001", "Mechanical Keyboard", 750000, 10, "Peripheral")
prod2 = Product("P002", "Gaming Mouse", 350000, 15, "Peripheral")
prod3 = Product("P003", "Monitor 24 inch", 2500000, 5, "Monitor")

# Agregasi Produk ditambahkan ke Store (Siklus hidup mandiri)
my_store.add_product(prod1)
my_store.add_product(prod2)
my_store.add_product(prod3)


# INISIALISASI STAFF (Inheritance dari Person)
# Default admin untuk login mudah
admin_staff = Staff(
    name="Admin Utama", username="admin", password="admin123",
    employee_id="EMP000", role="Manager", salary=15000000,
    phone="081111111111", gmail="admin@alfauzi.com"
)

staff1 = Staff(
    name="Budi Santoso", username="budi_kasir", password="pass123",
    employee_id="EMP001", role="Kasir", salary=4500000,
    phone="081234567890", gmail="budi@gmail.com", birth_date="1998-05-10", gender="Male"
)

staff2 = Staff(
    name="Siti Aminah", username="siti_teknisi", password="pass123",
    employee_id="EMP002", role="Teknisi", salary=6000000,
    phone="081345678901", gmail="siti@gmail.com", birth_date="1999-08-15", gender="Female"
)

staff3 = Staff(
    name="Andi Wijaya", username="andi_manager", password="pass123",
    employee_id="EMP003", role="Manager", salary=12000000,
    phone="081456789012", gmail="andi@gmail.com", birth_date="1990-01-20", gender="Male"
)

# Agregasi: Staff ditambahkan ke Store
my_store.add_staff(admin_staff)
my_store.add_staff(staff1)
my_store.add_staff(staff2)
my_store.add_staff(staff3)

# INISIALISASI CUSTOMER (Inheritance dari Person)
cust1 = Customer(
    id_customer="C001", name="Rina Marlina", username="rina_m", password="password1",
    address="Jl. Pahlawan No. 10", phone="085678901234", gmail="rina@yahoo.com",
    birth_date="1999-05-12", gender="Female", membership_tier="Silver"
)

cust2 = Customer(
    id_customer="C002", name="Daffa Pratama", username="daffa_p", password="password2",
    address="Jl. Ahmad Yani No. 5", phone="085789012345", gmail="daffa@gmail.com",
    birth_date="2000-08-20", gender="Male", membership_tier="Gold"
)

cust3 = Customer(
    id_customer="C003", name="Nadia Putri", username="nadia_putri", password="password3",
    address="Jl. Diponegoro No. 88", phone="085890123456", gmail="nadia@outlook.com",
    birth_date="2001-01-15", gender="Female", membership_tier="Bronze"
)

customers_db = [cust1, cust2, cust3]
staffs_db = [admin_staff, staff1, staff2, staff3]
sales_db = []

# --- TRANSAKSI 1 ---
sale1 = Sale("TRX-001", cust1)
sale1.add_item(prod1, 1)
sale1.add_item(prod2, 2)
staff1.process_transaction(sale1)
sales_db.append(sale1)

# --- TRANSAKSI 2 ---
sale2 = Sale("TRX-002", cust2)
sale2.add_item(prod3, 1)
staff2.process_transaction(sale2)
sales_db.append(sale2)

# --- TRANSAKSI 3 ---
sale3 = Sale("TRX-003", cust3)
sale3.add_item(prod1, 1)
sale3.add_item(prod3, 1)
staff3.process_transaction(sale3)
sales_db.append(sale3)


# FUNGSI AUTHENTIKASI & DASHBOARD
def login():
    clear_screen()
    print("=" * 50)
    print("              LOGIN")
    print("=" * 50)
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    for staff in staffs_db:
        if staff.username == username and staff.password == password:
            return staff, "staff"
    
    for cust in customers_db:
        if cust.username == username and cust.password == password:
            return cust, "customer"
    
    return None, None


def staff_dashboard(staff):
    while True:
        clear_screen()
        print("=" * 50)
        print(f"  STAFF DASHBOARD: {staff.name}")
        print(f"  Role: {staff.role}")
        print("=" * 50)
        print("1. Store Summary")
        print("2. Process New Sale")
        print("3. Manage Products")
        print("4. My Profile")
        print("5. Logout")
        print("=" * 50)
        
        choice = input("Choose menu: ")
        
        if choice == "1":
            clear_screen()
            my_store.show_summary()
            pause()
        elif choice == "2":
            sale_menu(my_store, customers_db, sales_db)
        elif choice == "3":
            product_menu(my_store)
        elif choice == "4":
            clear_screen()
            staff.show_person_info()
            pause()
        elif choice == "5":
            break
        else:
            print("[!] Invalid choice!")
            pause()


def customer_dashboard(customer):
    while True:
        clear_screen()
        print("=" * 50)
        print(f"  CUSTOMER DASHBOARD: {customer.name}")
        print(f"  Membership: {customer.membership_tier}")
        print(f"  Points: {customer.loyalty_points}")
        print("=" * 50)
        print("1. View Products")
        print("2. Buy Product")
        print("3. My Profile")
        print("4. Logout")
        print("=" * 50)
        
        choice = input("Choose menu: ")
        
        if choice == "1":
            clear_screen()
            my_store.show_products()
            pause()
        elif choice == "2":
            sale_menu(my_store, customers_db, sales_db)
        elif choice == "3":
            clear_screen()
            customer.show_person_info()
            pause()
        elif choice == "4":
            break
        else:
            print("[!] Invalid choice!")
            pause()


def main():
    while True:
        clear_screen()
        print("=" * 50)
        print("  COMPUTER SALES MANAGEMENT SYSTEM")
        print("=" * 50)
        print(f"Store: {my_store.name}")
        print(f"Location: {my_store.location}")
        print("=" * 50)
        print("1. Login")
        print("2. Register as Customer")
        print("3. OOP Testing")
        print("4. Exit")
        print("=" * 50)
        
        choice = input("Choose menu: ")
        
        if choice == "1":
            user, role = login()
            if user:
                print(f"\n[V] Login successful! Welcome, {user.name}.")
                pause()
                if role == "staff":
                    staff_dashboard(user)
                else:
                    customer_dashboard(user)
            else:
                print("\n[!] Invalid username or password!")
                pause()
        
        elif choice == "2":
            customer_menu(customers_db)
        
        elif choice == "3":
            testing_menu(
                my_store._products, 
                customers_db, 
                sales_db, 
                Product, 
                Customer, 
                Sale,
                store=my_store
            )
        
        elif choice == "4":
            clear_screen()
            print("Thank you for using Computer Sales Management System!")
            break
        
        else:
            print("[!] Invalid choice!")
            pause()


if __name__ == "__main__":
    main()