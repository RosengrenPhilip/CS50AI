"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy, copy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board) -> str:
    """
    Returns player who has the next turn on a board.
    """
    num_x = 0
    num_o = 0
    for row in board:
        for position in row:
            if position == X:
                num_x += 1
            elif position == O:
                num_o += 1
    if num_o < num_x:
        #print("o:s turn")
        return O
    else:
        #print("Xs turn")
        return X
    
    raise NotImplementedError

def actions(board) -> set:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for row_index, row in enumerate(board):
        for column_index, value in enumerate(row):
            if value == EMPTY:
                action_set.add((row_index, column_index))
    return action_set
    raise NotImplementedError


def result(board, action) -> list[list]:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_to_move = player(board)
    resulting_board = deepcopy(board)
    action_row_index = action[0]
    action_col_index = action[1]
    if board[action_row_index][action_col_index] is not EMPTY:
        raise Exception("invalid move")
    else:
        resulting_board[action_row_index][action_col_index] = player_to_move
        return resulting_board

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_horizontal_winner(player: str):
        for row in board:
            if all(position == player for position in row):
                return player
    
    def check_vertical_winner(player: str):
        for col_index in range(3):
            if all(board[row_index][col_index] == player for row_index in range(3)):
                return player
    
    def check_diagonal_winner(player: str):
        if all(board[i][i] == player for i in range(3)):
            return player
        if all(board[i][2 - i] == player for i in range(3)):
            return player
    
    for player in [X, O]:
        if check_horizontal_winner(player):
            return player
        if check_vertical_winner(player):
            return player
        if check_diagonal_winner(player):
            return player

    return None
    raise NotImplementedError

def board_is_full(board):
    return all(position is not EMPTY for row in board for position in row)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or board_is_full(board):
        return True
    else:
        return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    else:
        return 0
    
    raise NotImplementedError

def max_value(board):
        v = -math.inf
        if terminal(board):
            return utility(board)

        for action in actions(board):
               v = max(v, min_value(result(board, action)))
        return v
    
def min_value(board):
        v = math.inf
        if terminal(board):
            return utility(board)
        
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    best_action = None
    if player(board) == X:
        current_max_value = -math.inf
        for action in actions(board):
            min_result = min_value(result(board, action))
            if min_result > current_max_value:
                current_max_value = min_result
                best_action = action
    
    else:
        current_min_value = math.inf
        for action in actions(board):
            max_result = max_value(result(board, action))
            if max_result < current_min_value:
                current_min_value = max_result
                best_action = action
    
    return best_action


    
    raise NotImplementedError
