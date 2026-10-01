class Hero():
    def __init__(self,name, health, attack, armor, mana=50):
        self.name = name
        self._health = health
        self.attack = attack 
        self.mana = mana
        self.armor = armor
    
    def __str__(self):
        return f'nama hero {self.name}'
    
    def diserang(self, jumlah):
        self._health = max(self._health - jumlah, 0)
        
    def serang(self, target):
        damage = max(self.attack - target.armor, 0)
        target.diserang(damage)
        print(f'{self.name} menyerang {target.name}, damage {damage}')
        
    @property
    def health(self):
        return self._health
        
class Archer(Hero):
    def __init__(self,name, health, attack, armor, mana=50, misschange=50):
        super().__init__(name, health, attack, armor, mana=50)
        self.misschange = misschange
    

    def serang(self, target):
        super().serang(target)
        print(f'menyerang mengunakan panah')
        # print(f'{self.name} menyerang menggunakan panah {target.name}, damage {damage}')
        

class Warrior(Hero):
    pass


class Mage(Hero):
    pass


class EnergiArcher(Archer):
    def __init__(self,name, health, attack, armor, mana=50, misschange=50, energi=100):
        super().__init__(name, health, attack, armor, mana, misschange)
        self.energi = energi
        
    def serang(self, target):
        if self.energi > 20:
            self.energi -= 20
            damage = max(self.attack * 2 - target.armor, 0)
            target.diserang(damage)
            print(f'{self.name} menyerang menggunakan panah {target.name}, damage {damage}, sisa energi {self.energi}')
        else:
            print('Energi Habis gada bonus atack')
            super().serang(target)


class Healing():
    def heal (self, jumlah):
        self._health += jumlah
        print(f'{self.name} melakukan helaing {jumlah}')
        
        
class Support(Archer, Healing):
    pass

roger = Hero('Roger', 100, 20, 10)
Axe = Mage('Axe', 100, 59, 19)
Renger = Archer('Renger', 100, 59, 50, 19)
Kimmy = EnergiArcher('Renger', 100, 59, 50, 19, 100)
nana =  Support('nana', 100, 59, 50, 19)

for _ in range (5):
    Kimmy.serang(roger)

nana.serang(Kimmy)
nana.heal(100)

# roger.serang(Renger)
# Renger.serang(roger)
# roger.diserang(100)

# print(roger.__dict__)
# print(Axe.__dict__)
# print(isinstance(Axe, Warrior))