from typing import Optional
from ui import print_main_menu, print_sub_menu, print_start_message
from main_cases import main_cases
from sub_cases import cases as sub_cases


def _parse_int_choice(s: str) -> Optional[int]:
    s = s.strip()
    if s == "":
        return None
    try:
        return int(s)
    except ValueError:
        return None


def main() -> None:
    print_start_message()
    print_main_menu()
    raw = input()
    cmd = _parse_int_choice(raw)
    if cmd == 4:
        print("Goodbye.")
        return
    if cmd is None or not (1 <= cmd <= 3):
        print("Enter a valid number.")
        main()
    start = main_cases[cmd - 1]()

    solve_board(start)


def solve_board(start) -> None:
    print_sub_menu()
    raw = input()
    cmd = _parse_int_choice(raw)
    if cmd == 3:
        print("Goodbye.")
        return
    if cmd is None or not (1 <= cmd <= 2):
        print("Enter a valid number.")
        solve_board(start)
    sub_cases[cmd - 1](start)
