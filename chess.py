from queue import Queue

WIDTH = 8
HEIGHT = 8
EMPTY_CHAR = 'O'
OCCUPIED_CHAR = 'X'

#board = [[EMPTY_CHAR  for row in range(WIDTH)] for col in range(HEIGHT)]

def generateBoard(width, height, occupied_spots):
    board = [[EMPTY_CHAR  for row in range(width)] for col in range(height)]
    for spot in occupied_spots:
        board[spot[0]][spot[1]] = OCCUPIED_CHAR
    return board

def printBoard(board):
    for row in board:
        print(row)

def isWithinBoard(curLoc):
    row = curLoc[0]
    col = curLoc[1]
    return row >= 0 and row < WIDTH and col >= 0 and col < HEIGHT

#TODO: safer to do both checks within hear as general rule of thumb?
#otherwise could get out of bounds index
def isOccupiedSpot(board, curLoc):
    return board[curLoc[0]][curLoc[1]] == OCCUPIED_CHAR

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
    pass

def _genPossibleRookMoves(curLoc):
    pass

def _genPossibleBishopMoves(curLoc):
    pass

def generatePossibleMoves(board, curLoc, piece): 
    possibleMoves = []
    if piece.lower() == 'king':
        possibleMoves = _genPossibleKingMoves(curLoc)
    return keepValidMoves(board, possibleMoves) 

def find_shortest_path(board, startLoc, endLoc, piece):
    if not isWithinBoard(board, startLoc) or isOccupied(board, endLoc):
        return None
    
    locToParent, endLoc = _breadth_first_search(board, startLoc, endLoc, piece)
    path = _backtrace(locToParent, endLoc)

    return path

def find_min_moves(board, startLoc, endLoc, piece):
    path = find_shortest_path(board, startLoc, endLoc, piece)
    if len(path) == 0:
        return None
    return len(path) - 1

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
        print('queue:', list(queue))
    print('no end location found!')
    return None

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

board = generateBoard(8, 8, [])
startLoc = (5,0)
board[startLoc[0]][startLoc[1]] = 'S'
endLoc = (3,2)
board[endLoc[0]][endLoc[1]] = 'E'
printBoard(board)
locToParent,endLoc = _breadth_first_search(board, startLoc, endLoc, 'king')
print('locToParent:', locToParent)
print('endLoc:', endLoc)
path = _backtrace(locToParent, startLoc, endLoc)
print('path:', path)
for move in path:
    if move != startLoc and move != endLoc:
        board[move[0]][move[1]] = '-'

printBoard(board)


