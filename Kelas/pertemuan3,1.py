class Shop:
    def __init__(self, name):
        self.name = name

    def proses_pembelian(self, hero, item):
        if hero.gold >= item.harga:
            hero.gold -= item.harga

            print(
                f"{self.name} membeli {item.name} "
                f"dengan harga {item.harga} gold, "
                f"sisa gold {hero.gold}"
            )

            return True

        print(
            f"Gold {hero.name} tidak cukup "
            f"untuk membeli {item.name}"
        )

        return False


class Item:
    def __init__(self, name, harga, bonus_attack=0, bonus_armor=0):
        self.name = name
        self.harga = harga
        self.bonus_attack = bonus_attack
        self.bonus_armor = bonus_armor

    def __str__(self):
        return (
            f"Item: {self.name} | "
            f"+{self.bonus_attack} Attack | "
            f"+{self.bonus_armor} Armor"
        )


class Skill:
    def __init__(self, name, damage, mana_cost):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost

    def __str__(self):
        return (
            f"{self.name} | "
            f"{self.damage} Damage | "
            f"{self.mana_cost} Mana"
        )


class Hero:
    jumlahHero = 0
    MAKS_SLOT = 4

    def __init__(
        self,
        name,
        health,
        mana,
        armor,
        attack,
        gold,
        list_skill
    ):
        Hero.jumlahHero += 1

        self.name = name
        self.health = health
        self.mana = mana
        self.armor = armor
        self.attack = attack
        self.gold = gold

        # Aggregation
        self._inventory = []

        # Composition
        self._skills = [
            Skill(name, dmg, mana)
            for name, dmg, mana in list_skill
        ]

    # Association
    def beli_item(self, shop, item):
        if len(self._inventory) >= Hero.MAKS_SLOT:
            print(f"Inventory {self.name} sudah penuh")
            return

        if shop.proses_pembelian(self, item):
            self._inventory.append(item)

            print(
                f"{item.name} berhasil ditambahkan "
                f"ke inventory {self.name}"
            )

    # Aggregation
    def ambil_item(self, item):
        if len(self._inventory) >= Hero.MAKS_SLOT:
            print(f"Inventory {self.name} sudah penuh")
            return

        self._inventory.append(item)

        print(
            f"+ {self.name} mengambil {item.name}"
        )

    # Composition
    def gunakan_skill(self, nomor_skill, lawan):
        skill = self._skills[nomor_skill - 1]
        if self.mana < skill.mana_cost:
            print(f"mana {self.name} tidak cukup untuk skill {skill.name}")
            return
        self.mana -= skill.mana_cost
        lawan.health -= skill.damage
        print(f"{self.name} memakai {skill.name} ke {lawan.name} sisa health {lawan.name}: {lawan.health}")

    def tampilkan_inventory(self):
        print(f"\nInventory {self.name}:")

        if not self._inventory:
            print("Inventory kosong.")
            return

        for item in self._inventory:
            print(f"- {item}")

    def tampilkan_skill(self):
        print(f"\nSkill {self.name}:")

        for skill in self._skills:
            print(f"- {skill}")


brodi = Hero(
    "Brodi",
    3000,
    10000,
    10,
    100,
    10000,
    [
        ("Tembak", 100, 10),
        ("Loncat", 10, 5)
    ]
)

alpa = Hero(
    "alpa",
    3000,
    10000,
    10,
    100,
    10000,
    [
        ("Tembak", 100, 10),
        ("Loncat", 10, 5)
    ]
)

shop = Shop("Belanja Item")

bod = Item(
    "BOD",
    3100,
    bonus_attack=160
)

winter = Item(
    "Winter",
    2140,
    bonus_attack=15,
    bonus_armor=45
)

# Association
brodi.beli_item(shop, bod)

# Aggregation
brodi.ambil_item(winter)

# Menampilkan inventory
brodi.tampilkan_inventory()

# Composition
brodi.tampilkan_skill()

brodi.gunakan_skill(1, alpa)
