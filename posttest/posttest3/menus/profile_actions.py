from models.person import Person
from utils import ui, pause, ask_valid, run_form, read_menu_choice, safe


def edit_profile(person, crumb="Profile"):
    """Ubah data profil. ENTER = pertahankan nilai lama."""
    fields = [
        dict(key="name", label="Name", checker=Person.check_name, default=person.name),
        dict(key="phone", label="Phone", checker=Person.check_phone, default=person.phone),
        dict(key="gmail", label="Email", checker=Person.check_gmail, default=person.gmail),
        dict(key="birth_date", label="Birth date (YYYY-MM-DD)", default=person.birth_date or None, required=False),
        dict(key="gender", label="Gender", default=person.gender or None, required=False),
    ]
    if hasattr(person, "address"):
        from models.customer import Customer
        fields.append(dict(key="address", label="Address", checker=Customer.check_address, default=person.address))
    data = run_form(f"Edit profile - {person.name}", fields, crumb)
    if data is None:
        return False
    try:
        person.update_profile(**data)
    except ValueError as error:
        ui.err(str(error))
        return False
    ui.ok("Profile updated.")
    return True


def edit_username(app, person, crumb="Profile"):
    ui.screen(f"Change username - {person.name}", crumb)

    def check(value):
        value = Person.check_username(value)
        if not app.username_available(value, ignore=person):
            raise ValueError(f"Username '{value}' is already taken!")
        return value

    new_username = ask_valid("New username", check, default=person.username)
    if new_username is None:
        return False
    person.username = new_username
    ui.ok(f"Username is now '{new_username}'.")
    return True


def change_own_password(person, crumb="Profile"):
    ui.screen("Change password", crumb)

    def check_old(value):
        if not person.verify_password(value):
            raise ValueError("That is not your current password.")
        return value

    old = ask_valid("Current password", check_old, secret=True)
    if old is None:
        return False
    new = ask_valid("New password (min 6 characters)", Person.check_password, secret=True)
    if new is None:
        return False

    def check_same(value):
        if value != new:
            raise ValueError("Passwords do not match.")
        return value

    if ask_valid("Repeat new password", check_same, secret=True) is None:
        return False
    person.set_password(new)
    ui.ok("Password changed.")
    return True


def reset_password(person, crumb="Accounts"):
    """Dipakai admin/superadmin untuk akun orang lain (tanpa password lama)."""
    ui.screen(f"Reset password - {person.username}", crumb)
    new = ask_valid("New password (min 6 characters)", Person.check_password, secret=True)
    if new is None:
        return False
    person.set_password(new)
    ui.ok(f"Password for {person.username} has been reset.")
    return True


def profile_menu(app, user):
    """Menu Profil & Akun: dipakai oleh semua role."""
    while True:
        ui.screen("My profile & account", "Dashboard > Profile")
        user.show_person_info()
        ui.menu([("Edit profile", ""), ("Change username", ""), ("Change password", "")],
                "WHAT DO YOU WANT TO DO?", back="Back")
        choice = read_menu_choice(3)
        if choice is None:
            pause()
            continue
        if choice == 0:
            return
        if choice == 1:
            edit_profile(user, "Dashboard > Profile")
        elif choice == 2:
            edit_username(app, user, "Dashboard > Profile")
        elif choice == 3:
            change_own_password(user, "Dashboard > Profile")
        pause()
