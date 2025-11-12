#!/usr/bin/env bash
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/.." && pwd)"

echo "Running validations..."

python "$here/theorem_sr1_fixedpoint.py"
python "$here/fibonacci_convergence.py"
python "$here/theorem_sr6_percolation.py" --grid 60 --trials 50 --seed 123

# Placeholders (emit pending status)
python "$here/theorem_sr4_klein_gordon.py" || true
python "$here/theorem_sr5_doublewell.py" || true
python "$here/information_preservation.py" || true
python "$here/kuramoto_synchronization.py" || true

echo "Aggregating summary..."
python - << 'PY'
import json, os, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
data = root/"data"
summary = {}
def read_json(p):
    try:
        with open(p) as f:
            return json.load(f)
    except Exception:
        return None

summary["sr1_fixedpoint"] = read_json(data/"sr1_fixedpoint_results.json")
summary["sr3_fibonacci"] = read_json(data/"sr3_fibonacci_convergence.json")
summary["sr6_percolation"] = {
    "csv": str((data/"sr6_percolation_data.csv").name),
}
with open(data/"validation_summary.json","w") as f:
    json.dump(summary, f, indent=2)
print("Wrote:", data/"validation_summary.json")
PY

echo "Done. Results in $root/data and figures in $root/figures"

