# main.py

from fianco_game import FiancoGame
from ai import AIPlayer
from ui import GameUI

def main():
    """
    Main function to run the Fianco game.
    """
    # Prompt for human player color
    human_color_input = input("Choose your color (W/B): ").upper()
    while human_color_input not in ['W', 'B']:
        human_color_input = input("Invalid input. Choose your color (W/B): ").upper()
    human_player = 1 if human_color_input == 'W' else 2
    ai_player = 3 - human_player

    game = FiancoGame()
    ai_instance = AIPlayer(depth=3)  # Use 'depth' instead of 'max_depth'
    game_ui = GameUI(game, human_player, ai_player, ai_instance)
    game_ui.run()

if __name__ == "__main__":
    main()
