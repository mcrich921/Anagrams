import string
import random
import csv
import time

# csv word list from
# http://www.gwicks.net/dictionaries.htm - English 84,000 text file
file = open('/PATH/TO/enigmix.csv')
dictIndex = csv.DictReader(file)

# gets all words from csv into a list
words = []
for col in dictIndex:
    words.append(col['Words'])

# make list of alphabet and assign some to special roles
upAlph = list(string.ascii_uppercase)
vowels = ['A', 'E', 'I', 'O', 'U']
consonants = upAlph
for let in vowels:
    consonants.remove(let)

weirdLetters = ['X', 'Z', 'Q', 'J']
uncommonLetters = ['W', 'K', 'V', 'Y']


# returns the lowercase version of a string
def low(x):
    return x.lower()


# returns the uppercase version of a string
def up(x):
    return x.upper()


# returns the lowercase version of a list
def lowLst(lst):
    newList = []
    for i in range(len(lst)):
        newList.append(lst[i].lower())
    return newList


# Select 7 random letters for the user to use, end up with list
def letterSelect():
    unusedVowels = vowels
    letIndex = []
    # Gives a letter index to be randomly chosen from, using weighting to make sure
    # weird letters are rarer
    for let in upAlph:
        if let in weirdLetters:
            letIndex.append(let)
        elif let in uncommonLetters:
            for i in range(3):
                letIndex.append(let)
        else:
            for i in range(6):
                letIndex.append(let)

    #Creates empty list of chosen letters and adds two vowels
    letChosen = []
    for i in range(2):
        let = random.choice(unusedVowels)
        letChosen.append(let)
        unusedVowels.remove(let)
        while let in letIndex:
            letIndex.remove(let)
    
    #Adds rest of letters to the list
    while len(letChosen) < 7:
        let = random.choice(letIndex)
        letChosen.append(let)
        while let in letIndex:
            letIndex.remove(let)
    
    #Shuffles list to make sure vowels appear randomly
    random.shuffle(letChosen)

    return letChosen


# check if all letters in a given list are in an index list
def rightLetters(check, index):
    valid = True
    check = lowLst(check)
    index = lowLst(index)
    for i in range(len(check)):
        if not(check[i] in index):
            valid = False
            break
    return valid


# checks to see if the guessed words meets all the criterion to be considered valid
def validGuess(guess, letLst, guessedWords, dict):
    if len(guess) > 2 and rightLetters(guess, letLst) and not (guess in lowLst(guessedWords)) and guess in dict:
        return True
    else:
        return False


# gives points based off of length of guess
def points(guess):
    pts = 0
    l = len(guess)
    if l<6:
        pts = l*100
    elif l == 6:
        pts = 800
    else:
        pts = 800 + 400 * (l - 6)
    
    splitGuess = list(up(guess))
    for let in splitGuess:
        if let in weirdLetters:
            pts += 50
        elif let in uncommonLetters:
            pts += 25

    return pts


def longestWord(letLst, dict):
    possibleWords = []
    for i in dict:
        letWrong = 0
        if len(i) > 2 and i[0] in letLst:
            for j in range(len(i)):
                if not i[j] in letLst:
                    letWrong += 1
        else:
            letWrong += 1
        if letWrong == 0:
            possibleWords.append(i)

    longest = possibleWords[0]
    for ele in possibleWords:
        if len(ele) > len(longest):
            longest = ele

    return up(longest)



# play the game with number of turns being the dictating factor
def playTurns():
    gameOver = False
    lettersChosen = letterSelect()
    guessedWords = []
    turn = 0
    ptsTotal = 0
    while not gameOver:
        rightGuess = False
        print(lettersChosen)
        # tells the user how many turns they have left and then asks for an input
        print("Guesses Left: " + str(5 - turn))
        guess = low(input("\nGuess a Word Now:\n"))
        # checks if user's guess is valid, then if it is adds it to guessed words
        # gives the user points, updates right guess to help with turn, and tells them they are correct
        # and how many points they got along with a list of correct words they already guessed
        if validGuess(guess, lettersChosen, guessedWords, words):
            guessedWords.append(up(guess))
            pts = points(guess)
            ptsTotal += pts
            rightGuess = True
            print("Correct!\n" + "+" + str(pts) + " Points!")
            print("Guessed Words: " + ", ".join(guessedWords))
        else:
            # tells the user one reason why their guess isn't valid
            if not rightLetters(guess, lettersChosen):
                print("Invalid: Only use given letters")
            elif len(guess) < 3:
                print("Invalid: Too short")
            elif guess in lowLst(guessedWords):
                print("Invalid: Already guessed")
            elif guess not in words:
                print("Invalid: Not a real word")

        # updates turn number only if the guess is correct
        if rightGuess:
            turn += 1
            if turn == 5:
                gameOver = True

    print("You got: " + str(ptsTotal) + " points! Good Job!")


# play the game with the time parameter being the dictating factor
def playTime():
    gameOver = False
    lettersChosen = letterSelect()
    guessedWords = []
    ptsTotal = 0
    sec = 60
    startTime = time.time()
    while not gameOver:
        print(lettersChosen)
        # gets guess from user and stores to variable
        guess = low(input("\nGuess a Word Now:\n"))
        # checks if user's guess is valid, then if it is adds it to guessed words
        # gives the user points, updates time, and tells them they are correct and how many points they got
        # along with a list of correct words they already guessed
        if validGuess(guess, lettersChosen, guessedWords, words):
            guessedWords.append(up(guess))
            pts = points(guess)
            ptsTotal += pts
            print("Correct!\n+" + str(pts) + " Points!")
            print("Guessed Words: " + ", ".join(guessedWords))
            endTime = time.time()
        else:
            # tells the user the reason why their guess isn't valid
            if not rightLetters(guess, lettersChosen):
                print("Invalid: Only use given letters")
            elif len(guess) < 3:
                print("Invalid: Too short")
            elif guess in lowLst(guessedWords):
                print("Invalid: Already guessed")
            elif guess not in words:
                print("Invalid: Not a real word")
            endTime = time.time()
        if int(endTime - startTime) >= sec:
            print("Time Left: 0 seconds")
        else:
            print("Time Left: " + str(sec - int(endTime - startTime)) + " seconds")

        # time condition that ends the game if the time is out/over
        if endTime - startTime >= sec:
            gameOver = True
    print("You got: " + str(ptsTotal) + " points in " + str(len(guessedWords)) + " words! Good Job!")
    print("Longest Possible Word:" + longestWord(lowLst(lettersChosen), words))


def play():
    gamemodeChosen = False
    # lets user pick a gamemode, either turn or time based
    while not gamemodeChosen:
        choice = input("Choose a gamemode:\nTurns\nTime\n")
        if low(choice) == "turns":
            gamemodeChosen = True
            playTurns()
        elif low(choice) == "time":
            gamemodeChosen = True
            playTime()
        else:
            print("Please enter a valid gamemode")

play()