from models.person import Person

class Staff(Person):
    total_staff = 0
    VALID_ROLES = ["Admin", "Kasir", "Manager", "Teknisi", "Gudang"]
    BONUS_THRESHOLD = 50
    BONUS_AMOUNT = 500_000

    def __init__(self, name, username, password, employee_id, role, salary, phone, gmail, birth_date="", gender=""):
        super().__init__(name, username, password, phone, gmail, birth_date, gender)
        self.employee_id = employee_id
        self._role = ""
        self.__salary = 0
        self.__total_bonus = 0
        self.role = role
        self.salary = salary
        self.total_sales_processed = 0
        self.is_active = True
        Staff.total_staff += 1

    def show_person_info(self):
        super().show_person_info()
        print(f"Employee ID           : {self.employee_id}")
        print(f"Role                  : {self._role}")
        print(f"Salary                : Rp{self.__salary:,}")
        print(f"Total Sales Processed : {self.total_sales_processed}")
        print(f"Total Bonus Earned    : Rp{self.__total_bonus:,}")
        print(f"Status                : {'Active' if self.is_active else 'Inactive'}")

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, new_role):
        if not new_role or new_role.strip() == "":
            raise ValueError("[!] Role cannot be empty!")
        if new_role not in Staff.VALID_ROLES:
            raise ValueError(f"[!] Invalid role! Must be one of: {', '.join(Staff.VALID_ROLES)}")
        self._role = new_role.strip()

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, new_salary):
        if not isinstance(new_salary, (int, float)):
            raise ValueError("[!] Salary must be a number!")
        if new_salary < 0:
            raise ValueError("[!] Salary cannot be negative!")
        self.__salary = new_salary

    def change_role(self, new_role):
        self.role = new_role
        print(f"[V] Role for {self._name} has been changed to [{new_role}] successfully.")

    def give_raise(self, amount):
        if amount <= 0:
            raise ValueError("[!] Raise amount must be positive!")
        old_salary = self.__salary
        self.__salary += amount
        print(f"[+] Salary for {self._name} raised: Rp{old_salary:,} → Rp{self.__salary:,}")

    def deactivate(self):
        self.is_active = False
        print(f"[-] Staff {self._name} ({self.employee_id}) has been deactivated.")
        
    def activate(self):
        self.is_active = True
        print(f"[+] Staff {self._name} ({self.employee_id}) has been activated.")

    def claim_bonus(self):
        if self.__total_bonus > 0:
            amount = self.__total_bonus
            self.__total_bonus = 0
            print(f"[V] Bonus sebesar Rp{amount:,} berhasil dicairkan oleh {self._name}!")
            return amount
        else:
            print(f"[!] {self._name} belum memiliki bonus yang bisa dicairkan.")
            return 0

    def _check_and_apply_bonus(self):
        if self.total_sales_processed > 0 and self.total_sales_processed % Staff.BONUS_THRESHOLD == 0:
            self.__total_bonus += Staff.BONUS_AMOUNT
            print(f"\n CONGRATULATIONS, {self._name}!")
            print(f"  Anda telah mencapai {self.total_sales_processed} transaksi.")
            print(f"  Bonus sebesar Rp{Staff.BONUS_AMOUNT:,} telah ditambahkan!")

    def process_transaction(self, sale):
        if not self.is_active:
            print(f"[!] Staff {self._name} is inactive. Cannot process transactions!")
            return False

        print(f"\n[Cashier {self._name}] Processing sale {sale.id_sale}...")
        
        if sale.process_sale():
            self.total_sales_processed += 1
            print(f"[V] Transaction {sale.id_sale} processed successfully by {self._name}.")
            self._check_and_apply_bonus()
            return True
        return False

    @classmethod
    def add_role(cls, new_role):
        if not new_role or new_role.strip() == "":
            raise ValueError("[!] Role cannot be empty!")
        new_role = new_role.strip()
        if new_role in cls.VALID_ROLES:
            print(f"[!] Role '{new_role}' already exists!")
            return False
        cls.VALID_ROLES.append(new_role)
        print(f"[+] Role '{new_role}' has been added successfully!")
        return True

    @classmethod
    def remove_role(cls, role_to_remove):
        if not role_to_remove or role_to_remove.strip() == "":
            raise ValueError("[!] Role cannot be empty!")
        role_to_remove = role_to_remove.strip()
        if role_to_remove not in cls.VALID_ROLES:
            print(f"[!] Role '{role_to_remove}' does not exist!")
            return False
        if len(cls.VALID_ROLES) <= 1:
            print("[!] Cannot remove the last role! At least one role must exist.")
            return False
        cls.VALID_ROLES.remove(role_to_remove)
        print(f"[-] Role '{role_to_remove}' has been removed successfully!")
        return True

    @classmethod
    def change_role_name(cls, old_role, new_role):
        if old_role not in cls.VALID_ROLES:
            print(f"[!] Role '{old_role}' does not exist!")
            return False
        if new_role in cls.VALID_ROLES:
            print(f"[!] Role '{new_role}' already exists!")
            return False
        index = cls.VALID_ROLES.index(old_role)
        cls.VALID_ROLES[index] = new_role
        print(f"[V] Role '{old_role}' changed to '{new_role}' successfully!")
        return True

    @classmethod
    def reset_valid_roles(cls):
        cls.VALID_ROLES = ["Admin", "Kasir", "Manager", "Teknisi", "Gudang"]
        print("[V] Valid roles has been reset to default!")

    @staticmethod
    def calculate_tax(salary):
        if salary <= 5_000_000:
            return 0
        elif salary <= 10_000_000:
            return salary * 0.05
        else:
            return salary * 0.10