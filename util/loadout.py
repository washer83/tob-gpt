from Player import Player, PlayerStats, AttackStyle

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
