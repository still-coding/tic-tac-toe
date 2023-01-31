#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""UI and main loop module"""

from time import sleep

from curtsies import FSArray, FullscreenWindow, Input, fsarray
from curtsies.fmtfuncs import blue, bold, green, on_blue, on_red, red

import game


SYMBOL_MAPPING = {game.Symbol.E: "-", game.Symbol.X: "X", game.Symbol.O: "O"}

player_pos = game.Position()


def get_board_image(board, blue=True):
    """Returns the board image for a given board state.

    Args:
        board (list of Symbols): current board state.
        blue (bool, optional): "Cursor" background. Can be blue or red. Defaults to True.

    Returns:
        list of FmtStr: list for convert to fsarray and print on screen.
    """
    lines = []
    for i in range(game.BOARD_SIZE):
        raw_line = board[i * game.BOARD_SIZE : i * game.BOARD_SIZE + game.BOARD_SIZE]
        str_line = ""
        for j, sym in enumerate(raw_line):
            if player_pos.row == i and player_pos.col == j:
                str_line += (
                    on_blue(SYMBOL_MAPPING[sym])
                    if blue
                    else on_red(SYMBOL_MAPPING[sym])
                )
            else:
                str_line += SYMBOL_MAPPING[sym]
            str_line += " "
        lines.append(str_line)
    return lines


def game_over_message(winner):
    """Gives game over message (win, lose or draw).

    Args:
        winner (Symbol): Winner symbol

    Returns:
        FmtStr: Colored game over message
    """
    if winner == game.player_symbol:
        return green("You have vanquished your foe! Congratulations!")
    if winner == game.ai_symbol:
        return red("You have been defeated by AI! Good luck next time!")
    return blue("It's a draw! Not bad!")


def main():
    """Main game loop and UI draw logic. Very bloated. -_-
    """
    with FullscreenWindow() as window:
        with Input() as input_generator:
            greeting = [
                bold(blue("Welcome to tic-tac-toe game!")),
                "Game starts with Xs turn.",
                f"Press {bold('any key')} to play with Xs or {bold('[O] key')} to play with Os.",
            ]
            window.render_to_terminal(fsarray(greeting))
            for c in input_generator:
                if c in "oO":
                    select = game.Symbol.O
                else:
                    select = game.Symbol.X
                break
            game.new_game(select)
            controls = [
                f"You: {SYMBOL_MAPPING[game.player_symbol]}",
                f"AI: {SYMBOL_MAPPING[game.ai_symbol]}",
                "Controls:",
                f'> {bold("Arrow keys")} to move',
                f'> {bold("[Space]")} to put {SYMBOL_MAPPING[game.player_symbol]}',
                f'> {bold("[Esc]")} to exit game',
                "",
            ]
            if game.turn_num % 2:
                game.ai_move()
                game.turn_num += 1
            window.render_to_terminal(fsarray(controls + get_board_image(game.board)))
            winner = None
            for c in input_generator:
                player_select_success = True
                if c == "<ESC>":
                    break
                if c == "<RIGHT>":
                    player_pos.right()
                if c == "<LEFT>":
                    player_pos.left()
                if c == "<UP>":
                    player_pos.up()
                if c == "<DOWN>":
                    player_pos.down()
                if c == "<SPACE>":
                    player_select_success = game.player_move(player_pos)
                    if player_select_success:
                        game.turn_num += 1
                    if winner := game.we_have_a_winner():
                        window.render_to_terminal(
                            controls
                            + get_board_image(game.board, player_select_success)
                            + [bold(game_over_message(winner))]
                        )
                        break

                if game.turn_num % 2:
                    game.ai_move()
                    game.turn_num += 1
                if winner := game.we_have_a_winner():
                    window.render_to_terminal(
                        controls
                        + get_board_image(game.board)
                        + [bold(game_over_message(winner))]
                    )
                    break
                window.render_to_terminal(controls + get_board_image(game.board, player_select_success))

            if winner:
                for c in input_generator:
                    if c == "<ESC>":
                        break


if __name__ == "__main__":
    main()
