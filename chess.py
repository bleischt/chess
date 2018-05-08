from queue import Queue

HEIGHT = 8 #rows
LENGTH = 8 #cols
EMPTY_CHAR = 'O'
OCCUPIED_CHAR = 'X'


# Generate chess board with  given 
def generateBoard(occupied_spots):
    board = [[EMPTY_CHAR  for row in range(HEIGHT)] for col in range(LENGTH)]
    for spot in occupied_spots:
        board[spot[0]][spot[1]] = OCCUPIED_CHAR
    return board

#Print a simple character representation of the board
def printBoard(board):
    for row in board:
        print(row)

# Returns true if the given location is within the dimensions of the game board.
def isWithinBoard(curLoc):
    row = curLoc[0]
    col = curLoc[1]
    return row >= 0 and row < HEIGHT and col >= 0 and col < LENGTH

#TODO: safer to do both checks within here as general rule of thumb?
#otherwise could get out of bounds index
def isOccupiedSpot(board, curLoc):
    return board[curLoc[0]][curLoc[1]] == OCCUPIED_CHAR

# Returns the set of moves that are valid: not occupied and within the dimensions of 
# the game board.
def keepValidMoves(board, possibleMoves):
    possibleValidMoves = []
    for move in possibleMoves:
        if isWithinBoard(move) and not isOccupiedSpot(board, move):
            possibleValidMoves.append(move)    
    return possibleValidMoves

def _genPossibleKingMoves(curLoc):
    row = curLoc[0]
    col = curLoc[1]

    possibleMoves = [
        (row-1, col),
        (row-1, col+1),
        (row, col+1),
        (row+1, col+1),
        (row+1, col),
        (row+1, col-1),
        (row, col-1),
        (row-1, col-1)
        ]

    return possibleMoves

def _genPossibleKnightMoves(curLoc):
    row = curLoc[0]
    col = curLoc[1]

    possibleMoves = [
        (row-1, col-2),
        (row-2, col-1), 
        (row-2, col+1),
        (row-1, col+2),
        (row+1, col+2),
        (row+2, col+1),
        (row+2, col-1),
        (row+1, col-2)
        ]
    
    return possibleMoves

def _genPossibleRookMoves(board, curLoc):
    possibleMoves = []

    _genMovesInDirection(board, possibleMoves, curLoc, 1, 0)
    _genMovesInDirection(board, possibleMoves, curLoc, -1, 0)
    _genMovesInDirection(board, possibleMoves, curLoc, 0, 1)
    _genMovesInDirection(board, possibleMoves, curLoc, 0, -1)

    return possibleMoves

def _genPossibleBishopMoves(board, curLoc):
    possibleMoves = []

    _genMovesInDirection(board, possibleMoves, curLoc, 1, 1)
    _genMovesInDirection(board, possibleMoves, curLoc, -1, -1)
    _genMovesInDirection(board, possibleMoves, curLoc, 1, -1)
    _genMovesInDirection(board, possibleMoves, curLoc, -1, 1)

    return possibleMoves

# Generates moves in any straight line direction based on current location and
# given increments to row and column.
# Ex: Given location (0,0) and addToRow=1 and addToCol=1,
# function will return (1,1), (2,2), (3,3), etc. (diagonal down right) until edge of the 
# game board is reached or until spot is occupied.
def _genMovesInDirection(board, movesList, curLoc, addToRow, addToCol):
    row = curLoc[0] + addToRow
    col = curLoc[1] + addToCol

    while isWithinBoard((row, col)) and not isOccupiedSpot(board, (row, col)):
        movesList.append((row, col))
        row += addToRow
        col += addToCol

# Generates all possible valid moves of the given piece from its current location
# on the given board
def generatePossibleMoves(board, curLoc, piece): 
    possibleMoves = []
    if piece.lower() == 'king':
        possibleMoves = _genPossibleKingMoves(curLoc)
    if piece.lower() == 'rook':
        possibleMoves = _genPossibleRookMoves(board, curLoc)
    if piece.lower() == 'knight':
        possibleMoves = _genPossibleKnightMoves(curLoc)
    if piece.lower() == 'bishop':
        possibleMoves = _genPossibleBishopMoves(board, curLoc)
    return keepValidMoves(board, possibleMoves) 

# Returs True if the given start and end location are on the same color
def isOnSameColor(startLoc, endLoc):
    # one color has row/col values always even/even or edd/odd
    # other color has row/col values always even/odd or odd/even
    return (startLoc[0] % 2 == startLoc[1] % 2) == (endLoc[0] % 2 == endLoc[1] % 2)

# Finds and returns a shortest path between the given start and end location
# for the given piece on the game board.
def find_shortest_path(board, startLoc, endLoc, piece):
    if not isWithinBoard(startLoc) or \
            not isWithinBoard(endLoc) or \
            isOccupiedSpot(board, endLoc):
        return None

    # if the current piece is a bishop
    # check that it can reach given end location based on the color
    if piece.lower() == 'bishop' and not isOnSameColor(startLoc, endLoc):
        return None
    
    # perform search to find end location and generate path from search
    locToParent, endLoc = _breadth_first_search(board, startLoc, endLoc, piece)
    path = _backtrace(locToParent, startLoc, endLoc)

    return path

# Finds the minimum number of moves to get from start to end location
# of the specified piece on the given game board
def find_min_moves(board, startLoc, endLoc, piece):
    path = find_shortest_path(board, startLoc, endLoc, piece)
    if len(path) == 0:
        return None
    return len(path) - 1

# Performs a BFS from given start to end location constrained by the 
# possible moves of the given piece on the given game board.
def _breadth_first_search(board, startLoc, endLoc, piece):
    queue = Queue()
    queue.put(startLoc)

    seen = set()
    seen.add(startLoc)

    locToParent = dict()

    while not queue.empty():
        curLoc = queue.get()
        print('curLoc:', curLoc)
        possibleMoves = generatePossibleMoves(board, curLoc, piece)
        print('possibleMoves:')
        for move in possibleMoves:
            if move not in seen:
                locToParent[move] = curLoc
                queue.put(move)
                seen.add(move)
                print(move)
            if move == endLoc:
                return (locToParent, endLoc)
    print('no end location found!')
    return None

# Given the starting and end locations and a mapping of explored nodes to
# parents nodes obtained during search, returns the path from start to end.
def _backtrace(locToParent, startLoc, endLoc):
    path = []
    curLoc = endLoc
    while curLoc != startLoc:
        path.append(curLoc)
        curLoc = locToParent[curLoc]
    path.append(curLoc)
    path.reverse()
    return path

#board[1][1] = 'X'
#board[2][2] = 'X'
#board[3][4] = 'X'
#printBoard(board)
#print(_genPossibleKingMoves((3,3)))
#print(keepValidMoves(board, _genPossibleKingMoves((3,3))))
#print(_genPossibleKingMoves((0,0)))
#print(keepValidMoves(board, _genPossibleKingMoves((0,0))))


board = generateBoard([(1,1), (2,2), (3,4)])
startLoc = (1,6)
board[startLoc[0]][startLoc[1]] = 'S'
endLoc = (3,2)
board[endLoc[0]][endLoc[1]] = 'E'
printBoard(board)
#locToParent,endLoc = _breadth_first_search(board, startLoc, endLoc, 'king')
path = find_shortest_path(board, startLoc, endLoc, 'bishop')
print('path:', path)
#numMoves = find_min_moves(board, startLoc, endLoc, 'bishop')
#print('numMoves:', numMoves)
#print('locToParent:', locToParent)
#print('endLoc:', endLoc)
#path = _backtrace(locToParent, startLoc, endLoc)
print('path:', path)
for move in path:
    if move != startLoc and move != endLoc:
        board[move[0]][move[1]] = '-'

printBoard(board)


