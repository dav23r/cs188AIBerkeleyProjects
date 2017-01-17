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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        
        mdist = util.manhattanDistance
        def lenToClosest(pos, positionsList):
            if len(positionsList) == 0:
                return 0
            return min( mdist(pos, p) for p in positionsList )
   
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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPositions = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # dimensions of table
        walls = successorGameState.getFood()
        maxManhDist = walls.width + walls.height

        # coefficients
        highC, mediumC, lowC = 10, 8, 5 
        highC *= maxManhDist
        # hazardous distance between pacman and ghost
        hazDist = 5

        heuristic = 0
        # Heuristic of the state is inversely proportional to the num of remaining food units
        heuristic -= highC * len(newFood)
        # Also, make value to be inversely related to length to the closest food
        heuristic -= lowC * lenToClosest(newPos, newFood)
        # We are afraid of ghost, so don't let them come too close
        heuristic += highC * min( lenToClosest(newPos, newGhostPositions), hazDist )
        # It's nice to scare ghost along the way
        heuristic += mediumC * sum(newScaredTimes)

        return heuristic

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

class MinimaxAgent(MultiAgentSearchAgent):

    '''
    Implements query for nextAction of MinimaxAgent
    '''
    def getAction(self, gameState):

        # Returns a direction the agent should follow determined by exploring
        # nodes up to 'depthToExplore'. Implements miniMax algorithm
        def miniMax(currentGameState, curAgentIndex, curDepth = 0):
            
            if curDepth == depthToExplore:
                return (self.evaluationFunction(currentGameState), Directions.STOP)

            # Decide on whether minimization or maximization should be performed
            aggregator = max if curAgentIndex == 0 else min 
            
            nextAgentIndex = (curAgentIndex + 1) % numAgents
            nextDepth = curDepth + 1
            # format of childNode: (value associated, direction to move)
            childNodes = []
            for action in currentGameState.getLegalActions(curAgentIndex):
                succGameState = currentGameState.generateSuccessor( curAgentIndex, action )
                valueAfterAction, _ = miniMax( succGameState, nextAgentIndex, nextDepth ) # ignore 'next action'
                childNodes.append( (valueAfterAction, action) )

            # If the are no transitions, evaluate the state using approximate function
            if len(childNodes) == 0:
                return (self.evaluationFunction(currentGameState), Directions.STOP)

            return aggregator( childNodes, key = lambda rv: rv[0] ) # sort nodes by 'value'
            

        numAgents = gameState.getNumAgents()
        depthToExplore = self.depth * numAgents
        
        # It's pacman's turn first
        bestValue, action = miniMax(gameState, 0) 
        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    
    '''
    Implements query for nextAction of AlphaBetaAgent
    '''
    def getAction(self, gameState):

        infinity = 10 ** 7

        # Returns a direction the agent should follow determined by exploring
        # nodes up to 'depthToExplore'. Implements miniMax with alphaBeta algorithm
        def alphaBeta(currentGameState, curAgentIndex, curDepth, alpha, beta):

            if curDepth == depthToExplore:
                return (self.evaluationFunction(currentGameState), Directions.STOP)

            # Decide on whether minimization or maximization should be performed
            toMaximize = (curAgentIndex == 0)

            legalActions = currentGameState.getLegalActions(curAgentIndex)
            if len(legalActions) == 0:
                return (self.evaluationFunction(currentGameState), Directions.STOP)
            
            nextAgentIndex = (curAgentIndex + 1) % numAgents
            nextDepth = curDepth + 1

            # Traverse child nodes, keeping track of alpha/beta
            v = - infinity if toMaximize else infinity
            bestAction = -1
            for action in legalActions:
                succGameState = currentGameState.generateSuccessor( curAgentIndex, action )
                valueAfterAction, _ = alphaBeta( succGameState, nextAgentIndex, nextDepth, alpha, beta )
                
                if toMaximize:
                    if valueAfterAction > v:
                        v = valueAfterAction
                        bestAction = action
                    if v > beta:
                        return (v, bestAction)
                    alpha = max(v, alpha)
                else:
                    if valueAfterAction < v:
                        v = valueAfterAction
                        bestAction = action
                    if v < alpha:
                        return (v, bestAction)
                    beta = min(v, beta)

            return (v, bestAction)
            

        numAgents = gameState.getNumAgents()
        depthToExplore = self.depth * numAgents
        
        # It's pacman's turn first
        bestValue, bestAction = alphaBeta(gameState, 0, 0, -infinity, infinity)
        return bestAction



class ExpectimaxAgent(MultiAgentSearchAgent):

    '''
    Implements query for nextAction of ExpectimaxAgent
    '''
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        dummyDir = "doesn't matter"
        def expectiMax(currentGameState, curAgentIndex, curDepth = 0):

            if curDepth == depthToExplore:
                return (self.evaluationFunction(currentGameState), Directions.STOP)

            # Decide who's turn is right now, pacman will just maximize utility,
            # ghost on the other hand will average out values of successor states
            pacmansMove = (curAgentIndex == 0) 
            
            nextAgentIndex = (curAgentIndex + 1) % numAgents
            nextDepth = curDepth + 1
            # format of childNode: (value associated, direction to move)
            childNodes = []
            for action in currentGameState.getLegalActions(curAgentIndex):
                succGameState = currentGameState.generateSuccessor( curAgentIndex, action )
                valueAfterAction, _ = expectiMax( succGameState, nextAgentIndex, nextDepth ) # ignore 'next action'
                childNodes.append( (valueAfterAction, action) )

            # If the are no transitions, evaluate the state using approximate function
            if len(childNodes) == 0:
                return (self.evaluationFunction(currentGameState), Directions.STOP)

            if pacmansMove:
                return max( childNodes, key = lambda node: node[0] ) # maximize value
            # Things are bit more complex if ghost is about to play
            valuesOfChildren = map(lambda x: x[0], childNodes) # extract values
            return ( sum(valuesOfChildren) / float(len(valuesOfChildren)), dummyDir )

        numAgents = gameState.getNumAgents()
        depthToExplore = self.depth * numAgents
        
        # It's pacman's turn first
        bestValue, action = expectiMax(gameState, 0) 
        return action
   
    
def betterEvaluationFunction(currentGameState):
    from random import randint
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 
      Here are parameters we take into account:
      num of left food units (invesely proportional with high coefficient)
      min distance to ghost if it's less than 'hazDist' (proportional with high coefficient)
      min distance to closest food unit (inversely proportional with moderate coef.)
      score retrieved from GameState obj (positively related)
      the time ghost will remain scared  (positively related, low coef.)
      Finally some randomness is added as an attempt to build better (on average) 
      tiebreaker. Without that randomness you will observe seemingly odd behaviour
      of pacman with shallow MinMax search.
    """
    mdist = util.manhattanDistance
    def lenToClosest(pos, positionsList):
        if len(positionsList) == 0:
            return 0
        return min( mdist(pos, p) for p in positionsList )

    # Useful information you can extract from a GameState (pacman.py)
    pacmanPos = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    ghostPositions = currentGameState.getGhostPositions()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    # dimensions of table
    walls = currentGameState.getFood()
    maxManhDist = walls.width + walls.height
    score = currentGameState.getScore()

    # coefficients
    closestGhostC  = 70
    eatC           = 60
    closestFoodC   = 50
    scaredTimeC    = 40
    scoreC         = 30
    
    eatC *= maxManhDist
    closestGhostC *= maxManhDist 

    # hazardous distance between pacman and ghost
    hazDist = 2

    heuristic = 0
    # Heuristic of the state is inversely proportional to the num of remaining food units
    heuristic -= eatC * len(foodPos)
    # Also, make value to be inversely related to length to the closest food
    heuristic -= closestFoodC * lenToClosest(pacmanPos, foodPos)
    # We are afraid of ghost, so don't let them come too close
    heuristic += eatC * min( lenToClosest(pacmanPos, ghostPositions), hazDist )
    # The higher score the better
    heuristic += scoreC * score
    # It's nice to scare ghost along the way
    heuristic += scaredTimeC * sum(scaredTimes)

    heuristic += randint(1, 2) # blend in some randomness

    return heuristic

# Abbreviation
better = betterEvaluationFunction

