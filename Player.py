import json
import math
import random
from Prayer import Prayer, PRAYERS
from AttackTypes import AttackStyle, AttackType
from pathlib import Path
from typing import Dict, Optional, Union
from util.player_info import *
from util.powered_staves_data import POWERED_STAVES_MAX_HIT

class PlayerStats:
    def __init__(self, attack: int, strength: int, defense: int, magic: int, ranged: int, hp: int):
        self.attack_level = attack
        self.strength_level = strength
        self.defense_level = defense
        self.magic_level = magic
        self.ranged_level = ranged

class Player:
    def __init__(self, name: str, stats: PlayerStats, attack_style: str, offensive_stat: str, prayer_name: str = None, equipment_file: str = "./resources/equipment.json"):
        self.name = name
        self.stats = stats
        self.attack_style = attack_style
        self.offensive_stat = offensive_stat
        self.prayer_active = PRAYERS.get(prayer_name)
        self.gear = {}
        self.special_attack_energy = 100
        self.special_regen_ticks = 0  
        self.thrall_active = False
        self.thrall_ticks = 0
        self.thrall_attack_cooldown = 4
        self.vengeance_active = False
        self.vengeance_cooldown = 50
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
    
    def calculate_max_hit(self) -> int:
        attack_type = self.get_attack_type()
        if attack_type == AttackType.MELEE:
            return self.calculate_melee_max_hit()
        elif attack_type == AttackType.RANGED:
            return self.calculate_ranged_max_hit()
        elif attack_type == AttackType.MAGIC:
            return self.calculate_magic_max_hit()
        else:
            return 0

    def calculate_melee_attack_roll(self) -> int:
        """Calculates the melee attack roll."""
        equipment_bonus = sum(
            next((i['offensive'][self.offensive_stat] for i in self.equipment_data if i['name'] == item), 0)
            for item in self.gear.values()
        )
        
        effective_level = self.stats.attack_level

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
        
        effective_level = self.stats.ranged_level

        if self.prayer_active:
            effective_level = int(effective_level * (1 + self.prayer_active.ranged_bonus))

        effective_level += 3 if self.attack_style == AttackStyle.ACCURATE else 0
        effective_level += 8

        return effective_level * (equipment_bonus + 64)

    def calculate_magic_attack_roll(self) -> int:
        """Calculates the magic attack roll, applying special effects for Tumeken's Shadow."""
        # Check if Tumeken's Shadow is equipped
        tumeken_equipped = "Tumeken's shadow" in self.gear.values()

        # Calculate magic equipment bonus, applying 3x for all gear except Tumeken's Shadow
        equipment_bonus = 0
        for item in self.gear.values():
            item_data = next((i for i in self.equipment_data if i['name'] == item), None)
            if item_data:
                # If Tumeken's Shadow is equipped, multiply other gear's magic bonus by 3
                if tumeken_equipped:
                    equipment_bonus += 3 * item_data.get('offensive', {}).get('magic', 0)
                else:
                    equipment_bonus += item_data.get('offensive', {}).get('magic', 0)

        # Calculate the effective magic level
        if self.prayer_active and self.prayer_active.magic_bonus:
            effective_level = math.floor(self.stats.magic_level * (1 + self.prayer_active.magic_bonus))
        else:
            effective_level = self.stats.magic_level

        # Add the attack style bonus (Accurate style for magic, e.g., +2 bonus)
        if self.attack_style == AttackStyle.ACCURATE:
            effective_level += 2

        # Add flat magic level bonuses (e.g., +9 for magic)
        effective_level += 9
        effective_level = math.floor(effective_level)

        return effective_level * (equipment_bonus + 64)
    
    def calculate_melee_max_hit(self) -> int:
        str_level = self.stats.strength_level
        
        if self.prayer_active.strength_bonus:
            prayer_modifier = (1 + self.prayer_active.strength_bonus)
        else: 
            prayer_modifier = 1

        effective_str_level = math.floor(str_level * prayer_modifier)
        
        if self.attack_style == AttackStyle.AGGRESSIVE:
            style_bonus = 3
        elif self.attack_style == AttackStyle.CONTROLLED:
            style_bonus = 1
        else: 
            style_bonus = 0

        #TODO add void
        effective_str_level = math.floor(effective_str_level + style_bonus + 8)

        str_bonus = sum(
            next((i['bonuses'].get('str', 0) for i in self.equipment_data if i['name'] == item), 0)
            for item in self.gear.values()
        )

        final_max_hit = (((effective_str_level * (str_bonus + 64)) + 320)/640)
        return math.floor(final_max_hit)

    def calculate_ranged_max_hit(self) -> int:
        """Calculates the max ranged hit for whatever idk who cares"""
        effective_ranged_str = self.stats.ranged_level

        if self.prayer_active.ranged_str_bonus:
            prayer_bonus = 1 + self.prayer_active.ranged_str_bonus
        else:
            prayer_bonus = 1
        
        attack_style_bonus = 3 if self.attack_style == AttackStyle.ACCURATE else 0

        #TODO add void and tbow
        effective_ranged_str = (self.stats.ranged_level * prayer_bonus) + attack_style_bonus + 8

        ranged_strength_bonus = sum(
            next((i['bonuses'].get('ranged_str', 0) for i in self.equipment_data if i['name'] == item), 0)
            for item in self.gear.values()
        )

        final_max_hit = 0.5 + ((effective_ranged_str * (ranged_strength_bonus + 64))/640)
        return math.floor(final_max_hit)

    def calculate_magic_max_hit(self) -> int:
        """Calculates the max magic hit for powered staves based on the player's magic level."""
        
        # Get the equipped weapon (powered staff)
        staff_name = self.gear.get("weapon")
        
        if not staff_name:  # Adjust to start from level 85
            raise ValueError(f"Weapon '{staff_name}' is not a powered staff.")

        # Fetch the player's current magic level
        magic_level = self.stats.magic_level

        # Get the base max hit from the lookup table, making sure the magic level is within bounds
        max_hit = POWERED_STAVES_MAX_HIT.get(min(magic_level, 125), {}).get(staff_name, 0)

        # Calculate the magic strength bonus from gear (such as Ancestral gear)
        magic_strength_bonus = sum(
            next((i['bonuses'].get('magic_str', 0) for i in self.equipment_data if i['name'] == item), 0)
            for item in self.gear.values()
        )

        magic_strength_bonus = magic_strength_bonus / 10
  
        # If Tumeken's Shadow is equipped, triple the magic strength bonus
        if staff_name == "Tumeken's shadow":
            magic_strength_bonus *= 3

        if self.prayer_active.magic_damage_bonus:
            magic_strength_bonus += (self.prayer_active.magic_damage_bonus*100)

        final_max_hit = max_hit * (1 + (magic_strength_bonus/100))

        return math.floor(final_max_hit)

    def attack(self):
        """Performs an attack if cooldown allows."""
        #print("Inside of attack field.")
        if self.attack_cooldown > 0:
            #print(f"Attack failed. {self.name} is on cooldown for {self.attack_cooldown} more ticks.")
            return False

        if self.thrall_active and self.thrall_ticks >= self.thrall_attack_cooldown:
            self.thrall_attack()
            self.thrall_ticks = 0  # Reset thrall's attack cooldown

        # Reset cooldown based on the weapon's speed
        weapon = self.gear.get("weapon")
        if weapon:
            self.attack_cooldown = self.get_weapon_speed()
            #print(f"{self.name} attacks with {weapon}! Cooldown set to {self.attack_cooldown} ticks.")
            return True
        else:
            #print(f"{self.name} attacks with bare hands! (Default cooldown of 4 ticks)")
            self.attack_cooldown = 4
            return True

    def thrall_attack(self):
        """Simulates the thralls attack."""
        thrall_damage = random.randint(0, 3)
        #print(f"{self.name}'s thrall hit for {thrall_damage} damage.")
        return thrall_damage
    
    def get_weapon_speed(self):
        """Returns the speed (in ticks) of the currently equipped weapon."""
        weapon = self.gear.get("weapon", None)
        if not weapon:
            return 4  # Default to 4-tick speed for bare hands
        
        # Assuming your equipment data has a 'speed' attribute for each weapon
        return next((i['speed'] for i in self.equipment_data if i['name'] == weapon), 4)


    def tick(self):
        """Increments tick variables. This should be called every game tick."""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.special_regen_ticks += 1
        self.regenerate_special_attack()
        
        if self.thrall_active:
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
        #print(f"{self.name} has summoned a thrall.")

    def dismiss_thrall(self):
        """Dismisses active thrall."""
        self.thrall_active = False
        self.thrall_ticks = 0
        #print(f"{self.name}'s thrall has been dismissed.")

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