from tabulate import tabulate
from utils import clear_screen, pause


def customer_menu(customers):
    while True:
        clear_screen()

        print("==========================================")
        print("            CUSTOMER MANAGEMENT")
        print("==========================================")
        print("1. Show Customers")
        print("2. Change Address")
        print("3. Change Status")
        print("4. Change Customer Type")
        print("5. Back")
        print("==========================================")

        choice = input("Choose menu: ")

        if choice == "1":
            clear_screen()

            data = []

            for customer in customers:
                data.append([
                    customer.id_customer,
                    customer.name,
                    customer.phone,
                    customer.address,
                    customer.status
                ])

            print(tabulate(
                data,
                headers=[
                    "ID Customer",
                    "Name",
                    "Phone",
                    "Address",
                    "Status"
                ],
                tablefmt="grid"
            ))

            pause()

        elif choice == "2":
            clear_screen()

            for i, customer in enumerate(customers, start=1):
                print(f"{i}. {customer.name}")

            try:
                number = int(input("Choose customer: "))

                if 1 <= number <= len(customers):
                    new_address = input("New address: ")
                    customers[number - 1].change_address(new_address)
                else:
                    print("Customer not found!")

            except ValueError:
                print("Input must be a number!")

            pause()

        elif choice == "3":
            clear_screen()

            for i, customer in enumerate(customers, start=1):
                print(f"{i}. {customer.name}")

            try:
                number = int(input("Choose customer: "))

                if 1 <= number <= len(customers):
                    print("1. Active")
                    print("2. Inactive")

                    status_choice = input("Choose status: ")

                    try:
                        if status_choice == "1":
                            customers[number - 1].status = "Active"
                            print("Status changed successfully!")

                        elif status_choice == "2":
                            customers[number - 1].status = "Inactive"
                            print("Status changed successfully!")

                        else:
                            print("Invalid choice!")

                    except ValueError as error:
                        print(error)

                else:
                    print("Customer not found!")

            except ValueError:
                print("Input must be a number!")

            pause()

        elif choice == "4":
            clear_screen()

            print("1. Regular")
            print("2. Premium")
            print("3. VIP")

            type_choice = input("Choose customer type: ")

            try:
                if type_choice == "1":
                    customers[0].change_customer_type("Regular")

                elif type_choice == "2":
                    customers[0].change_customer_type("Premium")

                elif type_choice == "3":
                    customers[0].change_customer_type("VIP")

                else:
                    print("Invalid choice!")

            except ValueError as error:
                print(error)

            pause()

        elif choice == "5":
            break

        else:
            print("Invalid choice!")
            pause()