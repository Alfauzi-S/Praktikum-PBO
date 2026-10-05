class Product:
    total_products = 0
    VALID_CATEGORIES = ["Peripheral", "Laptop", "PC", "Monitor", "Aksesoris", "Lainnya"]

    def __init__(self, id_product, name, price, stock, category):
        if not name or name.strip() == "":
            raise ValueError("[!] Product name cannot be empty!")
        
        if category not in Product.VALID_CATEGORIES:
            raise ValueError(f"[!] Invalid category! Must be one of: {', '.join(Product.VALID_CATEGORIES)}")
        
        self.id_product = id_product
        self.name = name
        self.category = category
        self._price = 0
        self._stock = 0
        self.price = price
        self.stock = stock
        Product.total_products += 1

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if not isinstance(new_price, (int, float)):
            raise ValueError("[!] Price must be a number!")
        if new_price <= 0:
            raise ValueError("[!] Price must be greater than 0!")
        self._price = float(new_price)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, new_stock):
        if not isinstance(new_stock, int):
            raise ValueError("[!] Stock must be an integer!")
        if new_stock < 0:
            raise ValueError("[!] Stock cannot be negative!")
        self._stock = new_stock

    def add_stock(self, qty):
        if qty <= 0:
            raise ValueError("[!] Quantity to add must be greater than 0!")
        self.stock += qty
        print(f"[+] Stock for '{self.name}' added by {qty}. New stock: {self._stock}")

    def reduce_stock(self, qty):
        if qty <= 0:
            print("[!] Quantity to reduce must be greater than 0!")
            return False
        
        if qty > self._stock:
            print(f"[!] Not enough stock for '{self.name}'! Available: {self._stock}, Requested: {qty}")
            return False
        
        self.stock -= qty 
        return True

    def show_info(self):
        print(f"[{self.id_product}] {self.name}")
        print(f"  Category : {self.category}")
        print(f"  Price    : Rp{self._price:,.0f}")
        print(f"  Stock    : {self._stock} unit")
        print("-" * 30)

    def __str__(self):
        return f"[{self.id_product}] {self.name} - Rp{self._price:,.0f} (Stok: {self._stock})"

    @classmethod
    def add_category(cls, new_category):
        if not new_category or new_category.strip() == "":
            raise ValueError("[!] Category cannot be empty!")
        new_category = new_category.strip()
        if new_category in cls.VALID_CATEGORIES:
            print(f"[!] Category '{new_category}' already exists!")
            return False
        cls.VALID_CATEGORIES.append(new_category)
        print(f"[+] Category '{new_category}' added successfully!")
        return True

    @classmethod
    def remove_category(cls, category_to_remove):
        if not category_to_remove or category_to_remove.strip() == "":
            raise ValueError("[!] Category cannot be empty!")
        category_to_remove = category_to_remove.strip()
        if category_to_remove not in cls.VALID_CATEGORIES:
            print(f"[!] Category '{category_to_remove}' does not exist!")
            return False
        if len(cls.VALID_CATEGORIES) <= 1:
            print("[!] Cannot remove the last category!")
            return False
        cls.VALID_CATEGORIES.remove(category_to_remove)
        print(f"[-] Category '{category_to_remove}' removed successfully!")
        return True

    @classmethod
    def show_categories(cls):
        print("\n=== VALID PRODUCT CATEGORIES ===")
        for i, cat in enumerate(cls.VALID_CATEGORIES, 1):
            print(f"  {i}. {cat}")
        print("=" * 30 + "\n")

    @staticmethod
    def validate_price(price):
        return isinstance(price, (int, float)) and price > 0

    @staticmethod
    def format_price(price):
        if not isinstance(price, (int, float)):
            return "Rp0"
        return f"Rp{float(price):,.0f}"