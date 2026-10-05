from tabulate import tabulate
from models.sale import Sale
from utils import clear_screen, pause


def sale_menu(products, customers, sales):
    while True:
        clear_screen()

        print("==========================================")
        print("              SALES MANAGEMENT")
        print("==========================================")
        print("1. Create Sale")
        print("2. Show Sales")
        print("3. Change Tax")
        print("4. Back")
        print("==========================================")

        choice = input("Choose menu: ")

        if choice == "1":
            clear_screen()

            print("CUSTOMERS")

            for i, customer in enumerate(customers, start=1):
                print(f"{i}. {customer.name}")

            try:
                customer_number = int(input("Choose customer: "))

                if not 1 <= customer_number <= len(customers):
                    print("Customer not found!")
                    pause()
                    continue

                print("\nPRODUCTS")

                for i, product in enumerate(products, start=1):
                    print(
                        f"{i}. {product.name} "
                        f"(Stock: {product.stock})"
                    )

                product_number = int(input("Choose product: "))

                if not 1 <= product_number <= len(products):
                    print("Product not found!")
                    pause()
                    continue

                quantity = int(input("Quantity: "))

                print("\nDISCOUNT OPTIONS")
                print("1. No Discount")
                print("2. Apply Discount")

                discount_choice = input("Choose: ")

                discount_percentage = 0

                if discount_choice == "2":
                    try:
                        discount_percentage = float(input("Discount percentage (%): "))

                        if discount_percentage < 0 or discount_percentage > 100:
                            print("Invalid discount! Using 0%")
                            discount_percentage = 0

                    except ValueError:
                        print("Invalid input! Using 0%")

                sale_id = f"S{len(sales) + 1:03d}"

                sale = Sale(
                    sale_id,
                    customers[customer_number - 1],
                    products[product_number - 1],
                    quantity,
                    discount_percentage
                )

                if sale.process_sale():
                    sales.append(sale)
                    sale.show_receipt()

            except ValueError as error:
                print(error)

            pause()

        elif choice == "2":
            clear_screen()

            if len(sales) == 0:
                print("No sales found!")

            else:
                data = []

                for sale in sales:
                    data.append([
                        sale.id_sale,
                        sale.customer.name,
                        sale.product.name,
                        sale.quantity,
                        f"Rp{sale.total:,.0f}"
                    ])

                print(tabulate(
                    data,
                    headers=[
                        "ID Sale",
                        "Customer",
                        "Product",
                        "Quantity",
                        "Total"
                    ],
                    tablefmt="grid"
                ))

            pause()

        elif choice == "3":
            clear_screen()

            print(f"Current Tax: {Sale.tax}%")

            try:
                new_tax = float(input("New Tax (%): "))
                Sale.change_tax(new_tax)

            except ValueError:
                print("Input must be a number!")

            pause()

        elif choice == "4":
            break

        else:
            print("Invalid choice!")
            pause()