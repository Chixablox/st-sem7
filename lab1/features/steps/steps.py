from behave import given, when, then
from classes.atm import ATM
from classes.authentication import UserAccount
from classes.coffeemachine import CoffeeMachine

# Для банкомата
@given('есть пользователь "{user}", у которого на балансе {balance:d} рублей')
def step_given_user_with_balance(context, user, balance):
    context.atm = ATM(user, balance)


@when("этот пользователь пытается снять со счёта {amount:d} рублей")
def step_when_withdraw(context, amount):
    context.result_message = context.atm.withdraw(amount)


# Для аутентификации
@given('есть пользователь с логином "{login}", у которого пароль "{password}"')
def step_given_user(context, login, password):
    context.user = UserAccount(login, password)


@when('пользователь "{login}" вводит неправильные пароли:')
def step_when_wrong_passwords(context, login):
    for row in context.table:
        password_attempt = row["Неправ_пароль"]
        context.result_message = context.user.try_login(password_attempt)


# Для кофемашины
@given("кофемашина, в которой есть {milk:d} мл молока")
def step_given_coffee_machine(context, milk):
    context.coffee_machine = CoffeeMachine(milk)


@when("заказывают капучино")
def step_when_order_cappuccino(context):
    context.result_message = context.coffee_machine.make_cappuccino()


# Общее
@then('появляется сообщение "{msg}"')
def step_then_error_message(context, msg):
    assert context.result_message == msg
