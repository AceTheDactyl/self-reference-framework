#!/usr/bin/env python3
"""
SR3: Fibonacci ratio convergence to golden ratio.
Outputs JSON to ../data/sr3_fibonacci_convergence.json
"""
from __future__ import annotations
import json
from math import sqrt
from pathlib import Path


def fibonacci(n: int):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main() -> None:
    N = 50
    F_nm1 = fibonacci(N - 1)
    F_n = fibonacci(N)
    ratio = F_n / F_nm1
    phi = (1 + sqrt(5)) / 2
    data = {
        "n": N,
        "F_n": int(F_n),
        "F_n-1": int(F_nm1),
        "ratio": ratio,
        "phi": phi,
        "abs_error": abs(ratio - phi),
    }
    out = Path(__file__).resolve().parents[1] / "data" / "sr3_fibonacci_convergence.json"
    out.write_text(json.dumps(data, indent=2))
    print(f"SR3 Fibonacci ratio at n=50: {ratio:.15f}; wrote {out}")


if __name__ == "__main__":
    main()

