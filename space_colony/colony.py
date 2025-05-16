import random
from models.colonist import Farmer, Scientist, Engineer,Miner
from models.building import Habitat, Farm, Laboratory, Mine,SolarPanel,OxygenGenerator,WaterReclaimer
from models.resource import Water, Food, Materials, Oxygen,Energy
from models.events import MeteorStrike, DustStorm, SupplyDrop, NewColonist, EquipmentMalfunction, DiseaseOutbreak, ResourceDiscovery

class Colony:
    """Represents a space colony with colonists, buildings, and resources."""
    
    def __init__(self,name):
        self._name = name
        self._colonists = []
        self._buildings = []
        self._day = 1
        self._research_points = 0

        # Initialize resources
        self._resources = {
            "Food": Food(quantity=30, production_rate=0),

            "Water": Water(quantity=40, production_rate=0),
            "Materials": Materials(quantity=50, production_rate=0),
            "Oxygen": Oxygen(quantity=20, production_rate=0),
            "Energy": Energy( production_rate=0)
        }
          
        # Initialize events
        self._events = [
            MeteorStrike(),
            DustStorm(),
            SupplyDrop(),
            NewColonist(),
            EquipmentMalfunction(),
            DiseaseOutbreak(),
            ResourceDiscovery()
        ]

        self._setup_initial_colony()
    
    def _setup_initial_colony(self):

        self.add_building(Habitat(capacity=5))
        self.add_building(Farm(size=2))
        self.add_building(Laboratory(size=2))
        self.add_building(Mine(size=2))
        self.add_building(SolarPanel(size=2))
        self.add_building(OxygenGenerator(size=2))
        self.add_building(WaterReclaimer(size=2))

        self.add_colonist(Engineer(name="Alice"))   
        self.add_colonist(Scientist(name="Bob"))
        self.add_colonist(Farmer(name="Charlie"))
        self.add_colonist(Miner(name="David"))


    @property
    def name(self):
        return self._name
    
    @property
    def colonists(self):
        return self._colonists
    
    @property
    def buildings(self):
        return self._buildings
    
    @property
    def resources(self):
        return self._resources
    
    @property
    def day(self):
        return self._day
    
    @property
    def research_points(self):
        return self._research_points
    
    def add_colonist(self, colonist):
        """Add a colonist to the colony."""

        self._colonists.append(colonist)

    def add_building(self, building):
        """Add a new building to the colony.
        
        Args:
            building: Building object to add
        """
        self._buildings.append(building)
        
        # Check if it's a production building that affects resource rates
        resource_mapping = {
            Farm: "Food",
            WaterReclaimer: "Water",
            OxygenGenerator: "Oxygen",
            Mine: "Materials",
            SolarPanel: "Energy"
        }
        
        for building_type, resource_name in resource_mapping.items():
            if isinstance(building, building_type):
                # The building's operate method will handle actual production
                break
    
    def remove_dead_colonists(self):
        """Remove dead colonists from the colony."""
        self._colinists = [c for c in self._colonists if c.is_alive]

    def get_alive_colonists(self):
        """Get a list of alive colonists."""
        return [c for c in self._colonists if c.is_alive]
    
    def advance_day(self):
        """Advance the colony by one day."""
        self._day += 1

        daily_log = [f"=== Day {self._day} ==="]

        self._resources["Energy"].reset_day()

        self._operate_buildings(daily_log)

        self._update_colonists(daily_log)

        spoiled_food = self._resources["Food"].update_day()
        if spoiled_food > 0:
            daily_log.append(f"{spoiled_food} units of food spoiled.")
        
        self._check_random_event(daily_log)

        alive_before = len(self._colonists)
        self.remove_dead_colonists()
        alive_after = len(self._colonists)
        if alive_before != alive_after:
            daily_log.append(f"{alive_before - alive_after} colonists died today.")
        
        return daily_log
    
    def _operate_buildings(self, daily_log):
        """Operate all buildings and update resource production.
        
        Args:
            daily_log: List to append daily messages to
        """
        energy_production = 0

        for building in self._buildings:
            if isinstance(building, SolarPanel) and building.is_operational:
                result = building.operate()
                if result[0] == "energy":
                    energy_production += result[1]
                   
        self._resources["Energy"]._production_rate = energy_production

        daily_log.append(f"Energy production: {energy_production} units.")

        total_energy_needs= sum(b.energy_usage for b in self._buildings if b.is_operational and 
                                not isinstance(b, SolarPanel))
        energy_sufficient = energy_production >= total_energy_needs
        
        if not energy_sufficient:
            daily_log.append(f"WARNING: Energy shortage! Producing {energy_production:.1f} but need {total_energy_needs:.1f}")
        
        production={
            "food": 0,
            "water": 0,
            "oxygen": 0,
            "materials": 0,
            "happiness": 0,
            "research_boost": 0

        }

        for building in self._buildings:
            if isinstance(building,SolarPanel):
                continue

            has_energy = energy_sufficient or random.random() < (energy_production / total_energy_needs)

            building.update_day(energy_available=has_energy)

            if building.is_operational and has_energy:
                result = building.operate()
                if result[0] in production:
                    production[result[0]] += result[1]
                    

        self._resources["Food"]._production_rate = production["food"]
        self._resources["Water"]._production_rate = production["water"]
        self._resources["Oxygen"]._production_rate = production["oxygen"]
        self._resources["Materials"]._production_rate = production["materials"]

         # Actually produce the resources
        for resource in ["Food", "Water", "Oxygen", "Materials"]:
            produced = self._resources[resource].produce()
            if produced > 0:
                daily_log.append(f"{resource} production: {produced:.1f} units")
        
        self._daily_happiness_boost = production["happiness"]
        self._daily_research_boost = production["research_boost"]

    def _update_colonists(self, daily_log):
        """Update colonist status and happiness.
        
        Args:
            daily_log: List to append daily messages to
            """
        
        alive_colonists = self.get_alive_colonists()

        fed_count=0
        for colonist in alive_colonists:
            if colonist.consume_resources(self._resources["Food"], self._resources["Water"]):
                fed_count += 1
            
            colonist.boost_happiness(self._daily_happiness_boost/len(alive_colonists))

        daily_log.append(f"Fed {fed_count}/{len(alive_colonists)} colonists")

        research_points = 0
        maintenance_points = 0

        for colonist in alive_colonists:
            work_results = colonist.work()
            work_type, efficiency = work_results

            if work_type == "research":
                # Apply research boost from labs
                boosted_efficiency = efficiency * (1 + self._daily_research_boost)
                research_points += boosted_efficiency
            elif work_type == "maintenance":
                maintenance_points += efficiency

           
            # Update colonist for the new day
            colonist.update_day()
        
        # Apply research points
        if research_points > 0:
            self._research_points += research_points
            daily_log.append(f"Research conducted: +{research_points:.1f} points")
        
        # Apply maintenance to random buildings
        if maintenance_points > 0 and self._buildings:
            # Prioritize buildings in worse condition
            buildings_to_repair = sorted(self._buildings, key=lambda b: b.condition)[:3]
            repair_per_building = maintenance_points / len(buildings_to_repair)
            
            for building in buildings_to_repair:
                building.repair(repair_per_building)
            
            daily_log.append(f"Maintenance performed on {len(buildings_to_repair)} buildings")

    def _check_random_event(self, daily_log):
        
        if random.random() < 0.15:
            event = random.choice(self._events)
            outcome = event.execute(self)
            daily_log.append(f"EVENT - {event.name}: {outcome}")
    
    def build_new_building(self, building_type,*args):
        """Attempt to build a new building.
        
        Args:6
            building_type: Type of building to construct
            *args: Arguments for building constructor
            
        Returns:
            tuple: (success, message)
        """
        
        cost_mapping = {
            Habitat: 10,
            Farm: 15,
            WaterReclaimer: 20,
            OxygenGenerator: 25,
            SolarPanel: 15,
            Mine: 20,
            Laboratory: 30
        }
        base_cost = cost_mapping.get(building_type, 20)

        # Adjust cost based on size if applicable
        size = args[0] if args else 1
        materials_cost = base_cost * size
        
        # Check if we have enough materials
        if self._resources["Materials"].quantity < materials_cost:
            return (False, f"Not enough materials. Need {materials_cost}, have {self._resources['Materials'].quantity}.")
        
        # Deduct materials
        self._resources["Materials"].consume(materials_cost)
        
        # Create and add the new building
        new_building = building_type(*args)
        self.add_building(new_building)
        
        return (True, f"Successfully built a new {new_building.name}!")
    
    def get_colony_status(self):
        """Get the current status of the colony.
        
        Returns:
            dict: Dictionary with colony status
        """
        status = {
            "alive_colonists": len(self.get_alive_colonists()),
            "avg_health": 0,
            "avg_happiness": 0,
            "habitat_capacity": 0,
        }

        # Get alive colonists
        alive_colonists = self.get_alive_colonists()

        # Calculate average health and happiness
        avg_health = sum(c.health for c in alive_colonists) / len(alive_colonists) if alive_colonists else 0
        avg_happiness = sum(c.happiness for c in alive_colonists) / len(alive_colonists) if alive_colonists else 0

        # Calculate building capacities
        habitat_capacity = sum(b.capacity for b in self._buildings if isinstance(b, Habitat))


        building_counts = {}
        for building in self._buildings:
            building_type = building.__class__.__name__
            if building_type not in building_counts:
                building_counts[building_type] = {"total": 0, "operational": 0}
            
            building_counts[building_type]["total"] += 1
            if building.is_operational:
                building_counts[building_type]["operational"] += 1
        return {
            "day": self._day,
            "colonists": {
                "total": len(self._colonists),
                "alive": len(alive_colonists),
                "avg_health": avg_health,
                "avg_happiness": avg_happiness,
                "habitat_capacity": habitat_capacity
            },
            "resources": {
                "food": {
                    "amount": self._resources["Food"].quantity,
                    "production": self._resources["Food"].production_rate
                },
                "water": {
                    "amount": self._resources["Water"].quantity,
                    "production": self._resources["Water"].production_rate
                },
                "oxygen": {
                    "amount": self._resources["Oxygen"].quantity,
                    "production": self._resources["Oxygen"].production_rate
                },
                "materials": {
                    "amount": self._resources["Materials"].quantity,
                    "production": self._resources["Materials"].production_rate
                },
                "energy": {
                    "production": self._resources["Energy"].production_rate
                }
            },
            "buildings": building_counts,
            "research": self._research_points
        }