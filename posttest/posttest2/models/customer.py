from models.person import Person

class Customer(Person):
    total_customers = 0

    def __init__(self, name, username, password, id_customer, address, phone, gmail, birth_date="", gender="", membership_tier="Bronze"):
        super().__init__(name, username, password, birth_date, gender)
        self.id_customer = id_customer
        self._address = ""
        self._phone = ""
        self.__gmail = ""
        self.address = address
        self.phone = phone
        self.gmail = gmail
        self.membership_tier = membership_tier
        self.loyalty_points = 0
        self.__total_spending = 0
        
        Customer.total_customers += 1

    def show_person_info(self):
        super().show_person_info()
        print(f"ID Customer           : {self.id_customer}")
        print(f"Address               : {self.address}")
        print(f"Phone                 : {self.phone}")
        print(f"Gmail                 : {self.gmail}")
        print(f"Membership            : {self.membership_tier}")
        print(f"Loyalty Points        : {self.loyalty_points}")
        print(f"Total Spending        : Rp{self.__total_spending:,}")

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, new_address):
        if not new_address or new_address.strip() == "":
            raise ValueError("[!] Address cannot be empty!")
        self._address = new_address.strip()

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, new_phone):
        if not new_phone or new_phone.strip() == "":
            raise ValueError("[!] Phone cannot be empty!")
        if len(new_phone) < 10 or len(new_phone) > 13:
            raise ValueError("[!] Invalid mobile number! Must be 10-13 digits.")
        if not new_phone.isdigit():
            raise ValueError("[!] Phone number must contain only digits!")
        self._phone = new_phone.strip()
        
    @property
    def gmail(self):
        return self.__gmail

    @gmail.setter
    def gmail(self, new_gmail):
        if not new_gmail or new_gmail.strip() == "":
            raise ValueError("[!] Gmail cannot be empty!")
        if "@" not in new_gmail or "." not in new_gmail.split("@")[-1]:
            raise ValueError("[!] Invalid gmail format! Example: user@gmail.com")
        if " " in new_gmail:
            raise ValueError("[!] Gmail cannot contain spaces!")
        self.__gmail = new_gmail.strip().lower()
    
    def change_phone(self, new_phone):
        self.phone = new_phone
        print(f"[V] Phone for {self.username} has been changed successfully.")
    
    def change_gmail(self, password, new_gmail):
        if self.password == password:
            self.gmail = new_gmail
            print(f"[V] Gmail for {self.username} has been changed successfully.")
        else:
            print("[!] Wrong password!")

    @property
    def total_spending(self):
        return self.__total_spending

    def add_spending(self, amount):
        if amount < 0:
            raise ValueError("[!] Spending amount cannot be negative!")
        self.__total_spending += amount
        self._auto_upgrade_membership()

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
            print(f"[+] Congratulations! {self._name} moved up a tier from [{old_tier}] to [{new_tier}]")

    def add_points(self, points):
        if points < 0:
            raise ValueError("[!] Points cannot be negative!")
        self.loyalty_points += points
        print(f"[+] {self._name} earned [{points}] points.")

    def redeem_points(self, points):
        if points > self.loyalty_points:
            print(f"[!] Not enough points! Current points: {self.loyalty_points}")
            return False
        self.loyalty_points -= points
        print(f"[+] {self._name} exchanged {points} points.")
        return True

    @staticmethod
    def calculate_discount(total_amount, membership_tier):
        discount_rates = {"Bronze": 0.0, "Silver": 0.01, "Gold": 0.05, "Platinum": 0.10}
        rate = discount_rates.get(membership_tier, 0.0)
        discount = int(total_amount * rate)
        return discount