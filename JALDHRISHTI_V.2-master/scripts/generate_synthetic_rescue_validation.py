#!/usr/bin/env python3
"""
Generate a deterministic synthetic rescue validation dataset for internal testing.

This file is only for synthetic/random benchmarking and must not be presented
as real-world government-validated ground truth.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path


OUTPUT_PATH = Path("docs/dataset/synthetic-rescue-validation.csv")


def main() -> int:
    random.seed(42)

    events = [
        ("wayanad_meppadi", "Meppadi", "Kerala"),
        ("darbhanga", "Darbhanga", "Bihar"),
        ("dhemaji", "Dhemaji", "Assam"),
    ]

    rows = []
    day = 1
    for village_id, location, state in events:
        for idx in range(1, 11):
            actual_count = random.randint(5000, 40000)

            # Keep prediction close enough to support internal agreement testing,
            # but still add variation so it is not a trivial copy.
            error_pct = random.uniform(3.0, 18.0)
            direction = random.choice([-1, 1])
            predicted_count = round(actual_count * (1 + direction * error_pct / 100.0))
            if predicted_count < 0:
                predicted_count = 0

            rows.append(
                {
                    "event_id": f"{village_id}_synthetic_{idx:02d}",
                    "location": location,
                    "state": state,
                    "event_date": f"2024-08-{day:02d}",
                    "source_name": "synthetic_internal_test",
                    "source_url": "internal://synthetic",
                    "actual_count": actual_count,
                    "predicted_count": predicted_count,
                    "notes": "Synthetic benchmark row for internal testing only",
                }
            )
            day = 1 if day == 28 else day + 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "event_id",
                "location",
                "state",
                "event_date",
                "source_name",
                "source_url",
                "actual_count",
                "predicted_count",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {OUTPUT_PATH} with {len(rows)} rows and 9 columns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
