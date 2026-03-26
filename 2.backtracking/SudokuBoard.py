class SudokuBoard:
    def __init__(self, id_game, numbers):
        self.id_game = id_game
        self.numbers = numbers

    def _get_numbers_in_row(self, row):
        return self.numbers[int(row)]

    def _get_numbers_in_column(self, column):
        return [self.numbers[row][int(column)] for row in range(9)]

    def _get_numbers_in_3x3(self, coords):
        start_row = (coords[0] // 3) * 3
        start_col = (coords[1] // 3) * 3

        return [
            self.numbers[i][j]
            for i in range(start_row, start_row + 3)
            for j in range(start_col, start_col + 3)
        ]

    def is_number_in_row(self, number, row):
        return number in self._get_numbers_in_row(row)

    def is_number_in_column(self, number, column):
        return number in self._get_numbers_in_column(column)

    def is_number_in_3x3(self, number, coords):
        return number in self._get_numbers_in_3x3(coords)

    def coords_of_first_empty(self):
        for row in range(9):
            for col, num in enumerate(self._get_numbers_in_row(row)):
                if num == 0:
                    return row, col
        return False

    def __str__(self):
        text = f"ID Game: {self.id_game}\n"

        for i, row in enumerate(self.numbers):
            part1 = " ".join(map(str, row[0:3]))
            part2 = " ".join(map(str, row[3:6]))
            part3 = " ".join(map(str, row[6:9]))
            text += f"{part1} | {part2} | {part3}\n"
            if (i + 1) % 3 == 0 and i < 8:
                text += "----------------------\n"
        return text

    def print_with_color(self, coords, color):
        target_row, target_col = coords
        RESET = "\033[0m"
        text = ""

        for i, row_values in enumerate(self.numbers):
            formatted_row = []
            for j, num in enumerate(row_values):
                if i == target_row and j == target_col:
                    formatted_row.append(f"{color}{num}{RESET}")
                else:
                    formatted_row.append(str(num))

            part1 = " ".join(formatted_row[0:3])
            part2 = " ".join(formatted_row[3:6])
            part3 = " ".join(formatted_row[6:9])

            text += f"{part1} | {part2} | {part3}\n"

            if (i + 1) % 3 == 0 and i < 8:
                text += "----------------------\n"
        print(text)

def print_array_of_games(array_of_games):
    print(*(s for s in array_of_games), sep="\n")

