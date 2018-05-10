# chess
This project represents a utility class for planning moves in chess with various pieces. It was built with the intent to be able to answer the following problem statement: 

### Problem Statement
Given an 8x8 chess board, find the minimum number of moves required to move a king, knight, and a rook from a given start to a given end location. 

_The currently supported chess pieces are:_
1. King
2. Rook
3. Bishop
4. Knight

### Assumptions
- No constraints are placed on the board other than size (e.g. there can be any number of pieces on it)
- The possible moves for a piece are according to the standard rules of chess (e.g. Knight can jump over other pieces)
- Min moves and shortest path are found assuming no other pieces pieces on the board are moved.

### API Overview
The project is split into a `driver` module to run the app (in this case, examples), a `chess` utility module containing all the chess-related methods, and a `test_chess` unit test module.

Private methods are prefixed with two underscores "__" and are not intended to be available to the user.

The top-level method `find_min_moves` should be used to find the minimum number of moves required for a given chess piece to move from start to end location.

Public Methods:

```
find_min_moves(board, start_location, end_location, chess_piece)
find_shortest_path(board, start_location, end_location, chess_piece)
generate_possible_moves(board, cur_location, chess_piece)
keep_valid_moves(board, possible_moves)
is_within_board(cur_location)
is_occupied_spot(board, cur_location)
is_on_same_color(first_loc, second_location)
generate_board(occupied_spots)
print_board(board)
```

### Game Board
The 8x8 chess board can be printed using the `print_board` method. 

The only information maintained by the board is what the "free" and "occupied" spots are.

Locations are indicated by a tuple of 2 integers (row, column) referencing the board grid. For example, location (1, 2) references row 1, column 2 on the grid below, where the upper left-hand box is considered the origin (0, 0).
```
['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
```

### Instructions to Run Examples & Tests
1. Clone the repository.
2. `cd` into `chess` directory.
3. Run `python3 -m unittest test_chess.py`.
4. Run `python3 driver.py` to view output of examples.




