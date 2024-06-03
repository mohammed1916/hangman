import random
from tabulate import tabulate
import sqlite3

print('H A N G M A N')

class backend:
    def __init__(self):
        self.conn = sqlite3.connect('hangman_records.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS records (level text, player_name text, remaining_lives integer)''')
    
# conn = sqlite3.connect('hangman_records.db')
# c = conn.cursor()
# print(c)


    def update_records(self, player_name, level, remaining_lives):
        # Check if the player already has a record for the level
        self.c.execute("SELECT remaining_lives FROM records WHERE level=? AND player_name=? ", (player_name, level))
        result = self.c.fetchone()

        if result is None:
            # Insert a new record for the player and level
            self.c.execute("INSERT INTO records VALUES (?, ?, ?)", (level, player_name, remaining_lives))
        else:
            # Update the existing record if the new remaining lives is higher
            if remaining_lives > result[0]:
                self.c.execute("UPDATE records SET remaining_lives=? WHERE player_name=? AND level=?", (remaining_lives, player_name, level))

        # Commit the changes to the database
        self.conn.commit()

    def get_records(self):
        self.c.execute("SELECT * FROM records")
        records = self.c.fetchall()
        print(tabulate(records, headers=["Level", "Player Name", "Remaining Lives"], tablefmt="fancy_grid"))
        return records

class HangmanGame:
    def __init__(self, backend_db):
        self.backend_db = backend_db
        self.level = 0
        self.player_name = ''
        self.missedLetters = ''
        self.correctLetters = ''
        self.secretWord = ''
        self.gameIsDone = False
        self.life = 8

    def getRandomWord(self, wordList):
        wordIndex = random.randint(0, len(wordList) - 1)
        return wordList[wordIndex]

    def displayBoard(self):
        print(HANGMAN_PICS[len(self.missedLetters)])
        print()
        print('Missed letters:', end=' ')
        for letter in self.missedLetters:
            print(letter, end=' ')
        print()

        blanks = '_' * len(self.secretWord)

        for i in range(len(self.secretWord)):
            if self.secretWord[i] in self.correctLetters:
                blanks = blanks[:i] + self.secretWord[i] + blanks[i+1:]

        for letter in blanks:
            print(letter, end=' ')
        print()

    def getGuess(self):
        while True:
            data = [[ansi_decorator('38;5;220')(lambda: str(self.life - len(self.missedLetters)) )()]]
            print(tabulate(data,headers=['Remaining lives:'], tablefmt="fancy_grid", stralign="center", numalign="center"))
            print('Guess a letter.')
            guess = input()
            guess = guess.lower()
            if len(guess) != 1:
                data = [[ansi_decorator('38;5;196')(lambda: "ERROR" )()]]
                print(tabulate(data,headers=['Please enter a single letter.'], tablefmt="fancy_grid", stralign="center", numalign="center"))
                print()
            elif guess in self.correctLetters or guess in self.missedLetters:
                data = [[ansi_decorator('38;5;196')(lambda: "ERROR" )()]]
                print(tabulate(data,headers=['You have already guessed that letter. Choose again.'], tablefmt="fancy_grid", stralign="center", numalign="center"))
            elif guess not in 'abcdefghijklmnopqrstuvwxyz':
                data = [[ansi_decorator('38;5;196')(lambda: "ERROR" )()]]
                print(tabulate(data,headers=['Please enter a LETTER.'], tablefmt="fancy_grid", stralign="center", numalign="center"))
            else:
                return guess

    def selectLevel(self,level):
        self.level = level
        if level == "1": # easy
            life = 8
            return words[displaySelectLevel()]
        elif level == "2": # moderate
            life = 6
            return words[displaySelectLevel()]
        elif level == "3": # hard
            self.life = 6
            return words[random.randint(0, len(words) - 1)]

    def playGame(self):
        self.displayBoard()
        guess = self.getGuess()

        if guess in self.secretWord:
            self.correctLetters += guess
            foundAllLetters = True
            for i in range(len(self.secretWord)):
                if self.secretWord[i] not in self.correctLetters:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                print('Yes! The secret word is "' + self.secretWord + '"! You have won!')
                self.gameIsDone = True
        else:
            self.missedLetters += guess
            if len(self.missedLetters) == self.life - 1:
                self.displayBoard()
                print('You have run out of guesses!\nAfter ' + str(len(self.missedLetters)) + ' missed guesses and ' + str(len(self.correctLetters)) + ' correct guesses, the word was "' + self.secretWord + '"')
                self.gameIsDone = True

    def playAgain(self):
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')

    def menu(self):
        displayMenu(self)
        input_key = getMenuInput()
        if input_key in ['1', '2', '3']:
            self.secretWord = self.getRandomWord(self.selectLevel(input_key))
            self.playGame()
        elif input_key == '4':
            displayHallOfFame(self.backend_db, self)
            
        elif input_key == '5':
            self.displayAbout()
            self.menu()

    # def play(self):
    #     while True:
    #         self.playGame()
    #         if self.gameIsDone:
    #             if self.playAgain():
    #                 self.missedLetters = ''
    #                 self.correctLetters = ''
    #                 self.gameIsDone = False
    #                 self.life = 8
    #                 self.secretWord = self.getRandomWord(words)
    #                 self.menu()
    #             else:
    #                 break

    def displayAbout(self):
        header = [[ansi_decorator('32')(lambda: """ABOUT THE GAME""")()]]
        data = [
            ["""Easy""", 
            """The user will be given the chance to select the list from which the random word will \n
            be selected (Animal, Shape, Place). This will make it easier to guess the secret word. \n
            Also, the number of trials will be increased from 6 to 8."""],
            ["""Moderate""", 
            """Similar to Easy, the user will be given the chance to select the set \n
            from which the random word will be selected (Animal, Shape, Place), but the number of \n
            trials will be reduced to 6. The last two graphics will not be used or displayed."""],
            ["""Hard""", 
            """The code will randomly select a set of words. From this set, the code will \n
            randomly select a word. The user will have no clue about the secret word. Also, the number \n
            of trials will remain at 6."""]
        ]
        header_table = tabulate(header, tablefmt="double_outline", stralign="center", numalign="center")
        table = tabulate(data, headers=['Level', 'Description'], tablefmt='fancy_grid')
        print(header_table)
        print(table)
        
        print("Press any key to return to Main Menu...")
        input()


HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\\  |
      |
     ===''', '''
  +---+
  O   |
 /|\\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\\  |
 / \\  |
     ===''', '''
  +---+
 [O   |
 /|\\  |
 / \\  |
     ===''', '''
  +---+
 [O]  |
 /|\\  |
 / \\  |
     ===''']        
                
                
                
animal = 'ant baboon badger bat bear beaver camel cat clam cobra panda zebra sheep'.split()
Shapes = 'square triangle rectangle circle ellipse rhombus trapezoid Place'.split()
Place = 'Cairo London Paris Baghdad Istanbul Riyadh'.split()

words = [animal, Shapes, Place]
levels = ['Easy', 'Moderate', 'Hard']




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



backend_db = backend()
hangman_game = HangmanGame(backend_db)
hangman_game.menu()



while True:
    hangman_game.playGame()
    # Ask the player if they want to play again (but only if the game is done).
    if hangman_game.gameIsDone:
        backend_db.update_records(hangman_game.player_name, levels[int(hangman_game.level)-1] , hangman_game.life)
        if hangman_game.playAgain():
            hangman_game.missedLetters = ''
            hangman_game.correctLetters = ''
            hangman_game.gameIsDone = False
            hangman_game.life = 8
            hangman_game.secretWord = hangman_game.getRandomWord(words)
            displayHallOfFame(backend_db, hangman_game)
        else:
            backend_db.conn.close()
            break