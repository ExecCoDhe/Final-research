"""Automatically build correction families and claims from free SEC data.

Steps:
 1. SEC full-text search finds 8-K reports with Item 4.02 ("Non-Reliance on
    Previously Issued Financial Statements") in a date range.
 2. For each company, SEC Company Facts lists every annual net income (loss)
    figure and the filing that reported it. A period whose figure changed in a
    later 10-K or 10-K/A, with the non-reliance notice in between, becomes a
    correction family.
 3. Each family gets up to seven claims under the same policies as the pilot.
    Labels come from the scoped reference rules (verifier.py, rule P) and are
    "silver" labels: a person must spot-check a sample against the filings
    (see families.csv, columns check_*).

Usage:  python build_dataset.py [--target 40] [--max-companies 200]
"""

import argparse
import json
import os
import sys
import time
from datetime import date, timedelta
from decimal import Decimal

import requests

from common import CODE_DIR, DATA_DIR, load_settings, write_csv
from verifier import run_rule

CACHE_DIR = os.path.join(CODE_DIR, "cache")
SEARCH_URL = "https://efts.sec.gov/LATEST/search-index"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
PILOT_CIKS = {"0001093691", "0000794367", "0000867773", "0001008654", "0001101680"}
MAIN_CONCEPT = "NetIncomeLoss"
CONTROL_CONCEPTS = [
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "NetCashProvidedByUsedInInvestingActivities",
    "NetCashProvidedByUsedInFinancingActivities",
]
PAUSE = 0.5  # at most two requests per second, well under the SEC's limit of ten


class Sec:
    def __init__(self, email):
        if not email or "@" not in email:
            sys.exit("Put your email in code/settings.txt (SEC_EMAIL=...). The SEC requires it.")
        self.headers = {"User-Agent": f"DTU BTech research project {email}"}

    def get_json(self, url, params=None):
        for attempt in range(5):
            time.sleep(PAUSE)
            try:
                r = requests.get(url, params=params, headers=self.headers, timeout=60)
            except requests.RequestException:
                time.sleep(2 * (attempt + 1))
                continue
            if r.status_code == 404:
                return None
            if r.status_code == 200:
                try:
                    data = r.json()
                except ValueError:
                    data = None
                if data is not None and "errorType" not in data:
                    return data
            time.sleep(2 * (attempt + 1))
        return None


def find_non_reliance_notices(sec, start, end, max_hits):
    """Return {cik: {"name", "notices": [(file_date, accession, url)]}}."""
    companies = {}
    offset = 0
    while offset < max_hits:
        data = sec.get_json(SEARCH_URL, {
            "q": '"should no longer be relied upon"', "forms": "8-K",
            "dateRange": "custom", "startdt": start, "enddt": end, "from": offset})
        if not data:
            break
        hits = data["hits"]["hits"]
        if not hits:
            break
        for hit in hits:
            src = hit["_source"]
            if "4.02" not in (src.get("items") or []):
                continue
            if "6770" in (src.get("sics") or []):  # blank-check shell companies (SPACs)
                continue
            name = (src.get("display_names") or ["?"])[0].split("  (")[0].strip()
            if "acquisition corp" in name.lower():
                continue
            cik = src["ciks"][0]
            if cik in PILOT_CIKS:
                continue
            accession = src["adsh"]
            filename = hit["_id"].split(":", 1)[1]
            url = (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
                   f"{accession.replace('-', '')}/{filename}")
            entry = companies.setdefault(cik, {"name": name, "notices": []})
            if all(n[1] != accession for n in entry["notices"]):
                entry["notices"].append((src["file_date"], accession, url))
        offset += len(hits)
        print(f"  searched {offset} of {data['hits']['total']['value']} notices; "
              f"{len(companies)} companies kept so far")
        if offset >= data["hits"]["total"]["value"]:
            break
    return companies


def company_facts(sec, cik):
    """Return the annual USD facts for the concepts we use, cached on disk."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{cik}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    data = sec.get_json(FACTS_URL.format(cik=cik))
    keep = {"entityName": None, "concepts": {}}
    if data:
        keep["entityName"] = data.get("entityName")
        gaap = data.get("facts", {}).get("us-gaap", {})
        for concept in [MAIN_CONCEPT] + CONTROL_CONCEPTS:
            if concept in gaap and "USD" in gaap[concept].get("units", {}):
                annual = [f for f in gaap[concept]["units"]["USD"]
                          if f.get("start") and 350 <= days(f["start"], f["end"]) <= 380]
                keep["concepts"][concept] = {"label": gaap[concept].get("label") or concept,
                                             "facts": annual}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(keep, f)
    return keep


def days(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def next_day(d):
    return (date.fromisoformat(d) + timedelta(days=1)).isoformat()


def common_step(*values):
    """Largest power of ten (up to one million USD) dividing every value, in USD millions."""
    for exponent, step in ((6, "1"), (5, "0.1"), (4, "0.01"), (3, "0.001")):
        if all(int(v) % (10 ** exponent) == 0 for v in values):
            return Decimal(step)
    return None


def to_millions(value, step):
    return (Decimal(int(value)) / Decimal(1_000_000)).quantize(step)


def find_family(facts, notices):
    """Pick the most recent fiscal year whose net income changed in a later
    annual filing, with a non-reliance notice filed between the two."""
    concept = facts["concepts"].get(MAIN_CONCEPT)
    if not concept:
        return None
    periods = {}
    for f in concept["facts"]:
        periods.setdefault((f["start"], f["end"]), []).append(f)
    candidates = []
    for (start, end), entries in periods.items():
        entries.sort(key=lambda f: f["filed"])
        originals = [f for f in entries if f.get("form") == "10-K"]
        if not originals:
            continue
        original = originals[0]
        for later in entries:
            if later["filed"] <= original["filed"] or later.get("form") not in ("10-K", "10-K/A"):
                continue
            old, new = int(original["val"]), int(later["val"])
            if old == new or abs(new - old) < 0.005 * max(abs(old), 1):
                continue
            # A change of more than 3x usually means a merger or a change of
            # reporting entity rather than an error correction.
            if max(abs(old), abs(new)) > 3 * max(min(abs(old), abs(new)), 1):
                continue
            step = common_step(old, new)
            if step is None or abs(new - old) < 2 * step * 1_000_000:
                continue
            between = sorted(n for n in notices if original["filed"] < n[0] < later["filed"])
            if not between:
                continue
            candidates.append({"start": start, "end": end, "original": original,
                               "corrected": later, "notice": between[0], "step": step})
            break
    if not candidates:
        return None
    return max(candidates, key=lambda c: c["end"])


def find_control(facts, family):
    """A second figure for the same year that both filings report identically."""
    for concept in CONTROL_CONCEPTS:
        info = facts["concepts"].get(concept)
        if not info:
            continue
        same_period = [f for f in info["facts"]
                       if f["start"] == family["start"] and f["end"] == family["end"]]
        old = [f for f in same_period if f["accn"] == family["original"]["accn"]]
        new = [f for f in same_period if f["accn"] == family["corrected"]["accn"]]
        if old and new and int(old[0]["val"]) == int(new[0]["val"]):
            step = common_step(int(old[0]["val"]))
            if step is not None:
                return {"concept": concept, "label": info["label"], "val": int(old[0]["val"]), "step": step}
    return None


def money(value_musd):
    if value_musd < 0:
        return f"a net loss of USD {abs(value_musd)} million"
    return f"net income of USD {value_musd} million"


def index_url(cik, accession):
    return (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
            f"{accession.replace('-', '')}/{accession}-index.html")


def build_family_records(n, cik, name, fam, control):
    fid = f"A{n:03d}"
    orig, corr, notice = fam["original"], fam["corrected"], fam["notice"]
    step = fam["step"]
    v_old, v_new = to_millions(orig["val"], step), to_millions(corr["val"], step)
    period = f"{fam['start']} to {fam['end']}"
    metric = "Net income (loss)"

    docs = [
        {"doc_id": f"{fid}-O", "family_id": fid, "issuer": name, "cik": cik, "form": "10-K",
         "accession": orig["accn"], "filing_date": orig["filed"], "url": index_url(cik, orig["accn"]),
         "doc_type": "numeric_report", "withdraws_doc_ids": "",
         "evidence_text": f"Annual report (Form 10-K) covering the fiscal year {period}. "
                          f"It reports {money(v_old)} for that fiscal year."
                          + (f" It reports {control['label']} of USD {to_millions(control['val'], control['step'])} million."
                             if control else "")},
        {"doc_id": f"{fid}-W", "family_id": fid, "issuer": name, "cik": cik, "form": "8-K",
         "accession": notice[1], "filing_date": notice[0], "url": notice[2],
         "doc_type": "non_reliance_notice", "withdraws_doc_ids": f"{fid}-O",
         "evidence_text": "Current report (Form 8-K), Item 4.02 Non-Reliance on Previously Issued "
                          "Financial Statements: the company states that previously issued financial "
                          "statements, including the annual report above, should no longer be relied upon. "
                          "No corrected amounts are given in this report."},
        {"doc_id": f"{fid}-R", "family_id": fid, "issuer": name, "cik": cik, "form": corr["form"],
         "accession": corr["accn"], "filing_date": corr["filed"], "url": index_url(cik, corr["accn"]),
         "doc_type": "numeric_report", "withdraws_doc_ids": "",
         "evidence_text": ("Amended annual report (Form 10-K/A)" if corr["form"] == "10-K/A"
                           else "Later annual report (Form 10-K) with comparative columns")
                          + f" covering the fiscal year {period}. It reports {money(v_new)} for that fiscal "
                            f"year, a corrected figure that replaces the amount originally reported."
                          + (f" It reports {control['label']} of USD {to_millions(control['val'], control['step'])} million."
                             if control else "")},
    ]
    facts = [
        {"fact_id": f"{fid}-F1", "family_id": fid, "doc_id": f"{fid}-O", "metric": metric,
         "period_start": fam["start"], "period_end": fam["end"], "value": str(v_old), "step": str(step),
         "unit": "USD million (negative = loss)", "role": "original", "replaces_fact_id": ""},
        {"fact_id": f"{fid}-F2", "family_id": fid, "doc_id": f"{fid}-R", "metric": metric,
         "period_start": fam["start"], "period_end": fam["end"], "value": str(v_new), "step": str(step),
         "unit": "USD million (negative = loss)", "role": "corrected", "replaces_fact_id": f"{fid}-F1"},
    ]
    if control:
        cv = to_millions(control["val"], control["step"])
        for k, doc in (("F3", "O"), ("F4", "R")):
            facts.append({"fact_id": f"{fid}-{k}", "family_id": fid, "doc_id": f"{fid}-{doc}",
                          "metric": control["label"], "period_start": fam["start"], "period_end": fam["end"],
                          "value": str(cv), "step": str(control["step"]), "unit": "USD million",
                          "role": "original" if doc == "O" else "corrected",
                          "replaces_fact_id": f"{fid}-F3" if doc == "R" else ""})

    packet = "+".join(d["doc_id"] for d in docs)
    after_fix = next_day(corr["filed"])
    year = f"the fiscal year ending {fam['end']}"
    templates = [
        ("original_as_filed", after_fix, v_old, "original_as_filed_old_value", "S",
         f"In its original annual report for {year}, {name} reported {money(v_old)}."),
        ("corrected_named", after_fix, v_old, "corrected_old_value", "C",
         f"According to the corrected figures, {name} had {money(v_old)} for {year}."),
        ("as_known_packet", next_day(orig["filed"]), v_new, "before_correction_new_value", "C",
         f"Based on the reliable filings available at the time, {name} had {money(v_new)} for {year}."),
        ("as_known_packet", after_fix, v_new, "after_correction_new_value", "S",
         f"Based on the reliable filings available at the time, {name} had {money(v_new)} for {year}."),
        ("unspecified", after_fix, v_old, "unspecified_old_value", "U",
         f"{name} reported {money(v_old)} for {year}."),
    ]
    if next_day(notice[0]) <= corr["filed"]:
        templates.append(("as_known_packet", next_day(notice[0]), v_old, "withdrawal_gap_old_value", "U",
                          f"Based on the reliable filings available at the time, {name} had {money(v_old)} for {year}."))
    claims = []
    for i, (policy, cutoff, value, template, expected, text) in enumerate(templates, 1):
        claims.append({"case_id": f"{fid}-{i}", "family_id": fid, "issuer": name, "metric": metric,
                       "period_start": fam["start"], "period_end": fam["end"], "claim": text,
                       "policy": policy, "cutoff_date": cutoff, "packet": packet,
                       "claimed_value": str(value), "claim_step": str(step), "operand_metric": "",
                       "operand_new": "", "operand_old": "", "gold_label": "",
                       "label_source": "silver_rule_P", "template": template, "expected": expected})
    if control:
        cv = to_millions(control["val"], control["step"])
        claims.append({"case_id": f"{fid}-{len(claims) + 1}", "family_id": fid, "issuer": name,
                       "metric": control["label"], "period_start": fam["start"], "period_end": fam["end"],
                       "claim": f"According to the corrected figures, {name}'s {control['label']} for {year} "
                                f"was USD {cv} million.",
                       "policy": "corrected_named", "cutoff_date": after_fix, "packet": packet,
                       "claimed_value": str(cv), "claim_step": str(control["step"]), "operand_metric": "",
                       "operand_new": "", "operand_old": "", "gold_label": "",
                       "label_source": "silver_rule_P", "template": "unchanged_control", "expected": "S"})

    family_row = {"family_id": fid, "issuer": name, "cik": cik, "period_start": fam["start"],
                  "period_end": fam["end"], "original_accession": orig["accn"], "original_filed": orig["filed"],
                  "original_value_musd": str(v_old), "notice_filed": notice[0], "notice_url": notice[2],
                  "corrected_form": corr["form"], "corrected_accession": corr["accn"],
                  "corrected_filed": corr["filed"], "corrected_value_musd": str(v_new),
                  "original_url": index_url(cik, orig["accn"]), "corrected_url": index_url(cik, corr["accn"]),
                  "control_metric": control["label"] if control else "",
                  "flag": ("large change (over 30%): confirm it is an error correction, not a merger or "
                           "reclassification" if abs(v_new - v_old) > Decimal("0.3") * abs(v_old) else ""),
                  "check_original_value": "", "check_corrected_value": "", "check_notice_covers_year": "",
                  "checked_by": "", "check_notes": ""}
    return docs, facts, claims, family_row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2019-01-01")
    parser.add_argument("--end", default="2024-12-31")
    parser.add_argument("--target", type=int, default=40, help="number of companies (families) to collect")
    parser.add_argument("--max-companies", type=int, default=250, help="companies to inspect at most")
    parser.add_argument("--max-hits", type=int, default=4000, help="search results to read at most")
    args = parser.parse_args()

    sec = Sec(load_settings().get("SEC_EMAIL"))
    print("Step 1: searching SEC for non-reliance notices (Form 8-K Item 4.02)...")
    companies = find_non_reliance_notices(sec, args.start, args.end, args.max_hits)
    order = sorted(companies, key=lambda c: max(n[0] for n in companies[c]["notices"]), reverse=True)

    print(f"\nStep 2: checking up to {args.max_companies} companies for changed annual net income...")
    all_docs, all_facts, all_claims, families, skipped = [], [], [], [], []
    for inspected, cik in enumerate(order[:args.max_companies], 1):
        facts = company_facts(sec, cik)
        name = " ".join((facts.get("entityName") or companies[cik]["name"]).split())
        fam = find_family(facts, companies[cik]["notices"])
        if not fam:
            skipped.append({"cik": cik, "issuer": name, "reason": "no annual net-income change bracketing a notice"})
            continue
        control = find_control(facts, fam)
        docs, fact_rows, claims, family_row = build_family_records(len(families) + 1, cik, name, fam, control)
        all_docs += docs
        all_facts += fact_rows
        all_claims += claims
        families.append(family_row)
        print(f"  [{inspected}] family {family_row['family_id']}: {name} {fam['end']} "
              f"{family_row['original_value_musd']} -> {family_row['corrected_value_musd']} USD million")
        if len(families) >= args.target:
            break

    print("\nStep 3: labelling claims with the scoped reference rules...")
    documents = {d["doc_id"]: d for d in all_docs}
    facts_typed = [dict(f, value=Decimal(f["value"]), step=Decimal(f["step"])) for f in all_facts]
    kept = []
    for claim in all_claims:
        typed = dict(claim, claimed_value=Decimal(claim["claimed_value"]),
                     claim_step=Decimal(claim["claim_step"]), packet_ids=claim["packet"].split("+"))
        label = run_rule("P", typed, documents, facts_typed)
        if label != claim["expected"]:
            print(f"  dropped {claim['case_id']}: rule gives {label}, template expects {claim['expected']}")
            continue
        claim["gold_label"] = label
        kept.append(claim)

    out = os.path.join(DATA_DIR, "auto")
    write_csv(os.path.join(out, "documents.csv"), all_docs)
    write_csv(os.path.join(out, "facts.csv"), all_facts)
    write_csv(os.path.join(out, "claims.csv"), kept)
    write_csv(os.path.join(out, "families.csv"), families)
    write_csv(os.path.join(out, "skipped_companies.csv"), skipped, ["cik", "issuer", "reason"])
    counts = {lab: sum(c["gold_label"] == lab for c in kept) for lab in "SCU"}
    print(f"\nDone: {len(families)} companies, {len(kept)} claims "
          f"(S={counts['S']}, C={counts['C']}, U={counts['U']}). Files are in {out}")
    print("Next: open families.csv and spot-check some families against the SEC links (columns check_*).")


if __name__ == "__main__":
    main()
