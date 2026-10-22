from datetime import datetime


class Notification:
    """Notifikasi dalam aplikasi. Untuk admin (branch) atau untuk customer."""

    def __init__(self, id_notif, message, branch=None, customer=None, request=None):
        self.id_notif = id_notif
        self.message = message
        self.branch = branch
        self.customer = customer
        self.request = request
        self.is_read = False
        self.created_at = datetime.now()

    def mark_read(self):
        self.is_read = True

    def __str__(self):
        mark = " " if self.is_read else "*"
        return f"{mark} [{self.created_at:%d-%m %H:%M}] {self.message}"
