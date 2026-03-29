#!/usr/bin/env python3
"""
Generate a clean synthetic model-output dataset for Meppadi, Kerala.

This dataset is intended for internal benchmarking and presentation rehearsal.
It is not government data and must not be presented as official ground truth.
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path


OUTPUT_CSV = Path("docs/dataset/kerala_meppadi_synthetic_model_output_30000.csv")
OUTPUT_SUMMARY = Path("docs/dataset/kerala_meppadi_synthetic_model_output_30000_summary.md")


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def gaussian(lon: float, lat: float, center_lon: float, center_lat: float, spread_lon: float, spread_lat: float) -> float:
    dx = (lon - center_lon) / spread_lon
    dy = (lat - center_lat) / spread_lat
    return math.exp(-0.5 * (dx * dx + dy * dy))


def risk_level_from_score(score: float) -> str:
    if score >= 0.85:
        return "extreme"
    if score >= 0.65:
        return "high"
    if score >= 0.40:
        return "medium"
    return "low"


def priority_from_values(trapped: int, score: float) -> str:
    if trapped >= 5 and score >= 0.80:
        return "critical"
    if trapped >= 3 and score >= 0.60:
        return "high"
    if trapped >= 1 and score >= 0.35:
        return "medium"
    return "low"


def main() -> int:
    random.seed(20260329)

    state = "Kerala"
    district = "Wayanad"
    village = "Meppadi"
    event_id = "meppadi_monsoon_case_01"
    event_date = "2024-08-01"

    min_lon, min_lat, max_lon, max_lat = 76.10, 11.52, 76.17, 11.59
    grid_x_count = 150
    grid_y_count = 200
    step_lon = (max_lon - min_lon) / grid_x_count
    step_lat = (max_lat - min_lat) / grid_y_count

    rows = []
    total_present = 0
    total_trapped = 0

    for gx in range(grid_x_count):
        for gy in range(grid_y_count):
            lon = min_lon + (gx + 0.5) * step_lon
            lat = min_lat + (gy + 0.5) * step_lat

            ridge = math.sin(gx * 0.08) * 85 + math.cos(gy * 0.06) * 70
            valley = gaussian(lon, lat, 76.135, 11.555, 0.012, 0.010)
            eastern_drainage = gaussian(lon, lat, 76.148, 11.547, 0.010, 0.008)
            high_ground = gaussian(lon, lat, 76.125, 11.585, 0.009, 0.008)

            elevation = 780 + ridge - valley * 95 - eastern_drainage * 55 + high_ground * 45
            elevation = round(clamp(elevation, 640, 930), 2)

            rain_pattern = 165 + math.sin(gx * 0.05) * 26 + math.cos(gy * 0.04) * 18 + random.uniform(-12, 12)
            rainfall_24h_mm = round(clamp(rain_pattern, 95, 255), 1)

            elev_norm = clamp((elevation - 640) / (930 - 640), 0.0, 1.0)
            low_elevation_factor = 1.0 - elev_norm

            flood_depth = (
                0.12
                + (rainfall_24h_mm / 240.0) * 0.95
                + valley * 1.15
                + eastern_drainage * 0.55
                + low_elevation_factor * 0.60
                - high_ground * 0.45
                + random.uniform(-0.08, 0.08)
            )
            flood_depth_m = round(clamp(flood_depth, 0.0, 3.4), 2)

            depth_norm = clamp(flood_depth_m / 3.4, 0.0, 1.0)
            rain_norm = clamp((rainfall_24h_mm - 95) / (255 - 95), 0.0, 1.0)
            risk_score = (
                depth_norm * 0.50
                + rain_norm * 0.20
                + valley * 0.18
                + eastern_drainage * 0.07
                + low_elevation_factor * 0.05
            )
            risk_score = round(clamp(risk_score, 0.0, 0.99), 2)
            risk_level = risk_level_from_score(risk_score)

            pop_density = (
                gaussian(lon, lat, 76.135, 11.555, 0.010, 0.010) * 1.00
                + gaussian(lon, lat, 76.145, 11.575, 0.011, 0.010) * 0.65
                + gaussian(lon, lat, 76.126, 11.548, 0.010, 0.009) * 0.55
            )

            people_present = int(
                round(
                    clamp(
                        pop_density * 5.2
                        + max(0.0, 0.8 - high_ground * 0.5)
                        + random.uniform(-0.7, 0.9),
                        0.0,
                        9.0,
                    )
                )
            )

            trap_ratio = (
                risk_score * 0.72
                + depth_norm * 0.14
                + valley * 0.08
                - high_ground * 0.10
                + random.uniform(-0.05, 0.05)
            )
            trap_ratio = clamp(trap_ratio, 0.0, 0.95)

            people_trapped = min(people_present, int(round(people_present * trap_ratio)))
            rescue_priority = priority_from_values(people_trapped, risk_score)

            total_present += people_present
            total_trapped += people_trapped

            rows.append(
                {
                    "record_id": f"MPD-{gx:03d}-{gy:03d}",
                    "event_id": event_id,
                    "event_date": event_date,
                    "state": state,
                    "district": district,
                    "village": village,
                    "latitude": f"{lat:.6f}",
                    "longitude": f"{lon:.6f}",
                    "elevation_m": f"{elevation:.2f}",
                    "rainfall_24h_mm": f"{rainfall_24h_mm:.1f}",
                    "flood_depth_m": f"{flood_depth_m:.2f}",
                    "risk_score": f"{risk_score:.2f}",
                    "risk_level": risk_level,
                    "people_present_est": people_present,
                    "people_trapped_est": people_trapped,
                    "rescue_priority": rescue_priority,
                }
            )

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "record_id",
                "event_id",
                "event_date",
                "state",
                "district",
                "village",
                "latitude",
                "longitude",
                "elevation_m",
                "rainfall_24h_mm",
                "flood_depth_m",
                "risk_score",
                "risk_level",
                "people_present_est",
                "people_trapped_est",
                "rescue_priority",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    risk_counts = {"low": 0, "medium": 0, "high": 0, "extreme": 0}
    for row in rows:
        risk_counts[row["risk_level"]] += 1

    summary = f"""# Kerala Meppadi Synthetic Model Output Summary

- Rows: {len(rows)}
- Columns: 16
- State: Kerala
- District: Wayanad
- Village: Meppadi
- Event ID: {event_id}
- Event Date: {event_date}
- Total people present estimate: {total_present}
- Total people trapped estimate: {total_trapped}

## Risk Level Distribution

- Low: {risk_counts["low"]}
- Medium: {risk_counts["medium"]}
- High: {risk_counts["high"]}
- Extreme: {risk_counts["extreme"]}

## Important Note

This file is a clean synthetic model-output dataset for internal testing and presentation rehearsal.
It is not official ground-truth or government-verified rescue data.
"""

    OUTPUT_SUMMARY.write_text(summary, encoding="utf-8")
    print(f"Generated {OUTPUT_CSV} with {len(rows)} rows and 16 columns")
    print(f"Total people present estimate: {total_present}")
    print(f"Total people trapped estimate: {total_trapped}")
    print(f"Summary written to: {OUTPUT_SUMMARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
