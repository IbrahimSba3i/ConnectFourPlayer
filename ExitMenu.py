from AbstractWindow import AbstractWindow
from GameManager import GameManager
import sfml as sf

class ExitMenu(AbstractWindow):

	def __init__(self, window):
		super().__init__(window)

	def initialize_contents(self):
		try:
			self._exit_text = sf.Text('Are you sure you want to exit?')
			self._exit_text.font = GameManager.game_font
			self._exit_text.character_size = 25

			x_offset = (self._window.size.x - self._exit_text.global_bounds.width) / 2
			y_offset = 160
			self._exit_text.position = x_offset, y_offset

			y_offset = y_offset + self._exit_text.global_bounds.height + 120

			self._menu_items = [sf.Text(x) for x in ['Yes', 'No']]
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
				if self._selection_cursor is 0: # Yes
					self._window.close()
				elif self._selection_cursor is 1: # No
					self.close()
				else: print('Unknown command: ' + str(self._selection_cursor))

	def draw_contents(self):
		self._window.draw(self._exit_text)
		for item in self._menu_items:
			self._window.draw(item)
