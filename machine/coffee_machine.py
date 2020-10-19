inactive_prompt = 'Write action (buy, fill, take, remaining, exit):'
buy_prompt = 'What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:'
fill_water_prompt = 'Write how many ml of water do you want to add:'
fill_milk_prompt = 'Write how many ml of milk do you want to add:'
fill_beans_prompt = 'Write how many grams of coffee beans do you want to add:'
fill_cups_prompt = 'Write how many disposable cups of coffee do you want to add:'

buy_action = 'buy'
fill_action = 'fill'
take_action = 'take'
exit_action = 'exit'
back_action = 'back'
remaining_action = 'remaining'

code_espresso = 1
code_latte = 2
code_cappuccino = 3

# espresso
espresso_water = 250
espresso_beans = 16
espresso_cost = 4

# latte
latte_water = 350
latte_milk = 75
latte_beans = 20
latte_cost = 7

# cappuccino
cappuccino_water = 200
cappuccino_milk = 100
cappuccino_beans = 12
cappuccino_cost = 6

state_inactive = 'inactive'
state_buying = 'buying'
state_filling = 'filling'
state_filling_water = 'filling_water'
state_filling_milk = 'filling_milk'
state_filling_beans = 'filling_beans'
state_filling_cups = 'filling_cups'


class CoffeeMachine:
    def __init__(self,
                 money,
                 water,
                 milk,
                 beans,
                 cups,
                 state=state_inactive):
        self.money = money
        self.water = water
        self.milk = milk
        self.beans = beans
        self.cups = cups
        self.state = state

    def process(self, action):
        if self.state == state_inactive:
            if action == buy_action:
                self.buy_scene(action)
            elif action == fill_action:
                self.state = state_filling
                self.fill_scene(action)
            elif action == take_action:
                self.take_scene()
            elif action == remaining_action:
                self.remaining_scene()
            else:
                return False
        elif self.state == state_buying:
            self.buy_scene(action)
        elif self.state == state_filling \
                or self.state == state_filling_water \
                or self.state == state_filling_milk \
                or self.state == state_filling_beans \
                or self.state == state_filling_cups:
            self.fill_scene(action)

        return True

    def buy_scene(self, next_action):
        if self.state == state_inactive:
            print(buy_prompt)
            self.state = state_buying
            return

        should_process = False
        if next_action != back_action:
            next_action = int(next_action)
            should_process = self.check_stocks(next_action)

        if not should_process:
            self.state = state_inactive
            print(inactive_prompt)
            return

        if next_action == code_espresso:
            self.water -= espresso_water
            self.beans -= espresso_beans
            self.money += espresso_cost
        elif next_action == code_latte:
            self.water -= latte_water
            self.milk -= latte_milk
            self.beans -= latte_beans
            self.money += latte_cost
        elif next_action == code_cappuccino:
            self.water -= cappuccino_water
            self.milk -= cappuccino_milk
            self.beans -= cappuccino_beans
            self.money += cappuccino_cost
        else:
            self.state = state_inactive
            print(inactive_prompt)
            return

        self.cups -= 1

        self.state = state_inactive
        print('I have enough resources, making you a coffee!')
        print(inactive_prompt)

    def fill_scene(self, action):
        if self.state == state_filling:
            print(fill_water_prompt)
            self.state = state_filling_water
        elif self.state == state_filling_water:
            self.water += int(action)
            print(fill_milk_prompt)
            self.state = state_filling_milk
        elif self.state == state_filling_milk:
            self.milk += int(action)
            print(fill_beans_prompt)
            self.state = state_filling_beans
        elif self.state == state_filling_beans:
            self.beans += int(action)
            print(fill_cups_prompt)
            self.state = state_filling_cups
        elif self.state == state_filling_cups:
            self.cups += int(action)
            print(inactive_prompt)
            self.state = state_inactive

    def take_scene(self):
        print('I gave you $' + str(self.money))
        self.money = 0
        self.state = state_inactive

    def remaining_scene(self):
        self.print_stocks()
        self.state = state_inactive

    def print_stocks(self):
        print('The coffee machine has:\n'
              + str(self.water)
              + ' of water\n'
              + str(self.milk)
              + ' of milk\n'
              + str(self.beans)
              + ' of coffee beans\n'
              + str(self.cups)
              + ' of disposable cups\n'
              + str(self.money)
              + ' of money')

    def check_stocks(self, drink):
        cups = 'cups'
        water = 'water'
        milk = 'milk'
        beans = 'coffee beans'

        def check_water(drink_code):
            if drink_code == code_espresso and self.water < espresso_water:
                return False
            elif drink_code == code_latte and self.water < latte_water:
                return False
            elif drink_code == code_cappuccino and self.water < cappuccino_water:
                return False
            return True

        def check_milk(drink_code):
            if drink_code == code_latte and self.milk < latte_milk:
                return False
            elif drink_code == code_cappuccino and self.milk < cappuccino_milk:
                return False
            return True

        def check_beans(drink_code):
            if drink_code == code_espresso and self.beans < espresso_beans:
                return False
            elif drink_code == code_latte and self.beans < latte_beans:
                return False
            elif drink_code == code_cappuccino and self.beans < cappuccino_beans:
                return False
            return True

        can_make_drink = True
        enough_cups = self.cups > 0
        enough_water = check_water(drink)
        enough_milk = check_milk(drink)
        enough_beans = check_beans(drink)

        if not enough_cups:
            can_make_drink = False
            print(CoffeeMachine.get_not_enough_statement(cups))

        if not enough_water:
            can_make_drink = False
            print(CoffeeMachine.get_not_enough_statement(water))

        if not enough_milk:
            can_make_drink = False
            print(CoffeeMachine.get_not_enough_statement(milk))

        if not enough_beans:
            can_make_drink = False
            print(CoffeeMachine.get_not_enough_statement(beans))

        return can_make_drink

    @staticmethod
    def get_not_enough_statement(item):
        return 'Sorry, not enough ' + item + '!'


coffee_machine = CoffeeMachine(550, 400, 540, 120, 9)

while True:
    process = coffee_machine.process(input())
    if not process:
        break
