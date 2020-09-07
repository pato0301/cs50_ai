"""
Tic Tac Toe Player
"""
import itertools
import math
import copy

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    row_X = 0
    row_O = 0
    
    # Initial state of the Game
    if board == initial_state():
        return X

    for row in board:
        row_X += row.count(X)
        row_O += row.count(O)

    if row_X == row_O and not terminal(board):
        return X
    elif row_X > row_O:
        return O
    else:
        return O

    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    options = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                options.add((i,j))
    return options
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Get the row and column
    # print(action)
    row = action[0]
    column = action[1]

    # Copy the board
    board_temp = copy.deepcopy(board)

    # Check for error
    if board_temp[row][column] != EMPTY:
            raise NameError('Movement no allow') #IndexError

    # Draw new board
    player_move = player(board)
    board_temp[row][column] = player_move

    return board_temp

    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Count X and O in each row, if 3 then that player wins
    for row in board:
        row_X = row.count(X)
        row_O = row.count(O)
        if row_X == 3:
            return X
        elif row_O == 3:
            return O

    # Count X and O in each column, if 3 then that player wins
    columns = []
    for column in range(len(board)):
        each_column = []
        for row in board:
            each_column.append(row[column])
        columns.append(each_column)


    for column in columns:
        row_X = column.count(X)
        row_O = column.count(O)
        if row_X == 3:
            return X
        elif row_O == 3:
            return O

    # Checks diagonals
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X

    # No winner/tie
    return None

    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    empty_counter = 0
    for row in board:
        empty_counter += row.count(EMPTY)
    if empty_counter == 0:
        return True
    elif winner(board) is not None:
        return True
    else:
        return False

    return False
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    # raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    possible_actions = actions(board)
    alpha = -math.inf
    beta = math.inf

    if player(board) == X:
        v_prima = -math.inf
        possible_moves = set()

        for action in possible_actions:
            v = min_value(result(board,action),alpha,beta)
            if v > v_prima:
                v_prima = v
                possible_moves = action
    else:
        v_prima = math.inf
        possible_moves = set()

        for action in possible_actions:
            v = max_value(result(board,action),alpha,beta)
            if v < v_prima:
                v_prima = v
                possible_moves = action

    return possible_moves

    # raise NotImplementedError

def max_value(board,alpha,beta):

    # Calculate the maximum value
    if terminal(board):
        return utility(board)
    
    v_prima = -math.inf
    possible_actions = actions(board)

    for action in possible_actions:
        v = max(v_prima,min_value(result(board,action),alpha,beta))
        v_prima = max(v_prima,v)
        alpha = max(v_prima,alpha)
        if alpha >= beta:
            break
    
    return v

def min_value(board,alpha,beta):

    # Calculate the minimum value
    if terminal(board):
        return utility(board)
    
    v_prima = math.inf
    possible_actions = actions(board)

    for action in possible_actions:
        v = min(v_prima,max_value(result(board,action),alpha,beta))
        v_prima = min(v_prima,v)
        beta = min(v_prima,beta)
        if alpha >= beta:
            break
    return v