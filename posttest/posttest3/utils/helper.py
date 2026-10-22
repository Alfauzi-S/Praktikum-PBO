import os
import sys


def clear_screen():
    if sys.stdin.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress ENTER to continue...")


def header(title):
    print("=" * 56)
    print(title.center(56))
    print("=" * 56)


def ask(prompt, default=None):
    text = input(f"{prompt}" + (f" [{default}]" if default not in (None, "") else "") + ": ").strip()
    return text if text else (default if default is not None else "")


def ask_int(prompt, minimum=None):
    try:
        value = int(input(f"{prompt}: ").strip())
    except ValueError:
        print("[!] Please enter a whole number!")
        return None
    if minimum is not None and value < minimum:
        print(f"[!] Value must be at least {minimum}!")
        return None
    return value


def ask_float(prompt):
    try:
        return float(input(f"{prompt}: ").strip())
    except ValueError:
        print("[!] Please enter a number!")
        return None


def confirm(prompt):
    return input(f"{prompt} (y/n): ").strip().lower() == "y"


def pick(items, title, label=str):
    """Tampilkan daftar bernomor, kembalikan item terpilih (atau None jika batal)."""
    if not items:
        print("  (nothing to show)")
        return None
    print(f"\n{title}")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {label(item)}")
    print("  0. Cancel")
    number = ask_int("Choose number", 0)
    if not number or number > len(items):
        return None
    return items[number - 1]


def safe(action):
    """Jalankan aksi; tampilkan pesan jika ValueError (validasi model)."""
    try:
        return action()
    except ValueError as error:
        print(f"[!] {error}")
        return None
