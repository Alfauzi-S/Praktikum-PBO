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
from utils import ui, pause, read_menu_choice


def testing_menu(app):
    tests = [
        ("Encapsulation", test_encapsulation),
        ("Relations (Asosiasi, Agregasi, Komposisi)", test_relations),
        ("Abstraction (Abstract Base Class)", test_abstraction),
        ("Polymorphism (Inheritance, Duck Typing, Operator)", test_polymorphism),
        ("SOLID (OCP & DIP)", test_solid),
    ]
    while True:
        ui.screen("OOP testing", "Main menu > OOP Testing")
        ui.hint("Tests use temporary objects, so your data is never changed.")
        ui.menu([(label, "") for label, _ in tests] + [("Run all tests", ui.c("1-5", "dim"))],
                "CHOOSE A TEST", back="Back to main menu")
        choice = read_menu_choice(len(tests) + 1)
        if choice is None:
            pause()
        elif choice == 0:
            return
        elif choice <= len(tests):
            label, test = tests[choice - 1]
            ui.screen(f"Test: {label}", "Main menu > OOP Testing")
            test(app)
            pause()
        else:
            ui.clear()
            for label, test in tests:
                ui.screen(f"Test: {label}", "Main menu > OOP Testing > Run all", clear_first=False)
                test(app)
                print()
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
            ui.ok(f"stock = {value} accepted -> {product.stock}")
        except ValueError as error:
            ui.ok(f"stock = {value} rejected: {error}")
    print(f"Password is private: hasattr(customer, '__password') -> {hasattr(customer, '__password')}")
    print(f"verify_password('secret1') -> {customer.verify_password('secret1')}")


def test_relations(app):
    store, branch, product, admin, customer = _demo_world()

    ui.section("[Komposisi] Store membuat Branch DI DALAM add_branch() (tidak dari luar):")
    new_branch = store.add_branch("Cabang Baru", "Jl. Baru", "0541999999")
    print(f"    {new_branch.name} dibuat oleh Store -> total cabang: {len(store)}")

    ui.section("[Komposisi] Sale membuat SaleItem DI DALAM add_item():")
    sale = Sale("TRX-DEMO", customer, branch, admin)
    sale.add_item(product, 2)
    print(f"    Sale punya {len(sale)} item (SaleItem tidak dibuat dari luar Sale)")

    ui.section("[Agregasi] Product & Admin dibuat DI LUAR Branch, lalu didaftarkan:")
    lone_branch = Branch("B99", "Cabang Lepas", "Jl. Lepas", "0541000099")
    spare_product = Product("P901", "Spare Keyboard", 300000, 5, "Peripheral")
    spare_admin = Admin("EMP901", "Spare Admin", "spareadmin", "secret1", "081200000005", "s@demo.com")
    lone_branch.add_product(spare_product)
    lone_branch.add_admin(spare_admin)
    print(f"    Branch punya {len(lone_branch)} produk dan {len(lone_branch.admins)} admin")
    del lone_branch
    print(f"    Branch dihapus, tetapi '{spare_product.name}' dan '{spare_admin.name}' masih ada")
    print("    (siklus hidup mandiri: bisa dipindah ke cabang lain)")

    ui.section("[Asosiasi] Sale hanya mengacu ke Customer / Admin:")
    print(f"    sale.customer = {sale.customer.name}, sale.handled_by = {sale.handled_by.name}")
    print(f"    customer tetap ada tanpa sale: {customer.name}")


def test_abstraction(app):
    for abstract in (Person, PaymentMethod):
        ui.section(f"[1] {abstract.__name__} abstract methods: {sorted(abstract.__abstractmethods__)}")
        ui.section(f"[2] Mencoba membuat objek {abstract.__name__}() ...")
        try:
            abstract("x")
        except TypeError as error:
            ui.ok(f"TypeError: {error}")

    class IncompletePayment(PaymentMethod):
        def validate(self):
            return True

    ui.section("[3] Subclass yang lupa mengimplementasikan abstract method:")
    try:
        IncompletePayment("x")
    except TypeError as error:
        ui.ok(f"TypeError: {error}")

    ui.section("[4] Subclass lengkap berhasil dibuat:")
    for obj in (CashPayment("Test", 1000), BankTransferPayment("Test", "BRI", "12345678"),
                Customer("C0", "Test", "tester", "secret1", "081200000009", "t@t.com", "Jl. T"),
                Admin("E0", "Test", "tester2", "secret1", "081200000008", "t@t.com"),
                SuperAdmin("E1", "Test", "tester3", "secret1", "081200000007", "t@t.com")):
        ui.ok(f"{type(obj).__name__} -> {obj}")

    ui.section("[5] Method konkret process() dipakai bersama semua subclass:")
    for payment in (CashPayment("Demo", 100_000), BankTransferPayment("Demo", "BNI", "98765432"),
                    EWalletPayment("Demo", "OVO", "081200001111", 100_000)):
        payment.process(50_000)


def test_polymorphism(app):
    store, branch, product, admin, customer = _demo_world()
    boss = SuperAdmin("EMP901", "Demo Boss", "demoboss", "secret1", "081200000003", "b@demo.com")

    ui.section("[1] Polimorfisme via pewarisan: satu loop, perilaku tiap role berbeda")
    note = Notification("N0", "Demo", branch=branch)
    for user in (customer, admin, boss):
        print(f"    {user.get_role():<12} | permissions={len(user.get_permissions()):>2} | "
              f"can_see(notif cabang)={user.can_see(note)}")
    store.add_branch("Second Branch", "Jl. Demo 3", "0541000002")   # agar perbedaan terlihat
    print("    Admin.accessible_branches   ->", [b.name for b in admin.accessible_branches(store)])
    print("    SuperAdmin.accessible_branches ->", [b.name for b in boss.accessible_branches(store)])

    ui.section("Metode pembayaran: calculate_fee() di-override tiap subclass")
    payments = [CashPayment("Demo", 2_000_000), BankTransferPayment("Demo", "BCA", "1234567890"),
                EWalletPayment("Demo", "GoPay", "081234567890", 5_000_000)]
    for payment in payments:
        payment._amount = 1_000_000
        print(f"    {payment.method_name:<13} fee {ui.rupiah(payment.calculate_fee()):>12} | {payment.describe()}")

    ui.section("[2] Duck Typing: kelas tanpa pewarisan, method send() sama")
    notify_customer([EmailNotifier("demo@mail.com"), SMSNotifier("081234567890"),
                     WhatsAppNotifier("081234567890")], "Pesanan Anda sedang dikemas.")

    ui.section("[3] Operator Overloading")
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
            self._note(f"Voucher used {ui.rupiah(self._amount)}")

    ui.section("[OCP] VoucherPayment dibuat tanpa mengubah Sale / PaymentMethod / OrderService.")
    sale = Sale("TRX-SOLID", customer, branch, admin)
    sale.add_item(product, 1)
    ok = sale.checkout(VoucherPayment(customer.name, 500_000))
    ui.section("[DIP] Sale.checkout() hanya bergantung pada abstraksi PaymentMethod")
    (ui.ok if ok else ui.err)(f"checkout berhasil: {ok}")
