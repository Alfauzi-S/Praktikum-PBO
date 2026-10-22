from menus.cart import build_cart
from menus.views import (choose_branch, product_table, price_breakdown, MY_REQUEST_HEADERS,
                         MY_REQUEST_ALIGNS, my_request_rows)
from utils import ui, pause, ask, confirm, choose, safe


def _timeline(request):
    """Garis waktu status request: Requested -> Reviewed -> Completed/Rejected."""
    done, now, todo = ("green", "bold"), ("yellow", "bold"), ("gray",)
    final = {"COMPLETED": "Completed", "REJECTED": "Rejected"}.get(request.status, "Completed")
    steps = [("Requested", done), ("Reviewed by admin", done if request.status != "PENDING" else now)]
    if request.status == "PENDING":
        steps.append((final, todo))
    else:
        steps.append((final, ("red", "bold") if request.status == "REJECTED" else done))
    parts = [ui.c(f"{ui.SYM['dot']} {label}", *style) for label, style in steps]
    ui.panel("PROGRESS", [("  " + ui.SINGLE["h"] * 3 + "  ").join(parts)], "cyan")


# ------------------------------------------------------------------ view products
def view_products(app, user):
    ui.screen("Browse products", "Dashboard > Products")
    branch = choose_branch(app.store.branches, "Which branch do you want to browse?")
    if not branch:
        return
    keyword, order = "", "1"
    while True:
        ui.screen(f"Products - {branch.name}", "Dashboard > Products")
        products = [p for p in branch.products
                    if keyword.lower() in (p.name + p.category + p.id_product).lower()]
        if order == "2":
            products = sorted(products)                    # memakai Product.__lt__
        elif order == "3":
            products = sorted(products, reverse=True)
        label = {"1": "default order", "2": "cheapest first", "3": "most expensive first"}[order]
        product_table(products, title=f"{len(products)} product(s)  -  {label}"
                      + (f"  -  search: '{keyword}'" if keyword else ""))
        print()
        ui.hint("1 = default   2 = cheapest first   3 = most expensive first   /text = search   "
                "S = shop here   0 = back")
        command = ask("Choose").strip()
        if command == "0" or command == "":
            return
        if command in {"1", "2", "3"}:
            order = command
        elif command.startswith("/"):
            keyword = command[1:].strip()
        elif command.lower() == "s":
            shop(app, user, branch)
            return


# ------------------------------------------------------------------ shop
def shop(app, user, branch=None):
    """Customer memilih barang -> request + notifikasi ke admin cabang."""
    if branch is None:
        ui.screen("Shop", "Dashboard > Shop")
        branch = choose_branch(app.store.branches, "Which branch do you want to shop at?")
        if not branch:
            return
    cart = build_cart(user, branch, "Dashboard > Shop")
    if cart is None:
        return

    ui.screen("Review your request", "Dashboard > Shop > Review")
    ui.table(["Item", "Qty", "Unit price", "Subtotal"],
             [[p.name, str(q), ui.rupiah(p.price), ui.rupiah(p.price * q)] for p, q in cart],
             ["l", "r", "r", "r"], color="green")
    price_breakdown(sum(p.price * q for p, q in cart), user.discount_percentage, "ESTIMATED PRICE")
    ui.hint("Final price is confirmed by the admin when the order is created.")
    note = ask("Note for admin (optional, ENTER to skip)")
    if not confirm("Send this request to the admin?", default=True):
        ui.warn("Request not sent.")
        pause()
        return

    request = safe(lambda: app.service.submit_request(user, branch, cart, note))
    if request:
        print()
        ui.panel("REQUEST SENT", [
            ui.c(f"{ui.SYM['ok']} {request.id_request} has been sent to {branch.name}.", "bold", "green"),
            "",
            "What happens next:",
            "  1. The admin of this branch receives a notification",
            "  2. The admin creates your order and validates the payment",
            "  3. You get a notification here (and by email/SMS) when it is done",
            "",
            ui.c("Track it any time in: My Orders / Status", "dim"),
        ], "green")
    pause()


# ------------------------------------------------------------------ my orders
def show_request_detail(request):
    ui.screen(f"Request {request.id_request}", "Dashboard > My Orders")
    _timeline(request)
    request.show()
    if request.sale:
        request.sale.show_receipt()


def my_orders(app, user):
    while True:
        ui.screen("My orders & status", "Dashboard > My Orders")
        mine = app.requests_of(user)
        if not mine:
            ui.hint("You have no requests yet. Use 'Shop' to create one.")
            pause()
            return
        counts = {s: sum(1 for r in mine if r.status == s) for s in ("PENDING", "COMPLETED", "REJECTED")}
        ui.stat_cards([("Pending", str(counts["PENDING"]), "yellow"),
                       ("Completed", str(counts["COMPLETED"]), "green"),
                       ("Rejected", str(counts["REJECTED"]), "red")])
        request = choose(mine, title="Your requests (newest first)",
                         headers=MY_REQUEST_HEADERS, row=my_request_rows, aligns=MY_REQUEST_ALIGNS,
                         prompt="Open request number")
        if request is None:
            return
        show_request_detail(request)
        pause()


# ------------------------------------------------------------------ notifications
def notifications(app, user):
    while True:
        ui.screen("My notifications", "Dashboard > Notifications")
        inbox = app.inbox(user)
        if not inbox:
            ui.hint("No notifications yet.")
            pause()
            return
        rows = [[ui.c(ui.SYM["dot"] + " new", "bold", "yellow") if not n.is_read else ui.c("  read", "gray"),
                 ui.time_ago(n.created_at), n.message] for n in inbox]
        ui.table(["", "When", "Message"], rows, ["l", "l", "l"])
        for n in inbox:
            n.mark_read()
        linked = [n for n in inbox if n.request]
        ui.hint("All marked as read.")
        chosen = choose(linked, title="Open the related request?", headers=["Message"],
                        row=lambda n: [n.message], prompt="Open number")
        if chosen is None:
            return
        show_request_detail(chosen.request)
        pause()


ACTIONS = [
    ("view_products", "Browse Products", view_products, None),
    ("shop", "Shop (create request)", shop, None),
    ("my_orders", "My Orders / Status",
     my_orders, lambda app, user: _pending_note(app, user)),
    ("my_notifications", "Notifications",
     notifications, lambda app, user: _unread_note(app, user)),
]


def _pending_note(app, user):
    n = sum(1 for r in app.requests_of(user) if r.status == "PENDING")
    return ui.c(f"{n} pending", "bold", "yellow") if n else ""


def _unread_note(app, user):
    n = app.unread_count(user)
    return ui.c(f"{n} new", "bold", "yellow") if n else ""
