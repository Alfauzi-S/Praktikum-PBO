from utils.helper import clear_screen, pause
from menus import product_menu, sale_menu, customer_menu

def staff_dashboard(staff, my_store, customers_db, sales_db):
    while True:
        clear_screen()
        print("=" * 50)
        print(f"  STAFF DASHBOARD: {staff.name}")
        print(f"  Role: {staff.role}")
        print("=" * 50)
        print("1. Store Summary")
        print("2. Process New Sale")
        print("3. Manage Products")
        print("4. Manage Customers")
        print("5. My Profile")
        print("6. Logout")
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
            customer_menu(customers_db)
        elif choice == "5":
            clear_screen()
            staff.show_person_info()
            pause()
        elif choice == "6":
            break
        else:
            print("[!] Invalid choice!")
            pause()