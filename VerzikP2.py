import random
import math

class VerzikP2:
    def __init__(self, scale: int):

        # Scale dependent variables
        if scale == 5:
            self.base_hp = 3500
        elif scale == 4:
            self.base_hp = 3062
        else:
            self.base_hp = 2625
        
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
        self.attack_cooldown_ticks = 4
        self.lightning_damage = 20  # Fixed lightning attack damage
        self.current_attack_count = 0  # To track attacks for the cycle (CCCCL)
        self.attack_pattern = ['C', 'C', 'C', 'C', 'L']  # C = cabbage, L = lightning
        self.current_attack_index = 0  # Start at the first attack in the cycle
        self.ticks_since_last_attack = 0  # Track the ticks since Verzik's last attack


    def take_damage(self, damage: int):
        self.hp -= damage
        self.hp = max(0, self.hp)
        print(f"Verzik takes {damage} damage. HP left: {self.hp}")
        return self.hp <= 0
    
    # Defense rolls per style
    def slash_defense_roll(self):
        defense_roll = (self.defence_lvl + 9) * (self.slash_def + 64)
        return defense_roll
    
    def ranged_def_roll(self):
        defense_roll = (self.defence_lvl + 9) * (self.ranged_def + 64)
        return defense_roll
    
    def magic_def_roll(self):
        defense_roll = (self.magic_lvl + 9) * (self.magic_def + 64)
        return defense_roll

    def verzik_attack(self):
        """Verzik performs an attack based on the current tick and cycle."""
        # Check if Verzik's HP is below 35% before performing the attack
        if self.hp <= self.reds_threshold:
            print("Verzik's HP is below 35%. Phase 2 ends.")
            self.phase_active = False
            return

        attack_type = self.attack_pattern[self.current_attack_index]

        if attack_type == 'C':
            # Cabbage attack (regular attack)
            print(f"Verzik throws a cabbage!")
            return

        elif attack_type == 'L':
            # Lightning attack (deals damage to Verzik)
            print(f"Verzik shoots a lightning attack and takes {self.lightning_damage} damage!")
            self.take_damage(self.lightning_damage)
            return

    def simulate_tick(self, player_damage):
        """Simulate one tick where both Verzik and the player can attack."""
        # Player can attack on every tick
        verzik_defeated = self.take_damage(player_damage)

        if not verzik_defeated:
            # Verzik checks if it's time to attack (every 4 ticks)
            if self.ticks_since_last_attack == self.attack_cooldown_ticks:
                self.verzik_attack()
                if not self.phase_active:
                    return  # End phase if HP is below 35%

                # Move to the next attack in the cycle (CCCCL)
                self.current_attack_index = (self.current_attack_index + 1) % len(self.attack_pattern)
                self.ticks_since_last_attack = 0  # Reset the attack cooldown
            else:
                print(f"Verzik is on cooldown. {self.attack_cooldown_ticks - self.ticks_since_last_attack} tick(s) remaining.")
                self.ticks_since_last_attack += 1
        else:
            self.phase_active = False
            print("Verzik P2 has been defeated.")

    def is_phase_active(self):
        """Check if phase 2 is still active."""
        return self.phase_active  # Return the phase's active status  

verzik = VerzikP2(scale=3)

tick = 0
while verzik.is_phase_active():
    print(f"Tick {tick+1}:")
    if tick%5 == 0:
        player_damage = random.randint(0,100)
    else:
        player_damage = 0
    verzik.simulate_tick(player_damage)
    tick += 1
    if not verzik.is_phase_active():
        print("!!! Reds Spawned !!!\n")
        print(f"HP Proc: {verzik.hp/verzik.base_hp * 100}%")