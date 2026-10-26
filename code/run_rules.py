"""Run the five rule-based verifiers on a dataset and compare with the expected labels.

Usage:
  python run_rules.py            (pilot: the 30 hand-checked cases)
  python run_rules.py auto       (the automatically built SEC dataset)
"""

import os
import sys

from common import RESULTS_DIR, load_dataset, read_csv, write_csv, CODE_DIR
from scoring import score, format_report
from verifier import RULES, run_all_rules

RULE_NAMES = {
    "B1": "B1 context-only (ignores time and policy)",
    "B3": "B3 latest figure before the cutoff (ignores policy)",
    "B4": "B4 policy-aware latest (ignores withdrawal notices)",
    "B4W": "B4W policy-aware latest + withdrawal flag",
    "P": "P scoped reference resolver",
}

MANUAL_TRACE = os.path.join(CODE_DIR, "..", "pilot", "manual_baseline_trace.csv")
MANUAL_COLUMNS = {"B1": "B1_context_only", "B3": "B3_cutoff_latest", "B4": "B4_policy_latest",
                  "B4W": "B4_plus_withdrawal", "P": "P_scoped_reference"}


def compare_with_manual_trace(rows):
    """Check that the program reproduces every hand-applied rule decision."""
    manual = {r["case_id"]: r for r in read_csv(MANUAL_TRACE)}
    mismatches = []
    for row in rows:
        for rule, column in MANUAL_COLUMNS.items():
            if row[rule] != manual[row["case_id"]][column]:
                mismatches.append(f"{row['case_id']} {rule}: program={row[rule]} manual={manual[row['case_id']][column]}")
    return mismatches


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "pilot"
    documents, facts, claims = load_dataset(name)
    rows = run_all_rules(claims, documents, facts)

    out_csv = os.path.join(RESULTS_DIR, f"rules_{name}.csv")
    write_csv(out_csv, rows, ["case_id", "family_id", "policy", "gold_label"] + RULES)

    report = [f"# Rule-based verifiers on the `{name}` dataset", "",
              f"{len(claims)} claims from {len({c['family_id'] for c in claims})} companies.", ""]
    print(f"\n{len(claims)} claims, dataset '{name}'\n")
    print(f"{'Rule':55s} {'Correct':>8s} {'Errors':>7s} {'Accuracy':>9s}")
    for rule in RULES:
        stats = score(rows, rule)
        print(f"{RULE_NAMES[rule]:55s} {stats['correct']:>5d}/{stats['n']:<3d}{stats['errors']:>6d} {stats['accuracy']:>9.1%}")
        report.append(format_report(RULE_NAMES[rule], stats))

    if name == "pilot":
        mismatches = compare_with_manual_trace(rows)
        if mismatches:
            msg = "WARNING: program differs from the hand-applied trace:\n" + "\n".join(mismatches)
        else:
            msg = ("Check passed: the program reproduces all 150 hand-applied decisions "
                   "(30 cases x 5 rules) in pilot/manual_baseline_trace.csv.")
        print("\n" + msg)
        report.insert(4, msg + "\n")

    out_md = os.path.join(RESULTS_DIR, f"rules_{name}_report.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"\nPer-case predictions: {out_csv}\nFull report: {out_md}")


if __name__ == "__main__":
    main()
