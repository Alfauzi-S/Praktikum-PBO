class Person:
    total_people = 0

    def __init__(self, name, username, password, birth_date="", gender=""):
        self._name = name
        self.__password = password
        self.username = username
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

    def change_password(self, old_password, new_password):
        if self.__password == old_password:
            self.password = new_password
            print(f"[V] Password for {self.username} has been changed successfully.")
        else:
            print("[!] The old password is wrong!")

    def show_person_info(self):
        print(f"Name       : {self._name}")
        print(f"Username   : {self.username}")
        print(f"Password   : {'*' * len(self.__password)}")
        print(f"Birth Date : {self.birth_date}")
        print(f"Gender     : {self.gender}")