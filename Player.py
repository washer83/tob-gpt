import json
from pathlib import Path
from typing import Dict, Optional, Union
from util.player_info import *

class Prayer:
    def __init__(self, name: str, attack_bonus: float, strength_bonus: float, defense_bonus: float):
        self.name = name
        self.attack_bonus = attack_bonus
        self.strength_bonus = strength_bonus
        self.defense_bonus = defense_bonus

class PlayerStats:
    def __init__(self, attack: int, strength: int, defense: int, magic: int, ranged: int, hp: int):
        self.attack = attack
        self.strength = strength
        self.defense = defense
        self.magic = magic
        self.ranged = ranged

class AttackStyle:
    ACCURATE = "Accurate"
    AGGRESSIVE = "Aggressive"
    DEFENSIVE = "Defensive"
    CONTROLLED = "Controlled"
    RAPID = "Rapid"
    LONGRANGE = "Longrange"

class AttackType:
    MELEE = "Melee"
    RANGED = "Ranged"
    MAGIC = "Magic"

class Player:
    def __init__(self, name: str, stats: PlayerStats, attack_style: str, offensive_stat: str, prayer_active: Optional[Prayer], equipment_file: str = "./resources/equipment.json"):
        self.name = name
        self.stats = stats
        self.attack_style = attack_style
        self.offensive_stat = offensive_stat
        self.prayer_active = prayer_active
        self.gear = {}
        self.special_attack_energy = 100
        self.special_regen_ticks = 0  
        self.thrall_active = False
        self.thrall_ticks = 0
        self.vengeance_active = False
        self.attack_cooldown = 0
        self.load_equipment(equipment_file)

    def load_equipment(self, equipment_file: str):
        """Loads equipment data from a JSON file."""
        equipment_path = Path(equipment_file)
        if equipment_path.is_file():
            with open(equipment_file, 'r') as file:
                self.equipment_data = json.load(file)
        else:
            raise FileNotFoundError(f"Equipment file not found at {equipment_file}.")
    
    def equip_item(self, item_name: str):
        """Equips an item, modifies stats."""
        item = next((i for i in self.equipment_data if i['name'] == item_name), None)
        if not item:
            raise ValueError(f"Item {item_name} not found.")
        
        slot = item['slot']
        if slot in self.gear:
            self.unequip_item(slot)
        
        self.gear[slot] = item_name
        self.modify_stats(item, remove=False)

    def unequip_item(self, slot: str):
        """Unequips an item from specified slot."""
        if slot not in self.gear:
            raise ValueError(f"No item equipped in slot {slot}.")
        
        item_name = self.gear.pop(slot)
        item = next((i for i in self.equipment_data if i['name'] == item_name), None)
        self.modify_stats(item, remove=True)

    def modify_stats(self, item: Dict, remove=False):
        """Modifies player's stats based on the item's offensive, defensive, and bonuses."""
        multiplier = -1 if remove else 1
        
        # Apply offensive stats
        for stat, value in item.get('offensive', {}).items():
            if stat not in self.stats.__dict__:
                self.stats.__dict__[stat] = 0
            self.stats.__dict__[stat] += multiplier * value
        
        # Apply defensive stats
        for stat, value in item.get('defensive', {}).items():
            if stat not in self.stats.__dict__:
                self.stats.__dict__[stat] = 0
            self.stats.__dict__[stat] += multiplier * value
        
        # Apply bonus stats
        for stat, value in item.get('bonuses', {}).items():
            if stat not in self.stats.__dict__:
                self.stats.__dict__[stat] = 0
            self.stats.__dict__[stat] += multiplier * value

    def get_attack_type(self) -> str:
        """Determines the attack type based on the equipped weapon."""
        weapon = self.gear.get("weapon")
        if not weapon:
            return AttackType.MELEE  # Default to melee if no weapon equipped

        weapon_category = next((i['category'] for i in self.equipment_data if i['name'] == weapon), None)
        if weapon_category in ["Bow", "Crossbow"]:
            return AttackType.RANGED
        elif weapon_category in ["Staff", "Powered Staff"]:
            return AttackType.MAGIC
        else:
            return AttackType.MELEE

    def calculate_attack_roll(self) -> int:
        """Calculates the attack roll based on the current attack type."""
        attack_type = self.get_attack_type()
        if attack_type == AttackType.MELEE:
            return self.calculate_melee_attack_roll()
        elif attack_type == AttackType.RANGED:
            return self.calculate_ranged_attack_roll()
        elif attack_type == AttackType.MAGIC:
            return self.calculate_magic_attack_roll()
        return 0

    def calculate_melee_attack_roll(self) -> int:
        """Calculates the melee attack roll."""
        equipment_bonus = sum(
            next((i['offensive'][self.offensive_stat] for i in self.equipment_data if i['name'] == item), 0)
            for item in self.gear.values()
        )
        
        effective_level = self.stats.attack

        if self.prayer_active:
            effective_level = int(effective_level * (1 + self.prayer_active.attack_bonus))

        effective_level += 3 if self.attack_style == AttackStyle.ACCURATE else 1 if self.attack_style == AttackStyle.CONTROLLED else 0
        effective_level += 8

        return effective_level * (equipment_bonus + 64)

    def calculate_ranged_attack_roll(self) -> int:
        """Calculates the ranged attack roll."""
        equipment_bonus = sum(
            next((i['offensive']['ranged'] for i in self.equipment_data if i['name'] == item), 0)
            for item in self.gear.values()
        )
        
        effective_level = self.stats.ranged

        if self.prayer_active:
            effective_level = int(effective_level * (1 + self.prayer_active.attack_bonus))

        effective_level += 3 if self.attack_style == AttackStyle.ACCURATE else 0
        effective_level += 8

        return effective_level * (equipment_bonus + 64)

    def calculate_magic_attack_roll(self) -> int:
        """Calculates the magic attack roll."""
        equipment_bonus = sum(
            next((i['offensive']['magic'] for i in self.equipment_data if i['name'] == item), 0)
            for item in self.gear.values()
        )
        
        effective_level = self.stats.magic

        if self.prayer_active:
            effective_level = int(effective_level * (1 + self.prayer_active.attack_bonus))

        effective_level += 8

        return effective_level * (equipment_bonus + 64)
    
    def attack(self):
        """Performs an attack if cooldown allows."""
        if self.attack_cooldown > 0:
            print(f"Attack failed. {self.name} is on cooldown for {self.attack_cooldown} more ticks.")
            return False

        if self.thrall_active == True and self.thrall_ticks >= 4:
            print(f"{self.name} can attack with thrall.")
            #TODO: add thrall hit 
            self.thrall_ticks = 0

        # Reset cooldown based on the weapon's speed
        weapon = self.gear.get("weapon")
        if weapon:
            weapon_speed = next((i['speed'] for i in self.equipment_data if i['name'] == weapon), 4)
            self.attack_cooldown = weapon_speed
            print(f"{self.name} attacks with {weapon}! Cooldown set to {weapon_speed} ticks.")
            return True
        else:
            print(f"{self.name} attacks with bare hands! (Default cooldown of 4 ticks)")
            self.attack_cooldown = 4
            return True

    def tick(self):
        """Increments tick variables. This should be called every game tick."""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.special_regen_ticks += 1
        self.regenerate_special_attack()

        self.thrall_ticks += 1
        #TODO: Add thrall check here

    def regenerate_special_attack(self):
        """Regenerates special attack in increments of 10% at a time."""
        lightbearer = 'Lightbearer' in self.gear.values()
        regen_interval = 50 if lightbearer else 100

        if self.special_regen_ticks >= regen_interval and self.special_attack_energy < 100:
            self.special_attack_energy += 10
            self.special_attack_energy = min(self.special_attack_energy, 100) # Cap at 100
            self.special_regen_ticks = 0

            print(f"{self.name} regenerates special attack energy. Current: {self.special_attack_energy}%")

    def use_special_attack(self, energy_cost: int):
        """Use a special attack, if enough energy."""
        if self.special_attack_energy >= energy_cost:
            self.special_attack_energy -= energy_cost
            print(f"{self.name} used a special attack.")
            return True
        else:
            print(f"{self.name} doesn't have enough energy. Current: {self.special_attack_energy}, requested: {energy_cost}")

    def summon_thrall(self):
        """Summons a thrall."""
        self.thrall_active = True
        self.thrall_ticks = 3 # Thrall should attack next tick after being summoned.
        print(f"{self.name} has summoned a thrall.")

    def dismiss_thrall(self):
        """Dismisses active thrall."""
        self.thrall_active = False
        self.thrall_ticks = 0
        print(f"{self.name}'s thrall has been dismissed.")

    def take_damage(self, damage: int):
        """Reduces player's HP by given damage."""
        self.hp -= damage
        if self.vengeance_active:
            reflected_damage = int(damage*0.75)
            print(f"{self.name}'s vengeance has been activated.")
            self.vengeance_active = False
        if self.hp < 0:
            self.hp = 0
            print("he dead.")
        print(f"{self.name} took {damage}. HP remaining {self.hp}")
    
    def heal(self, amount: int):
        """Heals by a certain amount."""
        self.hp += amount
        if self.hp > 99:
            self.hp = 99
        print(f"{self.name} healed {amount} HP. Now {self.hp} HP.")
        
    def calculate_total_bonuses(self):
        total_bonuses = {
            "str": 0,
            "ranged_str": 0,
            "magic_str": 0,
            "prayer": 0,
        }
        for item_name in self.gear.values():
            item = next((i for i in self.equipment_data if i['name'] == item_name), {})
            for key in total_bonuses.keys():
                total_bonuses[key] += item.get('bonuses', {}).get(key, 0)
        return total_bonuses

    def calculate_total_offensive(self):
        total_offensive = {
            "stab": 0,
            "slash": 0,
            "crush": 0,
            "magic": 0,
            "ranged": 0,
        }
        for item_name in self.gear.values():
            item = next((i for i in self.equipment_data if i['name'] == item_name), {})
            for key in total_offensive.keys():
                total_offensive[key] += item.get('offensive', {}).get(key, 0)
        return total_offensive

    def calculate_total_defensive(self):
        total_defensive = {
            "stab": 0,
            "slash": 0,
            "crush": 0,
            "magic": 0,
            "ranged": 0,
        }
        for item_name in self.gear.values():
            item = next((i for i in self.equipment_data if i['name'] == item_name), {})
            for key in total_defensive.keys():
                total_defensive[key] += item.get('defensive', {}).get(key, 0)
        return total_defensive

    def __str__(self):
        return f"Player: {self.name}\n Gear: {self.gear}"

# Example usage:
player_stats = PlayerStats(attack=118, strength=118, defense=118, magic=112, ranged=112, hp=121)
prayer = Prayer(name="Piety", attack_bonus=0.20, strength_bonus=0.23, defense_bonus=0.25)
player = Player(name="test", stats=player_stats, attack_style=AttackStyle.AGGRESSIVE, offensive_stat="slash", prayer_active=prayer)

player.equip_item("Bandos godsword")
player.equip_item("Bandos tassets")

print_bonuses(player)
print_gear(player)
print_roll(player)


# Attack with the weapon, reducing the cooldown
player.attack()

# Simulate a few game ticks
for _ in range(3):
    player.tick()
    print(f"Tick passed. {player.attack_cooldown} ticks remaining on cooldown.")

# Attempt to attack again
player.attack()

# Simulate more ticks and attack again
player.tick()
player.tick()
player.attack()