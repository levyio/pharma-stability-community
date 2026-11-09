#!/usr/bin/env python3
"""Recompute per-brand Welch and ordinary one-way ANOVA on a user-supplied CSV.

The article's raw device table is NOT redistributed here. Source: Wood et al.,
Int J Circumpolar Health (2024), doi:10.1080/22423982.2024.2367273,
CC BY-NC 4.0. Data should be obtained from the original source lawfully.
Exploratory endpoint = expelled mass, NOT drug potency, sterility or dose
delivered into tissue. This script makes no safety/clinical prediction.
"""
import argparse
import csv
import json
import math
import statistics
from collections import defaultdict

REQUIRED = {"brand", "freeze_thaw_cycles", "expiry_ym", "ejected_mass_g"}


def f_statistics(groups):
    """Ordinary and Welch one-way F tests (F and df without external packages)."""
    arrays = [list(map(float, group)) for group in groups]
    if len(arrays) < 2 or any(len(x) < 2 for x in arrays):
        raise ValueError("At least two groups with >=2 physical devices each required")
    k = len(arrays)
    n = [len(a) for a in arrays]
    means = [statistics.mean(a) for a in arrays]
    variances = [statistics.variance(a) for a in arrays]
    if any(v <= 0 for v in variances):
        raise ValueError("Welch ANOVA undefined for zero within-group variance")
    grand = sum(m * count for m, count in zip(means, n)) / sum(n)
    ss_between = sum(count * (m - grand) ** 2 for m, count in zip(means, n))
    ss_within = sum((count - 1) * v for count, v in zip(n, variances))
    ordinary_f = (ss_between / (k - 1)) / (ss_within / (sum(n) - k))
    weights = [count / v for count, v in zip(n, variances)]
    weight_total = sum(weights)
    weighted_mean = sum(weight * m for weight, m in zip(weights, means)) / weight_total
    weighted_ss = sum(weight * (m - weighted_mean) ** 2 for weight, m in zip(weights, means)) / (k - 1)
    adjustment_sum = sum(
        ((1 - weight / weight_total) ** 2) / (count - 1)
        for weight, count in zip(weights, n)
    )
    correction = 1 + 2 * (k - 2) * adjustment_sum / (k**2 - 1)
    welch_f = weighted_ss / correction
    welch_df2 = (k**2 - 1) / (3 * adjustment_sum)
    return {
        "count": n, "mean_g": means,
        "sd_g": [math.sqrt(v) for v in variances],
        "ordinary_f": ordinary_f, "ordinary_df": [k - 1, sum(n) - k],
        "welch_f": welch_f, "welch_df": [k - 1, welch_df2]
    }


def analyze(path):
    groups = defaultdict(lambda: defaultdict(list))
    expiry_by_group = defaultdict(lambda: defaultdict(set))
    with open(path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError("CSV columns required: brand,freeze_thaw_cycles,expiry_ym,ejected_mass_g")
        for line_no, row in enumerate(reader, start=2):
            brand = row["brand"].strip()
            cycles = int(row["freeze_thaw_cycles"])
            expiry = row["expiry_ym"].strip()
            value = float(row["ejected_mass_g"])
            if not brand or cycles < 0 or not math.isfinite(value) or value <= 0:
                raise ValueError(f"invalid row {line_no}")
            if len(expiry) != 7 or expiry[4] != "-" or not (1 <= int(expiry[5:]) <= 12):
                raise ValueError(f"expiry_ym must be YYYY-MM at row {line_no}")
            groups[brand][cycles].append(value)
            expiry_by_group[brand][cycles].add(expiry)
    result = {}
    for brand, by_cycle in groups.items():
        order = sorted(by_cycle)
        summary = f_statistics([by_cycle[c] for c in order])
        summary["cycle_groups"] = order
        summary["expiry_by_group"] = {str(c): sorted(expiry_by_group[brand][c]) for c in order}
        try:
            from scipy.stats import f as f_distribution
            summary["ordinary_p"] = float(f_distribution.sf(summary["ordinary_f"], *summary["ordinary_df"]))
            summary["welch_p"] = float(f_distribution.sf(summary["welch_f"], *summary["welch_df"]))
        except ImportError:
            summary["p_values"] = "SciPy not installed: F and degrees of freedom provided"
        result[brand] = summary
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="Own transcription of original Table 1; dataset not included")
    args = parser.parse_args()
    print(json.dumps(analyze(args.csv), indent=2, sort_keys=True))
