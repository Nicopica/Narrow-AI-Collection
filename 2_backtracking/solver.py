# times_retracked = 0

def solve_sudoku(sudoku_game):
    # global times_retracked

    empty_spot = sudoku_game.coords_of_first_empty()

    if not empty_spot:  # solved
        # print(times_retracked)
        return sudoku_game

    row, col = empty_spot

    for number in range(1, 10):
        if (not sudoku_game.is_number_in_row(number, row) and
            not sudoku_game.is_number_in_column(number, col) and
            not sudoku_game.is_number_in_3x3(number, (row, col))):

            sudoku_game.numbers[row][col] = number
            sudoku_game.print_with_color((row, col), "\033[32m")

            # If false: backtracking
            if solve_sudoku(sudoku_game):
                return sudoku_game

            sudoku_game.numbers[row][col] = 0
            sudoku_game.print_with_color((row, col), "\033[31m")

    # times_retracked += 1
    return False