#!/usr/bin/env python3
"""
Generate publication-quality figures into ../figures/
Implements:
- Figure 2: Validation Status (bar chart)
- Figure 4: Fibonacci Convergence (ratio to golden ratio)
"""
from __future__ import annotations
import json
from math import sqrt
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt


def fig2_validation_status(outdir: Path):
    categories = ["Validated", "Pending", "Removed"]
    counts = [13, 18, 2]
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(categories, counts, color=colors, edgecolor='black', linewidth=1.5)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}/33', ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Theorems', fontsize=12)
    ax.set_title('Validation Status (13/33 = 39%)', fontsize=14, fontweight='bold')
    ax.set_ylim([0, 20])
    ax.grid(axis='y', alpha=0.3)
    out = outdir / 'fig2_validation_status.pdf'
    fig.tight_layout()
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"Wrote {out}")


def fig4_fibonacci(outdir: Path, data_dir: Path):
    dpath = data_dir / 'sr3_fibonacci_convergence.json'
    if not dpath.exists():
        raise SystemExit(f"Missing data file: {dpath}. Run fibonacci_convergence.py first.")
    data = json.loads(dpath.read_text())
    phi = (1 + sqrt(5)) / 2
    ratio = data['ratio']
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(phi, color='k', linestyle='--', label=r"$\varphi$")
    ax.plot([data['n']], [ratio], 'o', color='#2c3e50', label='F_50/F_49')
    ax.set_xlabel('n')
    ax.set_ylabel('F_n/F_{n-1}')
    ax.set_title('Fibonacci Convergence to Golden Ratio')
    ax.legend()
    out = outdir / 'fig4_fibonacci_ratios.pdf'
    fig.tight_layout()
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"Wrote {out}")


def main():
    root = Path(__file__).resolve().parents[1]
    outdir = root / 'figures'
    datadir = root / 'data'
    outdir.mkdir(parents=True, exist_ok=True)
    # Prefer a non-interactive backend for headless
    matplotlib.use('Agg', force=True)
    fig2_validation_status(outdir)
    fig4_fibonacci(outdir, datadir)


if __name__ == '__main__':
    main()

