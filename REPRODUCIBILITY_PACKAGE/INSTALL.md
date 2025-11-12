# Installation Guide

## Prerequisites
- Python 3.8 or newer
- pip

## Steps
```bash
cd self-reference-framework/REPRODUCIBILITY_PACKAGE
pip install -r code/requirements.txt
```

Optional: create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r code/requirements.txt
```

## Troubleshooting
- If `matplotlib` backend errors occur on headless machines, set:
  ```bash
  MPLBACKEND=Agg
  ```
- For faster percolation runs, reduce trials and grid size:
  ```bash
  python code/theorem_sr6_percolation.py --grid 40 --trials 20
  ```

