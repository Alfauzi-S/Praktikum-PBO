import math

from models.payment import CashPayment, BankTransferPayment, EWalletPayment
from models.person import Person
from utils import ui, ask_valid, ask_float, choose, to_float


def _cash(customer, total):
    due = math.ceil(total)
    amount = ask_valid("Cash received (Rp)", to_float, default=due)
    return None if amount is None else CashPayment(customer.name, amount)


def _transfer(customer, total):
    bank = ask_valid("Bank name", default="BCA")
    if bank is None:
        return None
    account = ask_valid("Sender account number (8-16 digits)", BankTransferPayment.check_account)
    return None if account is None else BankTransferPayment(customer.name, bank, account)


def _ewallet(customer, total):
    provider = ask_valid("E-Wallet provider (GoPay / OVO / DANA)", default="GoPay")
    if provider is None:
        return None
    phone = ask_valid("Wallet phone number", Person.check_phone, default=customer.phone)
    if phone is None:
        return None
    balance = ask_valid("Customer wallet balance (Rp)", to_float)
    return None if balance is None else EWalletPayment(customer.name, provider, phone, balance)


# Tabel metode pembayaran: menambah metode baru = menambah satu baris (OCP)
PAYMENT_OPTIONS = [
    ("Cash", "no fee", "amount received", _cash),
    ("Bank Transfer", f"fee {ui.rupiah(BankTransferPayment.ADMIN_FEE)}", "bank + account number", _transfer),
    ("E-Wallet", f"fee {EWalletPayment.FEE_RATE * 100:.1f}%", "provider + phone + balance", _ewallet),
]


def choose_payment(customer, total):
    """Admin memilih metode & memasukkan data pembayaran. Mengembalikan PaymentMethod / None."""
    ui.panel("AMOUNT DUE", [f"{ui.c('Customer', 'dim')}  {customer.name}",
                            f"{ui.c('Total   ', 'dim')}  {ui.c(ui.rupiah(total), 'bold', 'green')}"], "yellow")
    option = choose(PAYMENT_OPTIONS, title="Payment method", headers=["Method", "Fee", "You will enter"],
                    row=lambda o: [ui.c(o[0], "bold"), o[1], o[2]], prompt="Select method")
    if option is None:
        return None
    print()
    return option[3](customer, total)
