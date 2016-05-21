from MainMenu import MainMenu
from GameManager import GameManager
import sfml as sf

def main():
	window = sf.RenderWindow(sf.VideoMode(GameManager.window_width, GameManager.window_height), "Connect 4")
	menu = MainMenu(window)
	menu.open()

if __name__ == '__main__':
	main()
