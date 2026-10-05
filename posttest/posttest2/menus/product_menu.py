from tabulate import tabulate
from utils import clear_screen, pause


def product_menu(products):
    while True:
        clear_screen()

        print("==========================================")
        print("             PRODUCT MANAGEMENT")
        print("==========================================")
        print("1. Show Products")
        print("2. Add Stock")
        print("3. Reduce Stock")
        print("4. Change Store Name")
        print("5. Back")
        print("==========================================")

        choice = input("Choose menu: ")

        if choice == "1":
            clear_screen()

            data = []

            for product in products:
                data.append([
                    product.id_product,
                    product.name,
                    f"Rp{product.price:,}",
                    product.stock,
                    product.category
                ])

            print(tabulate(
                data,
                headers=[
                    "ID Product",
                    "Name",
                    "Price",
                    "Stock",
                    "Category"
                ],
                tablefmt="grid"
            ))

            pause()

        elif choice == "2":
            clear_screen()

            for i, product in enumerate(products, start=1):
                print(f"{i}. {product.name}")

            try:
                number = int(input("Choose product: "))
                amount = int(input("Stock amount: "))

                if 1 <= number <= len(products):
                    products[number - 1].add_stock(amount)
                else:
                    print("Product not found!")

            except ValueError:
                print("Input must be a number!")

            pause()

        elif choice == "3":
            clear_screen()

            for i, product in enumerate(products, start=1):
                print(f"{i}. {product.name}")

            try:
                number = int(input("Choose product: "))
                amount = int(input("Stock amount: "))

                if 1 <= number <= len(products):
                    products[number - 1].reduce_stock(amount)
                else:
                    print("Product not found!")

            except ValueError:
                print("Input must be a number!")

            pause()

        elif choice == "4":
            clear_screen()

            print(f"Current Store Name: {products[0].store_name}")

            new_name = input("New Store Name: ")

            products[0].change_store_name(new_name)

            pause()

        elif choice == "5":
            break

        else:
            print("Invalid choice!")
            pause()