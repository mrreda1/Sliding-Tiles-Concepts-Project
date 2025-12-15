from typing import Tuple
from utils import neighbors, a_star, inversion_count, replay_path, pretty, is_solvable

Board = Tuple[int, ...]


def case_1(start: Board):
    print("\nRunning A* ...")

    path, explored, expansions, runtime = a_star(start)
    print(f"Explored: {explored}, Expansions: {
          expansions}, Time: {runtime:.3f}s")

    if path is None:
        print("No solution found.")
        return

    print(f"Solved! Moves: {len(path) - 1}.")

    def derive_actions_recursive(idx, acc):
        if idx >= len(path):
            return tuple(acc)

        prev = path[idx - 1]
        cur = path[idx]

        neighs = neighbors(prev)

        def find_action(i):
            if i >= len(neighs):
                return None

            n, a = neighs[i]
            if n == cur:
                return a

            return find_action(i + 1)

        action = find_action(0)
        return derive_actions_recursive(idx + 1, acc + (action,))

    if len(path) > 1:
        actions = derive_actions_recursive(1, ())
        print("Actions:", " -> ".join(actions))

    else:
        print("Already at goal.")

    ans = input("Replay? (y or y <delay seconds>): ").strip().lower()
    if ans.startswith("y"):
        parts = ans.split()
        try:
            delay = float(parts[1]) if len(parts) > 1 else 0.0
        except Exception:
            delay = 0.0
        replay_path(path, delay=delay)


def case_2(start: Board):
    print("\nStart state:\n" + pretty(start))
    print("Solvable:", is_solvable(start))
    print("Inversion count:", inversion_count(start))


cases = (case_1, case_2)
