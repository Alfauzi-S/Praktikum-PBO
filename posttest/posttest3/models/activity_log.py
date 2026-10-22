from datetime import datetime


class LogEntry:
    def __init__(self, kind, actor, message, branch=None, amount=0):
        self.kind = kind
        self.actor = actor
        self.message = message
        self.branch = branch
        self.amount = amount
        self.created_at = datetime.now()

    def __str__(self):
        amount = f" | Rp{self.amount:,.0f}" if self.amount else ""
        branch = f" | {self.branch.name}" if self.branch else ""
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {self.kind:<10} | {self.actor}{branch} | {self.message}{amount}"


class ActivityLog:
    """Catatan / history semua kejadian penting di sistem."""

    REQUEST = "REQUEST"
    ORDER = "ORDER"
    REJECTED = "REJECTED"
    PRODUCT = "PRODUCT"
    ACCOUNT = "ACCOUNT"
    STORE = "STORE"

    def __init__(self):
        self._entries = []

    def add(self, kind, actor, message, branch=None, amount=0):
        self._entries.append(LogEntry(kind, actor, message, branch, amount))

    def entries(self, branches=None, kinds=None):
        """branches=None -> semua; entri tanpa cabang selalu ikut jika branches None."""
        result = self._entries
        if branches is not None:
            result = [e for e in result if e.branch in branches]
        if kinds is not None:
            result = [e for e in result if e.kind in kinds]
        return list(reversed(result))

    def __len__(self):
        return len(self._entries)
