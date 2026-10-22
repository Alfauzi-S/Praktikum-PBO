class Person:
    total_people = 0

    def __init__(self, name, username, password, phone, gmail, birth_date="", gender=""):
        self._name = name
        self.__password = password
        self.username = username
        self._phone = ""
        self.__gmail = ""
        self.phone = phone
        self.gmail = gmail
        self.birth_date = birth_date
        self.gender = gender
        Person.total_people += 1
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not new_name or new_name.strip() == "":
            raise ValueError("Name cannot be empty!")
        self._name = new_name

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password):
        if not new_password or new_password.strip() == "":
            raise ValueError("[!] Password cannot be empty!")
        if len(new_password) < 6:
            raise ValueError("[!] Password must be at least 6 characters!")
        self.__password = new_password

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, new_phone):
        if not new_phone or new_phone.strip() == "":
            raise ValueError("[!] Phone cannot be empty!")
        if len(new_phone) < 10 or len(new_phone) > 13:
            raise ValueError("[!] Invalid mobile number! Must be 10-13 digits.")
        if not new_phone.isdigit():
            raise ValueError("[!] Phone number must contain only digits!")
        self._phone = new_phone.strip()
        
    @property
    def gmail(self):
        return self.__gmail

    @gmail.setter
    def gmail(self, new_gmail):
        if not new_gmail or new_gmail.strip() == "":
            raise ValueError("[!] Gmail cannot be empty!")
        if "@" not in new_gmail or "." not in new_gmail.split("@")[-1]:
            raise ValueError("[!] Invalid gmail format! Example: user@gmail.com")
        if " " in new_gmail:
            raise ValueError("[!] Gmail cannot contain spaces!")
        self.__gmail = new_gmail.strip().lower()
    
    def change_phone(self, new_phone):
        self.phone = new_phone
        print(f"[V] Phone for {self.username} has been changed successfully.")
    
    def change_gmail(self, password, new_gmail):
        if self.__password == password:
            self.gmail = new_gmail
            print(f"[V] Gmail for {self.username} has been changed successfully.")
        else:
            print("[!] Wrong password!")

    def change_password(self, old_password, new_password):
        if self.__password == old_password:
            self.password = new_password
            print(f"[V] Password for {self.username} has been changed successfully.")
        else:
            print("[!] The old password is wrong!")

    def show_person_info(self):
        print(f"Name                  : {self._name}")
        print(f"Username              : {self.username}")
        print(f"Password              : {'*' * len(self.__password)}")
        print(f"Phone                 : {self._phone}")
        print(f"Gmail                 : {self.__gmail}")
        print(f"Birth Date            : {self.birth_date}")
        print(f"Gender                : {self.gender}")