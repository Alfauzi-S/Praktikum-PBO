from models.payment import CashPayment, BankTransferPayment, EWalletPayment
from models.notifier import build_channels, notify_customer


def _ask_cash(customer):
    return CashPayment(customer.name, float(input("Cash given (Rp): ")))


def _ask_transfer(customer):
    bank = input("Bank name: ").strip()
    account = input("Account number: ").strip()
    return BankTransferPayment(customer.name, bank, account)


def _ask_ewallet(customer):
    provider = input("E-Wallet provider (e.g. GoPay/OVO/DANA): ").strip()
    phone = input("Phone number: ").strip()
    balance = float(input("Wallet balance (Rp): "))
    return EWalletPayment(customer.name, provider, phone, balance)


# Menu pembayaran berbasis tabel: menambah metode baru cukup menambah satu baris
# di sini, tanpa mengubah Sale maupun alur menu (OCP).
PAYMENT_OPTIONS = {
    "1": ("Cash", _ask_cash),
    "2": ("Bank Transfer", _ask_transfer),
    "3": ("E-Wallet", _ask_ewallet),
}


def choose_payment(customer):
    """Menampilkan pilihan pembayaran dan mengembalikan objek PaymentMethod (atau None)."""
    print("\n--- Payment Method ---")
    for key, (label, _) in PAYMENT_OPTIONS.items():
        print(f"{key}. {label}")

    choice = input("Choose payment method: ").strip()
    if choice not in PAYMENT_OPTIONS:
        print("[!] Invalid payment method!")
        return None

    try:
        return PAYMENT_OPTIONS[choice][1](customer)
    except ValueError as e:
        print(f"[!] Invalid payment input: {e}")
        return None


def send_confirmation(customer, sale):
    print("\n--- Notification ---")
    notify_customer(
        build_channels(customer),
        f"Hi {customer.name}, payment for {sale.id_sale} (Rp{sale.total:,.0f}) received. Thank you!",
    )
