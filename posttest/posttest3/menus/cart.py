"""Keranjang belanja satu layar: dipakai customer (Shop) dan admin (Create Order)."""
from menus.views import product_table, price_breakdown
from utils import ui, ask, ask_int, confirm, choose


def _find(products, text):
    if text.isdigit() and 1 <= int(text) <= len(products):
        return products[int(text) - 1]
    return next((p for p in products if p.id_product.lower() == text.lower()), None)


def _matches(product, keyword):
    keyword = keyword.lower()
    return keyword in product.name.lower() or keyword in product.category.lower() \
        or keyword in product.id_product.lower()


def _show_cart(cart, discount):
    if not cart:
        ui.hint("Your cart is empty. Type a product number or ID to add it.")
        return
    ui.table(["Item", "Qty", "Unit price", "Subtotal"],
             [[p.name, str(q), ui.rupiah(p.price), ui.rupiah(p.price * q)] for p, q in cart],
             ["l", "r", "r", "r"], title=f"Cart ({sum(q for _, q in cart)} item)", color="green")
    price_breakdown(sum(p.price * q for p, q in cart), discount, "ESTIMATED PRICE")


def build_cart(customer, branch, crumb="", who="Customer"):
    """Kembalikan daftar (product, qty), atau None jika dibatalkan."""
    cart = []                                   # [[product, qty], ...]
    keyword = ""
    notice = None                               # pesan hasil aksi sebelumnya, tampil di layar berikutnya
    while True:
        ui.screen(f"Shopping cart - {branch.name}", crumb)
        if notice:
            {"ok": ui.ok, "err": ui.err, "warn": ui.warn}[notice[0]](notice[1])
            print()
            notice = None
        shown = [p for p in branch.products if _matches(p, keyword)] if keyword else branch.products
        product_table(shown, title=f"Products{f'  (filter: {keyword})' if keyword else ''}",
                      cart=cart, numbered=True)
        _show_cart(cart, customer.discount_percentage)
        ui.hint("Number/ID = add   |   /word = search   |   R = remove   |   C = clear   |   "
                "S = send   |   Q = cancel")
        command = ask("Command").strip()
        lowered = command.lower()

        if lowered == "s":
            if cart:
                return [(p, q) for p, q in cart]
            notice = ("err", "Cart is empty. Add at least one product first.")
        elif lowered == "q":
            if not cart or confirm("Discard this cart?"):
                return None
        elif lowered == "c":
            if cart and confirm("Clear the whole cart?"):
                cart.clear()
                notice = ("ok", "Cart cleared.")
        elif lowered == "r":
            line = choose(cart, title="Remove which item?", headers=["Item", "Qty"],
                          row=lambda x: [x[0].name, str(x[1])], aligns=["l", "r"])
            if line:
                cart.remove(line)
                notice = ("ok", f"Removed {line[0].name}.")
        elif command.startswith("/"):
            keyword = command[1:].strip()
        elif command:
            product = _find(shown, command)
            if not product:
                notice = ("err", f"'{command}' not found. Use the # or ID from the table.")
            elif product.stock <= 0:
                notice = ("err", f"{product.name} is out of stock.")
            else:
                already = next((q for p, q in cart if p is product), 0)
                available = product.stock - already
                if available <= 0:
                    notice = ("warn", f"You already have all {product.stock} in stock in your cart.")
                else:
                    qty = ask_int(f"Quantity for {product.name} (max {available})", 1, default=1)
                    if qty is None:
                        continue
                    if qty > available:
                        notice = ("err", f"Only {available} more available.")
                    elif already:
                        next(line for line in cart if line[0] is product)[1] += qty
                        notice = ("ok", f"Cart updated: {product.name} x{already + qty}")
                    else:
                        cart.append([product, qty])
                        notice = ("ok", f"Added {product.name} x{qty}")
