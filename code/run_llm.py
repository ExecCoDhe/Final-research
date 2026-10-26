"""Ask a free AI language model (LLM) to verify each claim, and score its answers.

Two conditions:
  full  the model is told the policy, the cutoff date and the rules
  bare  the model only sees the claim and the documents (what a normal user
        would ask); this shows what the model assumes by default

Usage examples:
  python run_llm.py --provider gemini --dataset pilot --condition full
  python run_llm.py --provider groq --dataset auto --condition bare
  python run_llm.py --provider gemini --list-models
  python run_llm.py --dry-run          (prints one prompt; no key needed)

Answers are saved after every claim, so you can stop and re-run safely: cases
already answered are skipped.
"""

import argparse
import json
import os
import re
import sys
import time

import requests

from common import RESULTS_DIR, load_dataset, load_settings, read_csv, write_csv
from scoring import format_report, score

PROVIDERS = {
    "gemini": {"base": "https://generativelanguage.googleapis.com/v1beta/openai",
               "key": "GEMINI_API_KEY", "model": "GEMINI_MODEL"},
    "groq": {"base": "https://api.groq.com/openai/v1", "key": "GROQ_API_KEY", "model": "GROQ_MODEL"},
    "ollama": {"base": "http://localhost:11434/v1", "key": None, "model": "OLLAMA_MODEL"},
}

POLICY_TEXT = {
    "original_as_filed": "ORIGINAL AS FILED: judge the claim against the figure in the company's original "
                         "report, even if it was later corrected or withdrawn.",
    "corrected_named": "CORRECTED: judge the claim against the corrected (restated or revised) figure in the "
                       "later correcting report, not against its 'as previously reported' column.",
    "as_known_packet": "AS KNOWN AT THE CUTOFF: use only documents filed before the cutoff date. A correction "
                       "filed before the cutoff replaces the original figure. If a notice filed before the "
                       "cutoff says the earlier statements should no longer be relied upon, and no corrected "
                       "figure was filed before the cutoff, the answer is U.",
    "unspecified": "UNSPECIFIED: the claim does not say whether it means the original or the corrected figure. "
                   "Consider both; if they lead to different answers, the answer is U.",
    "explicit_display_comparison": "DISPLAYED-VALUE ARITHMETIC: compute the stated calculation using the two "
                                   "displayed figures named in the claim.",
}

FULL_SYSTEM = """You verify claims about company financial reports using ONLY the evidence documents given.

Answer with one label:
  S = supported: the figure that the policy selects agrees with the claim.
  C = contradicted: the figure that the policy selects is clearly different from the claim.
  U = undetermined: the evidence under this policy cannot settle the claim.

Rules:
1. Follow the AUTHORITY POLICY given with the claim. It decides which version of a figure counts.
2. Documents filed on or after the cutoff date did not exist yet at the cutoff. The policies say how to use the cutoff.
3. Check the exact metric (for example 'net income' versus 'net income attributable to stockholders' versus 'income from continuing operations') and the exact fiscal period.
4. Figures in parentheses are losses or outflows; a claim of a 'net loss of USD X million' refers to the size of the loss.
5. A rounded figure (for example in USD thousands) cannot prove a claim about an exact, unrounded amount; such a claim is U.

Reply with JSON only, for example: {"label": "S", "reason": "one short sentence"}"""

BARE_SYSTEM = """You check claims about company financial reports using the evidence documents given.

Answer with one label:
  S = the evidence supports the claim.
  C = the evidence contradicts the claim.
  U = the evidence is not enough to decide.

Reply with JSON only, for example: {"label": "S", "reason": "one short sentence"}"""


def build_prompt(claim, documents, condition):
    lines = [f"CLAIM: {claim['claim']}"]
    if condition == "full":
        lines.append(f"AUTHORITY POLICY: {POLICY_TEXT[claim['policy']]}")
        lines.append(f"CUTOFF DATE: {claim['cutoff_date']}")
    lines.append("")
    lines.append("EVIDENCE DOCUMENTS:")
    for doc_id in claim["packet_ids"]:
        d = documents[doc_id]
        lines.append(f"[{doc_id}] {d['issuer']}, Form {d['form']}, filed {d['filing_date']}: {d['evidence_text']}")
    system = FULL_SYSTEM if condition == "full" else BARE_SYSTEM
    return system, "\n".join(lines)


def parse_label(text):
    try:
        match = re.search(r"\{.*\}", text, re.S)
        data = json.loads(match.group(0)) if match else {}
        label = str(data.get("label", "")).strip().upper()[:1]
        if label in ("S", "C", "U"):
            return label, str(data.get("reason", ""))[:300]
    except (ValueError, AttributeError):
        pass
    match = re.search(r'"label"\s*:\s*"?([SCU])', text)
    if match:
        return match.group(1), text[:300]
    return "invalid", text[:300]


def call_model(provider, settings, model, system, user):
    info = PROVIDERS[provider]
    headers = {"Content-Type": "application/json"}
    if info["key"]:
        headers["Authorization"] = f"Bearer {settings.get(info['key'], '')}"
    body = {"model": model, "temperature": 0,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    for attempt in range(6):
        try:
            r = requests.post(f"{info['base']}/chat/completions", headers=headers, json=body, timeout=120)
        except requests.RequestException as e:
            print(f"    network problem ({e.__class__.__name__}); retrying")
            time.sleep(10 * (attempt + 1))
            continue
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"] or ""
        if r.status_code in (429, 500, 502, 503):
            wait = 20 * (attempt + 1)
            print(f"    provider busy or rate limit reached (HTTP {r.status_code}); waiting {wait}s")
            time.sleep(wait)
            continue
        sys.exit(f"\nThe provider refused the request (HTTP {r.status_code}):\n{r.text[:600]}\n\n"
                 f"Check the API key in settings.txt, or run with --list-models to see valid model names.")
    return ""


def list_models(provider, settings):
    info = PROVIDERS[provider]
    headers = {"Authorization": f"Bearer {settings.get(info['key'], '')}"} if info["key"] else {}
    r = requests.get(f"{info['base']}/models", headers=headers, timeout=60)
    if r.status_code != 200:
        sys.exit(f"Could not list models (HTTP {r.status_code}): {r.text[:400]}")
    for m in r.json().get("data", []):
        print(m.get("id"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=list(PROVIDERS), default="gemini")
    parser.add_argument("--dataset", default="pilot")
    parser.add_argument("--condition", choices=["full", "bare"], default="full")
    parser.add_argument("--model", help="overrides the model name in settings.txt")
    parser.add_argument("--limit", type=int, default=0, help="only the first N claims (0 = all)")
    parser.add_argument("--list-models", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="print one prompt and stop")
    args = parser.parse_args()

    settings = load_settings()
    documents, facts, claims = load_dataset(args.dataset)
    if args.limit:
        claims = claims[:args.limit]

    if args.dry_run:
        system, user = build_prompt(claims[0], documents, args.condition)
        print("=== SYSTEM MESSAGE ===\n" + system + "\n\n=== USER MESSAGE ===\n" + user)
        print(f"\nCorrect answer for {claims[0]['case_id']}: {claims[0]['gold_label']}")
        return

    info = PROVIDERS[args.provider]
    if info["key"] and not settings.get(info["key"]):
        sys.exit(f"No {info['key']} in settings.txt. See README.md, section 'Get a free AI key'.")
    if args.list_models:
        list_models(args.provider, settings)
        return

    model = args.model or settings.get(info["model"])
    pause = float(settings.get("SECONDS_BETWEEN_CALLS", "5"))
    safe_model = re.sub(r"[^A-Za-z0-9.-]+", "-", model)
    out_csv = os.path.join(RESULTS_DIR, f"llm_{args.dataset}_{args.provider}_{safe_model}_{args.condition}.csv")
    fields = ["case_id", "family_id", "policy", "gold_label", "prediction", "reason", "raw"]
    done = {r["case_id"]: r for r in read_csv(out_csv)} if os.path.exists(out_csv) else {}

    results = dict(done)
    print(f"Model {model} via {args.provider}, condition '{args.condition}', {len(claims)} claims")
    for i, claim in enumerate(claims, 1):
        if claim["case_id"] in done and done[claim["case_id"]]["prediction"] != "invalid":
            continue
        system, user = build_prompt(claim, documents, args.condition)
        text = call_model(args.provider, settings, model, system, user)
        label, reason = parse_label(text)
        mark = "ok " if label == claim["gold_label"] else "MISS"
        print(f"  [{i}/{len(claims)}] {claim['case_id']:8s} correct={claim['gold_label']} model={label:7s} {mark}")
        results[claim["case_id"]] = {
            "case_id": claim["case_id"], "family_id": claim["family_id"], "policy": claim["policy"],
            "gold_label": claim["gold_label"], "prediction": label, "reason": reason,
            "raw": text.replace("\n", " ")[:500]}
        write_csv(out_csv, list(results.values()), fields)
        time.sleep(pause)

    rows = [results[c["case_id"]] for c in claims if c["case_id"] in results]
    write_csv(out_csv, rows, fields)
    stats = score(rows, "prediction")
    report = format_report(f"{model} ({args.provider}), condition '{args.condition}', dataset '{args.dataset}'", stats)
    print("\n" + report)
    with open(out_csv.replace(".csv", "_report.md"), "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Saved: {out_csv}")


if __name__ == "__main__":
    main()
