class Branch:
    """Cabang toko. Memegang produk dan admin yang dibuat di luar (agregasi)."""

    def __init__(self, branch_id, name, address, phone):
        self.branch_id = branch_id
        self.name = name
        self.address = address
        self.phone = phone
        self._products = []         # Agregasi: Branch o-- Product
        self._admins = []           # Agregasi: Branch o-- Admin

    @property
    def products(self):
        return list(self._products)

    @property
    def admins(self):
        return list(self._admins)

    def update_info(self, name=None, address=None, phone=None):
        if name is not None:
            if not name.strip():
                raise ValueError("Branch name cannot be empty!")
            self.name = name.strip()
        if address is not None:
            self.address = address.strip()
        if phone is not None:
            self.phone = phone.strip()

    # ---------- Produk ----------
    def add_product(self, product):
        if self.get_product(product.id_product):
            raise ValueError(f"Product ID '{product.id_product}' already exists in {self.name}!")
        self._products.append(product)

    def remove_product(self, id_product):
        product = self.get_product(id_product)
        if not product:
            raise ValueError(f"Product '{id_product}' not found!")
        self._products.remove(product)

    def get_product(self, id_product):
        return next((p for p in self._products if p.id_product.lower() == id_product.lower()), None)

    def next_product_id(self):
        numbers = [int(p.id_product[1:]) for p in self._products if p.id_product[1:].isdigit()]
        return f"P{max(numbers, default=0) + 1:03d}"

    # ---------- Admin ----------
    def add_admin(self, admin):
        if admin not in self._admins:
            self._admins.append(admin)
        admin.branch = self

    def remove_admin(self, admin):
        if admin in self._admins:
            self._admins.remove(admin)
        if admin.branch is self:
            admin.branch = None

    def __len__(self):
        return len(self._products)

    def __str__(self):
        return f"{self.name} - {self.address}"
