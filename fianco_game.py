import numpy as np


class FiancoGame:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        # Set up the black pieces (top of the board)
        self.board[0, :] = 2  # Full row of black pieces
        self.board[1, [1, 7]] = 2
        self.board[2, [2, 6]] = 2
        self.board[3, [3, 5]] = 2

        # Set up the white pieces (bottom of the board)
        self.board[8, :] = 1  # Full row of white pieces
        self.board[7, [1, 7]] = 1
        self.board[6, [2, 6]] = 1
        self.board[5, [3, 5]] = 1

        self.current_player = 1

    def get_possible_moves(self, player):
        moves = []
        captures = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == player:
                    # Check regular moves
                    for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        if player == 1:
                            di = -di  # White moves upwards
                        if 0 <= i + di < 9 and 0 <= j + dj < 9 and self.board[i + di][j + dj] == 0:
                            moves.append((i, j, i + di, j + dj))

                    # Check capture moves
                    for di, dj in [(2, 2), (2, -2), (-2, 2), (-2, -2)]:
                        if player == 1:
                            di = -di  # White moves upwards
                        if 0 <= i + di < 9 and 0 <= j + dj < 9 and self.board[i + di][j + dj] == 0:
                            if self.board[i + di // 2][j + dj // 2] == 3 - player:  # Opponent's piece
                                captures.append((i, j, i + di, j + dj))

        return captures if captures else moves

    def make_move(self, move):
        start_i, start_j, end_i, end_j = move
        print(f"Moving piece from ({start_i}, {start_j}) to ({end_i}, {end_j})")  # Debugging line
        print(f"Piece at start: {self.board[start_i][start_j]}")  # Debugging line

        self.board[end_i][end_j] = self.board[start_i][start_j]  # Move the piece
        self.board[start_i][start_j] = 0  # Empty the starting position

        if abs(start_i - end_i) == 2:  # This checks if it's a capture move
            capture_i = (start_i + end_i) // 2
            capture_j = (start_j + end_j) // 2
            print(f"Captured piece at ({capture_i}, {capture_j})")  # Debugging line
            self.board[capture_i][capture_j] = 0  # Remove the captured piece

        print("Board after move:")
        self.print_board()  # Debugging line to see the board state after each move

        self.current_player = 3 - self.current_player

    def is_terminal(self):
        return 1 in self.board[0, :] or 2 in self.board[8, :]

    def evaluate(self):
        # Simple evaluation: difference in piece count and advancement
        white_score = np.sum(self.board == 1) + np.sum(8 - np.where(self.board == 1)[0])
        black_score = np.sum(self.board == 2) + np.sum(np.where(self.board == 2)[0])
        return white_score - black_score if self.current_player == 1 else black_score - white_score

    def print_board(self):
        bold_start = "\033[1m"
        bold_end = "\033[0m"

        print("    A   B   C   D   E   F   G   H   I")
        print("  +---+---+---+---+---+---+---+---+---+")
        for i in range(9):
            row = str(9 - i) + " | "  # Adjust row number to match the bottom-up numbering
            for j in range(9):
                if self.board[i, j] == 1:
                    row += f'{bold_start}W{bold_end} | '
                elif self.board[i, j] == 2:
                    row += f'{bold_start}B{bold_end} | '
                else:
                    row += '  | '
            print(row + str(9 - i))
            print("  +---+---+---+---+---+---+---+---+---+")
        print("    A   B   C   D   E   F   G   H   I")


def convert_move_to_notation(start_i, start_j, end_i, end_j):
    start_row = str(9 - start_i)  # Convert to row number as seen by the user
    end_row = str(9 - end_i)
    start_col = chr(ord('A') + start_j)  # Convert to column letter
    end_col = chr(ord('A') + end_j)
    return f"{start_col}{start_row} {end_col}{end_row}"


def negamax(game, depth, alpha, beta, color):
    if depth == 0 or game.is_terminal():
        return color * game.evaluate()

    max_value = float('-inf')
    for move in game.get_possible_moves(game.current_player):
        game_copy = FiancoGame()
        game_copy.board = np.copy(game.board)
        game_copy.current_player = game.current_player
        game_copy.make_move(move)
        value = -negamax(game_copy, depth - 1, -beta, -alpha, -color)
        max_value = max(max_value, value)
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return max_value


def main():
    game = FiancoGame()
    print("Initial board state:")
    game.print_board()

    while not game.is_terminal():
        if game.current_player == 1:
            move = input("Enter your move (e.g., A1 A2 or a1 a2): ").upper()  # Convert input to uppercase
            start_pos, end_pos = move.split()
            start_i, start_j = int(start_pos[1]) - 1, ord(start_pos[0]) - ord('A')
            end_i, end_j = int(end_pos[1]) - 1, ord(end_pos[0]) - ord('A')
            game.make_move((start_i, start_j, end_i, end_j))
        else:
            best_move = None
            best_value = float('-inf')
            for move in game.get_possible_moves(game.current_player):
                game_copy = FiancoGame()
                game_copy.board = np.copy(game.board)
                game_copy.current_player = game.current_player
                game_copy.make_move(move)
                value = -negamax(game_copy, 3, float('-inf'), float('inf'), -1)
                if value > best_value:
                    best_value = value
                    best_move = move

            # Convert the best_move to human-readable format
            ai_move_notation = convert_move_to_notation(*best_move)
            print(f"AI's chosen move: {ai_move_notation}")
            game.make_move(best_move)

        print("Board state after move:")
        game.print_board()

    print("Game over!")


if __name__ == "__main__":
    main()
