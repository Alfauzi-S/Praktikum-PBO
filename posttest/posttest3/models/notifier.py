"""Kanal notifikasi untuk pelanggan.

Ketiga kelas di bawah TIDAK saling berhubungan lewat pewarisan, tetapi sama-sama
punya method send(message). Ini adalah contoh Duck Typing.
"""


class EmailNotifier:
    def __init__(self, address):
        self.address = address

    def send(self, message):
        print(f"  [EMAIL -> {self.address}] {message}")


class SMSNotifier:
    def __init__(self, phone):
        self.phone = phone

    def send(self, message):
        print(f"  [SMS -> {self.phone}] {message}")


class WhatsAppNotifier:
    def __init__(self, phone):
        self.phone = phone

    def send(self, message):
        print(f"  [WHATSAPP -> {self.phone}] {message}")


def notify_customer(channels, message):
    """Duck typing: kanal apa pun yang punya send() bisa dipakai."""
    for channel in channels:
        channel.send(message)


def build_channels(customer):
    """Kanal default untuk seorang customer."""
    return [EmailNotifier(customer.gmail), SMSNotifier(customer.phone)]
