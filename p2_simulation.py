from Player import *
from VerzikP2 import VerzikP2
from util.attack_handler import AttackHandler

player_stats = PlayerStats(attack=118, strength=118, defense=118, magic=112, ranged=112, hp=121)

player = Player(name="TestPlayer", 
                stats=player_stats, 
                attack_style=AttackStyle.ACCURATE, 
                offensive_stat="magic", 
                prayer_name="Augury")

player.equip_item("Tumeken's shadow")
player.equip_item("Ancestral hat")
player.equip_item("Ancestral robe top")
player.equip_item("Ancestral robe bottom")
player.equip_item("Occult necklace")
player.equip_item("Tormented bracelet")
player.equip_item("Eternal boots")
player.equip_item("Magus ring")
player.equip_item("Imbued zamorak cape")

verzik = VerzikP2(scale=3)

attack_handler = AttackHandler(player, verzik)

#sim 
tick = 0
while verzik.is_phase_active():
    print(f"Tick {tick + 1}:")
    
    # Player can attack if not on cooldown
    if player.attack_cooldown == 0:
        player_damage = attack_handler.perform_attack()
        verzik.take_damage(player_damage)
    else:
        print(f"{player.name} is on cooldown for {player.attack_cooldown} more ticks.")
    
    # Decrement cooldown and check other player states
    player.tick()

    # Verzik's actions
    verzik.simulate_tick(0)

    tick += 1

    if not verzik.is_phase_active():
        print("!!! Reds Spawned!!!\n")
        print(f"HP Proc: {verzik.hp / verzik.base_hp * 100}%")