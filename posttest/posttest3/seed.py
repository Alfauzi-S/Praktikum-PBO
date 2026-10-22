import contextlib
import io

from models.store import Store
from models.product import Product
from models.admin import SuperAdmin
from models.app_data import AppData
from models.order_service import OrderService
from models.payment import CashPayment, BankTransferPayment, EWalletPayment


def build_app():
    """Membuat data awal lewat alur yang sama dengan aplikasi (output dibungkam)."""
    store = Store("Alfauzi Computer Store", "Perangkat & aksesori komputer terpercaya",
                  "0541123456", "info@alfauzi.com")
    app = AppData(store)
    app.service = OrderService(app)

    with contextlib.redirect_stdout(io.StringIO()):
        smr = store.add_branch("Samarinda", "Jl. Pahlawan No. 1, Samarinda", "0541111111")
        bpn = store.add_branch("Balikpapan", "Jl. Jend. Sudirman No. 8, Balikpapan", "0542222222")

        for branch, stock_bonus in ((smr, 0), (bpn, -3)):
            branch.add_product(Product("P001", "Mechanical Keyboard", 750000, 10 + stock_bonus, "Peripheral"))
            branch.add_product(Product("P002", "Gaming Mouse", 350000, 15 + stock_bonus, "Peripheral"))
            branch.add_product(Product("P003", "Monitor 24 inch", 2500000, 5 + stock_bonus, "Monitor"))
        smr.add_product(Product("P004", "Laptop Office 14 inch", 7500000, 4, "Laptop"))

        boss = SuperAdmin("EMP000", "Super Admin", "superadmin", "super123",
                          "081100000000", "super@alfauzi.com")
        app.add_user(boss)
        admin_smr = app.register_admin("Budi Santoso", "admin_smr", "admin123", "081234567890",
                                       "budi@gmail.com", smr, "1998-05-10", "Male")
        admin_bpn = app.register_admin("Siti Aminah", "admin_bpn", "admin123", "081345678901",
                                       "siti@gmail.com", bpn, "1999-08-15", "Female")

        rina = app.register_customer("Rina Marlina", "rina_m", "password1", "085678901234",
                                     "rina@yahoo.com", "Jl. Pahlawan No. 10", "1999-05-12", "Female")
        daffa = app.register_customer("Daffa Pratama", "daffa_p", "password2", "085789012345",
                                      "daffa@gmail.com", "Jl. Ahmad Yani No. 5", "2000-08-20", "Male")
        nadia = app.register_customer("Nadia Putri", "nadia_putri", "password3", "085890123456",
                                      "nadia@outlook.com", "Jl. Diponegoro No. 88", "2001-01-15", "Female")

        svc = app.service
        # Riwayat awal: request -> diproses admin -> pesanan tercatat
        req1 = svc.submit_request(rina, smr, [(smr.get_product("P001"), 1), (smr.get_product("P002"), 2)])
        svc.fulfill_request(req1, admin_smr, CashPayment(rina.name, 2_500_000))
        req2 = svc.submit_request(daffa, bpn, [(bpn.get_product("P003"), 1)])
        svc.fulfill_request(req2, admin_bpn, BankTransferPayment(daffa.name, "BCA", "1234567890"))
        # Satu request yang masih menunggu admin (demo notifikasi)
        svc.submit_request(nadia, smr, [(smr.get_product("P004"), 1)], "Tolong siapkan hari ini")
    return app
