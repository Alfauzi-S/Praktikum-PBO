from models.customer import Customer
from models.admin import Admin
from models.notification import Notification
from models.activity_log import ActivityLog


class AppData:
    """Penyimpanan data aplikasi (in-memory): toko, akun, request, pesanan, notifikasi, log."""

    def __init__(self, store):
        self.store = store                  # Asosiasi: AppData -> Store
        self.users = []
        self.requests = []
        self.sales = []
        self.notifications = []
        self.log = ActivityLog()
        self._counters = {}

    def next_id(self, prefix, width=3):
        self._counters[prefix] = self._counters.get(prefix, 0) + 1
        return f"{prefix}{self._counters[prefix]:0{width}d}"

    # ---------- Akun ----------
    @property
    def customers(self):
        return [u for u in self.users if isinstance(u, Customer)]

    @property
    def admins(self):
        return [u for u in self.users if isinstance(u, Admin)]     # termasuk SuperAdmin

    def find_user(self, username):
        return next((u for u in self.users if u.username.lower() == username.lower()), None)

    def username_available(self, username, ignore=None):
        other = self.find_user(username)
        return other is None or other is ignore

    def authenticate(self, username, password):
        user = self.find_user(username)
        if user and user.verify_password(password):
            return user
        return None

    def register_customer(self, name, username, password, phone, gmail, address,
                          birth_date="", gender="", actor="System"):
        if not self.username_available(username):
            raise ValueError(f"Username '{username}' is already taken!")
        customer = Customer(self.next_id("C"), name, username, password, phone, gmail,
                            address, birth_date, gender)
        self.users.append(customer)
        self.log.add(ActivityLog.ACCOUNT, actor, f"Customer registered: {customer.name} ({customer.id_customer})")
        return customer

    def register_admin(self, name, username, password, phone, gmail, branch,
                       birth_date="", gender="", actor="System"):
        if not self.username_available(username):
            raise ValueError(f"Username '{username}' is already taken!")
        admin = Admin(self.next_id("EMP"), name, username, password, phone, gmail,
                      None, birth_date, gender)
        branch.add_admin(admin)
        self.users.append(admin)
        self.log.add(ActivityLog.ACCOUNT, actor, f"Admin created: {admin.name} ({admin.employee_id})", branch)
        return admin

    def add_user(self, user):
        self.users.append(user)

    # ---------- Notifikasi ----------
    def notify(self, message, branch=None, customer=None, request=None):
        notif = Notification(self.next_id("N"), message, branch, customer, request)
        self.notifications.append(notif)
        return notif

    def inbox(self, user):
        return [n for n in reversed(self.notifications) if user.can_see(n)]

    def unread_count(self, user):
        return sum(1 for n in self.inbox(user) if not n.is_read)

    def pending_requests(self, branches):
        return [r for r in self.requests if r.status == r.PENDING and r.branch in branches]
