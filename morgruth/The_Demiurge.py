import random
import time
import sys

class CosmologicalEngine:
    def __init__(self):
        # --- UNIVERSAL CONSTANTS ---
        self.constants = {
            "Efficiency": 1.2,    # The Catalyst Modifier
            "Entropy": 0.001,     # Natural decay of resources
            "Planar_Focus": 1.0,  # Multiplier for high-tier yields
            "GP_to_AC_Rate": 10   # The Golden Ratio
        }

        # --- THE SOVEREIGN LEDGER (THE MATERIAL PLANE) ---
        self.vault = {
            "GP": 10134.6,
            "AC": 1600.0,
            "Aether-Grain": 5000.0,
            "Shadow-Oak": 2914.8,
            "Obsidian": 473.4,
            "Iron-Ore": 487.2,
            "Static-Essence": 27.03,
            "Aether-Crystals": 51.8
        }

        # --- COSMIC STATE ---
        self.universe_age = 0 # Measured in Cycles
        self.active = True

    def apply_entropy(self):
        """Simulates the natural decay of the universe."""
        for resource in ["Aether-Grain", "Shadow-Oak"]:
            loss = self.vault[resource] * self.constants["Entropy"]
            self.vault[resource] -= round(loss, 2)

    def trigger_cosmic_event(self):
        """Random Planar shifts that affect the universe."""
        events = [
            ("Supernova", "Static-Essence", 5.0),
            ("Rift Collapse", "Obsidian", -10.0),
            ("Aether Storm", "Aether-Crystals", 2.0),
            ("Merchant Nebula", "GP", 500.0)
        ]
        if random.random() > 0.95:
            event, res, change = random.choice(events)
            self.vault[res] = round(max(0, self.vault[res] + change), 2)
            print(f"!!! [COSMOS] {event}: {res} affected by {change}")

    def run_universe_cycle(self):
        """The heartbeat of the universe."""
        print("\n--- UNIVERSE INITIALIZED: FABRIC OF MORGRUTH ACTIVE ---")
        try:
            while self.active:
                self.universe_age += 1
                
                # 1. Harvest local reality
                gain = random.uniform(5, 15) * self.constants["Efficiency"]
                self.vault["Aether-Grain"] += round(gain, 2)
                
                # 2. Process Trade (The Law of Balance)
                if self.vault["Aether-Grain"] > 5000:
                    surplus = self.vault["Aether-Grain"] - 5000
                    self.vault["GP"] += round(surplus * 0.5, 2)
                    self.vault["Aether-Grain"] = 5000.0
                
                # 3. Apply Entropy & Events
                self.apply_entropy()
                self.trigger_cosmic_event()

                # 4. Output Reality State
                print(f"[Cycle {self.universe_age}] Gold: {self.vault['GP']} | Credits: {self.vault['AC']} | Essence: {self.vault['Static-Essence']}")
                time.sleep(0.8)
                
        except KeyboardInterrupt:
            print("\nUniverse Suspended in Stasis.")

    def menu(self):
        while True:
            print("\n" + "∞"*30)
            print("  MORGRUTH COSMOLOGICAL ENGINE")
            print("∞"*30)
            print("1. Pulse the Universe (Start Cycles)")
            print("2. View Universal Ledger")
            print("3. Modify Constants (Alter Reality)")
            print("4. Collapse Universe (Exit)")
            
            choice = input("\nAction: ")
            if choice == "1": self.run_universe_cycle()
            elif choice == "2": self.show_ledger()
            elif choice == "3": self.alter_reality()
            elif choice == "4": break

    def show_ledger(self):
        print(f"\n--- Ledger at Cycle {self.universe_age} ---")
        for k, v in self.vault.items():
            print(f"{k:<15} : {v}")

    def alter_reality(self):
        print("\n--- Current Constants ---")
        for k, v in self.constants.items(): print(f"{k}: {v}")
        target = input("Which constant to alter? ")
        if target in self.constants:
            try:
                self.constants[target] = float(input(f"New value for {target}: "))
            except: print("Invalid calculation.")

if __name__ == "__main__":
    engine = CosmologicalEngine()
    engine.menu()