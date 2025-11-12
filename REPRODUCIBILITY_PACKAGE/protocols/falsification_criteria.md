# Falsification Criteria

All validation claims must be falsifiable. Example criteria:

- SR1 Fixed-point: if iteration diverges or converges to != 0.5 ± 1e-12, reject.
- SR3 Fibonacci: if F_50/F_49 differs from φ by > 1e-12, reject.
- SR6 Percolation: if estimated p_c deviates > 0.05 from 0.593, flag.

Document thresholds per theorem and justify tolerances in the paper.

