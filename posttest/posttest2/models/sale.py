from models.sale_item import SaleItem
from datetime import datetime

class Sale:
    total_sales = 0
    tax = 11

    def __init__(self, id_sale, customer):
        self.id_sale = id_sale
        self.customer = customer
        self._items = []
        self.discount_percentage = 0
        self.__total = 0
        self.is_completed = False
        Sale.total_sales += 1

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, new_total):
        if new_total < 0:
            raise ValueError("[!] Total cannot be negative!")
        self.__total = new_total

    @property
    def items_count(self):
        return len(self._items)

    def add_item(self, product, quantity):
        if quantity <= 0:
            print("[!] Quantity must be greater than 0!")
            return False

        if quantity > product.stock:
            print(f"[!] Not enough stock for {product.name}!")
            return False

        for item in self._items:
            if item.product.id_product == product.id_product:
                additional = quantity
                if additional > product.stock:
                    print(f"[!] Not enough stock for {product.name}!")
                    return False
                item.quantity += additional
                item.subtotal = item.quantity * item.product.price
                product.reduce_stock(additional)
                print(f"[+] Added {additional}x more {product.name} to sale. Total: {item.quantity}x")
                return True

        new_item = SaleItem(product, quantity)
        self._items.append(new_item)
        product.reduce_stock(quantity)
        print(f"[+] Added {quantity}x {product.name} to sale.")
        return True

    def remove_item(self, product_id):
        initial_count = len(self._items)
        
        for item in self._items:
            if item.product.id_product == product_id:
                item.product.stock += item.quantity
                print(f"[+] Stock for '{item.product.name}' restored by {item.quantity}.")
                break
        
        self._items = [item for item in self._items if item.product.id_product != product_id]
        
        if len(self._items) < initial_count:
            print(f"[-] Item {product_id} removed from sale.")
            return True
        else:
            print(f"[!] Item {product_id} not found in sale.")
            return False

    def set_discount(self, percentage):
        if 0 <= percentage <= 100:
            self.discount_percentage = percentage
            print(f"[+] Discount set to {percentage}%")
        else:
            print("[!] Discount must be between 0 and 100!")

    def calculate_total(self):
        grand_subtotal = sum(item.subtotal for item in self._items)
        after_discount = Sale.calculate_discount(grand_subtotal, self.discount_percentage)
        tax_amount = after_discount * (Sale.tax / 100)
        self.total = after_discount + tax_amount

    def process_sale(self):
        if not self._items:
            print("[!] Cannot process an empty sale!")
            return False

        if self.is_completed:
            print("[!] This sale has already been processed!")
            return False

        self.calculate_total()

        points_earned = int(self.total // 10000)
        self.customer.add_points(points_earned)

        self.customer.add_spending(self.total)

        self.is_completed = True
        print("[V] Sale processed successfully!")
        return True

    def show_receipt(self):
        if not self._items:
            print("[!] No items in this sale!")
            return

        grand_subtotal = sum(item.subtotal for item in self._items)
        after_discount = Sale.calculate_discount(grand_subtotal, self.discount_percentage)
        discount_amount = grand_subtotal - after_discount
        tax_amount = after_discount * (Sale.tax / 100)

        print("\n" + "=" * 50)
        print("              SALES RECEIPT")
        print("=" * 50)
        print(f"Sale ID     : {self.id_sale}")
        print(f"Customer    : {self.customer.name} ({self.customer.membership_tier})")
        print(f"Date        : {Sale._get_current_date()}")
        print("-" * 50)
        
        for item in self._items:
            print(item)

        print("-" * 50)
        print(f"Subtotal    : Rp{grand_subtotal:,.0f}")

        if self.discount_percentage > 0:
            print(f"Discount    : {self.discount_percentage}% (-Rp{discount_amount:,.0f})")

        if Sale.tax > 0:
            print(f"Tax ({Sale.tax}%)   : +Rp{tax_amount:,.0f}")

        print("=" * 50)
        print(f"TOTAL       : Rp{self.total:,.0f}")
        print("=" * 50 + "\n")

    def show_items(self):
        print(f"\n=== ITEMS IN SALE {self.id_sale} ===")
        if not self._items:
            print("  No items yet.")
        else:
            for i, item in enumerate(self._items, 1):
                print(f"{i}. {item}")
        print(f"Total Items: {len(self._items)}\n")

    @classmethod
    def change_tax(cls, new_tax):
        if new_tax < 0:
            print("[!] Tax cannot be negative!")
        else:
            old_tax = cls.tax
            cls.tax = new_tax
            print(f"[V] Tax changed: {old_tax}% → {cls.tax}%")

    @classmethod
    def reset_total_sales(cls):
        cls.total_sales = 0

    @staticmethod
    def calculate_discount(total, percentage):
        if percentage < 0 or percentage > 100:
            return total
        return total - (total * percentage / 100)

    @staticmethod
    def _get_current_date():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")