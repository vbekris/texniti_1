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
from util import Stack, Queue, PriorityQueue


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

def depthFirstSearch(problem: SearchProblem):
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

    frontier = Stack()
    explored = set()
    start = problem.getStartState() 
    
    if problem.isGoalState(start):
        return []
    
    frontier.push( (start, [] , 0) ) #state, path, cost
        
    while not frontier.isEmpty():
        
        state, path, cost = frontier.pop()
        
        if problem.isGoalState(state):
            return path
        if state not in explored:
            explored.add(state)
            for nextState, action, stepCost in problem.getSuccessors(state):
                if nextState not in explored:
                    newState = nextState    
                    new_path = path + [action]
                    newCost = cost + stepCost
                    frontier.push((newState, new_path, newCost))
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = Queue()
    explored = set()
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []
    frontier.push( (start, [] , 0) ) #state, path, cost
    while not frontier.isEmpty():
        
        state, path, cost = frontier.pop()
        
        if problem.isGoalState(state):
            return path
        if state not in explored:
            explored.add(state)
            for nextState, action, stepCost in problem.getSuccessors(state):
                if nextState not in explored:
                    newState = nextState    
                    new_path = path + [action]
                    newCost = cost + stepCost
                    frontier.push((newState, new_path, newCost))
    return []
    

def uniformCostSearch(problem):

    frontier = PriorityQueue()  #to programma termatizei eite otan gemisei to pque mono me diafoertika paths pros to goal eite otan adeiasei kai den yparxei lysi
    explored = set()
    best_g = {}

    start = problem.getStartState()
    # edge case: start is goal
    if problem.isGoalState(start):
        return []

    # αρχικοποίηση
    frontier.push( (start, [], 0),  priority = 0 )  
    best_g[start] = 0

    while not frontier.isEmpty():
        state, path, cost = frontier.pop()

        # skip αν έχουμε ήδη βρει καλύτερο g για αυτό το state
        if best_g.get(state, float("inf")) < cost:
            continue

        if problem.isGoalState(state):  # 
            return path  # path

        if state in explored:
            continue
        explored.add(state)

        for (nextState, action, stepCost) in problem.getSuccessors(state):
            newCost = cost + stepCost
            # αν είναι η πρώτη φορά ή βρήκαμε φθηνότερο μονοπάτι
            if newCost < best_g.get(nextState, float("inf")):
                best_g[nextState] = newCost
                newPath = path + [action]
                frontier.push( (nextState, newPath, newCost), priority = newCost )  # 

    return []  # αν δεν υπάρχει λύση


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest#
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = PriorityQueue()
    expl = set()     #explored κομβοι
    best_g = {}
    
    
    start = problem.getStartState()
    frontier.push( (start, [], 0), priority = heuristic(start, problem) )
    best_g[start] = 0
    
    
    if problem.isGoalState(start):
        return []
    while not frontier.isEmpty():
        state, path, cost = frontier.pop()
        
        
        if(problem.isGoalState(state)):
            return path
        if state in expl:
            
            
            continue
        expl.add(state)
        
        
        for nextState, action, stepCost in problem.getSuccessors(state):
            newCost = cost + stepCost
            
            
            if newCost < best_g.get(nextState, float("inf")): #το απειρο ειναι default key σε dictionary
                best_g[nextState] = newCost
                newPath = path + [action]
                f = newCost + heuristic(nextState, problem)
                frontier.push( (nextState, newPath, newCost), priority = f )
    
    return []  # αν δεν υπάρχει λύση    
        

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch