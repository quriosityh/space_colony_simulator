import random
from abc import ABC, abstractmethod

class Event(ABC):
    """Abstract base class for random events."""
    
    def __init__(self, name, description):
        self._name = name
        self._description = description
    
    @property
    def name(self):
        """Get event name."""
        return self._name
    
    @property
    def description(self):
        """Get event description."""
        return self._description
    
    @abstractmethod
    def execute(self, colony):
        """Execute event effects on the colony.
        
        Args:
            colony: Colony object to affect
            
        Returns:
            str: Outcome description
        """
        pass
    
    def __str__(self):
        """String representation of the event."""
        return f"{self._name}: {self._description}"


class MeteorStrike(Event):
    """Meteor strikes a random building."""
    
    def __init__(self):
        super().__init__(
            "Meteor Strike",
            "A meteor has struck your colony!"
        )
    
    def execute(self, colony):
        """Damage a random building."""
        if not colony.buildings:
            return "No buildings were damaged as your colony has no structures."
        
        building = random.choice(colony.buildings)
        damage = random.randint(20, 50)
        
        # Apply damage to building condition
        old_condition = building.condition
        building._condition = max(0, building.condition - damage)
        
        if building.condition <= 20 and old_condition > 20:
            return f"A meteor struck your {building.name}! It took {damage}% damage and is now non-operational."
        else:
            return f"A meteor struck your {building.name}! It took {damage}% damage but remains operational."


class DustStorm(Event):
    """Dust storm affects solar panels and colonist happiness."""
    
    def __init__(self):
        super().__init__(
            "Dust Storm",
            "A powerful dust storm is sweeping through the colony!"
        )
    
    def execute(self, colony):
        """Reduce solar panel output and colonist happiness."""
        results = []
        
        # Affect solar panels
        solar_panel_count = 0
        for building in colony.buildings:
            if isinstance(building, SolarPanel):
                solar_panel_count += 1
                # Temporarily reduce efficiency by adding dust
                building._condition = max(30, building.condition - 15)
        
        if solar_panel_count > 0:
            results.append(f"{solar_panel_count} solar panels were covered with dust, reducing efficiency.")
        
        # Affect colonist happiness
        living_colonists = [c for c in colony.colonists if c.is_alive]
        for colonist in living_colonists:
            colonist._happiness = max(0, colonist.happiness - 10)
        
        if living_colonists:
            results.append(f"The storm has decreased morale among {len(living_colonists)} colonists.")
        
        return " ".join(results) if results else "The dust storm passed without significant effect."


class SupplyDrop(Event):
    """Supply ship delivers resources."""
    
    def __init__(self):
        super().__init__(
            "Supply Drop",
            "A supply ship from Earth has arrived with resources!"
        )
    
    def execute(self, colony):
        """Add random resources to colony."""
        # Determine what resources to add
        food_amount = random.randint(20, 50)
        water_amount = random.randint(15, 40)
        materials_amount = random.randint(10, 30)
        
        # Add resources
        colony.resources["Food"]._quantity += food_amount
        colony.resources["Water"]._quantity += water_amount
        colony.resources["Materials"]._quantity += materials_amount
        
        # Boost colonist happiness
        for colonist in colony.colonists:
            if colonist.is_alive:
                colonist._happiness = min(100, colonist.happiness + 15)
        
        return f"Supply drop received! Added {food_amount} Food, {water_amount} Water, and {materials_amount} Materials. Colonist morale improved."


class NewColonist(Event):
    """A new colonist arrives at the colony."""
    
    def __init__(self):
        super().__init__(
            "New Arrival",
            "A new colonist has arrived from Earth!"
        )
        self._specializations = ["Engineer", "Scientist", "Farmer", "Miner"]
        self._names = [
            "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", 
            "Quinn", "Dakota", "Reese", "Skyler", "Finley", "Sage", "Blair"
        ]
    
    def execute(self, colony):
        """Add a new colonist to the colony."""
        # Check habitat capacity
        total_capacity = sum(b.capacity for b in colony.buildings if isinstance(b, Habitat))
        current_colonists = len(colony.colonists)
        
        if current_colonists >= total_capacity:
            return "A new colonist arrived but had to be turned away due to insufficient habitat space."
        
        # Create random colonist
        specialization = random.choice(self._specializations)
        name = random.choice(self._names)
        
        # Add appropriate colonist type based on specialization
        if specialization == "Engineer":
            colonist = Engineer(name)
        elif specialization == "Scientist":
            colonist = Scientist(name)
        elif specialization == "Farmer":
            colonist = Farmer(name)
        else:  # Miner
            colonist = Miner(name)
        
        colony.add_colonist(colonist)
        return f"{name} the {specialization} has joined your colony!"


class EquipmentMalfunction(Event):
    """Critical equipment malfunction in a random building."""
    
    def __init__(self):
        super().__init__(
            "Equipment Malfunction",
            "Critical equipment malfunction detected!"
        )
    
    def execute(self, colony):
        """Cause a random building to malfunction."""
        if not colony.buildings:
            return "No buildings were affected as your colony has no structures."
            
        # Select a random operational building
        operational_buildings = [b for b in colony.buildings if b.is_operational]
        if not operational_buildings:
            return "No operational buildings were affected."
            
        building = random.choice(operational_buildings)
        building._operational = False
        building._condition = max(10, building.condition - 30)
        
        # Engineers might be able to fix it faster
        engineers = [c for c in colony.colonists if c.specialization == "Engineer" and c.is_alive]
        
        if engineers:
            engineer_text = f" {len(engineers)} engineer(s) have been notified and are working on repairs."
        else:
            engineer_text = " You have no engineers to perform immediate repairs."
            
        return f"Critical malfunction in the {building.name}! It's now non-operational.{engineer_text}"


class DiseaseOutbreak(Event):
    """Disease outbreak affects colonist health."""
    
    def __init__(self):
        super().__init__(
            "Disease Outbreak",
            "A mysterious illness is spreading among colonists!"
        )
    
    def execute(self, colony):
        """Make colonists sick, reducing health."""
        living_colonists = [c for c in colony.colonists if c.is_alive]
        if not living_colonists:
            return "There are no living colonists to be affected by the disease."
            
        # Determine how many get sick (30-70%)
        sick_count = max(1, int(len(living_colonists) * random.uniform(0.3, 0.7)))
        sick_colonists = random.sample(living_colonists, sick_count)
        
        # Make them sick
        for colonist in sick_colonists:
            health_loss = random.randint(10, 30)
            colonist._health = max(1, colonist.health - health_loss)
            colonist._happiness = max(0, colonist.happiness - 20)
        
        return f"Disease outbreak! {sick_count} colonists have fallen ill, reducing their health and happiness."


class ResourceDiscovery(Event):
    """Discovery of resource deposit."""
    
    def __init__(self):
        super().__init__(
            "Resource Discovery",
            "Your colonists have discovered a valuable resource deposit!"
        )
    
    def execute(self, colony):
        """Add a random resource windfall."""
        # Decide which resource is discovered
        resource_type = random.choice(["Materials", "Water"])
        amount = random.randint(30, 100)
        
        # Add resources
        colony.resources[resource_type]._quantity += amount
        
        # Scientist bonus
        scientists = [c for c in colony.colonists if c.specialization == "Scientist" and c.is_alive]
        if scientists:
            for scientist in scientists:
                scientist._happiness = min(100, scientist.happiness + 10)
            scientist_text = f" Your scientists are excited about studying the discovery!"
        else:
            scientist_text = ""
            
        return f"Resource discovery! {amount} units of {resource_type} have been added to your stockpile.{scientist_text}"


# For type hints in the events
from models.building import SolarPanel, Habitat
from models.colonist import Engineer, Scientist, Farmer, Miner