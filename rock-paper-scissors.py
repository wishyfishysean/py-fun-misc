import random

user_wins = 0
computer_wins = 0

options = ["rock", "paper", "scissors"]
while True:
    user_input = input("Type Rock, Paper or Scissors or Quit: ").lower()
    if user_input == "Quit":
        break

    if user_input not in options:
        continue


    random_number = random.randin(0, 2)
    # 0 is rock,1 is paper, 2 is scissors
    computer_pick = options[random_number]
    print("Computer picked", computer_pick + ".")

    if user_input == "rock" and computer_pick == "scissors":
        print("Winner winner!")
        user_wins += 1



print("Goodbye, thanks for playing!")