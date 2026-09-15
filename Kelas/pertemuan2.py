class Hero:
    jumlah_hero = 0 

    def __init__(self, name, health, attack, armor):
        self.__name = name      
        self.__health = health 
        self.attack = attack    
        self.__armor = armor  # Diubah ke private agar bisa sinkron dengan deleter
        Hero.jumlah_hero += 1

    # 1. Properti Name (Getter)
    @property
    def name(self):
        return self.__name

    # 2. Properti Health (Getter)
    @property
    def health(self):
        return self.__health

    # 3. Properti Health (Setter) - Mengontrol perubahan darah
    @health.setter
    def health(self, darahbaru) -> None:
        if darahbaru <= 0:
            self.__health = 0
            print(f"{self.name} has fallen!") # Memanggil properti 'name' di atas
        else:
            self.__health = darahbaru

    # 4. Properti Armor (Getter) - Wajib ada sebelum deleter
    @property
    def armor(self):
        return self.__armor
    
    # 5. Properti Armor (Deleter) - Menghapus armor
    @armor.deleter
    def armor(self):
        print(f"Warning: {self.name}'s armor has been completely destroyed!")
        del self.__armor

    # 6. Properti HeroPower (Getter Kalkulasi)
    @property
    def heroPower(self) -> int:
        # Menggunakan self.__armor karena variabel aslinya private
        return self.attack + self.__armor + self.__health

    # 7. Magic Method String Representation
    def __str__(self):
        return f"Attack Hero: {self.attack}"

# =========================================================
# CARA MEMANGGIL SETIAP BAGIAN
# =========================================================

# Pembuatan Objek
sniper = Hero("sniper", 100, 11, 5)

# --- 1. Cara Manggil Getter ---
print(sniper.name)       # Hasil: sniper (tanpa kurung)
print(sniper.health)     # Hasil: 100
print(sniper.heroPower)  # Hasil: 116 (11 + 5 + 100)

# --- 2. Cara Manggil Setter ---
sniper.health -= 50      # Mengurangi darah. Sekarang darah = 50
print(sniper.health)     # Hasil: 50

sniper.health -= 60      # Mengurangi darah sampai minus. 
                         # Otomatis mencetak: "sniper has fallen!"

# --- 3. Cara Manggil Magic Method ---
print(sniper)            # Otomatis memanggil __str__. Hasil: Attack Hero: 11
print(sniper.__dict__)   # Melihat isi objek mentah dalam bentuk dictionary

# --- 4. Cara Manggil Deleter ---
del sniper.armor         # Otomatis mencetak pesan warning armor hancur
