from abc import ABC, abstractmethod
import random

class Colonist:

    def __init__(self, name, specialization):
        self._name = name
        self._specialization = specialization
        self._health = 100
        self._happiness = 70
        self._hunger = 0
        self._thirst = 0
        self._is_alive = True

    @property
    def name(self):
        return self.name
    
    @property
    def specialization(self):
        return self._specialization

    @property
    def health(self):
        return self._health

    @property
    def happiness(self):
        return self._happiness

    @property
    def hunger(self):
        return self._hunger

    @property
    def thirst(self):
        return self._thirst
    
    @property
    def is_alive(self):
        return self._is_alive
    
    def consume_resources(self,food,water):

        """ here food and water are the objects resources """

        if food.consume(1) and    water.consume(0.5):
            self._hunger = 0
            self._thirst = 0
            return True
        
        if not food.consume(1):
            self._hunger += 25
        if not water.consume(0.5):
            self._thirst += 30
            
        self.update_health()
        return False
    
    def update_health(self):
         
            health_loss=0

            if self._hunger > 0:
                health_loss += self._hunger / 5
                self._happiness -= 5

            if self._thirst > 0:
                health_loss += self._thirst / 4
                self._happiness -= 7

            self._health -= health_loss
        
            if self._health <= 0:
                self._is_alive = False
                self._health = 0

    def boost_happiness(self, amount):
        self._happiness = min(self._happiness + amount, 100)

    def update_day(self):
        """Update colonist status for a new day."""
        if not self._is_alive:
            return
            
        # Natural happiness decrease
        self._happiness = max(0, self._happiness - 2)
        
        # Natural health recovery if not hungry/thirsty
        if self._hunger == 0 and self._thirst == 0 and self._health < 100:
            self._health = min(100, self._health + 5)

    def work(self):
        pass

    def __str__(self):
        return f"Colonist(name={self._name}, specialization={self._specialization}, health={self._health}, happiness={self._happiness}, hunger={self._hunger}, thirst={self._thirst}, is_alive={self._is_alive})"
    
    def __repr__(self):
        return f"Colonist({self._name}, {self._specialization}, {self._health}, {self._happiness}, {self._hunger}, {self._thirst}, {self._is_alive})"
    
class Engineer(Colonist):
    def __init__(self, name):
        super().__init__(name, "Engineer")
        self._skill_level = random.randint(1,10)

    def work(self):
        # Engineer-specific work logic
        
        """ returns worktype, efficiency
        influenced by health happines 
        """

        if not self.is_alive:
            return (None,0)
        
        efficiency = self._skill_level * (self._happiness/100) * (self.health/100)
        return ("Maintenance", efficiency)

    
    
    def repair_building(self, building):
        """Repair a building's condition.
        
        Args:
            building: Building to repair
            
        Returns:
            float: Amount of condition repaired
        """
        if not self._is_alive:
            return 0
            
        repair_amount = 20 * (self._skill_level / 10) * (self._health / 100)
        building.repair(repair_amount)
        self._happiness += 5  # Engineers enjoy fixing things
        return repair_amount

class Scientist(Colonist):
    """Scientist colonist specialized in research."""
    
    def __init__(self, name):
        super().__init__(name, "Scientist")
        self._skill_level = random.randint(1, 10)
    
    def work(self):
        """Perform scientific research.
        
        Returns:
            tuple: (work_type, research_points) - research points influenced by factors
        """
        if not self._is_alive:
            return ("none", 0)
            
        research_points = self._skill_level * (self._health / 100) * (self._happiness / 100) * 5
        return ("research", research_points)
    

class Farmer(Colonist):
    """Farmer colonist specialized in food production."""
    
    def __init__(self, name):
        super().__init__(name, "Farmer")
        self._skill_level = random.randint(1, 10)
    
    def work(self):
        """Perform farming work.
        
        Returns:
            tuple: (work_type, farming_efficiency) - efficiency influenced by factors
        """
        if not self._is_alive:
            return ("none", 0)
            
        efficiency = self._skill_level * (self._health / 100) * (self._happiness / 100) * 1.2
        return ("farming", efficiency)
    
    def boost_food_production(self, farm):
        """Boost a farm's food production.
        
        Args:
            farm: Farm building to boost
            
        Returns:
            float: Amount of boost applied
        """
        if not self._is_alive:
            return 0
            
        boost = 0.2 * self._skill_level * (self._health / 100)
        farm.boost_production(boost)
        return boost

class Miner(Colonist):
    """Miner colonist specialized in material extraction."""
    
    def __init__(self, name):
        super().__init__(name, "Miner")
        self._skill_level = random.randint(1, 10)
    
    def work(self):
        """Perform mining work.
        
        Returns:
            tuple: (work_type, mining_efficiency) - efficiency influenced by factors
        """
        if not self._is_alive:
            return ("none", 0)
            
        efficiency = self._skill_level * (self._health / 100) * (self._happiness / 100) * 1.1
        return ("mining", efficiency)
