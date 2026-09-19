from models import Product, Customer, Sale
from menus import product_menu, customer_menu, sale_menu, testing_menu
from utils import clear_screen, pause

product1 = Product(
    "P001",
    "Mechanical Keyboard",
    750000,
    10,
    "Keyboard"
)

product2 = Product(
    "P002",
    "Gaming Mouse",
    350000,
    15,
    "Mouse"
)

products = [
    product1,
    product2
]


customer1 = Customer(
    "C001",
    "Andi",
    "081234567890",
    "Samarinda"
)

customer2 = Customer(
    "C002",
    "Budi",
    "082345678901",
    "Balikpapan"
)

customers = [
    customer1,
    customer2
]


sale1 = Sale(
    "S001",
    customer1,
    product1,
    1
)

sale2 = Sale(
    "S002",
    customer2,
    product2,
    2
)

sale1.calculate_total()
sale2.calculate_total()

sales = [
    sale1,
    sale2
]


def main():
    while True:
        clear_screen()

        print("==============================================")
        print("       COMPUTER SALES MANAGEMENT SYSTEM")
        print("==============================================")
        print(f"Store : {Product.store_name}")
        print("Devices and Accessories")
        print("==============================================")
        print("1. Product Management")
        print("2. Customer Management")
        print("3. Sales Management")
        print("4. OOP Testing")
        print("5. Exit")
        print("==============================================")

        choice = input("Choose menu: ")

        if choice == "1":
            product_menu(products)

        elif choice == "2":
            customer_menu(customers)

        elif choice == "3":
            sale_menu(products, customers, sales)

        elif choice == "4":
            testing_menu(
                products,
                customers,
                sales,
                Product,
                Customer,
                Sale
            )

        elif choice == "5":
            clear_screen()

            print(
                "Thank you for using "
                "Computer Sales Management System!"
            )

            break

        else:
            print("Invalid choice!")
            pause()


if __name__ == "__main__":
    main()