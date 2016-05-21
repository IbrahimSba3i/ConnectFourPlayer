import sfml as sf
from AbstractWindow import AbstractWindow
from GameManager import GameManager
from AIController import AIController

class MainGameWindow(AbstractWindow):

	def __init__(self, window):
		super().__init__(window)

	def get_coordinates(self, i, j):
		return (self._x_offset + j * (self._radius * 2 + self._x_shift), self._y_offset + i * (self._radius * 2 + self._y_shift))

	def add_chip(self, player, i, j):
		if i < 0 or i >= self._board_rows_count or j < 0 or j >= self._board_columns_count:
			return False

		self._board_map[i][j] = player

		chip = sf.Sprite(self._chips_texture)
		chip.texture_rectangle = (0, 0, 150, 150) if player is 1 else (0, 150, 150, 150)

		source_width = chip.global_bounds.width
		source_height = chip.global_bounds.height

		target_width = (self._radius - 3) * 2
		target_height = (self._radius - 3) * 2

		chip.origin = source_width / 2, source_height / 2
		chip.ratio = target_width / source_width, target_height / source_height
		chip.position = self.get_coordinates(i, j)

		self._chips_sprites.append(chip)
		return True

	def start_moving(self, i, j):
		animation_target_x, self._animation_chip_target_y = self.get_coordinates(i, j)
		self._is_chip_animating = True

	def end_game(self, msg):
		self._is_game_finished = True
		self._game_finished_text.string = msg
		self._game_finished_text.origin = self._game_finished_text.global_bounds.width / 2, self._game_finished_text.global_bounds.height / 2
		self._game_finished_text.position = self._window.size.x / 2, self._window.size.y / 2

	def update_contents(self):
		if self._is_chip_animating:
			if self._pending_chip.position.y >= self._animation_chip_target_y:
				self.add_chip(self._turn, self._animation_target_row, self.__animation_target_column)

				game_state = self._ai_controller.evaluate_game_state()
				if game_state is 1:
					self.end_game('You Win!')
				elif game_state is 2:
					self.end_game('You Lose!')
				elif game_state is 3:
					self.end_game('Draw!')

				self._is_chip_animating = False
				if self._turn is 1:
					self._turn = 2
					self._pending_chip.texture_rectangle = (0, 150, 150, 150)
				else:
					self._turn = 1
					self._pending_chip.texture_rectangle = (0, 0, 150, 150)
					self._player_selection_column = 3
					self._pending_chip.position = self.get_coordinates(-1, self._player_selection_column)
			else:
				self._pending_chip.position = self._pending_chip.position.x, self._pending_chip.position.y + 15

		elif self._turn is 2:
			if not self._is_game_finished:
				self._player_selection_column = self._ai_controller.get_decision()
				self._pending_chip.position = self.get_coordinates(-1, self._player_selection_column)
				self._animation_target_row, self.__animation_target_column = self._ai_controller.get_chip_insert_position(self._player_selection_column)
				self.start_moving(self._animation_target_row, self.__animation_target_column)

	def initialize_contents(self):

		self._board_sprite_texture = sf.Texture.from_file("Data/Images/board.png")
		self._board_sprite = sf.Sprite(self._board_sprite_texture)
		self._board_sprite.origin = self._board_sprite.global_bounds.width / 2, self._board_sprite.global_bounds.height / 2
		self._board_sprite.position = self._window.size.x / 2, self._window.size.y / 2

		self._board_rows_count = 6
		self._board_columns_count = 7

		self._chips_texture = sf.Texture.from_file('Data/Images/chips.png')

		self._radius = 35
		self._x_shift = 20
		self._y_shift = 10
		self._x_offset = self._board_sprite.global_bounds.left + self._radius + 15
		self._y_offset = self._board_sprite.global_bounds.top + self._radius + 6.5

		self._circle_holes = [[sf.CircleShape() for x in range(self._board_columns_count)] for y in range(self._board_rows_count)]
		for i in range(len(self._circle_holes)):
			for j in range(len(self._circle_holes[i])):
				self._circle_holes[i][j].radius = self._radius - 3
				self._circle_holes[i][j].origin = self._circle_holes[i][j].radius, self._circle_holes[i][j].radius
				self._circle_holes[i][j].point_count = 100
				self._circle_holes[i][j].outline_color = GameManager.blue_color
				self._circle_holes[i][j].outline_thickness = 4
				self._circle_holes[i][j].fill_color = sf.Color.TRANSPARENT
				self._circle_holes[i][j].position = self.get_coordinates(i, j)


		self._board_map = [[0 for x in range(self._board_columns_count)] for y in range(self._board_rows_count)]
		self._chips_sprites = []

		self._ai_controller = AIController(self._board_map)

		self._turn = 1
		self._player_selection_column = 3

		self._is_chip_animating = False

		self._pending_chip = sf.Sprite(self._chips_texture)
		self._pending_chip.texture_rectangle = (0, 0, 150, 150)
		source_width = self._pending_chip.global_bounds.width
		source_height = self._pending_chip.global_bounds.height

		target_width = (self._radius - 3) * 2
		target_height = (self._radius - 3) * 2

		self._pending_chip.origin = source_width / 2, source_height / 2
		self._pending_chip.ratio = target_width / source_width, target_height / source_height
		self._pending_chip.position = self.get_coordinates(-1, self._player_selection_column)

		self._is_game_finished = False

		self._game_finished_text = sf.Text()
		self._game_finished_text.font = GameManager.game_font
		self._game_finished_text.character_size = 50
		self._game_finished_text.origin = self._game_finished_text.global_bounds.width / 2, self._game_finished_text.global_bounds.height / 2
		self._game_finished_text.position = self._window.size.x / 2, self._window.size.y / 2
		self._game_finished_text.color = sf.Color.WHITE

		self._game_finished_background = sf.RectangleShape()
		self._game_finished_background.fill_color = sf.Color(0, 0, 0, 200)
		self._game_finished_background.size = self._window.size

		#self.set_background_file("Data/Images/plain.png")

	def move_selection_left(self):
		self._player_selection_column = (self._player_selection_column - 1 + self._board_columns_count) % self._board_columns_count
		self._pending_chip.position = self.get_coordinates(-1, self._player_selection_column)

	def move_selection_right(self):
		self._player_selection_column = (self._player_selection_column + 1) % self._board_columns_count
		self._pending_chip.position = self.get_coordinates(-1, self._player_selection_column)

	def handle_event(self, event):
		if type(event) is sf.KeyEvent and event.pressed is True:
			if not self._is_game_finished:
				if event.code is sf.Keyboard.LEFT:
					if self._turn is 1 and not self._is_chip_animating:
						self.move_selection_left()
				elif event.code is sf.Keyboard.RIGHT:
					if self._turn is 1 and not self._is_chip_animating:
						self.move_selection_right()
				elif event.code is sf.Keyboard.RETURN:
					if self._turn is 1 and not self._is_chip_animating:
						self._animation_target_row, self.__animation_target_column = self._ai_controller.get_chip_insert_position(self._player_selection_column)
						self.start_moving(self._animation_target_row, self.__animation_target_column)
				elif event.code is sf.Keyboard.ESCAPE:
					self.close()
			else:
				self.close()

	def draw_contents(self):
		self._window.draw(self._pending_chip)
		for chip in self._chips_sprites:
			self._window.draw(chip)
		self._window.draw(self._board_sprite)
		for i in range(len(self._circle_holes)):
			for j in range(len(self._circle_holes[i])):
				self._window.draw(self._circle_holes[i][j])
		if self._is_game_finished:
			self._window.draw(self._game_finished_background)
			self._window.draw(self._game_finished_text)
