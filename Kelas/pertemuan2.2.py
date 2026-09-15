from dataclasses import dataclass

class Hero:
    name: str
    hp: int
    atk: int
    armor: int

    def __post_init__(self):
        print