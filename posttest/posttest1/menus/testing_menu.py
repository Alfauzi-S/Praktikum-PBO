from utils import clear_screen, pause


def testing_menu(products, customers, sales, Product, Customer, Sale):
    while True:
        clear_screen()

        print("==========================================")
        print("               OOP TESTING")
        print("==========================================")
        print("1. Test Objects")
        print("2. Test Instance Method")
        print("3. Test Class Method")
        print("4. Test Static Method")
        print("5. Test Getter and Setter")
        print("6. Test Inheritance")
        print("7. Run All Tests")
        print("8. Back")
        print("==========================================")

        choice = input("Choose menu: ")

        if choice == "1":
            clear_screen()

            print("========== OBJECT TEST ==========")
            print(f"Product objects  : {len(products)}")
            print(f"Customer objects : {len(customers)}")
            print(f"Sale objects     : {len(sales)}")

            print("\nProduct Objects:")
            for product in products:
                print(f"- {product.id_product} | {product.name}")

            print("\nCustomer Objects:")
            for customer in customers:
                print(f"- {customer.id_customer} | {customer.name}")

            print("\nSale Objects:")
            for sale in sales:
                print(f"- {sale.id_sale} | {sale.product.name}")

            pause()

        elif choice == "2":
            clear_screen()

            print("========== INSTANCE METHOD ==========")

            print("\nProduct.show_info()")
            products[0].show_info()

            print("\nCustomer.show_info()")
            customers[0].show_info()

            print("\nSale.show_receipt()")
            sales[0].show_receipt()

            pause()

        elif choice == "3":
            clear_screen()

            print("========== CLASS METHOD ==========")

            print(f"Old Store Name : {Product.store_name}")
            Product.change_store_name("Alfauzi Computer Store")
            print(f"New Store Name : {Product.store_name}")

            print()

            print(f"Old Store Branch : {Customer.store_branch}")
            Customer.change_store_branch("Balikpapan")
            print(f"New Store Branch : {Customer.store_branch}")

            print()

            print(f"Old Tax : {Sale.tax}%")
            Sale.change_tax(10)
            print(f"New Tax : {Sale.tax}%")

            pause()

        elif choice == "4":
            clear_screen()

            print("========== STATIC METHOD ==========")

            print(f"Validate Price  : {Product.validate_price(500000)}")
            print(f"Validate Phone  : {Customer.validate_phone('081234567890')}")
            print(f"Format Price    : {Product.format_price(750000)}")
            print(f"Discount Result : {Sale.calculate_discount(750000, 10)}")

            pause()

        elif choice == "5":
            clear_screen()

            print("========== GETTER AND SETTER ==========")

            product = products[0]

            print(f"Current Stock : {product.stock}")

            print("\nTesting valid setter...")
            try:
                product.stock = 20
                print(f"New Stock     : {product.stock}")
            except ValueError as error:
                print(error)

            print("\nTesting invalid setter...")
            try:
                product.stock = -10
            except ValueError as error:
                print(f"Error : {error}")

            pause()

        elif choice == "6":
            clear_screen()

            print("========== INHERITANCE ==========")

            customer = customers[0]

            print("Parent Class  : Person")
            print("Child Class   : Customer")

            print("\nCalling method from Person:")
            customer.show_person_info()

            pause()

        elif choice == "7":
            clear_screen()

            print("==========================================")
            print("             RUN ALL OOP TESTS")
            print("==========================================")

            print("\n1. Object Test")
            print(f"Product objects  : {len(products)}")
            print(f"Customer objects : {len(customers)}")
            print(f"Sale objects     : {len(sales)}")

            print("\n2. Instance Method")
            products[0].show_info()

            print("\n3. Class Method")
            print(f"Store Name : {Product.store_name}")

            print("\n4. Static Method")
            print(f"Valid Price : {Product.validate_price(500000)}")

            print("\n5. Getter")
            print(f"Current Stock : {products[0].stock}")

            print("\n6. Valid Setter")
            try:
                products[0].stock = 25
                print(f"New Stock : {products[0].stock}")
            except ValueError as error:
                print(error)

            print("\n7. Invalid Setter")
            try:
                products[0].stock = -5
            except ValueError as error:
                print(f"Error : {error}")

            print("\n8. Inheritance")
            customers[0].show_person_info()

            print("\nAll OOP tests completed!")
            pause()

        elif choice == "8":
            break

        else:
            print("Invalid choice!")
            pause()