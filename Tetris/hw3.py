from typing import List, Tuple
from random import choice as choose


Block = List[Tuple[int, int]]
Pivot = Tuple[int, int]

BLOCK_I, BLOCK_J, BLOCK_L, BLOCK_S, BLOCK_Z, BLOCK_T, BLOCK_O = range(7)
LEFT, RIGHT, ROTATE_CW, ROTATE_CCW, DOWN, DROP, QUIT = range(7)

BLOCKS = [[(0, -1), (0, 0), (0, 1), (0, 2)],
          [(0, -1), (0, 0), (0, 1), (-1, 1)],
          [(0, -1), (0, 0), (0, 1), (1, 1)],
          [(0, 0), (1, 0), (0, 1), (1, 1)],
          [(-1, 0), (0, 0), (0, 1), (1, 1)],
          [(-1, 0), (0, 0), (0, 1), (1, 0)],
          [(0, 0), (1, 0), (0, 1), (1, 1)]]

WALL = "##"
SQUARE = "[]"
EMPTY = "  "

Arena = List[List[str]]


def coords(block_type: int) -> Block:
    return(BLOCKS[block_type])


def rotate_cw(arena: Arena, coords: Block, pivot: Pivot) -> Block:
    new_coords = []
    for x, y in coords:
        if not is_occupied(arena, pivot[1]-y, pivot[0]+x):
            new_coords.append((-y, x))
        else:
            return(coords)
    return(new_coords)


def rotate_ccw(arena: Arena, coords: Block, pivot: Pivot) -> Block:
    new_coords = []
    for x, y in coords:
        if not is_occupied(arena, pivot[1]+y, pivot[0]-x):
            new_coords.append((y, -x))
        else:
            return(coords)
    return(new_coords)


def new_arena(cols: int, rows: int) -> Arena:
    arena: Arena = []
    for i in range(rows):
        arena.append([])
        for j in range(cols):
            arena[i].append(EMPTY)
    return(arena)


def is_occupied(arena: Arena, x: int, y: int) -> bool:
    if x in range(len(arena)) and y in range(len(arena[0])):
        return(not arena[x][y] == EMPTY)
    else:
        return(False)


def set_occupied(arena: Arena, x: int, y: int, occupied: bool) -> None:
    arena[x][y] = SQUARE


def draw(arena: Arena, score: int, pivot, block) -> None:
    for i in range(len(arena)):
        print(WALL, end='')
        for j in range(len(arena[0])):
            if (j, i) in ((x+pivot[0], y+pivot[1]) for x, y in block):
                print(SQUARE, end='')
            else:
                print(arena[i][j], end='')
        print(WALL)
    print(WALL*(len(arena[0])+2))
    print('   Score: ', score)


def next_block() -> Block:
    # change this function as you wish
    return coords(choose(range(6)))


def left(pivot: Pivot):
    pass


def right(arena: Arena, block: Block, pivot: Pivot):
    pass


def down(arena: Arena, block: Block, pivot: Pivot):
    pass


def drop(arena: Arena, block: Block, pivot: Pivot):
    pass


def choice_hendler(arena: Arena, block: Block, pivot: Pivot,
                   choice: int) -> Tuple[bool, bool]:
    if choice == 0:
        left(arena, block, pivot)
    if choice == 1:
        right(arena, block, pivot)
    if choice == 2:
        block = rotate_cw(arena, block, pivot)
    if choice == 3:
        block = rotate_ccw(arena, block, pivot)
    if choice == 4:
        down(arena, block, pivot)
    if choice == 5:
        drop(arena, block, pivot)
    if choice == 6:
        return(False, False)
    return(True, True)


def poll_event() -> int:
    # change this function as you wish
    choice = int(input("Your choice: "))
    while choice not in range(7):
        choice = int(input("Your choice: "))
    return(choice)


def play(arena: Arena) -> int:
    game = True
    score = 0
    arena_width = len(arena[0])
    while game:
        active_block = next_block()
        if active_block[0][1] == -1:
            offset = 1
        else:
            offset = 0
        pivot = (arena_width//2, offset)
        block = True
        draw(arena, score, pivot, active_block)
        while block:
            block, game = choice_hendler(arena, active_block,
                                         pivot, poll_event())
            draw(arena, score, pivot, active_block)
    return(score)


def main() -> None:
    play(new_arena(7, 7))


if __name__ == '__main__':
    main()