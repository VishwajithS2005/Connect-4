col_num=7
row_num=6
def get_valid_locations(board):
	valid_locations = []
	for col in range(col_num):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations						#Returns list of columns which are not full

def is_valid_location(board, col):				#Check if the specific column is not full
	return board[0][col] is None

def Drawcheck(board):
    if len(get_valid_locations(board)) == 0:	#Declare tie if all columns are full
        return True
    return False
