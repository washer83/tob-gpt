class Prayer:
    def __init__(self, name: str, 
                 attack_bonus: float = 0.0, strength_bonus: float = 0.0, defense_bonus: float = 0.0, 
                 ranged_bonus: float = 0.0, ranged_str_bonus: float = 0.0, ranged_def_bonus: float = 0.0, 
                 magic_bonus: float = 0.0, magic_damage_bonus: float = 0.0, magic_def_bonus: float = 0.0):
        self.name = name
        self.attack_bonus = attack_bonus
        self.strength_bonus = strength_bonus
        self.defense_bonus = defense_bonus
        self.ranged_bonus = ranged_bonus
        self.ranged_str_bonus = ranged_str_bonus
        self.ranged_def_bonus = ranged_def_bonus
        self.magic_bonus = magic_bonus
        self.magic_damage_bonus = magic_damage_bonus
        self.magic_def_bonus = magic_def_bonus

PRAYERS = {
    "Piety": Prayer(name="Piety", attack_bonus=0.20, strength_bonus=0.23, defense_bonus=0.25),
    "Chivalry": Prayer(name="Chivalry", attack_bonus=0.15, strength_bonus=0.18, defense_bonus=0.20),
    "Rigour": Prayer(name="Rigour", ranged_bonus=0.20, ranged_str_bonus=0.23, defense_bonus=0.25),
    "Augury": Prayer(name="Augury", magic_bonus=0.25, magic_damage_bonus=0.04, magic_def_bonus=0.25),
    "None": Prayer(name="None")
}