from models.order_request import OrderRequest
from menus.payment_prompt import choose_payment
from menus.profile_actions import edit_profile, edit_username, reset_password
from utils import clear_screen, pause, header, ask, ask_int, ask_float, confirm, pick, safe


def select_branch(app, user):
    """Admin: otomatis cabangnya. SuperAdmin: memilih salah satu (polimorfisme accessible_branches)."""
    branches = user.accessible_branches(app.store)
    if not branches:
        print("[!] You are not assigned to any branch.")
        return None
    if len(branches) == 1:
        return branches[0]
    return pick(branches, "Choose branch:", str)


# ---------------------------------------------------------------- notifications
def notifications(app, user):
    clear_screen()
    header("NOTIFICATIONS")
    inbox = app.inbox(user)
    if not inbox:
        print("  No notifications.")
    for n in inbox:
        print(n)
        n.mark_read()
    print("\n(* = was unread)")
    pause()


# ---------------------------------------------------------------- requests
def incoming_requests(app, user):
    while True:
        clear_screen()
        header("CUSTOMER REQUESTS")
        pending = app.pending_requests(user.accessible_branches(app.store))
        request = pick(pending, "Pending requests (choose to process):", str)
        if not request:
            if not pending:
                pause()
            return
        process_request(app, user, request)


def process_request(app, user, request):
    clear_screen()
    header(f"PROCESS {request.id_request}")
    request.show()
    print("\n1. Create order & validate payment")
    print("2. Reject request")
    print("0. Back")
    choice = input("Choose: ").strip()

    if choice == "1":
        customer = request.customer
        preview = request.estimated_total
        discount = preview * customer.discount_percentage / 100
        print(f"\nSubtotal Rp{preview:,.0f} - discount {customer.discount_percentage}% "
              f"(Rp{discount:,.0f}) + tax {_tax()}% on the rest")
        payment = choose_payment(customer)
        if payment is None:
            pause()
            return
        sale = safe(lambda: app.service.fulfill_request(request, user, payment))
        if sale:
            print(f"\n[V] Order {sale.id_sale} created and recorded to history.")
            sale.show_receipt()
        else:
            print("\n[!] Order not created (payment invalid or stock changed). Request stays PENDING.")
        pause()
    elif choice == "2":
        reason = ask("Reason")
        safe(lambda: app.service.reject_request(request, user, reason))
        print("[V] Request rejected. Customer notified.")
        pause()


def _tax():
    from models.sale import Sale
    return Sale.tax


# ---------------------------------------------------------------- walk-in order
def create_order(app, user):
    clear_screen()
    header("CREATE ORDER (WALK-IN)")
    branch = select_branch(app, user)
    if not branch:
        pause()
        return
    customer = pick(app.customers, "Choose customer:", lambda c: f"{c.name} ({c.membership_tier}) - {c.id_customer}")
    if not customer:
        return

    items = []
    while True:
        print(f"\nItems so far: {', '.join(f'{p.name} x{q}' for p, q in items) or '-'}")
        product = pick(branch.products, "Add product (0 to finish):", str)
        if not product:
            break
        qty = ask_int(f"Quantity for {product.name}", 1)
        if qty:
            if sum(q for p, q in items if p is product) + qty > product.stock:
                print(f"[!] Not enough stock! Available: {product.stock}")
            else:
                items.append((product, qty))
    if not items:
        print("[!] No items. Cancelled.")
        pause()
        return

    payment = choose_payment(customer)
    if payment is None:
        pause()
        return
    sale = safe(lambda: app.service.create_walkin_order(user, customer, branch, items, payment))
    if sale:
        sale.show_receipt()
    else:
        print("\n[!] Order failed. Stock restored.")
    pause()


# ---------------------------------------------------------------- products
def manage_products(app, user):
    branch = select_branch(app, user)
    if not branch:
        pause()
        return
    while True:
        clear_screen()
        header(f"MANAGE PRODUCTS - {branch.name}")
        for p in branch.products:
            print(f"  {p}  [{p.category}]")
        print("-" * 56)
        print("1. Add   2. Edit   3. Restock   4. Delete   0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_product(app, user, branch)
        elif choice == "2":
            product = pick(branch.products, "Edit which product?", str)
            if product:
                edit_product(app, user, branch, product)
        elif choice == "3":
            product = pick(branch.products, "Restock which product?", str)
            qty = ask_int("Quantity to add", 1) if product else None
            if qty:
                safe(lambda: product.add_stock(qty))
                app.log.add("PRODUCT", user.name, f"Restocked {product.name} +{qty}", branch)
                print("[V] Stock updated.")
        elif choice == "4":
            product = pick(branch.products, "Delete which product?", str)
            if product and confirm(f"Delete {product.name}?"):
                safe(lambda: branch.remove_product(product.id_product))
                app.log.add("PRODUCT", user.name, f"Deleted product {product.name}", branch)
                print("[V] Product deleted.")
        elif choice == "0":
            return
        else:
            print("[!] Invalid choice!")
        pause()


def add_product(app, user, branch):
    from models.product import Product
    Product.show_categories()
    name = ask("Product name")
    category = ask("Category")
    price = ask_float("Price (Rp)")
    stock = ask_int("Initial stock", 0)
    if price is None or stock is None:
        return
    product = safe(lambda: Product(branch.next_product_id(), name, price, stock, category))
    if product is None:
        return
    try:
        branch.add_product(product)
    except ValueError as error:
        print(f"[!] {error}")
        return
    app.log.add("PRODUCT", user.name, f"Added product {product.name}", branch)
    print(f"[V] Product {product.id_product} added.")


def edit_product(app, user, branch, product):
    print("(Leave blank to keep the current value)")
    name = ask("Name", product.name)
    category = ask("Category", product.category)
    price = ask("Price", f"{product.price:.0f}")
    try:
        product.name = name
        product.category = category
        product.price = float(price)
        app.log.add("PRODUCT", user.name, f"Edited product {product.name}", branch)
        print("[V] Product updated.")
    except ValueError as error:
        print(f"[!] {error}")


# ---------------------------------------------------------------- customers
def manage_customers(app, user):
    while True:
        clear_screen()
        header("MANAGE CUSTOMERS")
        for c in app.customers:
            state = "" if c.is_active else " [INACTIVE]"
            print(f"  {c.id_customer} | {c.name} | {c.username} | {c.membership_tier}{state}")
        print("-" * 56)
        print("1. Add   2. View/Edit profile   3. Change username   4. Reset password")
        print("5. Activate/Deactivate   0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_customer(app, user)
        elif choice in {"2", "3", "4", "5"}:
            customer = pick(app.customers, "Choose customer:", lambda c: f"{c.name} ({c.username})")
            if customer:
                if choice == "2":
                    clear_screen()
                    customer.show_person_info()
                    edit_profile(customer)
                elif choice == "3":
                    edit_username(app, customer)
                elif choice == "4":
                    reset_password(customer)
                else:
                    customer.is_active = not customer.is_active
                    print(f"[V] {customer.name} is now {'Active' if customer.is_active else 'Inactive'}.")
                app.log.add("ACCOUNT", user.name, f"Updated customer {customer.name}")
        elif choice == "0":
            return
        else:
            print("[!] Invalid choice!")
        pause()


def add_customer(app, user):
    data = dict(
        name=ask("Full name"), username=ask("Username"), password=ask("Password (min 6)"),
        phone=ask("Phone"), gmail=ask("Email"), address=ask("Address"),
        birth_date=ask("Birth date (optional)"), gender=ask("Gender (optional)"),
    )
    customer = safe(lambda: app.register_customer(actor=user.name, **data))
    if customer:
        print(f"[V] Customer {customer.id_customer} created.")


# ---------------------------------------------------------------- history
def history(app, user):
    while True:
        clear_screen()
        header("HISTORY / LOG")
        print("1. Completed orders (receipts)")
        print("2. Activity log (requests, orders, rejections, changes)")
        print("0. Back")
        choice = input("Choose: ").strip()
        branches = user.accessible_branches(app.store)
        if choice == "1":
            sales = [s for s in reversed(app.sales) if s.branch in branches]
            sale = pick(sales, "Completed orders:", str)
            if sale:
                sale.show_receipt()
                pause()
        elif choice == "2":
            clear_screen()
            header("ACTIVITY LOG")
            entries = app.log.entries(branches=branches, kinds={"REQUEST", "ORDER", "REJECTED", "PRODUCT"})
            for entry in entries or []:
                print(entry)
            if not entries:
                print("  Empty.")
            pause()
        elif choice == "0":
            return
        else:
            print("[!] Invalid choice!")
            pause()


ACTIONS = [
    ("notifications", lambda app, user: f"Notifications ({app.unread_count(user)} new)", notifications),
    ("incoming_requests",
     lambda app, user: f"Customer Requests ({len(app.pending_requests(user.accessible_branches(app.store)))} pending)",
     incoming_requests),
    ("create_order", "Create Order (walk-in)", create_order),
    ("manage_products", "Manage Products", manage_products),
    ("manage_customers", "Manage Customers", manage_customers),
    ("history", "History / Log", history),
]
