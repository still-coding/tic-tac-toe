"""Game logic module."""

from dataclasses import dataclass
from enum import Enum
from random import randint


BOARD_SIZE = 3
Symbol = Enum("Symbol", ["E", "X", "O"])

board = None
player_symbol = None
ai_symbol = None

turn_num = 0


@dataclass
class Position:
    """Board position store and management for ease of use in game loop.
    """
    row: int = 0
    col: int = 0

    def up(self):
        self.row = self.row - 1 if self.row else 0

    def down(self):
        self.row = self.row + 1 if self.row < BOARD_SIZE - 1 else BOARD_SIZE - 1

    def left(self):
        self.col = self.col - 1 if self.col else 0

    def right(self):
        self.col = self.col + 1 if self.col < BOARD_SIZE - 1 else BOARD_SIZE - 1

    def linearize(self):
        return self.row * BOARD_SIZE + self.col


def new_game(selected_player_symbol=Symbol.X):
    """Empties the board and defaults necessary internal game variables.

    Args:
        selected_player_symbol (Symbol, optional): Symbol player selects in the beginning of the game. Defaults to Symbol.X.
    """
    global board, player_symbol, ai_symbol, turn_num
    board = [Symbol.E for _ in range(BOARD_SIZE * BOARD_SIZE)]
    turn_num = 0 if selected_player_symbol == Symbol.X else 1
    player_symbol = selected_player_symbol
    ai_symbol = Symbol.O if selected_player_symbol == Symbol.X else Symbol.X


def player_move(position):
    """Checks if player can mark ones position on the board.

    Args:
        position (Position): current player position

    Returns:
        bool: success of move
    """
    if board[position.linearize()] != Symbol.E:
        return False
    board[position.linearize()] = player_symbol
    return True


def ai_move():
    """Dumbest strategy - AI chooses first empty random position.
    """
    ai_pos = BOARD_SIZE * BOARD_SIZE // 2
    while board[ai_pos] != Symbol.E:
        ai_pos = randint(0, BOARD_SIZE * BOARD_SIZE - 1)
    board[ai_pos] = ai_symbol


def win_conditions():
    """Generates every win condition mask for the given board size.

    Yields:
        list of bool: win condition board mask
    """
    zeros = [False for _ in range(BOARD_SIZE)]
    ones = [True for _ in range(BOARD_SIZE)]
    for i in range(BOARD_SIZE):
        # lines
        yield zeros[:] * i + ones[:] + zeros[:] * (BOARD_SIZE - i - 1)
        # columns
        yield [j % BOARD_SIZE == i for j in range(BOARD_SIZE * BOARD_SIZE)]
    del zeros, ones
    # diagonals
    yield [i == j for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
    yield [
        i == BOARD_SIZE - j - 1 for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)
    ]


def we_have_a_winner():
    """Checks if there is a winner.
    Returns:
        Symbol or None: winner symbol if there is one, None otherwise.
    """
    for candidate in (Symbol.X, Symbol.O):
        for cond in win_conditions():
            if list(map(lambda x, y: x == candidate and y, board, cond)) == cond:
                return candidate
    if all([place != Symbol.E for place in board]):
        return Symbol.E
    return None
