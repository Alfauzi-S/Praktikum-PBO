from abc import ABC, abstractmethod
from datetime import datetime


class PaymentMethod(ABC):
    """Abstract Base Class: kontrak untuk semua metode pembayaran di toko.

    Subclass WAJIB mengimplementasikan validate(), calculate_fee(), dan execute().
    Alur pembayaran (process) sama untuk semua subclass sehingga ditulis sekali
    di sini sebagai method konkret.
    """

    method_name = "Payment"
    total_payments = 0

    def __init__(self, payer_name):
        if not payer_name or payer_name.strip() == "":
            raise ValueError("[!] Payer name cannot be empty!")
        self._payer_name = payer_name.strip()      # Protected: dipakai subclass
        self._amount = 0                           # Protected: diisi saat process()
        self.__reference_code = ""                 # Private: dibuat otomatis
        self.is_paid = False
        PaymentMethod.total_payments += 1

    @property
    def reference_code(self):
        return self.__reference_code

    def _generate_reference(self):
        """Method konkret internal: membuat kode referensi unik."""
        stamp = datetime.now().strftime("%H%M%S")
        self.__reference_code = f"{self.method_name[:3].upper()}-{PaymentMethod.total_payments:04d}-{stamp}"

    # ---------- Abstract methods (kontrak) ----------
    @abstractmethod
    def validate(self):
        """Kembalikan True jika pembayaran boleh dilakukan."""

    @abstractmethod
    def calculate_fee(self):
        """Kembalikan biaya tambahan metode pembayaran ini (Rp)."""

    @abstractmethod
    def execute(self):
        """Lakukan pembayaran (ubah saldo / catat uang masuk)."""

    # ---------- Method konkret (dipakai bersama semua subclass) ----------
    def get_total_charge(self):
        return self._amount + self.calculate_fee()

    def process(self, amount):
        """Alur yang sama untuk semua metode: validasi -> eksekusi -> status."""
        if amount <= 0:
            print("[!] Payment amount must be greater than 0!")
            return False

        self._amount = amount
        print(f"\n[Payment] {self.method_name} | Payer: {self._payer_name}")
        print(f"          Amount: Rp{amount:,.0f} + Fee: Rp{self.calculate_fee():,.0f} "
              f"= Rp{self.get_total_charge():,.0f}")

        if not self.validate():
            self.is_paid = False
            print(f"[!] {self.method_name} payment FAILED.")
            return False

        self.execute()
        self._generate_reference()
        self.is_paid = True
        print(f"[V] {self.method_name} payment SUCCESS. Ref: {self.reference_code}")
        return True

    def describe(self):
        """Dioverride subclass; versi default dipakai jika tidak di-override."""
        return f"{self.method_name} by {self._payer_name}"

    # ---------- Operator overloading ----------
    def __str__(self):
        return f"{self.describe()} (fee Rp{self.calculate_fee():,.0f})"

    def __lt__(self, other):
        return self.calculate_fee() < other.calculate_fee()

    def __gt__(self, other):
        return self.calculate_fee() > other.calculate_fee()


class CashPayment(PaymentMethod):
    method_name = "Cash"

    def __init__(self, payer_name, cash_given):
        super().__init__(payer_name)
        self.cash_given = cash_given
        self._change = 0                           # Protected: kembalian

    @property
    def change(self):
        return self._change

    def validate(self):
        return self.cash_given >= self.get_total_charge()

    def calculate_fee(self):
        return 0

    def execute(self):
        self._change = self.cash_given - self.get_total_charge()
        print(f"          Cash given: Rp{self.cash_given:,.0f} | Change: Rp{self._change:,.0f}")

    def describe(self):
        return f"Cash from {self._payer_name} (given Rp{self.cash_given:,.0f})"


class BankTransferPayment(PaymentMethod):
    method_name = "BankTransfer"
    ADMIN_FEE = 2500

    def __init__(self, payer_name, bank_name, account_number):
        super().__init__(payer_name)
        self.bank_name = bank_name
        self.__account_number = account_number     # Private: data sensitif

    @property
    def masked_account(self):
        return "*" * (len(self.__account_number) - 4) + self.__account_number[-4:]

    def validate(self):
        acc = self.__account_number
        return acc.isdigit() and 8 <= len(acc) <= 16

    def calculate_fee(self):
        return BankTransferPayment.ADMIN_FEE

    def execute(self):
        print(f"          Transferred via {self.bank_name} ({self.masked_account})")

    def describe(self):
        return f"Bank transfer {self.bank_name} {self.masked_account}"


class EWalletPayment(PaymentMethod):
    method_name = "EWallet"
    FEE_RATE = 0.015

    def __init__(self, payer_name, provider, phone, balance):
        super().__init__(payer_name)
        self.provider = provider
        self.phone = phone
        self.__balance = balance                   # Private: saldo dompet digital

    @property
    def balance(self):
        return self.__balance

    def validate(self):
        phone_ok = self.phone.isdigit() and 10 <= len(self.phone) <= 13
        return phone_ok and self.__balance >= self.get_total_charge()

    def calculate_fee(self):
        return self._amount * EWalletPayment.FEE_RATE

    def execute(self):
        self.__balance -= self.get_total_charge()
        print(f"          {self.provider} ({self.phone}) | Remaining balance: Rp{self.__balance:,.0f}")

    def describe(self):
        return f"E-Wallet {self.provider} {self.phone}"
