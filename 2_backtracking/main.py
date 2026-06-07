from Task2_backtracking.solver import solve_sudoku
from Task2_backtracking.utils import get_sudoku_games


def main():
    # solve_sudoku(get_sudoku_games()[0])
    print(*(solve_sudoku(s) for s in get_sudoku_games()), sep="\n")


if __name__ == '__main__':
    main()
