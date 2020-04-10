from copy import deepcopy
import time

X = "X"
O = "O"
EMPTY = E = None


def initial_state():
			return [[E, E, E],
					[E, E, E],
					[E, E, E]]

def initial_state_paper():
			return [[E, X, O],
					[X, X, E],
					[E, O, E]]

def max_value_classic(board):
	print('Checking MAX move... ', board)
	if terminal(board):
		print('MAX FOUND: ', utility(board))
		return utility(board)
	else:
		v = 2
		for action in actions(board):
			v = min(v, min_value_classic(result(board, action)))
	return v

def min_value_classic(board):
	print('Checking MIN move... ', board)
	if terminal(board):
		print('MIN FOUND: ', utility(board))
		return utility(board)
	else:
		v = -2
		for action in actions(board):
			v = max(v, max_value_classic(result(board, action)))
	return v

def minimax_classic(board):
	#if board == initial_state():
	#	return (1,1)
	if terminal(board):
		return None
	array = dict()
	for action in actions(board):
		print(action)
		if player(board) == X:
			value = max_value_classic(result(board, action))
			array[action] = value
		else:
			value = min_value_classic(result(board, action))
			array[action] = value
		print('RESULTS: ', array)
	if player(board) == X:
		return max(array, key=lambda unit: array[unit])
	else:
		return min(array, key=lambda unit: array[unit])


def player(board):
	d = {'X': 0, 'O': 0, None: 0}
	for i in board:
		for j in i:
			d[j] = d[j] + 1
	if d[X] == d[O]:
		return X
	else:
		return O


def actions(board):
	result = set()
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == EMPTY:
				result.add(tuple([i,j]))
	return result


def result(board, action):
	result = deepcopy(board)
	if board[action[0]][action[1]] is not None:
		raise NameError('NotValidAction')
	else:
		result[action[0]][action[1]] = player(board)
	return result


def winner(board):
	for i in board:
		if i[0] == i[1] == i[2] and i[0] != EMPTY:
			return i[0]
	for i in range(len(board)):
		if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
			return board[0][i]
	if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
		return board[0][0]
	elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
		return board[0][2]
	else:
		return None

def terminal(board):
	if winner(board) is not None:
		return True
	d = {'X': 0, 'O': 0, None: 0}
	for i in board:
		for j in i:
			d[j] = d[j] + 1
	if d[EMPTY] == 0:
		return True
	return False


def utility(board):
	win = winner(board)
	if win == X:
		return 1
	elif win == O:
		return -1
	else:
		return 0


def max_value(board, alpha, beta):
	minv = 2
	print('Checking MAX move... ', board, alpha, beta)
	if terminal(board):
		print('MAX FOUND: ', utility(board))
		return utility(board)
	else:
		v = 2
		for action in actions(board):
			v = min(v, min_value(result(board, action), alpha, beta))
			if v < minv:
				print('v less than minv, so minv = v: ', minv, v)
				minv = v
			if minv <= alpha:
				print('alpha', alpha, beta, minv)
				return minv
			if minv < beta:
				print('minv less than beta, so beta = minv: ', beta, minv)
				beta = minv
		return v


def min_value(board, alpha, beta):
	maxv = -2
	print('Checking MIN move... ', board, alpha, beta)
	if terminal(board):
		print('MIN FOUND: ', utility(board))
		return utility(board)
	else:
		v = -2
		for action in actions(board):
			v = max(v, max_value(result(board, action), alpha, beta))
			if v > maxv:
				print('v more than maxv, so maxv = v: ', maxv, v)
				maxv = v
			if maxv >= beta:
				print('beta', alpha, beta, v)
				return maxv
			if maxv > alpha:
				print('maxv more than alpha, so alpha = maxv: ', alpha, maxv)
				alpha = maxv
		return v


def minimax(board):
	if terminal(board):
		return None
	array = dict()
	for action in actions(board):
		print()
		print(action)
		if player(board) == X:
			value = max_value(result(board, action), -2, 2)
			array[action] = value
		else:
			value = min_value(result(board, action), -2, 2)
			array[action] = value
		print('RESULTS: ', array)
	if player(board) == X:
		return max(array, key=lambda unit: array[unit])
	else:
		return min(array, key=lambda unit: array[unit])


board = initial_state_paper()
print(player(board))
#print(actions(board))
#print(result(board, actions(board).pop()))
#s = actions(board)

#print(winner(board))
#print(terminal(board))
#print(utility(board))
start = time.time()
classic_result = minimax_classic(board)
print(classic_result)
end = time.time()
print('CLASSIC Evaluation time: {}s'.format(round(end - start, 7)))


start = time.time()
pruning_result = minimax(board)
print(pruning_result)
end = time.time()
print('PRUNING Evaluation time: {}s'.format(round(end - start, 7)))

print(classic_result)
print(pruning_result)
if classic_result == pruning_result:
	print("YES!")
else:
	print("NO")
