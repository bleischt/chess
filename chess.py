from queue import Queue

NUM_ROWS = 8  # rows
NUM_COLS = 8  # cols
EMPTY_CHAR = 'O'
OCCUPIED_CHAR = 'X'

BISHOP = 'bishop'
KING = 'king'
ROOK = 'rook'
KNIGHT = 'knight'

SUPPORTED_PIECES = {BISHOP, KING, ROOK, KNIGHT}


def generate_board(occupied_spots):
    """
    Generates a chess game board containing characters marking the empty and occupied spots.

    Should any input occupied spots be located out of the bounds of the board, they will be ignored.

    :param occupied_spots: a set of locations to be marked as occupied by chess pieces on the game board
    :return a 2D list of characters representing the game board, with dimensions HEIGHT and LENGTH, character EMPTY_CHAR
     for a spot containing no chess piece, and character OCCUPIED_CHAR for a spot containing a
     chess piece
    """
    board = [[EMPTY_CHAR for row in range(NUM_ROWS)] for col in range(NUM_COLS)]
    for spot in occupied_spots:
        if is_within_board(spot):
            board[spot[0]][spot[1]] = OCCUPIED_CHAR
    return board


def print_board(board):
    """
    Prints a simple character representation of the board to stdout.

    :param board: a 2D list of characters representing the game board, with dimensions HEIGHT and LENGTH, character EMPTY_CHAR
     for a spot containing no chess piece, and character OCCUPIED_CHAR for a spot containing a
     chess piece
    """
    for row in board:
        print(row)


def is_within_board(cur_loc):
    """
    Determines if the given location falls withing the bounds of the game board.

    :param cur_loc: an integer tuple representing the location to check for falling within board bounds
    :return: True if the given location lies within the bounds of the game board, False if it lies outside
    """
    row = cur_loc[0]
    col = cur_loc[1]
    return row >= 0 and row < NUM_ROWS and col >= 0 and col < NUM_COLS


def is_occupied_spot(board, cur_loc):
    """
    Determine if the given location is occupied by a chess piece on the game board.

    :param board: a 2D list of characters representing the game board, with dimensions HEIGHT and LENGTH, character EMPTY_CHAR
     for a spot containing no chess piece, and character OCCUPIED_CHAR for a spot containing a
     chess piece
    :param cur_loc: an integer tuple representing the location being considered
    :return: True if the given location is occupied by a chess piece, False if it's open,
     or None if the given location doesn't lie within the bounds of the game board
    """
    if not is_within_board(cur_loc):
        return None
    return board[cur_loc[0]][cur_loc[1]] == OCCUPIED_CHAR


def generate_possible_moves(board, cur_loc, piece):
    """
    Generates all possible valid moves of the given piece from its current location
    on the board.

    :param board: a 2D list of characters representing the game board, with dimensions HEIGHT and LENGTH, character EMPTY_CHAR
     for a spot containing no chess piece, and character OCCUPIED_CHAR for a spot containing a
     chess piece
    :param cur_loc: an integer tuple representing the current location of the given chess piece on the game board
    :param piece: the chess piece to be moved
    :return: a set of integer tuples representing valid locations the given chess piece can move to on the game board
    """
    if not is_within_board(cur_loc) or piece.lower() not in SUPPORTED_PIECES:
        return None

    possible_moves = []
    if piece.lower() == KING:
        possible_moves = __gen_possible_king_moves(cur_loc)
    if piece.lower() == ROOK:
        possible_moves = __gen_possible_rook_moves(board, cur_loc)
    if piece.lower() == KNIGHT:
        possible_moves = __gen_possible_knight_moves(cur_loc)
    if piece.lower() == BISHOP:
        possible_moves = __gen_possible_bishop_moves(board, cur_loc)

    return keep_valid_moves(board, possible_moves)


def __gen_possible_king_moves(cur_loc):
    """
    Generates all possible moves for a knight chess piece given its current location on the game board.
    These moves are not necessarily all valid.
    """
    row = cur_loc[0]
    col = cur_loc[1]

    possible_moves = [
        (row - 1, col),
        (row - 1, col + 1),
        (row, col + 1),
        (row + 1, col + 1),
        (row + 1, col),
        (row + 1, col - 1),
        (row, col - 1),
        (row - 1, col - 1)
    ]

    return possible_moves


def __gen_possible_knight_moves(cur_loc):
    """
    Generates all possible moves for a knight chess piece given its current location on the game board.
    These moves are not necessarily all valid.
    """
    row = cur_loc[0]
    col = cur_loc[1]

    possible_moves = [
        (row - 1, col - 2),
        (row - 2, col - 1),
        (row - 2, col + 1),
        (row - 1, col + 2),
        (row + 1, col + 2),
        (row + 2, col + 1),
        (row + 2, col - 1),
        (row + 1, col - 2)
    ]

    return possible_moves


def __gen_possible_rook_moves(board, cur_loc):
    """
    Generates all possible valid moves for a rook chess piece given its current location on the game board.
    """
    possible_moves = []

    __gen_moves_in_direction(board, possible_moves, cur_loc, 1, 0)
    __gen_moves_in_direction(board, possible_moves, cur_loc, -1, 0)
    __gen_moves_in_direction(board, possible_moves, cur_loc, 0, 1)
    __gen_moves_in_direction(board, possible_moves, cur_loc, 0, -1)

    return possible_moves


def __gen_possible_bishop_moves(board, cur_loc):
    """
    Generates all possible valid moves for a bishop chess piece given its current location on the game board.
    """
    possible_moves = []

    __gen_moves_in_direction(board, possible_moves, cur_loc, 1, 1)
    __gen_moves_in_direction(board, possible_moves, cur_loc, -1, -1)
    __gen_moves_in_direction(board, possible_moves, cur_loc, 1, -1)
    __gen_moves_in_direction(board, possible_moves, cur_loc, -1, 1)

    return possible_moves


def __gen_moves_in_direction(board, moves_list, cur_loc, add_to_row, add_to_col):
    """
    Generates moves in any straight line direction based on current location and
    given increments to row and column.


    Ex: Given location (0,0), addToRow=1, and addToCol=1, function will return
    (1,1), (2,2), (3,3), etc. (diagonal down right) until edge of the game board
    is reached or until spot is occupied.
    """
    row = cur_loc[0] + add_to_row
    col = cur_loc[1] + add_to_col

    # generate moves in the direction specified by add_to_row/add_to_col until
    # moving in that direction is no longer valid (reaches edge of board or collides with other chess piece)
    while is_within_board((row, col)) and not is_occupied_spot(board, (row, col)):
        moves_list.append((row, col))
        row += add_to_row
        col += add_to_col


def keep_valid_moves(board, possible_moves):
    """
    Returns the set of moves that are valid: not occupied and within the dimensions of
    the game board.

    :param board: a 2D list of characters representing the game board, with dimensions HEIGHT and LENGTH, character EMPTY_CHAR
     for a spot containing no chess piece, and character OCCUPIED_CHAR for a spot containing a
     chess piece
    :param possible_moves: a set of integer tuples representing the moves to check for validity on the game board
    :return: a set of integer tuples representing moves that are valid on the game board
    """
    possible_valid_moves = set()
    for move in possible_moves:
        if is_within_board(move) and not is_occupied_spot(board, move):
            possible_valid_moves.add(move)
    return possible_valid_moves


def is_on_same_color(first_loc, second_loc):
    """
    Determines if the two given locations appear on the same 'color'
    (traditionally white and black) of the chess board.

    :param first_loc: an integer tuple representing the first location to compare
    :param second_loc: an integer tuple representing the second location to compare
    :return: True if the two given locations appear on the same color on the game board,
     False if they appear on different colors, or None if they're not within bounds of the game board
    """
    # One color necessarily has row/col values always following the pattern 'even/even' or 'edd/odd'.
    # The other color necessarily has 'row/col' values always following the pattern 'even/odd' or 'odd/even'.
    # Locations appear on same color if they have same pattern of even and odd values.
    if not is_within_board(first_loc) or not is_within_board(second_loc):
        return None
    return (first_loc[0] % 2 == first_loc[1] % 2) == (second_loc[0] % 2 == second_loc[1] % 2)


def find_shortest_path(board, start_loc, end_loc, piece):
    """
    Finds a shortest path between the given start and end locations
    for the given chess piece on the game board.

    :param board: a 2D list of characters representing the game board, with dimensions HEIGHT and LENGTH, character EMPTY_CHAR
     for a spot containing no chess piece, and character OCCUPIED_CHAR for a spot containing a
     chess piece
    :param start_loc: an integer tuple representing the starting location of the given chess piece
    :param end_loc: an integer tuple representing the desired end location of the given chess piece
    :param piece: the chess piece for which the shortest path is to be found
    :return: a list of locations on the game board required to travel from the given start
     to the given end location (in sequential order), including the start and end locations themselves,
     or None if no path can be found
    """
    if not is_within_board(start_loc) or \
            not is_within_board(end_loc) or \
            is_occupied_spot(board, end_loc):
        return None

    if start_loc == end_loc:
        return [start_loc]
    elif piece.lower() == 'bishop' and not is_on_same_color(start_loc, end_loc):
        return None

    # perform search to find end location and generate path from search
    loc_to_parent = __breadth_first_search(board, start_loc, end_loc, piece)

    if loc_to_parent is None:
        return None

    path = __backtrace(loc_to_parent, start_loc, end_loc)

    return path


def find_min_moves(board, start_loc, end_loc, piece):
    """
    Finds the minimum number of moves required to get from start to end location
    of the specified piece on the given game board, should one exist.

    :param board: a 2D list of characters representing the game board, with dimensions HEIGHT and LENGTH, character EMPTY_CHAR
     for a spot containing no chess piece, and character OCCUPIED_CHAR for a spot containing a
     chess piece
    :param start_loc: an integer tuple representing the starting location of the given chess piece
    :param end_loc: an integer tuple representing the desired end location of the given chess piece
    :param piece: the chess piece for which the minimum number of moves is to be found
    :return: the minimum number of moves required to move from start to end location, or None if
    there is no possible path between the given start and end locations
    """

    path = find_shortest_path(board, start_loc, end_loc, piece)

    if path is None:
        return None

    return len(path) - 1


def __breadth_first_search(board, start_loc, end_loc, piece):
    """
    # Performs a BFS from given start to end location constrained by the possible moves
    of the given piece on the given game board. Returns None if the search fails.
    """
    # queue to maintain the fringe nodes of the BFS
    queue = Queue()
    queue.put(start_loc)

    # set of locations already seen during traversal to avoid cycles during search
    seen = set()
    seen.add(start_loc)

    # mapping from a board location to the location it came from during search
    # ex: (0, 1) -> (0, 0) when performing search starting at location (0,0)
    loc_to_parent = dict()

    # perform BFS by iterating through the fringe nodes and checking for the end location
    while not queue.empty():
        cur_loc = queue.get()
        possible_moves = generate_possible_moves(board, cur_loc, piece)
        for loc in possible_moves:
            # if we haven't already seen this loc before,
            # note the location it came from, add it to the fringe of the BFS, and mark it seen
            if loc not in seen:
                loc_to_parent[loc] = cur_loc
                queue.put(loc)
                seen.add(loc)
            if loc == end_loc:
                return loc_to_parent

    return None

def __backtrace(locToParent, start_loc, end_loc):
    """
    Given the starting and end locations and a mapping of explored nodes to
    parents nodes obtained during search, returns the path from start to end.
    """
    path = []
    cur_loc = end_loc

    # start from end location and continue looking up its parent location
    # until a path from end to start is constructed
    while cur_loc != start_loc:
        path.append(cur_loc)
        cur_loc = locToParent[cur_loc]

    path.append(cur_loc)
    path.reverse()

    return path

