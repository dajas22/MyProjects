from random import choice


INVALID_POSITION = 0
EMPTY_POSITION = 1
ROUND_OVER = 2
PLAY_AGAIN = 3


def init(size, start):
    return(([start]*size) + [0], ([start]*size) + [0])


def gamecycle(our, their, position):
    state = ROUND_OVER
    # tuple(player field, length of player field with/without bank
    # is player on turn if yes then 1)
    active_field = (our, len(our)-1, 1)
    other_field = (their, len(our)-2, 0)
    # takes balls from chosen position
    steps, our[position] = our[position], 0
    pointer = position

    while steps != 0:
        # if true switches fields and set poiter to 0
        if pointer == active_field[1]:
            active_field, other_field = other_field, active_field
            pointer = 0

        else:
            pointer += 1

        active_field[0][pointer] += 1
        steps -= 1
    # if last ball drops into the field owned by current player
    if active_field[2] == 1:
        # if it drops in the bank
        if pointer == len(our)-1:
            state = PLAY_AGAIN
        # if it drops in an empty spot and their spor is not empty
        elif (our[pointer] == 1 and
                their[abs(pointer-(len(our)-2))] != 0):
            # takes their and our ball and put in our bank
            our[len(our)-1] += our[pointer] + their[abs(pointer-(len(our)-2))]
            our[pointer], their[abs(pointer-(len(our)-2))] = 0, 0

    return(state)


def play(our, their, position):
    if position in range(len(our)-1):
        if our[position] != 0:
            return(gamecycle(our, their, position))

        else:
            return(EMPTY_POSITION)

    else:
        return(INVALID_POSITION)


def random_choice(our):
    random = []

    for i, value in enumerate(our[:len(our)-1]):
        # adds index of not empty element
        if value != 0:
            random.append(i)

    if random == []:
        return(None)

    return(choice(random))


def run_random_game(size, start):
    our_score = 0
    their_score = 0
    our, their = init(size, start)
    active_player = our
    other_player = their

    while True:
        choice = random_choice(active_player)
        # there is no more move if choice is None
        if choice is None:
            # ends the game
            break
        # calculates 1 round
        round = play(active_player, other_player, choice)
        # 2 == current player ends turn
        if round == 2:
            active_player, other_player = other_player, active_player
        # 3 == current player plays again
        elif round == 3:
            continue
    # counts points
    for i in their:
        their_score += i
    for i in our:
        our_score += i

    return(our_score, their_score)


def main():
    # --- init ---

    assert init(6, 3) \
        == ([3, 3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 3, 0])

    assert init(9, 7) \
        == ([7, 7, 7, 7, 7, 7, 7, 7, 7, 0], [7, 7, 7, 7, 7, 7, 7, 7, 7, 0])

    # --- play ---

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, -1) == INVALID_POSITION
    assert our == [3, 0, 6, 0]
    assert their == [3, 3, 3, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 0) == PLAY_AGAIN
    assert our == [0, 1, 7, 1]
    assert their == [3, 3, 3, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 1) == EMPTY_POSITION
    assert our == [3, 0, 6, 0]
    assert their == [3, 3, 3, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 2) == ROUND_OVER
    assert our == [4, 0, 0, 6]
    assert their == [4, 0, 4, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 3) == INVALID_POSITION
    assert our == [3, 0, 6, 0]
    assert their == [3, 3, 3, 0]

    # --- random_choice ---

    assert random_choice([1, 2, 3, 4, 0]) in [0, 1, 2, 3]

    assert random_choice([3, 3, 0, 3, 3, 7]) in [0, 1, 3, 4]

    assert random_choice([0, 0, 0, 1]) is None

    print(run_random_game(6, 3))


if __name__ == '__main__':
    main()
