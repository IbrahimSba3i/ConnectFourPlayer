import sfml as sf

class AbstractWindow:
	def __init__(self, window):
		self._window = window
		self._clear_color = sf.Color(255, 255, 255)
		self._background_sprite = None
		self._background_texture = None
		self._window_opened = True
		self._clock = sf.Clock()
		self._fps = 30
		self._frame_time = sf.milliseconds(1000 / self._fps)

	def set_fps(self, fps):
		self._fps = fps
		self._frame_time = sf.milliseconds(1000 / self._fps)

	def set_background_file(self, file_name):
		self._background_texture = sf.Texture.from_file(file_name)
		self._background_sprite = sf.Sprite(self._background_texture)

	def initialize_contents(self):
		raise NotImplementedError

	def handle_event(self, event):
		raise NotImplementedError

	def draw_contents(self):
		raise NotImplementedError

	def update_contents(self):
		pass

	def set_clear_color(self, color):
		self._clear_color = color

	def close(self):
		self._window_opened = False

	def open(self):
		self.initialize_contents()
		while self._window.is_open and self._window_opened:
			if self._clock.elapsed_time >= self._frame_time:
				self._clock.restart()
				for event in self._window.events:
					if type(event) is sf.CloseEvent:
						self._window.close()
					else:
						self.handle_event(event)

				self.update_contents()

				self._window.clear(self._clear_color)
				if self._background_sprite is not None:
					self._window.draw(self._background_sprite)
				self.draw_contents()
				self._window.display()
