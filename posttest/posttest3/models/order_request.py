from datetime import datetime
from models.sale_item import SaleItem


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
        print(f"Request   : {self.id_request}  [{self.status}]")
        print(f"Customer  : {self.customer.name} ({self.customer.membership_tier})")
        print(f"Branch    : {self.branch.name}")
        print(f"Created   : {self.created_at:%Y-%m-%d %H:%M}")
        if self.note:
            print(f"Note      : {self.note}")
        for i, item in enumerate(self._items, 1):
            print(f"  {i}. {item}")
        print(f"Estimated subtotal: Rp{self.estimated_total:,.0f}")
        if self.reject_reason:
            print(f"Rejected reason: {self.reject_reason}")

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return (f"{self.id_request} | {self.customer.name} | {self.branch.name} | "
                f"{len(self)} item(s) | Rp{self.estimated_total:,.0f} | {self.status}")
