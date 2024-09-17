from Player import *
from VerzikP2 import VerzikP2
from util.attack_handler import AttackHandler
from util.loadout import default_loadouts, create_player

# Load the default loadouts
loadouts = default_loadouts()

# Initialize the mager and ranger with their default loadouts
mager = create_player("Mager", loadouts["melee"])  # Start with melee loadout
ranger = create_player("Ranger", loadouts["melee"])  # Assume we have a range loadout for the ranger

# Initialize Verzik
verzik = VerzikP2(scale=2)

# Create attack handlers for both players
attack_handler_mager_melee = AttackHandler(mager, verzik)  # Melee attack handler for mager
attack_handler_mager_mage = AttackHandler(None, verzik)  # Mage attack handler (will update this when swapping loadouts)
attack_handler_ranger = AttackHandler(ranger, verzik)

mager.summon_thrall()
ranger.summon_thrall()

# Simulation loop
tick = 0
while verzik.is_phase_active():
    #print(f"Tick {tick + 1}:")

    # Check if Verzik is attacking this tick
    verzik_attacking = verzik.ticks_since_last_attack == verzik.attack_cooldown_ticks

    # Mager attack logic
    if mager.attack_cooldown == 0:
        if verzik_attacking:
        
            # If Verzik is attacking on the same tick, swap to Mage loadout
            #print(f"{mager.name} swaps to Mage gear to avoid missing.")

            # Temporarily swap to mage loadout and attack
            mager = create_player("Mager", loadouts["mage_8_way"])  # Switch to mage loadout
            attack_handler_mager_mage = AttackHandler(mager, verzik)  # Update attack handler for mage loadout
            player_damage = attack_handler_mager_mage.perform_attack()  # Perform attack using mage gear

            # Swap back to melee loadout after the attack
            mager = create_player("Mager", loadouts["melee"])  # Switch back to melee loadout
            attack_handler_mager_melee = AttackHandler(mager, verzik)  # Reset attack handler to melee loadout
        else:
            # Otherwise, use Melee loadout
            player_damage = attack_handler_mager_melee.perform_attack()  # Melee attack
        verzik.take_damage(player_damage)
    else:
        pass
        #print(f"{mager.name} is on cooldown for {mager.attack_cooldown} more ticks.")

    # Ranger attack logic
    if ranger.attack_cooldown == 0:
        if verzik_attacking:
            # Ranger misses the tick if Verzik is attacking on the same tick
            #print(f"{ranger.name} misses the attack due to Verzik attacking on the same tick.")
            ranger.attack_cooldown = 1  # Add a 1-tick cooldown to simulate missing
        else:
            # Ranger attacks as normal
            player_damage_ranger = attack_handler_ranger.perform_attack()
            verzik.take_damage(player_damage_ranger)
    else:
        #print(f"{ranger.name} is on cooldown for {ranger.attack_cooldown} more ticks.")
        pass

    # Decrement the cooldowns for both players
    mager.tick()
    ranger.tick()

    # Verzik's actions
    verzik.simulate_tick(0)

    tick += 1

    if not verzik.is_phase_active():
        print(f"!!! Reds Spawned at tick {tick}!!!")
        print(f"HP Proc: {verzik.hp / verzik.base_hp * 100}%")
