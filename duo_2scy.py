import csv
import random
from Player import Player
from VerzikP2 import VerzikP2
from util.attack_handler import AttackHandler
from util.loadout import default_loadouts, create_player, switch_player_to_loadout
from tqdm import tqdm
from multiprocessing import Pool

def run_p2_simulation(_unused: int = 0) -> tuple:
    """
    Runs a single Verzik P2 fight simulation.
    Returns (ticks_elapsed, total_mager_damage, total_ranger_damage).
    """
    # -------------------------------
    # 1. Load default loadouts
    # -------------------------------
    loadouts = default_loadouts()

    # -------------------------------
    # 2. Create players
    # -------------------------------
    mager = create_player("Mager", loadouts["melee"])   # Start with melee gear
    ranger = create_player("Ranger", loadouts["melee"]) # Start with melee gear or "ranged"

    mager.summon_thrall()
    ranger.summon_thrall()

    # Track total damage done by each player
    total_mager_damage = 0
    total_ranger_damage = 0

    # -------------------------------
    # 3. Create Verzik P2
    # -------------------------------
    verzik = VerzikP2(scale=2)
    verzik.attacks_since_last_crab = 20  # Force crab spawn quickly for the example

    # -------------------------------
    # 4. Create AttackHandlers
    # -------------------------------
    attack_handler_mager = AttackHandler(mager, verzik)
    attack_handler_ranger = AttackHandler(ranger, verzik)

    # Optional: pick random crab popper
    popper = random.choice([mager, ranger])

    ticks_elapsed = 0
    while verzik.is_phase_active():
        # We'll aggregate total damage this tick in queued_dmg
        queued_dmg = 0

        # Check if Verzik is about to do an attack this tick
        verzik_attacking = (verzik.ticks_since_last_attack == verzik.attack_cooldown_ticks)

        # 4a) Purple crab logic
        if verzik.purple_crab_active:
            if popper.attack_cooldown == 0:
                # Switch to blowpipe loadout for popper (example)
                # Adjust your actual blowpipe loadout name if needed
                if popper.name == "Ranger":
                    switch_player_to_loadout(popper, loadouts["range_bp"])
                if popper.name == "Mager":
                    switch_player_to_loadout(popper, loadouts["mage_bp"])

                # Attack crab
                ah_popper = AttackHandler(popper, verzik)
                dmg = ah_popper.perform_attack()
                queued_dmg += dmg

                # Switch back to melee
                switch_player_to_loadout(popper, loadouts["melee"])

            popper.tick()

        else:
            # 4b) Mager logic
            if mager.attack_cooldown == 0:
                if verzik_attacking:
                    # Force a miss this tick (skip the attack)
                    mager.attack_cooldown = 1
                else:
                    dmg = attack_handler_mager.perform_attack()
                    queued_dmg += dmg
                    total_mager_damage += dmg

            # 4c) Ranger logic
            if ranger.attack_cooldown == 0:
                if verzik_attacking:
                    # Force a miss this tick (skip the attack)
                    ranger.attack_cooldown = 1
                else:
                    dmg = attack_handler_ranger.perform_attack()
                    queued_dmg += dmg
                    total_ranger_damage += dmg

            # Ticking down
            mager.tick()
            ranger.tick()

        # 4d) Apply all queued damage
        # Instead of direct take_damage, we can pass it into simulate_tick
        # but let's do direct for clarity:
        # verzik.take_damage(queued_dmg)

        # 4e) Verzik sim tick
        verzik.simulate_tick(queued_dmg)

        ticks_elapsed += 1

        # Check if done
        if not verzik.is_phase_active():
            proc = round(verzik.hp / verzik.base_hp * 100, 2)
            break

    return (ticks_elapsed, total_mager_damage, total_ranger_damage, proc)


def run_multiple_simulations(num_iterations=10, output_csv="p2_results.csv"):
    """
    Parallelizes multiple Verzik P2 simulations and writes results to CSV,
    with a progress bar from tqdm.
    """
    print("Beginning P2 simulations for DUO_1_SHADOW_1_SCY ...")
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["iter", "time", "mager_dmg", "ranger_dmg"])

        # 2) Use multiprocessing Pool
        with Pool() as pool:
            # We pass a range(num_iterations) so each worker has a separate job.
            # `_unused` can be used for seeding or scenario indexing if needed.
            # We'll enumerate the results, starting at 1, for iteration counting.
            for iteration, (ticks_elapsed, mager_dmg, ranger_dmg, proc) in enumerate(
                tqdm(pool.imap(run_p2_simulation, range(num_iterations)), 
                     total=num_iterations),
                start=1
            ):
                # 3) Write each result row to CSV
                writer.writerow([
                    iteration,
                    ticks_elapsed,
                    mager_dmg,
                    ranger_dmg,
                    proc
                ])

                # Print or log if you want
                # print(f"Iteration {iteration} -> ticks={ticks_elapsed}, Mager={mager_dmg}, Ranger={ranger_dmg}")

    print(f"Done! Results written to {output_csv}.")


if __name__ == "__main__":
    run_multiple_simulations(num_iterations=1000, output_csv="verzik/results/duo/duo_2scy_rancour_thrall_results.csv")
    print("Done! Check your p2_results.csv file for results.")
