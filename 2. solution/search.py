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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    st = util.Stack()
    st.push(problem.getStartState())

    visited = set()
    

    action_list = []

    parent = {}

    last = 0

    while not st.isEmpty():
        v = st.pop()
        visited.add(v)

        if problem.isGoalState(v):
            last = v
            break

        for (next_state, action, cost) in problem.getSuccessors(v):
            if next_state not in visited:
                st.push(next_state)
                parent[next_state] = (v, action)

    return get_actions(last, parent)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
  
    st = util.Queue()
    st.push(problem.getStartState())

    visited = set()
    visited.add(problem.getStartState())

    action_list = []

    parent = {}

    last = 0

    while not st.isEmpty():
        v = st.pop()

        if problem.isGoalState(v):
            last = v
            break

        for (next_state, action, cost) in problem.getSuccessors(v):
            if next_state not in visited:
                st.push(next_state)
                visited.add(next_state)
                parent[next_state] = (v, action)

    return get_actions(last, parent)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    pq = util.PriorityQueue()
    pq.push(problem.getStartState(), 0)

    action_list = []
    dist = {}
    parent = {}
    last = 0

    dist[problem.getStartState()] = 0

    while not pq.isEmpty():
        v = pq.pop()

        if problem.isGoalState(v):
            last = v
            break

        for (next_state, action, cost) in problem.getSuccessors(v):
            if (next_state not in dist.keys() ) or dist[next_state] > dist[v] + cost:
                pq.update(next_state, dist[v] + cost)
                dist[next_state] = dist[v] + cost
                parent[next_state] = (v, action)


    return get_actions(last, parent)
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    pq = util.PriorityQueue()
    
    action_list = []
    f = {}
    g = {}
    parent = {}
    last = 0

    f[problem.getStartState()] = heuristic(problem.getStartState(), problem)
    g[problem.getStartState()] = 0

    open_set = set()
    closed_set = set()

    open_set.add(problem.getStartState())
    pq.update(problem.getStartState(), f[problem.getStartState()])

    while not pq.isEmpty():
        v = pq.pop()

        if problem.isGoalState(v):
            last = v
            break

        closed_set.add(v)
        open_set.remove(v)

        for (next_state, action, cost) in problem.getSuccessors(v):

            if next_state in closed_set:
                continue

            if next_state not in open_set  or g[next_state] > g[v] + cost:
                
                g[next_state] = g[v] + cost
                f[next_state] = g[next_state] + heuristic(next_state, problem)
                parent[next_state] = (v, action)
                open_set.add(next_state)
                pq.update(next_state, f[next_state])

    return get_actions(last, parent)
    


def get_actions(last, parent):
    action_list = []
    while(last in parent.keys()):
        (pi, act) = parent[last]
        last = pi
        action_list.append(act)

    action_list.reverse()
    return action_list

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
