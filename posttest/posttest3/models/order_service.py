from utils import ui
from models.sale import Sale
from models.order_request import OrderRequest
from models.activity_log import ActivityLog
from models.notifier import build_channels, notify_customer


class OrderService:
    """Alur belanja: customer request -> notifikasi admin -> admin buat pesanan
    & validasi pembayaran -> tercatat di log/history."""

    def __init__(self, app):
        self.app = app

    # 1. Customer memilih barang -> request + notifikasi ke admin cabang
    def submit_request(self, customer, branch, items, note=""):
        if not items:
            raise ValueError("Cannot submit an empty request!")
        request = OrderRequest(self.app.next_id("REQ"), customer, branch, note)
        for product, qty in items:
            request.add_item(product, qty)
        self.app.requests.append(request)
        self.app.notify(
            f"New request {request.id_request} from {customer.name} "
            f"({len(request)} item, est. {ui.rupiah(request.estimated_total)})",
            branch=branch, request=request)
        self.app.log.add(ActivityLog.REQUEST, customer.name,
                         f"Created request {request.id_request}", branch, request.estimated_total)
        return request

    # 2. Admin membuat pesanan dari request + validasi pembayaran
    def fulfill_request(self, request, admin, payment):
        if request.status != OrderRequest.PENDING:
            raise ValueError("This request has already been handled!")
        sale = self._build_sale(admin, request.customer, request.branch,
                                [(i.product, i.quantity) for i in request.items])
        if sale is None or not self._pay(sale, payment):
            return None
        request.mark_completed(sale, admin)
        self.app.notify(f"Your request {request.id_request} is completed as order {sale.id_sale}. "
                        f"Total {ui.rupiah(sale.total)}", customer=request.customer, request=request)
        return sale

    def reject_request(self, request, admin, reason):
        if request.status != OrderRequest.PENDING:
            raise ValueError("This request has already been handled!")
        request.mark_rejected(admin, reason or "No reason given")
        self.app.notify(f"Your request {request.id_request} was rejected: {request.reject_reason}",
                        customer=request.customer, request=request)
        self.app.log.add(ActivityLog.REJECTED, admin.name,
                         f"Rejected {request.id_request}: {request.reject_reason}", request.branch)

    # Pesanan langsung oleh admin (customer datang ke toko)
    def create_walkin_order(self, admin, customer, branch, items, payment):
        sale = self._build_sale(admin, customer, branch, items)
        if sale is None or not self._pay(sale, payment):
            return None
        self.app.notify(f"Order {sale.id_sale} created for you. Total {ui.rupiah(sale.total)}", customer=customer)
        return sale

    # ---------- internal ----------
    def _build_sale(self, admin, customer, branch, items):
        sale = Sale(self.app.next_id("TRX"), customer, branch, admin)
        for product, qty in items:
            if not sale.add_item(product, qty):
                sale.cancel()
                return None
        sale.set_discount(customer.discount_percentage)
        return sale

    def _pay(self, sale, payment):
        if not sale.checkout(payment):
            sale.cancel()                      # stok dikembalikan jika pembayaran gagal
            return False
        self.app.sales.append(sale)
        self.app.log.add(ActivityLog.ORDER, sale.handled_by.name,
                         f"Order {sale.id_sale} for {sale.customer.name} paid via {payment.method_name}",
                         sale.branch, sale.total)
        notify_customer(build_channels(sale.customer),
                        f"Payment for {sale.id_sale} ({ui.rupiah(sale.total)}) validated. Thank you!")
        return True
