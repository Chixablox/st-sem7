class CoffeeMachine:
    def __init__(self, milk_ml):
        self.milk = milk_ml

    def make_cappuccino(self):
        milk_needed = 100
        if self.milk < milk_needed:
            return "Не хватает молока"
        self.milk -= milk_needed
        return "Капучино готов"
