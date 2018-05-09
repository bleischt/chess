from unittest import TestCase

import chess
from chess import generate_board
from chess import is_within_board
from chess import keep_valid_moves
from chess import is_occupied_spot
from chess import generate_possible_moves
from chess import is_on_same_color
from chess import find_shortest_path
from chess import find_min_moves

class TestChessLib(TestCase):

    def test_generate_board(self):

        # empty board
        board = generate_board([])
        for row in board:
            for char in row:
                self.assertEqual(chess.EMPTY_CHAR, char)

        # board with occupied spots, both in and out of bounds
        occupied_spots = {(2,3), (1, 1), (1, 1), (7, 3), (9, 12), (-1, 2)}
        board = generate_board(occupied_spots)
        for row in range(chess.NUM_ROWS):
            for col in range(chess.NUM_COLS):
                if (row, col) in occupied_spots:
                    self.assertEqual(chess.OCCUPIED_CHAR, board[row][col])
                else:
                    self.assertEqual(chess.EMPTY_CHAR, board[row][col])

        # board with all spots occupied
        occupied_spots = {(row, col) for row in range(chess.NUM_ROWS) for col in range(chess.NUM_COLS)}
        board = generate_board(occupied_spots)
        for row in range(chess.NUM_ROWS):
            for col in range(chess.NUM_COLS):
                self.assertEqual(chess.OCCUPIED_CHAR, board[row][col])


    def test_is_within_board(self):
        # test middle valid
        cur_loc = (2, 3)
        result = is_within_board(cur_loc)
        self.assertTrue(result)

        # test border valid
        cur_loc = (7, 0)
        result = is_within_board(cur_loc)
        self.assertTrue(result)

        # test neg row
        cur_loc = (-8, 3)
        result = is_within_board(cur_loc)
        self.assertFalse(result)

        # test neg col
        cur_loc = (8, -3)
        result = is_within_board(cur_loc)
        self.assertFalse(result)

        # test neg row & neg col
        cur_loc = (-1, -3)
        result = is_within_board(cur_loc)
        self.assertFalse(result)

        # test big row
        cur_loc = (8, 3)
        result = is_within_board(cur_loc)
        self.assertFalse(result)

        # test big col
        cur_loc = (1, 8)
        result = is_within_board(cur_loc)
        self.assertFalse(result)

        # test big row and col
        cur_loc = (18, 8)
        result = is_within_board(cur_loc)
        self.assertFalse(result)


    def test_is_occupied_spot(self):
        # test occupied
        board = generate_board({(3, 3), (0, 0)})
        cur_loc = (3, 3)
        result = is_occupied_spot(board, cur_loc)
        self.assertTrue(result)

        # test not occupied
        board = generate_board({(1, 2), (3, 4)})
        cur_loc = (3, 3)
        result = is_occupied_spot(board, cur_loc)
        self.assertFalse(result)

        # test out of bounds
        board = generate_board({})
        cur_loc = (-3, 3)
        result = is_occupied_spot(board, cur_loc)
        self.assertIsNone(result)

    def test_keep_valid_moves(self):

        # test all valid
        board = generate_board({(6, 3)})
        moves = {(1, 1), (2, 3), (4, 2)}
        result = keep_valid_moves(board, moves)
        self.assertEqual(moves, set(result))

        # test empty
        board = generate_board({})
        moves = set()
        result = keep_valid_moves(board, moves)
        self.assertEqual(set(), result)

        # test remove out of bounds
        board = generate_board({(6, 3)})
        moves = {(1, 1), (2, -3), (14, 2)}
        result = keep_valid_moves(board, moves)
        self.assertEqual({(1,1 )}, result)

        # test occupied
        board = generate_board({(6, 3), (2, 3)})
        moves = {(1, 1), (2, 3), (4, 2)}
        result = keep_valid_moves(board, moves)
        self.assertEqual({(1, 1), (4, 2)}, result)

        # test out of bounds and occupied
        board = generate_board({(6, 3)})
        moves = {(1, -1), (2, 3), (4, 12)}
        result = keep_valid_moves(board, moves)
        self.assertEqual({(2, 3)}, result)

    def test_generate_possible_moves(self):
        # test king middle
        board = generate_board({})
        cur_loc = (3, 3)
        result = generate_possible_moves(board, cur_loc, chess.KING)
        expected = {(3, 2), (2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2)}
        self.assertEqual(result, expected)

        # test king edge
        board = generate_board({})
        cur_loc = (0, 0)
        result = generate_possible_moves(board, cur_loc, chess.KING)
        expected = {(0, 1), (1, 1), (1, 0)}
        self.assertEqual(result, expected)

        # test king edge with obstacles
        board = generate_board({(1, 2), (0, 2), (0, 3)})
        cur_loc = (1, 3)
        result = generate_possible_moves(board, cur_loc, chess.KING)
        expected = {(0, 4), (1, 4), (2, 4), (2, 3), (2, 2)}
        self.assertEqual(result, expected)

        # test bishop middle
        board = generate_board({})
        cur_loc = (1, 5)
        result = generate_possible_moves(board, cur_loc, chess.BISHOP)
        expected = {(0, 4), (0, 6), (2, 6), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0), (3, 7)}
        self.assertEqual(result, expected)

        # test bishop edge
        board = generate_board({})
        cur_loc = (1, 0)
        result = generate_possible_moves(board, cur_loc, chess.BISHOP)
        expected = {(0, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6)}
        self.assertEqual(result, expected)

        # test bishop with obstacles
        board = generate_board({})
        cur_loc = (1, 5)
        result = generate_possible_moves(board, cur_loc, chess.BISHOP)
        expected = {(0, 4), (0, 6), (2, 6), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0), (3, 7)}
        self.assertEqual(result, expected)

        # test knight middle
        board = generate_board({})
        cur_loc = (4, 3)
        result = generate_possible_moves(board, cur_loc, chess.KNIGHT)
        expected = {(2, 2), (3, 1), (5, 1), (6, 2), (2, 4), (3, 5), (5, 5), (6, 4)}
        self.assertEqual(result, expected)

        # test knight edge
        board = generate_board({})
        cur_loc = (7, 7)
        result = generate_possible_moves(board, cur_loc, chess.KNIGHT)
        expected = {(5, 6), (6, 5)}
        self.assertEqual(result, expected)

        # test knight with obstacles
        board = generate_board({(3, 1), (6, 2)})
        cur_loc = (4, 3)
        result = generate_possible_moves(board, cur_loc, chess.KNIGHT)
        expected = {(2, 2), (5, 1), (2, 4), (3, 5), (5, 5), (6, 4)}
        self.assertEqual(result, expected)

        # test rook middle
        board = generate_board({})
        cur_loc = (4, 3)
        result = generate_possible_moves(board, cur_loc, chess.ROOK)
        expected = {(3, 3), (2, 3), (1, 3), (0, 3), (5, 3), (6, 3), (7, 3),
                    (4, 2), (4, 1), (4, 0), (4, 4), (4, 5), (4, 6), (4, 7)}
        self.assertEqual(result, expected)

        # test rook edge
        board = generate_board({})
        cur_loc = (7, 0)
        result = generate_possible_moves(board, cur_loc, chess.ROOK)
        expected = {(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
                    (7, 7), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)}
        self.assertEqual(result, expected)

        # test rook with obstacles
        board = generate_board({(2, 3), (4, 0), (4, 2)})
        cur_loc = (4, 3)
        result = generate_possible_moves(board, cur_loc, chess.ROOK)
        expected = {(3, 3), (5, 3), (6, 3), (7, 3), (4, 4), (4, 5), (4, 6), (4, 7)}
        self.assertEqual(result, expected)

        # test no moves - boxed off
        board = generate_board({(1, 0), (1, 2), (3, 0), (3, 2)})
        cur_loc = (2, 1)
        result = generate_possible_moves(board, cur_loc, chess.BISHOP)
        self.assertEqual(0, len(result))

        # test out of bounds location 1
        board = generate_board({})
        cur_loc = (-1, 1)
        result = generate_possible_moves(board, cur_loc, chess.KING)
        self.assertIsNone(result)

        # test out of bounds location 2
        board = generate_board({})
        cur_loc = (12, 1)
        result = generate_possible_moves(board, cur_loc, chess.KING)
        self.assertIsNone(result)


    def test_is_on_same_color(self):
        # on same color white
        result = is_on_same_color((0, 0), (0, 2))
        self.assertTrue(result)

        # on same color black
        result = is_on_same_color((3,4), (0, 7))
        self.assertTrue(result)

        # on different color
        result = is_on_same_color((1, 1), (5, 2))
        self.assertFalse(result)

        # out of bounds location one
        result = is_on_same_color((-1, 1), (5, 2))
        self.assertFalse(result)

        #out of bounds location two
        result = is_on_same_color((1, 1), (15, 2))
        self.assertIsNone(result)

    def test_find_shortest_path(self):
        # test king with obstacles
        board = generate_board({(1, 4), (0, 4), (2, 4)})
        start_loc = (1, 2)
        end_loc = (1, 5)
        path = find_shortest_path(board, start_loc, end_loc, chess.KING)
        self.assertEqual(len(path), 5)
        self.assertEqual(path[0], start_loc)
        self.assertEqual(path[-1], end_loc)
        self.assertIn(path[1], generate_possible_moves(board, path[0], chess.KING))
        self.assertIn(path[2], generate_possible_moves(board, path[1], chess.KING))
        self.assertIn(path[3], generate_possible_moves(board, path[2], chess.KING))


        # test bishop with obstacles
        board = generate_board({(4, 1), (3, 2), (2, 1)})
        start_loc = (2, 1)
        end_loc = (5, 2)
        path = find_shortest_path(board, start_loc, end_loc, chess.BISHOP)
        self.assertEqual(len(path), 4)
        self.assertEqual(path[0], start_loc)
        self.assertEqual(path[-1], end_loc)
        self.assertIn(path[1], generate_possible_moves(board, path[0], chess.BISHOP))
        self.assertIn(path[2], generate_possible_moves(board, path[1], chess.BISHOP))


        # test knight with obstacles
        board = generate_board({(2, 2), (2, 3), (3, 3), (3, 2), (3, 4), (4, 4)})
        start_loc = (4, 1)
        end_loc = (2, 5)
        path = find_shortest_path(board, start_loc, end_loc, chess.KNIGHT)
        self.assertEqual(len(path), 5)
        self.assertEqual(path[0], start_loc)
        self.assertEqual(path[-1], end_loc)
        self.assertIn(path[1], generate_possible_moves(board, path[0], chess.KNIGHT))
        self.assertIn(path[2], generate_possible_moves(board, path[1], chess.KNIGHT))
        self.assertIn(path[3], generate_possible_moves(board, path[2], chess.KNIGHT))

        # test rook with obstacles
        board = generate_board({(2, 3), (4, 4), (4, 5), (4, 6), (5, 3), (6, 4)})
        start_loc = (2, 1)
        end_loc = (5, 4)
        path = find_shortest_path(board, start_loc, end_loc, chess.ROOK)
        self.assertEqual(len(path), 5)
        self.assertEqual(path[0], start_loc)
        self.assertEqual(path[-1], end_loc)
        self.assertIn(path[1], generate_possible_moves(board, path[0], chess.ROOK))
        self.assertIn(path[2], generate_possible_moves(board, path[1], chess.ROOK))
        self.assertIn(path[3], generate_possible_moves(board, path[2], chess.ROOK))

    def test_find_min_moves(self):

        # test king middle
        board = generate_board({})
        start_loc = (3, 3)
        end_loc = (5, 1)
        result = find_min_moves(board, start_loc, end_loc, chess.KING)
        self.assertEqual(result, 2)

        # test king edge
        board = generate_board({})
        start_loc = (0, 0)
        end_loc = (7, 7)
        result = find_min_moves(board, start_loc, end_loc, chess.KING)
        self.assertEqual(result, 7)

        # test king with obstacles
        board = generate_board({(1,4), (0,4), (2,4)})
        start_loc = (1, 2)
        end_loc = (1, 5)
        result = find_min_moves(board, start_loc, end_loc, chess.KING)
        self.assertEqual(result, 4)

        # test bishop middle
        board = generate_board({})
        start_loc = (2, 3)
        end_loc = (3, 6)
        result = find_min_moves(board, start_loc, end_loc, chess.BISHOP)
        self.assertEqual(result, 2)

        # test bishop edge
        board = generate_board({})
        start_loc = (0, 7)
        end_loc = (7, 0)
        result = find_min_moves(board, start_loc, end_loc, chess.BISHOP)
        self.assertEqual(result, 1)

        # test bishop with obstacles
        board = generate_board({(4,1), (3,2), (2, 1)})
        start_loc = (2, 1)
        end_loc = (5, 2)
        result = find_min_moves(board, start_loc, end_loc, chess.BISHOP)
        self.assertEqual(result, 3)

        # test knight middle
        board = generate_board({})
        start_loc = (2, 1)
        end_loc = (6, 3)
        result = find_min_moves(board, start_loc, end_loc, chess.KNIGHT)
        self.assertEqual(result, 2)

        # test knight edge
        board = generate_board({})
        start_loc = (0, 0)
        end_loc = (7, 5)
        result = find_min_moves(board, start_loc, end_loc, chess.KNIGHT)
        self.assertEqual(result, 4)

        # test knight with obstacles
        board = generate_board({(2, 2), (2, 3), (3, 3), (3,2), (3,4), (4,4)})
        start_loc = (4, 1)
        end_loc = (2, 5)
        result = find_min_moves(board, start_loc, end_loc, chess.KNIGHT)
        self.assertEqual(result, 4)

        # test rook middle
        board = generate_board({})
        start_loc = (5, 1)
        end_loc = (3, 3)
        result = find_min_moves(board, start_loc, end_loc, chess.ROOK)
        self.assertEqual(result, 2)

        # test rook edge
        board = generate_board({})
        start_loc = (0, 0)
        end_loc = (7, 7)
        result = find_min_moves(board, start_loc, end_loc, chess.ROOK)
        self.assertEqual(result, 2)

        # test rook with obstacles
        board = generate_board({(2,3), (4,4), (4,5), (4,6), (5,3), (6,4)})
        start_loc = (2, 1)
        end_loc = (5, 4)
        result = find_min_moves(board, start_loc, end_loc, chess.ROOK)
        self.assertEqual(result, 4)

        # test unreachable - boxed off
        board = generate_board({(4, 4), (5,5), (5, 3), (6, 4)})
        start_loc = (2, 1)
        end_loc = (5, 4)
        result = find_min_moves(board, start_loc, end_loc, chess.ROOK)
        self.assertIsNone(result)

        # test unreachable - bishop on different color
        board = generate_board({})
        start_loc = (1, 1)
        end_loc = (0, 3)
        result = find_min_moves(board, start_loc, end_loc, chess.BISHOP)
        self.assertIsNone(result)

        # test unreachable - out of bounds start location
        board = generate_board({})
        start_loc = (-1, 1)
        end_loc = (0, 3)
        result = find_min_moves(board, start_loc, end_loc, chess.KING)
        self.assertIsNone(result)

        # test unreachable -  out of bounds end location
        board = generate_board({})
        start_loc = (1, 1)
        end_loc = (200, 3)
        result = find_min_moves(board, start_loc, end_loc, chess.KNIGHT)
        self.assertIsNone(result)

        # test unreachable - piece occupying end location
        board = generate_board({(2,2)})
        start_loc = (1, 1)
        end_loc = (2, 2)
        result = find_min_moves(board, start_loc, end_loc, chess.ROOK)
        self.assertIsNone(result)

        # same start and end location
        board = generate_board({})
        start_loc = (1, 1)
        end_loc = (1, 1)
        result = find_min_moves(board, start_loc, end_loc, chess.KING)
        self.assertEqual(result, 0)


