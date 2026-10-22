from menus import customer_actions, admin_actions, superadmin_actions
from menus.profile_actions import profile_menu
from menus.views import REQUEST_ALIGNS
from utils import ui, pause, read_menu_choice

# Registry semua aksi: (kunci permission, label, handler, fungsi_catatan). Urutan = urutan menu.
ALL_ACTIONS = (
    customer_actions.ACTIONS
    + admin_actions.ACTIONS
    + superadmin_actions.ACTIONS
    + [("profile", "My Profile & Account", profile_menu, None)]
)


def build_menu(app, user):
    """Menu dibangun dari permission milik objek user (polimorfisme), bukan if/elif role."""
    permissions = user.get_permissions()
    return [(label, handler, note_fn) for key, label, handler, note_fn in ALL_ACTIONS if key in permissions]


# ------------------------------------------------------------------ ringkasan dashboard
# Setiap blok ringkasan dipilih lewat kunci permission, sama seperti menu.
def _customer_summary(app, user):
    ui.panel("MY MEMBERSHIP", ui.kv_lines([
        ("Tier", f"{ui.tier_badge(user.membership_tier)}  ({user.discount_percentage}% discount on every order)"),
        ("Progress", (f"{ui.progress_bar(user.tier_progress, 18)}  {ui.rupiah(user.next_tier()[1])} "
                      f"more to {user.next_tier()[0]}") if user.next_tier() else "Highest tier reached"),
        ("Points", f"{user.loyalty_points}"),
        ("Total spent", ui.rupiah(user.total_spending)),
    ], 11), "cyan")
    mine = app.requests_of(user)
    ui.stat_cards([
        ("Pending", str(sum(1 for r in mine if r.status == "PENDING")), "yellow"),
        ("Completed", str(sum(1 for r in mine if r.status == "COMPLETED")), "green"),
        ("New notifications", str(app.unread_count(user)), "cyan"),
    ])
    recent = mine[:3]
    if recent:
        ui.table(["Request", "Branch", "Est. total", "Status", "Created"],
                 [[ui.c(r.id_request, "bold"), r.branch.name, ui.rupiah(r.estimated_total),
                   ui.status_badge(r.status), ui.time_ago(r.created_at)] for r in recent],
                 ["l", "l", "r", "l", "l"], title="Recent activity")


def _admin_summary(app, user):
    branches = user.accessible_branches(app.store)
    pending = app.pending_requests(branches)
    low = [(b, p) for b in branches for p in b.low_stock_products()]
    ui.stat_cards([
        ("Pending", str(len(pending)), "yellow"),
        ("Orders today", str(len(app.sales_for(branches, today_only=True))), "green"),
        ("Revenue today", ui.rupiah(app.revenue_for(branches, today_only=True)), "green"),
        ("Low stock", str(len(low)), "red"),
    ])
    if pending:
        ui.table(["Request", "Customer", "Branch", "Est. total", "Waiting"],
                 [[ui.c(r.id_request, "bold"), r.customer.name, r.branch.name,
                   ui.rupiah(r.estimated_total), ui.c(ui.time_ago(r.created_at), "yellow")] for r in pending[:3]],
                 ["l", "l", "l", "r", "l"], title="Needs your attention", color="yellow")
    if low:
        ui.table(["Branch", "Product", "Stock"],
                 [[b.name, p.name, ui.stock_badge(p.stock)] for b, p in low[:3]],
                 ["l", "l", "r"], title="Low stock", color="red")


def _super_summary(app, user):
    store = app.store
    ui.table(["Branch", "Admins", "Products", "Orders", "Revenue"],
             [[ui.c(b.name, "bold"), str(len(b.admins)), str(len(b)), str(len(app.sales_for([b]))),
               ui.rupiah(app.revenue_for([b]))] for b in store.branches],
             ["l", "r", "r", "r", "r"], title=f"All branches - {store.name}", color="magenta")


# (kunci permission, fungsi). Admin dan SuperAdmin keduanya punya "incoming_requests";
# hanya SuperAdmin punya "manage_admins" sehingga hanya ia yang melihat ringkasan cabang.
SUMMARIES = [
    ("shop", _customer_summary),
    ("incoming_requests", _admin_summary),
    ("manage_admins", _super_summary),
]


def run_dashboard(app, user):
    while True:
        ui.screen(f"{user.get_role()} dashboard", f"{app.store.name}  |  {user.name} ({user.username})"
                  + (f"  |  {user.branch.name}" if getattr(user, "branch", None) else ""))
        permissions = user.get_permissions()
        for key, summary in SUMMARIES:
            if key in permissions:
                summary(app, user)
        menu = build_menu(app, user)
        ui.menu([(label(app, user) if callable(label) else label, note_fn(app, user) if note_fn else "")
                 for label, _, note_fn in menu], "MENU", back="Logout")
        choice = read_menu_choice(len(menu))
        if choice is None:
            pause()
        elif choice == 0:
            return
        else:
            menu[choice - 1][1](app, user)
