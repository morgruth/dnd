import random
import time

class FortMorgruthMiningOS:
    def __init__(self):
        # Initializing the World Ledger with the resources from your Book of Records
        self.inventory = {
            "Aether-Grain (Food)": 5000,
            "Shadow-Oak (Wood)": 1200,
            "Obsidian Shards": 150,
            "Shadow-Iron Ore": 300,
            "Static Essence": 10.0,
            "Aether Crystals": 5
        }
        self.extraction_active = True
        self.efficiency_modifier = 1.2  # The Catalyst of Spires Bonus

    def run_extraction_cycle(self):
        print("--- INITIALIZING WORLD EXTRACTION: FORT MORGRUTH ---")
        print(f"Status: Catalyst Presence Detected. Efficiency: {self.efficiency_modifier*100}%")
        print("Press Ctrl+C to stop the extraction and generate the Final Ledger.\n")
        
        try:
            while self.extraction_active:
                roll = random.random()
                
                # Logic for Resource Spawning (Sorted by rarity)
                if roll < 0.30:
                    found = "Aether-Grain (Food)"
                    amount = random.randint(20, 50)
                elif roll < 0.55:
                    found = "Shadow-Oak (Wood)"
                    amount = random.randint(15, 35)
                elif roll < 0.75:
                    found = "Obsidian Shards"
                    amount = random.randint(5, 15)
                elif roll < 0.90:
                    found = "Shadow-Iron Ore"
                    amount = random.randint(3, 8)
                elif roll < 0.97:
                    found = "Static Essence"
                    amount = random.uniform(0.5, 2.0)
                else:
                    found = "Aether Crystals"
                    amount = 1
                
                # Apply the Catalyst bonus and update the inventory
                final_amount = round(amount * self.efficiency_modifier, 2)
                self.inventory[found] += final_amount
                
                # Real-time console update
                prefix = "[HARVEST]" if "Food" in found or "Wood" in found else "[MINING]"
                print(f"{prefix} {found}: +{final_amount}")
                
                # Short delay to simulate the Rift's pulse
                time.sleep(1.5)
                
        except KeyboardInterrupt:
            self.generate_report()

    def generate_report(self):
        print("\n" + "="*40)
        print("       OFFICIAL WORLD INVENTORY LEDGER")
        print("="*40)
        for item, count in self.inventory.items():
            # Formatting for clean reading
            print(f"{item:<20} | {count:>10}")
        print("="*40)
        print("Status: Goods secured in the Vaults of Fort Morgruth.")
        print("The Catalyst's reach expands.")

# Execution
if __name__ == "__main__":
    miner = FortMorgruthMiningOS()
    miner.run_extraction_cycle()