"""Rule-based verifiers for policy- and time-conditioned financial claims.

Labels: S = supported, C = contradicted, U = underdetermined.

Rules (see pilot/protocol_v1.md):
  B1   context-only: every matching figure in the packet, ignoring time and policy.
  B3   cutoff-aware latest: newest figure filed before the cutoff, ignoring policy.
  B4   policy-aware latest: honours original/corrected/unspecified policies;
       otherwise newest eligible figure. Ignores non-reliance notices.
  B4W  B4 plus a withdrawal flag: an eligible non-reliance notice covering the
       selected figure, with no eligible replacement, gives U.
  P    scoped reference resolver: applies cutoff, explicit corrections and
       withdrawals to build the set of active figures, then judges every
       admissible interpretation.
"""

from decimal import Decimal

RULES = ["B1", "B3", "B4", "B4W", "P"]
HALF = Decimal("0.5")


def fact_interval(fact):
    half = fact["step"] * HALF
    return (fact["value"] - half, fact["value"] + half)


def claim_interval(claim):
    half = claim["claim_step"] * HALF
    return (claim["claimed_value"] - half, claim["claimed_value"] + half)


def judge(intervals, claim):
    """S if every interpretation lies inside the claim, C if every one lies
    outside it, U otherwise (including when there is no interpretation)."""
    if not intervals:
        return "U"
    lo_c, hi_c = claim_interval(claim)
    if all(lo_c <= lo and hi <= hi_c for lo, hi in intervals):
        return "S"
    if all(hi < lo_c or lo > hi_c for lo, hi in intervals):
        return "C"
    return "U"


def eligible(doc, cutoff):
    """A document counts only on calendar days after its official filing date."""
    return doc["filing_date"] < cutoff


class Packet:
    """The evidence a claim may use: documents named in its packet and the
    figures they report for the claim's metric and period."""

    def __init__(self, claim, documents, facts):
        self.claim = claim
        self.docs = {d: documents[d] for d in claim["packet_ids"]}
        metric = claim.get("operand_metric") or claim["metric"]
        self.facts = [
            f for f in facts
            if f["doc_id"] in self.docs
            and f["metric"] == metric
            and f["period_start"] == claim["period_start"]
            and f["period_end"] == claim["period_end"]
            and f["role"] in ("original", "corrected")
        ]
        self.notices = [d for d in self.docs.values() if d["doc_type"] == "non_reliance_notice"]

    def by_role(self, role):
        return [f for f in self.facts if f["role"] == role]

    def eligible_facts(self, cutoff):
        return [f for f in self.facts if eligible(self.docs[f["doc_id"]], cutoff)]

    def latest(self, facts):
        if not facts:
            return []
        newest = max(self.docs[f["doc_id"]]["filing_date"] for f in facts)
        return [f for f in facts if self.docs[f["doc_id"]]["filing_date"] == newest]

    def withdrawn_doc_ids(self, cutoff):
        withdrawn = set()
        for notice in self.notices:
            if eligible(notice, cutoff):
                withdrawn.update(x for x in notice["withdraws_doc_ids"].split(";") if x)
        return withdrawn

    def active_facts(self, cutoff):
        """Eligible figures that are neither replaced by an eligible correction
        nor withdrawn by an eligible non-reliance notice."""
        pool = self.eligible_facts(cutoff)
        replaced = {f["replaces_fact_id"] for f in pool if f.get("replaces_fact_id")}
        withdrawn = self.withdrawn_doc_ids(cutoff)
        return [f for f in pool if f["fact_id"] not in replaced and f["doc_id"] not in withdrawn]

    def display_difference(self):
        """Displayed-value arithmetic for explicit two-document comparisons."""
        claim = self.claim
        new = [f for f in self.facts if f["doc_id"] == claim["operand_new"]]
        old = [f for f in self.facts if f["doc_id"] == claim["operand_old"]]
        if len(new) != 1 or len(old) != 1:
            return []
        point = new[0]["value"] - old[0]["value"]
        return [(point, point)]


def intervals(facts):
    return [fact_interval(f) for f in facts]


def run_rule(rule, claim, documents, facts):
    packet = Packet(claim, documents, facts)
    policy = claim["policy"]
    cutoff = claim["cutoff_date"]

    if policy == "explicit_display_comparison":
        return judge(packet.display_difference(), claim)

    if rule == "B1":
        return judge(intervals(packet.facts), claim)

    if rule == "B3":
        return judge(intervals(packet.latest(packet.eligible_facts(cutoff))), claim)

    original = packet.by_role("original")
    corrected = packet.by_role("corrected")
    latest_eligible = packet.latest(packet.eligible_facts(cutoff))

    if rule in ("B4", "B4W"):
        if policy == "original_as_filed":
            return judge(intervals(original), claim)
        if policy == "corrected_named":
            return judge(intervals(corrected), claim)
        if policy == "unspecified":
            return judge(intervals(original + latest_eligible), claim)
        if policy == "as_known_packet":
            if rule == "B4W":
                withdrawn = packet.withdrawn_doc_ids(cutoff)
                if any(f["doc_id"] in withdrawn for f in latest_eligible):
                    return "U"
            return judge(intervals(latest_eligible), claim)
        raise ValueError(f"Unknown policy {policy}")

    if rule == "P":
        if policy == "original_as_filed":
            return judge(intervals([f for f in original if eligible(packet.docs[f["doc_id"]], cutoff)]), claim)
        if policy == "corrected_named":
            return judge(intervals([f for f in corrected if eligible(packet.docs[f["doc_id"]], cutoff)]), claim)
        if policy == "as_known_packet":
            return judge(intervals(packet.active_facts(cutoff)), claim)
        if policy == "unspecified":
            interpretations = original + packet.active_facts(cutoff)
            return judge(intervals(interpretations), claim)
        raise ValueError(f"Unknown policy {policy}")

    raise ValueError(f"Unknown rule {rule}")


def run_all_rules(claims, documents, facts):
    rows = []
    for claim in claims:
        row = {"case_id": claim["case_id"], "family_id": claim["family_id"],
               "policy": claim["policy"], "gold_label": claim["gold_label"]}
        for rule in RULES:
            row[rule] = run_rule(rule, claim, documents, facts)
        rows.append(row)
    return rows
