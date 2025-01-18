#!/usr/bin/env python3

import glob
import json
import os
import random


def get_intro_input():
    print("Main menu:\n"
          "(1): New game\n"
          "(2): New game with drink choice\n"
          "(3): Rules\n"
          "(4): Adding new choices\n"
          "(0): Exit\n")
    return input("Please enter a number: ")

def exit_game():
    print("\nExiting game...")
    print("Goodbye!")
    exit()

def print_rules():
    print("Rules of the game:\n"
          "- The game is played with two or more players.\n"
          "- The players take turns to choose between answering a question truthfully or performing a dare or drink.\n"
          "- If a player chooses truth, they must answer the question honestly.\n"
          "- If a player chooses dare, they must perform the dare.\n"
          "- If a player chooses drink, they must drink a shot.\n"
          "- The game will provide a random question or dare for the player to answer or perform.\n"
          "- Player should choose the chosen option.\n"
          "- The game will keep track of the score of each player and show when the game is over.\n")

def print_new_choices():
    print("Choices stored as json file in folder databank. You can add your own choices, or create new files. "
          "The json file should have the following format:\n"
          "---------------------------------\n"
          "{\n"
          '\t"truth": [ "question0", "question1", ... ] \n'
          '\t"dare": [ "dare0", "dare1", ... ] \n'
          "}\n"
          "---------------------------------\n")

def print_scores(scores_p):
    for p, score_data in scores_p.items():
        print(f"{p}:\n\tTruth: {score_data['truth']},\n\tDare: {score_data['dare']}" +
              (f",\n\tDrink: {score_data['drink']}" if 'drink' in score_data else "") + "\n")
    print("----------------------------------------")
    for p, score_data in scores_p.items():
        print(f"{p}:\n")
        print("\tTruths:")
        for q in score_data['questions']:
            print(f"\t\t{q}")
        print("\tDares:")
        for d in score_data['dares']:
            print(f"\t\t{d}\n\n")

if __name__ == "__main__":
    print("Truth or Dare v1.0")
    print("------------------")
    print("Welcome to the game of Truth or Dare!\n")

    while True:  # Main menu loop
        choice = get_intro_input()
        match choice:
            case "0":
                exit_game()
            case "1":
                drink_choice = False
                break
            case "2":
                drink_choice = True
                break
            case "3":
                print_rules()
            case "4":
                print_new_choices()
            case _:
                print("Invalid input. Please try again.\n")


    # Get game set
    game_sets = glob.glob(os.path.join("databank", '*.json'))  # Get all json files in databank folder

    game_set_path = None

    if not game_sets:
        print("No game sets found in databank folder.")
        exit_game()
    elif len(game_sets) == 1:
        print(f"Using game set: {os.path.splitext(os.path.basename(game_sets[0]))[0]}")
        game_set_path = game_sets[0]
    else:
        while True:
            print("\nChoose a game set:")
            for i, game_set_name in enumerate(game_sets):
                print(f"({i+1}): {os.path.splitext(os.path.basename(game_set_name))[0]}")
            print("(0): Exit game")
            choice = input("Please enter a number: ")
            if choice == "0":
                exit_game()
            try:
                game_set_path = game_sets[int(choice)-1]
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
                continue
            break

    with open(game_set_path, 'r') as file:
        game_set = json.load(file)

    if "truth" not in game_set or "dare" not in game_set:
        print("Invalid game set. Exiting game.")
        exit_game()

    dare_count = len(game_set['dare'])
    truth_count = len(game_set['truth'])

    # Get player names
    players = []
    while True:
        player_name = input("Enter player name (or leave empty to start game): ")
        if player_name in players:
            print("Player already exists. Please enter a different name.")
            continue
        if not player_name:
            break
        players.append(player_name)

    if not players:
        print("No players found. Exiting game.")
        exit_game()

    print(f"\nWelcome {', '.join(players)}")

    scores = dict()
    for player in players:
        scores[player] = {
            "truth": 0,
            "dare": 0,
            "questions": [],
            "dares": []
        }
        if drink_choice:
            scores[player]["drink"] = 0
    turn = 0
    eliminated = []

    # Game loop
    while True:
        question = ""
        dare = ""
        player = players[turn % len(players)]
        if player in eliminated:
            turn += 1
            continue
        print("----------------------------------------")
        print(f"\n{player}'s turn:{question}{dare}")  # these added to silence the warning
        print("Truth or Dare or Drink?")
        choice = input("(1): Truth\n"
                       "(2): Dare\n" +
                       ("(3): Drink\n" if drink_choice else "") +
                       "(0): Exit game\n"
                       "Please enter a number: ")
        print("")
        # Process player choice
        target = ""
        if not drink_choice and choice == "3":
            choice = "x"
        match choice:
            case "0":
                print_scores(scores)
                exit_game()
            case "1":
                question = random.choice(game_set['truth'])
                print(f"Truth: {question}")
            case "2":
                dare = random.choice(game_set['dare'])
                if len(players) > 2:
                    other_players = set(players) - {player} - set(eliminated)
                    target = random.choice(list(other_players))
                    print(f"Target (if applicable): {target}")
                print(f"Dare: {dare}")
            case "3":
                print("Drink a shot!")
            case _:
                print("Invalid input. Please try again.")
                continue


        # ask if player wants to continue
        print("\nPress enter to if player did the task, or anything else to eliminate the player.")
        if input() != "":
            eliminated.append(player)
        else:
            if choice == "1":
                scores[player]["truth"] += 1
                scores[player]["questions"].append(question)
            elif choice == "2":
                scores[player]["dare"] += 1
                dare = f"{dare} (Target (if applicable): {target})" if len(players) > 2 else dare
                scores[player]["dares"].append(dare)
            elif choice == "3":
                scores[player]["drink"] += 1
            turn += 1

        if len(eliminated) == len(players)-1:  # one player left
            winner = set(players) - set(eliminated)
            print(f"Gave over!\n{next(iter(winner))} is the winner!")
            print_scores(scores)
            exit_game()
