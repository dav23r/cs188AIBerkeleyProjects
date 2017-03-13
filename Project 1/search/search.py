# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    from util import Stack
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """
    # Passing 'stack' to be used as fringe for generic search will result in dfs algorithm.
    return genericSearch(problem, fringe = Stack(), useCost = False)

def breadthFirstSearch(problem):
    from util import Queue
    """Search the shallowest nodes in the search tree first."""
    # Using 'queue' as a fringe will lead to breadth-first traversal.
    return genericSearch(problem, fringe = Queue(), useCost = False) 

def uniformCostSearch(problem):
    from util import PriorityQueueWithFunction as pq
    """Search the node of least total cost first."""
    # 'Priority queue' alongside with cost will work for weighted graphs as ucs
    # Function is passed to compare 'state' items by the cumulative cost from start to the state.
    func = lambda node: node.getCost() 
    return genericSearch(problem, fringe = pq(func), useCost = True) 

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial. Using this 
    heuristic essentially boils down to uniform cost search.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    from util import PriorityQueueWithFunction as pq
    """Search the node that has the lowest combined cost and heuristic first."""
    # This time function estimates cost as price from start to current node +
    # heuristical belief of cost from current to the goal state
    func = lambda node: node.getCost() + heuristic(node.getState(), problem)
    return genericSearch(problem, fringe = pq(func), useCost = True)

def dijkstraWithAllPaths(problem):
    from util import PriorityQueueWithFunction as pq
    """Same as ucs, but with paths to all states traversed, not just 'goal'."""
    func = lambda node: node.getCost()
    # the format is (dirs to goal, dict of (some state -> dirs to that state from start)
    return genericSearch(problem, fringe = pq(func), useCost = True, allStates = True)

# Searches state spaces using different traversals determined by type of 'fringe'
# If allStates is True, function will store pathes to all states not just 'goal'
def genericSearch(problem, fringe, useCost, allStates = False):
    
    # Inner class for conveniently storing search nodes
    class Node():
        def __init__(self, directions, state, cumulativeCost = None):
            self.directions = directions
            self.state = state
            if cumulativeCost != None:
                self.cumulativeCost = cumulativeCost

        getDirections = lambda self: self.directions
        getState      = lambda self: self.state
        getCost       = lambda self: self.cumulativeCost

    """
    Generic graph traversal. Depending on the fringe search will be performed
    in a particular way (dfs, bfs, A*, ucs)
    """
    # Initialize fringe with single start state, if cost is to be considered add arg
    startNodeArg = ( [], problem.getStartState() )
    if useCost: startNodeArg += (0,)
    # Asterisk unpacks arguments
    fringe.push( Node(*startNodeArg) ) # add new node to the fringe with provided args
    # Set to store already considered coords
    traversedStates = set()
    # Store (state -> cost to get there from start state) in dictionary
    if allStates:
        paths = {}

    # Do the following: extract states from fringe
    # and process them until either goal is found
    # of fringe becomes empty
    while not fringe.isEmpty():
        # Extract next 'State' object which stores directions, coord and optionally cost 
        curNode = fringe.pop()
        curState = curNode.getState()
        # If we already came across this one move to next iteration
        if curState in traversedStates:
            continue
        traversedStates.add(curState)
        # Store in the dictionary
        if allStates:
            paths[curState] = curNode.getDirections()
        # Yayy, we found it
        if problem.isGoalState(curState):
            dirs = curNode.getDirections()
            return dirs if not allStates else (dirs, paths)
        # Extend fringe with new visible states
        for successor in problem.getSuccessors(curState):
            nextState, directionToMove, price = successor    # price is used only if flag is on
            nextNodeArg = ( curNode.getDirections()[:] + [directionToMove], nextState ) # [:] deep copy
            if useCost: nextNodeArg += (curNode.getCost() + price,)
            fringe.push( Node(*nextNodeArg) ) 

    return [] if not allStates else ([], paths) # Cant reach the goal state, better stay where you are

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
