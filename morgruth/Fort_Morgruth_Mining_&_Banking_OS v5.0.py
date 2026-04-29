import random
import time
import sys

class FortMorgruthOS:
    def __init__(self):
        # Current Global Ledger State
        self.inventory = {
            "Aether-Grain (Food)": 5000.0,
            "Shadow-Oak (Wood)": 2780.4,
            "Obsidian Shards": 359.4,
            "Shadow-Iron Ore": 436.8,
            "Static Essence": 23.09,
            "Aether Crystals": 51.8
        }
        
        self.bank_gp = 11012.80    # Liquid Gold
        self.aether_credits = 1500.0 # Planar Credits
        
        self.market_prices = {
            "Aether-Grain (Food)": 0.5,
            "Shadow-Oak (Wood)": 1.2,
            "Obsidian Shards": 5.0,
            "Shadow-Iron Ore": 8.0,
            "Aether Crystals": 100.0
        }
        
        self.efficiency = 1.2 # Catalyst Modifier
        self.running = True

    def run_trade_caravan(self):
        """Logic for automatic surplus liquidation"""
        # Food Stabilization
        if self.inventory["Aether-Grain (Food)"] > 5000:
            surplus = self.inventory["Aether-Grain (Food)"] - 5000
            profit = round(surplus * self.market_prices["Aether-Grain (Food)"], 2)
            self.bank_gp += profit
            self.inventory["Aether-Grain (Food)"] = 5000.0
            print(f">>> [TRADE] Caravan: Sold {round(surplus, 1)} Food for {profit} GP.")

        # Crystal Overflow Safeguard
        if self.inventory["Aether Crystals"] > 60:
            export_count = 10
            profit = export_count * self.market_prices["Aether Crystals"]
            self.inventory["Aether Crystals"] -= export_count
            self.bank_gp += profit
            print(f">>> [BANK] Rare Trade: Exported {export_count} Crystals for {profit} GP.")

    def convert_currency(self):
        """10 GP : 1 AC Conversion Logic"""
        print(f"\n--- Planar Exchange ---")
        print(f"Current Gold: {self.bank_gp} GP")
        try:
            amount = float(input("Enter Gold amount to convert to Aether-Credits: "))
            if amount <= self.bank_gp:
                self.bank_gp -= amount
                added_ac = amount / 10
                self.aether_credits += added_ac
                print(f"Success: Added {added_ac} AC to Planar Account.")
            else:
                print("Error: Insufficient Gold reserves.")
        except ValueError:
            print("Invalid input.")

    def main_menu(self):
        while True:
            print("\n" + "="*30)
            print(" FORT MORGRUTH: SOVEREIGN OS")
            print("="*30)
            print(f"1. Start Extraction Cycle")
            print(f"2. View Sovereign Ledger")
            print(f"3. Planar Exchange (GP -> AC)")
            print(f"4. Exit System")
            
            choice = input("\nSelect Command: ")
            
            if choice == "1":
                self.run_extraction()
            elif choice == "2":
                self.generate_report()
            elif choice == "3":
                self.convert_currency()
            elif choice == "4":
                print("Vaults Sealed. Farewell, Morgruth.")
                sys.exit()

    def run_extraction(self):
        print("\n--- Cycle Started (Press Ctrl+C to stop) ---")
        try:
            while True:
                roll = random.random()
                if roll < 0.30: found = "Aether-Grain (Food)"; amount = random.randint(20, 50)
                elif roll < 0.55: found = "Shadow-Oak (Wood)"; amount = random.randint(15, 35)
                elif roll < 0.75: found = "Obsidian Shards"; amount = random.randint(5, 15)
                elif roll < 0.90: found = "Shadow-Iron Ore"; amount = random.randint(3, 8)
                elif roll < 0.97: found = "Static Essence"; amount = random.uniform(0.5, 2.0)
                else: found = "Aether Crystals"; amount = 1
                
                gain = round(amount * self.efficiency, 2)
                self.inventory[found] = round(self.inventory[found] + gain, 2)
                
                print(f"[LOG] {found}: +{gain} | Total: {self.inventory[found]}")
                
                if random.random() > 0.8:
                    self.run_trade_caravan()
                
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nCycle Paused.")

    def generate_report(self):
        print("\n" + "-"*45)
        print(f"{'SOVEREIGN BANK ACCOUNTS':^45}")
        print("-" * 45)
        print(f"Liquid Gold (GP):     {round(self.bank_gp, 2):>15}")
        print(f"Planar Credits (AC):  {round(self.aether_credits, 2):>15}")
        print("-" * 45)
        for item, count in self.inventory.items():
            print(f"{item:<25} | {count:>15}")
        print("-" * 45)

if __name__ == "__main__":
    system = FortMorgruthOS()
    system.main_menu()