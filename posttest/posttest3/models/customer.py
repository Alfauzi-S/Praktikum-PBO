from models.person import Person
from utils import ui


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

    @staticmethod
    def check_address(value):
        if not value or value.strip() == "":
            raise ValueError("Address cannot be empty!")
        return value.strip()

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = Customer.check_address(value)

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

    # ---------- Progres tier (untuk ditampilkan di dashboard) ----------
    def next_tier(self):
        """(nama_tier_berikutnya, sisa_belanja) atau None jika sudah tertinggi."""
        higher = [(limit, tier) for limit, tier in Customer.TIERS if limit > self.__total_spending]
        if not higher:
            return None
        limit, tier = min(higher)
        return tier, limit - self.__total_spending

    @property
    def tier_progress(self):
        """Rasio 0..1 menuju tier berikutnya."""
        floor = next(limit for limit, tier in Customer.TIERS if tier == self.membership_tier)
        higher = [limit for limit, _ in Customer.TIERS if limit > floor]
        if not higher:
            return 1.0
        ceiling = min(higher)
        return (self.__total_spending - floor) / (ceiling - floor)

    def add_spending(self, amount):
        if amount < 0:
            raise ValueError("Spending cannot be negative!")
        self.__total_spending += amount
        self._auto_upgrade_membership()

    def _auto_upgrade_membership(self):
        # Tier ditentukan dari tabel data, bukan rantai if/elif
        new_tier = next(tier for limit, tier in Customer.TIERS if self.__total_spending >= limit)
        if new_tier != self.membership_tier:
            ui.ok(f"{ui.SYM['star']} {self._name} moved from {self.membership_tier} to {ui.tier_badge(new_tier)}!")
            self.membership_tier = new_tier

    def add_points(self, points):
        if points < 0:
            raise ValueError("Points cannot be negative!")
        self.loyalty_points += points

    def info_pairs(self):
        nxt = self.next_tier()
        progress = (f"{ui.progress_bar(self.tier_progress, 14)} {ui.rupiah(nxt[1])} to {nxt[0]}"
                    if nxt else "Highest tier reached")
        return super().info_pairs() + [
            ("Customer ID", self.id_customer),
            ("Address", self._address),
            ("Membership", f"{ui.tier_badge(self.membership_tier)} ({self.discount_percentage}% discount)"),
            ("Progress", progress),
            ("Points", str(self.loyalty_points)),
            ("Total spent", ui.rupiah(self.__total_spending)),
        ]
