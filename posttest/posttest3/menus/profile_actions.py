from utils import clear_screen, pause, header, ask, confirm, safe


def edit_profile(person):
    """Ubah data profil (nama, telepon, email, dll). Kosongkan input = tidak diubah."""
    print("\n(Leave blank to keep the current value)")
    fields = dict(
        name=ask("Name", person.name),
        phone=ask("Phone", person.phone),
        gmail=ask("Email", person.gmail),
        birth_date=ask("Birth date (YYYY-MM-DD)", person.birth_date),
        gender=ask("Gender", person.gender),
    )
    if hasattr(person, "address"):
        fields["address"] = ask("Address", person.address)
    try:
        person.update_profile(**fields)
        print("[V] Profile updated.")
    except ValueError as error:
        print(f"[!] {error}")


def edit_username(app, person):
    new_username = ask("New username", person.username)
    if not app.username_available(new_username, ignore=person):
        print(f"[!] Username '{new_username}' is already taken!")
        return
    try:
        person.username = new_username
        print("[V] Username updated.")
    except ValueError as error:
        print(f"[!] {error}")


def change_own_password(person):
    old = ask("Current password")
    new = ask("New password (min 6 chars)")
    try:
        person.change_password(old, new)
        print("[V] Password changed.")
    except ValueError as error:
        print(f"[!] {error}")


def reset_password(person):
    """Dipakai admin/superadmin untuk akun orang lain (tanpa password lama)."""
    new = ask(f"New password for {person.username} (min 6 chars)")
    try:
        person.set_password(new)
        print("[V] Password reset.")
    except ValueError as error:
        print(f"[!] {error}")


def profile_menu(app, user):
    """Menu Profil & Akun: dipakai oleh semua role."""
    while True:
        clear_screen()
        header("MY PROFILE & ACCOUNT")
        user.show_person_info()
        print("-" * 56)
        print("1. Edit profile")
        print("2. Change username")
        print("3. Change password")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            edit_profile(user)
        elif choice == "2":
            edit_username(app, user)
        elif choice == "3":
            change_own_password(user)
        elif choice == "0":
            return
        else:
            print("[!] Invalid choice!")
        pause()
