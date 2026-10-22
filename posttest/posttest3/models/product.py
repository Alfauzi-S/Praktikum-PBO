class Product:
    VALID_CATEGORIES = ["Peripheral", "Laptop", "PC", "Monitor", "Aksesoris", "Lainnya"]

    def __init__(self, id_product, name, price, stock, category):
        self.id_product = id_product
        self._name = ""
        self._category = ""
        self._price = 0
        self._stock = 0
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or value.strip() == "":
            raise ValueError("Product name cannot be empty!")
        self._name = value.strip()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value not in Product.VALID_CATEGORIES:
            raise ValueError(f"Invalid category! Choose: {', '.join(Product.VALID_CATEGORIES)}")
        self._category = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a number greater than 0!")
        self._price = float(value)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Stock must be a non-negative integer!")
        self._stock = value

    def add_stock(self, qty):
        if qty <= 0:
            raise ValueError("Quantity must be greater than 0!")
        self.stock += qty

    def reduce_stock(self, qty):
        if qty <= 0 or qty > self._stock:
            return False
        self.stock -= qty
        return True

    # ---------- Operator overloading ----------
    def __str__(self):
        return f"[{self.id_product}] {self._name} - Rp{self._price:,.0f} (Stock: {self._stock})"

    def __lt__(self, other):
        return self._price < other._price

    def __gt__(self, other):
        return self._price > other._price

    @classmethod
    def show_categories(cls):
        print("Categories: " + ", ".join(cls.VALID_CATEGORIES))

    @staticmethod
    def validate_price(price):
        return isinstance(price, (int, float)) and price > 0
