from pathlib import Path
import importlib.util


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_percolation_smoke():
    code = Path(__file__).resolve().parents[1] / "code" / "theorem_sr6_percolation.py"
    mod = load_module(code)
    # Smoke test: run estimator with tiny grid/trials completes and writes CSV
    pvals = [0.55, 0.59, 0.62]
    data = mod.estimate(grid_size=20, trials=5, p_values=pvals, seed=1)
    assert len(data) == len(pvals)

