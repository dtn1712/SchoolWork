from SlidingBrickPuzzle import SlidingBrickPuzzle

# Load game and display game state
a = SlidingBrickPuzzle()
print "------Load Game and Display Game State--------"
a.loadGameStateFromDisk("SBP-level0.txt")
print "Game State: "
a.displayGameState()
print "----------------------------------------------"

print "\n"

print "-------Check Puzzle Solved---------"
a.loadGameStateFromDisk("SBP-level0-true.txt")
print "Game State: "
a.displayGameState()
print "Solve: " + str(a.isSolved())
print "-----------------------------------"

#print a.allPossibleMoveOfPiece(3)

print "\n"

print "-------Check Comparison State--------"
print "State 1: "
a.loadGameStateFromDisk("SBP-level0.txt")
a.displayGameState()
b = SlidingBrickPuzzle()
b.loadGameStateFromDisk("SBP-level0.txt")
print 
print "State 2: "
print b.displayGameState()
print "Is Identical: " + str(a.isComparison(b.current_state))
print "-------------------------------------"

print "\n"

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