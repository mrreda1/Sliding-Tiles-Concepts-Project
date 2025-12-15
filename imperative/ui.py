def print_start_message():
    print("8-puzzle (imperative) — AI solver included.")


def print_main_menu():
    print("\nOptions:")
    print(" 1) Use a random solvable scramble")
    print(" 2) Enter a custom state (9 numbers, 0 for blank)")
    print(" 3) Use a known 'hard' start")
    print(" 4) Quit")
    print("Choose (1-4):", end=" ")


def print_sub_menu():
    print("\nWhat would you like to do now?")
    print(" 1) Let AI solve it (A* with Manhattan)")
    print(" 2) Show solvability / start over")
    print(" 3) Quit")
    print("Choose (1-3):", end=" ")
