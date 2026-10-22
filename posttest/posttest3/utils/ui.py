"""Komponen tampilan terminal: warna, kotak, tabel, kartu statistik, badge.

Hanya memakai standard library. Warna otomatis mati jika output bukan terminal
(atau variabel NO_COLOR diset), dan simbol otomatis diganti ASCII jika
FORCE_ASCII diset.
"""
import os
import re
import sys
from datetime import datetime

try:                                        # pastikan simbol kotak tampil benar
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                           # noqa: BLE001 - stream tidak mendukung reconfigure
    pass


def _color_enabled():
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return sys.stdout.isatty()


COLOR = _color_enabled()
UNICODE = not os.environ.get("FORCE_ASCII")
if COLOR and os.name == "nt":
    os.system("")                           # aktifkan ANSI di Windows 10+

W = 76                                      # lebar layar tetap agar rapi di terminal standar

_CODES = {
    "bold": 1, "dim": 2, "italic": 3, "underline": 4,
    "black": 30, "red": 31, "green": 32, "yellow": 33, "blue": 34, "magenta": 35,
    "cyan": 36, "white": 37, "gray": 90,
    "bright_red": 91, "bright_green": 92, "bright_yellow": 93, "bright_blue": 94,
    "bright_magenta": 95, "bright_cyan": 96,
    "bg_red": 41, "bg_green": 42, "bg_yellow": 43, "bg_blue": 44, "bg_magenta": 45,
    "bg_cyan": 46, "bg_gray": 100,
}
_ANSI = re.compile(r"\x1b\[[0-9;]*m")

if UNICODE:
    SINGLE = dict(tl="┌", tr="┐", bl="└", br="┘", h="─", v="│", lt="├", rt="┤", tt="┬", bt="┴", x="┼")
    DOUBLE = dict(tl="╔", tr="╗", bl="╚", br="╝", h="═", v="║")
    SYM = dict(ok="✔", err="✖", warn="▲", info="●", dot="●", bar="▌", arrow="›", enter="↵",
               full="█", empty="░", ellipsis="…", star="★")
else:
    SINGLE = dict(tl="+", tr="+", bl="+", br="+", h="-", v="|", lt="+", rt="+", tt="+", bt="+", x="+")
    DOUBLE = dict(tl="+", tr="+", bl="+", br="+", h="=", v="|")
    SYM = dict(ok="[OK]", err="[X]", warn="[!]", info="[i]", dot="*", bar="|", arrow=">", enter="<Enter>",
               full="#", empty="-", ellipsis="~", star="*")


# ------------------------------------------------------------------ dasar teks
def c(text, *styles):
    """Beri warna/gaya pada teks (no-op jika warna dimatikan)."""
    text = str(text)
    if not COLOR or not styles:
        return text
    codes = ";".join(str(_CODES[s]) for s in styles)
    return f"\033[{codes}m{text}\033[0m"


def strip(text):
    return _ANSI.sub("", str(text))


def vlen(text):
    """Panjang yang terlihat (tanpa kode warna)."""
    return len(strip(text))


def pad(text, width, align="left"):
    gap = max(0, width - vlen(text))
    if align == "right":
        return " " * gap + str(text)
    if align == "center":
        left = gap // 2
        return " " * left + str(text) + " " * (gap - left)
    return str(text) + " " * gap


def trunc(text, width):
    text = str(text)
    if vlen(text) <= width or "\x1b" in text:
        return text
    return text[: max(1, width - 1)] + SYM["ellipsis"]


# ------------------------------------------------------------------ format data
def rupiah(amount):
    """Rp 1.500.000 (format Indonesia)."""
    return "Rp " + f"{amount:,.0f}".replace(",", ".")


def time_ago(moment):
    seconds = int((datetime.now() - moment).total_seconds())
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{seconds // 60} min ago"
    if seconds < 86400:
        return f"{seconds // 3600} h ago"
    return f"{seconds // 86400} d ago"


def progress_bar(ratio, width=20, color="green"):
    ratio = max(0.0, min(1.0, ratio))
    filled = round(ratio * width)
    return c(SYM["full"] * filled, color) + c(SYM["empty"] * (width - filled), "gray")


# ------------------------------------------------------------------ badge
_STATUS_COLORS = {
    "PENDING": "yellow", "COMPLETED": "green", "REJECTED": "red",
    "REQUEST": "cyan", "ORDER": "green", "PRODUCT": "magenta", "ACCOUNT": "blue", "STORE": "yellow",
    "Active": "green", "Inactive": "red",
}
_TIER_COLORS = {"Bronze": "yellow", "Silver": "cyan", "Gold": "bright_yellow", "Platinum": "magenta"}


def badge(text, color="white"):
    return c(f"{SYM['dot']} {text}", "bold", color)


def status_badge(status):
    return badge(status, _STATUS_COLORS.get(status, "white"))


def tier_badge(tier):
    return c(tier, "bold", _TIER_COLORS.get(tier, "white"))


def stock_badge(stock, low=3):
    if stock <= 0:
        return c("OUT", "bold", "red")
    if stock <= low:
        return c(f"{stock} LOW", "bold", "yellow")
    return c(str(stock), "green")


# ------------------------------------------------------------------ pesan
def ok(message):
    print(f"  {c(SYM['ok'], 'bold', 'green')} {message}")


def err(message):
    print(f"  {c(SYM['err'], 'bold', 'red')} {c(message, 'red')}")


def warn(message):
    print(f"  {c(SYM['warn'], 'bold', 'yellow')} {c(message, 'yellow')}")


def info(message):
    print(f"  {c(SYM['info'], 'bold', 'cyan')} {message}")


def hint(message):
    print(c(f"  {message}", "dim"))


# ------------------------------------------------------------------ kotak
def banner(title, subtitle="", color="cyan"):
    """Banner besar (menu utama / login)."""
    inner = W - 2

    def row(text=""):
        return c(DOUBLE["v"], color) + pad(text, inner, "center") + c(DOUBLE["v"], color)

    print(c(DOUBLE["tl"] + DOUBLE["h"] * inner + DOUBLE["tr"], color))
    print(row())
    print(row(c(title, "bold")))
    if subtitle:
        print(row(c(subtitle, "dim")))
    print(row())
    print(c(DOUBLE["bl"] + DOUBLE["h"] * inner + DOUBLE["br"], color))


def screen(title, crumb=""):
    """Kepala layar standar: breadcrumb (redup) + judul."""
    if crumb:
        print(c(f"  {crumb}", "dim"))
    print(c(f"  {SYM['bar']} ", "bold", "cyan") + c(title.upper(), "bold"))
    print(c("  " + SINGLE["h"] * (W - 4), "gray"))


def section(title, color="cyan"):
    print()
    print(c(f"  {SYM['bar']} ", "bold", color) + c(title, "bold"))


def panel(title, lines, color="blue", width=W):
    """Kotak berjudul berisi beberapa baris teks."""
    inner = width - 2
    head = f" {title} " if title else ""
    rest = SINGLE["h"] * max(0, inner - 1 - vlen(head))
    print(c(SINGLE["tl"] + SINGLE["h"], color) + c(head, "bold", color) + c(rest + SINGLE["tr"], color))
    for line in lines:
        print(c(SINGLE["v"], color) + " " + pad(trunc(line, inner - 2), inner - 2) + " " + c(SINGLE["v"], color))
    print(c(SINGLE["bl"] + SINGLE["h"] * inner + SINGLE["br"], color))


def kv_lines(pairs, key_width=None):
    key_width = key_width or max((vlen(k) for k, _ in pairs), default=0)
    return [c(pad(k, key_width), "dim") + "  " + str(v) for k, v in pairs]


def kv(pairs, key_width=None, indent=2):
    for line in kv_lines(pairs, key_width):
        print(" " * indent + line)


def table(headers, rows, aligns=None, title=None, color="blue", empty="Nothing to show."):
    """Tabel dengan garis kotak. Sel boleh berisi kode warna."""
    if title:
        section(title, color)
    if not rows:
        print(c(f"  {empty}", "dim"))
        return
    n = len(headers)
    aligns = aligns or ["l"] * n
    rows = [[str(cell) for cell in row] for row in rows]
    widths = [max(vlen(headers[i]), *(vlen(r[i]) for r in rows)) for i in range(n)]
    total = sum(widths) + 3 * n + 1
    while total > W - 2:                       # kecilkan kolom terlebar bila kelebihan
        # utamakan memangkas kolom teks (rata kiri); kolom angka/uang dijaga utuh
        pool = [k for k in range(n) if aligns[k] == "l" and widths[k] > 8] or list(range(n))
        j = max(pool, key=lambda k: widths[k])
        if widths[j] <= 6:
            break
        widths[j] -= 1
        total -= 1

    def line(left, mid, right):
        return c("  " + left + mid.join(SINGLE["h"] * (w + 2) for w in widths) + right, "gray")

    def row(cells, header=False):
        parts = []
        for i, cell in enumerate(cells):
            text = trunc(cell, widths[i])
            if header:
                text = c(text, "bold", color)
            parts.append(" " + pad(text, widths[i], {"l": "left", "r": "right", "c": "center"}[aligns[i]]) + " ")
        bar = c(SINGLE["v"], "gray")
        return "  " + bar + bar.join(parts) + bar

    print(line(SINGLE["tl"], SINGLE["tt"], SINGLE["tr"]))
    print(row(headers, header=True))
    print(line(SINGLE["lt"], SINGLE["x"], SINGLE["rt"]))
    for r in rows:
        print(row(r))
    print(line(SINGLE["bl"], SINGLE["bt"], SINGLE["br"]))


def stat_cards(cards):
    """Baris kartu statistik. cards = [(label, value, color), ...]."""
    n = len(cards)
    gap = 1
    width = (W - 2 - gap * (n - 1)) // n
    top, mid1, mid2, bot = [], [], [], []
    for label, value, color in cards:
        inner = width - 2
        top.append(c(SINGLE["tl"] + SINGLE["h"] * inner + SINGLE["tr"], "gray"))
        mid1.append(c(SINGLE["v"], "gray") + pad(c(label, "dim"), inner, "center") + c(SINGLE["v"], "gray"))
        mid2.append(c(SINGLE["v"], "gray") + pad(c(value, "bold", color), inner, "center") + c(SINGLE["v"], "gray"))
        bot.append(c(SINGLE["bl"] + SINGLE["h"] * inner + SINGLE["br"], "gray"))
    for part in (top, mid1, mid2, bot):
        print("  " + (" " * gap).join(part))


def menu(items, title="MENU", back="Logout", color="cyan"):
    """Menu bernomor. items = [(label, catatan_kanan), ...]; 0 selalu untuk kembali."""
    content = W - 4
    lines = []
    for i, (label, note) in enumerate(items, 1):
        left = f"{c(f'{i:>2}', 'bold', color)}  {label}"
        if note:
            left += " " * max(1, content - vlen(left) - vlen(note)) + note
        lines.append(left)
    lines.append(c(" 0", "bold", "red") + "  " + c(back, "dim"))
    panel(title, lines, color)


def feed(items, empty="Nothing to show."):
    """Daftar kronologis 2 baris per entri. items = [(waktu, badge, kanan, teks, meta), ...]."""
    import textwrap
    if not items:
        print(c(f"  {empty}", "dim"))
        return
    for when, badge_text, right, text, meta in items:
        head = f"  {c(when, 'dim')}  {badge_text}"
        if right:
            gap = max(2, W - 2 - vlen(head) - vlen(right))
            head += " " * gap + c(right, "bold", "green")
        print(head)
        for line in textwrap.wrap(text, W - 8) or [""]:
            print(f"      {line}")
        if meta:
            print(f"      {c(meta, 'gray')}")
