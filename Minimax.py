import math
import random
import copy
from Winning_Move import winning_move
from Draw import get_valid_locations, is_valid_location, Drawcheck

col_num = 7   #Number of Columns
row_num = 6   #Number of Rows

def minimax(board, depth, alpha, beta, maximizingPlayer):     #Minimax Algorithm with Alpha-Beta Pruning
    valid_locations = get_valid_locations(board)              #Get possible positions to place the coin
    is_terminal = is_terminal_node(board)                     #Check if the game has ended
    if depth == 0 or is_terminal:
        if is_terminal:                                       #If the move ends the game, give the max or min score
            if winning_move(board, 1):
                return (None, 1_000_000_000_000_000)
            elif winning_move(board, 0):
                return (None, -1_000_000_000_000_000)
            else:                                             #Depth = 0 
                return (None, 0)
        else:
            return (None, score_position(board, 1))           #Evaluate the board position and return score   

    if not valid_locations:                                   #No possible moves, return None
        return (None, 0)

    if maximizingPlayer:                        #Maximizing player (AI)
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)         #Get top most row in the column
            if row is None:
                continue
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, row, col, 1)         #Simulate the move and get the new board
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]       #Recursively call minimax for the new board
            if new_score > value:                   
                value = new_score
                column = col
            alpha = max(alpha, value)               #Update alpha to the best score(maximum) found so far
            if alpha >= beta:                       #Prune the remaining branches
                break
        return column, value
    else:                               #Minimizing player (Player)
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, row, col, 0)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)             #Update beta to the best score(minimum) found so far
            if alpha >= beta:                   #Prune the remaining branches
                break
        return column, value


def is_terminal_node(board):
    return winning_move(board, 0) or winning_move(board, 1) or len(get_valid_locations(board)) == 0


def get_next_open_row(board, col):
    for r in range(row_num - 1, -1, -1):
        if board[r][col] is None:
            return r
    return None


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def score_position(board, piece):
    score = 0
    center_array = [row[col_num // 2] for row in board if row[col_num // 2] is not None]     # Center column
    score += center_array.count(piece) * 3

    # Horizontal Window
    for r in range(row_num):
        row_array = board[r][:]
        for c in range(col_num - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # Vertical Window
    for c in range(col_num):
        col_array = [row[c] for row in board]
        for r in range(row_num - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # Diagonal 1 Window
    for r in range(row_num - 3):
        for c in range(col_num - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Diagonal 2 Window
    for r in range(row_num - 3):
        for c in range(col_num - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def evaluate_window(window, piece):
    score = 0
    opp_piece = 1 if piece == 0 else 0

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(None) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(None) == 2:
        score += 2

    if window.count(opp_piece) == 4:
        score -= 200
    if window.count(opp_piece) == 3 and window.count(None) == 1:
        score -= 8

    return score
