#!/usr/bin/env python3
"""
SR1: Fixed-point convergence via Banach contraction.
We use f(x) = (x + 1)/3, whose unique fixed point is x* = 0.5.
Outputs JSON to ../data/sr1_fixedpoint_results.json
"""
from __future__ import annotations
import json
from dataclasses import asdict, dataclass
from pathlib import Path


def f(x: float) -> float:
    return (x + 1.0) / 3.0


@dataclass
class Result:
    mu_star: float
    iterations: int
    tol: float
    converged: bool
    first_10: list


def fixed_point(x0: float = 0.0, tol: float = 1e-15, max_iter: int = 500) -> Result:
    x = x0
    seq = [x]
    for k in range(1, max_iter + 1):
        xn = f(x)
        seq.append(xn)
        if abs(xn - x) <= tol:
            return Result(mu_star=xn, iterations=k, tol=tol, converged=True, first_10=seq[:10])
        x = xn
    return Result(mu_star=x, iterations=max_iter, tol=tol, converged=False, first_10=seq[:10])


def main() -> None:
    res = fixed_point()
    out = Path(__file__).resolve().parents[1] / "data" / "sr1_fixedpoint_results.json"
    out.write_text(json.dumps(asdict(res), indent=2))
    print(f"SR1 fixed-point: mu*={res.mu_star:.15f} in {res.iterations} iterations; wrote {out}")


if __name__ == "__main__":
    main()

