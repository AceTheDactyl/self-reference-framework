#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path

def main():
    nb = nbf.v4.new_notebook()
    cells = []
    cells.append(nbf.v4.new_markdown_cell("""
# Tutorial 3: Phase Transitions (Interactive)

Visualize percolation threshold and (placeholder) Kuramoto synchronization.
"""))
    cells.append(nbf.v4.new_code_cell(
        r'''
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import random


def percolates(grid):
    n = len(grid)
    q = deque()
    seen = [[False] * n for _ in range(n)]
    for j in range(n):
        if grid[0][j]:
            q.append((0, j))
            seen[0][j] = True
    while q:
        i, j = q.popleft()
        if i == n - 1:
            return True
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            ni, nj = i+di, j+dj
            if 0 <= ni < n and 0 <= nj < n and not seen[ni][nj] and grid[ni][nj]:
                seen[ni][nj] = True
                q.append((ni, nj))
    return False


def sweep(n=50, trials=30, pvals=None, seed=0):
    rng = random.Random(seed)
    if pvals is None:
        pvals = np.linspace(0.5, 0.66, 12)
    probs = []
    for p in pvals:
        hits = 0
        for _ in range(trials):
            grid = [[rng.random() < p for _ in range(n)] for _ in range(n)]
            hits += percolates(grid)
        probs.append(hits / trials)
    return np.array(pvals), np.array(probs)

p, prob = sweep(n=50, trials=25, seed=1)
fig, ax = plt.subplots(figsize=(6,4))
ax.plot(p, prob, 'o-', label='Percolation probability')
ax.axvline(0.593, color='r', linestyle='--', label='~0.593')
ax.set_xlabel('p (site open probability)')
ax.set_ylabel('Percolates (fraction)')
ax.set_title('2D Site Percolation Threshold (Estimate)')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig('percolation_threshold.png', dpi=150, bbox_inches='tight')
plt.show()
'''))
    cells.append(nbf.v4.new_markdown_cell("""
## Kuramoto Synchronization (Placeholder)

Interactive Kuramoto demo to be added in a future version.
"""))
    nb['cells'] = cells
    out = Path('tutorials') / '03_phase_transitions_interactive.ipynb'
    out.parent.mkdir(exist_ok=True)
    nbf.write(nb, out)
    print('Wrote', out)

if __name__ == '__main__':
    main()
