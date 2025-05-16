import os
import time
import random
from colony import Colony
from models.building import Habitat, Farm, WaterReclaimer, OxygenGenerator, SolarPanel, Mine, Laboratory
from models.colonist import Engineer, Scientist, Farmer, Miner

class SpaceColonySimulator:
    """Main class for running the Space Colony Simulator."""
    
    def __init__(self):
        self.colony = None
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_separator(self):
        """Print a separator line."""
        print("-" * 60)
    
    def start_new_colony(self):
        """Start a new colony simulation."""
        self.clear_screen()
        print("Welcome to the Space Colony Simulator!")
        self.print_separator()
        
        colony_name = input("Enter a name for your new colony: ")
        self.colony = Colony(colony_name)
        
        print(f"\nColony '{colony_name}' established! You start with basic buildings and 3 colonists.")
        input("Press Enter to continue...")
    
    def display_colony_status(self):
        """Display the current status of the colony."""
        if not self.colony:
            return
            
        self.clear_screen()
        status = self.colony.get_colony_status()
        
        print(f"=== {self.colony.name} Colony - Day {status['day']} ===")
        self.print_separator()
        
        # Display colonist info
        print(f"Colonists: {status['colonists']['alive']}/{status['colonists']['total']} alive " +
              f"(Capacity: {status['colonists']['habitat_capacity']})")
        print(f"Average Health: {status['colonists']['avg_health']:.1f}%")
        print(f"Average Happiness: {status['colonists']['avg_happiness']:.1f}%")
        self.print_separator()
        
        # Display resources
        print("Resources:")
        print(f"Food: {status['resources']['food']['amount']:.1f} " +
              f"(+{status['resources']['food']['production']:.1f}/day)")
        print(f"Water: {status['resources']['water']['amount']:.1f} " +
              f"(+{status['resources']['water']['production']:.1f}/day)")
        print(f"Oxygen: {status['resources']['oxygen']['amount']:.1f} " +
              f"(+{status['resources']['oxygen']['production']:.1f}/day)")
        print(f"Materials: {status['resources']['materials']['amount']:.1f} " +
              f"(+{status['resources']['materials']['production']:.1f}/day)")
        print(f"Energy Production: {status['resources']['energy']['production']:.1f}/day")
        self.print_separator()
        
        # Display buildings
        print("Buildings:")
        for building_type, counts in status['buildings'].items():
            print(f"{building_type}: {counts['operational']}/{counts['total']} operational")
        self.print_separator()
        
        print(f"Research Points: {status['research']:.1f}")
    
    def display_colonists(self):
        """Display detailed information about colonists."""
        if not self.colony:
            return
            
        self.clear_screen()
        print(f"=== Colonists in {self.colony.name} ===")
        self.print_separator()
        
        for i, colonist in enumerate(self.colony.colonists, 1):
            print(f"{i}. {colonist}")
        
        self.print_separator()
        input("Press Enter to return to main menu...")
    
    def display_buildings(self):
        """Display detailed information about buildings."""
        if not self.colony:
            return
            
        self.clear_screen()
        print(f"=== Buildings in {self.colony.name} ===")
        self.print_separator()
        
        for i, building in enumerate(self.colony.buildings, 1):
            print(f"{i}. {building}")
        
        self.print_separator()
        input("Press Enter to return to main menu...")
    
    def build_menu(self):
        """Display the building construction menu."""
        if not self.colony:
            return
            
        self.clear_screen()
        print("=== Build New Structures ===")
        self.print_separator()
        
        print(f"Available Materials: {self.colony.resources['Materials'].quantity}")
        self.print_separator()
        
        building_options = [
            ("Habitat (10 materials per capacity)", Habitat, "capacity"),
            ("Farm (15 materials per size)", Farm, "size"),
            ("Water Reclaimer (20 materials per size)", WaterReclaimer, "size"),
            ("Oxygen Generator (25 materials per size)", OxygenGenerator, "size"),
            ("Solar Panel (15 materials per size)", SolarPanel, "size"),
            ("Mine (20 materials per size)", Mine, "size"),
            ("Laboratory (30 materials per size)", Laboratory, "size")
        ]
        
        for i, (name, _, _) in enumerate(building_options, 1):
            print(f"{i}. {name}")
        
        print("0. Return to main menu")
        self.print_separator()
        
        choice = input("Enter your choice (0-7): ")
        if not choice.isdigit() or int(choice) < 0 or int(choice) > 7:
            return
            
        choice = int(choice)
        if choice == 0:
            return
            
        # Get building details
        _, building_class, param_name = building_options[choice - 1]
        
        param_value = input(f"Enter {param_name} (1-10): ")
        if not param_value.isdigit() or int(param_value) < 1 or int(param_value) > 10:
            print("Invalid input. Construction canceled.")
            input("Press Enter to continue...")
            return
            
        param_value = int(param_value)
        
        # Try to build
        success, message = self.colony.build_new_building(building_class, param_value)
        print(message)
        input("Press Enter to continue...")
    
    def advance_day(self):
        """Advance the simulation by one day."""
        if not self.colony:
            return
            
                        git init
            git add .
            git commit -m "Initial commit"
            git branch -M main
            git remote add origin {your_github_repo_url}
            git push -u origin main
        self.clear_screen()
        print(f"Advancing to day {self.colony.day + 1}...")
        time.sleep(1)
        
        # Get daily log
        daily_log = self.colony.advance_day()
        
        # Display log
        self.clear_screen()
        print("\n".join(daily_log))
        self.print_separator()
        input("Press Enter to continue...")
    
    def auto_advance(self):
        """Automatically advance multiple days."""
        if not self.colony:
            return
            
        self.clear_screen()
        days = input("How many days to simulate automatically? (1-30): ")
        if not days.isdigit() or int(days) < 1 or int(days) > 30:
            print("Invalid input.")
            input("Press Enter to continue...")
            return
            
        days = int(days)
        
        self.clear_screen()
        print(f"Auto-advancing {days} days...")
        time.sleep(1)
        
        for _ in range(days):
            self.colony.advance_day()
            # Slight pause to make it look like computation is happening
            time.sleep(0.1)
        
        print(f"Advanced {days} days successfully.")
        input("Press Enter to continue...")
    
    def run(self):
        """Run the main simulation loop."""
        if not self.colony:
            self.start_new_colony()
        
        while True:
            self.display_colony_status()
            self.print_separator()
            
            print("\nMain Menu:")
            print("1. View Colonists")
            print("2. View Buildings")
            print("3. Build New Structure")
            print("4. Advance One Day")
            print("5. Auto-advance Multiple Days")
            print("6. Start New Colony")
            print("0. Exit")
            
            choice = input("\nEnter your choice (0-6): ")
            
            if choice == "1":
                self.display_colonists()
            elif choice == "2":
                self.display_buildings()
            elif choice == "3":
                self.build_menu()
            elif choice == "4":
                self.advance_day()
            elif choice == "5":
                self.auto_advance()
            elif choice == "6":
                self.start_new_colony()
            elif choice == "0":
                self.clear_screen()
                print("Thanks for playing Space Colony Simulator!")
                break
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)


if __name__ == "__main__":
    simulator = SpaceColonySimulator()
    simulator.run()