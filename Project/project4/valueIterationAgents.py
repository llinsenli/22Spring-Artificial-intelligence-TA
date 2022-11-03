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
import collections

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

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        for i in range(self.iterations):
            iterationValues = util.Counter()
            # Go through every state
            for s in self.mdp.getStates():
                # If the state is terminal, the action should be exit, the next state is None
                if self.mdp.isTerminal(s):
                    self.values[s] = self.mdp.getReward(s, 'exit', '')
                # For each state, return the max qvalue from all action
                else:
                    actions = self.mdp.getPossibleActions(s)
                    iterationValues[s] = max([self.computeQValueFromValues(s, a) for a in actions])
            self.values = iterationValues



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
        "*** YOUR CODE HERE ***"
        transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        value = 0
        for ts in transitionStatesAndProbs:
            # t[0] is the next state, t[1] is the transition probability
            stateTransitionReward = self.mdp.getReward(state, action, ts[0])
            value += stateTransitionReward + self.discount * (self.values[ts[0]] * ts[1])
        return value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # Create the action and Qvalue in a diction {'action1': Qvalue1,'action2':QValue2}
        # All keys are defaulted to have value 0
        stateAction = util.Counter()
        # Go through all possible action in currect state
        # Use the stateAction  {'action1': Qvalue1,'action2':QValue2} dictionary to store action and Qvalue
        for action in self.mdp.getPossibleActions(state):
            stateAction[action] = self.computeQValueFromValues(state, action)
        # Return the key that have the largest value in the dictionary
        best_action = stateAction.argMax()
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        mdpStates = self.mdp.getStates()
        indexIterator = 0
        for iteration in range(0, self.iterations):
            if indexIterator == len(mdpStates): indexIterator = 0
            targetState = mdpStates[indexIterator]
            indexIterator += 1
            if self.mdp.isTerminal(targetState):
                continue
            bestAction = self.computeActionFromValues(targetState)
            QValue = self.computeQValueFromValues(targetState, bestAction)
            self.values[targetState] = QValue

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        self.queue = util.PriorityQueue()
        self.predecessors = util.Counter()

        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                self.predecessors[s] = set()

        for s in self.mdp.getStates():
            if self.mdp.isTerminal(s):
                continue
            possibleActions = self.mdp.getPossibleActions(s)
            for action in possibleActions:
                nextTransitions = self.mdp.getTransitionStatesAndProbs(s, action)
                for nextState, prob in nextTransitions:
                    if prob != 0 and not self.mdp.isTerminal(nextState):
                        self.predecessors[nextState].add(s)
            currentValue = self.values[s]
            bestAction = self.computeActionFromValues(s)
            highestQValue = self.computeQValueFromValues(s, bestAction)
            diff = abs(currentValue - highestQValue)
            self.queue.push(s, -diff)

        for iteration in range(0, self.iterations):
            if self.queue.isEmpty():
                return 0

            s = self.queue.pop()
            bestAction = self.computeActionFromValues(s)
            self.values[s] = self.computeQValueFromValues(s, bestAction)

            for p in self.predecessors[s]:
                currentValue = self.values[p]
                bestAction = self.computeActionFromValues(p)
                highestQValue = self.computeQValueFromValues(p, bestAction)
                diff = abs(currentValue - highestQValue)
                if diff > self.theta:
                    self.queue.update(p, -diff)
