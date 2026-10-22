from datetime import datetime
from models.sale_item import SaleItem


class Sale:
    """Pesanan resmi yang dibuat admin setelah pembayaran divalidasi."""

    tax = 11

    def __init__(self, id_sale, customer, branch, handled_by):
        self.id_sale = id_sale
        self.customer = customer                    # Asosiasi: Sale -> Customer
        self.branch = branch                        # Asosiasi: Sale -> Branch
        self.handled_by = handled_by                # Asosiasi: Sale -> Admin
        self.payment = None                         # Asosiasi: Sale -> PaymentMethod (abstraksi)
        self._items = []
        self.discount_percentage = 0
        self.__total = 0
        self.is_completed = False
        self.created_at = datetime.now()

    @property
    def total(self):
        return self.__total

    @property
    def items(self):
        return list(self._items)

    @property
    def subtotal(self):
        return sum(i.subtotal for i in self._items)

    def add_item(self, product, quantity):
        """Membuat SaleItem DI DALAM Sale (komposisi) dan mengurangi stok."""
        if quantity <= 0 or quantity > product.stock:
            print(f"[!] Not enough stock for {product.name}! Available: {product.stock}")
            return False
        existing = next((i for i in self._items if i.product is product), None)
        if existing:
            existing.quantity += quantity
        else:
            self._items.append(SaleItem(product, quantity))
        product.reduce_stock(quantity)
        return True

    def set_discount(self, percentage):
        if not 0 <= percentage <= 100:
            raise ValueError("Discount must be between 0 and 100!")
        self.discount_percentage = percentage

    @property
    def discount_amount(self):
        return self.subtotal * self.discount_percentage / 100

    @property
    def tax_amount(self):
        return (self.subtotal - self.discount_amount) * Sale.tax / 100

    def calculate_total(self):
        self.__total = self.subtotal - self.discount_amount + self.tax_amount
        return self.__total

    def checkout(self, payment):
        """Bayar lalu selesaikan. Hanya bergantung pada abstraksi PaymentMethod (DIP)."""
        if not self._items:
            print("[!] Cannot process an empty sale!")
            return False
        if self.is_completed:
            print("[!] This sale has already been processed!")
            return False

        self.calculate_total()
        if not payment.process(self.total):
            return False

        self.payment = payment
        self.customer.add_points(int(self.total // 10000))
        self.customer.add_spending(self.total)
        self.handled_by.record_order()
        self.is_completed = True
        return True

    def cancel(self):
        """Batalkan sale yang belum selesai dan kembalikan stok."""
        for item in self._items:
            item.product.stock += item.quantity
        self._items = []

    def show_receipt(self):
        print("\n" + "=" * 50)
        print("              SALES RECEIPT")
        print("=" * 50)
        print(f"Order ID    : {self.id_sale}")
        print(f"Branch      : {self.branch.name}")
        print(f"Customer    : {self.customer.name} ({self.customer.membership_tier})")
        print(f"Handled by  : {self.handled_by.name}")
        print(f"Date        : {self.created_at:%Y-%m-%d %H:%M:%S}")
        print("-" * 50)
        for item in self._items:
            print(f"  {item}")
        print("-" * 50)
        print(f"Subtotal    : Rp{self.subtotal:,.0f}")
        if self.discount_percentage:
            print(f"Discount    : {self.discount_percentage}% (-Rp{self.discount_amount:,.0f})")
        print(f"Tax ({Sale.tax}%)   : +Rp{self.tax_amount:,.0f}")
        print("=" * 50)
        print(f"TOTAL       : Rp{self.total:,.0f}")
        if self.payment:
            print(f"Payment     : {self.payment} | Ref {self.payment.reference_code}")
        print("=" * 50)

    # ---------- Operator overloading ----------
    def __len__(self):
        return len(self._items)

    def __lt__(self, other):
        return self.total < other.total

    def __gt__(self, other):
        return self.total > other.total

    def __str__(self):
        return f"{self.id_sale} | {self.customer.name} | {self.branch.name} | Rp{self.total:,.0f}"

    @classmethod
    def change_tax(cls, new_tax):
        if new_tax < 0:
            raise ValueError("Tax cannot be negative!")
        cls.tax = new_tax
