from utils.helper import clear_screen, pause
from models.sale import Sale
from models.customer import Customer


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
            buy_product(customer, my_store, sales_db)
            
        elif choice == "3":
            clear_screen()
            customer.show_person_info()
            pause()
            
        elif choice == "4":
            break
            
        else:
            print("[!] Invalid choice!")
            pause()


def buy_product(customer, my_store, sales_db):
    clear_screen()
    print("=" * 50)
    print("             SHOPPING")
    print("=" * 50)
    
    my_store.show_products()
    
    prod_id = input("\nEnter Product ID to buy (or 'cancel' to go back): ").strip()
    
    if prod_id.lower() == 'cancel':
        return
        
    product = my_store.get_product(prod_id)
    if not product:
        print(f"[!] Product '{prod_id}' not found!")
        pause()
        return
        
    try:
        qty = int(input(f"Enter quantity for '{product.name}': "))
        if qty <= 0:
            print("[!] Quantity must be greater than 0!")
            pause()
            return
    except ValueError:
        print("[!] Invalid quantity! Please enter a number.")
        pause()
        return
        
    new_sale = Sale(f"TRX-CUST-{len(sales_db) + 1:03d}", customer)

    success = new_sale.add_item(product, qty)
    
    if not success:
        print("[!] Purchase failed.")
        pause()
        return
        
    subtotal = sum(item.subtotal for item in new_sale._items)
    discount_amount = Customer.calculate_discount(subtotal, customer.membership_tier)
    
    discount_percentage = int((discount_amount / subtotal) * 100) if subtotal > 0 else 0
    new_sale.set_discount(discount_percentage)
    
    print("\n--- Order Summary ---")
    new_sale.show_items()
    
    confirm = input("Confirm purchase? (y/n): ").strip().lower()
    
    if confirm == 'y':
        if new_sale.process_sale():
            sales_db.append(new_sale)
            print("\n[V] Purchase successful! Thank you for shopping with us.")
            new_sale.show_receipt()
        else:
            print("\n[!] Failed to process purchase.")
    else:
        print("\n[!] Purchase cancelled.")
        product.add_stock(qty)
        print(f"[+] Stock for '{product.name}' restored.")
        
    pause()