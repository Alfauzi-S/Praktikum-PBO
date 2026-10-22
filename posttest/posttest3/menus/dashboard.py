from menus import customer_actions, admin_actions, superadmin_actions
from menus.profile_actions import profile_menu
from utils import clear_screen, pause, header

# Registry semua aksi: (kunci permission, label, handler). Urutan = urutan menu.
ALL_ACTIONS = (
    customer_actions.ACTIONS
    + admin_actions.ACTIONS
    + superadmin_actions.ACTIONS
    + [("profile", "My Profile & Account", profile_menu)]
)


def build_menu(app, user):
    """Menu dibangun dari permission milik objek user (polimorfisme), bukan if/elif role."""
    permissions = user.get_permissions()
    menu = []
    for key, label, handler in ALL_ACTIONS:
        if key in permissions:
            menu.append((label(app, user) if callable(label) else label, handler))
    return menu


def run_dashboard(app, user):
    while True:
        clear_screen()
        header(f"{user.get_role().upper()} DASHBOARD")
        print(f"Logged in as: {user.name} ({user.username})")
        if getattr(user, "branch", None):
            print(f"Branch      : {user.branch.name}")
        print("-" * 56)
        menu = build_menu(app, user)
        for i, (text, _) in enumerate(menu, 1):
            print(f"{i}. {text}")
        print("0. Logout")
        choice = input("Choose menu: ").strip()
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(menu):
            menu[int(choice) - 1][1](app, user)
        else:
            print("[!] Invalid choice!")
            pause()
