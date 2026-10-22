import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from seed import build_app
from menus.auth import login, register_customer
from menus.dashboard import run_dashboard
from menus.testing_menu import testing_menu
from utils import ui, pause, read_menu_choice


def main():
    app = build_app()
    while True:
        ui.banner("COMPUTER SALES MANAGEMENT SYSTEM", "Toko perangkat & aksesori komputer")
        ui.panel("STORE", ui.kv_lines([
            ("Name", ui.c(app.store.name, "bold")),
            ("Tagline", app.store.tagline),
            ("Branches", ", ".join(b.name for b in app.store.branches)),
        ], 9), "gray")
        ui.menu([("Login", ""), ("Register as customer", ""), ("OOP Testing", ui.c("for assessment", "dim"))],
                "MAIN MENU", back="Exit")
        choice = read_menu_choice(3)
        if choice is None:
            pause()
        elif choice == 1:
            user = login(app)
            if user:
                run_dashboard(app, user)
        elif choice == 2:
            register_customer(app)
        elif choice == 3:
            testing_menu(app)
        elif choice == 0:
            print()
            ui.ok("Thank you for using Computer Sales Management System!")
            break


if __name__ == "__main__":
    main()
