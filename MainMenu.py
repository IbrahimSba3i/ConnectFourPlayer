from AbstractWindow import AbstractWindow
from GameManager import GameManager
from ExitMenu import ExitMenu
from AboutWindow import AboutWindow
from TwoPlayersWindow import TwoPlayersWindow
from MainGameWindow import MainGameWindow
import sfml as sf

class MainMenu(AbstractWindow):

	def __init__(self, window):
		super().__init__(window)

	def initialize_contents(self):
		try:
			self._game_logo = sf.Text('Connect 4')
			self._game_logo.font = GameManager.logo_font
			self._game_logo.character_size = 75

			x_offset = (self._window.size.x - self._game_logo.global_bounds.width) / 2
			y_offset = 60
			self._game_logo.position = x_offset, y_offset

			y_offset = y_offset + self._game_logo.global_bounds.height + 120

			self._menu_items = [sf.Text(x) for x in ['Single Player', 'Two Players', 'About', 'Exit Game']]
			for i, item in enumerate(self._menu_items):
				item.font = GameManager.game_font
				item.character_size = 20
				item.origin = item.global_bounds.width / 2, item.global_bounds.height / 2
				item.position = self._window.size.x / 2, y_offset + i * 85
				item.color = GameManager.blue_color

			self._selection_cursor = 0
			self.set_selected(self._selection_cursor)

			self.set_background_file("Data/Images/plain.png")
		except IOError: exit(1)

	def move_cursor_up(self):
		self.set_unselected(self._selection_cursor)
		self._selection_cursor = (self._selection_cursor - 1 + len(self._menu_items)) % len(self._menu_items)
		self.set_selected(self._selection_cursor)

	def move_cursor_down(self):
		self.set_unselected(self._selection_cursor)
		self._selection_cursor = (self._selection_cursor + 1) % len(self._menu_items)
		self.set_selected(self._selection_cursor)

	def set_selected(self, index):
		self._menu_items[index].ratio = GameManager.scale_factor, GameManager.scale_factor

	def set_unselected(self, index):
		self._menu_items[index].ratio = 1.0, 1.0

	def handle_event(self, event):
		if type(event) is sf.KeyEvent and event.pressed is True:
			if event.code is sf.Keyboard.UP:
				self.move_cursor_up()
			elif event.code is sf.Keyboard.DOWN:
				self.move_cursor_down()
			elif event.code is sf.Keyboard.RETURN:
				if self._selection_cursor is 0:
					main_game_window = MainGameWindow(self._window)
					main_game_window.open()
				elif self._selection_cursor is 1: # Two Players
					two_players_window = TwoPlayersWindow(self._window)
					two_players_window.open()
				elif self._selection_cursor is 2: # About
					about_window = AboutWindow(self._window)
					about_window.open()
				elif self._selection_cursor is 3: # Exit
					exit_window = ExitMenu(self._window)
					exit_window.open()
				else: print('Unknown command: ' + str(self._selection_cursor))

	def draw_contents(self):
		self._window.draw(self._game_logo)
		for item in self._menu_items:
			self._window.draw(item)
