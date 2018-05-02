from collections import deque

WIDTH = 8
HEIGHT = 8
EMPTY_CHAR = 'O'

board = [[EMPTY_CHAR  for row in range(WIDTH)] for col in range(HEIGHT)]

start = (1, 1)
end = (5, 2)

def printBoard(board):
    for row in board:
        print(row)

def isWithinBoard(curLoc):
    row = curLoc[0]
    col = curLoc[1]
    return row >= 0 and row < WIDTH and col >= 0 and col < HEIGHT

def isOccupiedSpot(board, curLoc):
    return board[curLoc[0]][curLoc[1]] != EMPTY_CHAR

def keepValidMoves(board, possibleMoves):
    possibleValidMoves = []
    for move in possibleMoves:
        if not isOccupiedSpot(board, move) and isWithinBoard(move):
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

def generatePossibleMoves(board, curLoc, piece): 
    possibleMoves = []
    if piece.lower() == 'king':
        possibleMoves = _genPossibleKingMoves(curLoc)
    return keepValidMoves(board, possibleMoves) 


board[1][1] = 'X'
board[2][2] = 'X'
board[3][4] = 'X'
printBoard(board)
print(_genPossibleKingMoves((3,3)))
print(keepValidMoves(board, _genPossibleKingMoves((3,3))))
print(_genPossibleKingMoves((0,0)))
print(keepValidMoves(board, _genPossibleKingMoves((0,0))))




