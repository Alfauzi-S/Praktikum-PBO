from abc import ABC, abstractmethod
from datetime import datetime

from utils import ui


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
            raise ValueError("Payer name cannot be empty!")
        self._payer_name = payer_name.strip()      # Protected: dipakai subclass
        self._amount = 0                           # Protected: diisi saat process()
        self._notes = []                           # Protected: catatan hasil execute()
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

    def _note(self, text):
        """Dipakai subclass di execute() untuk mencatat detail yang ikut tampil di panel hasil."""
        self._notes.append(text)

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

    def failure_reason(self):
        """Alasan gagal; di-override subclass agar pesannya spesifik."""
        return "Payment data is invalid."

    def process(self, amount):
        """Alur yang sama untuk semua metode: validasi -> eksekusi -> status."""
        if amount <= 0:
            ui.err("Payment amount must be greater than 0!")
            return False

        self._amount = amount
        self._notes = []
        valid = self.validate()
        if valid:
            self.execute()
            self._generate_reference()
        self.is_paid = valid
        self._show_result(valid)
        return valid

    def _show_result(self, valid):
        lines = ui.kv_lines([
            ("Payer", self._payer_name),
            ("Amount", ui.rupiah(self._amount)),
            ("Fee", ui.rupiah(self.calculate_fee())),
            ("Total charge", ui.c(ui.rupiah(self.get_total_charge()), "bold")),
        ], 13) + [f"{ui.c('Detail', 'dim')}         {note}" for note in self._notes]
        if valid:
            lines.append(ui.c(f"{ui.SYM['ok']} PAYMENT VALIDATED   Ref {self.reference_code}", "bold", "green"))
        else:
            lines.append(ui.c(f"{ui.SYM['err']} PAYMENT REJECTED   {self.failure_reason()}", "bold", "red"))
        print()
        ui.panel(f"PAYMENT {ui.SYM['arrow']} {self.method_name}", lines, "green" if valid else "red")

    def describe(self):
        """Dioverride subclass; versi default dipakai jika tidak di-override."""
        return f"{self.method_name} by {self._payer_name}"

    # ---------- Operator overloading ----------
    def __str__(self):
        return f"{self.describe()} (fee {ui.rupiah(self.calculate_fee())})"

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
        self._note(f"Cash received {ui.rupiah(self.cash_given)}, change {ui.rupiah(self._change)}")

    def failure_reason(self):
        short = self.get_total_charge() - self.cash_given
        return f"Cash is short by {ui.rupiah(short)}."

    def describe(self):
        return f"Cash from {self._payer_name} (given {ui.rupiah(self.cash_given)})"


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

    @staticmethod
    def check_account(value):
        value = (value or "").strip()
        if not value.isdigit() or not 8 <= len(value) <= 16:
            raise ValueError("Account number must be 8-16 digits.")
        return value

    def validate(self):
        try:
            BankTransferPayment.check_account(self.__account_number)
        except ValueError:
            return False
        return True

    def calculate_fee(self):
        return BankTransferPayment.ADMIN_FEE

    def execute(self):
        self._note(f"Transferred via {self.bank_name} ({self.masked_account})")

    def failure_reason(self):
        return "Account number must be 8-16 digits."

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

    def _phone_ok(self):
        return self.phone.isdigit() and 10 <= len(self.phone) <= 13

    def validate(self):
        return self._phone_ok() and self.__balance >= self.get_total_charge()

    def calculate_fee(self):
        return self._amount * EWalletPayment.FEE_RATE

    def execute(self):
        self.__balance -= self.get_total_charge()
        self._note(f"{self.provider} {self.phone}, remaining balance {ui.rupiah(self.__balance)}")

    def failure_reason(self):
        if not self._phone_ok():
            return "Wallet phone number must be 10-13 digits."
        return f"Insufficient wallet balance ({ui.rupiah(self.__balance)})."

    def describe(self):
        return f"E-Wallet {self.provider} {self.phone}"
