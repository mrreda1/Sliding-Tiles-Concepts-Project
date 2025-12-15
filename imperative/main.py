from ui import print_main_menu
from ui import print_sub_menu
from ui import print_start_message
from main_cases import main_cases
from sub_cases import cases as sub_cases


def main():
    start = tuple()

    print_start_message()
    print_main_menu()

    try:
        cmd = int(input().strip())
        if cmd < 4 and cmd > 0:
            start = main_cases[cmd - 1]()
            solve_board(start)

        if cmd == 4:
            print("Goodbye.")
            return

        print("Invalid choice.")

    except:
        print("Enter a valid number.")

    main()


def solve_board(start):
    print_sub_menu()
    cmd = 0
    try:
        cmd = int(input().strip())
    except:
        print("Enter a valid number.")
        solve_board(start)

    if 1 <= cmd <= 2:
        sub_cases[cmd - 1](start)
    elif cmd == 3:
        print("Goodbye.")
    else:
        print("Invalid input.")
        solve_board(start)
