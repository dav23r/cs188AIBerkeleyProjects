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
    all_nodes = util.Stack()

    all_nodes.push([problem.getStartState(), []])
    been = set()

    while not all_nodes.isEmpty():
        curr_node = all_nodes.pop()
        st, movements = curr_node

        if problem.isGoalState(st):
            return movements

        if st not in been:
            been.add(st)

            for neighbor in problem.getSuccessors(st):
	        copy = neighbor[0], movements[:] + [neighbor[1]]
	        all_nodes.push(copy)

    return []


def breadthFirstSearch(problem):
    all_nodes = util.Queue()

    all_nodes.push([problem.getStartState(), []])
    been = set()

    while not all_nodes.isEmpty():
        curr_node = all_nodes.pop()
        st, movements = curr_node

        if problem.isGoalState(st):
            return movements

        if st not in been:
            been.add(st)

            for neighbor in problem.getSuccessors(st):
	        copy = neighbor[0], movements[:] + [neighbor[1]]
	        all_nodes.push(copy)

    return []

def calculate_priority(path):
    i = 0
    for bridge in path:
        i += bridge[2]

    return i

def uniformCostSearch(problem):
    all_nodes = util.PriorityQueueWithFunction(lambda n: n[2]) # compare by cost

    all_nodes.push([problem.getStartState(), [], 0]) # cost of 0 initially
    been = set()

    while not all_nodes.isEmpty():
        curr_node = all_nodes.pop()
        st, movements, cost = curr_node

        if problem.isGoalState(st):
            return movements

        if st not in been:
            been.add(st)

            for neighbor in problem.getSuccessors(st):
	        copy = neighbor[0], movements[:] + [neighbor[1]], neighbor[2] + cost
	        all_nodes.push(copy)

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def fn(path):
    i = 0
    for bridge in path:
        i += bridge[2]

    return i + path[len(path)-1][3]

def aStarSearch(problem, heuristic=nullHeuristic):
    
    startState = problem.getStartState()
    h = heuristic
    # compare by cost to achive that state + heuristic value there
    all_nodes = util.PriorityQueueWithFunction(lambda n: n[2] + h(n[0], problem)) 

    all_nodes.push([startState, [], 0]) # cost of 0 initially
    been = set()

    while not all_nodes.isEmpty():
        curr_node = all_nodes.pop()
        st, movements, cost = curr_node

        if problem.isGoalState(st):
            return movements

        if st not in been:
            been.add(st)

            for neighbor in problem.getSuccessors(st):
	        copy = neighbor[0], movements[:] + [neighbor[1]], neighbor[2] + cost
	        all_nodes.push(copy)

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
