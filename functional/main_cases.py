from typing import Optional, Tuple
from utils import pretty, random_solvable_scramble, is_solvable

Board = Tuple[int, ...]


def _parse_moves_input(s: str, default: int = 30) -> int:
    s = s.strip()
    if s == "":
        return default
    try:
        return int(s)
    except ValueError:
        return default


def _parse_custom_state_input(s: str) -> Optional[Board]:
    parts = s.strip().split()
    if len(parts) != 9:
        return None

    try:
        arr = tuple(int(x) for x in parts)
    except Exception:
        return None

    if set(arr) != set(range(9)):
        return None

    return arr


def case_1() -> Board:
    moves_raw = input("How many random moves? (default 30): ")
    moves = _parse_moves_input(moves_raw, default=30)
    start = random_solvable_scramble(moves)
    print("\nRandom solvable start generated:")
    print(pretty(start))
    return start


def case_2() -> Board:
    while True:
        print("\nEnter 9 numbers (0 = blank). Example: 1 2 3 4 5 6 7 8 0")
        s = input("State: ")
        parsed = _parse_custom_state_input(s)
        if parsed is None:
            print("Invalid format. Try again.")
            continue
        if not is_solvable(parsed):
            print("This state is NOT solvable. Try another.")
            continue
        print("Custom start accepted.")
        print(pretty(parsed))
        return parsed


def case_3() -> Board:
    start = (8, 6, 7, 2, 5, 4, 3, 0, 1)
    print("\nUsing classic hard start:")
    print(pretty(start))
    return start


main_cases = (case_1, case_2, case_3)
