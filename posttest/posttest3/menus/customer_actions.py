from utils import clear_screen, pause, header, ask, ask_int, confirm, pick, safe


def view_products(app, user):
    clear_screen()
    header("VIEW PRODUCTS")
    branch = pick(app.store.branches, "Choose branch:", str)
    if not branch:
        return
    print(f"\nProducts at {branch.name}")
    print("1. Default order   2. Cheapest first   3. Most expensive first")
    order = input("Sort: ").strip()
    products = branch.products
    if order == "2":
        products = sorted(products)                  # memakai Product.__lt__
    elif order == "3":
        products = sorted(products, reverse=True)
    print()
    for p in products:
        print(f"  {p}  [{p.category}]")
    pause()


def shop(app, user):
    """Customer memilih barang -> request + notifikasi ke admin cabang."""
    clear_screen()
    header("SHOP - CREATE ORDER REQUEST")
    branch = pick(app.store.branches, "Choose branch to shop at:", str)
    if not branch:
        return

    cart = []                                       # list (product, qty)
    while True:
        clear_screen()
        header(f"CART @ {branch.name}")
        for i, (p, q) in enumerate(cart, 1):
            print(f"  {i}. {p.name} x{q} = Rp{p.price * q:,.0f}")
        if not cart:
            print("  (cart is empty)")
        print(f"\nSubtotal: Rp{sum(p.price * q for p, q in cart):,.0f}  "
              f"(your {user.membership_tier} discount {user.discount_percentage}% applied by admin)")
        print("-" * 56)
        print("1. Add product   2. Remove product   3. Send request   0. Cancel")
        choice = input("Choose: ").strip()

        if choice == "1":
            product = pick(branch.products, "Products:", str)
            if product:
                qty = ask_int(f"Quantity for {product.name}", 1)
                if qty:
                    already = sum(q for p, q in cart if p is product)
                    if already + qty > product.stock:
                        print(f"[!] Not enough stock! Available: {product.stock}")
                    else:
                        cart.append((product, qty))
        elif choice == "2":
            item = pick(cart, "Remove which item?", lambda x: f"{x[0].name} x{x[1]}")
            if item:
                cart.remove(item)
        elif choice == "3":
            if not cart:
                print("[!] Cart is empty!")
            else:
                note = ask("Note for admin (optional)")
                request = safe(lambda: app.service.submit_request(user, branch, cart, note))
                if request:
                    print(f"\n[V] Request {request.id_request} sent. Admin of {branch.name} has been notified.")
                    pause()
                    return
        elif choice == "0":
            return
        else:
            print("[!] Invalid choice!")
        if choice in {"1", "2", "3"}:
            pause()


def my_orders(app, user):
    clear_screen()
    header("MY ORDERS")
    mine = [r for r in app.requests if r.customer is user]
    if not mine:
        print("  You have no requests yet.")
        pause()
        return
    request = pick(list(reversed(mine)), "Your requests:", str)
    if not request:
        return
    print()
    request.show()
    if request.sale:
        request.sale.show_receipt()
    pause()


def notifications(app, user):
    clear_screen()
    header("MY NOTIFICATIONS")
    inbox = app.inbox(user)
    if not inbox:
        print("  No notifications.")
    for n in inbox:
        print(n)
        n.mark_read()
    pause()


ACTIONS = [
    ("view_products", "View Products", view_products),
    ("shop", "Shop (create request)", shop),
    ("my_orders", "My Orders / Status", my_orders),
    ("my_notifications", lambda app, user: f"Notifications ({app.unread_count(user)} new)", notifications),
]
