class Store:
    total_stores = 0
    default_location = "Samarinda"
    company_name = "Alfauzi Computer Store"

    def __init__(self, name, location=None):
        if not name or name.strip() == "":
            raise ValueError("[!] Store name cannot be empty!")
        
        self.name = name.strip()
        self.location = location if location else Store.default_location
        self._products = []
        self._staffs = []
        Store.total_stores += 1

    def add_product(self, product):
        if any(p.id_product == product.id_product for p in self._products):
            print(f"[!] Product '{product.name}' already exists in {self.name}!")
            return False
        
        self._products.append(product)
        print(f"[+] Product '{product.name}' added to {self.name}")
        return True

    def remove_product(self, id_product):
        initial_count = len(self._products)
        self._products = [p for p in self._products if p.id_product != id_product]
        
        if len(self._products) < initial_count:
            print(f"[-] Product {id_product} removed from {self.name}")
            return True
        else:
            print(f"[!] Product {id_product} not found in {self.name}")
            return False

    def get_product(self, id_product):
        for p in self._products:
            if p.id_product == id_product:
                return p
        return None

    def show_products(self):
        print(f"\n=== PRODUCTS AT {self.name} ===")
        if not self._products:
            print("  No products available.")
        else:
            for p in self._products:
                p.show_info()
        print(f"Total Products: {len(self._products)}\n")

    def add_staff(self, staff):
        if any(s.employee_id == staff.employee_id for s in self._staffs):
            print(f"[!] Staff '{staff.name}' already exists in {self.name}!")
            return False
        
        self._staffs.append(staff)
        print(f"[+] Staff '{staff.name}' ({staff.role}) joined {self.name}")
        return True

    def remove_staff(self, employee_id):
        initial_count = len(self._staffs)
        self._staffs = [s for s in self._staffs if s.employee_id != employee_id]
        
        if len(self._staffs) < initial_count:
            print(f"[-] Staff {employee_id} removed from {self.name}")
            return True
        else:
            print(f"[!] Staff {employee_id} not found in {self.name}")
            return False

    def get_staff(self, employee_id):
        for s in self._staffs:
            if s.employee_id == employee_id:
                return s
        return None

    def show_staffs(self):
        print(f"\n=== STAFF AT {self.name} ===")
        if not self._staffs:
            print("  No staff available.")
        else:
            for s in self._staffs:
                s.show_person_info()
        print(f"Total Staff: {len(self._staffs)}\n")

    def get_total_stock(self):
        return sum(p.stock for p in self._products)

    def get_total_products_value(self):
        return sum(p.price * p.stock for p in self._products)

    def get_active_staff_count(self):
        return sum(1 for s in self._staffs if s.is_active)

    def show_summary(self):
        print("\n" + "=" * 50)
        print(f"  STORE SUMMARY: {self.name}")
        print("=" * 50)
        print(f"  Location         : {self.location}")
        print(f"  Company          : {Store.company_name}")
        print(f"  Total Products   : {len(self._products)} items")
        print(f"  Total Stock      : {self.get_total_stock()} units")
        print(f"  Inventory Value  : Rp{self.get_total_products_value():,.0f}")
        print(f"  Total Staff      : {len(self._staffs)} people")
        print(f"  Active Staff     : {self.get_active_staff_count()} people")
        print("=" * 50 + "\n")

    def __str__(self):
        return f"Store: {self.name} ({self.location})"

    @classmethod
    def change_default_location(cls, new_location):
        if not new_location or new_location.strip() == "":
            raise ValueError("[!] Location cannot be empty!")
        old_location = cls.default_location
        cls.default_location = new_location.strip()
        print(f"[V] Default location changed: '{old_location}' → '{cls.default_location}'")

    @classmethod
    def change_company_name(cls, new_name):
        if not new_name or new_name.strip() == "":
            raise ValueError("[!] Company name cannot be empty!")
        cls.company_name = new_name.strip()
        print(f"[V] Company name changed to: {cls.company_name}")

    @classmethod
    def reset_total_stores(cls):
        cls.total_stores = 0

    @staticmethod
    def validate_store_name(name):
        if not name or len(name.strip()) < 3:
            return False
        return name.strip().isalnum() or all(c.isalnum() or c == ' ' for c in name)

    @staticmethod
    def format_location(location):
        if not location:
            return "Unknown"
        return location.strip().title()