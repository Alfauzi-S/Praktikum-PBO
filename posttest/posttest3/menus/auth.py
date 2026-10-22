from models.person import Person
from models.customer import Customer
from utils import ui, pause, ask, ask_valid, run_form

DEMO_ACCOUNTS = [
    ("Super Admin", "superadmin", "super123"),
    ("Admin Samarinda", "admin_smr", "admin123"),
    ("Admin Balikpapan", "admin_bpn", "admin123"),
    ("Customer", "rina_m", "password1"),
]


def login(app):
    for attempt in range(1, 4):
        ui.screen("Login", "Main menu > Login")
        ui.panel("DEMO ACCOUNTS (for testing)",
                 [f"{ui.pad(ui.c(role, 'dim'), 18)} {ui.pad(ui.c(user, 'bold'), 14)} / {pw}"
                  for role, user, pw in DEMO_ACCOUNTS], "gray")
        ui.hint("Type /q at any prompt to go back.")
        print()
        username = ask_valid("Username")
        if username is None:
            return None
        password = ask_valid("Password", secret=True)
        if password is None:
            return None
        user = app.authenticate(username, password)
        if user is None:
            ui.err(f"Wrong username or password. Attempt {attempt} of 3.")
            pause()
            continue
        if not user.is_active:
            ui.err("This account is inactive. Please contact an admin.")
            pause()
            return None
        ui.ok(f"Welcome back, {ui.c(user.name, 'bold')}!  ({user.get_role()})")
        pause()
        return user
    ui.err("Too many failed attempts.")
    pause()
    return None


def register_customer(app):
    def check_username(value):
        value = Person.check_username(value)
        if not app.username_available(value):
            raise ValueError(f"Username '{value}' is already taken!")
        return value

    data = run_form("Register new customer", [
        dict(key="name", label="Full name", checker=Person.check_name),
        dict(key="username", label="Username (min 3, no spaces)", checker=check_username),
        dict(key="password", label="Password (min 6 characters)", checker=Person.check_password, secret=True),
        dict(key="phone", label="Phone number (10-13 digits)", checker=Person.check_phone),
        dict(key="gmail", label="Email", checker=Person.check_gmail),
        dict(key="address", label="Address", checker=Customer.check_address),
        dict(key="birth_date", label="Birth date (YYYY-MM-DD, optional)", required=False),
        dict(key="gender", label="Gender (optional)", required=False),
    ], "Main menu > Register")
    if data is None:
        pause()
        return
    customer = app.register_customer(actor=data["name"], **data)
    print()
    ui.panel("REGISTRATION SUCCESSFUL", [
        ui.c(f"{ui.SYM['ok']} Welcome, {customer.name}!", "bold", "green"),
        f"Customer ID : {customer.id_customer}",
        f"Username    : {customer.username}",
        "You can now log in and start shopping.",
    ], "green")
    pause()
