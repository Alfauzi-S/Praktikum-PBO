from models.person import Person
from menus.profile_actions import edit_profile, edit_username, reset_password
from menus.views import choose_branch
from utils import ui, pause, ask_valid, run_form, confirm, choose, read_menu_choice, safe


# ------------------------------------------------------------------ admins
def _admin_rows(a):
    name = ui.c(a.name, "bold", "magenta") if a.get_role() == "Super Admin" else a.name
    return [name, a.username, a.branch.name if a.branch else "All branches",
            str(a.orders_processed), ui.status_badge("Active" if a.is_active else "Inactive")]


def _create_admin(app, user, crumb):
    ui.screen("Create admin", crumb)
    branch = choose_branch(app.store.branches, "Assign the new admin to which branch?")
    if not branch:
        return

    def check_username(value):
        value = Person.check_username(value)
        if not app.username_available(value):
            raise ValueError(f"Username '{value}' is already taken!")
        return value

    data = run_form(f"Create admin for {branch.name}", [
        dict(key="name", label="Full name", checker=Person.check_name),
        dict(key="username", label="Username", checker=check_username),
        dict(key="password", label="Password (min 6)", checker=Person.check_password, secret=True),
        dict(key="phone", label="Phone (10-13 digits)", checker=Person.check_phone),
        dict(key="gmail", label="Email", checker=Person.check_gmail),
        dict(key="birth_date", label="Birth date (optional)", required=False),
        dict(key="gender", label="Gender (optional)", required=False),
    ], crumb)
    if data is None:
        return
    admin = safe(lambda: app.register_admin(branch=branch, actor=user.name, **data))
    if admin:
        ui.ok(f"Admin {admin.employee_id} '{admin.name}' created for {branch.name}.")


def manage_admins(app, user):
    crumb = "Dashboard > Admins"
    while True:
        ui.screen("Manage admins", crumb)
        admins = app.admins
        ui.stat_cards([("Branch admins", str(sum(1 for a in admins if a.get_role() == "Admin")), "cyan"),
                       ("Active", str(sum(1 for a in admins if a.is_active)), "green"),
                       ("Branches", str(len(app.store)), "yellow")])
        ui.table(["Name", "Username", "Branch", "Orders", "Status"],
                 [_admin_rows(a) for a in admins], ["l", "l", "l", "r", "l"], title="Accounts (super admin in purple)")
        ui.menu([("Create admin", ""), ("Edit profile", ""), ("Change username", ""), ("Reset password", ""),
                 ("Move to another branch", ""), ("Activate / Deactivate", "")], "ADMIN ACTIONS", back="Back")
        choice = read_menu_choice(6)
        if choice is None:
            pause()
            continue
        if choice == 0:
            return
        if choice == 1:
            _create_admin(app, user, crumb)
            pause()
            continue
        admin = choose(admins, title="Which admin?", headers=["ID", "Name", "Role"],
                       row=lambda a: [a.employee_id, a.name, a.get_role()], prompt="Admin number")
        if admin is None:
            continue
        if choice == 2:
            edit_profile(admin, crumb)
        elif choice == 3:
            edit_username(app, admin, crumb)
        elif choice == 4:
            reset_password(admin, crumb)
        elif choice == 5:
            branch = choose_branch(app.store.branches, f"Move {admin.name} to which branch?")
            if branch:
                if admin.branch:
                    admin.branch.remove_admin(admin)
                branch.add_admin(admin)
                ui.ok(f"{admin.name} now works at {branch.name}.")
        elif choice == 6:
            if admin is user:
                ui.err("You cannot deactivate your own account.")
            else:
                admin.is_active = not admin.is_active
                ui.ok(f"{admin.name} is now {'ACTIVE' if admin.is_active else 'INACTIVE'}.")
        app.log.add("ACCOUNT", user.name, f"Updated admin {admin.name}", admin.branch)
        pause()


# ------------------------------------------------------------------ store profile
def store_profile(app, user):
    crumb = "Dashboard > Store profile"
    while True:
        store = app.store
        ui.screen("Store profile", crumb)
        ui.panel("STORE", ui.kv_lines([
            ("Name", ui.c(store.name, "bold")), ("Tagline", store.tagline),
            ("Phone", store.phone), ("Email", store.email), ("Branches", str(len(store))),
        ], 10), "yellow")
        ui.menu([("Edit store profile", "")], "ACTIONS", back="Back")
        choice = read_menu_choice(1)
        if choice is None:
            pause()
        elif choice == 0:
            return
        else:
            data = run_form("Edit store profile", [
                dict(key="name", label="Store name", default=store.name),
                dict(key="tagline", label="Tagline", default=store.tagline),
                dict(key="phone", label="Phone", default=store.phone),
                dict(key="email", label="Email", default=store.email),
            ], crumb)
            if data is not None:
                try:
                    store.update_profile(**data)
                except ValueError as error:
                    ui.err(str(error))
                else:
                    app.log.add("STORE", user.name, "Updated store profile")
                    ui.ok("Store profile updated.")
            pause()


# ------------------------------------------------------------------ branches
def _branch_rows(app, b):
    return [b.branch_id, ui.c(b.name, "bold"), str(len(b)), str(len(b.admins)), ui.rupiah(app.revenue_for([b]))]


def _branch_details(branches):
    lines = []
    for b in branches:
        admins = ", ".join(a.name for a in b.admins) or "-"
        lines += [ui.c(f"{b.branch_id}  {b.name}", "bold"), f"   {b.address}  |  {b.phone}", f"   Admin: {admins}"]
    ui.panel("BRANCH DETAILS", lines, "blue")


def manage_branches(app, user):
    crumb = "Dashboard > Branches"
    while True:
        ui.screen("Manage branches", crumb)
        branches = app.store.branches
        ui.table(["ID", "Branch", "Products", "Admins", "Revenue"],
                 [_branch_rows(app, b) for b in branches], ["l", "l", "r", "r", "r"], title="Branches")
        _branch_details(branches)
        ui.menu([("Add branch", ""), ("Edit branch", ""), ("Remove branch", "")], "BRANCH ACTIONS", back="Back")
        choice = read_menu_choice(3)
        if choice is None:
            pause()
            continue
        if choice == 0:
            return
        if choice == 1:
            data = run_form("Add branch", [
                dict(key="name", label="Branch name"), dict(key="address", label="Address"),
                dict(key="phone", label="Phone"),
            ], crumb)
            if data is not None:
                branch = safe(lambda: app.store.add_branch(**data))
                if branch:
                    app.log.add("STORE", user.name, f"Added branch {branch.name}", branch)
                    ui.ok(f"Branch {branch.branch_id} '{branch.name}' created.")
            pause()
            continue
        branch = choose(branches, title="Which branch?", headers=["ID", "Branch"],
                        row=lambda b: [b.branch_id, b.name], prompt="Branch number")
        if branch is None:
            continue
        if choice == 2:
            data = run_form(f"Edit {branch.name}", [
                dict(key="name", label="Name", default=branch.name),
                dict(key="address", label="Address", default=branch.address),
                dict(key="phone", label="Phone", default=branch.phone),
            ], crumb)
            if data is not None:
                try:
                    branch.update_info(**data)
                except ValueError as error:
                    ui.err(str(error))
                else:
                    app.log.add("STORE", user.name, f"Edited branch {branch.name}", branch)
                    ui.ok("Branch updated.")
        elif choice == 3 and confirm(f"Remove branch {branch.name}?"):
            try:
                app.store.remove_branch(branch)
            except ValueError as error:
                ui.err(str(error))
            else:
                ui.ok("Branch removed.")
        pause()


ACTIONS = [
    ("manage_admins", "Manage Admins", manage_admins, None),
    ("store_profile", "Store Profile", store_profile, None),
    ("manage_branches", "Manage Branches", manage_branches, None),
]
