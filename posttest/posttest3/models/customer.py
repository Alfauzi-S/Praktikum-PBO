from models.person import Person


class Customer(Person):
    TIERS = [(50_000_000, "Platinum"), (10_000_000, "Gold"), (1_000_000, "Silver"), (0, "Bronze")]
    DISCOUNT_RATES = {"Bronze": 0.0, "Silver": 0.01, "Gold": 0.05, "Platinum": 0.10}
    PERMISSIONS = frozenset({"view_products", "shop", "my_orders", "my_notifications", "profile"})

    def __init__(self, id_customer, name, username, password, phone, gmail, address,
                 birth_date="", gender=""):
        super().__init__(name, username, password, phone, gmail, birth_date, gender)
        self.id_customer = id_customer
        self._address = ""
        self.address = address
        self.membership_tier = "Bronze"
        self.loyalty_points = 0
        self.__total_spending = 0

    def get_role(self):
        return "Customer"

    def get_permissions(self):
        return Customer.PERMISSIONS

    def can_see(self, notification):
        return notification.customer is self

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not value or value.strip() == "":
            raise ValueError("Address cannot be empty!")
        self._address = value.strip()

    def update_profile(self, address=None, **kwargs):
        super().update_profile(**kwargs)
        if address is not None:
            self.address = address

    @property
    def total_spending(self):
        return self.__total_spending

    @property
    def discount_percentage(self):
        return int(Customer.DISCOUNT_RATES[self.membership_tier] * 100)

    def add_spending(self, amount):
        if amount < 0:
            raise ValueError("Spending cannot be negative!")
        self.__total_spending += amount
        self._auto_upgrade_membership()

    def _auto_upgrade_membership(self):
        # Tier ditentukan dari tabel data, bukan rantai if/elif
        new_tier = next(tier for limit, tier in Customer.TIERS if self.__total_spending >= limit)
        if new_tier != self.membership_tier:
            print(f"[+] {self._name} moved from [{self.membership_tier}] to [{new_tier}]")
            self.membership_tier = new_tier

    def add_points(self, points):
        if points < 0:
            raise ValueError("Points cannot be negative!")
        self.loyalty_points += points

    def show_person_info(self):
        super().show_person_info()
        print(f"Customer ID           : {self.id_customer}")
        print(f"Address               : {self._address}")
        print(f"Membership            : {self.membership_tier} ({self.discount_percentage}% discount)")
        print(f"Loyalty Points        : {self.loyalty_points}")
        print(f"Total Spending        : Rp{self.__total_spending:,.0f}")
