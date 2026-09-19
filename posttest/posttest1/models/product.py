class Product:
    store_name = "Jaya Computer"
    store_category = "Computer Devices and Accessories"
    total_products = 0

    def __init__(self, id_product, name, price, stock, category):
        self.id_product = id_product
        self.name = name
        self.price = price
        self.category = category
        self.__stock = stock

        Product.total_products += 1

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, new_stock):
        if new_stock < 0:
            raise ValueError("Stock cannot be negative!")
        else:
            self.__stock = new_stock

    def show_info(self):
        print(f"ID Product : {self.id_product}")
        print(f"Name       : {self.name}")
        print(f"Price      : Rp{self.price:,}")
        print(f"Stock      : {self.stock}")
        print(f"Category   : {self.category}")

    def add_stock(self, amount):
        if amount <= 0:
            print("Amount must be greater than 0!")
        else:
            self.__stock += amount
            print("Stock added successfully!")

    def reduce_stock(self, amount):
        if amount <= 0:
            print("Amount must be greater than 0!")
        elif amount > self.__stock:
            print("Not enough stock!")
        else:
            self.__stock -= amount
            print("Stock reduced successfully!")

    @classmethod
    def change_store_name(cls, new_name):
        if new_name.strip() == "":
            print("Store name cannot be empty!")
        else:
            cls.store_name = new_name
            print("Store name changed successfully!")

    @staticmethod
    def validate_price(price):
        return price > 0

    @staticmethod
    def format_price(price):
        return f"Rp{price:,}"