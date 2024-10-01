# fianco_game.py

import numpy as np
from constants import BOARD_SIZE

def convert_move_to_notation(move):
    """
    Convert a move tuple to standard notation.
    E.g., (start_i, start_j, end_i, end_j) -> 'A1 A2'
    """
    start_i, start_j, end_i, end_j = move
    start = chr(start_j + ord('A')) + str(9 - start_i)
    end = chr(end_j + ord('A')) + str(9 - end_i)
    return f"{start} {end}"

class FiancoGame:
    """
    Class representing the Fianco game logic.
    Handles the board state, move generation, move execution, and game rules.
    """

    def __init__(self):
        """
        Initialize the game board and state.
        """
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self._setup_board()
        self.current_player = 1  # 1 for White, 2 for Black
        self.move_count = 0
        self.move_history = []  # Stores tuples of (player, move_notation)
        self.captured_pieces = {1: 0, 2: 0}  # Number of pieces captured by each player
        self.ai_time = 0  # Total time AI has taken
        self.player_time = {1: 0, 2: 0}  # Time taken by each player

    def _setup_board(self):
        """
        Set up the initial board configuration.
        """
        # Place black pieces at the top
        self.board[0, :] = 2
        self.board[1, [1, 7]] = 2
        self.board[2, [2, 6]] = 2
        self.board[3, [3, 5]] = 2

        # Place white pieces at the bottom
        self.board[8, :] = 1
        self.board[7, [1, 7]] = 1
        self.board[6, [2, 6]] = 1
        self.board[5, [3, 5]] = 1

    def clone(self):
        """
        Create a deep copy of the game state.
        Useful for AI to simulate moves without altering the actual game.
        """
        clone_game = FiancoGame()
        clone_game.board = np.copy(self.board)
        clone_game.current_player = self.current_player
        clone_game.move_count = self.move_count
        clone_game.move_history = self.move_history.copy()
        clone_game.captured_pieces = self.captured_pieces.copy()
        return clone_game

    def get_possible_moves(self, player):
        """
        Generate all possible moves for the given player.
        Returns a list of moves in the form (start_i, start_j, end_i, end_j).
        """
        moves = []
        captures = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == player:
                    # Regular moves: sideways and forward
                    directions = [(0, -1), (0, 1)]  # Sideways
                    if player == 1:  # White moves up
                        directions.append((-1, 0))
                    else:  # Black moves down
                        directions.append((1, 0))

                    # Check for regular moves
                    for di, dj in directions:
                        new_i, new_j = i + di, j + dj
                        if (0 <= new_i < BOARD_SIZE and 0 <= new_j < BOARD_SIZE and
                                self.board[new_i][new_j] == 0):
                            moves.append((i, j, new_i, new_j))

                    # Check for captures (diagonal forward jumps)
                    capture_directions = [(-1, -1), (-1, 1)] if player == 1 else [(1, -1), (1, 1)]
                    for di, dj in capture_directions:
                        mid_i, mid_j = i + di, j + dj
                        end_i, end_j = i + 2 * di, j + 2 * dj
                        if (0 <= mid_i < BOARD_SIZE and 0 <= mid_j < BOARD_SIZE and
                                0 <= end_i < BOARD_SIZE and 0 <= end_j < BOARD_SIZE and
                                self.board[mid_i][mid_j] == 3 - player and
                                self.board[end_i][end_j] == 0):
                            captures.append((i, j, end_i, end_j))
        # Mandatory capture rule
        return captures if captures else moves

    def make_move(self, move, move_duration=0):
        """
        Apply a move to the board.
        Updates the board state and move history.
        """
        start_i, start_j, end_i, end_j = move
        player = self.current_player

        # Move the piece
        self.board[end_i][end_j] = self.board[start_i][start_j]
        self.board[start_i][start_j] = 0

        # Check for capture
        if abs(start_i - end_i) == 2:
            mid_i, mid_j = (start_i + end_i) // 2, (start_j + end_j) // 2
            captured_piece = self.board[mid_i][mid_j]
            self.board[mid_i][mid_j] = 0
            self.captured_pieces[player] += 1

        # Record the move with duration (store move coordinates)
        self.move_history.append((player, move, move_duration))

        # Update game state
        self.current_player = 3 - player  # Switch player
        self.move_count += 1

    def undo_move(self):
        """
        Undo the last move.
        Removes the last move from the move history and restores the previous board state.
        """
        if not self.move_history:
            print("No moves to undo.")
            return

        # Remove the last move
        last_player, last_move, move_duration = self.move_history.pop()
        self.current_player = last_player
        self.move_count -= 1

        # Reverse the move
        start_i, start_j, end_i, end_j = last_move
        self.board[start_i][start_j] = self.board[end_i][end_j]
        self.board[end_i][end_j] = 0

        # If it was a capture, restore the captured piece
        if abs(start_i - end_i) == 2:
            mid_i, mid_j = (start_i + end_i) // 2, (start_j + end_j) // 2
            self.board[mid_i][mid_j] = 3 - self.current_player  # Opponent's piece
            self.captured_pieces[self.current_player] -= 1

    def is_terminal(self):
        """
        Check if the game has reached a terminal state.
        Returns True if the game is over, False otherwise.
        """
        # Check for victory by reaching the opposite side
        if 1 in self.board[0, :]:
            return True
        if 2 in self.board[8, :]:
            return True

        # Check for victory by capturing all opponent's pieces
        if not np.any(self.board == 1):
            return True
        if not np.any(self.board == 2):
            return True

        # Check if current player has no valid moves
        if not self.get_possible_moves(self.current_player):
            return True

            # Check for three consecutive identical moves by the same player
            # Check for three consecutive identical moves by the same player
        if len(self.move_history) >= 6:
            last_player = 3 - self.current_player  # Player who just moved
            last_moves = [move for move in self.move_history if move[0] == last_player][-3:]
            if len(last_moves) == 3 and all(move[1] == last_moves[0][1] for move in last_moves):
                return True

        return False

    def get_winner(self):
        """
        Determine the winner of the game.
        Returns:
            - 1 if White wins
            - 2 if Black wins
            - None if no winner yet
        """
        if 1 in self.board[0, :]:
            return 1  # White wins
        if 2 in self.board[8, :]:
            return 2  # Black wins
        if not np.any(self.board == 1):
            return 2  # Black wins
        if not np.any(self.board == 2):
            return 1  # White wins

        # Check for repeated moves
        if len(self.move_history) >= 6:
            last_player = 3 - self.current_player  # Player who just moved
            last_moves = [move for move in self.move_history if move[0] == last_player][-3:]
            if len(last_moves) == 3 and all(move[1] == last_moves[0][1] for move in last_moves):
                return 3 - last_player  # Opponent wins

        # Check if current player has no moves
        if not self.get_possible_moves(self.current_player):
            return 3 - self.current_player  # Opponent wins

        # Check for repeated moves
        if len(self.move_history) >= 6:
            last_player = 3 - self.current_player  # Player who just moved
            last_moves = [move for move in self.move_history if move[0] == last_player][-3:]
            if len(last_moves) == 3 and all(move[1] == last_moves[0][1] for move in last_moves):
                return 3 - last_player  # Opponent wins
        return None  # No winner yet

    def validate_move(self, move):
        """
        Validate if a move is legal for the current player.
        """
        return move in self.get_possible_moves(self.current_player)

    def evaluate(self):
        winner = self.get_winner()
        if winner == self.current_player:
            return 10000
        elif winner == 3 - self.current_player:
            return -10000

        # Piece counts
        white_pieces = np.argwhere(self.board == 1)
        black_pieces = np.argwhere(self.board == 2)

        white_score = len(white_pieces)
        black_score = len(black_pieces)

        # Positional scores
        white_positional_score = 0
        black_positional_score = 0

        for pos in white_pieces:
            i, j = pos
            # Advancement bonus
            advancement = (8 - i) * 0.5
            # Central control bonus
            centrality = (4 - abs(4 - j)) * 0.3
            white_positional_score += advancement + centrality

        for pos in black_pieces:
            i, j = pos
            # Advancement bonus
            advancement = i * 0.5
            # Central control bonus
            centrality = (4 - abs(4 - j)) * 0.3
            black_positional_score += advancement + centrality

        # Mobility scores
        white_mobility = len(self.get_possible_moves(1))
        black_mobility = len(self.get_possible_moves(2))

        # Threats (pieces that can be captured)
        white_threats = self._count_threats(1)
        black_threats = self._count_threats(2)

        # Total evaluation
        score = (
                (white_score - black_score) * 10
                + (white_positional_score - black_positional_score)
                + (white_mobility - black_mobility) * 0.5
                - (white_threats - black_threats) * 5
        )

        return score if self.current_player == 1 else -score

    def _count_threats(self, player):
        """
        Count the number of player's pieces that can be captured in the next turn.
        """
        opponent = 3 - player
        threats = 0
        opponent_moves = self.get_possible_moves(opponent)
        for move in opponent_moves:
            if abs(move[0] - move[2]) == 2:
                # Check if the capture targets a player's piece
                mid_i, mid_j = (move[0] + move[2]) // 2, (move[1] + move[3]) // 2
                if self.board[mid_i][mid_j] == player:
                    threats += 1
        return threats