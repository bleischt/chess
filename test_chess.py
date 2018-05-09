from unittest import TestCase

import chess
from chess import generate_board
from chess import is_within_board
from chess import keep_valid_moves
from chess import is_occupied_spot
from chess import keep_valid_moves
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

    def test_is_within_board(self):
        self.fail()

    def test_is_occupied_spot(self):
        self.fail()

    def test_keep_valid_moves(self):
        self.fail()

    def test_generate_possible_moves(self):
        self.fail()

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
        result = is_on_same_color((1, 1), (5, 2))
        self.assertFalse(result)

        #out of bounds location two
        result = is_on_same_color((1, 1), (5, 2))
        self.assertIsNone(result)

    def test_find_shortest_path(self):
        self.fail()

    def test_find_min_moves(self):

        # test king middle
        board = generate_board({})
        start_loc = (3, 3)
        end_loc = (5, 1)
        result = find_min_moves(board, start_loc, end_loc, chess.KING)
        self.assertEqual(result, 2)

        # test king edge

        # test king with obstacles

        # test bishop middle

        # test bishop edge

        # test bishop with obstacles

        # test knight middle

        # test knight edge

        # test knight with obstacles

        # test rook middle

        # test rook edge

        # test rook with obstacles

        # test unreachable - boxed off

        # test unreachable - bishop on different color

        # test unreachable - out of bounds start location

        #test unreachable -  out of bounds end location

        #test unreachable - piece occupying end location


