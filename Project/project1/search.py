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
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    start = (problem.getStartState(), [])
        # the stack is for the LIFO method since it is DFS
    fringe = util.Stack()
    fringe.push(start)
        #need to keep a set of the nodes that are visited
    visited = set()

    while fringe.isEmpty() == False: #first have to check that there are nodes in the fringe
        #remove the top node n from the fringe
        n = fringe.pop() #pop gets rid of the most recently added thing to the stack
        if problem.isGoalState(n[0]) == True: #need to check if n is the state that is the goal state
            return n[1] #returns the path to the current goal state
        elif (n[0] not in visited): #if its been visited, skip
            visited.add(n[0]) #add it to the set

            for i in problem.getSuccessors(n[0]): #get the nodes from the fringe
                currentState = i[0] #where we are visiting right now
                currentPath = n[1] #the path that we know and already exists
                newPath = [i[1]] #the direction to the child from the parent
                oldPath = currentPath+newPath #need to add the two to get path from parent to child
                nextNode = (currentState, oldPath)
                fringe.push(nextNode) #adds the node we just created to the stack

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = (problem.getStartState(), [])
    #now it is FIFO for BFS
    fringe = util.Queue()
    fringe.push(start)
    # need to keep a set of the nodes that are visited
    visited = set()

    while fringe.isEmpty() == False:  # first have to check that there are nodes in the fringe
        # remove the top node n from the fringe
        n = fringe.pop()  # pop gets rid of the most recently added thing to the stack
        if problem.isGoalState(n[0]) == True:  # need to check if n is the state that is the goal state
            return n[1]  # returns the path to the current goal state
        elif (n[0] not in visited):  # if its been visited, skip
            visited.add(n[0])  # add it to the set

            for i in problem.getSuccessors(n[0]):  # get the nodes from the fringe
                currentState = i[0]  # where we are visiting right now
                currentPath = n[1]  # the path that we know and already exists
                newPath = [i[1]]  # the direction to the child from the parent
                oldPath = currentPath + newPath  # need to add the two to get path from parent to child
                nextNode = (currentState, oldPath)
                fringe.push(nextNode)  # adds the node we just created to the stack

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    start = (problem.getStartState(), [], 0)
    # now it is a priority queue for UCS because you can retrieve specific pairs
    fringe = util.PriorityQueue()
    fringe.push(start, 1)
    # need to keep a set of the nodes that are visited
    visited = set()

    while fringe.isEmpty() == False:  # first have to check that there are nodes in the fringe
        # remove the top node n from the fringe
        n = fringe.pop()  # pop gets rid of the most recently added thing to the stack
        if problem.isGoalState(n[0]) == True:  # need to check if n is the state that is the goal state
            return n[1]  # returns the path to the current goal state
        elif (n[0] not in visited):  # if its been visited, skip
            visited.add(n[0])  # add it to the set

            for i in problem.getSuccessors(n[0]):  # get the nodes from the fringe
                currentState = i[0]  # where we are visiting right now
                currentPath = n[1]  # the path that we know and already exists
                newPath = [i[1]]  # the direction to the child from the parent
                oldPath = currentPath + newPath # need to add the two to get path from parent to child
                cost = i[2]
                nextCost = cost + n[2]
                nextNode = (currentState, oldPath, nextCost)
                fringe.push(nextNode, nextCost)  # adds the node we just created to the stack


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
