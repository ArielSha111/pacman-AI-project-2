# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition() # a (x, y)  like (6, 6)#
        newFood = successorGameState.getFood() # a matrix of booleans for all the food spots note you can use aslist() as well#
        newGhostStates = successorGameState.getGhostStates() # a game states of a ghost its iterable
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # a list of all the ghost states timers
        "*** YOUR CODE HERE ***"
        # we gonna take two factors in our mind
        # first is how threaten the pacmen is, if he is then we gonna take numbers of score
        # second is how much food is left, we gonna remove a factor of this amount from the score

        score = successorGameState.getScore()  # a number like 198.00 its basically what is the rate of the state#
        if newGhostStates:#if there are ghosts#
            min_ghost_distance = 999999
            for item in newGhostStates:
                cur_distance = manhattanDistance(newPos, item.getPosition())
                if cur_distance < min_ghost_distance:
                    min_ghost_distance = cur_distance
        score += min_ghost_distance# the farthest this ghost the higher score will be

        new_food_list = newFood.asList()
        min_food_distance = 999999
        value_of_food = 0
        if new_food_list:
            for item in new_food_list:
                if item: #count all the food that is true in the food metrix#
                    cur_distance = manhattanDistance(newPos, item)
                    value_of_food += 5 # give the food that left the highest value
                    if cur_distance < min_food_distance:
                        min_food_distance = cur_distance
            score -= (min_food_distance + value_of_food) # we consider both the distance of the closest
        # food and the amount of food left

        old_capsules = currentGameState.getCapsules()
        closest_capsules = 0
        if old_capsules:
            capsules_distances_list = []
            for item in old_capsules:
                capsules_distances_list.append(util.manhattanDistance(newPos, item))
            closest_capsules = min(capsules_distances_list)
        score -= (closest_capsules * 5)# the closest a capsule is the the bigger score will be

        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgentX(MultiAgentSearchAgent):

    def miniMax(self, gameState, depth, agent):
        val_and_act = [None] * 2  # crating the result list #
        # the first part and end of recursion #
        #############################################################################################################
        if depth == 0 or gameState.isWin() or gameState.isLose(): #if its the leafs or the end of the game#
            val_and_act[0] = self.evaluationFunction(gameState)  # then add to val_and_act the value of this gameState #
            val_and_act[1] = None  # then add the val_and_act the action 0 #
            return val_and_act
        #############################################################################################################

        #meangenig the ghosts and pacman#
        ############################################
        if agent == gameState.getNumAgents() - 1:#if we got to each ghost and to pacman we can move to the next depth with the first agent#
            depth -= 1 #the we finished this layer to all ghosts add 1 to the depth #
            new_agent = 0 #initilize the agent count#
        else:#stil not the last agent we can move to the next one#
            new_agent = agent + 1 #move to the next agent#
        ############################################

        # loop on each son of the tree and check it#
        ###############################################################################################################
        legal_actions = gameState.getLegalActions(agent) #getting all the legal actions for this gameState #
        for item in legal_actions: #loop on each action from the legal actions which is all the sons of the agent#
            successor = gameState.generateSuccessor(agent, item) #create a successor for the game state of agent to the action node #
            successor_value = self.miniMax(successor, depth, new_agent) #the next value is the miniMax value of the successor in that depth with the next agent #
            if not val_and_act[0] and not val_and_act[1] : #if the val_and_act is empty then we can check all the next parts we gotta make sure it ain't empty#
                val_and_act[0] = successor_value[0] #then add to result the value of next value #
                val_and_act[1] = item #then add the val_and_act the action #
            else: #if there is a val_and_act already #
                # the min max checks #
                #####################################################################################################
                previous_value = val_and_act[0] #just getting the  value of the previous action #
                if agent == 0 and successor_value[0] > previous_value: #if its pacman the its max player #
                    val_and_act[0] = successor_value[0] #setting the result to be with the next value of the action #
                    val_and_act[1] = item #setting the result to be with the next action #
                elif agent != 0 and successor_value[0] < previous_value: #if its not pacman then its min player then we check the check of min node#
                    val_and_act[0] = successor_value[0]  # setting the result to be with the next value of the action #
                    val_and_act[1] = item  # setting the val_and_act to be with the next action #
                #####################################################################################################
        ###############################################################################################################
        return val_and_act

    """
     Your minimax agent (question 2)
     """

    def getAction(self, gameState):
        """
           Returns the minimax action from the current gameState using self.depth
           and self.evaluationFunction.

           Here are some method calls that might be useful when implementing minimax.

           gameState.getLegalActions(agentIndex):
           Returns a list of legal actions for an agent
           agentIndex=0 means Pacman, ghosts are >= 1

           gameState.generateSuccessor(agentIndex, action):
           Returns the successor game state after an agent takes an action

           gameState.getNumAgents():
           Returns the total number of agents in the game

           gameState.isWin():
           Returns whether or not the game state is a winning state

           gameState.isLose():
           Returns whether or not the game state is a losing state
           """
        "*** YOUR CODE HERE ***"
        val_and_act = self.miniMax(gameState, self.depth, 0)
        action = val_and_act[1]
        return action

class AlphaBetaAgentX(MultiAgentSearchAgent):
    def AlphaBetaMiniMax(self, gameState, depth, agent, alpha, beta):
        val_and_act = [None] * 2  # crating the result list #
        # the first part and end of recursion #
        #############################################################################################################
        if depth == 0 or gameState.isWin() or gameState.isLose(): #if its the leafs or the end of the game#
            val_and_act[0] = self.evaluationFunction(gameState)  # then add to val_and_act the value of this gameState #
            val_and_act[1] = None  # then add the val_and_act the action 0 #
            return val_and_act
        #############################################################################################################

        #meangenig the ghosts and pacman#
        ############################################
        if agent == gameState.getNumAgents() - 1:#if we got to each ghost and to pacman we can move to the next depth with the first agent#
            depth -= 1 #the we finished this layer to all ghosts add 1 to the depth #
            new_agent = 0 #initilize the agent count#
        else:#stil not the last agent we can move to the next one#
            new_agent = agent + 1 #move to the next agent#
        ############################################

        # loop on each son of the tree and check it#
        ###############################################################################################################
        for item in gameState.getLegalActions(agent):
            if not val_and_act[0] and not val_and_act[1] : #if the val_and_act is empty then we can check all the next parts we gotta make sure it ain't empty#
                #we can be sure now that no cuting is needed for the tree then we can create the successor#
                successor = gameState.generateSuccessor(agent, item)  # create a successor for the game state of agent to the action node #
                successor_value = self.AlphaBetaMiniMax(successor, depth, new_agent, alpha, beta)  # the next value is the miniMax value of the successor in that depth with the next agent #
                val_and_act[0] = successor_value[0] #then add to result the value of next value #
                val_and_act[1] = item #then add the val_and_act the action #
            else:  # if there is a val_and_act already #
                # the min max checks #
                #####################################################################################################
                if val_and_act[0] > beta and agent == 0:
                    return val_and_act
                if val_and_act[0] < alpha and agent != 0:
                    return val_and_act
                # only when we sure that no cutting is needed then we can create the successors
                successor = gameState.generateSuccessor(agent, item)  # create a successor for the game state of agent to the action node #
                successor_value = self.AlphaBetaMiniMax(successor, depth, new_agent, alpha, beta)  # the next value is the miniMax value of the successor in that depth with the next agent #
                previous_value = val_and_act[0]
                if agent == 0 and successor_value[0] > previous_value: #if its pacman the its max player #
                    val_and_act[0] = successor_value[0] #setting the result to be with the next value of the action #
                    val_and_act[1] = item #setting the result to be with the next action #
                elif agent != 0 and successor_value[0] < previous_value:  # if its not pacman then its min player then we check the check of min node#
                    val_and_act[0] = successor_value[0]  # setting the result to be with the next value of the action #
                    val_and_act[1] = item  # setting the val_and_act to be with the next action #
                #####################################################################################################
            #now we can finally check the alpha and beta#
            if agent == 0:  # if its pacman then its max node#
                if alpha < val_and_act[0]:
                    alpha = val_and_act[0]  # act for the max nodes#
            else:
                if beta > val_and_act[0]:
                    beta = val_and_act[0]  # act for the min nodes#
        ###############################################################################################################
        return val_and_act

    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
          """
        "*** YOUR CODE HERE ***"
        val_and_act = self.AlphaBetaMiniMax(gameState, self.depth, 0, -999999, 999999)
        action = val_and_act[1]
        return action

class ExpectimaxAgentX(MultiAgentSearchAgent):

    def expectiMax(self, gameState, depth, agent):
        val_and_act = [None] * 2  # crating the result list #
        # the first part and end of recursion #
        #############################################################################################################
        if depth == 0 or gameState.isWin() or gameState.isLose(): #if its the leafs or the end of the game#
            val_and_act[0] = self.evaluationFunction(gameState)  # then add to val_and_act the value of this gameState #
            val_and_act[1] = None  # then add the val_and_act the action 0 #
            return val_and_act
        #############################################################################################################

        #meangenig the ghosts and pacman#
        ############################################
        if agent == gameState.getNumAgents() - 1:#if we got to each ghost and to pacman we can move to the next depth with the first agent#
            depth -= 1 #the we finished this layer to all ghosts add 1 to the depth #
            new_agent = 0 #initilize the agent count#
        else:#stil not the last agent we can move to the next one#
            new_agent = agent + 1 #move to the next agent#
        ############################################


        # loop on each son of the tree and check it#
        ###############################################################################################################

        agent_actions = gameState.getLegalActions(agent)
        successors_values_list = []
        for item in agent_actions:
            successor = gameState.generateSuccessor(agent, item)  # create a successor for the game state of agent to the action node #
            successor_value = self.expectiMax(successor, depth, new_agent)  # the next value is the miniMax value of the successor in that depth with the next agent #
            if not val_and_act[0] and not val_and_act[1] : #if the val_and_act is empty then we can check all the next parts we gotta make sure it ain't empty#
                if (agent == 0): #if its pacmen#
                    val_and_act[0] = successor_value[0]
                    val_and_act[1] = item  # the item is the same then do it either way#
                else: #else its a ghost#
                    #we gonna add to part_of_expectancy each of the successor_value divided by the ammount of ghost#
                    #since we gonna do it with it ghost and sum this up we gonna get the expectancy#
                    successors_values_list.append(successor_value[0])
            else:  # if there is a val_and_act already #
            #####################################################################################################
                previous_value = val_and_act[0] #just getting the  value of the previous action #
                if agent == 0 and successor_value[0] > previous_value: #if its pacman the its max player #
                    val_and_act[0] = successor_value[0]
                    val_and_act[1] = item
                #we gonna add to part_of_expectancy each of the successor_value divided by the ammount of ghost#
                #since we gonna do it with it ghost and sum this up we gonna get the expectancy#
                elif agent != 0:  # if its not pacman then its a ghost#
                    successors_values_list.append(successor_value[0])
                #####################################################################################################
        ###############################################################################################################
        if agent != 0: #if its not pacmen then the loop was for ghosts and successors_values_list been appended#
            val_and_act[0] = sum(successors_values_list)/float(len(successors_values_list)) #the way i calculate expectancy#
            val_and_act[1] = None #the action is not relevant - all of actions have the same value the expectancy#
            return val_and_act

        return val_and_act#if its pacmen return the needed value#

    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        val_and_act = self.expectiMax(gameState, self.depth, 0)
        action = val_and_act[1]
        return action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    this function based upon the amount of food left on the game
    its works very much like the evaluationFunction of the reflex agent
    but now checks all the distances from a current position and not from
    the next one
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    food = currentGameState.getFood()
    position = currentGameState.getPacmanPosition()  # a (x, y)  like (6, 6)#

    food_list = food.asList()
    min_food_distance = 999999
    if food_list:
        for item in food_list: #check every food that's left in the game#
            cur_distance = manhattanDistance(position, item) #calculate the distance from the current position to that food#
            if cur_distance < min_food_distance:
                min_food_distance = cur_distance
        score -= min_food_distance  # we consider both the distance of the closest
    # food and the amount of food left
    return score #score will be based upon the nearest food the nearest food is the highest value for the curent position#

# Abbreviation
better = betterEvaluationFunction

