"""
Library to assist chess player by finding the minimum number of moves for a given chess
piece from a given

"""
from chess import find_min_moves
import chess

def main():

    # Example 1 - King Min Moves
    chess_piece = chess.KING
    board = chess.generate_board({})
    start_location = (3, 3)
    end_location = (5, 1)
    min_num_moves = find_min_moves(board, start_location, end_location, chess_piece)
    print("A {} can move from location {} to {} in {} moves minimum.".
          format(chess_piece, start_location, end_location, min_num_moves))
    print()

    # Example 2 - Knight Path
    chess_piece = chess.KNIGHT
    board = chess.generate_board({(2, 2), (2, 3), (3, 3), (3,2), (3,4), (4,4)})
    start_location = (4, 1)
    end_location = (2, 5)
    path = chess.find_shortest_path(board, start_location, end_location, chess_piece)
    print("A {} can move from location {} to {} in {} moves minimum.".
          format(chess_piece, start_location, end_location, len(path) - 1))
    print("One possible shortest path:", path)

    # Add some markings to the board to show path, and print board
    for move in path:
        board[move[0]][move[1]] = '-'
    board[start_location[0]][start_location[1]] = 'S'
    board[end_location[0]][end_location[1]] = 'E'
    chess.print_board(board)

if __name__ == "__main__":
    main()