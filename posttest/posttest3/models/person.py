from abc import ABC, abstractmethod


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

    # ---------- Properti dengan validasi ----------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or value.strip() == "":
            raise ValueError("Name cannot be empty!")
        self._name = value.strip()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        value = (value or "").strip()
        if len(value) < 3 or " " in value:
            raise ValueError("Username must be at least 3 characters and contain no spaces!")
        self._username = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        value = (value or "").strip()
        if not value.isdigit() or not 10 <= len(value) <= 13:
            raise ValueError("Phone must be 10-13 digits!")
        self._phone = value

    @property
    def gmail(self):
        return self.__gmail

    @gmail.setter
    def gmail(self, value):
        value = (value or "").strip().lower()
        if " " in value or "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email format! Example: user@gmail.com")
        self.__gmail = value

    # ---------- Akun ----------
    def set_password(self, new_password):
        if not new_password or len(new_password) < 6:
            raise ValueError("Password must be at least 6 characters!")
        self.__password = new_password

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

    def show_person_info(self):
        print(f"Role                  : {self.get_role()}")
        print(f"Name                  : {self._name}")
        print(f"Username              : {self._username}")
        print(f"Password              : {'*' * 8}")
        print(f"Phone                 : {self._phone}")
        print(f"Email                 : {self.__gmail}")
        print(f"Birth Date            : {self.birth_date or '-'}")
        print(f"Gender                : {self.gender or '-'}")
        print(f"Status                : {'Active' if self.is_active else 'Inactive'}")

    def __str__(self):
        return f"{self._name} ({self.get_role()})"
