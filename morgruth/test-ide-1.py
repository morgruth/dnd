import random
import time

class FortMorgruthMiningOS:
    def __init__(self):
        # Current Inventory levels
        self.inventory = {
            "Aether-Grain (Food)": 6224.0,
            "Shadow-Oak (Wood)": 2156.4,
            "Obsidian Shards": 359.4,
            "Shadow-Iron Ore": 436.8,
            "Static Essence": 23.09,
            "Aether Crystals": 9.8
        }
        
        self.bank_balance = 10000.0  # Liquid Gold
        self.aether_credits = 1500.0 # Planar currency
        
        # MARKET PRICES (GP per unit)
        self.market_prices = {
            "Aether-Grain (Food)": 0.5,
            "Shadow-Oak (Wood)": 1.2,
            "Obsidian Shards": 5.0,
            "Shadow-Iron Ore": 8.0
        }
        
        self.extraction_active = True
        self.efficiency_modifier = 1.2 

    def run_trade_caravan(self):
        """Automatically sells surplus food (above 5000 units) for Gold."""
        if self.inventory["Aether-Grain (Food)"] > 5000:
            surplus = self.inventory["Aether-Grain (Food)"] - 5000
            earnings = surplus * self.market_prices["Aether-Grain (Food)"]
            self.inventory["Aether-Grain (Food)"] = 5000
            self.bank_balance += earnings
            print(f"[TRADE] Caravan Departed: Sold {surplus} Food for {earnings} GP.")

    def run_extraction_cycle(self):
        print("--- INITIALIZING BANKING & EXTRACTION: FORT MORGRUTH ---")
        print(f"Bank Balance: {self.bank_balance} GP | Credits: {self.aether_credits}")
        print("Processing Trade Routes... Press Ctrl+C to stop.\n")
        
        try:
            while self.extraction_active:
                roll = random.random()
                
                # Resource Spawning (Same logic as before)
                if roll < 0.30:
                    found = "Aether-Grain (Food)"
                    amount = random.randint(20, 50)
                elif roll < 0.55:
                    found = "Shadow-Oak (Wood)"
                    amount = random.randint(15, 35)
                # ... [Internal mining logic continues] ...
                else:
                    found = "Aether Crystals"
                    amount = 1
                
                # Apply extraction
                final_amount = round(amount * self.efficiency_modifier, 2)
                self.inventory[found] = round(self.inventory[found] + final_amount, 2)
                
                # Check for Trade Opportunities every pulse
                if random.random() > 0.8: # 20% chance for a merchant visit
                    self.run_trade_caravan()
                
                print(f"[LOG] {found}: +{final_amount} | Total: {self.inventory[found]}")
                time.sleep(1.5)
                
        except KeyboardInterrupt:
            self.generate_report()

    def generate_report(self):
        print("\n" + "="*55)
        print(f"SOVEREIGN BANK TOTAL: {self.bank_balance} GP")
        print("-" * 55)
        for item, count in self.inventory.items():
            print(f"{item:<20} | {count:>10}")
        print("="*55)

if __name__ == "__main__":
    miner = FortMorgruthMiningOS()
    miner.run_extraction_cycle()