# ui.py

import pygame
import sys
from constants import BOARD_SIZE, SQUARE_SIZE, WIDTH, HEIGHT, WHITE, BLACK, LIGHT_BROWN, DARK_BROWN, GREEN, RED, FPS
from fianco_game import convert_move_to_notation
from fianco_game import FiancoGame

class GameUI:
    """
    Handles all Pygame UI elements, user interactions, and rendering.
    """

    def __init__(self, game, human_player, ai_player, ai_instance):
        """
        Initialize the UI with the game instance and player roles.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fianco")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_coords = pygame.font.SysFont('Arial', 14)
        self.font_moves = pygame.font.SysFont('Arial', 18)
        self.font_pieces = pygame.font.SysFont('Arial', 24)

        self.game = game
        self.human_player = human_player
        self.ai_player = ai_player
        self.ai_instance = ai_instance

        self.selected_piece = None
        self.valid_moves = []
        self.ai_thinking = False

        # Initialize player timers
        self.start_time = pygame.time.get_ticks()
        self.last_move_time = self.start_time
        self.move_duration = 0

    def run(self):
        """
        Main loop for the game UI.
        """
        running = True
        while running:
            self.clock.tick(FPS)
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.last_move_time) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game.current_player == self.human_player:
                        self.handle_mouse_click(event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        continue
                    if event.key == pygame.K_u:
                        # Undo move when 'U' key is pressed
                        self.game.undo_move()
                        self.game.player_time[self.game.current_player] -= self.move_duration
                        # If it's AI's turn after undo, undo again to go back to human's turn
                        if self.game.current_player == self.ai_player and self.game.move_history:
                            self.game.undo_move()
                            self.game.player_time[self.game.current_player] -= self.move_duration

            if self.game.is_terminal():
                winner = self.game.get_winner()
                self.display_game_over(winner)
                running = False
                continue

            if self.game.current_player == self.ai_player:
                if not self.ai_thinking:
                    self.ai_thinking = True
                    ai_move_start_time = pygame.time.get_ticks()
                    ai_move = self.ai_instance.get_move(self.game)
                    ai_move_end_time = pygame.time.get_ticks()
                    ai_move_duration = (ai_move_end_time - ai_move_start_time) / 1000.0
                    self.game.ai_time += ai_move_duration
                    self.game.player_time[self.ai_player] += ai_move_duration
                    self.game.make_move(ai_move, ai_move_duration)
                    self.last_move_time = ai_move_end_time
                    self.move_duration = ai_move_duration
                    self.ai_thinking = False
            else:
                # Update player's time
                self.move_duration = elapsed_time
                self.game.player_time[self.human_player] += (current_time - self.last_move_time) / 1000.0
                self.last_move_time = current_time

            self.draw_board()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def handle_mouse_click(self, position):
        """
        Handle mouse click events for selecting and moving pieces.
        """
        x, y = position
        if x < BOARD_SIZE * SQUARE_SIZE:
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            if self.selected_piece:
                move = (self.selected_piece[0], self.selected_piece[1], row, col)
                if self.game.validate_move(move):
                    # Calculate move duration
                    current_time = pygame.time.get_ticks()
                    move_duration = (current_time - self.last_move_time) / 1000.0
                    self.game.player_time[self.human_player] += move_duration
                    self.game.make_move(move, move_duration)
                    self.last_move_time = current_time
                    self.move_duration = move_duration
                    self.selected_piece = None
                    self.valid_moves = []
                else:
                    self.selected_piece = None
                    self.valid_moves = []
            elif self.game.board[row][col] == self.human_player:
                self.selected_piece = (row, col)
                possible_moves = self.game.get_possible_moves(self.human_player)
                self.valid_moves = [move for move in possible_moves if move[0] == row and move[1] == col]

    def draw_board(self):
        """
        Render the game board, pieces, highlights, move log, and captured pieces.
        """
        # Clear the screen
        self.screen.fill((245, 245, 220))  # Light beige background

        # Draw the board squares and pieces
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(self.screen, color, rect)

                # Highlight selected piece
                if self.selected_piece and self.selected_piece[0] == row and self.selected_piece[1] == col:
                    pygame.draw.rect(self.screen, GREEN, rect, 3)

                # Highlight valid moves
                for move in self.valid_moves:
                    if move[2] == row and move[3] == col:
                        pygame.draw.rect(self.screen, RED, rect, 3)

                # Draw pieces
                piece = self.game.board[row][col]
                if piece != 0:
                    center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    radius = SQUARE_SIZE // 2 - 10
                    piece_color = WHITE if piece == 1 else BLACK
                    pygame.draw.circle(self.screen, piece_color, center, radius)

                # Draw coordinate labels
                coord_label = chr(col + ord('A')) + str(9 - row)
                text_surface = self.font_coords.render(coord_label, True, BLACK)
                self.screen.blit(text_surface, (col * SQUARE_SIZE + 5, row * SQUARE_SIZE + SQUARE_SIZE - 18))

        # Draw move log background
        move_log_rect = pygame.Rect(BOARD_SIZE * SQUARE_SIZE, 0, WIDTH - BOARD_SIZE * SQUARE_SIZE, HEIGHT)
        pygame.draw.rect(self.screen, (220, 220, 220), move_log_rect)  # Light gray background for side panel

        # Render move history with move times
        move_log_start_x = BOARD_SIZE * SQUARE_SIZE + 10
        move_log_start_y = 10
        line_height = 20
        recent_moves = self.game.move_history[-20:]  # Show last 20 moves
        for idx, (player, move_coords, move_duration) in enumerate(recent_moves):
            move_notation = convert_move_to_notation(move_coords)
            move_time_text = f"({move_duration:.1f}s)"
            if player == self.ai_player:
                move_text = f"B: {move_notation} {move_time_text}"
                text_surface = self.font_moves.render(move_text, True, RED)
            else:
                move_text = f"W: {move_notation} {move_time_text}"
                text_surface = self.font_moves.render(move_text, True, BLACK)
            self.screen.blit(text_surface, (move_log_start_x, move_log_start_y + idx * line_height))

        # Display captured pieces (properly indented outside the loop)
        captured_pieces_start_y = move_log_start_y + len(recent_moves) * line_height + 30
        text_surface = self.font_pieces.render("Captured Pieces:", True, BLACK)
        self.screen.blit(text_surface, (move_log_start_x, captured_pieces_start_y))

        # Draw captured white pieces (captured by black)
        for i in range(self.game.captured_pieces[2]):
            center = (move_log_start_x + 20 + i * 25, captured_pieces_start_y + 40)
            pygame.draw.circle(self.screen, WHITE, center, 10)

        # Draw captured black pieces (captured by white)
        for i in range(self.game.captured_pieces[1]):
            center = (move_log_start_x + 20 + i * 25, captured_pieces_start_y + 80)
            pygame.draw.circle(self.screen, BLACK, center, 10)

        # Draw player timers at the bottom of the screen
        timer_start_y = HEIGHT - 40
        timer_background_rect = pygame.Rect(0, BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE, 50)
        pygame.draw.rect(self.screen, (200, 200, 200), timer_background_rect)  # Background for timers

        timer_text = f"Your Time: {self.game.player_time[self.human_player]:.1f}s"
        ai_timer_text = f"AI Time: {self.game.player_time[self.ai_player]:.1f}s"
        text_surface = self.font_pieces.render(timer_text, True, BLACK)
        self.screen.blit(text_surface, (10, timer_start_y))
        ai_text_surface = self.font_pieces.render(ai_timer_text, True, BLACK)
        self.screen.blit(ai_text_surface, (BOARD_SIZE * SQUARE_SIZE // 2, timer_start_y))

    def display_game_over(self, winner):
        """
        Display the game over screen with stats.
        """
        # Clear the screen
        self.screen.fill((0, 0, 0))
        # Display the game over message
        if winner == self.human_player:
            game_over_text = "You win!"
        elif winner == self.ai_player:
            game_over_text = "AI wins!"
        else:
            game_over_text = "Game over!"

        font_game_over = pygame.font.SysFont('Arial', 48)
        text_surface = font_game_over.render(game_over_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.screen.blit(text_surface, text_rect)

        # Display game stats
        stats_text = [
            f"Total Moves: {self.game.move_count}",
            f"Your Time: {self.game.player_time[self.human_player]:.1f}s",
            f"AI Time: {self.game.player_time[self.ai_player]:.1f}s"
        ]
        font_stats = pygame.font.SysFont('Arial', 24)
        for idx, line in enumerate(stats_text):
            text_surface = font_stats.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + idx * 30))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
        # Wait until the user closes the window or presses a key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            pygame.time.wait(100)