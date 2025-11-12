#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path

def main():
    nb = nbf.v4.new_notebook()
    cells = []
    cells.append(nbf.v4.new_markdown_cell(
        """
# Tutorial 2: Golden Ratio & Fibonacci Emergence
## From Recursion to φ = 1.618...

**Learning objectives:**
- Understand the golden ratio equation x² = x + 1
- See Fibonacci sequence convergence to φ
- Explore real-world examples (phyllotaxis, art, architecture)

**Prerequisites:** Tutorial 1 completed
**Duration:** 20 minutes
"""))
    cells.append(nbf.v4.new_markdown_cell(
        """
## The Golden Ratio φ

The golden ratio is the unique positive solution to:

x² = x + 1 → x = (1 ± √5)/2

Positive solution: φ = (1 + √5)/2 ≈ 1.618033988...

Special property: φ² = φ + 1 (it equals its own reciprocal plus 1)
"""))
    cells.append(nbf.v4.new_code_cell(
        r'''
import numpy as np
phi = (1 + np.sqrt(5)) / 2
print(f"φ = {phi:.15f}")
print(f"φ² = {phi**2:.15f}")
print(f"φ + 1 = {phi + 1:.15f}")
print(f"Difference: {abs(phi**2 - (phi + 1)):.2e}")
'''))
    cells.append(nbf.v4.new_markdown_cell(
        """
## Fibonacci Sequence

Defined recursively:
- F₀ = 0
- F₁ = 1
- Fₙ = Fₙ₋₁ + Fₙ₋₂ for n ≥ 2

Key result: Fₙ/Fₙ₋₁ → φ as n → ∞
"""))
    cells.append(nbf.v4.new_code_cell(
        r'''
import matplotlib.pyplot as plt

def fibonacci(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib

n_terms = 50
fib = fibonacci(n_terms)
ratios = [fib[i] / fib[i-1] for i in range(2, len(fib))]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

import numpy as np
n = np.arange(2, len(fib))
ax1.plot(n, ratios, 'b-o', markersize=4, label='Fₙ/Fₙ₋₁')
ax1.axhline(phi, color='r', linestyle='--', linewidth=2, label=f'φ = {phi:.6f}')
ax1.set_xlabel('n')
ax1.set_ylabel('Fₙ/Fₙ₋₁')
ax1.set_title('Fibonacci Ratios Converging to Golden Ratio')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim([1.5, 1.7])

errors = np.abs(np.array(ratios) - phi)
ax2.semilogy(n, errors, 'g-o', markersize=4)
ax2.set_xlabel('n')
ax2.set_ylabel('|Fₙ/Fₙ₋₁ - φ| (log scale)')
ax2.set_title('Error Decreases Exponentially')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fibonacci_convergence.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"F50/F49 = {fib[49]/fib[48]:.15f}")
print(f"φ       = {phi:.15f}")
print(f"Error   = {abs(fib[49]/fib[48] - phi):.2e}")
'''))
    cells.append(nbf.v4.new_markdown_cell(
        """
## Golden Ratio in Nature & Art

Validated examples (from literature):
1. Phyllotaxis (plant spirals): golden angle ~137.5°
2. Quasicrystals: five-fold symmetry
3. E8 Quantum Criticality: energy ratios ~φ (Coldea et al., 2010)

Removed claims (overstated):
- Not universal in all self-referential systems
- Not mandatory in neural networks
- Not a universal optimization constant
"""))
    cells.append(nbf.v4.new_markdown_cell(
        """
## Interactive: Golden Rectangle
A golden rectangle has sides in ratio φ:1.
When you remove a square, what remains is another golden rectangle!
"""))
    cells.append(nbf.v4.new_code_cell(
        r'''
fig, ax = plt.subplots(figsize=(10, 6))

def draw_golden_rectangle(ax, x, y, width, depth=0, max_depth=6):
    if depth > max_depth:
        return
    height = width / phi
    color = plt.cm.viridis(depth / max_depth)
    rect = plt.Rectangle((x, y), width, height, fill=False, edgecolor=color, linewidth=2)
    ax.add_patch(rect)
    square = plt.Rectangle((x, y), height, height, fill=True, facecolor=color, alpha=0.2)
    ax.add_patch(square)
    draw_golden_rectangle(ax, x + height, y, width - height, depth + 1, max_depth)

draw_golden_rectangle(ax, 0, 0, 10, depth=0, max_depth=6)
ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-0.5, 7)
ax.set_aspect('equal')
ax.set_title('Golden Rectangle Spiral', fontsize=14, fontweight='bold')
ax.axis('off')
plt.tight_layout()
plt.savefig('golden_rectangle.png', dpi=150, bbox_inches='tight')
plt.show()
'''))
    cells.append(nbf.v4.new_markdown_cell(
        """
## Exercise: Binet's Formula

Implement and verify: Fₙ = (φⁿ - ψⁿ)/√5 where ψ = (1 - √5)/2.
"""))
    nb['cells'] = cells
    out = Path('tutorials') / '02_golden_ratio_fibonacci.ipynb'
    out.parent.mkdir(exist_ok=True)
    nbf.write(nb, out)
    print('Wrote', out)

if __name__ == '__main__':
    main()
