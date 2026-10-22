from utils.helper import clear_screen, pause
from models.customer import Customer

def customer_menu(customers_db):
    while True:
        clear_screen()
        print("=" * 50)
        print("         CUSTOMER MANAGEMENT (STAFF)")
        print("=" * 50)
        print("1. View All Customers")
        print("2. Add New Customer")
        print("3. View Customer Details")
        print("4. Back to Staff Dashboard")
        print("=" * 50)

        choice = input("Choose menu: ")

        if choice == "1":
            show_customers(customers_db)
        elif choice == "2":
            add_customer(customers_db)
        elif choice == "3":
            view_customer_details(customers_db)
        elif choice == "4":
            break
        else:
            print("[!] Invalid choice!")
            pause()


def show_customers(customers_db):
    clear_screen()
    print("\n=== ALL CUSTOMERS ===")
    if not customers_db:
        print("  No customers registered yet.")
    else:
        for i, cust in enumerate(customers_db, 1):
            print(f"{i}. {cust.name} ({cust.username}) - Tier: {cust.membership_tier} | Points: {cust.loyalty_points}")
    
    print(f"\nTotal Customers: {len(customers_db)}")
    pause()


def add_customer(customers_db):
    clear_screen()
    print("\n=== ADD NEW CUSTOMER ===")
    try:
        name = input("Full Name: ").strip()
        username = input("Username: ").strip()
        
        if any(c.username == username for c in customers_db):
            print(f"[!] Username '{username}' already exists!")
            pause()
            return
            
        password = input("Password (min 6 chars): ").strip()
        if len(password) < 6:
            print("[!] Password must be at least 6 characters!")
            pause()
            return
            
        phone = input("Phone Number: ").strip()
        gmail = input("Email: ").strip()
        address = input("Address: ").strip()
        new_id = f"C{len(customers_db) + 1:03d}"
        
        new_customer = Customer(
            id_customer=new_id,
            name=name,
            username=username,
            password=password,
            phone=phone,
            gmail=gmail,
            address=address
        )
        
        customers_db.append(new_customer)
        print(f"\n[V] Customer '{name}' added successfully!")
        
    except ValueError as e:
        print(f"\n[!] Error: {e}")
    
    pause()


def view_customer_details(customers_db):
    clear_screen()
    print("\n=== VIEW CUSTOMER DETAILS ===")
    if not customers_db:
        print("  No customers available.")
        pause()
        return
    
    for i, cust in enumerate(customers_db, 1):
        print(f"{i}. {cust.name}")
    
    try:
        choice = int(input("\nSelect customer number: ")) - 1
        if 0 <= choice < len(customers_db):
            print("\n--- Customer Details ---")
            customers_db[choice].show_person_info()
        else:
            print("[!] Invalid selection!")
    except ValueError:
        print("[!] Invalid input!")
    
    pause()