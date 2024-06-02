import random
from tabulate import tabulate
import time
from tabulate import tabulate

print('H A N G M A N')
# missedLetters = ''
# correctLetters = ''
# # secretWord = getRandomWord(words)
# secretWord = ''
# gameIsDone = False
# life = 8
class HangmanGame:
    def __init__(self):
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
            print('Guess a letter.')
            guess = input()
            guess = guess.lower()
            if len(guess) != 1:
                print('Please enter a single letter.')
            elif guess in self.correctLetters or guess in self.missedLetters:
                print('You have already guessed that letter. Choose again.')
            elif guess not in 'abcdefghijklmnopqrstuvwxyz':
                print('Please enter a LETTER.')
            else:
                return guess

    def selectLevel(self,level):
        if level == "1": # easy
            self.life = 8
            displaySelectLevel()
            return words[0]
        elif level == "2": # medium
            self.life = 6
            displaySelectLevel()
            return words[1]
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
        displayMenu()
        input_key = getMenuInput()
        if input_key in ['1', '2', '3']:
            self.secretWord = self.getRandomWord(self.selectLevel(input_key))
        elif input_key == '4':
            pass
        elif input_key == '5':
            self.displayAbout()
        self.playGame()

    def play(self):
        while True:
            self.playGame()
            if self.gameIsDone:
                if self.playAgain():
                    self.missedLetters = ''
                    self.correctLetters = ''
                    self.gameIsDone = False
                    self.life = 8
                    self.secretWord = self.getRandomWord(words)
                    self.menu()
                else:
                    break

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


# def getRandomWord(wordList):
#     # This function returns a random string from the passed list of strings.
#     wordIndex = random.randint(0, len(wordList) - 1)
#     return wordList[wordIndex]

# def displayBoard(missedLetters, correctLetters, secretWord):
#     print(HANGMAN_PICS[len(missedLetters)])
#     print()
 
#     print('Missed letters:', end=' ')
#     for letter in missedLetters:
#         print(letter, end=' ')
#     print()

#     blanks = '_' * len(secretWord)

#     for i in range(len(secretWord)): # Replace blanks with correctly guessed letters.
#         if secretWord[i] in correctLetters:
#             blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

#     for letter in blanks: # Show the secret word with spaces in between each letter.
#         print(letter, end=' ')
#     print()

# def getGuess(alreadyGuessed):
#     # Returns the letter the player entered. This function makes sure the player entered a single letter and not something else.
#     while True:
#         print('Guess a letter.')
#         guess = input()
#         guess = guess.lower()
#         if len(guess) != 1:
#             print('Please enter a single letter.')
#         elif guess in alreadyGuessed:
#             print('You have already guessed that letter. Choose again.')
#         elif guess not in 'abcdefghijklmnopqrstuvwxyz':
#             print('Please enter a LETTER.')
#         else:
#             return guess

def selectLevel(level):
    if level == "1": # easy
        life = 8
        return words[displaySelectLevel()]
    elif level == "2": # medium
        life = 6
        return words[displaySelectLevel()]
    elif level == "3": # hard
        life = 6
        return words[random.randint(0, len(words) - 1)]
    # else:
    #     return words[random.randint(0, len(words) - 1)]

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
        return input_key
    else:
        print('Invalid input. Please enter a valid level key.')
        displaySelectLevel()
    

    

def displayMenu():
    # Define the header
    header = [[ansi_decorator('32')(lambda: "    PLAY THE GAME     ")()]]

    # Define the main data
    data = [
        [ansi_decorator('33')(lambda: " Easy level ")(), ansi_decorator('44')(lambda: " 1 ")()],
        [ansi_decorator('33')(lambda: " Moderate level ")(), ansi_decorator('44')(lambda: " 2 ")()],
        [ansi_decorator('33')(lambda: " Hard level ")(), ansi_decorator('44')(lambda: " 3 ")()],
    ]

    # Define the footer data
    footer = [
        [ansi_decorator('33')(lambda: " Hall of fame ")(), ansi_decorator('44')(lambda: " 4 ")()],
        [ansi_decorator('33')(lambda: " About the game ")(), ansi_decorator('44')(lambda: " 5 ")()],
    ]

    # Create the header table with a single column
    header_table = tabulate(header, tablefmt="double_outline", stralign="center", numalign="center")

    # Create the main data table with two columns
    data_table = tabulate(data, headers=["LEVELS", "KEY"], tablefmt="mixed_outline", stralign="center", numalign="center")

    # Create the footer table with two columns
    footer_table = tabulate(footer, headers=["INFO", "KEY"], tablefmt="fancy_grid", stralign="center", numalign="center")

    # Print the tables
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


# def playAgain():
#     # This function returns True if the player wants to play again; otherwise, it returns False.
#     print('Do you want to play again? (yes or no)')
#     return input().lower().startswith('y')




# def playGame():

#     displayBoard(missedLetters, correctLetters, secretWord)

#     # Let the player enter a letter.
#     guess = getGuess(missedLetters + correctLetters)

#     if guess in secretWord:
#         correctLetters = correctLetters + guess

#         # Check if the player has won.
#         foundAllLetters = True
#         for i in range(len(secretWord)):
#             if secretWord[i] not in correctLetters:
#                 foundAllLetters = False
#                 break
#         if foundAllLetters:
#             print('Yes! The secret word is "' + secretWord + '"! You have won!')
#             gameIsDone = True
#     else:
#         missedLetters = missedLetters + guess

#         # Check if player has guessed too many times and lost.
#         if len(missedLetters) == life - 1:
#             displayBoard(missedLetters, correctLetters, secretWord)
#             print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
#             gameIsDone = True

# def displayAbout():
#     header = [[ansi_decorator('32')(lambda: """ABOUT THE GAME""")()]]
#     data = [
#         ["""Easy""", 
#          """The user will be given the chance to select the list from which the random word will \n
#          be selected (Animal, Shape, Place). This will make it easier to guess the secret word. \n
#          Also, the number of trials will be increased from 6 to 8."""],
#         ["""Moderate""", 
#          """Similar to Easy, the user will be given the chance to select the set \n
#          from which the random word will be selected (Animal, Shape, Place), but the number of \n
#          trials will be reduced to 6. The last two graphics will not be used or displayed."""],
#         ["""Hard""", 
#          """The code will randomly select a set of words. From this set, the code will \n
#          randomly select a word. The user will have no clue about the secret word. Also, the number \n
#          of trials will remain at 6."""]
#     ]
#     header_table = tabulate(header, tablefmt="double_outline", stralign="center", numalign="center")
#     table = tabulate(data, headers=['Level', 'Description'], tablefmt='fancy_grid')
#     print(header_table)
#     print(table)
    
#     print("Press any key to return to Main Menu...")
#     input()



# def menu():
#     displayMenu()
#     input_key = getMenuInput()
#     if input_key in ['1', '2', '3']:
#         secretWord = getRandomWord(selectLevel(input_key))
#     elif input_key == '4':
#         pass
#     elif input_key == '5':
#         displayAbout()
hangman_game = HangmanGame()
hangman_game.menu()

while True:
    hangman_game.playGame()
    # Ask the player if they want to play again (but only if the game is done).
    if hangman_game.gameIsDone:
        if hangman_game.playAgain():
            hangman_game.missedLetters = ''
            hangman_game.correctLetters = ''
            hangman_game.gameIsDone = False
            hangman_game.life = 8
            hangman_game.secretWord = hangman_game.getRandomWord(words)
            hangman_game.menu()
        else:
            break