from Player import Player, PlayerStats, AttackStyle
from Prayer import PRAYERS

def default_loadouts():
    loadouts = {
        "mage_8_way": {
            "stats": PlayerStats(attack=118, strength=118, defense=118, magic=112, ranged=112, hp=121),
            "prayer": "Augury",
            "attack_style": AttackStyle.LONGRANGE,  
            "offensive_stat": "magic",            
            "gear": [
                "Tumeken's shadow", 
                "Ancestral hat", 
                "Ancestral robe top", 
                "Ancestral robe bottom",
                "Occult necklace", 
                "Tormented bracelet", 
                "Primordial boots", 
                "Magus ring", 
                "Imbued zamorak cape"
            ]
        },
        "mage_7_way": {
            "stats": PlayerStats(attack=118, strength=118, defense=118, magic=112, ranged=112, hp=121),
            "prayer": "Augury",
            "attack_style": AttackStyle.LONGRANGE,  
            "offensive_stat": "magic",            
            "gear": [
                "Tumeken's shadow", 
                "Ancestral hat", 
                "Ancestral robe top", 
                "Ancestral robe bottom",
                "Occult necklace", 
                "Tormented bracelet", 
                "Primordial boots", 
                "Ultor ring", 
                "Imbued zamorak cape"
            ]
        },
        "mage_6_way": {
            "stats": PlayerStats(attack=118, strength=118, defense=118, magic=112, ranged=112, hp=121),
            "prayer": "Augury",
            "attack_style": AttackStyle.LONGRANGE,  
            "offensive_stat": "magic",            
            "gear": [
                "Tumeken's shadow", 
                "Ancestral hat", 
                "Ancestral robe top", 
                "Ancestral robe bottom",
                "Occult necklace", 
                "Tormented bracelet", 
                "Primordial boots", 
                "Ultor ring", 
                "Infernal cape"
            ]
        },
        "mage_bp": {
            "stats": PlayerStats(attack=118, strength=118, defense=118, magic=112, ranged=99, hp=121),
            "prayer": "Augury",
            "attack_style": AttackStyle.RAPID,  
            "offensive_stat": "ranged",            
            "gear": [
                "Toxic blowpipe", 
                "Torva full helm", 
                "Torva platebody", 
                "Torva platelegs",
                "Amulet of rancour", 
                "Tormented bracelet", 
                "Primordial boots", 
                "Ultor ring", 
                "Infernal cape"
            ]
        },
        "range_bp": {
            "stats": PlayerStats(attack=118, strength=118, defense=118, magic=112, ranged=99, hp=121),
            "prayer": "Piety",
            "attack_style": AttackStyle.RAPID,  
            "offensive_stat": "ranged",            
            "gear": [
                "Toxic blowpipe", 
                "Torva full helm", 
                "Torva platebody", 
                "Torva platelegs",
                "Necklace of anguish", 
                "Void knight gloves", 
                "Primordial boots", 
                "Ultor ring", 
                "Infernal cape"
            ]
        },
        "melee": {
            "stats": PlayerStats(attack=118, strength=118, defense=118, magic=112, ranged=112, hp=121),
            "prayer": "Piety",
            "attack_style": AttackStyle.AGGRESSIVE,  
            "offensive_stat": "slash",              
            "gear": [
                "Scythe of vitur", 
                "Torva full helm", 
                "Torva platebody", 
                "Torva platelegs",
                "Amulet of rancour", 
                "Ferocious gloves", 
                "Primordial boots", 
                "Ultor ring", 
                "Infernal cape"
            ]
        },
        "melee_bf": {
            "stats": PlayerStats(attack=118, strength=118, defense=118, magic=112, ranged=112, hp=121),
            "prayer": "Piety",
            "attack_style": AttackStyle.AGGRESSIVE,  
            "offensive_stat": "slash",              
            "gear": [
                "Scythe of vitur", 
                "Torva full helm", 
                "Torva platebody", 
                "Torva platelegs",
                "Amulet of fury", 
                "Ferocious gloves", 
                "Primordial boots", 
                "Ultor ring", 
                "Infernal cape"
            ]
        },
    }
    return loadouts

def switch_player_to_loadout(player, loadout):
    """
    Switch an existing Player object to the new loadout
    without losing ephemeral data like HP, cooldowns, special attack, etc.
    """
    # 1) Store ephemeral data you don’t want to lose
    #old_hp = player.hp
    old_special = player.special_attack_energy
    old_cooldown = player.attack_cooldown

    # 2) Unequip all currently worn gear
    slots_to_remove = list(player.gear.keys())  # Copy keys because we modify dict
    for slot in slots_to_remove:
        player.unequip_item(slot)

    # 3) Apply the new loadout’s stats, prayer, style, etc.
    #    If you don’t want to override PlayerStats (e.g., if you have potions/overloads),
    #    you can skip this step or partially apply it.
    player.stats = loadout["stats"]

    # Switch to the loadout’s prayer (if it exists in PRAYERS)
    player.prayer_active = PRAYERS.get(loadout["prayer"])

    # Set new attack style / offensive stat
    player.attack_style = loadout["attack_style"]
    player.offensive_stat = loadout["offensive_stat"]

    # 4) Equip the new gear
    for item_name in loadout["gear"]:
        player.equip_item(item_name)

    # 5) Restore ephemeral data
    #player.hp = old_hp
    player.special_attack_energy = old_special
    player.attack_cooldown = old_cooldown
    # If you track prayer points, reassign them here too
    # player.prayer_points = old_prayer_points

# Function to create a player based on loadout
def create_player(name, loadout):
    player = Player(
        name=name, 
        stats=loadout["stats"], 
        attack_style=loadout["attack_style"],  # Flexible attack style
        offensive_stat=loadout["offensive_stat"],  # Flexible offensive stat
        prayer_name=loadout["prayer"]
    )
    for item in loadout["gear"]:
        player.equip_item(item)
    return player
