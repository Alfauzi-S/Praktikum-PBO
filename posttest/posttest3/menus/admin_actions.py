from models.customer import Customer
from models.person import Person
from models.product import Product
from menus.cart import build_cart
from menus.payment_prompt import choose_payment
from menus.profile_actions import edit_profile, edit_username, reset_password
from menus.views import (choose_branch, product_table, price_breakdown, REQUEST_HEADERS, REQUEST_ALIGNS,
                         request_rows, SALE_HEADERS, SALE_ALIGNS, sale_rows)
from utils import (ui, pause, ask, ask_valid, run_form, confirm, choose, read_menu_choice, safe,
                   to_float, to_int)


def select_branch(app, user, crumb=""):
    """Admin: otomatis cabangnya. SuperAdmin: memilih (polimorfisme accessible_branches)."""
    branches = user.accessible_branches(app.store)
    if not branches:
        ui.err("You are not assigned to any branch.")
        return None
    if len(branches) == 1:
        return branches[0]
    ui.screen("Choose branch", crumb)
    return choose_branch(branches, "Which branch do you want to work on?")


# ------------------------------------------------------------------ pembayaran bersama
def pay_and_finish(customer, total, create_order):
    """Pilih metode -> validasi pembayaran -> buat pesanan. Boleh coba metode lain jika gagal."""
    while True:
        payment = choose_payment(customer, total)
        if payment is None:
            return None
        sale = safe(lambda: create_order(payment))
        if sale:
            print()
            ui.ok(ui.c(f"Order {sale.id_sale} created and saved to history.", "bold"))
            sale.show_receipt()
            return sale
        ui.warn("The order was not created. Stock has been restored.")
        if not confirm("Try another payment method?", default=True):
            return None


# ------------------------------------------------------------------ notifications
def notifications(app, user):
    while True:
        ui.screen("Notifications", "Dashboard > Notifications")
        inbox = app.inbox(user)
        if not inbox:
            ui.hint("No notifications.")
            pause()
            return
        rows = [[ui.c(ui.SYM["dot"] + " new", "bold", "yellow") if not n.is_read else ui.c("  read", "gray"),
                 ui.time_ago(n.created_at), n.branch.name if n.branch else "-", n.message] for n in inbox]
        ui.table(["", "When", "Branch", "Message"], rows, ["l", "l", "l", "l"])
        for n in inbox:
            n.mark_read()
        pending = [n for n in inbox if n.request and n.request.status == "PENDING"]
        ui.hint("All marked as read.")
        chosen = choose(pending, title="Open a pending request from these notifications?",
                        headers=["Message"], row=lambda n: [n.message], prompt="Open number")
        if chosen is None:
            return
        process_request(app, user, chosen.request)


# ------------------------------------------------------------------ requests
def incoming_requests(app, user):
    while True:
        ui.screen("Customer requests", "Dashboard > Requests")
        pending = app.pending_requests(user.accessible_branches(app.store))
        if not pending:
            ui.ok("All caught up - there are no pending requests.")
            pause()
            return
        request = choose(pending, title=f"{len(pending)} pending request(s)", headers=REQUEST_HEADERS,
                         row=request_rows, aligns=REQUEST_ALIGNS, prompt="Process request number")
        if request is None:
            return
        process_request(app, user, request)


def _stock_check(request):
    rows, can_fulfil = [], True
    for item in request.items:
        enough = item.product.stock >= item.quantity
        can_fulfil = can_fulfil and enough
        rows.append([item.product_name, str(item.quantity), str(item.product.stock),
                     ui.c(f"{ui.SYM['ok']} OK", "green") if enough else ui.c(f"{ui.SYM['err']} Not enough", "bold", "red")])
    ui.table(["Item", "Requested", "In stock", "Stock check"], rows, ["l", "r", "r", "l"], title="Stock check")
    return can_fulfil


def process_request(app, user, request):
    while True:
        ui.screen(f"Process {request.id_request}", "Dashboard > Requests > Process")
        request.show()
        if request.status != "PENDING":
            ui.warn("This request has already been handled.")
            pause()
            return
        customer = request.customer
        ui.hint(f"{customer.name}: {customer.loyalty_points} points, spent {ui.rupiah(customer.total_spending)}, "
                f"discount {customer.discount_percentage}%")
        can_fulfil = _stock_check(request)
        est = price_breakdown(request.estimated_total, customer.discount_percentage, "ORDER TOTAL")
        if not can_fulfil:
            ui.warn("Stock is not enough for this request. Reject it or restock the product first.")
        ui.menu([("Create order & validate payment", "" if can_fulfil else ui.c("blocked", "red")),
                 ("Reject request", "")], "ACTION", back="Back to list")
        choice = read_menu_choice(2)
        if choice is None:
            pause()
        elif choice == 0:
            return
        elif choice == 1:
            if not can_fulfil:
                ui.err("Cannot create the order: stock is not enough.")
                pause()
                continue
            sale = pay_and_finish(customer, est["total"],
                                  lambda payment: app.service.fulfill_request(request, user, payment))
            if sale:
                pause()
                return
        elif choice == 2:
            reason = ask_valid("Reason for rejecting (shown to customer)")
            if reason and confirm(f"Reject {request.id_request}?"):
                safe(lambda: app.service.reject_request(request, user, reason))
                ui.ok("Request rejected. The customer has been notified.")
                pause()
                return


# ------------------------------------------------------------------ walk-in order
def create_order(app, user):
    crumb = "Dashboard > Create order"
    branch = select_branch(app, user, crumb)
    if not branch:
        pause()
        return
    ui.screen("Create order (walk-in)", crumb)
    customer = choose(app.customers, title="Which customer is buying?",
                      headers=["ID", "Name", "Tier", "Phone"],
                      row=lambda c: [c.id_customer, c.name, ui.tier_badge(c.membership_tier), c.phone],
                      prompt="Customer number")
    if not customer:
        return
    items = build_cart(customer, branch, crumb)
    if items is None:
        return
    ui.screen("Confirm order", crumb)
    ui.table(["Item", "Qty", "Unit price", "Subtotal"],
             [[p.name, str(q), ui.rupiah(p.price), ui.rupiah(p.price * q)] for p, q in items],
             ["l", "r", "r", "r"], color="green")
    est = price_breakdown(sum(p.price * q for p, q in items), customer.discount_percentage, "ORDER TOTAL")
    pay_and_finish(customer, est["total"],
                   lambda payment: app.service.create_walkin_order(user, customer, branch, items, payment))
    pause()


# ------------------------------------------------------------------ products
def _pick_product(products, title):
    return choose(products, title=title, headers=["ID", "Product", "Price", "Stock"],
                  row=lambda p: [p.id_product, p.name, ui.rupiah(p.price), ui.stock_badge(p.stock)],
                  aligns=["l", "l", "r", "r"], prompt="Product number")


def _add_product(app, user, branch):
    Product.show_categories()
    data = run_form("Add product", [
        dict(key="name", label="Product name"),
        dict(key="category", label="Category", checker=Product.check_category),
        dict(key="price", label="Price (Rp)", checker=lambda v: Product.check_price(to_float(v))),
        dict(key="stock", label="Initial stock", checker=lambda v: to_int(v, 0), default=0),
    ], f"Dashboard > Products > {branch.name}")
    if data is None:
        return
    product = safe(lambda: Product(branch.next_product_id(), data["name"], data["price"],
                                   data["stock"], data["category"]))
    if product is None:
        return
    try:
        branch.add_product(product)
    except ValueError as error:
        ui.err(str(error))
        return
    app.log.add("PRODUCT", user.name, f"Added product {product.name}", branch)
    ui.ok(f"Product {product.id_product} '{product.name}' added.")


def _edit_product(app, user, branch, product):
    data = run_form(f"Edit {product.name}", [
        dict(key="name", label="Name", default=product.name),
        dict(key="category", label="Category", checker=Product.check_category, default=product.category),
        dict(key="price", label="Price (Rp)", checker=lambda v: Product.check_price(to_float(v)),
             default=f"{product.price:.0f}"),
    ], f"Dashboard > Products > {branch.name}")
    if data is None:
        return
    try:
        product.name, product.category, product.price = data["name"], data["category"], data["price"]
    except ValueError as error:
        ui.err(str(error))
        return
    app.log.add("PRODUCT", user.name, f"Edited product {product.name}", branch)
    ui.ok("Product updated.")


def manage_products(app, user):
    branch = select_branch(app, user, "Dashboard > Products")
    if not branch:
        pause()
        return
    keyword = ""
    while True:
        ui.screen(f"Products - {branch.name}", "Dashboard > Products")
        products = branch.products
        ui.stat_cards([
            ("Products", str(len(products)), "cyan"),
            ("Low stock", str(len(branch.low_stock_products())), "yellow"),
            ("Out of stock", str(sum(1 for p in products if p.stock == 0)), "red"),
            ("Inventory value", ui.rupiah(sum(p.price * p.stock for p in products)), "green"),
        ])
        shown = [p for p in products if keyword.lower() in (p.name + p.category + p.id_product).lower()]
        product_table(shown, title="Inventory" + (f"  (search: '{keyword}')" if keyword else ""))
        ui.menu([("Add product", ""), ("Edit product", ""), ("Restock", ""), ("Delete product", ""),
                 ("Search / clear search", "")], "PRODUCT ACTIONS", back="Back")
        choice = read_menu_choice(5)
        if choice is None:
            pause()
            continue
        if choice == 0:
            return
        if choice == 1:
            _add_product(app, user, branch)
        elif choice in (2, 3, 4):
            product = _pick_product(shown, {2: "Edit which product?", 3: "Restock which product?",
                                            4: "Delete which product?"}[choice])
            if product is None:
                continue
            if choice == 2:
                _edit_product(app, user, branch, product)
            elif choice == 3:
                qty = ask_valid(f"Quantity to add to {product.name}", lambda v: to_int(v, 1))
                if qty:
                    product.add_stock(qty)
                    app.log.add("PRODUCT", user.name, f"Restocked {product.name} +{qty}", branch)
                    ui.ok(f"{product.name} stock is now {product.stock}.")
            elif confirm(f"Delete {product.name}? This cannot be undone."):
                try:
                    branch.remove_product(product.id_product)
                except ValueError as error:
                    ui.err(str(error))
                else:
                    app.log.add("PRODUCT", user.name, f"Deleted product {product.name}", branch)
                    ui.ok("Product deleted.")
        elif choice == 5:
            keyword = ask("Search text (empty = show all)")
            continue
        pause()


# ------------------------------------------------------------------ customers
def _customer_rows(c):
    return [c.id_customer, c.name, c.username, ui.tier_badge(c.membership_tier),
            ui.rupiah(c.total_spending), ui.status_badge("Active" if c.is_active else "Inactive")]


def _add_customer(app, user):
    def check_username(value):
        value = Person.check_username(value)
        if not app.username_available(value):
            raise ValueError(f"Username '{value}' is already taken!")
        return value

    data = run_form("Add customer", [
        dict(key="name", label="Full name", checker=Person.check_name),
        dict(key="username", label="Username", checker=check_username),
        dict(key="password", label="Password (min 6)", checker=Person.check_password, secret=True),
        dict(key="phone", label="Phone (10-13 digits)", checker=Person.check_phone),
        dict(key="gmail", label="Email", checker=Person.check_gmail),
        dict(key="address", label="Address", checker=Customer.check_address),
        dict(key="birth_date", label="Birth date (optional)", required=False),
        dict(key="gender", label="Gender (optional)", required=False),
    ], "Dashboard > Customers")
    if data is None:
        return
    customer = safe(lambda: app.register_customer(actor=user.name, **data))
    if customer:
        ui.ok(f"Customer {customer.id_customer} '{customer.name}' created.")


def manage_customers(app, user):
    crumb = "Dashboard > Customers"
    while True:
        ui.screen("Customers", crumb)
        customers = app.customers
        ui.stat_cards([
            ("Customers", str(len(customers)), "cyan"),
            ("Active", str(sum(1 for c in customers if c.is_active)), "green"),
            ("Total spent", ui.rupiah(sum(c.total_spending for c in customers)), "green"),
        ])
        ui.table(["ID", "Name", "Username", "Tier", "Total spent", "Status"],
                 [_customer_rows(c) for c in customers], ["l", "l", "l", "l", "r", "l"], title="All customers")
        ui.menu([("Add customer", ""), ("View details & orders", ""), ("Edit profile", ""),
                 ("Change username", ""), ("Reset password", ""), ("Activate / Deactivate", "")],
                "CUSTOMER ACTIONS", back="Back")
        choice = read_menu_choice(6)
        if choice is None:
            pause()
            continue
        if choice == 0:
            return
        if choice == 1:
            _add_customer(app, user)
            pause()
            continue
        customer = choose(customers, title="Which customer?", headers=["ID", "Name", "Username"],
                          row=lambda c: [c.id_customer, c.name, c.username], prompt="Customer number")
        if customer is None:
            continue
        if choice == 2:
            ui.screen(f"Customer {customer.id_customer}", crumb)
            customer.show_person_info()
            branches = user.accessible_branches(app.store)
            sales = [s for s in app.sales_for(branches) if s.customer is customer]
            ui.table(SALE_HEADERS, [sale_rows(s) for s in reversed(sales)], SALE_ALIGNS,
                     title="Order history", empty="No orders yet.")
        elif choice == 3:
            edit_profile(customer, crumb)
        elif choice == 4:
            edit_username(app, customer, crumb)
        elif choice == 5:
            reset_password(customer, crumb)
        elif choice == 6:
            customer.is_active = not customer.is_active
            ui.ok(f"{customer.name} is now {'ACTIVE' if customer.is_active else 'INACTIVE'}.")
        if choice != 2:
            app.log.add("ACCOUNT", user.name, f"Updated customer {customer.name}")
        pause()


# ------------------------------------------------------------------ history
def history(app, user):
    crumb = "Dashboard > History"
    while True:
        branches = user.accessible_branches(app.store)
        ui.screen("History / log", crumb)
        sales = app.sales_for(branches)
        requests = [r for r in app.requests if r.branch in branches]
        ui.stat_cards([
            ("Orders", str(len(sales)), "green"),
            ("Revenue", ui.rupiah(sum(s.total for s in sales)), "green"),
            ("Requests", str(len(requests)), "cyan"),
            ("Rejected", str(sum(1 for r in requests if r.status == "REJECTED")), "red"),
        ])
        ui.menu([("Completed orders (open receipts)", ""), ("All requests (every status)", ""),
                 ("Activity log", "")], "HISTORY", back="Back")
        choice = read_menu_choice(3)
        if choice is None:
            pause()
        elif choice == 0:
            return
        elif choice == 1:
            ui.screen("Completed orders", crumb)
            sale = choose(list(reversed(sales)), title=f"{len(sales)} order(s)", headers=SALE_HEADERS,
                          row=sale_rows, aligns=SALE_ALIGNS, prompt="Open receipt number")
            if sale:
                ui.screen(f"Order {sale.id_sale}", crumb)
                sale.show_receipt()
                pause()
        elif choice == 2:
            ui.screen("All requests", crumb)
            ui.table(REQUEST_HEADERS, [request_rows(r) for r in reversed(requests)], REQUEST_ALIGNS,
                     empty="No requests yet.")
            pause()
        elif choice == 3:
            ui.screen("Activity log", crumb)
            entries = app.log.entries(branches=branches)
            multi = len(branches) > 1
            ui.feed([(f"{e.created_at:%d %b %H:%M}", ui.status_badge(e.kind),
                      ui.rupiah(e.amount) if e.amount else "", e.message,
                      f"by {e.actor}" + (f" @ {e.branch.name}" if e.branch and multi else ""))
                     for e in entries], empty="Log is empty.")
            pause()


def _unread(app, user):
    n = app.unread_count(user)
    return ui.c(f"{n} new", "bold", "yellow") if n else ""


def _pending(app, user):
    n = len(app.pending_requests(user.accessible_branches(app.store)))
    return ui.c(f"{n} pending", "bold", "yellow") if n else ""


def _low_stock(app, user):
    n = sum(len(b.low_stock_products()) for b in user.accessible_branches(app.store))
    return ui.c(f"{n} low", "bold", "red") if n else ""


ACTIONS = [
    ("notifications", "Notifications", notifications, _unread),
    ("incoming_requests", "Customer Requests", incoming_requests, _pending),
    ("create_order", "Create Order (walk-in)", create_order, None),
    ("manage_products", "Manage Products", manage_products, _low_stock),
    ("manage_customers", "Manage Customers", manage_customers, None),
    ("history", "History / Log", history, None),
]
