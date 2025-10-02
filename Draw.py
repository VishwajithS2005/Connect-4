col_num=7
row_num=6
def get_valid_locations(board):
	valid_locations = []
	for col in range(col_num):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def is_valid_location(board, col):
	return board[0][col] is None

def Drawcheck(board):
    if len(get_valid_locations(board)) == 0:
        return True
    return False
