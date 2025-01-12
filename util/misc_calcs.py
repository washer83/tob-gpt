import random

def ticks_to_time(ticks):
    """
    Converts game ticks to MM:SS format.
    
    :param ticks: int/list of game ticks
    :return: String (or list) in MM:SS format
    """
    def convert(t):
        total_seconds = t * 0.6
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return f"{minutes:02}:{seconds:02}"
    
    if isinstance(ticks, list):
        return [convert(t) for t in ticks]
    if isinstance(ticks, int):
        return convert(ticks)
    else:
        raise ValueError("Input must be an int or list.")

def calculate_purple_crab_hit(player) -> bool:
    player_attack_roll = player.calculate_attack_roll()
    purple_crab_def_roll = 3776
    
    if random.randint(0, player_attack_roll) > random.randint(0, purple_crab_def_roll):
        return True
    else:
        return False