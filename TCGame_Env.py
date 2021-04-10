#from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product

# Important functions:
# 1. is_winning()  - Takes in current state and returs True if there is a winning position in the board
# 2. is_terminal() - Modified this from the starter code to include player name (agent or env), 
#                    so that it can return "Win" or "Lose" depending on which player won the game
# 3. state_transition() - will return the next state after taking the specified action
# 4. step() - Updates the state with the specified action from agent, check if terminal state
#            if so, return the state, reward(using the return value from is_terminal & reward dict) and terminal status = True
#            if agent action is not terminal, take env action, and check is_terminal() and return similar values as above.
# 
# Reward Structure:
#  Is defined as a dictionary in the __init__, this is used as a lookup in step() function

class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array, board position when we start the game
        self.state = [np.nan for _ in range(9)]  
        
        # Define all possible values that can be used in the game
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] 
        
        # Define Reward structure
        self.reward = {'Win':10, 'Lose':-10, 'Tie':0, 'Resume':-1}
        
        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        
        # Define all possible winning positions
        win_pos=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        
        # Check any of the winning positions have numbers adding up to 15
        for pos in win_pos:
            if np.sum([curr_state[p] for p in pos]) == 15:
                return True
        return False

    def is_terminal(self, curr_state, player):
        # Terminal state could be winning state or when the board is filled up
        
        # Depending on which player is winning, return 'Win' if Agent won, or 'Lose' if env won the game
        if self.is_winning(curr_state) == True:
            if player == 'env':
                return True, 'Lose'
            else:
                return True, 'Win'

        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'

        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, 
        i.e, all combinations of allowed positions and allowed values"""

        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)



    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        curr_state[curr_action[0]]=curr_action[1]
        return(curr_state)
        

    def step(self, curr_state,curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. 
        Hint: First, check the board position after agent's move, whether the game is won/loss/tied. 
        Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""
        
        # Additional check to ensure we don't continue with a game already completed
        term=self.is_terminal(curr_state,'env')
        
        if term[0] == False:
            if curr_action not in [act for act in self.action_space(self.state)[0]]:
                raise Exception("Action not allowed")
            self.state = self.state_transition(self.state, curr_action)
            term=self.is_terminal(curr_state,'agent')
            
            # If we finished the game with agent's move, return state, reward=10 if won, reward=0 if Tied
            if term[1] != 'Resume':
                return(self.state,self.reward[term[1]],term[1]) 
            
            # Make a move from enviroment and return state
            act_env=random.choice( [act for act in self.action_space(self.state)[1]])
            self.state = self.state_transition(self.state, act_env)
            term=self.is_terminal(curr_state,'env')
            return(self.state,self.reward[term[1]],term[0]) 
        else:
            raise Exception("Game already completed")
            
    def reset(self):
        """ Reset board position to start again"""
        self.state = [np.nan for _ in range(9)]  
        return self.state
