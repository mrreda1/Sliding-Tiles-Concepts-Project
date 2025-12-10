#!/usr/bin/env python3

import heapq
import random
import time
from collections import deque

# --- Configuration ---
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # 0 is the blank
BOARD_SIZE = 3  # 3x3 puzzle

# --- Utility functions (imperative style) ---


def index_to_rc(i):
    return divmod(i, BOARD_SIZE)


def rc_to_index(r, c):
    return r * BOARD_SIZE + c


def pretty(state):
    """Return a string representation of the board state."""
    lines = []
    for r in range(BOARD_SIZE):
        row = []
        for c in range(BOARD_SIZE):
            v = state[r*BOARD_SIZE + c]
            row.append(str(v) if v != 0 else '.')
        lines.append(' '.join(row))
    return '\n'.join(lines)


def neighbors(state):
    """Return list of (neighbor_state, action_str) pairs."""
    i_blank = state.index(0)
    r, c = index_to_rc(i_blank)
    moves = []
    # Define moves as (dr, dc, action_name)
    for dr, dc, action in [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
            ni = rc_to_index(nr, nc)
            new_state = list(state)
            new_state[i_blank], new_state[ni] = new_state[ni], new_state[i_blank]
            moves.append((tuple(new_state), action))
    return moves


def manhattan(state, goal=GOAL):
    """Manhattan distance heuristic."""
    dist = 0
    for i, v in enumerate(state):
        if v == 0:
            continue
        goal_index = goal.index(v)
        r1, c1 = index_to_rc(i)
        r2, c2 = index_to_rc(goal_index)
        dist += abs(r1 - r2) + abs(c1 - c2)
    return dist


# --- Solvability utilities ---


def inversion_count(state):
    """Count inversions in the flattened state (ignore the blank)."""
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv


def is_solvable(state):
    """Check solvability for 3x3 puzzle: inversions must be even."""
    inv = inversion_count(state)
    return inv % 2 == 0


def random_solvable_scramble(moves=30):
    """Produce a random solvable state by performing random legal moves from goal."""
    state = list(GOAL)
    blank_pos = state.index(0)
    last_move = None
    for _ in range(moves):
        r, c = index_to_rc(blank_pos)
        possible = []
        for dr, dc, action in [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                ni = rc_to_index(nr, nc)
                # Avoid undoing the last move by action name (simple check)
                possible.append((ni, action))
        # pick random move
        ni, action = random.choice(possible)
        state[blank_pos], state[ni] = state[ni], state[blank_pos]
        blank_pos = ni
        last_move = action
    return tuple(state)

# --- A* Solver (imperative) ---


def a_star(start, goal=GOAL, heuristic=manhattan, max_expansions=500000):
    """
    A* search returning:
      path_states (list from start to goal) or None if not found,
      explored_count,
      expansions_count,
      runtime_seconds
    """
    start_time = time.time()
    if start == goal:
        return [start], 0, 0, 0.0

    open_heap = []
    # heap entries: (f_score, g_score, state)
    initial_h = heuristic(start, goal)
    heapq.heappush(open_heap, (initial_h, 0, start))

    came_from = {}   # state -> (parent_state, action)
    g_score = {start: 0}
    closed = set()
    expansions = 0

    while open_heap:
        _, g_current, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)

        if current == goal:
            # reconstruct path
            path = []
            s = current
            while s in came_from:
                parent, action = came_from[s]
                path.append((s, action))
                s = parent
            path.append((s, None))  # start
            path.reverse()
            states_path = [p for p, a in path]
            return states_path, len(closed), expansions, time.time() - start_time

        expansions += 1
        if expansions > max_expansions:
            return None, len(closed), expansions, time.time() - start_time

        for neigh, action in neighbors(current):
            tentative_g = g_score[current] + 1
            if neigh in g_score and tentative_g >= g_score[neigh]:
                continue
            came_from[neigh] = (current, action)
            g_score[neigh] = tentative_g
            f = tentative_g + heuristic(neigh, goal)
            heapq.heappush(open_heap, (f, tentative_g, neigh))

    return None, len(closed), expansions, time.time() - start_time

# --- Interactive / game loop (imperative) ---


def play_manual(state):
    """Allow the user to play the puzzle in the terminal (imperative)."""
    cur = list(state)
    while True:
        print("\nCurrent board:")
        print(pretty(tuple(cur)))
        if tuple(cur) == GOAL:
            print("Congratulations — you solved it!")
            break
        cmd = input(
            "Enter move (w/up, s/down, a/left, d/right), 'q' to quit: ").strip().lower()
        if not cmd:
            continue
        if cmd == 'q':
            print("Exiting play mode.")
            break
        # Map keys to actions
        key_action = {'w': 'Up', 'a': 'Left', 's': 'Down', 'd': 'Right',
                      'up': 'Up', 'down': 'Down', 'left': 'Left', 'right': 'Right'}
        action = key_action.get(cmd)
        if action is None:
            print("Invalid input. Use w/a/s/d or up/down/left/right.")
            continue
        # Try to perform the action if legal
        performed = False
        for neigh, act in neighbors(tuple(cur)):
            if act == action:
                cur = list(neigh)
                performed = True
                break
        if not performed:
            print("Move not legal.")


def replay_path(path_states, delay=0.0):
    """Print each state in path sequentially. delay in seconds between steps (0 for instant)."""
    for i, s in enumerate(path_states):
        print(f"\nStep {i}:\n{pretty(s)}")
        if delay > 0:
            time.sleep(delay)


def main():
    print("8-puzzle (imperative) — AI solver included.")
    # Choose initial configuration
    while True:
        print("\nOptions:")
        print(" 1) Use a random solvable scramble")
        print(" 2) Enter a custom state (9 numbers, 0 for blank)")
        print(" 3) Use a known 'hard' start")
        print(" 4) Quit")
        choice = input("Choose (1-4): ").strip()
        if choice == '1':
            moves = input(
                "How many random moves from goal? (recommended 10-50, default 30): ").strip()
            try:
                moves = int(moves) if moves else 30
            except:
                moves = 30
            start = random_solvable_scramble(moves)
            print("\nRandom solvable start generated.")
            print(pretty(start))
            break
        elif choice == '2':
            print(
                "Enter 9 numbers separated by spaces (0 represents blank). Example: 1 2 3 4 5 6 7 8 0")
            s = input("State: ").strip()
            parts = s.split()
            if len(parts) != 9:
                print("Please enter exactly 9 numbers.")
                continue
            try:
                arr = tuple(int(x) for x in parts)
            except:
                print("Invalid input — must be integers.")
                continue
            if set(arr) != set(range(9)):
                print("Numbers must be a permutation of 0..8.")
                continue
            if not is_solvable(arr):
                print("This state is NOT solvable. Try a different permutation.")
                continue
            start = arr
            print("Custom start accepted.")
            print(pretty(start))
            break
        elif choice == '3':
            # Classic hard starting position (a known difficult instance)
            start = (8, 6, 7, 2, 5, 4, 3, 0, 1)
            print("Using classic hard start:")
            print(pretty(start))
            break
        elif choice == '4':
            print("Goodbye.")
            return
        else:
            print("Invalid choice.")

    # Submenu: solve or play
    while True:
        print("\nWhat would you like to do now?")
        print(" 1) Let AI solve it (A* with Manhattan)")
        print(" 2) Show solvability / start over")
        print(" 3) Quit")
        cmd = input("Choose (1-3): ").strip()
        if cmd == '1':
            heuristic = manhattan
            print("\nRunning A* — this may take a little for very hard scrambles...")
            path, explored, expansions, runtime = a_star(
                start, GOAL, heuristic=heuristic)
            if path is None:
                print(f"No solution found within expansion limit. Explored: {
                      explored}, expansions: {expansions}, time: {runtime:.3f}s")
            else:
                print(f"Solved! Moves: {len(path)-1}, Explored states: {
                      explored}, Expansions: {expansions}, Time: {runtime:.3f}s")
                # Print action sequence (derive actions)
                actions = []
                for i in range(1, len(path)):
                    # find the action leading to state path[i] from path[i-1]
                    for neigh, action in neighbors(path[i-1]):
                        if neigh == path[i]:
                            actions.append(action)
                            break
                print("Actions:", ' -> '.join(actions))
                # Ask whether to replay
                ans = input(
                    "Replay solution step-by-step? (y/n, 'y' optionally with delay in seconds, e.g., y 0.5): ").strip().lower()
                if ans.startswith('y'):
                    parts = ans.split()
                    delay = float(parts[1]) if len(parts) > 1 else 0.0
                    replay_path(path, delay=delay)
        elif cmd == '2':
            print("\nStart state:\n" + pretty(start))
            print("Solvable:", is_solvable(start))
            print("Inversion count:", inversion_count(start))
        elif cmd == '3':
            print("Goodbye.")
            break
        else:
            print("Invalid input.")


if __name__ == "__main__":
    main()
