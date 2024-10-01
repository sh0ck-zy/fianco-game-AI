# OVERVIEW: Building Fianco Game Engine:

## Board Representation:

- Use a 2D array (9x9) to represent the board.
- 0 for empty, 1 for white (bottom player), 2 for black (top player).


## Game State:

- Current board
- Current player turn
- Move history (optional, but useful for debugging)


## Move Generation:

- Implement functions for:
  - a) Regular moves (forward, left, right)
  - b) Capture moves (diagonal forward jumps)
  - *Ensure to check for and prioritize capture moves*


## Game Rules:

- Implement move validation
- Handle mandatory captures
- Check for win condition (piece reaching opposite side)


## Negamax with Alpha-Beta Pruning:

- Implement the core algorithm
- Use a depth limit to control search time


## Evaluation Function:

- Consider factors like:

  - Piece advancement towards goal
  - Control of flanks
  - Number of pieces
  - Mobility (number of possible moves)




## Testing and Validation:

- Create a simple text-based interface for playing against the AI
- Implement a way to input moves and display the board state
