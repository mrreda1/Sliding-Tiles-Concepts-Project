from utils import neighbors
from utils import a_star
from utils import inversion_count
from utils import replay_path
from utils import pretty
from utils import is_solvable


def case_1(start):
    print("\nRunning A* — this may take a little for very hard scrambles...")
    path, explored, expansions, runtime = a_star(start)
    print(f" Explored: {explored}, Expansions: {
          expansions}, Time: {runtime:.3f}s")
    if path is None:
        print("No solution found within expansion limit.")
    else:
        print(f"Solved! Moves: {len(path)-1}.")

        actions = []
        for i in range(1, len(path)):
            for neigh, action in neighbors(path[i-1]):
                if neigh == path[i]:
                    actions.append(action)
                    break
        print("Actions:", ' -> '.join(actions))

        ans = input("Replay? (y or y <delay seconds>): ").strip().lower()
        if ans.startswith('y'):
            parts = ans.split()
            delay = float(parts[1]) if len(parts) > 1 else 0.0
            replay_path(path, delay=delay)


def case_2(start):
    print("\nStart state:\n" + pretty(start))
    print("Solvable:", is_solvable(start))
    print("Inversion count:", inversion_count(start))


cases = (case_1, case_2)
