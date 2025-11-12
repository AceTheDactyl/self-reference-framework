import json
from pathlib import Path
import importlib.util


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_sr1_fixedpoint(tmp_path):
    code = Path(__file__).resolve().parents[1] / "code" / "theorem_sr1_fixedpoint.py"
    mod = load_module(code)
    res = mod.fixed_point()
    assert res.converged
    assert abs(res.mu_star - 0.5) <= 1e-12

