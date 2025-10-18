from behave import given, when, then
from classes.atm import ATM
from classes.authentication import UserAccount
from classes.coffeemachine import CoffeeMachine

# Для банкомата
@given('есть пользователь "{owner}", у которого на балансе {balance:d} рублей')
def step_given_user_with_balance(context, owner, balance):
    context.atm = ATM(owner, balance)


@when("этот пользователь пытается снять со счёта {amount:d} рублей")
def step_when_withdraw(context, amount):
    try:
        context.atm.withdraw(amount)
        context.exception = None
    except ValueError as e:
        context.exception = str(e)


# Для аутентификации
@given('есть пользователь с логином "{login}", у которого пароль "{password}"')
def step_given_user(context, login, password):
    context.user = UserAccount(login, password)


@when('пользователь "{login}" вводит неправильный пароль "{password_attempt}"')
def step_when_wrong_password(context, login, password_attempt):
    try:
        context.user.try_login(password_attempt)
        context.exception = None
    except ValueError as e:
        context.exception = str(e)


# Для кофемашины
@given("кофемашина, в которой есть {milk:d} мл молока")
def step_given_coffee_machine(context, milk):
    context.coffee_machine = CoffeeMachine(milk)


@when("заказывают капучино")
def step_when_order_cappuccino(context):
    try:
        context.coffee_machine.make_cappuccino()
        context.exception = None
    except ValueError as e:
        context.exception = str(e)


# Общее
@then('появляется ошибка с сообщением "{msg}"')
def step_then_error_message(context, msg):
    assert context.exception == msg
