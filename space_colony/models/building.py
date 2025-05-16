from abc import ABC, abstractmethod

class Building(ABC):
    """Abstract base class for all colony buildings."""
    
    def __init__(self, name, size, energy_usage):
        self._name = name
        self._size = size
        self._energy_usage = energy_usage
        self._condition = 100  # 100% condition when new
        self._operational = True
    
    @property
    def name(self):
        """Get the building name."""
        return self._name
    
    @property
    def size(self):
        """Get the building size."""
        return self._size
    
    @property
    def energy_usage(self):
        """Get energy consumption per day."""
        return self._energy_usage
    
    @property
    def condition(self):
        """Get current condition."""
        return self._condition
    
    @property
    def is_operational(self):
        """Check if building is operational."""
        return self._operational and self._condition > 20
    
    def repair(self, amount):
        """Repair building condition.
        
        Args:
            amount: Amount of condition to repair
        """
        self._condition = min(100, self._condition + amount)
        if self._condition > 20:
            self._operational = True
    
    def update_day(self, energy_available=True):
        """Update building for a new day.
        
        Args:
            energy_available: Whether required energy is available
        """
        # Decrease condition naturally
        self._condition = max(0, self._condition - 1)
        
        # If no energy or poor condition, mark non-operational
        if not energy_available or self._condition <= 20:
            self._operational = False
        else:
            self._operational = True
    
    @abstractmethod
    def operate(self):
        """Perform daily building operation."""
        pass
    
    def __str__(self):
        """String representation of the building."""
        status = "Operational" if self.is_operational else "Non-operational"
        return f"{self._name} - Condition: {self._condition}% [{status}]"


class Habitat(Building):
    """Living quarters for colonists."""
    
    def __init__(self, capacity=10):
        super().__init__("Habitat", size=capacity*5, energy_usage=capacity*0.5)
        self._capacity = capacity
        self._comfort_level = 1.0  # Multiplier for happiness
    
    @property
    def capacity(self):
        """Get colonist capacity."""
        return self._capacity
    
    @property
    def comfort_level(self):
        """Get comfort level."""
        return self._comfort_level
    
    def upgrade_comfort(self, amount):
        """Upgrade habitat comfort.
        
        Args:
            amount: Amount to increase comfort level
        """
        self._comfort_level += amount
        self._energy_usage += amount * 0.2  # More comfort uses more energy
    
    def operate(self):
        """Daily habitat operation."""
        if self.is_operational:
            # Habitats don't produce anything but affect colonist happiness
            happiness_effect = 5 * self._comfort_level * (self._condition / 100)
            return ("happiness", happiness_effect)
        return ("happiness", 0)


class Farm(Building):
    """Food production facility."""
    
    def __init__(self, size=5):
        super().__init__("Farm", size=size, energy_usage=size*0.8)
        self._base_production = size * 2
        self._efficiency = 1.0
    
    def boost_production(self, amount):
        """Boost farm production efficiency.
        
        Args:
            amount: Efficiency boost amount
        """
        self._efficiency += amount
    
    def operate(self):
        """Daily farm operation."""
        if self.is_operational:
            # Calculate actual food production
            production = self._base_production * self._efficiency * (self._condition / 100)
            return ("food", production)
        return ("food", 0)


class WaterReclaimer(Building):
    """Water production facility."""
    
    def __init__(self, size=3):
        super().__init__("Water Reclaimer", size=size, energy_usage=size*1.2)
        self._base_production = size * 3
    
    def operate(self):
        """Daily water reclaimer operation."""
        if self.is_operational:
            # Calculate actual water production
            production = self._base_production * (self._condition / 100)
            return ("water", production)
        return ("water", 0)


class OxygenGenerator(Building):
    """Oxygen production facility."""
    
    def __init__(self, size=4):
        super().__init__("Oxygen Generator", size=size, energy_usage=size*1.5)
        self._base_production = size * 5
    
    def operate(self):
        """Daily oxygen generator operation."""
        if self.is_operational:
            # Calculate actual oxygen production
            production = self._base_production * (self._condition / 100)
            return ("oxygen", production)
        return ("oxygen", 0)


class SolarPanel(Building):
    """Energy production facility."""
    
    def __init__(self, size=2):
        super().__init__("Solar Panel", size=size, energy_usage=0)  # Doesn't consume energy
        self._base_production = size * 3
    
    def operate(self):
        """Daily solar panel operation."""
        if self.is_operational:
            # Calculate actual energy production
            production = self._base_production * (self._condition / 100)
            return ("energy", production)
        return ("energy", 0)


class Mine(Building):
    """Materials production facility."""
    
    def __init__(self, size=5):
        super().__init__("Mine", size=size, energy_usage=size*2)
        self._base_production = size * 1.5
    
    def operate(self):
        """Daily mine operation."""
        if self.is_operational:
            # Calculate actual materials production
            production = self._base_production * (self._condition / 100)
            return ("materials", production)
        return ("materials", 0)


class Laboratory(Building):
    """Research facility."""
    
    def __init__(self, size=4):
        super().__init__("Laboratory", size=size, energy_usage=size*1.8)
        self._research_multiplier = 1.0
    
    def upgrade_equipment(self, amount):
        """Upgrade lab equipment.
        
        Args:
            amount: Amount to improve research multiplier
        """
        self._research_multiplier += amount
        self._energy_usage += amount * 0.5  # Better equipment uses more energy
    
    def operate(self):
        """Daily laboratory operation."""
        if self.is_operational:
            # Labs boost scientist productivity
            research_boost = 1.5 * self._research_multiplier * (self._condition / 100)
            return ("research_boost", research_boost)
        return ("research_boost", 0)