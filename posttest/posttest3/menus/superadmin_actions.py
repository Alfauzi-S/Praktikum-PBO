from menus.profile_actions import edit_profile, edit_username, reset_password
from utils import clear_screen, pause, header, ask, confirm, pick, safe


# ---------------------------------------------------------------- admins
def manage_admins(app, user):
    while True:
        clear_screen()
        header("MANAGE ADMINS")
        for a in app.admins:
            state = "" if a.is_active else " [INACTIVE]"
            branch = a.branch.name if a.branch else "-"
            print(f"  {a.employee_id} | {a.name} | {a.username} | {a.get_role()} | {branch}{state}")
        print("-" * 56)
        print("1. Create admin   2. Edit profile   3. Change username   4. Reset password")
        print("5. Move to another branch   6. Activate/Deactivate   0. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            create_admin(app, user)
        elif choice in {"2", "3", "4", "5", "6"}:
            admin = pick(app.admins, "Choose admin:", lambda a: f"{a.name} ({a.username}) - {a.get_role()}")
            if admin:
                modify_admin(app, user, admin, choice)
        elif choice == "0":
            return
        else:
            print("[!] Invalid choice!")
        pause()


def create_admin(app, user):
    branch = pick(app.store.branches, "Assign to branch:", str)
    if not branch:
        return
    data = dict(
        name=ask("Full name"), username=ask("Username"), password=ask("Password (min 6)"),
        phone=ask("Phone"), gmail=ask("Email"), birth_date=ask("Birth date (optional)"),
        gender=ask("Gender (optional)"),
    )
    admin = safe(lambda: app.register_admin(branch=branch, actor=user.name, **data))
    if admin:
        print(f"[V] Admin {admin.employee_id} created for {branch.name}.")


def modify_admin(app, user, admin, choice):
    if choice == "2":
        clear_screen()
        admin.show_person_info()
        edit_profile(admin)
    elif choice == "3":
        edit_username(app, admin)
    elif choice == "4":
        reset_password(admin)
    elif choice == "5":
        branch = pick(app.store.branches, "Move to branch:", str)
        if branch:
            if admin.branch:
                admin.branch.remove_admin(admin)
            branch.add_admin(admin)
            print(f"[V] {admin.name} now works at {branch.name}.")
    elif choice == "6":
        if admin is user:
            print("[!] You cannot deactivate yourself!")
            return
        admin.is_active = not admin.is_active
        print(f"[V] {admin.name} is now {'Active' if admin.is_active else 'Inactive'}.")
    app.log.add("ACCOUNT", user.name, f"Updated admin {admin.name}", admin.branch)


# ---------------------------------------------------------------- store profile
def store_profile(app, user):
    store = app.store
    clear_screen()
    header("STORE PROFILE")
    print(f"Name     : {store.name}")
    print(f"Tagline  : {store.tagline}")
    print(f"Phone    : {store.phone}")
    print(f"Email    : {store.email}")
    print(f"Branches : {len(store)}")
    if not confirm("\nEdit store profile?"):
        return
    print("(Leave blank to keep the current value)")
    try:
        store.update_profile(
            name=ask("Store name", store.name), tagline=ask("Tagline", store.tagline),
            phone=ask("Phone", store.phone), email=ask("Email", store.email))
        app.log.add("STORE", user.name, "Updated store profile")
        print("[V] Store profile updated.")
    except ValueError as error:
        print(f"[!] {error}")
    pause()


# ---------------------------------------------------------------- branches
def manage_branches(app, user):
    while True:
        clear_screen()
        header("MANAGE BRANCHES")
        for b in app.store.branches:
            names = ", ".join(a.name for a in b.admins) or "-"
            print(f"  {b.branch_id} | {b.name} | {b.address} | {b.phone}")
            print(f"        products: {len(b)} | admins: {names}")
        print("-" * 56)
        print("1. Add branch   2. Edit branch   3. Remove branch   0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            branch = safe(lambda: app.store.add_branch(ask("Branch name"), ask("Address"), ask("Phone")))
            if branch:
                app.log.add("STORE", user.name, f"Added branch {branch.name}", branch)
                print(f"[V] Branch {branch.branch_id} created.")
        elif choice in {"2", "3"}:
            branch = pick(app.store.branches, "Choose branch:", str)
            if branch and choice == "2":
                print("(Leave blank to keep the current value)")
                safe(lambda: branch.update_info(ask("Name", branch.name), ask("Address", branch.address),
                                                ask("Phone", branch.phone)))
                app.log.add("STORE", user.name, f"Edited branch {branch.name}", branch)
                print("[V] Branch updated.")
            elif branch and confirm(f"Remove branch {branch.name}?"):
                if safe(lambda: app.store.remove_branch(branch)) is None and branch in app.store.branches:
                    pass
                else:
                    print("[V] Branch removed.")
        elif choice == "0":
            return
        else:
            print("[!] Invalid choice!")
        pause()


ACTIONS = [
    ("manage_admins", "Manage Admins", manage_admins),
    ("store_profile", "Store Profile", store_profile),
    ("manage_branches", "Manage Branches", manage_branches),
]
