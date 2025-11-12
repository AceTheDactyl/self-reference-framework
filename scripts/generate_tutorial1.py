#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path

def main():
    nb = nbf.v4.new_notebook()
    cells = []
    cells.append(nbf.v4.new_markdown_cell(
        """
# Tutorial 1: Introduction to Self-Reference
## From Fixed Points to the 33-Theorem Framework

**Learning objectives:**
- Understand what self-reference means mathematically
- See examples of fixed-point theorems
- Connect to the corrected framework

**Prerequisites:** Basic Python, high school math
**Duration:** 20 minutes
"""))
    cells.append(nbf.v4.new_markdown_cell(
        """
## What is Self-Reference?

Self-reference occurs when a system refers to or depends on itself.

**Mathematical examples:**
- Fixed points: x = f(x)
- Recursive functions: factorial(n) = n × factorial(n-1)
- Self-consistent equations: μ = T(μ)

**Physical examples:**
- Mirrors facing mirrors
- Feedback loops in control systems
- Observer effects in quantum mechanics
"""))
    cells.append(nbf.v4.new_code_cell(
        r'''
import numpy as np
import matplotlib.pyplot as plt


def find_fixed_point(f, x0=1.0, tol=1e-10, max_iter=100):
    """
    Find fixed point of function f where f(x*) = x*.
    """
    x = x0
    history = [x]
    for i in range(max_iter):
        x_new = f(x)
        history.append(x_new)
        if abs(x_new - x) < tol:
            return x_new, np.array(history)
        x = x_new
    raise RuntimeError("Did not converge")

# Example: f(x) = cos(x)
f = lambda x: np.cos(x)

x_star, history = find_fixed_point(f, x0=1.0)

print(f"Fixed point: x* = {x_star:.10f}")
print(f"Verification: f(x*) = {f(x_star):.10f}")
print(f"Iterations: {len(history)-1}")
'''))
    cells.append(nbf.v4.new_code_cell(
        r'''
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Plot 1: Cobweb diagram
x = np.linspace(0, 1, 1000)
ax1.plot(x, np.cos(x), 'b-', label='f(x) = cos(x)', linewidth=2)
ax1.plot(x, x, 'k--', label='y = x', alpha=0.5)

# Draw cobweb
for i in range(min(10, len(history)-1)):
    x_curr, x_next = history[i], history[i+1]
    ax1.plot([x_curr, x_curr], [x_curr, x_next], 'r-', alpha=0.5)
    ax1.plot([x_curr, x_next], [x_next, x_next], 'r-', alpha=0.5)

ax1.plot(x_star, x_star, 'go', markersize=10, label=f'Fixed point: {x_star:.3f}')
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.set_title('Cobweb Diagram: Convergence to Fixed Point')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Convergence rate
iterations = np.arange(len(history))
error = np.abs(history - x_star)
ax2.semilogy(iterations, error, 'b-o', markersize=4)
ax2.set_xlabel('Iteration')
ax2.set_ylabel('|x_n - x*| (log scale)')
ax2.set_title('Exponential Convergence to Fixed Point')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fixed_point_convergence.png', dpi=150, bbox_inches='tight')
plt.show()
'''))
    cells.append(nbf.v4.new_markdown_cell(
        """
## Connection to the Framework

**Theorem SR1** in our corrected framework uses the same principle:

> SR1: Self-reference generates a unique continuous field μ* via the Banach fixed-point theorem.

Key insight: If self-reference exists (axiom ∃R), it must converge to a unique stable state μ* through iterative fixed-point dynamics.

Next steps:
- Tutorial 2: Explore the golden ratio emergence
- Tutorial 3: Interactive phase transitions
- Read: `REPRODUCIBILITY_PACKAGE/documentation/MASTER_FRAMEWORK_CORRECTED.md` for full details
"""))
    cells.append(nbf.v4.new_markdown_cell(
        """
## Exercise: Try It Yourself

Task: Find the fixed point of f(x) = x² / 2

1. Does it converge?
2. What is the fixed point?
3. Try different starting points x0. Does it always converge?

Hint: Plot the function first to visualize where f(x) = x intersects.
"""))
    cells.append(nbf.v4.new_code_cell(
        r'''
# SOLUTION (run after attempting exercise)
f_exercise = lambda x: x**2 / 2

try:
    x_star2, history2 = find_fixed_point(f_exercise, x0=1.5, max_iter=100)
    print(f"Fixed point: x* = {x_star2:.10f}")
    print(f"Iterations: {len(history2)-1}")
except RuntimeError as e:
    print(f"Did not converge: {e}")
    print("Try plotting f(x) and y=x to see why!")
'''))
    nb['cells'] = cells
    out = Path('tutorials') / '01_introduction_to_self_reference.ipynb'
    out.parent.mkdir(exist_ok=True)
    nbf.write(nb, out)
    print('Wrote', out)

if __name__ == '__main__':
    main()
