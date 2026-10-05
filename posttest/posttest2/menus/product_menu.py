from utils.helper import clear_screen, pause
from models.product import Product


def product_menu(store):
    while True:
        clear_screen()
        print("=" * 50)
        print("         PRODUCT MANAGEMENT")
        print("=" * 50)
        print("1. Show All Products")
        print("2. Add New Product")
        print("3. Add Stock")
        print("4. Reduce Stock")
        print("5. Manage Categories")
        print("6. Back to Main Menu")
        print("=" * 50)

        choice = input("Choose menu: ")

        if choice == "1":
            show_products(store)
        elif choice == "2":
            add_product(store)
        elif choice == "3":
            add_stock(store)
        elif choice == "4":
            reduce_stock(store)
        elif choice == "5":
            manage_categories()
        elif choice == "6":
            break
        else:
            print("[!] Invalid choice!")
            pause()


def show_products(store):
    clear_screen()
    print("\n=== ALL PRODUCTS ===")
    store.show_products()
    pause()


def add_product(store):
    clear_screen()
    print("\n=== ADD NEW PRODUCT ===")
    
    try:
        id_product = input("Product ID (e.g., P004): ").strip()
        
        if store.get_product(id_product):
            print(f"[!] Product with ID '{id_product}' already exists!")
            pause()
            return
        
        name = input("Product Name: ").strip()
        price = float(input("Price (Rp): "))
        stock = int(input("Stock: "))
        
        from models.product import Product
        print(f"\nAvailable Categories: {', '.join(Product.VALID_CATEGORIES)}")
        category = input("Category: ").strip()
        new_product = Product(id_product, name, price, stock, category)
        if store.add_product(new_product):
            print(f"\n[V] Product '{name}' successfully added to {store.name}!")
        else:
            print(f"\n[!] Failed to add product.")
            
    except ValueError as e:
        print(f"\n[!] Error: {e}")
    
    pause()


def add_stock(store):
    clear_screen()
    print("\n=== ADD STOCK ===")
    
    store.show_products()
    
    id_product = input("Enter Product ID: ").strip()
    product = store.get_product(id_product)
    
    if product:
        try:
            qty = int(input(f"Quantity to add for '{product.name}': "))
            product.add_stock(qty)
        except ValueError as e:
            print(f"[!] Error: {e}")
    else:
        print(f"[!] Product '{id_product}' not found!")
    
    pause()


def reduce_stock(store):
    clear_screen()
    print("\n=== REDUCE STOCK ===")
    
    store.show_products()
    
    id_product = input("Enter Product ID: ").strip()
    product = store.get_product(id_product)
    
    if product:
        try:
            qty = int(input(f"Quantity to reduce for '{product.name}': "))
            if product.reduce_stock(qty):
                print(f"[V] Stock reduced successfully. New stock: {product.stock}")
        except ValueError as e:
            print(f"[!] Error: {e}")
    else:
        print(f"[!] Product '{id_product}' not found!")
    
    pause()


def manage_categories():
    from models.product import Product
    
    while True:
        clear_screen()
        print("\n=== MANAGE CATEGORIES ===")
        Product.show_categories()
        print("1. Add Category")
        print("2. Remove Category")
        print("3. Back")
        
        choice = input("Choose menu: ")
        
        if choice == "1":
            new_cat = input("New category name: ").strip()
            try:
                Product.add_category(new_cat)
            except ValueError as e:
                print(f"\n{e}")
                
        elif choice == "2":
            cat_to_remove = input("Category to remove: ").strip()
            try:
                Product.remove_category(cat_to_remove)
            except ValueError as e:
                print(f"\n{e}")
                
        elif choice == "3":
            break
        else:
            print("[!] Invalid choice!")
        
        pause()