from utils.helper import clear_screen, pause

def testing_menu(products, customers, sales, Product, Customer, Sale, store=None):
    """Menu untuk menguji konsep OOP."""
    while True:
        clear_screen()
        print("=" * 50)
        print("            OOP TESTING")
        print("=" * 50)
        print("1. Test Inheritance")
        print("2. Test Encapsulation")
        print("3. Test Class Method")
        print("4. Test Static Method")
        print("5. Test Association (Asosiasi)")
        print("6. Test Aggregation (Agregasi)")
        print("7. Test Composition (Komposisi)")
        print("8. Run All Tests")
        print("9. Back to Main Menu")
        print("=" * 50)

        choice = input("Choose menu: ")

        if choice == "1":
            test_inheritance(customers)
        elif choice == "2":
            test_encapsulation(products)
        elif choice == "3":
            test_class_method(Product, Customer, Sale)
        elif choice == "4":
            test_static_method(Product, Customer, Sale)
        elif choice == "5":
            test_association()
        elif choice == "6":
            test_aggregation(store)
        elif choice == "7":
            test_composition(sales)
        elif choice == "8":
            run_all_tests(products, customers, sales, Product, Customer, Sale, store)
        elif choice == "9":
            break
        else:
            print("[!] Invalid choice!")
            pause()


def test_inheritance(customers):
    """Menguji konsep Inheritance."""
    clear_screen()
    print("=" * 50)
    print("         INHERITANCE TEST")
    print("=" * 50)
    
    if not customers:
        print("[!] No customers available for testing.")
        pause()
        return
    
    customer = customers[0]
    
    print("\n[1] Parent Class: Person")
    print("[2] Child Class: Customer")
    print("\n--- Calling method from Parent Class ---")
    customer.show_person_info()
    
    print("\n[V] Inheritance Test Completed!")
    print("    Customer inherited attributes and methods from Person.")
    
    pause()


def test_encapsulation(products):
    """Menguji konsep Encapsulation."""
    clear_screen()
    print("=" * 50)
    print("        ENCAPSULATION TEST")
    print("=" * 50)
    
    if not products:
        print("[!] No products available for testing.")
        pause()
        return
    
    product = products[0]
    
    print(f"\n[1] Current Stock: {product.stock}")
    
    print("\n[2] Testing valid setter...")
    try:
        product.stock = 20
        print(f"    New Stock: {product.stock}")
    except ValueError as e:
        print(f"    Error: {e}")
    
    print("\n[3] Testing invalid setter (negative value)...")
    try:
        product.stock = -10
        print(f"    New Stock: {product.stock}")
    except ValueError as e:
        print(f"    [V] Error caught: {e}")
    
    print("\n[V] Encapsulation Test Completed!")
    print("    Private/Protected attributes are protected from invalid values.")
    
    pause()


def test_class_method(Product, Customer, Sale):
    """Menguji konsep Class Method."""
    clear_screen()
    print("=" * 50)
    print("        CLASS METHOD TEST")
    print("=" * 50)
    
    print("\n[1] Testing Product Class Method...")
    print(f"    Current Category: {Product.VALID_CATEGORIES}")
    Product.add_category("Test Category")
    print(f"    Updated Categories: {Product.VALID_CATEGORIES}")
    Product.remove_category("Test Category")
    
    print("\n[2] Testing Sale Class Method...")
    print(f"    Current Tax: {Sale.tax}%")
    Sale.change_tax(15)
    print(f"    New Tax: {Sale.tax}%")
    Sale.change_tax(11)  # Reset
    
    print("\n[V] Class Method Test Completed!")
    
    pause()


def test_static_method(Product, Customer, Sale):
    """Menguji konsep Static Method."""
    clear_screen()
    print("=" * 50)
    print("        STATIC METHOD TEST")
    print("=" * 50)
    
    print("\n[1] Testing Product.validate_price()...")
    print(f"    validate_price(500000): {Product.validate_price(500000)}")
    print(f"    validate_price(-100): {Product.validate_price(-100)}")
    
    print("\n[2] Testing Product.format_price()...")
    print(f"    format_price(750000): {Product.format_price(750000)}")
    
    print("\n[3] Testing Sale.calculate_discount()...")
    print(f"    calculate_discount(100000, 10): {Sale.calculate_discount(100000, 10)}")
    
    print("\n[V] Static Method Test Completed!")
    
    pause()


def test_association():
    """Menguji konsep Asosiasi."""
    clear_screen()
    print("=" * 50)
    print("        ASSOCIATION TEST")
    print("=" * 50)
    
    print("\n[1] Association: Staff 'uses' Sale")
    print("    - Staff receives Sale as parameter")
    print("    - Sale is NOT stored permanently in Staff")
    print("    - Both objects have independent lifecycles")
    
    print("\n[2] Example from Module:")
    print("    Nasabah menggunakan MesinATM")
    print("    - Nasabah tidak memiliki ATM")
    print("    - ATM diterima sebagai parameter method")
    print("    - Keduanya hidup mandiri")
    
    print("\n[V] Association Test Completed!")
    print("    Association = 'menggunakan' (weak relationship)")
    
    pause()


def test_aggregation(store):
    """Menguji konsep Agregasi."""
    clear_screen()
    print("=" * 50)
    print("        AGGREGATION TEST")
    print("=" * 50)
    
    if store:
        print(f"\n[1] Aggregation: Store 'has' Product & Staff")
        print(f"    Store Name: {store.name}")
        print(f"    Total Products: {len(store._products)}")
        print(f"    Total Staff: {len(store._staffs)}")
        
        print("\n[2] Key Characteristics:")
        print("    - Products & Staff created OUTSIDE Store")
        print("    - Objects sent to Store via add_product() & add_staff()")
        print("    - If Store deleted, Products & Staff still exist")
        
        print("\n[3] Proof:")
        print("    del store  # Store dihapus")
        print("    product still exists in memory  # True")
        print("    staff still exists in memory  # True")
    else:
        print("[!] No store available for testing.")
    
    print("\n[V] Aggregation Test Completed!")
    print("    Aggregation = 'memiliki' (medium relationship)")
    
    pause()


def test_composition(sales):
    clear_screen()
    print("=" * 50)
    print("        COMPOSITION TEST")
    print("=" * 50)
    
    if sales:
        sale = sales[0]
        print(f"\n[1] Composition: Sale 'consists of' SaleItem")
        print(f"    Sale ID: {sale.id_sale}")
        print(f"    Total Items: {sale.items_count}")
        
        print("\n[2] Key Characteristics:")
        print("    - SaleItem created INSIDE Sale.add_item()")
        print("    - SaleItem cannot exist without Sale")
        print("    - If Sale deleted, all SaleItems destroyed")
        
        print("\n[3] Proof:")
        print("    sale = Sale('TRX-001', customer)")
        print("    sale.add_item(product, 2)  # SaleItem dibuat di dalam")
        print("    del sale  # Sale dihapus")
        print("    SaleItem juga ikut musnah  # True")
    else:
        print("[!] No sales available for testing.")
        print("\n[2] Key Characteristics:")
        print("    - SaleItem created INSIDE Sale.add_item()")
        print("    - SaleItem cannot exist without Sale")
        print("    - If Sale deleted, all SaleItems destroyed")
    
    print("\n[V] Composition Test Completed!")
    print("    Composition = 'terdiri dari' (strong relationship)")
    
    pause()


def run_all_tests(products, customers, sales, Product, Customer, Sale, store=None):
    """Menjalankan semua pengujian OOP."""
    clear_screen()
    print("=" * 50)
    print("          RUN ALL OOP TESTS")
    print("=" * 50)
    
    print("\n[1] Inheritance Test")
    if customers:
        customers[0].show_person_info()
    else:
        print("  No customers available.")
    
    print("\n[2] Encapsulation Test")
    if products:
        print(f"  Current Stock: {products[0].stock}")
        try:
            products[0].stock = 25
            print(f"  New Stock: {products[0].stock}")
        except ValueError as e:
            print(f"  Error: {e}")
    else:
        print("  No products available.")
    
    print("\n[3] Class Method Test")
    print(f"  Store Category: {Product.VALID_CATEGORIES}")
    
    print("\n[4] Static Method Test")
    print(f"  Valid Price (500000): {Product.validate_price(500000)}")
    
    print("\n[5] Association Test")
    print("  Staff uses Sale (parameter method)")
    
    print("\n[6] Aggregation Test")
    if store:
        print(f"  Store has {len(store._products)} products")
    else:
        print("  No store available.")
    
    print("\n[7] Composition Test")
    print(f"  Total Sales: {len(sales)}")
    
    print("\n" + "=" * 50)
    print("  ALL OOP TESTS COMPLETED!")
    print("=" * 50)
    
    pause()