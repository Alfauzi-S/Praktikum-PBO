class SaleItem:
    """Satu baris barang. Dibuat di dalam Sale / OrderRequest (komposisi)."""

    def __init__(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0!")
        self.product = product                      # Asosiasi: SaleItem -> Product
        self.product_name = product.name            # snapshot agar riwayat tetap akurat
        self.unit_price = product.price
        self.quantity = quantity

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product_name} x{self.quantity} @ Rp{self.unit_price:,.0f} = Rp{self.subtotal:,.0f}"
