#!/usr/bin/env python3
"""
SR6: 2D site percolation (square lattice) estimation of critical threshold p_c.
Approach: simulate top-to-bottom percolation across a grid using BFS.
Outputs CSV with p vs percolation probability to ../data/sr6_percolation_data.csv
"""
from __future__ import annotations
import argparse
import csv
import random
from collections import deque
from pathlib import Path


def percolates(grid):
    n = len(grid)
    q = deque()
    seen = [[False] * n for _ in range(n)]
    # enqueue all open top-row cells
    for j in range(n):
        if grid[0][j]:
            q.append((0, j))
            seen[0][j] = True
    # BFS
    while q:
        i, j = q.popleft()
        if i == n - 1:
            return True
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and not seen[ni][nj] and grid[ni][nj]:
                seen[ni][nj] = True
                q.append((ni, nj))
    return False


def trial(n, p, rng):
    grid = [[rng.random() < p for _ in range(n)] for _ in range(n)]
    return percolates(grid)


def estimate(grid_size: int, trials: int, p_values, seed: int) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    results = []
    for p in p_values:
        hits = 0
        for _ in range(trials):
            if trial(grid_size, p, rng):
                hits += 1
        results.append((p, hits / trials))
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", type=int, default=60)
    ap.add_argument("--trials", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    # coarse p-grid near known threshold ~0.593
    pvals = [round(x, 3) for x in [0.50, 0.54, 0.56, 0.58, 0.59, 0.595, 0.60, 0.62, 0.64, 0.66]]
    data = estimate(args.grid, args.trials, pvals, args.seed)

    out_csv = Path(__file__).resolve().parents[1] / "data" / "sr6_percolation_data.csv"
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["p", "percolation_probability", "grid", "trials", "seed"])
        for p, prob in data:
            w.writerow([p, f"{prob:.4f}", args.grid, args.trials, args.seed])
    print(f"SR6 percolation sweep wrote {out_csv}")


if __name__ == "__main__":
    main()

