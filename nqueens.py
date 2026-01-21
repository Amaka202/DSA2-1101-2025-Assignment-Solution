# TASK ONE: n-queens problem

from __future__ import annotations

import random
import sys
from typing import List, Tuple, Optional

import matplotlib.pyplot as plt


# =========================
# Core helpers
# =========================

def positions_to_set(positions: List[List[int]]) -> set[tuple[int, int]]:
    return {(r, c) for r, c in positions}


def print_board_ascii(size: int, positions: List[List[int]], title: str = "") -> None:
    """
    Prints a chessboard-like view to the console.
    Q = queen, . = empty
    """
    if title:
        print(f"\n{title}")

    pos_set = positions_to_set(positions)
    for r in range(size):
        row_cells = []
        for c in range(size):
            row_cells.append("Q" if (r, c) in pos_set else ".")
        print(" ".join(row_cells))
    print()  # spacing


def visualize_board_matplotlib(size: int, positions: List[List[int]], title: str) -> None:
    """
    Matplotlib visualisation of the board.
    Uses a checkerboard pattern and overlays queens as 'Q'.
    """
    board = [[(r + c) % 2 for c in range(size)] for r in range(size)]

    fig, ax = plt.subplots()
    ax.imshow(board, interpolation="nearest")  # default colours are fine

    # draw queens
    for r, c in positions:
        ax.text(c, r, "Q", ha="center", va="center", fontsize=16)

    ax.set_title(title)
    ax.set_xticks(range(size))
    ax.set_yticks(range(size))
    ax.set_xlim(-0.5, size - 0.5)
    ax.set_ylim(size - 0.5, -0.5)
    plt.show()



def nQueensLasVegas(size: int) -> Tuple[bool, List[List[int]]]:
    """
    Las Vegas N-Queens:
    - Place queens row-by-row.
    - For each row, choose randomly among safe columns.
    - If a row has no safe columns, fail immediately.

    Returns:
      (success, positions)
      positions is a list of [row, col] for each placed queen (may be partial if fail).
    """
    if size < 1:
        return (False, [])

    positions: List[Tuple[int, int]] = []
    cols = set()
    diag1 = set()  # r - c
    diag2 = set()  # r + c

    for r in range(size):
        safe_cols = []
        for c in range(size):
            if c in cols:
                continue
            if (r - c) in diag1:
                continue
            if (r + c) in diag2:
                continue
            safe_cols.append(c)

        if not safe_cols:
            return (False, [[rr, cc] for rr, cc in positions])

        chosen_c = random.choice(safe_cols)
        positions.append((r, chosen_c))
        cols.add(chosen_c)
        diag1.add(r - chosen_c)
        diag2.add(r + chosen_c)

    return (True, [[r, c] for r, c in positions])


def nQueensBacktracking(size: int) -> Tuple[bool, List[List[int]]]:
    """
    Backtracking N-Queens:
    - Place queens row-by-row.
    - Try columns left-to-right.
    - Backtrack when no valid column exists for a row.

    Returns:
      (success, positions)
      positions is a list of [row, col] for each placed queen (full length if success).
    """
    if size < 1:
        return (False, [])
    if size in (2, 3):
        return (False, [])

    positions: List[Optional[Tuple[int, int]]] = [None] * size
    cols = set()
    diag1 = set()  # r - c
    diag2 = set()  # r + c

    def dfs(r: int) -> bool:
        if r == size:
            return True

        for c in range(size):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue

            positions[r] = (r, c)
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)

            if dfs(r + 1):
                return True

            # backtrack
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
            positions[r] = None

        return False

    success = dfs(0)
    final_positions = [[r, c] for (r, c) in positions if (r, c) is not None]
    return (success, final_positions)


def nQueensBacktrackingVersion2(size: int, startingPosition: Tuple[int, int]) -> Tuple[bool, List[List[int]]]:
    """
    Backtracking N-Queens with a user-defined starting queen position.
    The queen at startingPosition is fixed and must be included.

    startingPosition uses 0-based indexing: (row, col)

    Returns:
      (success, positions)
    """
    if size < 1:
        return (False, [])
    if size in (2, 3):
        return (False, [])
    r0, c0 = startingPosition
    if not (0 <= r0 < size and 0 <= c0 < size):
        return (False, [])

    positions: List[Optional[Tuple[int, int]]] = [None] * size

    cols = set()
    diag1 = set()
    diag2 = set()

    # Place the fixed queen
    positions[r0] = (r0, c0)
    cols.add(c0)
    diag1.add(r0 - c0)
    diag2.add(r0 + c0)

    def dfs(r: int) -> bool:
        if r == size:
            return True
        if r == r0:
            return dfs(r + 1)

        for c in range(size):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue

            positions[r] = (r, c)
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)

            if dfs(r + 1):
                return True

            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
            positions[r] = None

        return False

    success = dfs(0)
    final_positions = [[r, c] for (r, c) in positions if (r, c) is not None]
    return (success, final_positions)


def estimate_success_rates(size: int, runs: int = 10_000, seed: int = 42) -> dict[str, float]:
    """
    Returns success rates for:
      - backtracking (deterministic)
      - las_vegas (randomised)
    """
    random.seed(seed)

    bt_successes = 0
    lv_successes = 0

    for _ in range(runs):
        ok_bt, _ = nQueensBacktracking(size)
        ok_lv, _ = nQueensLasVegas(size)
        bt_successes += 1 if ok_bt else 0
        lv_successes += 1 if ok_lv else 0

    return {
        "backtracking": bt_successes / runs,
        "las_vegas": lv_successes / runs,
    }



def _read_line(prompt: str) -> str:
    return input(prompt).strip()


def _parse_int(s: str) -> Optional[int]:
    try:
        return int(s)
    except ValueError:
        return None


def _parse_starting_position(raw: str, size: int) -> Optional[Tuple[int, int]]:
    """
    Accepts formats like:
      "2 3"
      "2,3"
      "3, 4"
    Treats user input as 1-based indexing for friendliness, then converts to 0-based.
    """
    cleaned = raw.replace(",", " ")
    parts = [p for p in cleaned.split() if p]
    if len(parts) != 2:
        return None

    r = _parse_int(parts[0])
    c = _parse_int(parts[1])
    if r is None or c is None:
        return None

    # user enters 1..n, convert to 0..n-1
    r0, c0 = r - 1, c - 1
    if not (0 <= r0 < size and 0 <= c0 < size):
        return None

    return (r0, c0)


def run_program() -> None:
    """
    Runs the full required flow:
    - ask for size
    - ask for approach (Backtracking or Las Vegas)
    - show empty board
    - run algorithm
    - show final board regardless of success/failure
    """
    print("N-Queens Solver")
    print("Type 'exit' at any prompt to quit.\n")

    while True:
        raw_size = _read_line("Enter board size n (example: 8): ")
        if raw_size.lower() == "exit":
            print("Exiting.")
            return

        size = _parse_int(raw_size)
        if size is None or size < 1:
            print("Invalid input. Please enter a positive integer.\n")
            continue

        raw_mode = _read_line("Choose approach: backtracking / lasvegas: ")
        if raw_mode.lower() == "exit":
            print("Exiting.")
            return

        mode = raw_mode.strip().lower()
        if mode not in {"backtracking", "lasvegas"}:
            print("Invalid approach. Please type: backtracking or lasvegas.\n")
            continue

        # Show empty board
        print_board_ascii(size, [], title="Empty board:")

        # Run chosen solver
        success = False
        positions: List[List[int]] = []

        if mode == "lasvegas":
            success, positions = nQueensLasVegas(size)

        else:
            # Backtracking selected: ask if they want a fixed starting queen
            use_start = _read_line("Do you want to set a starting queen position? (y/n): ").strip().lower()
            if use_start == "exit":
                print("Exiting.")
                return

            if use_start in {"y", "yes"}:
                raw_pos = _read_line(
                    f"Enter starting queen position as row,col (1 to {size}), e.g. 1,1 or 3 4: "
                )
                if raw_pos.lower() == "exit":
                    print("Exiting.")
                    return

                starting = _parse_starting_position(raw_pos, size)
                if starting is None:
                    print("Invalid starting position format or out of range.\n")
                    continue

                success, positions = nQueensBacktrackingVersion2(size, starting)
            else:
                success, positions = nQueensBacktracking(size)

        # Final visualisation
        result_title = f"Final board (success={success}) with {len(positions)} queen(s) placed:"
        print_board_ascii(size, positions, title=result_title)

        raw_vis = _read_line("Show matplotlib visualisation? (y/n): ").strip().lower()
        if raw_vis == "exit":
            print("Exiting.")
            return
        if raw_vis in {"y", "yes"}:
            visualize_board_matplotlib(size, positions, title=result_title)

        raw_again = _read_line("Run again? (y/n): ").strip().lower()
        if raw_again == "exit":
            print("Exiting.")
            return
        if raw_again not in {"y", "yes"}:
            print("Goodbye.")
            return



if __name__ == "__main__":
    run_program()
