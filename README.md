# 🧩 Sliding Tiles Concepts Project

A complete **8-Puzzle (Sliding Tiles)** implementation in **Python**,
designed to **compare Imperative and Pure Functional programming paradigms**,
with an **AI solver using A\* search and Manhattan distance heuristic**.

This project focuses on **problem-solving, search algorithms,
state representation, and software design styles**.

<br>

## 📌 Overview

The **8-puzzle** is a classic problem in Artificial Intelligence.
It consists of a `3 × 3` grid containing numbers `1–8` and one empty space (`0`).
The goal is to slide tiles until the board reaches the target configuration:

```bash
1 2 3
4 5 6
7 8 0
```

This repository contains **two full implementations**:

- **Imperative version** — traditional mutable control flow
- **Functional version** — strict functional style with immutable states

Both versions:

- Share the **same logic**
- Use **A\* search**
- Enforce **solvability rules**
- Support **random, custom, and hardcoded starts**

<br>

## 📂 Project Structure

```bash
Sliding-Tiles-Concepts-Project/
│
├── functional/
│   ├── app.py
│   ├── main.py
│   ├── main_cases.py
│   ├── sub_cases.py
│   ├── ui.py
│   └── utils.py
│
├── imperative/
│   ├── app.py
│   ├── main.py
│   ├── main_cases.py
│   ├── sub_cases.py
│   ├── ui.py
│   └── utils.py
│
└── README.md
```

<br>

## ⚙️ Requirements

- **Python 3.8+**
- No external libraries required (pure standard library)

<br>

## 🚀 How to Run

### Functional Version

```bash
cd functional
python app.py
```

<br>

### Imperative Version

```bash
cd imperative
python app.py
```

<br>

## 🧠 Core Concepts Implemented

### ✔ State Representation

- Board represented as an **immutable tuple of length 9**
- `0` represents the blank tile

```python
(1, 2, 3,
 4, 5, 6,
 7, 8, 0)
```

<br>

### ✔ Solvability Check

Uses **inversion count** (valid for 3×3 puzzles):

- Even number of inversions → **solvable**
- Odd number of inversions → **unsolvable**

```python
def is_solvable(state):
    return inversion_count(state) % 2 == 0
```

<br>

### ✔ Neighbor Generation

Generates all valid board states reachable by one move:

```python
(neighbor_state, "Up" | "Down" | "Left" | "Right")
```

<br>

### ✔ Manhattan Distance Heuristic

Used by A* search to estimate distance to the goal:

```python
h(n) = |x1 - x2| + |y1 - y2|
```

<br>

## 🤖 A\* Search Algorithm

Implemented from scratch using `heapq`.

### A* Returns

- Solution path (list of states)

- Explored states count

- Expansion count

- Runtime in seconds

```python
path, explored, expansions, runtime = a_star(start)
```

<br>

### Expansion Limit

To prevent infinite search:

```python
max_expansions = 500_000
```

<br>

## 🎮 User Interface Flow

### Main Menu

```bash
1) Random solvable scramble
2) Custom state input
3) Known hard start
4) Quit
```

<br>

### Sub Menu

```bash
1) Solve using AI (A*)
2) Show solvability & inversion count
3) Quit
```

<br>

## 🔁 Replay Mode

After solving, the user can replay the solution step-by-step:

```bash
Replay? (y or y <delay_seconds>)
```

Example:

```bash
y 0.5
```

<br>

## 🧪 Functional vs Imperative Design

### Functional Version

- Immutable board states

- Recursive logic

- No shared mutable state

- Emphasis on pure functions

Example:

```python
def derive_actions_recursive(idx, acc):
    ...
```

<br>

### Imperative Version

- Explicit loops

- Mutable variables

- Direct control flow

Example:

```python
for i in range(1, len(path)):
    ...
```

<br>

### 🧠 Educational Goals

This project demonstrates:

- Search algorithms (A*)

- Heuristic design

- State-space exploration

- Functional vs Imperative trade-offs

- Clean CLI program architecture
