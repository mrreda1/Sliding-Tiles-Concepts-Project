from utils import pretty
from utils import random_solvable_scramble
from utils import is_solvable


def case_1():
    """ Random solvable start status"""

    moves = input(
        "How many random moves from goal?"
        " (recommended 10-50, default 30): ").strip()
    try:
        moves = int(moves) if moves else 30
    except:
        moves = 30
    start = random_solvable_scramble(moves)
    print("\nRandom solvable start generated.")
    print(pretty(start))
    return start


def case_2():
    """ Custom start status """

    while True:
        print("Enter 9 numbers separated by spaces (0 represents blank)."
              "Example: 1 2 3 4 5 6 7 8 0")
        s = input("State: ").strip()
        parts = s.split()
        if len(parts) != 9:
            print("Please enter exactly 9 numbers.")
            continue
        arr = tuple()
        try:
            arr = tuple(int(x) for x in parts)
        except:
            print("Invalid input — must be integers.")
        if set(arr) != set(range(9)):
            print("Numbers must be a permutation of 0..8.")
            continue
        if not is_solvable(arr):
            print("This state is NOT solvable."
                  "Try a different permutation.")
            continue
        start = arr
        print("Custom start accepted.")
        print(pretty(start))
        return start


def case_3():
    """ Classic hard starting position (a known difficult instance) """

    start = (8, 6, 7, 2, 5, 4, 3, 0, 1)
    print("Using classic hard start:")
    print(pretty(start))
    return start


main_cases = [case_1, case_2, case_3]
