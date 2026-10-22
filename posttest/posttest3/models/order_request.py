from datetime import datetime
from models.sale_item import SaleItem
from utils import ui


class OrderRequest:
    """Permintaan belanja dari customer. Menunggu diproses admin cabang."""

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"

    def __init__(self, id_request, customer, branch, note=""):
        self.id_request = id_request
        self.customer = customer                    # Asosiasi: OrderRequest -> Customer
        self.branch = branch                        # Asosiasi: OrderRequest -> Branch
        self.note = note
        self._items = []
        self.status = OrderRequest.PENDING
        self.created_at = datetime.now()
        self.handled_by = None
        self.reject_reason = ""
        self.sale = None

    @property
    def items(self):
        return list(self._items)

    def add_item(self, product, quantity):
        existing = next((i for i in self._items if i.product is product), None)
        wanted = quantity + (existing.quantity if existing else 0)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0!")
        if wanted > product.stock:
            raise ValueError(f"Not enough stock for {product.name}! Available: {product.stock}")
        if existing:
            existing.quantity = wanted
        else:
            self._items.append(SaleItem(product, quantity))     # Komposisi

    def remove_item(self, index):
        del self._items[index]

    @property
    def estimated_total(self):
        return sum(i.subtotal for i in self._items)

    def mark_completed(self, sale, admin):
        self.status, self.sale, self.handled_by = OrderRequest.COMPLETED, sale, admin

    def mark_rejected(self, admin, reason):
        self.status, self.handled_by, self.reject_reason = OrderRequest.REJECTED, admin, reason

    def show(self):
        lines = ui.kv_lines([
            ("Request", f"{ui.c(self.id_request, 'bold')}   {ui.status_badge(self.status)}"),
            ("Customer", f"{self.customer.name} ({ui.tier_badge(self.customer.membership_tier)})"),
            ("Branch", self.branch.name),
            ("Created", f"{self.created_at:%Y-%m-%d %H:%M}  ({ui.time_ago(self.created_at)})"),
        ] + ([("Note", self.note)] if self.note else [])
          + ([("Rejected", ui.c(self.reject_reason, "red"))] if self.reject_reason else [])
          + ([("Handled by", self.handled_by.name)] if self.handled_by else []), 11)
        ui.panel("REQUEST DETAIL", lines, "cyan")
        ui.table(["Item", "Qty", "Unit price", "Subtotal"],
                 [[i.product_name, str(i.quantity), ui.rupiah(i.unit_price), ui.rupiah(i.subtotal)]
                  for i in self._items], ["l", "r", "r", "r"])

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return (f"{self.id_request} | {self.customer.name} | {self.branch.name} | "
                f"{len(self)} item(s) | {ui.rupiah(self.estimated_total)} | {self.status}")
