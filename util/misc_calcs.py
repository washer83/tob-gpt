import random

def calculate_purple_crab_hit(player) -> bool:
    player_attack_roll = player.calculate_attack_roll()
    purple_crab_def_roll = 3776
    
    if random.randint(0, player_attack_roll) > random.randint(0, purple_crab_def_roll):
        return True
    else:
        return False