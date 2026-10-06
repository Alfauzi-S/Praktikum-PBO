from abc import ABC, abstractmethod

class Hero(ABC):
    def __init__(self, name, health, attack, armor):
        self.name = name
        self.health = health
        self.attack = attack
        self.armor = armor
        
    @abstractmethod
    def ulti(self, target):
        pass
        
    def hitung_damage(self, target):
        return max(self.attack - target.armor, 0)
    
    def serang(self, targer):
        damage = self.hitung_damage(targer)
        self.health -= damage
        print(f"{self.name} menyerang {targer.name}, damage {damage}")
        
    def __add__(self, Healing):
        return self.health + Healing
    
    def __sub__(self, burn):
        darah = self.health
        for i in range(5):
            darah = self.health - burn
            print("darah :", darah)
            self.health = darah
        print(self.health)
            
        
class Mage(Hero):
    def ulti(self, target):
        print((self.attack * 88) - target.health)

    
    def hitung_damage(self, target):
        return self.attack # True Damage
    
class Warrior(Hero):
    def ulti(self, target):
        print((self.attack * 67) - target.health)
    
    def hitung_damage(self, target):
        return super().hitung_damage(target) + 10 # Bonus attack 10

class Minion:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

sora = Warrior("sora", 60, 100, 30)
eudora = Mage("eudora", 100, 60, 5)
minion = Minion("minipn", 50, 5)

# eudora.serang(minion)
# eudora.serang(sora)
# sora.serang(eudora)

# eudora.ulti(sora)
# sora.ulti(eudora)

print(eudora + 100)
print(eudora - 10)

print(isinstance(eudora, Mage))
print(isinstance(eudora, Warrior))
print(isinstance(eudora, Hero))
print(type(eudora))