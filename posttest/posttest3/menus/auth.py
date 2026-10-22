from utils import clear_screen, pause, header, ask, safe


def login(app):
    clear_screen()
    header("LOGIN")
    username = ask("Username")
    password = ask("Password")
    user = app.authenticate(username, password)
    if user is None:
        print("\n[!] Invalid username or password!")
        pause()
        return None
    if not user.is_active:
        print("\n[!] This account is inactive. Contact an admin.")
        pause()
        return None
    print(f"\n[V] Login successful! Welcome, {user.name} ({user.get_role()}).")
    pause()
    return user


def register_customer(app):
    clear_screen()
    header("REGISTER NEW CUSTOMER")
    data = dict(
        name=ask("Full name"), username=ask("Username"), password=ask("Password (min 6 chars)"),
        phone=ask("Phone number"), gmail=ask("Email"), address=ask("Address"),
        birth_date=ask("Birth date (YYYY-MM-DD, optional)"), gender=ask("Gender (optional)"),
    )
    customer = safe(lambda: app.register_customer(actor=data["name"], **data))
    if customer:
        print(f"\n[V] Registration successful! Your Customer ID: {customer.id_customer}")
    pause()
