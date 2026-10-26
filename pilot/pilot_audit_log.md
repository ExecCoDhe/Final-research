# Pilot evidence and construction audit

26 October 2026. This supplements the original proposal's audit; it does not replace it. The findings below concern the current five-family pilot. Sources are identified in `source_manifest.csv` and the issuer evidence records. Independent review remains pending.

| Issue found during construction/checking | Resolution in current package |
|---|---|
| Earlier pilot status described one issuer/six claims | Replaced with five issuers/30 draft claims; retained the old six-case file as a historical subset, not extra data |
| SEC acceptance display, official filing date and research retrieval date can differ | Preserve each separately; do not label the index display UTC; SunPower UTC values separately cross-checked against SEC submissions API |
| Plug's original report and SunPower's original report were accepted on the preceding displayed date | Eligibility uses dates after official filing, not the preceding acceptance display |
| SunPower filename uses 20231018 and committee decision is 19 October, while filing date is 24 October | Use official 24 October filing for day-level eligibility; record other dates only in their proper roles |
| A later retrospective correction note alone cannot establish contemporaneous non-reliance | Retrieved SunPower's original 8-K Item 4.02 and its filing index; included it as SPW |
| SunPower stockholder income differs from consolidated net income | Select the exact stockholder row: 56,037 to 42,849 thousand; do not substitute 60,463 to 47,275 thousand |
| Plug company-attributable loss differs from common-stockholder-attributable loss | Select the Company caption; reject substitution of the corrected common-stockholder row |
| Tupperware continuing-operations income differs from total net income | Preserve both row identities; 151.0 million is not selected total net income of 15.6 million |
| Macy's selected fiscal-2023 year is not calendar 2023 | Record exact interval 2023-01-29 to 2024-02-03 and 53-week context |
| Macy's calls the errors immaterial and refers to an earlier quarterly revision | Describe a revision for issuer-described immaterial misstatements; do not call M1 the first correction or automatically a material restatement |
| DZS and Plug contain duplicate facts/coarser rounded narrative renderings | Deduplicate identical occurrences and select statement precision; do not treat 37.4 vs 37.431 million, or 14.2 vs 14.244 million, as independent conflicting versions |
| Restatement scenario dimensions can be mistaken for new economic scopes | Preserve exact dimensions; map previously-reported/adjustment roles using reconciliation columns; do not indiscriminately drop dimensions |
| Displayed rounded amounts do not establish exact underlying equality | Distinguish reported-value claims from exact-unrounded claims; use a declared conservative interval convention and invite reviewer challenge |
| Loss magnitudes are positive in wording while signed XBRL values are negative | Explicitly document sign conversion and verify reconciliation arithmetic |
| Simple latest-number control understates what a strong baseline can handle | Add B4+W after inspection and disclose its exploratory origin; report its tie with the proposed reference resolver |
| Same analyst drafted key and manually applied rules | Call the comparison a reference-rule trace, not model accuracy, human agreement or independent validation |
| Five correction events yield 30 related variants | Count five issuer clusters; no claim-level independence or significance test |
| Public repository exposes proposed answers | Separate neutral review pack; require reviewer declaration of prior exposure; no automatic claim of blinding |
| Source evidence notes contain interpretive conclusions | Exclude those notes and protocol examples from the first-pass pack; provide neutral locators and general instructions instead |
| Broader history and screening are incomplete | Explicit packet-relative interpretation and five-family count; keep the 20-family/10-issuer gate pending |

## Arithmetic and structural checks

The inspected reconciliations are -85,465 + 1,722 = -83,743 (Plug, USD thousands), 56,037 - 13,188 = 42,849 (SunPower stockholder income, USD thousands), 18.6 - 3.0 = 15.6 (Tupperware, USD millions), and -37,431 - 3,839 = -41,270 (DZS, USD thousands). Macy's displayed difference is 45 - 105 = -60 million USD; that subtraction is not presented as a standalone full reconciliation of its revision causes.

Structural validation checks 30 unique case IDs, six cases per family, all source IDs resolving, 18/8/4 provisional S/C/U counts, aligned manual traces, and blank reviewer labels. Numeric spot checks preserve the selected raw facts and contexts. Source hashes fingerprint inspected downloaded bytes; they do not imply that full documents are bundled or that future mutable API responses will have the same hash.

No human review, model run, runtime benchmark, annotation-cost observation or statistical significance result is claimed. Archive validation checks file integrity and review-pack separation; it does not validate the research hypotheses.
