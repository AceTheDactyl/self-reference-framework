# SR6 Percolation Protocol

This protocol describes the computational estimation of the 2D square-lattice
site-percolation threshold.

## Overview
- Grid: N x N lattice (default N=60)
- Open site with probability p (Bernoulli)
- Percolation: existence of an open path from top to bottom
- Estimator: fraction of percolating trials at each p

## Steps
1. Choose grid size N and number of trials T.
2. For each p in a sweep around 0.59, generate T random grids.
3. Use BFS/union-find to detect top-to-bottom connectivity.
4. Record percolation probability vs p; estimate p_c near 0.593.

## Reproducibility
- Fixed RNG seed is used for determinism in default runs.
- Outputs: `data/sr6_percolation_data.csv`

