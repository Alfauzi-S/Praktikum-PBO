from models.person import Person
from models.customer import Customer
from models.admin import Admin, SuperAdmin
from models.product import Product
from models.store import Store
from models.branch import Branch
from models.sale import Sale
from models.sale_item import SaleItem
from models.notification import Notification
from models.payment import PaymentMethod, CashPayment, BankTransferPayment, EWalletPayment
from models.notifier import EmailNotifier, SMSNotifier, WhatsAppNotifier, notify_customer
from utils import clear_screen, pause, header


def testing_menu(app):
    tests = [
        ("Test Encapsulation", test_encapsulation),
        ("Test Relations (Asosiasi, Agregasi, Komposisi)", test_relations),
        ("Test Abstraction (Abstract Base Class)", test_abstraction),
        ("Test Polymorphism (Inheritance, Duck Typing, Operator)", test_polymorphism),
        ("Test SOLID (OCP & DIP)", test_solid),
    ]
    while True:
        clear_screen()
        header("OOP TESTING")
        for i, (label, _) in enumerate(tests, 1):
            print(f"{i}. {label}")
        print(f"{len(tests) + 1}. Run All Tests")
        print("0. Back to Main Menu")
        choice = input("Choose menu: ").strip()
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(tests):
            clear_screen()
            label, test = tests[int(choice) - 1]
            header(label.upper())
            test(app)
            pause()
        elif choice == str(len(tests) + 1):
            clear_screen()
            for label, test in tests:
                header(label.upper())
                test(app)
                print()
            pause()
        else:
            print("[!] Invalid choice!")
            pause()


# ------------------------------------------------------------------ helpers
def _demo_world():
    """Objek sementara agar data utama tidak berubah."""
    store = Store("Demo Store", "demo", "0541000000", "demo@store.com")
    branch = store.add_branch("Demo Branch", "Jl. Demo 1", "0541000001")
    product = Product("P900", "Demo Mouse", 200000, 10, "Peripheral")
    branch.add_product(product)
    admin = Admin("EMP900", "Demo Admin", "demoadmin", "secret1", "081200000001", "a@demo.com")
    branch.add_admin(admin)
    customer = Customer("C900", "Demo Customer", "democust", "secret1", "081200000002",
                        "c@demo.com", "Jl. Demo 2")
    return store, branch, product, admin, customer


# ------------------------------------------------------------------ tests
def test_encapsulation(app):
    _, _, product, _, customer = _demo_world()
    print(f"Stock now: {product.stock}")
    for value in (20, -10):
        try:
            product.stock = value
            print(f"[V] stock = {value} accepted -> {product.stock}")
        except ValueError as error:
            print(f"[V] stock = {value} rejected: {error}")
    print(f"Password is private: hasattr(customer, '__password') -> {hasattr(customer, '__password')}")
    print(f"verify_password('secret1') -> {customer.verify_password('secret1')}")


def test_relations(app):
    store, branch, product, admin, customer = _demo_world()

    print("[Komposisi] Store membuat Branch DI DALAM add_branch() (tidak dari luar):")
    new_branch = store.add_branch("Cabang Baru", "Jl. Baru", "0541999999")
    print(f"    {new_branch.name} dibuat oleh Store -> total cabang: {len(store)}")

    print("\n[Komposisi] Sale membuat SaleItem DI DALAM add_item():")
    sale = Sale("TRX-DEMO", customer, branch, admin)
    sale.add_item(product, 2)
    print(f"    Sale punya {len(sale)} item (SaleItem tidak dibuat dari luar Sale)")

    print("\n[Agregasi] Product & Admin dibuat DI LUAR Branch, lalu didaftarkan:")
    lone_branch = Branch("B99", "Cabang Lepas", "Jl. Lepas", "0541000099")
    spare_product = Product("P901", "Spare Keyboard", 300000, 5, "Peripheral")
    spare_admin = Admin("EMP901", "Spare Admin", "spareadmin", "secret1", "081200000005", "s@demo.com")
    lone_branch.add_product(spare_product)
    lone_branch.add_admin(spare_admin)
    print(f"    Branch punya {len(lone_branch)} produk dan {len(lone_branch.admins)} admin")
    del lone_branch
    print(f"    Branch dihapus, tetapi '{spare_product.name}' dan '{spare_admin.name}' masih ada")
    print("    (siklus hidup mandiri: bisa dipindah ke cabang lain)")

    print("\n[Asosiasi] Sale hanya mengacu ke Customer / Admin:")
    print(f"    sale.customer = {sale.customer.name}, sale.handled_by = {sale.handled_by.name}")
    print(f"    customer tetap ada tanpa sale: {customer.name}")


def test_abstraction(app):
    for abstract in (Person, PaymentMethod):
        print(f"\n[1] {abstract.__name__} abstract methods: {sorted(abstract.__abstractmethods__)}")
        print(f"[2] Mencoba membuat objek {abstract.__name__}() ...")
        try:
            abstract("x")
        except TypeError as error:
            print(f"    [V] TypeError: {error}")

    class IncompletePayment(PaymentMethod):
        def validate(self):
            return True

    print("\n[3] Subclass yang lupa mengimplementasikan abstract method:")
    try:
        IncompletePayment("x")
    except TypeError as error:
        print(f"    [V] TypeError: {error}")

    print("\n[4] Subclass lengkap berhasil dibuat:")
    for obj in (CashPayment("Test", 1000), BankTransferPayment("Test", "BRI", "12345678"),
                Customer("C0", "Test", "tester", "secret1", "081200000009", "t@t.com", "Jl. T"),
                Admin("E0", "Test", "tester2", "secret1", "081200000008", "t@t.com"),
                SuperAdmin("E1", "Test", "tester3", "secret1", "081200000007", "t@t.com")):
        print(f"    [V] {type(obj).__name__} -> {obj}")

    print("\n[5] Method konkret process() dipakai bersama semua subclass:")
    for payment in (CashPayment("Demo", 100_000), BankTransferPayment("Demo", "BNI", "98765432"),
                    EWalletPayment("Demo", "OVO", "081200001111", 100_000)):
        payment.process(50_000)


def test_polymorphism(app):
    store, branch, product, admin, customer = _demo_world()
    boss = SuperAdmin("EMP901", "Demo Boss", "demoboss", "secret1", "081200000003", "b@demo.com")

    print("[1] Polimorfisme via pewarisan: satu loop, perilaku tiap role berbeda")
    note = Notification("N0", "Demo", branch=branch)
    for user in (customer, admin, boss):
        print(f"    {user.get_role():<12} | permissions={len(user.get_permissions()):>2} | "
              f"can_see(notif cabang)={user.can_see(note)}")
    store.add_branch("Second Branch", "Jl. Demo 3", "0541000002")   # agar perbedaan terlihat
    print("    Admin.accessible_branches   ->", [b.name for b in admin.accessible_branches(store)])
    print("    SuperAdmin.accessible_branches ->", [b.name for b in boss.accessible_branches(store)])

    print("\n    Metode pembayaran: calculate_fee() di-override tiap subclass")
    payments = [CashPayment("Demo", 2_000_000), BankTransferPayment("Demo", "BCA", "1234567890"),
                EWalletPayment("Demo", "GoPay", "081234567890", 5_000_000)]
    for payment in payments:
        payment._amount = 1_000_000
        print(f"    {payment.method_name:<13} fee Rp{payment.calculate_fee():>9,.0f} | {payment.describe()}")

    print("\n[2] Duck Typing: kelas tanpa pewarisan, method send() sama")
    notify_customer([EmailNotifier("demo@mail.com"), SMSNotifier("081234567890"),
                     WhatsAppNotifier("081234567890")], "Pesanan Anda sedang dikemas.")

    print("\n[3] Operator Overloading")
    cheap, pricey = Product("P1", "Cheap", 100000, 1, "Aksesoris"), Product("P2", "Pricey", 900000, 1, "Aksesoris")
    print(f"    Pricey > Cheap -> {pricey > cheap} (__gt__) | min() -> {min(cheap, pricey).name} (__lt__)")
    print(f"    str(payment) -> {payments[1]} (__str__)")
    sale = Sale("T1", customer, branch, admin)
    sale.add_item(product, 3)
    print(f"    len(sale) -> {len(sale)} (__len__) | len(branch) -> {len(branch)} products")


def test_solid(app):
    store, branch, product, admin, customer = _demo_world()

    class VoucherPayment(PaymentMethod):
        method_name = "Voucher"

        def __init__(self, payer_name, value):
            super().__init__(payer_name)
            self.value = value

        def validate(self):
            return self.value >= self._amount

        def calculate_fee(self):
            return 0

        def execute(self):
            print(f"          Voucher used: Rp{self._amount:,.0f}")

    print("[OCP] VoucherPayment dibuat tanpa mengubah Sale / PaymentMethod / OrderService.")
    sale = Sale("TRX-SOLID", customer, branch, admin)
    sale.add_item(product, 1)
    ok = sale.checkout(VoucherPayment(customer.name, 500_000))
    print(f"[DIP] Sale.checkout() hanya bergantung pada abstraksi PaymentMethod -> berhasil: {ok}")
