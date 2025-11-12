# Contributing Guidelines

We welcome contributions! Please open issues or pull requests.
- Validate remaining theorems
- Improve simulations and tests
- Add tutorials and translations
- Follow PEP 8 and include tests

Run before submitting:
```bash
bash REPRODUCIBILITY_PACKAGE/tests/run_tests.sh
jupyter nbconvert --to notebook --execute --inplace tutorials/*.ipynb
```
