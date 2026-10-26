# Pilot protocol v1 — 26 October 2026

This operationalizes the existing proposal; the 44-page proposal is unchanged. This is a **retrospective, constructed-claim, manually checked feasibility pilot**, not a preregistered test of a trained model. The protocol was refined while inspecting these examples. No held-out performance claim is permitted.

## Sample and evidence contract

Thirty claims, six per issuer, span five correction events: Plug Power, Macy's, SunPower, Tupperware, and DZS. Multiple years, line items, or quarterly statements in one correction event are not counted as additional independent families. All five issuers are reserved for pilot/development-of-instructions purposes and excluded from the proposed main experiment.

Each case identifies a reporting interval, a metric/caption, the same evidence packet for all rules, an authority policy, and a conservative day-level cutoff. The packet can contain later documents, but an as-known rule must discard ineligible documents before reasoning. This controlled packet is **not a complete historical disclosure search**. “As-known” means as-known within the supplied eligible packet, not everything the market knew.

Source IDs and exact SEC index acceptance strings appear in `source_manifest.csv`. Acceptance, official filing date, public dissemination, and our retrieval date are distinct. Except for separately documented SunPower API UTC timestamps, index timestamps are preserved as displayed without assigning an unsupported timezone. A document is conservatively eligible only on calendar dates after its official filing date. There are no intraday claims. This avoids relying on an acceptance timestamp to prove the precise public-release time.

### Authority policies

- `original_as_filed`: use the original named accession's reported figure. A later withdrawal does not erase the historical fact that the original document reported that figure.
- `corrected_named`: use the specified later disclosure's current corrected/revised column, not its historical “previously reported” column.
- `as_known_packet`: restrict by the cutoff, honor eligible correction and non-reliance notices, and use an active authoritative figure. If the only relevant statement has been withdrawn and no eligible replacement is present, the amount is underdetermined.
- `unspecified`: consider both original-as-filed and corrected-state interpretations allowed by the evaluation contract. Divergence gives U. This is an explicit benchmark ambiguity convention; it is not a claim that every reader would interpret such wording ambiguously.
- `explicit_display_comparison`: compare the two named disclosed point values using the stated calculation. This does not assert the difference between exact unrounded economic quantities.

### Labels and precision

S = supported under the policy and packet; C = incompatible positive evidence under that contract; U = insufficient/ambiguous evidence. Missing evidence does not establish C. A human's inability to finish review is `needs_source` or `needs_expert` in the review-status field, not automatically a semantic U label.

Most cases ask about **displayed reported figures**. A quoted displayed value is distinguished from the unknown exact underlying amount. P018 explicitly asks about an unrounded amount: SunPower's USD-thousands precision gives a conservative interval [42,848,500, 42,849,500] USD around the displayed 42,849,000 USD. The exact singleton is not established, so the proposed label is U. This is a design convention subject to reviewer challenge.

Loss/outflow magnitudes in claim wording are positive; the source's signed numerical facts are negative. Macy's fiscal 2023 runs 2023-01-29 through 2024-02-03; it is not calendar 2023. SunPower's selected metric is net income **attributable to stockholders**, not consolidated net income before noncontrolling interests.

Retain economic dimensions (segment, geography, ownership scope). Restatement-scenario members such as `ScenarioPreviouslyReportedMember` are explicitly mapped to authority roles only when the source table confirms that role. Do not silently discard all dimensions. `fact_spotchecks.csv` records the exact inspected facts, context IDs, dimensions and precision.

## Manual baseline specifications

These are **analyst-applied reference rules**, not executed models or reproductions of published systems. All receive the same packet and policy. The analyst also drafted the labels, so the comparison is not independent validation.

| Rule | Behavior |
|---|---|
| B1: context-only | Match the economic metric/period/unit and compare all original/current point values in the packet, without time/authority selection. Agreement supports or contradicts; conflicting values give U. Explicit two-document arithmetic and precision use the common numerical rules. |
| B3: cutoff-aware latest | Discard future documents; choose the latest eligible numerical fact. Defaults to latest for unspecified policy and ignores original-as-filed intent and non-reliance status. This is an intentionally limited control, not the strongest competitor. |
| B4: policy-aware latest | Honor named original/corrected accessions and unspecified-policy ambiguity; otherwise choose the latest eligible numerical fact. It does not revoke a numerical fact based on a non-numerical withdrawal notice. |
| B4+W: simple withdrawal-aware control | B4 plus a reviewed status flag for an explicit eligible non-reliance notice covering the metric/period. With no active replacement, return U. Added during pilot construction to avoid crediting the proposal for a capability a small baseline extension supplies. |
| P: proposed reference resolver | Apply scoped correction/status relations and all interpretation/precision rules. On this small packet set its decisive logic may coincide with B4+W; this is not concealed. |

No confidence scores, risk–coverage curves, latency, implementation accuracy, or statistical significance are estimated from this manual exercise. Five issuer clusters do not meet even the six-nonzero-pair minimum for the stated two-sided exact sign test at 5%; 30 related claims do not create 30 independent units.

## Review and versioning

The sole authoritative current case file is `pilot_cases_draft.csv`. The older `first_family_claims.csv` is retained for link continuity; its six cases are included, not additional observations. The reviewer gets `reviewer_pack.zip`, which omits draft labels, analyst reasons, and manual baseline outputs. Blinding is procedural: the public repository contains those other files, and any prior exposure must be declared.

Freeze an independent review copy before comparing labels. Preserve original reviewer answers, proposed revisions, and adjudication reasons. Corrections produce a versioned dataset and updated analysis, not overwritten evidence of agreement. An unresolved substantive ambiguity remains U or is excluded with a reason; it is not forced into a preferred class.

## Gates

The 30-draft-claim/five-issuer acquisition target is reached. Independent review, observed annotation time, agreement, and final labels remain pending. The proposal's broader 20-eligible-family/10-issuer screening target remains unmet: this pilot has five families across five issuers, not 20. No go-ahead for the full 600-claim study follows automatically.
