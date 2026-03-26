from Assignment2.SudokuBoard import SudokuBoard

SUDOKU_PATH="data/sudoku.txt"


def readData(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.readlines()

    except FileNotFoundError:
        exit(f"Error: The file '{path}' was not found.")

def get_sudoku_games():
    raw_data = readData(SUDOKU_PATH)
    data = [
        [int(char) for char in line.strip()]
        for line in raw_data
        if line.strip() and not line.startswith("SUDOKU")
    ]
    split_data = [data[i: i + 9] for i in range(0, len(data), 9)]
    return [SudokuBoard(i, game_rows) for i, game_rows in enumerate(split_data)]
