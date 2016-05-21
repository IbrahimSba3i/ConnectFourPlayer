from random import randint
from WinLoseClassifier import WinLoseClassifier
from GameManager import GameManager
from FeaturesConverter import FeaturesConverter

class AIController:

	def __init__(self, board):
		self._conv = FeaturesConverter()

		self._clf = WinLoseClassifier(testing_mode = False)
		self._clf.train()
		print (self._clf.test())

		self._board = board

	def player_wins_horizontal(self, player):
		for i in range(len(self._board)):
			for j in range(4):
				identical = True
				for k in range(4):
					if self._board[i][j + k] is not player:
						identical = False
				if identical:
					return True
		return False

	def player_wins_vertical(self, player):
		for i in range(len(self._board[0])):
			for j in range(3):
				identical = True
				for k in range(4):
					if self._board[j + k][i] is not player:
						identical = False
				if identical:
					return True
		return False

	def player_wins_main_diagonal(self, player):
		for i in range(3):
			j = 0
			while i + j < 3:
				identical = True
				for k in range(4):
					if self._board[i + j + k][j + k] is not player:
						identical = False
				if identical:
					return True
				j = j + 1
		for i in range(1, 4):
			j = 0
			while i + j < 4:
				identical = True
				for k in range(4):
					if self._board[j + k][i + j + k] is not player:
						identical = False
				if identical:
					return True
				j = j + 1
		return False

	def player_wins_other_diagonal(self, player):
		for i in range(3):
			j = 0
			while i + j < 3:
				identical = True
				for k in range(4):
					if self._board[i + j + k][6 - j - k] is not player:
						identical = False
				if identical:
					return True
				j = j + 1
		for i in range(1, 4):
			j = 0
			while i + j < 4:
				identical = True
				for k in range(4):
					if self._board[j + k][6 - i - j - k] is not player:
						identical = False
				if identical:
					return True
				j = j + 1
		return False

	def can_win_horizontal(self, player):
		for i in range(len(self._board)):
			for j in range(4):
				count = 0
				for k in range(4):
					if self._board[i][j + k] is player:
						count = count + 1
					else:
						r, c = i, j + k
				if count is 3:
					gr, gc = self.get_chip_insert_position(c)
					if gr is r:
						return True, gc
		return False, -1

	def can_win_vertical(self, player):
		for i in range(len(self._board[0])):
			for j in range(3):
				count = 0
				for k in range(4):
					if self._board[j + k][i] is player:
						count = count + 1
					else:
						r, c = j + k, i
				if count is 3:
					gr, gc = self.get_chip_insert_position(c)
					if gr is r:
						return True, gc
		return False, -1

	def can_win_main_diagonal(self, player):
		for i in range(3):
			j = 0
			while i + j < 3:
				count = 0
				for k in range(4):
					if self._board[i + j + k][j + k] is player:
						count = count + 1
					else:
						r, c = i + j + k, j + k
				if count is 3:
					gr, gc = self.get_chip_insert_position(c)
					if gr is r:
						return True, gc
				j = j + 1
		for i in range(1, 4):
			j = 0
			while i + j < 4:
				count = 0
				for k in range(4):
					if self._board[j + k][i + j + k] is player:
						count = count + 1
					else:
						r, c = j + k, i + j + k
				if count is 3:
					gr, gc = self.get_chip_insert_position(c)
					if gr is r:
						return True, gc
				j = j + 1
		return False, -1

	def can_win_other_diagonal(self, player):
		for i in range(3):
			j = 0
			while i + j < 3:
				count = 0
				for k in range(4):
					if self._board[i + j + k][6 - j - k] is player:
						count = count + 1
					else:
						r, c = i + j + k, 6 - j - k
				if count is 3:
					gr, gc = self.get_chip_insert_position(c)
					if gr is r:
						return True, gc
				j = j + 1
		for i in range(1, 4):
			j = 0
			while i + j < 4:
				count = 0
				for k in range(4):
					if self._board[j + k][6 - i - j - k] is player:
						count = count + 1
					else:
						r, c = j + k, 6 - i - j - k
				if count is 3:
					gr, gc = self.get_chip_insert_position(c)
					if gr is r:
						return True, gc
				j = j + 1
		return False, -1

	def evaluate_game_state(self):
		winning = [False, False]
		for player in [1, 2]:
			if self.player_wins_horizontal(player) or self.player_wins_vertical(player) or self.player_wins_main_diagonal(player) or self.player_wins_other_diagonal(player):
				winning[player - 1] = True

		if winning[0] and winning[1]:
			return 3
		elif winning[0]:
			return 1
		elif winning[1]:
			return 2
		else:
			return 0

	def get_chip_insert_position(self, column):
		j = column
		i = 0
		while i < len(self._board) and self._board[i][j] is 0:
			i = i + 1
		i = i - 1
		return i, j

	def calculate_winning_probability_index_bt(self, player = 2, depth = 1, max_depth = 4):
		game_state = self.evaluate_game_state()
		if game_state is 1:
			return (1.0, -1) if player is 1 else (0.0, -1)
		elif game_state is 2:
			return (1.0, -1) if player is 2 else (0,0, -1)
		elif game_state is 3:
			return 0.5, -1
		else:
			if depth is max_depth:
				winning_columns = []
				draw_columns = []
				lose_columns = []
				sum_val = 0.0
				count = 0
				for column in range(7):
					i, j = self.get_chip_insert_position(column)
					if i >= 0:
						self._board[i][j] = player
						decisison = self.whos_winning()
						self._board[i][j] = 0

						if decisison is player:
							probability = 1.0
						elif decisison is 3:
							probability = 0.5
						else:
							probability = 0

						sum_val = sum_val + probability

						if probability is 1.0:
							winning_columns.append(column)
						elif probability is 0.5:
							draw_columns.append(column)

						count = count + 1

				if player is 1:
					return sum_val / count, -1
				else:
					if len(winning_columns) is not 0:
						return 1.0, winning_columns[randint(0, len(winning_columns) - 1)]
					elif len(draw_columns) is not 0:
						return 0.5, draw_columns[randint(0, len(draw_columns) - 1)]
					else:
						return 0.0, lose_columns[randint(0, len(lose_columns) - 1)]

			else:
				sum_val = 0.0
				min_val = 0.0
				min_index = 0
				count = 0
				for column in range(7):
					i, j = self.get_chip_insert_position(column)
					if i >= 0:
						self._board[i][j] = player
						win, index = self.calculate_winning_probability_index_bt(3 - player, depth + 1, max_depth)

						sum_val = sum_val + win
						if win < min_val:
							min_index = index
							min_val = win
						self._board[i][j] = 0
						count = count + 1
				if player is 2:
					return 1.0 - min_val, min_index
				else:
					return 1.0 - (sum_val / count), -1

	def calculate_winning_probability_index(self):
		max_index = 0
		max_val = 0.0
		for column in range(7):
			i, j = self.get_chip_insert_position(column)
			if i >= 0:
				self._board[i][j] = 2
				decisison = self.get_class_two_probability()
				self._board[i][j] = 0
				if decisison > max_val:
					max_val = decisison
					max_index = column
		return max_val, max_index

	def can_win(self, player):
		f, c = self.can_win_horizontal(player)
		if f: return True, c
		f, c = self.can_win_vertical(player)
		if f: return True, c
		f, c = self.can_win_main_diagonal(player)
		if f: return True, c
		f, c = self.can_win_other_diagonal(player)
		if f: return True, c
		else: return False, -1

	def get_decision(self):
		can, index = self.can_win(2)
		if can: return index
		can, index = self.can_win(1)
		if can: return index
		prob, index = self.calculate_winning_probability_index()
		return index

	def get_class_two_probability(self):
		f = self._conv.game_board_to_features_vector(self._board)
		return self._clf.get_class_probability(f, 2)

	def whos_winning(self):
		f = self._conv.game_board_to_features_vector(self._board)
		return self._clf.get_decision(f)
