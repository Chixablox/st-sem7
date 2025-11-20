class ATM:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "Недостаточно средств на счёте"
        self.balance -= amount
        return "Средства успешно сняты"
