from AbstractWindow import AbstractWindow
from GameManager import GameManager
import sfml as sf

class AboutWindow(AbstractWindow):

	def __init__(self, window):
		super().__init__(window)

	def initialize_contents(self):
		try:
			self._text = sf.Text('Created by: Ibrahim ElSebaie')
			self._text.font = GameManager.game_font
			self._text.character_size = 30

			self._text.origin = self._text.global_bounds.width / 2, self._text.global_bounds.height / 2
			self._text.position = self._window.size.x / 2, self._window.size.y / 2

			self.set_background_file("Data/Images/plain.png")
		except IOError: exit(1)

	def handle_event(self, event):
		if type(event) is sf.KeyEvent and event.pressed is True:
			self.close()

	def draw_contents(self):
		self._window.draw(self._text)
