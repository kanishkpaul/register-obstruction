"""Check the internal consistency of the public aggregate evidence."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
MARKED = {"FORMAL", "FAMILIAR", "INTIMATE"}


def read_csv(name: str) -> list[dict[str, str]]:
    with (RESULTS / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def check_classifier() -> None:
    metrics = read_csv("classifier_validation.csv")
    confusion = read_csv("classifier_confusion.csv")
    by_language: dict[str, int] = defaultdict(int)
    for row in confusion:
        by_language[row["language"]] += int(row["count"])
    assert by_language == {"bn": 147, "hi": 150}

    gated = [
        row for row in metrics if row["class"] in MARKED
    ]
    assert len(gated) == 6
    assert all(float(row["precision"]) >= 0.90 for row in gated)


def check_baselines() -> None:
    rows = read_csv("direct_vs_pivot.csv")
    grouped: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        grouped[row["system"]][row["path"]] = row
        assert int(row["n"]) == 256
        total = (
            float(row["survival_pct"])
            + float(row["flip_pct"])
            + float(row["neutralization_pct"])
        )
        assert abs(total - 100.0) <= 0.002

    assert len(grouped) == 5
    assert all(set(paths) == {"direct", "pivot"} for paths in grouped.values())
    assert float(grouped["Gemma-3-12B"]["direct"]["survival_pct"]) > float(
        grouped["Gemma-3-12B"]["pivot"]["survival_pct"]
    )
    assert float(grouped["IndicTrans2"]["direct"]["survival_pct"]) < float(
        grouped["IndicTrans2"]["pivot"]["survival_pct"]
    )


def check_provenance() -> None:
    provenance = json.loads((RESULTS / "provenance.json").read_text())
    assert len(provenance["source"]["commit"]) == 40
    assert provenance["validation"]["independent_human_annotation"] is False
    assert provenance["frozen_set"]["verified_by_human"] is False
    assert provenance["frozen_set"]["register_items"] == 256
    for section, key in [
        ("validation", "private_report_sha256"),
        ("frozen_set", "content_freeze_sha256"),
        ("baseline_results", "private_per_item_export_sha256"),
    ]:
        assert len(provenance[section][key]) == 64


def main() -> None:
    check_classifier()
    check_baselines()
    check_provenance()
    print("public result tables are internally consistent")


if __name__ == "__main__":
    main()
