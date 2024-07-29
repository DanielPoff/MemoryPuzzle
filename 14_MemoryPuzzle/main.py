# Memory Puzzle
# Author: Daniel Poff
# Source: al Sweigart al@inventwithpython.com
# Date: 11/9/23 - 11/28/23 (Kinda procrastinated on bug fixes)



# __IMPORTS__ #
from assets.scripts.settings import *
from assets.scripts.classes.game import Game


def main():
	# Checks for problems with user set settings.
	SettingsError()
	# Start Game
	game = Game()
	game.gameLoop()


def SettingsError():
	# Checks if the amount of tiles is even
	if BOARDWIDTH * BOARDHEIGHT % 2 != 0:
		print(BOARDWIDTH * BOARDHEIGHT % 2)
		Game.Quit('Board needs to have an even number of boxes for pairs of matches')
	# Checks if there is enough colors and shapes to play the game with the current board size.
	assert len(COLORS) * len(SHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, 'Board is too big for the number of shapes/colors defined.'


if __name__ == "__main__":
	main()






