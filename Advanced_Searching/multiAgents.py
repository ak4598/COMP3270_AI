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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        food = newFood.asList()
        score = successorGameState.getScore()

        for f in food:
            food_distance = util.manhattanDistance(f, newPos)
            if food_distance != 0:
                score += 1/food_distance
        
        for ghost in newGhostStates:
            ghost_position = ghost.getPosition()
            ghost_distance = util.manhattanDistance(ghost_position, newPos)
            if ghost_distance > 1: 
                score += 1/ghost_distance
            else:
                score -= 99999

        # return successorGameState.getScore()
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

class MinimaxAgent(MultiAgentSearchAgent):
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
        def max_value(state, depth, agentIndex):
            depth -= 1
            if depth < 0 or state.isWin() or state.isLose():
                return (self.evaluationFunction(state), None)
            
            value = float('-inf')
            
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                score = min_value(successor, depth, agentIndex+1)[0]
                if score > value:
                    value = score
                    max_action = action

            return (value, max_action)

        def min_value(state, depth, agentIndex):
            if depth < 0 or state.isWin() or state.isLose():
                return (self.evaluationFunction(state), None)
            
            value = float('inf')
            
            if agentIndex < state.getNumAgents()-1:
                min_or_max = min_value
                next_agent = agentIndex+1
            
            else:
                min_or_max = max_value
                next_agent = 0
            
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                score = min_or_max(successor, depth, next_agent)[0]
                if score < value:
                    value = score
                    min_action = action
   
            return (value, min_action)

        return max_value(gameState, self.depth, 0)[1]

        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(state, depth, agentIndex, alpha, beta):
            depth -= 1
            if depth < 0 or state.isWin() or state.isLose():
                return (self.evaluationFunction(state), None)
            
            value = float('-inf')
            
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                score = min_value(successor, depth, agentIndex+1, alpha, beta)[0]
                if score > value:
                    value = score
                    max_action = action

                if value > beta:
                    return (value, max_action)

                if value > alpha:
                    alpha = value

            return (value, max_action)

        def min_value(state, depth, agentIndex, alpha, beta):
            if depth < 0 or state.isWin() or state.isLose():
                return (self.evaluationFunction(state), None)
            
            value = float('inf')
            
            if agentIndex < state.getNumAgents()-1:
                min_or_max = min_value
                next_agent = agentIndex+1
            
            else:
                min_or_max = max_value
                next_agent = 0
            
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                score = min_or_max(successor, depth, next_agent, alpha, beta)[0]
                if score < value:
                    value = score
                    min_action = action

                if value < alpha:
                    return(value, min_action)

                if value < beta:
                    beta = value
   
            return (value, min_action)

        alpha = float('-inf')
        beta = float('inf')
        return max_value(gameState, self.depth, 0, alpha, beta)[1]        
        # util.raiseNotDefined()
        

class ExpectimaxAgent(MultiAgentSearchAgent):
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

        def max_value(state, depth, agentIndex):
            depth -= 1
            if depth < 0 or state.isWin() or state.isLose():
                return (self.evaluationFunction(state), None)
            
            value = float('-inf')
            
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                score = exp_value(successor, depth, agentIndex+1)[0]
                if score > value:
                    value = score
                    max_action = action

            return (value, max_action)

        def exp_value(state, depth, agentIndex):
            if depth < 0 or state.isWin() or state.isLose():
                return (self.evaluationFunction(state), None)

            value = 0
            exp_action = None

            if agentIndex < state.getNumAgents()-1:
                max_or_exp = exp_value
                next_agent = agentIndex+1
            
            else:
                max_or_exp = max_value
                next_agent = 0

            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                score = max_or_exp(successor, depth, next_agent)[0]

                prob = score/len(state.getLegalActions(agentIndex))
                value += prob

            return (value, exp_action)

        return max_value(gameState, self.depth, 0)[1]

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    curr_food = currentGameState.getFood()
    curr_position = currentGameState.getPacmanPosition()
    curr_capsules = currentGameState.getCapsules()
    curr_ghost_positions = currentGameState.getGhostPositions()
    curr_scared_times = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]

    food_list = curr_food.asList()

    if len(food_list) != 0:
        closet_food_dist = min([util.manhattanDistance(curr_position, food) for food in food_list])
        food_score = 1/closet_food_dist

    else:
        food_score = 0

    if len(curr_capsules) != 0:
        closet_capsule_dist = min([util.manhattanDistance(curr_position, capsule) for capsule in curr_capsules])
        capsule_score = (1/closet_capsule_dist)*5

    else:
        capsule_score = 0


    closet_ghost_dist = min([util.manhattanDistance(curr_position, ghost_position) for ghost_position in curr_ghost_positions])
    if max(curr_scared_times) > 1:
        if closet_ghost_dist == 0:
            ghost_score = 500
        else:
            ghost_score = closet_ghost_dist
    else:
        if closet_ghost_dist == 0:
            ghost_score = -500
        else:
            ghost_score = 1/closet_ghost_dist

    return food_score + capsule_score + ghost_score + currentGameState.getScore()

    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

