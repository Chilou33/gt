from typing import List, Tuple, Dict, Any
from main import Piece, create_pieces

def create_level(
    rows: int,
    columns: int,
    piece_numbers_available: List[int],
    placed_pieces: List[Tuple[int, List[Tuple[int, int]]]] = None,
    blocked_cells: List[Tuple[int, int]] = None
) -> Dict[str, Any]:
    """
    Create a Katamino level.
    - rows, columns: board dimensions
    - piece_numbers_available: list of available piece numbers
    - placed_pieces: list of tuples (piece_number, list of coordinates [(y, x), ...])
    - blocked_cells: list of coordinates (y, x) to block (optional)
    Returns a dict with the board, pieces, victory conditions, etc.
    """
    # Empty board
    board = [[0 for _ in range(columns)] for _ in range(rows)]
    # Block certain cells if requested
    if blocked_cells:
        for y, x in blocked_cells:
            board[y][x] = -1  # -1 = blocked cell

    # Create all pieces and keep only those requested
    all_pieces = create_pieces(board)
    available_pieces = [p for p in all_pieces if p.number in piece_numbers_available]

    # Place already placed pieces if needed
    already_placed_pieces = []
    if placed_pieces:
        for piece_number, coords in placed_pieces:
            for p in all_pieces:
                if p.number == piece_number:
                    p.actual_coordinates = [list(coord) for coord in coords]
                    for y, x in coords:
                        board[y][x] = piece_number
                    already_placed_pieces.append(p)
                    break

    def victory(board):
        """Victory condition: all non-blocked cells are filled."""
        for row in board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    level = {
        "board": board,
        "available_pieces": available_pieces,
        "already_placed_pieces": already_placed_pieces,
        "victory_condition": victory,
        "blocked_cells": blocked_cells or []
    }
    return level

# Example usage:
if __name__ == "__main__":
    # Génère les données du niveau
    level = create_level(
        4, 12,
        piece_numbers_available=[1,2,3,4,5],
        placed_pieces=[(1, [(0,5),(1,5),(2,5),(3,5),(0,6)])],
        blocked_cells=[(4,11)]
    )
    # Pour lancer le jeu graphique avec ce niveau :
 # Tu peux aussi adapter pour passer les pièces disponibles
from main import KataminoBoard
KataminoBoard(level["board"]) 