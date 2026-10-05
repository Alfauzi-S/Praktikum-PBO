from models.person import Person


class Customer(Person):
    total_customers = 0

    def __init__(self, name, username, password, id_customer, address, phone, gmail, birth_date="", gender="", membership_tier="Bronze"):
        super().__init__(name, username, password, birth_date, gender)
        self.id_customer = id_customer
        self.address = address
        self.phone = phone
        self.gmail = gmail
        self.membership_tier = membership_tier
        self.loyalty_points = 0
        self.__total_spending = 0
        Customer.total_customers += 1

    def show_person_info(self):
        super().show_person_info()
        print(f"ID Customer    : {self.id_customer}")
        print(f"Address        : {self.address}")
        print(f"Membership     : {self.membership_tier}")
        print(f"Loyalty Points : {self.loyalty_points}")
        print(f"Total Spending : Rp{self.__total_spending:,}")

    def change_address(self, new_address):
        if not new_address or new_address.strip() == "":
            raise ValueError("Address cannot be empty!")
        self.address = new_address
        print(f"[+] Alamat {self._name} berhasil diubah menjadi: {new_address}")
        
    def change_phone(self, new_phone):
        if not new_phone or new_phone.strip() == "":
            raise ValueError("Phone cannot be empty!")
        self.address = new_phone
        print(f"[+] Alamat {self._name} berhasil diubah menjadi: {new_phone}")


    @property
    def total_spending(self):
        return self.__total_spending

    def add_spending(self, amount):
        if amount < 0:
            raise ValueError("Spending amount cannot be negative!")
        self.__total_spending += amount
        self._auto_upgrade_membership()

    def add_points(self, points):
        if points < 0:
            raise ValueError("Points cannot be negative!")
        self.loyalty_points += points
        print(f"[+] {self._name} mendapatkan [{points}] poin loyalitas.")

    def redeem_points(self, points):
        if points > self.loyalty_points:
            print(f"[-] Poin tidak cukup! Poin saat ini: {self.loyalty_points}")
            return False
        self.loyalty_points -= points
        print(f"[+] {self._name} menukarkan {points} poin.")
        return True

    def _auto_upgrade_membership(self):
        if self.__total_spending >= 50_000_000:
            new_tier = "Platinum"
        elif self.__total_spending >= 10_000_000:
            new_tier = "Gold"
        elif self.__total_spending >= 1_000_000:
            new_tier = "Silver"
        else:
            new_tier = "Bronze"

        if new_tier != self.membership_tier:
            old_tier = self.membership_tier
            self.membership_tier = new_tier
            print(f"Selamat! {self._name} naik tier dari [{old_tier}] -> [{new_tier}]")


    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and 10 <= len(phone) <= 15

    @staticmethod
    def calculate_discount(total_amount, membership_tier):
        discount_rates = {"Bronze": 0.0, "Silver": 0.01, "Gold": 0.05, "Platinum": 0.10}
        rate = discount_rates.get(membership_tier, 0.0)
        discount = int(total_amount * rate)
        return discount
