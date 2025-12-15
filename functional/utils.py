import heapq
import random
import time

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
BOARD_SIZE = 3


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
    # last_move = None
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
        # last_move = action
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


def replay_path(path_states, delay=0.0):
    """Print each state in path sequentially.
    delay in seconds between steps (0 for instant)."""

    for i, s in enumerate(path_states):
        print(f"\nStep {i}:\n{pretty(s)}")
        if delay > 0:
            time.sleep(delay)
