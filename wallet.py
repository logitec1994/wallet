from user_account import UserAccount

class Wallet: # Should create UserAccount
    def __init__(self, initial_capital: float = 0.0):
        self.account = UserAccount(initial_capital)