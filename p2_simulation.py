import random
from Player import Player
from VerzikP2 import VerzikP2
from util.attack_handler import AttackHandler
from util.loadout import default_loadouts, create_player, switch_player_to_loadout

# -------------------------------
# 1. Load default loadouts, create players
# -------------------------------
loadouts = default_loadouts()
debug_statements = False

# Create your two players using desired default loadouts:
# Suppose "mager" is *normally* on a Melee loadout (Scythe),
# but can switch to "Tumeken's shadow" as needed.
mager = create_player("Mager", loadouts["melee"])  # Start with melee gear
ranger = create_player("Ranger", loadouts["melee"])

mager_total_dmg, ranger_total_dmg = 0, 0

# -------------------------------
# 2. Initialize Verzik P2, scale=2
# -------------------------------
verzik = VerzikP2(scale=2)
verzik.attacks_since_last_crab = 20  # So the crab can spawn quickly

# -------------------------------
# 3. Attack Handlers
# -------------------------------
attack_handler_mager = AttackHandler(mager, verzik)
attack_handler_ranger = AttackHandler(ranger, verzik)

# Randomly select crab-popper
popper = ranger

# -------------------------------
# 4. Simulation Loop
# -------------------------------
tick = 0
while verzik.is_phase_active():
    print(f"{tick}: VERZIK_HP {verzik.hp}") if debug_statements else None
    
    # We'll aggregate total damage this tick in queued_dmg
    # so we can apply it all at once to Verzik before simulate_tick
    queued_dmg = 0
    
    # Check if Verzik is about to do an attack this tick
    verzik_attacking = (verzik.ticks_since_last_attack == verzik.attack_cooldown_ticks)
    
    # -------------------------------
    # 4a. Handle Purple Crab popping
    # -------------------------------
    if verzik.purple_crab_active and verzik.purple_crab_ticks_alive > 10:        
        if popper.attack_cooldown == 0:
            if popper.name == "Ranger":
                switch_player_to_loadout(popper, loadouts["range_bp"])
            if popper.name == "Mager":
                switch_player_to_loadout(popper, loadouts["mage_bp"])
            
            print("Attempting to pop the crab.") if debug_statements else None
            attack_handler_popper = AttackHandler(popper, verzik)
            attack_handler_popper.perform_attack()
            switch_player_to_loadout(popper, loadouts["melee"])
            popper.attack_cooldown = popper.attack_cooldown - 1
            popper.tick()
        else:
            print(f"POPPER COOLDOWN: {popper.attack_cooldown}") if debug_statements else None
            popper.tick()
    
    # -------------------------------
    # 4b. Mager Attack Logic
    # -------------------------------
    else:
        # If mager's cooldown is ready
    # For Mager
        if mager.attack_cooldown == 0:
            if verzik_attacking:
                # Switch to Shadow loadout for a guaranteed mage hit
                switch_player_to_loadout(mager, loadouts["mage_7_way"])
                mager_dmg = attack_handler_mager.perform_attack()
                queued_dmg += mager_dmg
                mager_total_dmg += mager_dmg
                print(f"    MAGER ATTACKED USING {mager.gear.get('weapon')} FOR {mager_dmg} DAMAGE...") if debug_statements else None
                # Switch back to melee if you want
                switch_player_to_loadout(mager, loadouts["melee"])
            else:
                # Just do scythe
                mager_dmg = attack_handler_mager.perform_attack()
                queued_dmg += mager_dmg
                mager_total_dmg += mager_dmg
                print(f"    MAGER ATTACKED USING {mager.gear.get('weapon')} FOR {mager_dmg} DAMAGE...") if debug_statements else None
        

    
        # -------------------------------
        # 4c. Ranger Attack Logic
        # -------------------------------
        if ranger.attack_cooldown == 0:
            if verzik_attacking:
                # The ranger "misses" if Verzik is attacking. 
                # If you want to forcibly skip the attack, you can do:
                #print("Ranger missed due to Verzik's attack this tick.")
                # Just set some small cooldown so they skip this tick
                print("     RANGER MISSING TICK.") if debug_statements else None
                ranger.attack_cooldown = 2
            else:
                ranger_dmg = attack_handler_ranger.perform_attack()
                queued_dmg += ranger_dmg
                ranger_total_dmg += ranger_dmg
                print(f"    RANGER ATTACKED USING {ranger.gear.get('weapon')} for {ranger_dmg} DAMAGE...") if debug_statements else None
        
        mager.tick()
        ranger.tick()  # Decrement ranger's cooldown

    
    # -------------------------------
    # 4d. Apply all queued damage to Verzik
    # -------------------------------
    #if queued_dmg > 0:
    #    verzik.take_damage(queued_dmg)
    #    print(f"Verzik took {queued_dmg} damage. Current HP: {verzik.hp}")
    
    # -------------------------------
    # 4e. Verzik's turn to act
    # -------------------------------
    verzik.simulate_tick(queued_dmg)
    tick += 1
    
    # Check if Verzik is done
    if not verzik.is_phase_active():
        print(f"!!! Reds spawned at tick {tick} !!!")
        print(f"HP Proc: {round(verzik.hp / verzik.base_hp * 100, 2)}%")
        print(f"MAGER: {mager_total_dmg} | RANGER: {ranger_total_dmg}")