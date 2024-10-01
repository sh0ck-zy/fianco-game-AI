# Understanding the Components

## 1. FiancoGame Class:
**Purpose:** Manages the game state, enforces rules, and provides methods for game actions.

### Key Methods:
- `__init__`: Initializes the game.
- `_setup_board`: Sets up the starting positions.
- `get_possible_moves`: Generates legal moves.
- `make_move`: Executes a move.
- `undo_move`: Reverses the last move.
- `is_terminal`: Checks if the game is over.
- `get_winner`: Determines the winner.
- `evaluate`: Evaluates the board state for the AI.

## 2. AIPlayer Class (in `ai.py`):
**Purpose:** Encapsulates AI behavior and move selection.

### Key Methods:
- `__init__`: Initializes the AI with a search depth.
- `get_move`: Determines the best move using negamax.

## 3. GameUI Class (in `ui.py`):
**Purpose:** Handles rendering and user interaction.

### Key Methods:
- `__init__`: Initializes Pygame and UI elements.
- `run`: Main loop that processes events and updates the display.
- `handle_mouse_click`: Processes user clicks for moving pieces.
- `draw_board`: Renders the board and UI components.

## 4. `main.py`:
**Purpose:** Entry point of the program.

### Key Actions:
- Prompts the user for their chosen color.
- Initializes the game, AI, and UI.
- Starts the game loop.

# Analyzing What We Have vs. What's Needed for a Powerful AI

## Current Capabilities:
- **Basic AI:** Uses the negamax algorithm with alpha-beta pruning.
- **Heuristics:** Simple evaluation function considering piece count and advancement.
- **Fixed Depth:** AI searches to a fixed depth (e.g., 3).

## Improvements Needed:

### Enhanced Evaluation Function:
- **Add More Heuristics:**
  - Piece mobility.
  - Control of key areas (flanks).
  - Piece safety (avoidance of being captured).
- **Dynamic Evaluation:**
  - Adjust weights based on the game phase (opening, middle, endgame).

### Search Algorithm Enhancements:
- **Iterative Deepening:**
  - Allows deeper searches within time constraints.
- **Transposition Tables:**
  - Cache previously evaluated positions to avoid redundant calculations.
- **Quiescence Search:**
  - Extend search in volatile positions to avoid the horizon effect.

### Move Ordering Improvements:
- **History Heuristics:**
  - Prioritize moves that have been good in previous searches.
- **Killer Moves:**
  - Keep track of moves that cause alpha-beta cutoffs.

### Time Management:
- Implement time controls to ensure the AI makes decisions promptly.

### Opening Book:
- Predefined set of strong opening moves to guide early game play.

### Endgame Databases:
- Precomputed optimal plays for endgame scenarios with few pieces.

### Parallel Processing (Optional):
- Utilize multiple cores to search different branches simultaneously.

---

## By Implementing These Improvements:
- The AI will make stronger, more strategic decisions.
- It will be better equipped to handle complex situations.
- Overall performance will increase, making it more competitive in a tournament.
