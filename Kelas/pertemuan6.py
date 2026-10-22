class Hero:
    def __init__(self, name, health):
        self.name = name
        self.health =health
        
    def serang(self, target):
        target.health -= 10
            
class TampilanHero:
    def tampilkan(self, hero):
        print(f"{hero.name} | {hero.health}")
        
class PenyimpanHero:
    def simpan(self, hero, nama_file):
        with open(nama_file, "a") as f:
            f.write(f"{hero.name}, {hero.health}")


layla = Hero("Layla", 70)
Hero("Balmond", 120).serang(layla)
TampilanHero().tampilkan(layla)
PenyimpanHero().simpan(layla, "data_hero.txt")