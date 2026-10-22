from abc import ABC, abstractmethod

from utils import ui


class Person(ABC):
    """Abstract base class untuk semua pengguna sistem (Customer, Admin, SuperAdmin).

    Subclass wajib menentukan role, hak akses (permission), dan notifikasi
    mana yang boleh dilihatnya. Data akun & profil dikelola di sini sekali saja.
    """

    total_people = 0

    def __init__(self, name, username, password, phone, gmail, birth_date="", gender=""):
        self._name = ""                 # Protected
        self._username = ""             # Protected
        self._phone = ""                # Protected
        self.__password = ""            # Private
        self.__gmail = ""               # Private
        self.name = name
        self.username = username
        self.set_password(password)
        self.phone = phone
        self.gmail = gmail
        self.birth_date = birth_date
        self.gender = gender
        self.is_active = True
        Person.total_people += 1

    # ---------- Abstract methods ----------
    @abstractmethod
    def get_role(self):
        """Nama role pengguna."""

    @abstractmethod
    def get_permissions(self):
        """Kumpulan kunci aksi yang boleh dilakukan role ini."""

    @abstractmethod
    def can_see(self, notification):
        """True jika notifikasi tersebut boleh dilihat pengguna ini."""

    # ---------- Validator (dipakai setter DAN form di menu agar aturannya satu) ----------
    @staticmethod
    def check_name(value):
        if not value or value.strip() == "":
            raise ValueError("Name cannot be empty!")
        return value.strip()

    @staticmethod
    def check_username(value):
        value = (value or "").strip()
        if len(value) < 3 or " " in value:
            raise ValueError("Username must be at least 3 characters with no spaces!")
        return value

    @staticmethod
    def check_phone(value):
        value = (value or "").strip()
        if not value.isdigit() or not 10 <= len(value) <= 13:
            raise ValueError("Phone must be 10-13 digits (numbers only)!")
        return value

    @staticmethod
    def check_gmail(value):
        value = (value or "").strip().lower()
        if " " in value or "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email format! Example: user@gmail.com")
        return value

    @staticmethod
    def check_password(value):
        if not value or len(value) < 6:
            raise ValueError("Password must be at least 6 characters!")
        return value

    # ---------- Properti dengan validasi ----------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = Person.check_name(value)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = Person.check_username(value)

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = Person.check_phone(value)

    @property
    def gmail(self):
        return self.__gmail

    @gmail.setter
    def gmail(self, value):
        self.__gmail = Person.check_gmail(value)

    # ---------- Akun ----------
    def set_password(self, new_password):
        self.__password = Person.check_password(new_password)

    def verify_password(self, password):
        return self.__password == password

    def change_password(self, old_password, new_password):
        if not self.verify_password(old_password):
            raise ValueError("The old password is wrong!")
        self.set_password(new_password)

    # ---------- Profil ----------
    def update_profile(self, name=None, phone=None, gmail=None, birth_date=None, gender=None):
        if name is not None:
            self.name = name
        if phone is not None:
            self.phone = phone
        if gmail is not None:
            self.gmail = gmail
        if birth_date is not None:
            self.birth_date = birth_date
        if gender is not None:
            self.gender = gender

    def info_pairs(self):
        """Pasangan (label, nilai) untuk kartu profil. Di-override subclass (polimorfisme)."""
        return [
            ("Role", ui.c(self.get_role(), "bold")),
            ("Name", self._name),
            ("Username", self._username),
            ("Password", "********"),
            ("Phone", self._phone),
            ("Email", self.__gmail),
            ("Birth date", self.birth_date or "-"),
            ("Gender", self.gender or "-"),
            ("Status", ui.status_badge("Active" if self.is_active else "Inactive")),
        ]

    def show_person_info(self):
        ui.panel("PROFILE", ui.kv_lines(self.info_pairs(), 12), "cyan")

    def __str__(self):
        return f"{self._name} ({self.get_role()})"
