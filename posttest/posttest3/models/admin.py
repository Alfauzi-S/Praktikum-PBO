from models.person import Person


class Admin(Person):
    """Admin cabang: membuat pesanan, mengelola produk & customer di cabangnya."""

    PERMISSIONS = frozenset({
        "notifications", "incoming_requests", "create_order", "manage_products",
        "manage_customers", "history", "profile",
    })

    def __init__(self, employee_id, name, username, password, phone, gmail,
                 branch=None, birth_date="", gender=""):
        super().__init__(name, username, password, phone, gmail, birth_date, gender)
        self.employee_id = employee_id
        self.branch = branch                    # Asosiasi: Admin -> Branch
        self._orders_processed = 0

    def get_role(self):
        return "Admin"

    def get_permissions(self):
        return Admin.PERMISSIONS

    def can_see(self, notification):
        return notification.branch is not None and notification.branch is self.branch

    def accessible_branches(self, store):
        """Admin biasa hanya boleh bekerja di cabangnya sendiri."""
        return [self.branch] if self.branch else []

    @property
    def orders_processed(self):
        return self._orders_processed

    def record_order(self):
        self._orders_processed += 1

    def show_person_info(self):
        super().show_person_info()
        print(f"Employee ID           : {self.employee_id}")
        print(f"Branch                : {self.branch.name if self.branch else '-'}")
        print(f"Orders Processed      : {self._orders_processed}")


class SuperAdmin(Admin):
    """Super admin: semua akses Admin + kelola admin, profil toko, dan cabang."""

    PERMISSIONS = Admin.PERMISSIONS | {"manage_admins", "store_profile", "manage_branches"}

    def get_role(self):
        return "Super Admin"

    def get_permissions(self):
        return SuperAdmin.PERMISSIONS

    def can_see(self, notification):
        return notification.branch is not None      # melihat notifikasi semua cabang

    def accessible_branches(self, store):
        return list(store.branches)                 # semua cabang
