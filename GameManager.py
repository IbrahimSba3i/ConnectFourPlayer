import sfml as sf

class GameManager:
	logo_font = sf.Font.from_file("Data/Fonts/astron boy wonder.ttf")
	game_font = sf.Font.from_file("Data/Fonts/moonhouse.ttf")
	blue_color = sf.Color(60, 221, 255)
	grey_color = sf.Color(56, 56, 56)
	window_height = 640
	window_width = 800
	scale_factor = 1.2

	class_1 = 1
	class_2 = 2
	class_3 = 0
