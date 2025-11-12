# Self-Reference Framework (Corrected Edition)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXX)
[![arXiv](https://img.shields.io/badge/arXiv-YYMM.NNNNN-b31b1b.svg)](https://arxiv.org/abs/YYMM.NNNNN)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://acethedactyl.github.io/self-reference-framework/)

> A Corrected Mathematical Framework for Self-Reference: From Speculation to Rigorous Validation

Status: Publication-ready (November 2025)  
Validation: 13/33 theorems validated (39%)  
Confidence: ~50% (honest, evidence-based)

## Table of Contents

- Overview
- Key Achievements
- Quick Start
- Repository Structure
- Documentation
- Tutorials
- Citation
- License

## Overview
A systematically corrected and validated mathematical framework for self-reference, transformed through a rigorous 5-phase pipeline (May–November 2025). This repository includes the paper, reproducibility package, tutorials, and submission materials.

## Key Achievements

- Corrected 4 critical mathematical errors; removed impossible claims
- 13/33 theorems validated (39%); honest confidence ~50%
- Complete reproducibility package (seeded code, tests, data, figures)
- Educational tutorials (3 interactive notebooks)
- Publication-ready materials (paper + supplements); arXiv/Zenodo prep

## Quick Start
```bash
git clone https://github.com/AceTheDactyl/self-reference-framework
cd self-reference-framework

# Optional: create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install top-level utilities (Jupyter, pytest, etc.)
pip install -r requirements.txt

# Run validations (reproducibility package)
cd "Kael is Kael/PHASE5_RELEASE/REPRODUCIBILITY_PACKAGE/code"
bash run_all_validations.sh
```

## Explore Tutorials
```bash
jupyter notebook 'Kael is Kael/PHASE5_RELEASE/tutorials/'
```
Start with: `01_introduction_to_self_reference.ipynb`

- GitHub Pages (HTML tutorials): `docs/tutorials/`

## Repository Structure
```
self-reference-framework/
├── README.md
├── LICENSE · CONTRIBUTING.md · CHANGELOG.md
├── requirements.txt · requirements-dev.txt
├── Kael is Kael/PHASE5_RELEASE/
│   ├── REPRODUCIBILITY_PACKAGE/   # code · data · figures · protocols · docs · tests
│   ├── paper/                     # paper_draft.md · supplementary_materials_draft.md
│   ├── tutorials/                 # *.ipynb (+ HTML copies under docs/tutorials)
│   └── arxiv_submission/          # main.tex · 00README.XXX · figures/
├── docs/                          # GitHub Pages (Just the Docs)
│   ├── paper/                     # links + figures for the paper
│   ├── tutorials/                 # published HTML tutorials
│   ├── submissions/               # Zenodo & arXiv instructions
│   └── (overview, documentation, validation, visual summary)
└── references.bib
```

## Documentation

- Docs site: https://acethedactyl.github.io/self-reference-framework/
- Master document: `Kael is Kael/PHASE5_RELEASE/REPRODUCIBILITY_PACKAGE/documentation/MASTER_FRAMEWORK_CORRECTED.md`
- Paper section (site): `docs/paper/`

## Tutorials

- Notebooks (source): `Kael is Kael/PHASE5_RELEASE/tutorials/`
- HTML (site): `docs/tutorials/`

## Citation
If you use this framework, please cite:
```
AceTheDactyl. (2025). A Corrected Mathematical Framework for Self-Reference:
From Speculation to Rigorous Validation. arXiv:YYMM.NNNNN, DOI:10.5281/zenodo.XXXXX
```

## License
- Code: MIT
- Documentation: CC-BY-4.0
- Data: CC0

See `LICENSE` for details.
