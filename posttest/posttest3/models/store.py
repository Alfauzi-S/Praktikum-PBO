from models.branch import Branch


class Store:
    """Profil toko pusat. Cabang dibuat DI DALAM Store (komposisi)."""

    def __init__(self, name, tagline, phone, email):
        self.name = name
        self.tagline = tagline
        self.phone = phone
        self.email = email
        self._branches = []

    @property
    def branches(self):
        return list(self._branches)

    def update_profile(self, name=None, tagline=None, phone=None, email=None):
        if name is not None:
            if not name.strip():
                raise ValueError("Store name cannot be empty!")
            self.name = name.strip()
        if tagline is not None:
            self.tagline = tagline.strip()
        if phone is not None:
            self.phone = phone.strip()
        if email is not None:
            self.email = email.strip()

    def add_branch(self, name, address, phone):
        """Komposisi: objek Branch dibuat di dalam Store, tidak dari luar."""
        if not name or not name.strip():
            raise ValueError("Branch name cannot be empty!")
        if any(b.name.lower() == name.strip().lower() for b in self._branches):
            raise ValueError(f"Branch '{name}' already exists!")
        branch = Branch(f"B{len(self._branches) + 1:02d}", name.strip(), address.strip(), phone.strip())
        self._branches.append(branch)
        return branch

    def remove_branch(self, branch):
        if branch.admins:
            raise ValueError("Cannot remove a branch that still has admins. Reassign them first.")
        self._branches.remove(branch)

    def get_branch(self, branch_id):
        return next((b for b in self._branches if b.branch_id == branch_id), None)

    def __len__(self):
        return len(self._branches)

    def __str__(self):
        return f"{self.name} - {self.tagline}"
