"""Accuracy, per-policy accuracy, per-company accuracy and confusion matrices."""

from collections import defaultdict

LABELS = ["S", "C", "U"]


def score(rows, pred_key, gold_key="gold_label"):
    rows = [r for r in rows if r.get(pred_key)]
    n = len(rows)
    if n == 0:
        return None
    correct = sum(r[pred_key] == r[gold_key] for r in rows)

    by_policy = defaultdict(lambda: [0, 0])
    by_family = defaultdict(lambda: [0, 0])
    confusion = {g: {p: 0 for p in LABELS + ["invalid"]} for g in LABELS}
    for r in rows:
        hit = r[pred_key] == r[gold_key]
        by_policy[r["policy"]][0] += hit
        by_policy[r["policy"]][1] += 1
        by_family[r["family_id"]][0] += hit
        by_family[r["family_id"]][1] += 1
        pred = r[pred_key] if r[pred_key] in LABELS else "invalid"
        confusion[r[gold_key]][pred] += 1

    family_acc = [c / t for c, t in by_family.values()]
    decisive = [r for r in rows if r[pred_key] in ("S", "C")]
    false_support = sum(1 for r in rows if r[gold_key] == "C" and r[pred_key] == "S")
    gold_c = sum(1 for r in rows if r[gold_key] == "C")
    return {
        "n": n,
        "correct": correct,
        "accuracy": correct / n,
        "errors": n - correct,
        "company_level_accuracy": sum(family_acc) / len(family_acc),
        "companies": len(by_family),
        "coverage": len(decisive) / n,
        "false_support_rate": (false_support / gold_c) if gold_c else None,
        "by_policy": {k: (c, t) for k, (c, t) in sorted(by_policy.items())},
        "confusion": confusion,
    }


def format_report(title, stats):
    lines = [f"### {title}", ""]
    if stats is None:
        return "\n".join(lines + ["No predictions.", ""])
    lines.append(f"- Accuracy: **{stats['correct']}/{stats['n']} = {stats['accuracy']:.1%}** "
                 f"({stats['errors']} errors)")
    lines.append(f"- Company-level accuracy (each company weighted equally, {stats['companies']} companies): "
                 f"{stats['company_level_accuracy']:.1%}")
    lines.append(f"- Decisive answers (S or C): {stats['coverage']:.1%}")
    if stats["false_support_rate"] is not None:
        lines.append(f"- False support (true answer C, predicted S): {stats['false_support_rate']:.1%}")
    lines.append("")
    lines.append("| Policy | Correct | Total | Accuracy |")
    lines.append("|---|---:|---:|---:|")
    for policy, (c, t) in stats["by_policy"].items():
        lines.append(f"| {policy} | {c} | {t} | {c / t:.0%} |")
    lines.append("")
    lines.append("Confusion matrix (rows = correct answer, columns = prediction):")
    lines.append("")
    lines.append("| correct \\ predicted | S | C | U | invalid |")
    lines.append("|---|---:|---:|---:|---:|")
    for g in LABELS:
        row = stats["confusion"][g]
        lines.append(f"| {g} | {row['S']} | {row['C']} | {row['U']} | {row['invalid']} |")
    lines.append("")
    return "\n".join(lines)
