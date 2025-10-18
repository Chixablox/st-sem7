class UserAccount:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.failed_attempts = 0
        self.blocked = False

    def try_login(self, password_attempt):
        if self.blocked:
            raise ValueError("Произошла блокировка аккаунта")
        if password_attempt != self.password:
            self.failed_attempts += 1
            if self.failed_attempts >= 3:
                self.blocked = True
                raise ValueError("Произошла блокировка аккаунта")
            else:
                raise ValueError("Неверный пароль")
        self.failed_attempts = 0
        return True
