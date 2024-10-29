from collections import defaultdict
import random


class NPC:
    def __init__(self, name: str, id: int = 0):
        self.name = name
        self.id = id
        self.questions = []
        self.act = 0
    
    def load_questions(self, questions):
        self.questions.extend(questions)

    def talk_to_player(self): 
        self.act = random.randint(0, len(self.questions)-1)
    
    def action(self): 
        self.talk_to_player()
        print(self.questions[self.act])
        return self.act
    
class Enemy:
    def __init__(self, name: str, id: int = 0, attack: int = 0):
        self.name = name
        self.id = id
        self.questions = []
        self.act = 0
        self.hp = attack + 1
        self.attack = attack

    def load_questions(self, questions):
        self.questions.extend(questions)
    
    def load_attack(self, attack):
        self.hp = attack
        self.attack = attack

    def talk_to_player(self):
        self.act = random.randint(0, len(self.questions)-1)

    def action(self):
        self.talk_to_player()
        print(self.questions[self.act])
        return self.act
    

    def take_hit(self, value = 1):
        self.hp -= value
        if self.hp <= 0:
            print("Монстр побежден")


class Direction:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        if self.name == "Зима":
            self.effect = 1
        elif self.name == "Лето":
            self.effect = -1
        else:
            self.effect = 0

        
class Protagonist:  
    def __init__(self, name: str, id: str):  
        self.id = id  
        self.name: str = name
        self.hp: int = 10
        self.strength: int = 2
        self.armor: int = 0
        self.inventory = defaultdict(int)

    def talk_to(self, npc: NPC):
        print(npc.talk_to_player())
        print("У меня нет денег")

    def attack(self, enemy: Enemy):
        enemy.take_hit(self.strength)

    def take_hit(self, value=1):
        self.hp -= value
        if self.hp <= 0:

            raise Exception("You died")
    
    def heal(self, value=1):
        self.hp += 1
        print(f"Ваша здоровье увеличено на {value}")

    def advance_strength(self, value: int = 1):
        self.strength += value
        print(f"Ваша сила увеличена на {value}")

    def advance_armor(self, value: int = 1):
        self.armor += value
        print(f"Показатель брони увеличен на {value}")

    def go(self, counter: int):
        counter += 1
        return counter

    def whereami(self, direction: Direction):
        print(f"\nВы находитесь в локации \"{direction.name}\". \n{direction.description}")

    def take(self, item: str):
        self.inventory[item] = self.inventory.setdefault(item, 0) + 1
        self.check_upgrade()
        self.show_inventory()
    

    def give(self, npc: NPC, item: str):
        self.inventory[item] -= 1
        if self.inventory[item] == 0:
            del self.inventory[item]
        npc.receive(item)

    def check_upgrade(self):
        if self.inventory["apple"] >= 3:
            self.advance_strength()
            self.inventory["apple"] -= 3
        elif self.inventory["boost"] >= 2:
            self.heal()
            self.inventory["boost"] -= 2
        elif self.inventory["metall"] >= 3:
            self.advance_armor()
            self.inventory["metall"] -= 3

    def show_inventory(self):
        print(f"== В вашем инвентаре: ")
        for k, v in self.inventory.items():
            print(f"-> {k} - {v} шт.")


    

    



