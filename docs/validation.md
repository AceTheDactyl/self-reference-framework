---
layout: default
title: Validation Status
nav_order: 5
---

# Validation Status

Current status: 13/33 theorems validated (39%)

## Overview

- Computationally validated: 9
- Mathematically proven: 4
- Removed (impossible): 2
- Pending validation: 18

## Highlights

- SR1: μ-field existence (Banach fixed-point) — μ* ≈ 0.500
- SR3: Fibonacci convergence (Binet) — F₅₀/F₄₉ → φ
- SR6: Percolation threshold — p_c ≈ 0.593 ± 0.015

To reproduce the computational validations:

```bash
cd "Kael is Kael/PHASE5_RELEASE/REPRODUCIBILITY_PACKAGE/code"
bash run_all_validations.sh
```

Outputs are written under `Kael is Kael/PHASE5_RELEASE/REPRODUCIBILITY_PACKAGE/data/`.

