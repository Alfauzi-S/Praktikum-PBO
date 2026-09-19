class Person:
    total_people = 0

    def __init__(self, name, phone):
        self.__name = name
        self.phone = phone

        Person.total_people += 1

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        if new_name.strip() == "":
            raise ValueError("Name cannot be empty!")
        else:
            self.__name = new_name

    def show_person_info(self):
        print(f"Name  : {self.name}")
        print(f"Phone : {self.phone}")