import random
import math
from util.misc_calcs import *

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
        boss_defense_roll = max(0, self.calculate_boss_defense_roll())  # Ensure no negative defense rolls
        
        #print(f"Player Attack Roll: {player_attack_roll}, Boss Defense Roll: {boss_defense_roll}")

        if random.randint(0, player_attack_roll) > random.randint(0, boss_defense_roll):
            return True
        else:
            return False

    def calculate_scythe_damage(self, max_hit: int) -> int:
        """Calculate scythe damage."""
        hit1 = hit2 = hit3 = 0
        max_hit1 = max_hit
        max_hit2 = math.floor(max_hit1/2)
        max_hit3 = math.floor(max_hit2/2)

        boss_defense_roll = self.calculate_boss_defense_roll()

        # First hit:
        if random.randint(0, self.calculate_hit_roll()) > random.randint(0, boss_defense_roll):
            hit1 = random.randint(0, max_hit1)
            if hit1 == 0:
                hit1 = 1 
        else:
            hit1 = 0
        
        # Second hit:
        if random.randint(0, self.calculate_hit_roll()) > random.randint(0, boss_defense_roll):
            hit2 = random.randint(0, max_hit2)
            if hit2 == 0:
                hit2 = 1
        else:
            hit2 = 0

        # Third hit: 
        if random.randint(0, self.calculate_hit_roll()) > random.randint(0, boss_defense_roll):
            hit3 = random.randint(0, max_hit3)
            if hit3 == 0:
                hit3 = 1
        else:
            hit3 = 0

        total_damage = hit1 + hit2 + hit3
        return total_damage
    
    def calculate_claw_special(self, max_hit: int) -> int:
        """Calculate the damage for a Dragon Claws special attack."""
        damage = 0
        boss_defense_roll = self.calculate_boss_defense_roll()

        # First roll (4-2-1-1)
        if random.randint(0, self.calculate_hit_roll()) > random.randint(0, boss_defense_roll):
            # First hit success
            hit1 = random.randint(max_hit // 2, max_hit - 1)
            hit2 = hit1 // 2
            hit3 = hit2 // 2
            hit4 = hit3 + 1
            damage = hit1 + hit2 + hit3 + hit4
        else:
            # Second roll (0-4-2-2)
            if random.randint(0, self.calculate_hit_roll()) > random.randint(0, boss_defense_roll):
                hit2 = random.randint(int(max_hit * 3 / 8), int(max_hit * 7 / 8))
                hit3 = hit2 // 2
                hit4 = hit3 + 1
                damage = hit2 + hit3 + hit4
            else:
                # Third roll (0-0-3-3)
                if random.randint(0, self.calculate_hit_roll()) > random.randint(0, boss_defense_roll):
                    hit3 = random.randint(int(max_hit * 1 / 4), int(max_hit * 3 / 4))
                    hit4 = hit3 + 1
                    damage = hit3 + hit4
                else:
                    # Fourth roll (0-0-0-5)
                    if random.randint(0, self.calculate_hit_roll()) > random.randint(0, boss_defense_roll):
                        hit4 = random.randint(int(max_hit * 1 / 4), int(max_hit * 5 / 4))
                        damage = hit4
                    else:
                        # Final fail case: 0-0-0-0 -> 2 damage or 0 damage
                        damage = 2 if random.random() <= 0.67 else 0

        return damage

    def calculate_damage(self, special_attack=False) -> int:
        max_hit = self.calculate_max_hit()
        #print(f"Max Hit: {max_hit}")

        if self.player.gear.get("weapon") == "Scythe of vitur":
            return self.calculate_scythe_damage(max_hit)

        if self.calculate_hit():
            hit = random.randint(0, max_hit)
            if hit == 0:
                hit = 1  # hit clamping
            return hit
        else:
            return 0

    def handle_purple_crab(self) -> None:
        """Handles the purple crab popping with the blowpipe."""
        if calculate_purple_crab_hit(self.player):  
            self.boss.pop_purple_crab()  # Pop the crab
        else:
            pass

    def perform_attack(self, special_attack: bool = False):
        """Perform the attack, respecting cooldowns and checking for purple crab status."""
        
        # If blowpipe is equipped and purple crab is active, handle the crab
        if self.player.gear.get("weapon") == "Toxic blowpipe" and self.boss.purple_crab_active:
            self.handle_purple_crab()
            self.player.attack_cooldown = 2  # Set the blowpipe cooldown to 2 ticks
            return 0  # Return early, as the attack is aimed at the crab

        # Check if the player can attack based on cooldown
        if self.player.attack():
            damage = self.calculate_damage(special_attack)
            #print(f"{self.player.name} swung {self.player.gear.get('weapon')} for {damage} dmg.")
            return damage  # Return calculated damage
        else:
            return 0  # Player is still on cooldown, no damage

