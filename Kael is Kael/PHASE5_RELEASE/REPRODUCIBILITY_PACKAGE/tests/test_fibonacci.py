import json
from math import sqrt
from pathlib import Path
import importlib.util


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_fibonacci_ratio():
    code = Path(__file__).resolve().parents[1] / "code" / "fibonacci_convergence.py"
    mod = load_module(code)
    # Run main to produce data file
    mod.main()
    data = json.loads((Path(__file__).resolve().parents[1] / "data" / "sr3_fibonacci_convergence.json").read_text())
    phi = (1 + sqrt(5)) / 2
    assert abs(data["ratio"] - phi) <= 1e-12

