from utils.helper import clear_screen, pause
from menus import sale_menu

def customer_dashboard(customer, my_store, customers_db, sales_db):
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