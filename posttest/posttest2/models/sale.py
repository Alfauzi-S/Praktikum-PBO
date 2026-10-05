class Sale:
    total_sales = 0
    tax = 11
    currency = "IDR"

    def __init__(self, id_sale, customer, product, quantity, discount_percentage=0):
        self.id_sale = id_sale
        self.customer = customer
        self.product = product
        self.quantity = quantity
        self.discount_percentage = discount_percentage
        self.__total = 0

        Sale.total_sales += 1

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, new_total):
        if new_total < 0:
            raise ValueError("Total cannot be negative!")
        else:
            self.__total = new_total

    def calculate_total(self):
        subtotal = self.product.price * self.quantity
        after_discount = Sale.calculate_discount(subtotal, self.discount_percentage)
        
        tax_amount = after_discount * (Sale.tax / 100)
        self.__total = after_discount + tax_amount

    def process_sale(self):
        if self.quantity <= 0:
            print("Quantity must be greater than 0!")
            return False

        if self.quantity > self.product.stock:
            print("Not enough product stock!")
            return False

        self.calculate_total()
        self.product.reduce_stock(self.quantity)

        print("Sale processed successfully!")
        return True

    def show_receipt(self):
        subtotal = self.product.price * self.quantity
        after_discount = Sale.calculate_discount(subtotal, self.discount_percentage)
        discount_amount = subtotal - after_discount
        
        tax_amount = after_discount * (Sale.tax / 100)

        print("\n==========================================")
        print("              SALES RECEIPT")
        print("==========================================")
        print(f"Sale ID     : {self.id_sale}")
        print(f"Customer    : {self.customer.name}")
        print(f"Product     : {self.product.name}")
        print(f"Price       : Rp{self.product.price:,}")
        print(f"Quantity    : {self.quantity}")
        print(f"Subtotal    : Rp{subtotal:,}")

        if self.discount_percentage > 0:
            print(f"Discount    : {self.discount_percentage}% (-Rp{discount_amount:,.0f})")
        
        if Sale.tax > 0:
            print(f"Tax ({Sale.tax}%)   : +Rp{tax_amount:,.0f}")
        
        print(f"Total       : Rp{self.total:,.0f}")
        print("==========================================")

    @classmethod
    def change_tax(cls, new_tax):
        if new_tax < 0:
            print("Tax cannot be negative!")
        else:
            cls.tax = new_tax
            print(f"Tax changed successfully to {cls.tax}%!")

    @staticmethod
    def calculate_discount(total, percentage):
        if percentage < 0 or percentage > 100:
            return total
        else:
            return total - (total * percentage / 100)