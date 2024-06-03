from global_data import *
from tabulate import tabulate


def ansi_decorator(code):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return f"\033[{code}m{func(*args, **kwargs)}\033[0m"
        return wrapper
    return decorator

def displaySelectLevel():
    header = [[ansi_decorator('32')(lambda: "    SELECT FROM THE FOLLOWING SETS OF SECRET WORDS     ")()]]    
    data = [
        [ansi_decorator('33')(lambda: "1. Animals")(), ansi_decorator('44')(lambda: " 1 ")()],
        [ansi_decorator('33')(lambda: "2. Shapes")(), ansi_decorator('44')(lambda: " 2 ")()],
        [ansi_decorator('33')(lambda: "3. Places")(), ansi_decorator('44')(lambda: " 3 ")()],
    ]
    header_table = tabulate(header, tablefmt="double_outline", stralign="center", numalign="center")
    data_table = tabulate(data, headers=["LEVELS", "KEY"], tablefmt="fancy_grid", stralign="center", numalign="center")
    print(header_table)
    print(data_table)
    
    print('Enter the key (1, 2, 3, 4, or 5) based on above Menu:')
    input_key = input()
    if input_key in ['1', '2', '3']:
        return int(input_key) - 1
    else:
        print('Invalid input. Please enter a valid level key.')
        displaySelectLevel()
    
def displayHallOfFame(backend_db, hangman_game):
    backend_db.get_records()
    print("Press any key to return to Main Menu...")
    input()
    hangman_game.menu()
    
    

def displayMenu(hangman_game):
    print("Please Enter your name:")
    player_name = input()
    hangman_game.player_name = player_name
    header = [[ansi_decorator('32')(lambda: "    PLAY THE GAME     ")()]]

    data = [
        [ansi_decorator('33')(lambda: " Easy level ")(), ansi_decorator('44')(lambda: " 1 ")()],
        [ansi_decorator('33')(lambda: " Moderate level ")(), ansi_decorator('44')(lambda: " 2 ")()],
        [ansi_decorator('33')(lambda: " Hard level ")(), ansi_decorator('44')(lambda: " 3 ")()],
    ]

    footer = [
        [ansi_decorator('33')(lambda: " Hall of fame ")(), ansi_decorator('44')(lambda: " 4 ")()],
        [ansi_decorator('33')(lambda: " About the game ")(), ansi_decorator('44')(lambda: " 5 ")()],
    ]

    header_table = tabulate(header, tablefmt="double_outline", stralign="center", numalign="center")
    data_table = tabulate(data, headers=["LEVELS", "KEY"], tablefmt="mixed_outline", stralign="center", numalign="center")
    footer_table = tabulate(footer, headers=["INFO", "KEY"], tablefmt="fancy_grid", stralign="center", numalign="center")

    print(header_table)
    print(data_table)
    print(footer_table)

def getMenuInput():
    while True:
        print('Enter the key (1, 2, 3, 4, or 5) based on above Menu:')
        input_key = input()
        if input_key in ['1', '2', '3', '4', '5']:
            return input_key
        else:
            print('Invalid input. Please enter a valid level key.')