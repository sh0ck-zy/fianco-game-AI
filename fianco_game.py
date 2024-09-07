import numpy as np
import time


class FiancoGame:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self._setup_board()
        self.current_player = 1  # White starts
        self.move_count = 0
        self.ai_time = 0

    def _setup_board(self):
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

    def get_possible_moves(self, player):
        moves = []
        captures = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == player:
                    # Check regular moves (forward and sideways only)
                    directions = [(0, -1), (0, 1)]  # Sideways moves
                    if player == 1:  # White moves up
                        directions.append((-1, 0))
                    else:  # Black moves down
                        directions.append((1, 0))

                    for di, dj in directions:
                        new_i, new_j = i + di, j + dj
                        if 0 <= new_i < 9 and 0 <= new_j < 9 and self.board[new_i][new_j] == 0:
                            moves.append((i, j, new_i, new_j))

                    # Check capture moves (only forward captures)
                    capture_directions = [(2, 2), (2, -2)] if player == 1 else [(-2, 2), (-2, -2)]
                    for di, dj in capture_directions:
                        new_i, new_j = i + di, j + dj
                        mid_i, mid_j = i + di // 2, j + dj // 2
                        if (0 <= new_i < 9 and 0 <= new_j < 9 and
                                self.board[new_i][new_j] == 0 and
                                self.board[mid_i][mid_j] == 3 - player):
                            captures.append((i, j, new_i, new_j))

        return captures if captures else moves

    def make_move(self, move):
        start_i, start_j, end_i, end_j = move
        self.board[end_i][end_j] = self.board[start_i][start_j]
        self.board[start_i][start_j] = 0

        if abs(start_i - end_i) == 2:  # Capture move
            capture_i, capture_j = (start_i + end_i) // 2, (start_j + end_j) // 2
            self.board[capture_i][capture_j] = 0

        self.current_player = 3 - self.current_player
        self.move_count += 1

    def is_terminal(self):
        # Check if any player has reached the opposite side
        if 1 in self.board[0, :] or 2 in self.board[8, :]:
            return True

        # Check if any player has no pieces left
        if 1 not in self.board or 2 not in self.board:
            return True

        # Check if current player has no valid moves
        if not self.get_possible_moves(self.current_player):
            return True

        return False

    def get_winner(self):
        if 1 in self.board[0, :]:
            return 1  # White wins
        if 2 in self.board[8, :]:
            return 2  # Black wins
        if 1 not in self.board:
            return 2  # Black wins by capturing all white pieces
        if 2 not in self.board:
            return 1  # White wins by capturing all black pieces
        if not self.get_possible_moves(self.current_player):
            return 3 - self.current_player  # Current player has no moves, so opponent wins
        return None  # No winner yet

    def validate_move(self, move):
        start_i, start_j, end_i, end_j = move
        player = self.current_player
        possible_moves = self.get_possible_moves(player)

        if move not in possible_moves:
            return False

        # Check for mandatory captures
        captures = [m for m in possible_moves if abs(m[0] - m[2]) == 2]
        if captures and move not in captures:
            return False

        return True

    def validate_move(self, move):
        possible_moves = self.get_possible_moves(self.current_player)
        return move in possible_moves

    def evaluate(self):
        winner = self.get_winner()
        if winner == self.current_player:
            return 1000
        elif winner == 3 - self.current_player:
            return -1000

        # Count pieces and their advancement
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


def convert_notation_to_move(notation):
    start, end = notation.split()
    start_col, start_row = ord(start[0]) - ord('A'), int(start[1]) - 1
    end_col, end_row = ord(end[0]) - ord('A'), int(end[1]) - 1
    return (8 - start_row, start_col, 8 - end_row, end_col)


def convert_move_to_notation(move):
    start_i, start_j, end_i, end_j = move
    start = chr(start_j + ord('A')) + str(9 - start_i)
    end = chr(end_j + ord('A')) + str(9 - end_i)
    return f"{start} {end}"


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
    print("Welcome to Fianco!")
    ai_color = input("Choose AI color (W/B): ").upper()
    ai_player = 1 if ai_color == 'W' else 2
    human_player = 3 - ai_player

    print("Initial board state:")
    game.print_board()

    game_start_time = time.time()

    while not game.is_terminal():
        if game.current_player == human_player:
            while True:
                move_notation = input("Enter your move (e.g., A1 A2): ").upper()
                move = convert_notation_to_move(move_notation)
                if game.validate_move(move):
                    game.make_move(move)
                    break
                else:
                    print("Invalid move. Try again.")
        else:
            print("AI is thinking...")
            ai_move_start_time = time.time()
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

            ai_move_end_time = time.time()
            ai_move_duration = ai_move_end_time - ai_move_start_time
            game.ai_time += ai_move_duration

            ai_move_notation = convert_move_to_notation(best_move)
            print(f"AI played: {ai_move_notation}")
            print(f"Time for this move: {ai_move_duration:.2f} seconds")
            game.make_move(best_move)

        print("\nBoard state after move:")
        game.print_board()
        print(f"Move count: {game.move_count}")
        print(f"Total AI thinking time: {game.ai_time:.2f} seconds")

        current_game_duration = time.time() - game_start_time
        print(f"Total game duration: {current_game_duration:.2f} seconds")

    print("Game over!")
    winner = "White" if game.current_player == 2 else "Black"
    print(f"{winner} wins!")

    final_game_duration = time.time() - game_start_time
    print(f"Final game duration: {final_game_duration:.2f} seconds")
    print(f"Final AI total thinking time: {game.ai_time:.2f} seconds")


if __name__ == "__main__":
    main()