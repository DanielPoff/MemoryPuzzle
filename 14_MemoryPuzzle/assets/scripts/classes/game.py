# __GAME CLASS__ #

# __IMPORTS__ #
from assets.scripts.settings import *


class Game:
	def __init__(self):
		# Initialize pygame and build window
		pg.init()
		self.clock = pg.time.Clock()
		self.screen = pg.display.set_mode(RES)
		self.screen.fill(BGCOLOR)
		pg.display.set_caption(TITLE)

		# VARIABLES
		self.running = True  # While true the game will continue to run
		self.mousex = 0  # Mouse
		self.mousey = 0  # Mouse
		self.boxx, self.boxy = self.getBoxAtPixel(self.mousex, self.mousey)  # Get box at Mouse pos
		self.mouseClicked = False  # Mouse
		self.firstSelection = None  # First box clicked

		self.left, self.top = None, None  # Just setting these here so the ide will quit yelling at me
		# __BOARD SETUP__
		self.board = []  # Board list, contains each column in the grid
		self.icons = []  # Contains the icons available for the board
		self.numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)  # Checks how many icons are needed
		self.mainBoard = self.getRandomizedBoard()
		self.revealedBoxes = self.generateRevealedBoxesData(False)
		self.icon1shape, self.icon1color = None, None
		self.icon2shape, self.icon2color = None, None
		# __START GAME ANIMATION__ #
		self.startGameAnimation(self.mainBoard)

	def gameLoop(self):
		while self.running:  # Main game loop
			self.mouseClicked = False
			# TICK
			self.clock.tick(FPS)
			# EVENT HANDLING
			self.event_detection()
			# DRAW
			self.draw(self.mainBoard, self.revealedBoxes)
			# UPDATE
			self.update()

	def update(self):
		self.boxx, self.boxy = self.getBoxAtPixel(self.mousex, self.mousey)

	def draw(self, mainBoard, revealedBoxes):
		self.screen.fill(BGCOLOR)  # Clearing the screen to prepare it for redrawing
		self.drawBoard(mainBoard, revealedBoxes)
		# Highlight box that mouse is over.
		if self.boxx is not None and self.boxy is not None:
			# ^^ Checks if mouse is currently over a box ^^
			if not self.revealedBoxes[self.boxx][self.boxy]:
				self.drawHighlightBox(self.boxx, self.boxy)
		pg.display.update()

	def event_detection(self):
		events = pg.event.get()
		for event in events:
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				self.Quit("User quit game")
			elif event.type == MOUSEMOTION:  # MOUSE MOVEMENT
				self.mousex, self.mousey = event.pos
			elif event.type == MOUSEBUTTONUP:  # CLICK DETECTION
				self.mousex, self.mousey = event.pos
				self.mouseClicked = True

			# Don't really like how this whole section is coded might change it.
			if self.boxx is not None and self.boxy is not None:
				if not self.revealedBoxes[self.boxx][self.boxy] and self.mouseClicked:
					# Revealing the clicked box
					self.revealBoxesAnimation(self.mainBoard, [(self.boxx, self.boxy)])
					self.revealedBoxes[self.boxx][self.boxy] = True  # Sets the box as revealed

					if self.firstSelection is None:  # If the current box was the first box clicked
						self.firstSelection = (self.boxx, self.boxy)
						print(f"first selection = {self.firstSelection}")
					else:  # If the current box was the second box clicked
						self.icon1shape, self.icon1color = self.getShapeAndColor(self.mainBoard, self.firstSelection[0], self.firstSelection[1])
						self.icon2shape, self.icon2color = self.getShapeAndColor(self.mainBoard, self.boxx, self.boxy)
						# print(self.icon1shape)

						if self.icon1shape != self.icon2shape or self.icon1color != self.icon2color:
							# If icons don't match, recover the selections
							print("icons dont match")
							pg.time.wait(1000)
							self.coverBoxesAnimation(self.mainBoard, [(self.firstSelection[0], self.firstSelection[1]), (self.boxx, self.boxy)])
							self.revealedBoxes[self.firstSelection[0]][self.firstSelection[1]] = False
							self.revealedBoxes[self.boxx][self.boxy] = False
							print(self.revealedBoxes)
						else:
							print("icons match")
							if self.hasWon(self.revealedBoxes):  # check if all pairs found
								self.gameWonAnimation(self.mainBoard)
						self.firstSelection = None

	@staticmethod
	def generateRevealedBoxesData(val):
		revealedBoxes = []
		for i in range(BOARDWIDTH):
			revealedBoxes.append([val] * BOARDHEIGHT)
		print(f"REVEALED BOXES: {revealedBoxes}")
		return revealedBoxes

	def getRandomizedBoard(self):
		# Gets a list of every shape in every color
		self.icons = []
		for color in COLORS:
			for shape in SHAPES:
				self.icons.append((shape, color))

		random.shuffle(self.icons)  # Randomize the order of the icons in the list
		# dunno if this actually needs self
		self.numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)  # Decided to set this again in case we change the size at some point
		self.icons = self.icons[:self.numIconsUsed] * 2  # Make 2 of each
		random.shuffle(self.icons)  # Randomize the icons again

		# Create the board data structure
		self.board = []
		for x in range(BOARDWIDTH):
			column = []
			for y in range(BOARDHEIGHT):
				if self.icons:
					print(self.icons[0])
					column.append(self.icons.pop(0))  # Removes icons from the list as we assign them
				else:
					print("All icons drawn")
			self.board.append(column)
		return self.board

	@staticmethod
	def splitIntoGroupsOf(groupSize, ListVar):
		# Splits a list into a list of lists, where the inner lists have at most groupSize number of items
		result = []
		for i in range(0, len(ListVar), groupSize):
			result.append(ListVar[i:i + groupSize])
		return result

	def leftTopCoordsOfBox(self, boxx, boxy):
		self.left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
		self.top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
		return self.left, self.top

	# Get the box where the mouse is.
	def getBoxAtPixel(self, x, y):
		for boxx in range(BOARDWIDTH):
			for boxy in range(BOARDHEIGHT):
				self.left, self.top = self.leftTopCoordsOfBox(boxx, boxy)
				boxRect = pg.Rect(self.left, self.top, BOXSIZE, BOXSIZE)
				if boxRect.collidepoint(x, y):
					return boxx, boxy  # If found return box x and box y
		return None, None  # If it can't find the box, return none.

	def drawIcon(self, shape, color, boxx, boxy):
		quarter = int(BOXSIZE * 0.25)  # syntactic sugar
		half = int(BOXSIZE * 0.5)		# syntactic sugar

		# did this without self originally and should work without it so why fix what's not broken
		left, top = self.leftTopCoordsOfBox(boxx, boxy)  # Get pixel coords from board coords
		# Draw the shapes. I hate how this is coded I want to redo it.
		if shape == DONUT:
			pg.draw.circle(self.screen, color, (left + half, top + half), half - 5)
			pg.draw.circle(self.screen, BGCOLOR, (left + half, top + half), quarter - 5)  # draws the hole in the donut
		elif shape == SQUARE:
			pg.draw.rect(self.screen, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
		elif shape == DIAMOND:
			pg.draw.polygon(self.screen, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
		elif shape == LINES:
			for i in range(0, BOXSIZE, 4):
				pg.draw.line(self.screen, color, (left, top + i), (left + i, top))
				pg.draw.line(self.screen, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
		elif shape == OVAL:
			pg.draw.ellipse(self.screen, color, (left, top + quarter, BOXSIZE, half))

	@staticmethod
	def getShapeAndColor(board, boxx, boxy):
		# shape value for x, y spot is stored in board [x] [y] [0]
		# color value for x, y spot is stored in board [x] [y] [1]
		try:
			return board[boxx][boxy][0], board[boxx][boxy][1]
		except IndexError:
			print("Index out of range.")
			print(f"Board: {board}\n Boxx: {boxx}, Boxy: {boxy}")
			pg.time.wait(200)
			return LINES, DARKRED

	# I really feel like I should make another class for all of these, but I don't want to

	def drawBoxCovers(self, board, boxes, coverage):
		# Draws boxes being covered/revealed. "boxes" is a list of two-item lists,
		# which have the x & y spot of the box
		for box in boxes:
			self.left, self.top = self.leftTopCoordsOfBox(box[0], box[1])
			pg.draw.rect(self.screen, BGCOLOR, (self.left, self.top, BOXSIZE, BOXSIZE))

			# Get the shape and color of the box
			shape, color = self.getShapeAndColor(board, box[0], box[1])
			pg.time.wait(10)
			self.drawIcon(shape, color, box[0], box[1])

			if coverage > 0:  # Only draw the cover if it's covered?
				pg.draw.rect(self.screen, BOXCOLOR, (self.left, self.top, coverage, BOXSIZE))
			pg.display.update()

	def revealBoxesAnimation(self, board, boxesToReveal):
		# Do the "box reveal" animation
		for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):
			self.drawBoxCovers(board, boxesToReveal, coverage)

	def coverBoxesAnimation(self, board, boxesToCover):
		# Do the "box cover" animation
		for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
			self.drawBoxCovers(board, boxesToCover, coverage)

	def drawBoard(self, board, revealed):
		# Draws all the boxes in their covered or revealed state.
		for boxx in range(BOARDWIDTH):
			for boxy in range(BOARDHEIGHT):
				self.left, self.top = self.leftTopCoordsOfBox(boxx, boxy)
				if not revealed[boxx][boxy]:
					# Draw a covered box.
					pg.draw.rect(self.screen, BOXCOLOR, (self.left, self.top, BOXSIZE, BOXSIZE))
				else:
					# Draw the revealed icon
					shape, color = self.getShapeAndColor(board, boxx, boxy)
					self.drawIcon(shape, color, boxx, boxy)

	# Yay, more functions
	def drawHighlightBox(self, boxx, boxy):
		self.left, self.top = self.leftTopCoordsOfBox(boxx, boxy)
		pg.draw.rect(self.screen, HIGHLIGHTCOLOR, (self.left - 5, self.top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

	def startGameAnimation(self, board):
		# Randomly reveal the boxes 8 at a time.
		# I don't know if these need a self declaration yet
		coveredBoxes = self.generateRevealedBoxesData(False)
		boxes = []

		for x in range(BOARDWIDTH):
			for y in range(BOARDHEIGHT):
				boxes.append((x, y))
		random.shuffle(boxes)
		boxGroups = self.splitIntoGroupsOf(8, boxes)

		self.drawBoard(board, coveredBoxes)
		for boxGroup in boxGroups:
			print(boxGroup)
			self.revealBoxesAnimation(board, boxGroup)
			self.coverBoxesAnimation(board, boxGroup)

	def Reset(self):
		# Reset the board
		self.mainBoard = self.getRandomizedBoard()
		self.revealedBoxes = self.generateRevealedBoxesData(False)

		# Replay start game animation
		print("replaying start animation")
		self.startGameAnimation(self.mainBoard)

	def gameWonAnimation(self, board):
		# Flash the background color when the player has won the game
		coveredBoxes = self.generateRevealedBoxesData(True)
		color1 = LIGHTBGCOLOR
		color2 = BGCOLOR

		for i in range(13):
			color1, color2 = color2, color1  # Swap colors
			self.screen.fill(color1)
			self.drawBoard(board, coveredBoxes)
			pg.display.update()
			pg.time.wait(300)

		self.Reset()

	@staticmethod
	def hasWon(revealedBoxes):
		# Returns True if all the boxes have been revealed, otherwise False
		for i in revealedBoxes:
			if False not in i:
				return True

			else:
				return False

	# Finally
	@staticmethod
	def Quit(message):
		print(message)
		pg.quit()
		exit()





