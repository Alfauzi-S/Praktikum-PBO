class SaleItem:
    total_items_created = 0

    def __init__(self, product, quantity):
        if quantity <= 0:
            raise ValueError("[!] Quantity must be greater than 0!")
        
        self.product = product
        self.quantity = quantity
        self.subtotal = product.price * quantity
        SaleItem.total_items_created += 1

    def __str__(self):
        return (f"  {self.product.name} x{self.quantity} "
                f"@ Rp{self.product.price:,.0f} = Rp{self.subtotal:,.0f}")

    def get_info(self):
        print(f"  [{self.product.id_product}] {self.product.name}")
        print(f"    Qty    : {self.quantity}")
        print(f"    Price  : Rp{self.product.price:,.0f}")
        print(f"    Subtotal: Rp{self.subtotal:,.0f}")