from utils.helper import clear_screen, pause
from models.staff import Staff
from models.store import Store


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
            test_association(Customer, Product, Sale)
        elif choice == "6":
            test_aggregation(store, Product)
        elif choice == "7":
            test_composition(sales, Product, Customer, Sale)
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
    print(f"    Current Categories: {Product.VALID_CATEGORIES}")
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


def test_association(Customer, Product, Sale):
    """Menguji konsep Asosiasi dengan objek sementara (tanpa mempengaruhi data utama)."""
    clear_screen()
    print("=" * 50)
    print("        ASSOCIATION TEST")
    print("=" * 50)
    
    print("\n[1] Membuat objek sementara untuk demonstrasi...")
    # Objek dibuat secara independen
    temp_cust = Customer("C999", "Test User", "testuser", "pass123", "Test Address", "081234567890", "test@test.com")
    temp_prod = Product("P999", "Test Product", 100000, 10, "Peripheral")
    temp_sale = Sale("TRX-TEST", temp_cust)
    temp_sale.add_item(temp_prod, 1)
    
    temp_staff = Staff("Test Staff", "teststaff", "pass123", "EMP999", "Kasir", 5000000, "081111111111", "staff@test.com")
    
    print(f"    - Dibuat Staff: {temp_staff.name}")
    print(f"    - Dibuat Sale: {temp_sale.id_sale}")
    
    print("\n[2] Mengeksekusi Asosiasi: Staff 'menggunakan' Sale")
    print("    Memanggil: temp_staff.process_transaction(temp_sale)")
    
    # Ini adalah bukti asosiasi: objek Sale diterima sebagai parameter dan diproses
    temp_staff.process_transaction(temp_sale)
    
    print("\n[3] Bukti Siklus Hidup Mandiri:")
    print("    - Staff memproses sale, tetapi TIDAK menyimpannya sebagai atribut permanen.")
    print(f"    - hasattr(temp_staff, 'sale') -> {hasattr(temp_staff, 'sale')} (False, tidak ada kepemilikan)")
    print("    - Kedua objek dapat hidup atau dihapus secara independen.")
    
    print("\n[V] Association Test Completed!")
    print("    Asosiasi = 'menggunakan' (hubungan lemah)")
    pause()


def test_aggregation(store, Product):
    """Menguji konsep Agregasi dengan objek sementara (tanpa mempengaruhi data utama)."""
    clear_screen()
    print("=" * 50)
    print("        AGGREGATION TEST")
    print("=" * 50)
    
    if store:
        print(f"\n[1] Kondisi Store Utama:")
        print(f"    Nama Store: {store.name}")
        print(f"    Total Produk: {len(store._products)}")
        print(f"    Total Staff: {len(store._staffs)}")
    
    print("\n[2] Membuat objek sementara DI LUAR store sementara...")
    temp_store = Store("Temp Store Demo", "Demo Location")
    temp_prod = Product("P888", "Temp Mouse", 200000, 50, "Peripheral")
    temp_staff = Staff("Temp Staff", "tempstaff", "pass123", "EMP888", "Kasir", 4000000, "081222222222", "temp@test.com")
    
    print(f"    Dibuat Product: {temp_prod.name}")
    print(f"    Dibuat Staff: {temp_staff.name}")
    
    print("\n[3] Agregasi: Menambahkan mereka ke store sementara...")
    temp_store.add_product(temp_prod)
    temp_store.add_staff(temp_staff)
    print(f"    Temp Store sekarang memiliki {len(temp_store._products)} produk.")
    
    print("\n[4] Bukti Siklus Hidup Mandiri (Agregasi):")
    print("    Menghapus objek store sementara (del temp_store)...")
    del temp_store
    print("    Store sementara dihapus dari memori.")
    
    print("\n[5] Memverifikasi objek sementara masih ada:")
    print(f"    temp_prod.name masih: '{temp_prod.name}'")
    print(f"    temp_staff.name masih: '{temp_staff.name}'")
    print("    -> Mereka TIDAK ikut musnah ketika store dihapus!")
    
    print("\n[V] Aggregation Test Completed!")
    print("    Agregasi = 'memiliki' (hubungan sedang, siklus hidup mandiri)")
    pause()


def test_composition(sales, Product, Customer, Sale):
    """Menguji konsep Komposisi dengan objek sementara (tanpa mempengaruhi data utama)."""
    clear_screen()
    print("=" * 50)
    print("        COMPOSITION TEST")
    print("=" * 50)
    
    if sales:
        print(f"\n[1] Kondisi Penjualan yang Ada:")
        print(f"    Total Sale di sistem: {len(sales)}")
        if len(sales) > 0:
            print(f"    Contoh Sale ID: {sales[0].id_sale} dengan {sales[0].items_count} item")
    
    print("\n[2] Membuat Sale sementara dan menambahkan item (Komposisi)...")
    temp_cust = Customer("C999", "Test User", "testuser", "pass123", "Test Address", "081234567890", "test@test.com")
    temp_prod = Product("P777", "Temp Keyboard", 300000, 20, "Peripheral")
    
    temp_sale = Sale("TRX-COMP-TEST", temp_cust)
    print(f"    Dibuat Sale: {temp_sale.id_sale}")
    print(f"    Memanggil temp_sale.add_item(temp_prod, 2)...")
    
    # Ini membuat SaleItem DI DALAM sale (bukti komposisi)
    temp_sale.add_item(temp_prod, 2)
    
    print(f"    Sale sekarang memiliki {temp_sale.items_count} item secara internal.")
    print("    Objek SaleItem dibuat LANGSUNG di dalam method Sale.add_item().")
    print("    Kita TIDAK memiliki variabel terpisah di luar yang memegang objek SaleItem tersebut.")
    
    print("\n[3] Bukti Siklus Hidup Terikat (Komposisi):")
    print("    SaleItem hanya ada SELAMA temp_sale ada.")
    print("    Jika kita menghapus temp_sale (del temp_sale), objek SaleItem di dalamnya juga ikut musnah.")
    print("    (Di Python, garbage collection menangani penghancuran ini secara otomatis).")
    
    print("\n[V] Composition Test Completed!")
    print("    Komposisi = 'terdiri dari' (hubungan kuat, siklus hidup terikat)")
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
    print("  Staff uses Sale (parameter method) - demonstrated in menu 5")
    
    print("\n[6] Aggregation Test")
    if store:
        print(f"  Store has {len(store._products)} products (independent lifecycle)")
    else:
        print("  No store available.")
    
    print("\n[7] Composition Test")
    print(f"  Total Sales: {len(sales)} (SaleItems created internally)")
    
    print("\n" + "=" * 50)
    print("  ALL OOP TESTS COMPLETED!")
    print("=" * 50)
    
    pause()