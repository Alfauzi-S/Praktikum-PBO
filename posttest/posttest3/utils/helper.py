"""Fungsi bantu input: prompt bergaya, validasi per kolom, form, pemilih bernomor."""
import getpass
import os
import sys

from utils import ui

CANCEL_WORD = "/q"


def clear_screen():
    ui.clear()


def pause(message="Press ENTER to continue"):
    input(ui.c(f"\n  {ui.SYM['enter']} {message} ", "dim"))


# ------------------------------------------------------------------ konversi + validasi angka
def to_int(value, minimum=None):
    try:
        number = int(str(value).replace(",", "").replace("_", "").strip())
    except ValueError:
        raise ValueError("Please enter a whole number (e.g. 3).")
    if minimum is not None and number < minimum:
        raise ValueError(f"Value must be at least {minimum}.")
    return number


def to_float(value):
    try:
        return float(str(value).replace(",", "").replace("_", "").strip())
    except ValueError:
        raise ValueError("Please enter a number (e.g. 150000).")


# ------------------------------------------------------------------ prompt dasar
def ask(label, default=None, secret=False):
    shown = f" [{default}]" if default not in (None, "") else ""
    prompt = f"  {ui.c(ui.SYM['arrow'], 'bold', 'cyan')} {label}{ui.c(shown, 'dim')}: "
    if secret and sys.stdin.isatty():
        text = getpass.getpass(prompt).strip()
    else:
        text = input(prompt).strip()
    return text if text else (str(default) if default not in (None,) else "")


def ask_valid(label, checker=None, default=None, required=True, secret=False):
    """Tanya sampai valid. Mengembalikan nilai, atau None jika pengguna mengetik /q."""
    while True:
        raw = ask(label, default, secret)
        if raw.lower() == CANCEL_WORD:
            return None
        if raw == "":
            if not required:
                return ""
            ui.err("This field is required.")
            continue
        if checker is None:
            return raw
        try:
            return checker(raw)
        except ValueError as error:
            ui.err(str(error))


def ask_int(label, minimum=None, default=None):
    return ask_valid(label, lambda v: to_int(v, minimum), default)


def ask_float(label, default=None):
    return ask_valid(label, to_float, default)


def confirm(label, default=False):
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"  {ui.c('?', 'bold', 'yellow')} {label} {ui.c(suffix, 'dim')}: ").strip().lower()
    if answer == "":
        return default
    return answer in {"y", "yes", "ya"}


def run_form(title, fields, crumb=""):
    """Form beberapa kolom. fields = [dict(key, label, checker, default, required, secret)].

    Setiap kolom divalidasi langsung (salah -> diulang). Ketik /q untuk membatalkan.
    """
    ui.screen(title, crumb)
    ui.hint(f"Type {CANCEL_WORD} at any prompt to cancel.")
    print()
    data = {}
    for field in fields:
        value = ask_valid(field["label"], field.get("checker"), field.get("default"),
                          field.get("required", True), field.get("secret", False))
        if value is None:
            ui.warn("Cancelled.")
            return None
        data[field["key"]] = value
    return data


# ------------------------------------------------------------------ pemilih
def choose(items, label=str, title=None, headers=None, row=None, aligns=None, prompt="Select number"):
    """Pilih satu item dari daftar bernomor. Kembalikan item, atau None jika batal (0 atau /q)."""
    if not items:
        ui.hint("Nothing to choose from.")
        return None
    if headers and row:
        ui.table(["#"] + headers, [[str(i)] + list(row(item)) for i, item in enumerate(items, 1)],
                 ["r"] + (aligns or ["l"] * len(headers)), title=title)
    else:
        if title:
            ui.section(title)
        for i, item in enumerate(items, 1):
            print(f"  {ui.c(f'{i:>2}', 'bold', 'cyan')}  {label(item)}")
    print(ui.c("   0  Cancel", "dim"))
    while True:
        raw = ask(f"{prompt} (0 = cancel)")
        if raw in {"0", "", CANCEL_WORD}:
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(items):
            return items[int(raw) - 1]
        ui.err(f"Enter a number between 1 and {len(items)}, or 0 to cancel.")


def read_menu_choice(count):
    """Baca pilihan menu 0..count. Kembalikan int atau None jika tidak valid."""
    raw = ask("Select")
    if raw.isdigit() and 0 <= int(raw) <= count:
        return int(raw)
    ui.err(f"Please choose a number between 0 and {count}.")
    return None


def safe(action):
    """Jalankan aksi; tampilkan pesan jika ValueError (validasi model)."""
    try:
        return action()
    except ValueError as error:
        ui.err(str(error))
        return None
