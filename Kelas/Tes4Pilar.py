import random
from abc import ABC, abstractmethod


# =========================================================
# ABSTRACTION
# =========================================================
# Character adalah class abstrak.
# Character tidak dibuat langsung sebagai object.
class Character(ABC):

    def __init__(self, name, hp, mp, atk, df, pnt, spd, crit, alive=True):
        self.name = name
        self.__hp = hp
        self.__mp = mp
        self.__atk = atk
        self.__df = df
        self.__pnt = pnt
        self.__spd = spd
        self.__crit = crit
        self.__alive = alive

    # =====================================================
    # ENCAPSULATION
    # =====================================================
    # Getter dan setter digunakan untuk mengontrol
    # akses terhadap atribut private.

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, value):
        self.__hp = max(0, value)

        if self.__hp <= 0:
            self.__alive = False

    @property
    def mp(self):
        return self.__mp

    @mp.setter
    def mp(self, value):
        self.__mp = max(0, value)

    @property
    def atk(self):
        return self.__atk

    @property
    def df(self):
        return self.__df

    @property
    def pnt(self):
        return self.__pnt

    @property
    def spd(self):
        return self.__spd

    @property
    def crit(self):
        return self.__crit

    @property
    def alive(self):
        return self.__alive

    # =====================================================
    # METHOD
    # =====================================================

    def serang(self, enemy):

        if not self.alive:
            print(f"{self.name} sudah kalah!")
            return

        if not enemy.alive:
            print(f"{enemy.name} sudah kalah!")
            return

        # Perhitungan damage
        dmg = self.atk - (enemy.df - self.pnt)

        if dmg < 0:
            dmg = 0

        # Dodge berdasarkan speed
        if self.spd <= enemy.spd:

            dodge = random.randint(
                self.spd,
                enemy.spd + random.randint(1, 5)
            )

            yourhit = random.randint(
                self.spd,
                enemy.spd + random.randint(1, 5)
            )

            if dodge == yourhit:
                print(f"{self.name} menyerang {enemy.name} -> MISS!")
                return

        # Critical hit
        crit_chance = random.randint(
            1,
            max(1, 10 - self.crit)
        )

        your_crit = random.randint(
            1,
            max(1, 10 - self.crit)
        )

        if crit_chance == your_crit:
            dmg *= 2
            print("CRITICAL HIT!")

        enemy.hp -= dmg

        print(
            f"{self.name} menyerang {enemy.name}"
            f" dengan damage {dmg}"
        )

        print(
            f"HP {enemy.name}: "
            f"{enemy.hp}"
        )

        if not enemy.alive:
            print(f"{enemy.name} telah dikalahkan!")

    # =====================================================
    # ABSTRACT METHOD
    # =====================================================
    # Setiap turunan Character wajib memiliki show_info()
    @abstractmethod
    def show_info(self):
        pass


# =========================================================
# INHERITANCE
# =========================================================
# Hero mewarisi Character
class Hero(Character):

    def __init__(
        self,
        name,
        hp,
        mp,
        atk,
        df,
        pnt,
        spd,
        crit,
        lv,
        exp
    ):

        super().__init__(
            name,
            hp,
            mp,
            atk,
            df,
            pnt,
            spd,
            crit
        )

        self.lv = lv
        self.exp = exp

    # =====================================================
    # POLYMORPHISM
    # =====================================================
    # Hero memiliki implementasi show_info sendiri.
    def show_info(self):

        print("\n===== HERO INFO =====")

        print(f"Name  : {self.name}")
        print(f"Level : {self.lv}")
        print(f"EXP   : {self.exp}")
        print(f"HP    : {self.hp}")
        print(f"MP    : {self.mp}")
        print(f"ATK   : {self.atk}")
        print(f"DEF   : {self.df}")
        print(f"PNT   : {self.pnt}")
        print(f"SPD   : {self.spd}")
        print(f"CRIT  : {self.crit}")
        print(f"Alive : {self.alive}")


# =========================================================
# INHERITANCE
# =========================================================
# Monster juga mewarisi Character
class Monster(Character):

    def __init__(
        self,
        name,
        hp,
        mp,
        atk,
        df,
        pnt,
        spd,
        crit,
        expPoint
    ):

        super().__init__(
            name,
            hp,
            mp,
            atk,
            df,
            pnt,
            spd,
            crit
        )

        self.expPoint = expPoint

    # =====================================================
    # POLYMORPHISM
    # =====================================================
    # Monster memiliki implementasi show_info sendiri.
    def show_info(self):

        print("\n===== MONSTER INFO =====")

        print(f"Name       : {self.name}")
        print(f"HP         : {self.hp}")
        print(f"MP         : {self.mp}")
        print(f"ATK        : {self.atk}")
        print(f"DEF        : {self.df}")
        print(f"PNT        : {self.pnt}")
        print(f"SPD        : {self.spd}")
        print(f"CRIT       : {self.crit}")
        print(f"EXP Point  : {self.expPoint}")
        print(f"Alive      : {self.alive}")


# =========================================================
# OBJECT
# =========================================================

odet = Hero(
    "Odette",
    500,      # HP
    100,      # MP
    100,      # ATK
    15,       # DEF
    5,        # PNT
    15,       # SPD
    5,        # CRIT
    1,        # Level
    0         # EXP
)

lord = Hero(
    "Lord",
    1000,      # HP
    0,        # MP
    150,      # ATK
    50,       # DEF
    0,        # PNT
    2,        # SPD
    3,        # CRIT
    100,      # Level
    0         # EXP
)

goblin = Monster(
    "Goblin",
    300,
    50,
    80,
    10,
    3,
    10,
    4,
    100
)


# =========================================================
# PROGRAM
# =========================================================

odet.show_info()
goblin.show_info()

print("\n===== BATTLE =====")

odet.serang(goblin)

print("\n===== STATUS SETELAH SERANGAN =====")

odet.show_info()
goblin.show_info()

odet.serang(lord)
lord.serang(odet)
odet.serang(lord)
lord.serang(odet)
odet.serang(lord)
lord.serang(odet)
odet.serang(lord)
lord.serang(odet)
odet.serang(lord)
lord.serang(odet)