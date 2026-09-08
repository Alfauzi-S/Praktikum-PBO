class Product:
    def __init__(self, name, price, stock, category, brand):
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
        self.brand = brand

    def tambah_stok(self, jumlah):
        self.stock += jumlah

    def kurangi_stok(self, jumlah):
        if self.stock == jumlah:
            self.stock -= jumlah

    def ubah_harga(self, harga_baru):
        self.price = harga_baru

    def show_info(self):
        print(f"Name : {self.name}")
        print(f"Price : {self.price}")
        print(f"Stock : {self.stock}")
        print(f"Categoty : {self.category}")
        print(f"Brand : {self.brand}")

mouse = Product("Mouse", 300000, 15, "Aksesoris", "Logitech")
mouse.tambah_stok(5)
mouse.kurangi_stok(2)
mouse.ubah_harga(280000)
mouse.show_info()

class Hero:
    def __init__(self, name, atk, spd, df, hp):
        self.name = name
        self.atk = atk
        self.spd = spd
        self.df = df
        self.hp = hp

    # INSTANCE METHOD
    def show_info(self):
        print(f"Name : {self.name}")
        print(f"Atk  : {self.atk}")
        print(f"Spd  : {self.spd}")
        print(f"DF   : {self.df}")
        print(f"HP   : {self.hp}")

    # CLASS METHOD
    @classmethod
    def info_class(cls):
        print(f"Nama class : {cls.__name__}")

    # STATIC METHOD
    @staticmethod
    def total_stat(atk, spd, df, hp):
        return atk + spd + df + hp


# Membuat objek
Atlas = Hero("Atlas", 5, 10, 25, 150)

# Instance Method
Atlas.show_info()

# Class Method
Hero.info_class()

# Static Method
total = Hero.total_stat(5, 10, 25, 150)
print("Total Stat :", total)