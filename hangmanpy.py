import random
from tabulate import tabulate
from global_data import *
from backend_handler import *
from helpers import *


print('H A N G M A N')



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











backend_db = backend()
hangman_game = HangmanGame(backend_db)
hangman_game.menu()



while True:
    hangman_game.playGame()
    # Ask the player if they want to play again (but only if the game is done).
    if hangman_game.gameIsDone:
        backend_db.update_records(hangman_game.player_name, levels[int(hangman_game.level)-1] , str(hangman_game.life - len(hangman_game.missedLetters)))
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