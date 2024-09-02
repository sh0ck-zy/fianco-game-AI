# fianco_game.py

import numpy as np

class FiancoGame:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.board[0:2, :] = 2  # Black pieces
        self.board[7:9, :] = 1  # White pieces
        self.current_player = 1

    def get_possible_moves(self, player):
        moves = []
        captures = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == player:
                    # Check regular moves
                    for di, dj in [(1,0), (-1,0), (0,1), (0,-1)]:
                        if player == 1:
                            di = -di  # White moves upwards
                        if 0 <= i+di < 9 and 0 <= j+dj < 9 and self.board[i+di][j+dj] == 0:
                            moves.append((i, j, i+di, j+dj))
                    
                    # Check capture moves
                    for di, dj in [(2,2), (2,-2), (-2,2), (-2,-2)]:
                        if player == 1:
                            di = -di  # White moves upwards
                        if 0 <= i+di < 9 and 0 <= j+dj < 9 and self.board[i+di][j+dj] == 0:
                            if self.board[i+di//2][j+dj//2] == 3 - player:  # Opponent's piece
                                captures.append((i, j, i+di, j+dj))
        
        return captures if captures else moves

    def make_move(self, move):
        start_i, start_j, end_i, end_j = move
        self.board[end_i][end_j] = self.board[start_i][start_j]
        self.board[start_i][start_j] = 0
        if abs(start_i - end_i) == 2:  # Capture move
            self.board[(start_i + end_i) // 2][(start_j + end_j) // 2] = 0
        self.current_player = 3 - self.current_player

    def is_terminal(self):
        return 1 in self.board[0, :] or 2 in self.board[8, :]

    def evaluate(self):
        # Simple evaluation: difference in piece count and advancement
        white_score = np.sum(self.board == 1) + np.sum(8 - np.where(self.board == 1)[0])
        black_score = np.sum(self.board == 2) + np.sum(np.where(self.board == 2)[0])
        return white_score - black_score if self.current_player == 1 else black_score - white_score

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
    print(game.board)
    
    # Example: AI makes a move
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

    print(f"AI's chosen move: {best_move}")
    game.make_move(best_move)
    print("Board state after AI move:")
    print(game.board)

if __name__ == "__main__":
    main()
