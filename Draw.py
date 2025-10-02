def Drawcheck(board):
    for row in board:
        for cell in row:
            if cell == None:
                return False
    return True