from utils.helper import clear_screen, pause
from models.sale import Sale

def sale_menu(store, customers_db, sales_db):
    while True:
        clear_screen()
        print("=" * 50)
        print("         SALES MANAGEMENT")
        print("=" * 50)
        print("1. Create New Sale")
        print("2. Show All Sales")
        print("3. View Sale Receipt")
        print("4. Change Tax Rate")
        print("5. Back to Main Menu")
        print("=" * 50)

        choice = input("Choose menu: ")

        if choice == "1":
            create_sale(store, customers_db, sales_db)
        elif choice == "2":
            show_sales(sales_db)
        elif choice == "3":
            view_receipt(sales_db)
        elif choice == "4":
            change_tax()
        elif choice == "5":
            break
        else:
            print("[!] Invalid choice!")
            pause()


def create_sale(store, customers_db, sales_db):
    clear_screen()
    print("\n=== CREATE NEW SALE ===")
    
    if not customers_db:
        print("[!] No customers available. Please register a customer first.")
        pause()
        return
    
    if not store._products:
        print("[!] No products available. Please add products first.")
        pause()
        return
    
    print("\nAvailable Customers:")
    for i, cust in enumerate(customers_db, 1):
        print(f"{i}. {cust.name} ({cust.membership_tier})")
    
    try:
        cust_idx = int(input("\nSelect customer number: ")) - 1
        if cust_idx < 0 or cust_idx >= len(customers_db):
            print("[!] Invalid selection!")
            pause()
            return
        
        customer = customers_db[cust_idx]
        
        sale_id = f"TRX-{len(sales_db) + 1:03d}"
        new_sale = Sale(sale_id, customer)
        
        print("\n--- Add Items to Sale ---")
        store.show_products()
        
        while True:
            prod_id = input("\nEnter Product ID (or 'done' to finish): ").strip()
            
            if prod_id.lower() == 'done':
                break
            
            product = store.get_product(prod_id)
            
            if product:
                try:
                    qty = int(input(f"Quantity for '{product.name}': "))
                    new_sale.add_item(product, qty)
                except ValueError:
                    print("[!] Invalid quantity!")
            else:
                print(f"[!] Product '{prod_id}' not found!")
        
        new_sale.show_items()

        if customer.membership_tier == "Gold":
            new_sale.set_discount(5)
        elif customer.membership_tier == "Platinum":
            new_sale.set_discount(10)
        elif customer.membership_tier == "Silver":
            new_sale.set_discount(1)
        
        if new_sale.items_count > 0:
            if new_sale.process_sale():
                sales_db.append(new_sale)
                print(f"\n[V] Sale {sale_id} completed successfully!")
                new_sale.show_receipt()
            else:
                print(f"\n[!] Failed to process sale.")
        else:
            print(f"\n[!] Sale cancelled (no items added).")
        
    except ValueError:
        print("[!] Invalid input!")
    
    pause()


def show_sales(sales_db):
    clear_screen()
    print("\n=== ALL SALES ===")
    
    if not sales_db:
        print("  No sales recorded yet.")
    else:
        for i, sale in enumerate(sales_db, 1):
            print(f"{i}. {sale.id_sale} - {sale.customer.name} - Rp{sale.total:,.0f}")
    
    print(f"\nTotal Sales: {len(sales_db)}")
    pause()


def view_receipt(sales_db):
    clear_screen()
    print("\n=== VIEW SALE RECEIPT ===")
    
    if not sales_db:
        print("  No sales available.")
        pause()
        return
    
    for i, sale in enumerate(sales_db, 1):
        print(f"{i}. {sale.id_sale} - {sale.customer.name}")
    
    try:
        choice = int(input("\nSelect sale number: ")) - 1
        if 0 <= choice < len(sales_db):
            sales_db[choice].show_receipt()
        else:
            print("[!] Invalid selection!")
    except ValueError:
        print("[!] Invalid input!")
    
    pause()


def change_tax():
    clear_screen()
    print("\n=== CHANGE TAX RATE ===")
    print(f"Current Tax Rate: {Sale.tax}%")
    
    try:
        new_tax = float(input("New tax rate (%): "))
        Sale.change_tax(new_tax)
    except ValueError:
        print("[!] Invalid input!")
    
    pause()