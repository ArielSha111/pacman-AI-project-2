# pacman-AI-project-2
In this project i have used common AI algorithms for a version of Pacman, including ghosts. using the base of AI algoritems.
Most of the code was written by the University of Berkeley except for the various search algorithms.

* the original source is: [pacman project 2](https://inst.eecs.berkeley.edu/~cs188/fa20/project2/)

# Introduction
Welcome to Multi-Agent Pacman In this project, Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently using general search algorithms and using them on verius Pacman scenarios.

# Download
1. Make sure to have any version of python 3.
1. Download the full repository.
1. In order to view the code - open the files on your python ide of choice.
1. Go over to cmd where the downloaded files are located.
1. Type the following commend to see it all works: python pacman.py


# How to play
1. Open the CMD on the path of the downloaded files
1. Type: python pacman.py
1. Use your keyboard to move the Pacman.
1. Make sure to not let pacman lose many points since the game will be over.

## Now, run the provided ReflexAgent in multiAgents.py
1. Type: python pacman.py -p ReflexAgent
1. 

**Note that it plays quite poorly even on simple layouts**

For example type: python pacman.py -p ReflexAgent -l testClassic


# AI algorithms and commands

**Open the CMD on the path of the downloaded files and then type any of commends that will be presented.**

**at any point if Pacman gets stuck, you can exit the game by type CTRL-c .**


> Note that pacman.py supports a number of options that can each be expressed in a long way (e.g. , --layout) or a short way (e.g., -l). You can see the list of all options and their default values via the next commend:
python pacman.py -h
---

## Reflex Agent
Improve the ReflexAgent in multiAgents.pyto play respectably. The provided reflex agent code provides some helpful examples of methods that query the GameState for information. A capable reflex agent will have to consider both food locations and ghost locations to perform well. Your agent should easily and reliably clear the testClassic layout:
1. Type : python pacman.py -p ReflexAgent -l testClassic
1. Type : python pacman.py --frameTime 0 -p ReflexAgent -k 1
1. Type : python pacman.py --frameTime 0 -p ReflexAgent -k 2

# MiniMax algorithm
1. Type : python autograder.py -q q2
1. Type : python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
1. Type : python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3

# Alpha-Beta Pruning algorithm
The AlphaBetaAgent minimax values should be identical to the MinimaxAgent minimax values, although the actions it selects can vary because of different tie-breaking behavior. Again, the minimax values of the initial state in the minimaxClassic layout are 9, 8, 7 and -492 for depths 1, 2, 3 and 4 respectively.
1. Type : python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
1. Type : python autograder.py -q q3
1. Type :

# Expectimax algorithm
As with the search and constraint satisfaction problems covered so far in this class, the beauty of these algorithms is their general applicability. To expedite your own development, we’ve supplied some test cases based on generic trees.
1. Type : python autograder.py -q q4
1. Type : python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
1. Type : python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
1. Type : python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10

# Evaluation Function
The autograder will run your agent on the smallClassic layout 10 times.
1. Type : python autograder.py -q q5

# viewing the code
## the main code that was not given and needed to be written by me located in the next filles:
1. search.py
1. searchAgent.py

## Files you might want to look at:
1. pacman.py
1. game.py
1. util.py
