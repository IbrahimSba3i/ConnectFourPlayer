

class FeaturesConverter:

	def __init__(self):
		self._rows = 6
		self._columns = 7

	def game_board_to_features_vector(self, board):
		counters = [0 for i in range(81)]
		features_vector = []
		for n in range(4, 5):
			self._extract_ngrams_horizontal(n, board, features_vector)
			self._extract_ngrams_vertical(n, board, features_vector)
			self._extract_ngrams_main_diagonal(n, board, features_vector)
			self._extract_ngrams_other_diagonal(n, board, features_vector)
		for x in features_vector:
			counters[x] = counters[x] + 1
		return counters

	def game_board_to_list(self, board):
		board_list = []
		for col in range(0, self._columns):
			for row in range(self._rows - 1, -1, -1):
				board_list.append(board[row][col])
		return board_list

	def list_to_game_board(self, l):
		board = [[0 for i in range(self._columns)] for j in  range(self._rows)]
		k = 0
		for col in range(0, self._columns):
			for row in range(self._rows - 1, -1, -1):
				board[row][col] = l[k]
				k = k + 1
		return board

	def list_to_features_vector(self, l):
		board = self.list_to_game_board(l)
		return self.game_board_to_features_vector(board)

	def _nums_to_int(self, l):
		num = 0
		for x in l:
			num = num * 3 + x
		return num

	def _extract_ngrams_horizontal(self, n, board, features_vector):
		for i in range(len(board)):
			for j in range(self._columns - n + 1):
				val = []
				for k in range(n):
					val.append(board[i][j + k])
				features_vector.append(self._nums_to_int(val))

	def _extract_ngrams_vertical(self, n, board, features_vector):
		for i in range(len(board[0])):
			for j in range(self._rows - n + 1):
				val = []
				for k in range(n):
					val.append(board[j + k][i])
				features_vector.append(self._nums_to_int(val))

	def _extract_ngrams_main_diagonal(self, n, board, features_vector):
		for i in range(self._rows - n + 1):
			j = 0
			while i + j < self._rows - n + 1:
				val = []
				for k in range(n):
					val.append(board[i + j + k][j + k])
				features_vector.append(self._nums_to_int(val))
				j = j + 1
		for i in range(1, self._columns - n + 1):
			j = 0
			while i + j < self._columns - n + 1:
				val = []
				for k in range(n):
					val.append(board[j + k][i + j + k])
				features_vector.append(self._nums_to_int(val))
				j = j + 1

	def _extract_ngrams_other_diagonal(self, n, board, features_vector):
		for i in range(self._rows - n + 1):
			j = 0
			while i + j < self._rows - n + 1:
				val = []
				for k in range(n):
					val.append(board[i + j + k][self._rows - j - k])
				features_vector.append(self._nums_to_int(val))
				j = j + 1
		for i in range(1, self._columns - n + 1):
			j = 0
			while i + j < self._columns - n + 1:
				val = []
				for k in range(n):
					val.append(board[j + k][self._rows - i - j - k])
				features_vector.append(self._nums_to_int(val))
				j = j + 1
