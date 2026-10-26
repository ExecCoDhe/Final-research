"""Collect every result into one table: results/SUMMARY.md."""

import glob
import os

from common import RESULTS_DIR, read_csv
from run_rules import RULE_NAMES
from scoring import score
from verifier import RULES


def row(name, stats, newest_agreement=""):
    by_policy = "; ".join(f"{p} {c}/{t}" for p, (c, t) in stats["by_policy"].items())
    return (f"| {name} | {stats['n']} | {stats['accuracy']:.1%} | {stats['company_level_accuracy']:.1%} | "
            f"{stats['coverage']:.0%} | {newest_agreement} | {by_policy} |")


def agreement_with(preds, rules, rule="B3"):
    """Share of claims where the model gives the same label as a rule."""
    by_case = {r["case_id"]: r[rule] for r in rules}
    pairs = [(p["prediction"], by_case[p["case_id"]]) for p in preds if p["case_id"] in by_case]
    return f"{sum(a == b for a, b in pairs) / len(pairs):.0%}" if pairs else ""


def main():
    lines = ["# Results summary", "",
             "Accuracy = share of claims answered with the correct label (S, C or U). "
             "Company-level accuracy weights every company equally, because claims about the same "
             "company are not independent. 'Same as newest-wins' is how often an AI model gives the same "
             "label as rule B3, which always trusts the newest figure before the cutoff; a high value in the "
             "'bare' condition means the model silently assumes that convention.", ""]
    header = ["| Method | Claims | Accuracy | Company-level | Decisive (S/C) | Same as newest-wins | Correct per policy |",
              "|---|---:|---:|---:|---:|---:|---|"]

    for dataset in ("pilot", "auto"):
        rules_csv = os.path.join(RESULTS_DIR, f"rules_{dataset}.csv")
        llm_files = sorted(glob.glob(os.path.join(RESULTS_DIR, f"llm_{dataset}_*.csv")))
        if not os.path.exists(rules_csv) and not llm_files:
            continue
        lines += [f"## Dataset: {dataset}", ""] + header
        rules = read_csv(rules_csv) if os.path.exists(rules_csv) else []
        for rule in RULES if rules else []:
            lines.append(row(RULE_NAMES[rule], score(rules, rule)))
        for path in llm_files:
            preds = read_csv(path)
            stats = score(preds, "prediction")
            if stats:
                name = os.path.basename(path)[len(f"llm_{dataset}_"):-len(".csv")]
                lines.append(row(f"AI model: {name}", stats, agreement_with(preds, rules) if rules else ""))
        lines.append("")

    out = os.path.join(RESULTS_DIR, "SUMMARY.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
    print(f"\nSaved: {out}")


if __name__ == "__main__":
    main()
