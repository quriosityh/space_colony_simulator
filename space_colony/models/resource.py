class Resource:

    def __init__(self,name,quantity=0,production_rate=0):
    
        self._name   = name
        self._quantity= quantity
        self._production_rate=production_rate

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name=name

    @property
    def quantity(self):
        return self._quantity
   
    @quantity.setter
    def quantity(self,quantity):
        if quantity < 0:
            self._quantity=0
        else:
            self._quantity=quantity 

    @property
    def production_rate(self):
        return self._production_rate

    @production_rate.setter
    def production_rate(self,production_rate):
        if production_rate < 0:
            raise ValueError("Production rate cannot be negative")
        else:
            self._production_rate=production_rate


    def __str__(self):
        return f"Resource: {self._name}, Quantity: {self._quantity}, Production Rate: {self._production_rate}"
    

    def __repr__(self): 
        return f"Resource({self._name}, {self._quantity}, {self._production_rate})"
    
    def consume(self, amount):
        if 0 < amount <= self._quantity:
            self._quantity -= amount
            return True
        else:
            return False
        
    def produce(self, _production_rate=1):
        self._quantity += _production_rate
        return _production_rate
    

class Food(Resource):

    def __init__(self, quantity=0, production_rate=0):
        super().__init__("Food", quantity, production_rate)
        self._spoilage_rate = 0.05  # 10% spoilage rate per cycle
        
    def update_day(self):
        spoilage = self._quantity * self._spoilage_rate
        self._quantity -= spoilage
        if self._quantity < 0:
            self._quantity = 0
        return spoilage
    
    
class Water(Resource):
    def __init__(self, quantity=0, production_rate=0):
        super().__init__("Water", quantity, production_rate)
        

class Oxygen(Resource):
    def __init__(self, quantity=0, production_rate=0):
        super().__init__("Oxygen", quantity, production_rate)

class Materials(Resource):
    def __init__(self, quantity=0, production_rate=0):
        super().__init__("Materials", quantity, production_rate)


class Energy(Resource):
    """Energy resource that cannot be stored (resets daily)."""

    def __init__(self, quantity=0, production_rate=0):
        super().__init__("Energy", quantity, production_rate)   
        self._consumed = 0
    
    def consume(self, amount):
        if self._consumed + amount <= self._production_rate :
            self.consumed += amount
            return True
        return False
    
    def reset_day(self):
        self.consumed=0