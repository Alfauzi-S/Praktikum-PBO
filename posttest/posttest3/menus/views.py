"""Potongan tampilan yang dipakai banyak menu (tabel produk, request, pesanan, dll)."""
from models.sale import Sale
from utils import ui, choose


def choose_branch(branches, title="Choose a branch"):
    return choose(branches, title=title, headers=["Branch", "Address", "Products"],
                  row=lambda b: [ui.c(b.name, "bold"), b.address, str(len(b))], aligns=["l", "l", "r"])


def product_table(products, title=None, cart=None, numbered=False):
    """Tabel produk. cart = daftar [product, qty] untuk menampilkan kolom 'In cart'."""
    headers = ["ID", "Product", "Category", "Price", "Stock"]
    aligns = ["l", "l", "l", "r", "r"]
    in_cart = {id(p): q for p, q in (cart or [])}
    if cart is not None:
        headers.append("In cart")
        aligns.append("r")
    rows = []
    for i, p in enumerate(products, 1):
        row = [p.id_product, p.name, p.category, ui.rupiah(p.price), ui.stock_badge(p.stock)]
        if cart is not None:
            row.append(ui.c(str(in_cart[id(p)]), "bold", "cyan") if id(p) in in_cart else ui.c("-", "gray"))
        rows.append([str(i)] + row if numbered else row)
    if numbered:
        headers, aligns = ["#"] + headers, ["r"] + aligns
    ui.table(headers, rows, aligns, title=title, empty="No products match.")


def price_breakdown(subtotal, discount_percentage, title="PRICE"):
    est = Sale.estimate(subtotal, discount_percentage)

    def money(label, value, style=None):
        text = ui.rupiah(value)
        gap = " " * max(1, ui.W - 6 - ui.vlen(label) - ui.vlen(text))
        return label + gap + (ui.c(text, *style) if style else text)

    lines = [money("Subtotal", est["subtotal"])]
    if discount_percentage:
        lines.append(money(f"Member discount {discount_percentage}%", -est["discount"], ("green",)))
    lines.append(money(f"Tax {Sale.tax}%", est["tax"]))
    lines.append(money(ui.c("TOTAL", "bold"), est["total"], ("bold", "green")))
    ui.panel(title, lines, "green")
    return est


def request_rows(request):
    return [ui.c(request.id_request, "bold"), request.customer.name,
            ui.rupiah(request.estimated_total), ui.status_badge(request.status), ui.time_ago(request.created_at)]


REQUEST_HEADERS = ["Request", "Customer", "Est. total", "Status", "Created"]
REQUEST_ALIGNS = ["l", "l", "r", "l", "l"]


def sale_rows(sale):
    return [ui.c(sale.id_sale, "bold"), sale.customer.name,
            ui.rupiah(sale.total), sale.payment.method_name if sale.payment else "-",
            f"{sale.created_at:%d %b %H:%M}"]


SALE_HEADERS = ["Order", "Customer", "Total", "Paid via", "Date"]
SALE_ALIGNS = ["l", "l", "r", "l", "l"]


def my_request_rows(request):
    """Versi ringkas untuk pelanggan (tanpa kolom nama sendiri)."""
    return [ui.c(request.id_request, "bold"), request.branch.name, str(len(request)),
            ui.rupiah(request.estimated_total), ui.status_badge(request.status), ui.time_ago(request.created_at)]


MY_REQUEST_HEADERS = ["Request", "Branch", "Items", "Est. total", "Status", "Created"]
MY_REQUEST_ALIGNS = ["l", "l", "r", "r", "l", "l"]
