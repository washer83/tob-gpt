def print_bonuses(player):
    print("\n\n+-----------------+-------+")
    print("|      Style      | Value |")
    print("+-----------------+-------+")

    total_bonuses = player.calculate_total_bonuses()
    total_offensive = player.calculate_total_offensive()
    total_defensive = player.calculate_total_defensive()

    print(f"| Strength        | {total_bonuses['str']:>5} |")
    print(f"| Ranged Strength | {total_bonuses['ranged_str']:>5} |")
    print(f"| Magic Strength  | {total_bonuses['magic_str']:>5} |")
    print(f"| Prayer          | {total_bonuses['prayer']:>5} |")

    print("+-----------------+-------+")
    print("|   Offensive     |       |")
    print("+-----------------+-------+")

    print(f"| Stab            | {total_offensive['stab']:>5} |")
    print(f"| Slash           | {total_offensive['slash']:>5} |")
    print(f"| Crush           | {total_offensive['crush']:>5} |")
    print(f"| Magic           | {total_offensive['magic']:>5} |")
    print(f"| Ranged          | {total_offensive['ranged']:>5} |")

    print("+-----------------+-------+")
    print("|   Defensive     |       |")
    print("+-----------------+-------+")

    print(f"| Stab            | {total_defensive['stab']:>5} |")
    print(f"| Slash           | {total_defensive['slash']:>5} |")
    print(f"| Crush           | {total_defensive['crush']:>5} |")
    print(f"| Magic           | {total_defensive['magic']:>5} |")
    print(f"| Ranged          | {total_defensive['ranged']:>5} |")

    print("+-----------------+-------+")


def print_gear(player):
    print("\n\n+-----------------+------------------------+")
    print("|      Slot       |         Item           |")
    print("+-----------------+------------------------+")
    for slot, item_name in player.gear.items():
        print(f"| {slot:<15} | {item_name:<22} |")
    print("+-----------------+------------------------+")


def print_roll(player):
    print("\n\n+-------------+---------+")
    print(f"| Attack Roll |  {player.calculate_attack_roll():>6} |")
    print("+-------------+---------+")

def print_max(player):
    print("\n\n+---------+--------+")
    print(f"| Max Hit | {player.calculate_max_hit():>6} |")
    print("+---------+--------+")
