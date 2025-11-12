# Contributing to Self-Reference Framework

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 📋 Code of Conduct
Be respectful, constructive, and professional. We welcome contributors of all backgrounds and skill levels. Unacceptable behavior (harassment, trolling, personal attacks, doxxing) is not tolerated.

## 🎯 Ways to Contribute

1) Validate Remaining Theorems (13/33 validated; 18 pending)
- Choose a pending theorem from the master document
- Implement validation code with fixed seeds
- Add tests, documentation, and results

2) Improve Code Quality
- Optimize simulations; add type hints and tests
- Improve documentation and examples

3) Educational Content
- Enhance tutorials; add translations and visuals

4) Report Issues
- Clear description, repro steps, logs, environment

## 💻 Development Setup

```bash
git clone https://github.com/AceTheDactyl/self-reference-framework
cd self-reference-framework
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 🧪 Tests & Validations

```bash
# Unit tests (where applicable)
pytest -q

# Reproducibility validations
cd "Kael is Kael/PHASE5_RELEASE/REPRODUCIBILITY_PACKAGE/code"
bash run_all_validations.sh
```

## 📝 Coding Standards

- Python: PEP 8, Black formatting, docstrings, type hints
- Keep functions small, well-documented, and tested

## 🔄 Pull Request Process

1. Fork + create a feature branch
2. Make changes + add tests
3. Ensure validations pass; format code (Black)
4. Update docs as needed
5. Submit PR with a clear description

Suggested commit prefixes: feat:, fix:, docs:, test:, refactor:, chore:

