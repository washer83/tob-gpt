import random
import math

class AttackHandler:
    def __init__(self, player, boss):
        self.player = player
        self.boss = boss

    def calculate_hit_roll(self) -> int:
        hit_roll = self.player.calculate_attack_roll()
        return hit_roll if hit_roll else 0
    
    def calculate_max_hit(self) -> int:
        max_hit = self.player.calculate_max_hit()
        return max_hit if max_hit else 0
    
    def calculate_boss_defense_roll(self) -> int:
        attack_type = self.player.get_attack_type()
        if attack_type == "Magic":
            return self.boss.magic_defense_roll()
        
        elif attack_type == "Ranged":
            return self.boss.ranged_defense_roll()
        
        elif attack_type == "Melee":
            if self.player.offensive_stat == "slash":
                return self.boss.slash_defense_roll()
            elif self.player.offensive_stat == "crush":
                return self.boss.crush_defense_roll()
            elif self.player.offensive_stat == "stab":
                return self.boss.stab_defense_roll()
            
        else:
            print(f"Attack type not found. {self.player.attack_type}")

    def calculate_hit(self) -> bool:
        player_attack_roll = self.calculate_hit_roll()
        boss_defense_roll = self.calculate_boss_defense_roll()

        if random.randint(0, player_attack_roll) > random.randint(0, boss_defense_roll):
            return True
        else:
            return False
        
    def calculate_damage(self) -> int:
        if self.calculate_hit():
            max_hit = self.calculate_max_hit()
            hit = random.randint(0, max_hit)
            if hit == 0:
                hit = 1 #hit clamping
            return hit
        else:
            return 0
        
    def perform_attack(self):
        if self.player.attack():
            damage = self.calculate_damage()
            if damage > 0:
                print(f"{self.player.name} hits {self.boss.__class__.__name__} for {damage} dmg!")
            else:
                print(f"{self.player.name} missed!")
            return damage

        else:
            print(f"Player on cooldown. CD: {self.player.attack_cooldown}")
            return 0