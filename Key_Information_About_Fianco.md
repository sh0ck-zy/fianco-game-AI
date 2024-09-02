# Key Information Needed for Fianco Game AI

## Board Representation
- 9x9 grid
- Piece representation for each player

## Move Generation
- Regular moves: left, right, or forward to adjacent empty squares
- Capture moves: diagonal forward jumps over opponent pieces

## Game State Evaluation
- Progress towards the opposite side of the board
- Control of flanks
- Piece count

## Terminal State Detection
- Check if any player has reached the opposite side

## Turn Management
- Handling mandatory captures
