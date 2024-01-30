# check for rows and columns 
def is_valid_num(row, col, number):
	for i in range(array_size):
		if array[row][i] == number or array[i][col] == number:
			return False
	return True


# recursive function with back track
def solve_rec(row = 0, col = 0):
	if  col == array_size and row == array_size - 1:
		return True
	if col == array_size:
		row += 1
		col = 0
	if array[row][col] != 0:
		return solve_rec(row, col + 1)
	for num in range(1, array_size + 1):
		if is_valid_num(row, col, num):
			array[row][col] = num
			if solve_rec(row, col + 1):
				return True
	array[row][col] = 0
	return False


# input board and return the solved board
def solver(board: list[list]) -> list[list]:
    global array
    array = board
    global array_size
    array_size = len(array)
    result = solve_rec()
    return array if result else None
