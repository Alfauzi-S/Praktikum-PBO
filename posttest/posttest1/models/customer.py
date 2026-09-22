from models.person import Person


class Customer(Person):
    total_customers = 0
    store_branch = "Samarinda"
    application_name = "Computer Sales Management System"

    def __init__(self, id_customer, name, phone, address):
        super().__init__(name, phone)

        self.id_customer = id_customer
        self.address = address
        self.customer_type = "Regular"
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
        print(f"Branch      : {Customer.store_branch}")
        print(f"Type        : {self.customer_type}")
        print(f"Status      : {self.status}")

    def change_address(self, new_address):
        if new_address.strip() == "":
            print("Address cannot be empty!")
        else:
            self.address = new_address
            print("Address changed successfully!")

    def change_type(self, new_type):
        valid_types = ["Regular", "Premium", "VIP"]
        if new_type not in valid_types:
            raise ValueError(f"Type must be one of: {', '.join(valid_types)}")
        self.customer_type = new_type
        print(f"Customer type changed to {new_type} successfully!")

    @classmethod
    def change_store_branch(cls, new_branch):
        if new_branch.strip() == "":
            raise ValueError("Store branch cannot be empty!")
        cls.store_branch = new_branch
        print(f"Store branch changed to {new_branch} successfully!")
        
    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and len(phone) >= 10