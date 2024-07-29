# MemoryPuzzle
Simple project made for getting the hang of Python. Template used - al Sweigart al@inventwithpython.com

Run game by runnig the "main.py" file.

# Required Dependencies

- sys
- random
- pygame

# Editing the settings
FPS changes the framerate and game speed which can effect performance
- Default: 30
  
WIDTH, and HEIGHT change the dimensions of the game canvas. EDITING THIS CAN BREAK THE GAME.
- Default : 640x480
- Changing this must be in a ratio.

BOARDWIDTH and BOARDHEIGHT change the amount of tiles on the canvas. This must be an even ratio as all tiles must have a copy.
- Default : 10x8

Adding shapes and colors can be a hassle but is relatively simple.
To add a shape, create a variable like so:

  SQUARE = 'square'
  
Then, add it to the "SHAPES" list.

For colors, they can be defined by RGB hues or the correct name. Example:

  WHITE = (255, 255, 255)
  
  Or, you can use
  
  WHITE = WHITE
