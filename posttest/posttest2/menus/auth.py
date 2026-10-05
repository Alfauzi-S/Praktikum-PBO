from utils.helper import clear_screen, pause
from models.customer import Customer

def login(staffs_db, customers_db):
    clear_screen()
    print("=" * 50)
    print("              LOGIN")
    print("=" * 50)
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    for staff in staffs_db:
        if staff.username == username and staff.password == password:
            return staff, "staff"
    
    for cust in customers_db:
        if cust.username == username and cust.password == password:
            return cust, "customer"
    
    print("\n[!] Invalid username or password!")
    pause()
    return None, None


def register_customer(staffs_db, customers_db):
    clear_screen()
    print("=" * 50)
    print("         REGISTER NEW CUSTOMER")
    print("=" * 50)
    
    name = input("Full Name: ").strip()
    username = input("Username: ").strip()
    
    all_users = staffs_db + customers_db
    if any(user.username == username for user in all_users):
        print(f"\n[!] Username '{username}' is already taken! Please choose another.")
        pause()
        return
    
    password = input("Password (min 6 characters): ").strip()
    if len(password) < 6:
        print("\n[!] Password must be at least 6 characters!")
        pause()
        return
        
    phone = input("Phone Number: ").strip()
    gmail = input("Email (Gmail): ").strip()
    address = input("Address: ").strip()
    birth_date = input("Birth Date (YYYY-MM-DD, optional): ").strip()
    gender = input("Gender (Male/Female, optional): ").strip()
    
    try:
        new_id = f"C{len(customers_db) + 1:03d}"
        new_customer = Customer(
            id_customer=new_id,
            name=name,
            username=username,
            password=password,
            address=address,
            phone=phone,
            gmail=gmail,
            birth_date=birth_date,
            gender=gender
        )
        
        customers_db.append(new_customer)
        
        print("\n" + "=" * 50)
        print("[V] REGISTRATION SUCCESSFUL!")
        print("=" * 50)
        print(f"Welcome, {new_customer.name}!")
        print(f"Your Customer ID is: {new_id}")
        print("Please use your new username and password to login.")
        print("=" * 50)
        
    except ValueError as e:
        print(f"\n[!] Registration failed due to invalid input:")
        print(f"    {e}")
        
    pause()