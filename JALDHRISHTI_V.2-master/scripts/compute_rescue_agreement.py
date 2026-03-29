#!/usr/bin/env python3
"""
Compute simple agreement metrics between real rescue/affected counts and model predictions.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path


def to_float(value: str) -> float:
    value = (value or "").strip()
    if not value:
        raise ValueError("missing numeric value")
    return float(value.replace(",", ""))


def compute_row_metrics(actual: float, predicted: float) -> tuple[float, float, float]:
    absolute_error = abs(predicted - actual)
    percentage_error = 0.0 if actual == 0 else (absolute_error / actual) * 100.0
    agreement_score = max(0.0, 100.0 - percentage_error)
    return absolute_error, percentage_error, agreement_score


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/compute_rescue_agreement.py <input_csv>")
        return 1

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Input CSV has headers but no data rows.")
        return 1

    required = {"event_id", "location", "state", "event_date", "source_name", "source_url", "actual_count", "predicted_count", "notes"}
    missing = required.difference(reader.fieldnames or [])
    if missing:
        print(f"Missing required columns: {', '.join(sorted(missing))}")
        return 1

    output_rows = []
    total_actual = 0.0
    total_predicted = 0.0
    total_abs_error = 0.0
    total_agreement = 0.0
    valid_rows = 0

    for row in rows:
        try:
            actual = to_float(row["actual_count"])
            predicted = to_float(row["predicted_count"])
        except ValueError:
            continue

        absolute_error, percentage_error, agreement_score = compute_row_metrics(actual, predicted)

        output_row = dict(row)
        output_row["absolute_error"] = f"{absolute_error:.2f}"
        output_row["percentage_error"] = f"{percentage_error:.2f}"
        output_row["agreement_score_pct"] = f"{agreement_score:.2f}"
        output_rows.append(output_row)

        total_actual += actual
        total_predicted += predicted
        total_abs_error += absolute_error
        total_agreement += agreement_score
        valid_rows += 1

    if valid_rows == 0:
        print("No valid numeric rows found in the CSV.")
        return 1

    output_path = input_path.with_name(f"{input_path.stem}_report.csv")
    fieldnames = list(rows[0].keys()) + ["absolute_error", "percentage_error", "agreement_score_pct"]
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    mean_absolute_error = total_abs_error / valid_rows
    mean_agreement_score = total_agreement / valid_rows
    total_percentage_error = 0.0 if total_actual == 0 else abs(total_predicted - total_actual) / total_actual * 100.0
    total_agreement_score = max(0.0, 100.0 - total_percentage_error)

    print(f"Rows evaluated: {valid_rows}")
    print(f"Average absolute error: {mean_absolute_error:.2f}")
    print(f"Average agreement score: {mean_agreement_score:.2f}%")
    print(f"Total actual count: {total_actual:.2f}")
    print(f"Total predicted count: {total_predicted:.2f}")
    print(f"Overall agreement score: {total_agreement_score:.2f}%")
    print(f"Report written to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
