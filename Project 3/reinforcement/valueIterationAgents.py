# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.
        """

        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations

        # Value iteration algorithm
        states = mdp.getStates()

        dp = [util.Counter(), util.Counter()] # stores q values of kth and k - 1th iterations
        i = 0 # pointer to current iteration's q values

        for iteration in xrange(iterations + 1):
            curValues = dp[i]
            prevValues = dp[i ^ 1]
            for state in states:
                vValue, _ = self.getValueAndActionOfState(state, prevValues)
                curValues[state] = vValue
            i ^= 1

        self.values = dp[i]

    # Computes v-value of given state using k-1th vector
    def getValueAndActionOfState(self, state, previousValues):
        mdp = self.mdp
        if mdp.isTerminal(state):
            return 0, None

        mdp = self.mdp
        actions = mdp.getPossibleActions(state)
        if len(actions) == 0:
            return 0, None

        inf = 10 ** 8
        maxQValue = -inf
        for action in actions:
            curQValue = self.getQValueOfState(state, action, previousValues)
            if curQValue > maxQValue:
                maxQValue = curQValue
                bestAction = action

        return maxQValue, bestAction
        
    # Computes q-value of given state using k-1th vector or v-values
    def getQValueOfState(self, state, action, previousValues):
        mdp = self.mdp
        res = 0

        for nextState, prob in mdp.getTransitionStatesAndProbs(state, action):
            reward = mdp.getReward(state, action, nextState)
            res += prob * (reward + self.discount * previousValues[nextState])

        return res
            
        
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        return self.getQValueOfState(state, action, self.values)

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        _, bestAction = self.getValueAndActionOfState(state, self.values)
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
