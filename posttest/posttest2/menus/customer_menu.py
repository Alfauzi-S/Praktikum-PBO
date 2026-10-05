from utils.helper import clear_screen, pause
from models.customer import Customer

def customer_menu(customers_db):
    while True:
        clear_screen()
        print("=" * 50)
        print("         CUSTOMER MANAGEMENT")
        print("=" * 50)
        print("1. Show All Customers")
        print("2. Add New Customer")
        print("3. Change Customer Info")
        print("4. View Customer Details")
        print("5. Back to Main Menu")
        print("=" * 50)

        choice = input("Choose menu: ")

        if choice == "1":
            show_customers(customers_db)
        elif choice == "2":
            add_customer(customers_db)
        elif choice == "3":
            change_customer_info(customers_db)
        elif choice == "4":
            view_customer_details(customers_db)
        elif choice == "5":
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
            print(f"{i}. {cust.name} ({cust.membership_tier}) - Points: {cust.loyalty_points}")
    
    print(f"\nTotal Customers: {len(customers_db)}")
    pause()


def add_customer(customers_db):
    """Mendaftarkan customer baru."""
    clear_screen()
    print("\n=== REGISTER NEW CUSTOMER ===")
    
    try:
        name = input("Full Name: ").strip()
        username = input("Username: ").strip()
        password = input("Password (min 6 chars): ").strip()
        phone = input("Phone Number: ").strip()
        gmail = input("Email: ").strip()
        address = input("Address: ").strip()
        birth_date = input("Birth Date (YYYY-MM-DD, optional): ").strip()
        gender = input("Gender (Male/Female, optional): ").strip()
        
        id_customer = f"C{len(customers_db) + 1:03d}"
        new_customer = Customer(
            id_customer=id_customer,
            name=name,
            username=username,
            password=password,
            address=address,
            phone=phone,
            gmail=gmail,
            birth_date=birth_date,
            gender=gender
        )
        
        customers_db.append(new_customer)
        print(f"\n[V] Customer '{name}' registered successfully!")
        print(f"    Customer ID: {id_customer}")
        
    except ValueError as e:
        print(f"\n[!] Error: {e}")
    
    pause()


def change_customer_info(customers_db):
    """Mengubah informasi customer."""
    clear_screen()
    print("\n=== CHANGE CUSTOMER INFO ===")
    
    if not customers_db:
        print("  No customers available.")
        pause()
        return
    
    for i, cust in enumerate(customers_db, 1):
        print(f"{i}. {cust.name} ({cust.username})")
    
    try:
        choice = int(input("\nSelect customer number: ")) - 1
        if 0 <= choice < len(customers_db):
            customer = customers_db[choice]
            
            print(f"\n--- Editing: {customer.name} ---")
            print("1. Change Phone")
            print("2. Change Gmail")
            print("3. Change Address")
            print("4. Back")
            
            sub_choice = input("Choose: ")
            
            if sub_choice == "1":
                new_phone = input("New phone number: ").strip()
                customer.change_phone(new_phone)
            elif sub_choice == "2":
                password = input("Enter current password to verify: ").strip()
                new_gmail = input("New gmail: ").strip()
                customer.change_gmail(password, new_gmail)
            elif sub_choice == "3":
                new_address = input("New address: ").strip()
                customer.address = new_address
                print(f"[V] Address changed successfully.")
            elif sub_choice == "4":
                return
            else:
                print("[!] Invalid choice!")
        else:
            print("[!] Invalid selection!")
            
    except ValueError:
        print("[!] Invalid input!")
    
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
            customer = customers_db[choice]
            print("\n--- Customer Details ---")
            customer.show_person_info()
        else:
            print("[!] Invalid selection!")
    except ValueError:
        print("[!] Invalid input!")
    
    pause()