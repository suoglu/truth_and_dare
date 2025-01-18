# Truth or Dare Game

## Contents of Readme

1. About
2. Usage
3. Adding new questions and dares

[![Repo on GitLab](https://img.shields.io/badge/repo-GitLab-6C488A.svg)](https://gitlab.com/suoglu/truth_and_dare)
[![Repo on GitHub](https://img.shields.io/badge/repo-GitHub-3D76C2.svg)](https://github.com/suoglu/truth_and_dare)

---

## About

Simple truth or dare game for the terminal. It is written in Python. It is a simple game that you can play with your friends.
You can add new questions and dares to the game. Game offers an optional drink mode, which adds drink option with truth and dare. 
Game keeps track of choices player make as well as dares and questions each player receive.

## Usage

Simply run the script. Follow the instructions on the screen. First you need to choose a game mode. Then enter player names. Player names must be unique. 
Each round one player has to choose, rotating in the order of giving player names. Game will present you possible choices. If you choose dare or truth,
game will randomly choose and present you with one. Then if the player does the task, press enter without entering anything. If player fails to perform, 
enter with anything other than empty entery. The player will be eliminated. When only one player stands, game is over. Or you can exit the game any time.
When the game ends; the number of each choices of players, as well as the dares and questions will be displayed.

## Adding new questions and dares

Simply add a new json file or edit one of the existing ones. Json file contains a dictionary with two keys; `truth` and `dare`. Each key contains a list of
the strings which has dares and questions. 

Example:
```json
{
    "truth": [ "question0", "question1", ... ],
    "dare": [ "dare0", "dare1", ... ]
}
```


