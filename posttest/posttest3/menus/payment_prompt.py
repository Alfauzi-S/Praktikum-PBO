from models.payment import CashPayment, BankTransferPayment, EWalletPayment
from utils import ask, ask_float


def _cash(customer):
    amount = ask_float("Cash received (Rp)")
    return None if amount is None else CashPayment(customer.name, amount)


def _transfer(customer):
    return BankTransferPayment(customer.name, ask("Bank name"), ask("Sender account number"))


def _ewallet(customer):
    provider = ask("E-Wallet provider (GoPay/OVO/DANA)")
    phone = ask("E-Wallet phone number")
    balance = ask_float("Customer wallet balance (Rp)")
    return None if balance is None else EWalletPayment(customer.name, provider, phone, balance)


# Tabel metode pembayaran: menambah metode baru = menambah satu baris (OCP)
PAYMENT_OPTIONS = {
    "1": ("Cash", _cash),
    "2": ("Bank Transfer", _transfer),
    "3": ("E-Wallet", _ewallet),
}


def choose_payment(customer):
    """Admin memilih metode & memasukkan data pembayaran. Mengembalikan PaymentMethod / None."""
    print("\n--- Payment Method ---")
    for key, (label, _) in PAYMENT_OPTIONS.items():
        print(f"{key}. {label}")
    choice = input("Choose payment method: ").strip()
    if choice not in PAYMENT_OPTIONS:
        print("[!] Invalid payment method!")
        return None
    try:
        return PAYMENT_OPTIONS[choice][1](customer)
    except ValueError as error:
        print(f"[!] {error}")
        return None
