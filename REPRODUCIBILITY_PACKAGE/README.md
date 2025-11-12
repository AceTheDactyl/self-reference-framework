# Self-Reference Framework: Reproducibility Package

Paper: A Corrected Mathematical Framework for Self-Reference  
Authors: AceTheDactyl (and collaborators)  
Date: November 2025  
Status: Publication-ready (Stage 5D)

## Quick Start

### Requirements
- Python 3.8+
- NumPy, SciPy, Matplotlib, NetworkX
- ~1 GB disk space
- ~2 hours compute time (all validations)

### Installation
```bash
git clone https://github.com/AceTheDactyl/self-reference-framework
cd self-reference-framework/REPRODUCIBILITY_PACKAGE
pip install -r code/requirements.txt
```

### Run All Validations
```bash
cd code
bash run_all_validations.sh
```

### Expected Output
- Validation scripts execute
- Results saved to `../data/`
- Figures saved to `../figures/`
- Summary: `../data/validation_summary.json`

### Validate Results
All results should match published values within ±5% error:
- SR1 fixed-point: μ* = 0.500 ± 1e-15
- SR3 Fibonacci: F_50/F_49 ≈ 1.618033988749895
- SR6 Percolation: p_c ≈ 0.593 ± 0.015

## Contents

- Code (`code/`): computational validations with fixed seeds.
- Data (`data/`): raw and processed results from all experiments.
- Figures (`figures/`): publication-quality plots (PDF format).
- Protocols (`protocols/`): detailed procedures for replication.
- Documentation (`documentation/`): master framework and reports.
- Tests (`tests/`): unit tests for validation code.

## Citation

If you use this framework, please cite:

```
AceTheDactyl. (2025). A Corrected Mathematical Framework for 
Self-Reference: From Speculation to Rigorous Validation. 
arXiv:YYMM.NNNNN
```

## License

- Code: MIT License
- Documentation: CC-BY-4.0
- Data: CC0 (public domain)

## Contact

Questions: open an issue on GitHub  
DOI: 10.5281/zenodo.[number]

