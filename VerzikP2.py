import random
import math

class VerzikP2:
    def __init__(self, scale: int):
        
        self.debug_statements = False

        # Scale dependent variables
        if scale == 5:
            self.base_hp = 3500
        elif scale == 4:
            self.base_hp = 3062
        else:
            self.base_hp = 2625
        
        # Stats
        self.defence_lvl = 200
        self.magic_lvl = 400
        self.range_lvl = 400
        self.stab_def = 100
        self.slash_def = 60
        self.crush_def = 100
        self.magic_def = 70
        self.ranged_def = 250
        self.hp = self.base_hp

        self.reds_threshold = int(math.floor(self.base_hp * 0.35))
        self.phase_active = True
        self.attack_cooldown_ticks = 3
        self.lightning_damage = 20  # Fixed lightning attack damage
        self.current_attack_count = 0  # To track attacks for the cycle (CCCCL)
        self.attack_pattern = ['C', 'C', 'C', 'C', 'L']  # C = cabbage, L = lightning
        self.current_attack_index = 0  # Start at the first attack in the cycle
        self.ticks_since_last_attack = 0  # Track the ticks since Verzik's last attack

        # Purple crab
        self.purple_crab_active = False
        self.attacks_since_last_crab = 0  # Track the number of Verzik's auto-attacks
        self.min_attacks_for_crab = 20  # Crab can only spawn after 20 auto-attacks
        self.purple_crab_ticks_alive = 0

    def take_damage(self, damage: int):
        self.hp -= damage
        self.hp = max(0, self.hp)
        if damage > 0:
            pass
        return self.hp <= 0
    
    def heal(self, health: int):
        self.hp += health
        self.hp = max(health, self.base_hp)
    
    def spawn_purple_crab(self):
        """Attempt to spawn the purple crab if conditions are met after 20 auto-attacks."""
        if self.attacks_since_last_crab >= self.min_attacks_for_crab:
            if random.random() < 1/3:
                self.purple_crab_active = True
                self.attacks_since_last_crab = 0  
                print("Purple crab spawned.") if self.debug_statements else None
            else:
                print("Crab conditions met, but not spawned.") if self.debug_statements else None

    def pop_purple_crab(self):
        """Pop the purple crab with a poison weapon and deal damage to Verzik."""
        if self.purple_crab_active:
            damage = random.randint(65, 75)
            print(f"Purple crab popped, dealing {damage} to Verzik.") if self.debug_statements else None
            self.take_damage(damage)
            self.purple_crab_active = False

    # Defense rolls per style
    def slash_defense_roll(self):
        defense_roll = (self.defence_lvl + 9) * (self.slash_def + 64)
        return defense_roll
    
    def ranged_defense_roll(self):
        defense_roll = (self.defence_lvl + 9) * (self.ranged_def + 64)
        return defense_roll
    
    def magic_defense_roll(self):
        defense_roll = (self.magic_lvl + 9) * (self.magic_def + 64)
        return defense_roll

    def verzik_attack(self):
        """Verzik performs an attack based on the current tick and cycle."""
        # Check if Verzik's HP is below 35% before performing the attack
        if self.hp <= self.reds_threshold:
            self.phase_active = False
            return

        # Check if a purple crab can spawn after a minimum of 20 auto-attacks
        self.attacks_since_last_crab += 1
        if self.attacks_since_last_crab >= self.min_attacks_for_crab:
            self.spawn_purple_crab()

        if self.purple_crab_active:
            attack_type = None  # No attack if the purple crab is active
        else: 
            attack_type = self.attack_pattern[self.current_attack_index]

        if attack_type == 'C':
            # Cabbage attack (regular attack)
            return

        elif attack_type == 'L':
            # Lightning attack (deals damage to Verzik)
            self.take_damage(self.lightning_damage)
            return
        
    def simulate_tick(self, player_damage):
        """Simulate one tick where both Verzik and the player can attack."""
        verzik_defeated = self.take_damage(player_damage)

        if self.purple_crab_active:
            self.purple_crab_ticks_alive += 1

        if not verzik_defeated:
            # Verzik checks if it's time to attack (every 3 ticks)
            if self.ticks_since_last_attack == self.attack_cooldown_ticks:
                self.verzik_attack()
                if not self.phase_active:
                    return  # End phase if HP is below 35%

                # Move to the next attack in the cycle (CCCCL)
                self.current_attack_index = (self.current_attack_index + 1) % len(self.attack_pattern)
                self.ticks_since_last_attack = 0  # Reset the attack cooldown

                if self.purple_crab_active and self.attacks_since_last_crab > 2:
                    heal_amount = random.randint(9,11)
                    print(f"VERZIK HEALING FOR: {heal_amount}") if self.debug_statements else None
                    self.heal(heal_amount)

            else:
                self.ticks_since_last_attack += 1
        else:
            self.phase_active = False

    def is_phase_active(self):
        """Check if phase 2 is still active."""
        return self.phase_active  # Return the phase's active status
