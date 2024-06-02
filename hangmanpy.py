import random
from tabulate import tabulate

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


def getRandomWord(wordList):
    # This function returns a random string from the passed list of strings.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def displayBoard(missedLetters, correctLetters, secretWord):
    print(HANGMAN_PICS[len(missedLetters)])
    print()
 
    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # Replace blanks with correctly guessed letters.
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # Show the secret word with spaces in between each letter.
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    # Returns the letter the player entered. This function makes sure the player entered a single letter and not something else.
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def selectLevel(level):
    if level == 'easy':
        return words[0]
    elif level == 'medium':
        return words[1]
    elif level == 'hard':
        return words[2]
    else:
        return words[random.randint(0, len(words) - 1)]
    
def displayMenu():
    # Define the header
    header = [["\033[32m    PLAY THE GAME     \033[0m"]]

    # Define the main data
    data = [
        ["\033[33m Easy level \033[0m", "\033[44m 1 \033[0m"],
        ["\033[33m Moderate level \033[0m", "\033[44m 2 \033[0m"],
        ["\033[33m Hard level \033[0m", "\033[44m 3 \033[0m"],
    ]

    # Define the footer data
    footer = [
        ["\033[33m Hall of fame \033[0m", "\033[44m 4 \033[0m"],
        ["\033[33m About the game \033[0m", "\033[44m 5 \033[0m"],
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




def playAgain():
    # This function returns True if the player wants to play again; otherwise, it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


print('H A N G M A N')
missedLetters = ''
correctLetters = ''
secretWord = getRandomWord(words)
gameIsDone = False

while True:
    displayMenu()
    displayBoard(missedLetters, correctLetters, secretWord)

    # Let the player enter a letter.
    guess = getGuess(missedLetters + correctLetters)

    if guess in secretWord:
        correctLetters = correctLetters + guess

        # Check if the player has won.
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print('Yes! The secret word is "' + secretWord + '"! You have won!')
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess

        # Check if player has guessed too many times and lost.
        if len(missedLetters) == len(HANGMAN_PICS) - 1:
            displayBoard(missedLetters, correctLetters, secretWord)
            print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
            gameIsDone = True

    # Ask the player if they want to play again (but only if the game is done).
    if gameIsDone:
        if playAgain():
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False
            secretWord = getRandomWord(words)
        else:
            break