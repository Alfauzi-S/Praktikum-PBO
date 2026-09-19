from models.person import Person


class Customer(Person):
    total_customers = 0
    customer_type = "Regular"
    application_name = "Computer Sales Management System"

    def __init__(self, id_customer, name, phone, address):
        super().__init__(name, phone)

        self.id_customer = id_customer
        self.address = address
        self.__status = "Active"

        Customer.total_customers += 1

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status):
        if new_status not in ["Active", "Inactive"]:
            raise ValueError("Status must be Active or Inactive!")
        else:
            self.__status = new_status

    def show_info(self):
        print(f"ID Customer : {self.id_customer}")
        print(f"Name        : {self.name}")
        print(f"Phone       : {self.phone}")
        print(f"Address     : {self.address}")
        print(f"Status      : {self.status}")

    def change_address(self, new_address):
        if new_address.strip() == "":
            print("Address cannot be empty!")
        else:
            self.address = new_address
            print("Address changed successfully!")

    @classmethod
    def change_customer_type(cls, new_type):
        if new_type.strip() == "":
            print("Customer type cannot be empty!")
        else:
            cls.customer_type = new_type
            print("Customer type changed successfully!")

    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and len(phone) >= 10