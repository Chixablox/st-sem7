class UserAccount:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.failed_attempts = 0
        self.block = False

    def try_login(self, password_attempt):
        if self.block:
            return "Произошла блокировка аккаунта"
        if password_attempt != self.password:
            self.failed_attempts += 1
            if self.failed_attempts >= 3:
                self.block = True
                return "Произошла блокировка аккаунта"
            else:
                return "Неверный пароль"
        self.failed_attempts = 0
        return "Выполнен успешный вход в аккаунт"
