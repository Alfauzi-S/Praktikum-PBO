"""Kanal notifikasi untuk pelanggan.

Ketiga kelas di bawah TIDAK saling berhubungan lewat pewarisan, tetapi sama-sama
punya method send(message). Ini adalah contoh Duck Typing.
"""
from utils import ui


def _line(tag, target, message, color):
    arrow = ui.SYM["arrow"]
    print(f"  {ui.c(f'{tag:<9}', 'bold', color)} {ui.c(arrow + ' ' + target, 'dim')}  {message}")


class EmailNotifier:
    def __init__(self, address):
        self.address = address

    def send(self, message):
        _line("EMAIL", self.address, message, "cyan")


class SMSNotifier:
    def __init__(self, phone):
        self.phone = phone

    def send(self, message):
        _line("SMS", self.phone, message, "magenta")


class WhatsAppNotifier:
    def __init__(self, phone):
        self.phone = phone

    def send(self, message):
        _line("WHATSAPP", self.phone, message, "green")


def notify_customer(channels, message):
    """Duck typing: kanal apa pun yang punya send() bisa dipakai."""
    for channel in channels:
        channel.send(message)


def build_channels(customer):
    """Kanal default untuk seorang customer."""
    return [EmailNotifier(customer.gmail), SMSNotifier(customer.phone)]
