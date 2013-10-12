import random

def swapIdx(state,idx1,idx2):
	for i in range(0,len(state)):
		for j in range(0,len(state[i])):
			if state[i][j] == idx1:
				state[i][j] = idx2
			elif state[i][j] == idx2:
				state[i][j] = idx2

def getBlockSide(state,piece):
	pos = []
	for i in range(0,len(state)):
		for j in range(0,len(state[i])):
			if int(state[i][j]) == int(piece):
				pos.append([i,j])

	# If the piece is not present, return empty list
	if len(pos) == 0:
		return []

	# Check the side of the piece
	vertical = []
	horizontal = []
	for item in pos:
		if item[0] not in horizontal: horizontal.append(item[0])
		if item[1] not in vertical: vertical.append(item[1])
	vertical.sort()
	horizontal.sort()

	return [vertical,horizontal]

class SlidingBrickPuzzle(object):
	def __init__(self):
		self.filename = None
		self.current_state = []
		self.original_state = []
		self.height = 0
		self.width = 0

	def loadGameStateFromDisk(self,filename):
		state = []
		try:
			f = open(filename,"r")
			first_line = f.readline().split(",")
			self.width = first_line[0]
			self.height = first_line[1]	
			for line in f:
				item = line.split(",")
				item = [x for x in item if x != "\n" and x != ""]
				state.append(item)
			self.filename = filename
			self.original_state = state 
			self.current_state = state
		except Exception as exception:
			print "Load game state from disk exception" + exception

	def displayGameState(self,state=None):
		if state == None:
			state = self.current_state
		try :
			print self.width + "," + self.height + ","
			for row in state:
				s = ""
				for item in row:
					s += str(item) + ","
				print s
		except Exception as exception:
			print "Display game state exception" + exception

	def cloneState(self,state=None):
		if state == None:
			state = self.current_state
		output = []
		for row in state:
			l = []
			for item in row:
				l.append(item)
			output.append(l)
		return output

	def isSolved(self,state=None):
		if state == None:
			state = self.current_state
		try:
			if len(state) == 0:
				return False
			for row in state:
				for item in row:
					if int(item) == -1:
						return False
			return True
		except Exception as exception:
			print "Checking puzzle exception " + exception 
		return False

	def allPossibleMoveOfPiece(self,piece,state=None):
		# Return empty list if the piece is not correct
		if int(piece) < 2:
			return []

		if state == None:
			state = self.current_state

		blockSide = getBlockSide(state,piece)
		vertical = blockSide[0]
		horizontal = blockSide[1]

		output = ["UP","DOWN","RIGHT","LEFT"]
		
		# Check UP move
		up_pos = horizontal[0] - 1
		for piece_pos in vertical:
			if int(state[up_pos][piece_pos]) != 0:
				output.remove('UP')
				break
	
		# Check DOWN move
		down_pos = horizontal[len(horizontal)-1] + 1
		for piece_pos in vertical:
			if int(state[down_pos][piece_pos]) != 0:
				output.remove('DOWN')
				break

		# Check LEFT move
		left_pos = vertical[0] - 1
		for piece_pos in horizontal:
			if int(state[piece_pos][left_pos]) != 0:
				output.remove('LEFT')
				break

		# Check RIGHT move
		right_pos = vertical[len(vertical)-1] + 1
		for piece_pos in horizontal:
			if int(state[piece_pos][right_pos]) != 0:
				output.remove('RIGHT')
				break

		return output
		
	def allPossibleMoveOfBoard(self,state=None):
		if state == None:
			state = self.current_state
		piece = {}
		for row in state:
			for item in row:
				if item not in piece and int(item) > 1:
					piece[item] = None
		
		for key in piece:
			piece[key] = self.allPossibleMoveOfPiece(key,state)
		
		return piece


	def applyMove(self,piece,direction,state):
		possibleMove = self.allPossibleMoveOfPiece(piece,state)
		if direction not in possibleMove:
			return
		else:
			blockSide = getBlockSide(state,piece)
			vertical = blockSide[0]
			horizontal = blockSide[1]
			if direction == "UP":
				new_empty_pos = horizontal[len(horizontal)-1]
				for i in range(0,len(horizontal)): 
					horizontal[i] -= 1
				for i in horizontal:
					for j in vertical:
						state[i][j] = piece
						state[new_empty_pos][j] = 0
			elif direction == "DOWN":
				new_empty_pos = horizontal[0]
				for i in range(0,len(horizontal)): 
					horizontal[i] += 1
				for i in horizontal:
					for j in vertical:
						state[i][j] = piece
						state[new_empty_pos][j] = 0
			elif direction == "LEFT":
				new_empty_pos = vertical[len(vertical)-1]
				for i in range(0,len(vertical)): 
					vertical[i] -= 1
				for i in horizontal:
					for j in vertical:
						state[i][j] = piece
						state[i][new_empty_pos] = 0
			else:
				new_empty_pos = vertical[0]
				for i in range(0,len(vertical)): 
					vertical[i] += 1
				for i in horizontal:
					for j in vertical:
						state[i][j] = piece
						state[i][new_empty_pos] = 0

	def applyMoveCloning(self,piece,direction,state=None):
		if state == None:
			state = self.current_state
		new_state = self.cloneState(state)
		self.applyMove(new_state,piece,direction)
		return new_state

	def isComparison(self,compare_state,original_state=None):
		if original_state == None:
			state1 = self.current_state
		state2 = compare_state
		try:
			if len(state1) != len(state2):
				return False
			for i in range(0,len(state1)):
				if len(state1[i]) != len(state2[i]):
					return False
				for j in range(0,len(state1[i])):
					if state1[i][j] != state2[i][j]:
						return False
			return True
		except Exception as exception: 
			print "Compare state exception" + exception
		return False

	def normalizeState(self):
		nextIdx = 3
		for i in range(0,len(self.current_state)):
			for j in range(0,len(self.current_state[i])):
				if self.current_state[i][j] == nextIdx:
					nextIdx += 1
				elif self.current_state[i][j] > nextIdx:
					swapIdx(self.current_state,nextIdx,self.current_state[i][j])
					nextIdx += 1


	def randomWalk(self,n,state=None):
		if state == None:
			state = self.current_state

		all_move = self.allPossibleMoveOfBoard(state)
		no_move_pieces = []
		for item in all_move:
			if len(all_move[item]) == 0:
				no_move_pieces.append(item)
		for item in no_move_pieces:
			all_move.pop(item,None)
		



#1) generate all the moves that can be generated in the board, 2) select one at random, 3) execute it, 4) normalize the resulting game state, 5) if we have reached the goal, or if we have executed N moves, stop; otherwise, go back to 1.


print "-------All Possible Move----------"
c = SlidingBrickPuzzle()
print "Game State:"
c.loadGameStateFromDisk("SBP-level3.txt")
c.displayGameState()
print "\nPossible move of piece 6: "
print c.allPossibleMoveOfPiece(6)
print "\nAll possible move of board: "
print c.allPossibleMoveOfBoard()
print "-------------------------------------------"

print "\n"

print "--------Apply Move---------"
print "Game State: "
c.displayGameState()
print "\nApply Move of Piece 8 Direction UP: "
c.applyMove(8,"UP",c.current_state)
c.displayGameState()
print "\nApply Move of Piece 8 Direction DOWN: "
c.applyMove(8,"DOWN",c.current_state)
c.displayGameState()
print "\nApply Move of Piece 9 Direction LEFT: "
c.applyMove(9,"LEFT",c.current_state)
c.displayGameState()
print "\nApply Move of Piece 9 Direction RIGHT: "
c.applyMove(9,"RIGHT",c.current_state)
c.displayGameState()
print "---------------------------"

print "\n"

print "------------Random Walk-----------"
c.randomWalk(3)
print "----------------------------------"