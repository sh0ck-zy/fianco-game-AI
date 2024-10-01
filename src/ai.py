# ai.py

from fianco_game import FiancoGame
import sys
import time

def negamax(game, depth, alpha, beta, color):
    """
    Negamax algorithm with alpha-beta pruning.
    Recursively searches the game tree to determine the best move.
    """
    if depth == 0 or game.is_terminal():
        return color * game.evaluate()

    max_value = float('-inf')
    possible_moves = game.get_possible_moves(game.current_player)

    # Move ordering: prioritize captures
    possible_moves.sort(key=lambda move: self.move_sort_key(move, game.current_player), reverse=True)

    for move in possible_moves:
        game_copy = game.clone()
        game_copy.make_move(move)
        # Check for repeated move
        last_player = game_copy.current_player  # After the move, current_player has switched
        last_moves = [m for m in game_copy.move_history if m[0] == last_player][-3:]
        if len(last_moves) == 3 and all(m[1] == last_moves[0][1] for m in last_moves):
            continue  # Skip moves that would result in a loss due to repetition
        value = -negamax(game_copy, depth - 1, -beta, -alpha, -color)
        max_value = max(max_value, value)
        alpha = max(alpha, value)
        if alpha >= beta:
            break  # Alpha-beta cutoff
    return max_value

class AIPlayer:
    def __init__(self, depth=3, time_limit=5.0):
        self.depth = depth
        self.time_limit = time_limit
        self.start_time = None
        self.transposition_table = {}

    def get_move(self, game):
        """
        Determine the best move for the AI player.
        """
        self.current_player = game.current_player  # Set the current player
        self.start_time = time.time()
        self.transposition_table = {}
        best_move = None
        try:
            best_value = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            possible_moves = game.get_possible_moves(game.current_player)
            possible_moves.sort(key=self.move_sort_key, reverse=True)
            for move in possible_moves:
                game_copy = game.clone()
                game_copy.make_move(move)
                value = -self.negamax(game_copy, self.depth - 1, -beta, -alpha, -1)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_move
        except TimeoutError:
            return best_move  # Return the best move found so far

    def negamax(self, game, depth, alpha, beta, color):
        if time.time() - self.start_time > self.time_limit:
            raise TimeoutError
        # Generate a hashable key for the current game state
        board_key = self._generate_board_key(game.board, game.current_player)
        if board_key in self.transposition_table:
            return self.transposition_table[board_key]

        if depth == 0 or game.is_terminal():
            eval_score = color * game.evaluate()
            self.transposition_table[board_key] = eval_score
            return eval_score

        max_value = float('-inf')
        possible_moves = game.get_possible_moves(game.current_player)
        possible_moves.sort(key=self.move_sort_key, reverse=True)
        for move in possible_moves:
            game_copy = game.clone()
            game_copy.make_move(move)
            value = -self.negamax(game_copy, depth - 1, -beta, -alpha, -color)
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        self.transposition_table[board_key] = max_value
        return max_value

    def _generate_board_key(self, board, player):
        """
        Generate a hashable key representing the board state and current player.
        """
        return (tuple(map(tuple, board)), player)

    def move_sort_key(self, move):
        start_i, start_j, end_i, end_j = move
        is_capture = abs(start_i - end_i) == 2
        # Calculate advancement for both players
        if self.current_player == 1:
            advancement = start_i - end_i
        else:
            advancement = end_i - start_i
        return (is_capture, advancement)


