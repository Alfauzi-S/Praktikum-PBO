from datetime import datetime
from models.sale_item import SaleItem
from utils import ui


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
            ui.warn(f"Not enough stock for {product.name}! Available: {product.stock}")
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

    @classmethod
    def estimate(cls, subtotal, discount_percentage):
        """Rincian harga: satu rumus dipakai nota, keranjang, dan pratinjau admin."""
        discount = subtotal * discount_percentage / 100
        tax = (subtotal - discount) * cls.tax / 100
        return {"subtotal": subtotal, "discount": discount, "tax": tax, "total": subtotal - discount + tax}

    @property
    def discount_amount(self):
        return Sale.estimate(self.subtotal, self.discount_percentage)["discount"]

    @property
    def tax_amount(self):
        return Sale.estimate(self.subtotal, self.discount_percentage)["tax"]

    def calculate_total(self):
        self.__total = Sale.estimate(self.subtotal, self.discount_percentage)["total"]
        return self.__total

    def checkout(self, payment):
        """Bayar lalu selesaikan. Hanya bergantung pada abstraksi PaymentMethod (DIP)."""
        if not self._items:
            ui.err("Cannot process an empty sale!")
            return False
        if self.is_completed:
            ui.err("This sale has already been processed!")
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
        """Struk bergaya kotak."""
        head = ui.kv_lines([
            ("Order ID", ui.c(self.id_sale, "bold")),
            ("Date", f"{self.created_at:%Y-%m-%d %H:%M}"),
            ("Branch", self.branch.name),
            ("Customer", f"{self.customer.name} ({ui.tier_badge(self.customer.membership_tier)})"),
            ("Handled by", self.handled_by.name),
        ], 11)
        lines = head + [ui.c(ui.SINGLE["h"] * (ui.W - 6), "gray")]
        for item in self._items:
            left = f"{item.product_name} x{item.quantity}"
            right = ui.rupiah(item.subtotal)
            lines.append(left + " " * max(1, ui.W - 6 - ui.vlen(left) - ui.vlen(right)) + right)
        lines.append(ui.c(ui.SINGLE["h"] * (ui.W - 6), "gray"))

        def money(label, value, style=None):
            text = ui.rupiah(value)
            gap = " " * max(1, ui.W - 6 - ui.vlen(label) - ui.vlen(text))
            return label + gap + (ui.c(text, *style) if style else text)

        lines.append(money("Subtotal", self.subtotal))
        if self.discount_percentage:
            lines.append(money(f"Discount {self.discount_percentage}%", -self.discount_amount, ("green",)))
        lines.append(money(f"Tax {Sale.tax}%", self.tax_amount))
        lines.append(money(ui.c("TOTAL", "bold"), self.total, ("bold", "green")))
        if self.payment:
            lines.append(ui.c(ui.SINGLE["h"] * (ui.W - 6), "gray"))
            lines.append(f"Paid via {self.payment.describe()}")
            lines.append(ui.c(f"Ref {self.payment.reference_code}", "dim"))
        print()
        ui.panel("SALES RECEIPT", lines, "green")

    # ---------- Operator overloading ----------
    def __len__(self):
        return len(self._items)

    def __lt__(self, other):
        return self.total < other.total

    def __gt__(self, other):
        return self.total > other.total

    def __str__(self):
        return f"{self.id_sale} | {self.customer.name} | {self.branch.name} | {ui.rupiah(self.total)}"

    @classmethod
    def change_tax(cls, new_tax):
        if new_tax < 0:
            raise ValueError("Tax cannot be negative!")
        cls.tax = new_tax
