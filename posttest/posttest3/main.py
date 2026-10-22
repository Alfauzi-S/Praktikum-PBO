import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from seed import build_app
from menus.auth import login, register_customer
from menus.dashboard import run_dashboard
from menus.testing_menu import testing_menu
from utils import clear_screen, pause, header


def main():
    app = build_app()
    while True:
        clear_screen()
        header("COMPUTER SALES MANAGEMENT SYSTEM")
        print(f"Store : {app.store.name}")
        print(f"        {app.store.tagline}")
        print(f"Branch: {', '.join(b.name for b in app.store.branches)}")
        print("=" * 56)
        print("1. Login")
        print("2. Register as Customer")
        print("3. OOP Testing")
        print("4. Exit")
        print("=" * 56)
        choice = input("Choose menu: ").strip()

        if choice == "1":
            user = login(app)
            if user:
                run_dashboard(app, user)
        elif choice == "2":
            register_customer(app)
        elif choice == "3":
            testing_menu(app)
        elif choice == "4":
            print("Thank you for using Computer Sales Management System!")
            break
        else:
            print("[!] Invalid choice!")
            pause()


if __name__ == "__main__":
    main()
