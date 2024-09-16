import random

class Maiden:
    def __init__(self, scale: int):
        """
        Initialize Maiden with a scaling factor that adjusts the health and number of crab spawns.
        scale: int from [1,5]
        """

        # Adjust scaling-dependent variables
        if scale == 5:
            self.max_health = 3500
            self.nylocas_spawn_count = 10
        elif scale == 4:
            self.max_health = 3062
            self.nylocas_spawn_count = 8
        else: 
            self.max_health = 2625
            self.nylocas_spawn_count = 6

        self.current_health = self.max_health
        self.current_phase = 0 # Pre-70s proc
        self.phase_thresholds = [0.7, 0.5, 0.3]
        self.blood_spawns = []
        self.nylocas = []
        self.is_active = True # Fight is active
        self.base_max = 36
        self.attack_speed = 10
        self.available_spawns = list(range(1, 11))  # Positions 1 to 10
        self.position_names = {
            1: "N1", 2: "N2", 3: "N3", 4: "N4a", 5: "N4b",
            6: "S1", 7: "S2", 8: "S3", 9: "S4a", 10: "S4b"
        }

    def take_damage(self, damage):
        """Apply damage to Maiden -- check for reds proc."""
        self.current_health -= damage
        print(f"Maiden has taken {damage}. Current HP: {self.current_health}")

        if self.current_health <= 0:
            self.is_active = False
            print("Maiden dead.")
        else:
            self.check_phase_change()

    def check_phase_change(self):
        """Check if red crabs should be spawning."""
        health_percentage = self.current_health / self.max_health
        if self.current_phase < len(self.phase_thresholds) and health_percentage <= self.phase_thresholds[self.current_phase]:
            self.advance_phase()

    def advance_phase(self):
        """
        Spawn red crabs.
        Phase key:
        0 : Pre-70s
        1 : 70s spawned
        2 : 50s spawned
        3 : 30s spawned
        """
        self.current_phase += 1
        self.available_positions = list(range(1, 11))
        print(f"Maiden has entered phase {self.current_phase}")
        self.spawn_nylocas()
        
    def spawn_nylocas(self):
        """Spawn reds that move towards the boss and heal her if they reach her."""
        spawned_positions = []
        
        for i in range(self.nylocas_spawn_count):
            # Choose a unique position for this phase
            position = random.choice(self.available_positions)
            self.available_positions.remove(position)
            position_name = self.position_names[position]
            spawned_positions.append(position_name)

            nylocas = {
                'position': position,
                'health': 175,  # TODO: CHECK HP
                'moving': True  # TODO: ADD DISTANCES
            }
            self.nylocas.append(nylocas)
        
        # Summary output of all spawns for this phase
        print(f"Nylocas have spawned at positions: {', '.join(spawned_positions)}.")

    def move_nylocas(self):
        """Simulate Nylocas movement towards Maiden."""
        for nylocas in self.nylocas:
            if nylocas['moving']:
                nylocas['position'] -= 1
                print(f"Nylocas from {nylocas['position']} is at DISTANCE.")

            if nylocas['position'] <= 0:
                self.heal_maiden(nylocas['health']*2)
                self.nylocas.remove(nylocas)

    def heal_maiden(self, heal_amount):
        """Heal maiden when a Nylocas reaches her (or blood splat)."""
        self.current_health += heal_amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        print(f"Maiden is healed by {heal_amount}. Current health: {self.current_health}.")

    def attack_player(self, player):
        """Attack a player. Placeholder -- account for prayer."""
        if player.is_praying == True:
            damage = random.randint(0, 0.5*self.max_hit)
        else:
            damage = random.randint(0, self.max_hit)
        print(f"Maiden attacks {player} for {damage} damage.")
        return damage
    
    def spawn_blood_spawn(self, player):
        """Spawn blood near the player."""
        blood_spawn = {
            'target': player.current_position,
            'time_to_disappear': 5 #TODO: Look into this
        }
        self.blood_spawns.append(blood_spawn)
        print(f"Blood spawn targeting player {player}")

    def update_blood_spawn(self):
        """Update all blood spawns, check if they should explode."""
        for spawn in self.blood_spawns:
            spawn['time_to_explode'] -= 1
            if spawn['time_to_explode'] <= 0:
                print(f"Blood spawn at {spawn['target']} exploded.")
                self.blood_spawns.remove(spawn)

maiden = Maiden(scale=3)
maiden.take_damage(310)
maiden.take_damage(310)
maiden.take_damage(310)
maiden.take_damage(310)
maiden.take_damage(310)
maiden.take_damage(310)

