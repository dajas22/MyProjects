from typing import List, Tuple, Optional

CLUES = List[Tuple[Tuple[int, int], Tuple[int, int]]]


class Clue:
    def __init__(self, total: int, position: Tuple[int, int],
                 is_row: bool, length: int):
        self.total = total
        self.position = position
        self.is_row = is_row
        self.length = length


class Kakuro:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.array = [[-1 for _ in range(width)] for _ in range(height)]
        self.clues: List[Clue] = []

    def set(self, x: int, y: int, value: int) -> None:
        self.array[y][x] = value

    def show_board(self) -> None:
        str_line = ""
        for line in self.array:
            for elem in line:
                if elem == -1:
                    str_line += '\\ '
                    continue
                str_line += (str(elem)+' ' if elem != 0 else '. ')
            print(str_line[:-1])
            str_line = ""

    def save(self, filename: str) -> None:
        line = ""
        with open(filename, "w") as write_file:
            for y, row in enumerate(self.array):
                for x, elem in enumerate(row):
                    if elem == -1:
                        clues = find_clues(self.clues, (x, y))
                        if clues == []:
                            line += ' \\ '
                        else:
                            str_1 = [' '+str(i.total) if not i.is_row
                                     else '  ' for i in clues]
                            str_2 = [str(i.total)+' ' if i.is_row
                                     else '  ' for i in clues]
                            line += str_1[0]+'\\'+str_2[-1]
                    elif elem == 0:
                        line += '  .  '
                    else:
                        line += ' '+str(elem)+' '
                print(line, file=write_file)
                line = ''

    def is_valid(self) -> bool:
        suma = 0
        for clue in self.clues:
            set_of_nums = set()
            pos = clue.position
            if clue.is_row:
                direction = (1, 0)
            else:
                direction = (0, 1)
            length = clue.length
            for _ in range(length):
                pos = add_tuple(pos, direction)
                x, y = pos
                num = self.array[y][x]
                suma += num
                if num in set_of_nums and num != 0:
                    return False
                else:
                    set_of_nums.add(num)
            if suma <= clue.total:
                suma = 0
                continue
            return False
        return True

    def pick_clue(self) -> Optional[Clue]:
        pass  # TODO

    def solve(self) -> bool:
        pass  # TODO


def find_clues(clue_list: List[Clue], position: Tuple[int, int]) -> List[Clue]:
    clues = []
    for clue in clue_list:
        if clue.position == position:
            clues.append(clue)
    return clues


def find_length(array: List[List[int]], position: Tuple[int, int],
                is_row: bool) -> int:
    length = 0
    if is_row:
        direction = (1, 0)
    else:
        direction = (0, 1)
    next_position = add_tuple(position, direction)
    while in_range_and_empty(next_position, array):
        length += 1
        next_position = add_tuple(next_position, direction)
    return length


def in_range_and_empty(position: Tuple[int, int],
                       array: List[List[int]]) -> bool:
    y, x = position
    return (x in range(len(array)) and
            y in range(len(array[0]))) and array[x][y] > -1


def add_tuple(tup1: Tuple[int, int], tup2: Tuple[int, int]) -> Tuple[int, int]:
    return (tup1[0] + tup2[0], tup1[1] + tup2[1])


def create_clues(line: str, row: int) -> CLUES:
    clues = []
    num = "0"
    colomn = 0
    down = 0
    new_line = ""
    for index in range(len(line)-1):
        if line[index] in " ." and line[index+1] in ' \n':
            continue
        new_line += line[index]
    line = new_line
    if line[0] == " ":
        line = line[1:]
    if line[-1] != ' ':
        line += " "
    for index in range(len(line)):
        letter = line[index]
        if letter == '\\':
            down = max(0, int(num))
            num = "0"
        elif (letter in "0123456789" and (line[index-1] in ' '
              and line[index+1] in '\n ')):
            continue
        elif letter in ' ':
            if not(down == 0 and num == '0'):
                clues.append(((down, max(0, int(num))), (colomn, row)))
            colomn += 1
            num = "0"
            down = 0
        else:
            num += letter
    return clues


def load_kakuro(filename: str) -> Kakuro:
    with open(filename) as unprocessed:
        field = []
        clues = []
        row = []
        line = unprocessed.readline()
        width = 0
        for letter in line:
            if letter in '\\\\.':
                width += 1
        height = 1
        while True:
            for index in range(len(line)-1):
                letter = line[index]
                if letter == '\\':
                    row.append(-1)
                elif letter == '.':
                    row.append(0)
                elif (letter in "0123456789" and (line[index-1] in ' '
                      and line[index+1] in '\n ')):
                    row.append(int(letter))
            field.append(row)
            row = list()
            clues.extend(create_clues(line, height-1))
            line = unprocessed.readline()
            if line == "":
                break
            height += 1
    clue_list = []
    for totals, coords in clues:
        is_row = False
        for total in totals:
            if total == 0:
                is_row = True
                continue
            clue_list.append(Clue(total, coords, is_row,
                             find_length(field, coords, is_row)))
            is_row = True
    kakuro = Kakuro(width, height)
    kakuro.array = field
    kakuro.clues = clue_list
    return kakuro


def cells_from_empty(total: int, length: int) -> List[List[int]]:
    pass


def cells_from_partial(total: int, partial: List[int]) -> List[List[int]]:
    pass  # TODO


# --- Tests ---

# Note: If there is a file with the following name in the current working
# directory, running these tests will overwrite that file!

TEST_FILENAME = "_ib111_tmp_file_"

EXAMPLE = ("\\   11\\  8\\     \\   \\   7\\ 16\\\n"
           "\\16   .   .   11\\   \\4   .   .\n"
           "\\7    .   .     .  7\\13  .   .\n"
           "\\   15\\ 21\\12   .   .    .   .\n"
           "\\12   .   .     .   .   4\\  6\\\n"
           "\\13   .   .     \\6  .    .   .\n"
           "\\17   .   .     \\   \\6   .   .\n")

TEST_FILENAME1 = 'sanity_example.txt'
TEST_FILENAME2 = 'sanity_example1.txt'
TEST_FILENAME3 = 'sanity_example2.txt'


def write_example(filename: str) -> None:
    with open(filename, "w") as file:
        file.write(EXAMPLE)


def example() -> Kakuro:
    write_example(TEST_FILENAME)
    return load_kakuro(TEST_FILENAME)


def test_1() -> None:
    kakuro = example()
    assert kakuro.width == 7
    assert kakuro.height == 7
    assert kakuro.array == [
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, 0, 0, -1, -1, 0, 0],
        [-1, 0, 0, 0, -1, 0, 0],
        [-1, -1, -1, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, -1, -1],
        [-1, 0, 0, -1, 0, 0, 0],
        [-1, 0, 0, -1, -1, 0, 0],
    ]

    clue_set = {(clue.total, clue.position, clue.is_row, clue.length)
                for clue in kakuro.clues}
    assert clue_set == {
        (11, (1, 0), False, 2),
        (8, (2, 0), False, 2),
        (7, (5, 0), False, 3),
        (16, (6, 0), False, 3),
        (16, (0, 1), True, 2),
        (11, (3, 1), False, 3),
        (4, (4, 1), True, 2),
        (7, (0, 2), True, 3),
        (7, (4, 2), False, 3),
        (13, (4, 2), True, 2),
        (15, (1, 3), False, 3),
        (21, (2, 3), False, 3),
        (12, (2, 3), True, 4),
        (12, (0, 4), True, 4),
        (4, (5, 4), False, 2),
        (6, (6, 4), False, 2),
        (13, (0, 5), True, 2),
        (6, (3, 5), True, 3),
        (17, (0, 6), True, 2),
        (6, (4, 6), True, 2),
    }


def test_2() -> None:
    kakuro = example()

    print("show_board result:")
    kakuro.show_board()
    print("---")

    print("save result:")
    kakuro.save(TEST_FILENAME)
    with open(TEST_FILENAME) as file:
        print(file.read(), end="")
    print("---")


def test_3() -> None:
    kakuro = example()
    assert kakuro.is_valid()

    kakuro.set(2, 1, 9)
    assert not kakuro.is_valid()

    kakuro.set(2, 1, 0)
    assert kakuro.is_valid()

    kakuro.set(1, 2, 1)
    kakuro.set(2, 2, 1)
    assert not kakuro.is_valid()

    kakuro.set(1, 2, 0)
    kakuro.set(2, 2, 0)
    assert kakuro.is_valid()

    kakuro.set(5, 5, 4)
    assert kakuro.is_valid()


def test_4() -> None:
    assert cells_from_empty(13, 2) \
        == [[4, 9], [5, 8], [6, 7], [7, 6], [8, 5], [9, 4]]

    assert cells_from_partial(12, [0, 0, 6, 0]) \
        == [[1, 2, 6, 3], [1, 3, 6, 2], [2, 1, 6, 3],
            [2, 3, 6, 1], [3, 1, 6, 2], [3, 2, 6, 1]]


def test_5() -> None:
    kakuro = example()
    clue = kakuro.pick_clue()

    assert clue is not None
    assert clue.total == 16
    assert clue.position == (0, 1)
    assert clue.is_row
    assert clue.length == 2

    kakuro.set(6, 5, 1)
    clue = kakuro.pick_clue()

    assert clue is not None
    assert clue.total == 6
    assert clue.position == (6, 4)
    assert not clue.is_row
    assert clue.length == 2

    kakuro.set(6, 6, 5)
    clue = kakuro.pick_clue()

    assert clue is not None
    assert clue.total == 6
    assert clue.position == (4, 6)
    assert clue.is_row
    assert clue.length == 2


def test_6() -> None:
    kakuro = example()
    kakuro.solve()
    assert kakuro.array == [
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, 9, 7, -1, -1, 1, 3],
        [-1, 2, 1, 4, -1, 4, 9],
        [-1, -1, -1, 5, 1, 2, 4],
        [-1, 1, 5, 2, 4, -1, -1],
        [-1, 6, 7, -1, 2, 3, 1],
        [-1, 8, 9, -1, -1, 1, 5],
    ]


def my_test() -> None:
    kakuro = load_kakuro(TEST_FILENAME3)
    kakuro = load_kakuro(TEST_FILENAME1)
    kakuro = load_kakuro(TEST_FILENAME2)
    for i in kakuro.clues:
        print(i.is_row, i.length, i.position, i.total)


if __name__ == '__main__':
    my_test()
    test_1()
    # uncomment to visually check the results:
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
