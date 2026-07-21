#!/usr/bin/env python3

from __future__ import annotations

import csv
from pathlib import Path
from typing import Final

HERE: Final = Path(__file__).resolve().parent


def main() -> int:
    with (HERE / "systems.csv").open(encoding="utf-8", newline="") as handle:
        systems = list(csv.DictReader(handle))
    with (HERE / "trustworthy_closure.csv").open(encoding="utf-8", newline="") as handle:
        outcomes = list(csv.DictReader(handle))

    print("Historical closure-association artifact")
    print(f"Loaded {len(systems)} core-system rows and {len(outcomes)} outcome rows.")
    print("No contingency is reported: the outcome overlaps validator evidence,")
    print("labels were revised post hoc, and the withdrawn binary predictor pools")
    print("heterogeneous gate, reliability, and calibration states.")
    print("The data do not establish even the direction of an association.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
