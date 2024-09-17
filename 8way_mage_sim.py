import csv
from Player import *
from VerzikP2 import VerzikP2
from util.attack_handler import AttackHandler
from util.loadout import default_loadouts, create_player
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm  

import csv
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

# Simulation to run the logic multiple times and store the results
def run_single_simulation(iteration, loadouts):
    # Initialize the mager and ranger with their default loadouts
    mager = create_player("Mager", loadouts["melee"])  # Start with melee loadout
    ranger = create_player("Ranger", loadouts["melee"])  # Assume we have a range loadout for the ranger

    # Initialize Verzik
    verzik = VerzikP2(scale=2)

    # Create attack handlers for both players
    attack_handler_mager_melee = AttackHandler(mager, verzik)  # Melee attack handler for mager
    attack_handler_mager_mage = AttackHandler(None, verzik)  # Mage attack handler (will update this when swapping loadouts)
    attack_handler_ranger = AttackHandler(ranger, verzik)

    # Summon thralls
    mager.summon_thrall()
    ranger.summon_thrall()

    # Variables to track damage
    mage_damage_total = 0
    ranger_damage_total = 0

    tick = 0
    while verzik.is_phase_active():
        verzik_attacking = verzik.ticks_since_last_attack == verzik.attack_cooldown_ticks

        # Mager attack logic
        if mager.attack_cooldown == 0:
            if verzik_attacking:
                mager = create_player("Mager", loadouts["mage_8_way"])  # Switch to mage loadout
                attack_handler_mager_mage = AttackHandler(mager, verzik)  # Update attack handler for mage loadout
                player_damage = attack_handler_mager_mage.perform_attack()  # Perform attack using mage gear
                mager = create_player("Mager", loadouts["melee"])  # Switch back to melee loadout
                attack_handler_mager_melee = AttackHandler(mager, verzik)  # Reset attack handler to melee loadout
            else:
                player_damage = attack_handler_mager_melee.perform_attack()  # Melee attack
            verzik.take_damage(player_damage)
            mage_damage_total += player_damage

        # Ranger attack logic
        if ranger.attack_cooldown == 0:
            if verzik_attacking:
                ranger.attack_cooldown = 1  # Ranger misses the attack due to Verzik attacking on the same tick
            else:
                player_damage_ranger = attack_handler_ranger.perform_attack()
                verzik.take_damage(player_damage_ranger)
                ranger_damage_total += player_damage_ranger

        # Decrement cooldowns
        mager.tick()
        ranger.tick()

        # Verzik's actions
        verzik.simulate_tick(0)

        tick += 1

    # Calculate damage percentages
    total_damage = mage_damage_total + ranger_damage_total
    mage_dmg_percent = (mage_damage_total / total_damage) * 100 if total_damage > 0 else 0
    range_dmg_percent = (ranger_damage_total / total_damage) * 100 if total_damage > 0 else 0
    proc_percent = (verzik.hp / verzik.base_hp) * 100


    # Return the result of the simulation
    return [iteration, tick, mage_dmg_percent, range_dmg_percent, proc_percent]

# Function to run simulations in parallel
def run_simulations_in_parallel(n):
    loadouts = default_loadouts()  # Load once, reused across all iterations
    results = []

    # Use ProcessPoolExecutor to parallelize the simulation
    with ProcessPoolExecutor() as executor:
        # Submit all tasks
        futures = [executor.submit(run_single_simulation, iteration, loadouts) for iteration in range(1, n + 1)]

        # Use tqdm to track progress
        for future in tqdm(as_completed(futures), total=n, desc="Simulating"):
            results.append(future.result())

    return results

# Function to save results to a CSV file
def save_results_to_csv(results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['iter', 'ticks_until_defeat', 'mage_dmg_percent', 'range_dmg_percent', 'proc_percent'])
        writer.writerows(results)

# Protect the multiprocessing logic with if __name__ == '__main__':
if __name__ == '__main__':
    n_simulations = 1000 # Adjust this number as needed
    results = run_simulations_in_parallel(n_simulations)
    save_results_to_csv(results, "8_way_mage_no_boots_results.csv")
    print("Simulations done!")