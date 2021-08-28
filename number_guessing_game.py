import random
import colorama
from colorama import Fore

print(Fore.BLUE+'''                                 
             -----------  NUMBER GUESSING GAME IN PYTHON  ------------
''')
print(Fore.CYAN+"You have 5 chances to guess my number")
enter = input("Press enter to continue")
print()

chance = 5

n = random.randrange(1, 50)
guess = int(input(Fore.RED+"Enter any number from 1 to 50: "))
while guess != n:
    if guess < n:
        print (Fore.CYAN+"your guess is low think higher!")
        chance -= 1
        print("you have",chance,"chance remaining")
        if chance == 0:
            print("play again")
            chance = 5
        guess = int(input(Fore.RED+"\nEnter any number from 1 to 50: "))

    else:
        print (Fore.CYAN+"your guess is high think lower! ")
        chance -= 1
        print("you have",chance , "chance remaining")
        if chance == 0:
            print("play again")
            chance = 5
        guess = int(input(Fore.RED+"\nEnter any number from 1 to 50: "))

print(Fore.GREEN+"\nYour guess is correct YOU WIN")