# Thirty-case pilot: evidence and decision record

26 October 2026. **Provisional, analyst-authored feasibility assessment; not measured model performance.**

## Decision

Continue with independent review and targeted acquisition. Keep the original proposal as the blueprint, but do not claim that a complex resolver is necessary or superior. The current cases motivate explicit authority, time, metric and precision contracts. A small withdrawal-aware extension to the strong simple baseline already matches the proposed reference logic on all 30 draft labels.

## Completed and pending

| Item | Status |
|---|---|
| Constructed claims | 30 drafts, six for each of five issuers |
| Independent correction families | Five, not 30 |
| Primary sources inspected | 11 SEC filings: five original annual reports, five corrective/revised annual reports, one contemporaneous non-reliance 8-K |
| Provenance | Document/index links, exact index acceptance displays, filing dates, retrieval dates and SHA-256 fingerprints |
| Numerical spot checks | 24 selected XBRL facts with context, period, dimensions, units, scale and precision; narrative/table locators accompany them |
| Draft label counts | 18 S, eight C, four U; descriptive only, not a target balance |
| Manual baseline trace | Complete; analyst-applied rules, not executable-model outputs |
| Independent human review, adjudication and annotation timing | Pending; review pack provided |
| Broader screening target | Five accepted families/five issuers acquired; 20-family/10-issuer gate unmet |
| Main experiment, statistical testing, held-out evaluation | Not started |

The 30 claims were constructed after viewing selected correction events. There is no random-sampling claim, screening yield estimate, natural misinformation prevalence estimate, or held-out split within this pilot. All five issuers remain excluded from the eventual main-study partitions.

## What the sources establish

The issuer-specific evidence records cite the original statements and correction notes; `source_manifest.csv` identifies exact accessions. At displayed precision, the selected changes are:

| Family | Selected reported figure, original → revised/restated | Interpretation issue |
|---|---|---|
| [Plug Power](evidence/PLUG-2019.md) | Net loss attributable to the Company: 85.465 → 83.743 million USD loss magnitude | Company attribution differs from common-stockholder attribution; investing cash outflow is unchanged |
| [Macy's](evidence/MACYS-2023.md) | Fiscal-2023 net income: 105 → 45 million USD | Issuer describes correction of immaterial misstatements; fiscal year ends in February 2024; net sales unchanged |
| [SunPower](evidence/SUNPOWER-2022.md) | Net income attributable to stockholders: 56.037 → 42.849 million USD | Contemporaneous non-reliance notice precedes the selected replacement; stockholder income differs from consolidated income |
| [Tupperware](evidence/TUPPERWARE-2021.md) | Fiscal-2021 net income: 18.6 → 15.6 million USD | Continuing-operations income is a different metric; displayed-value subtraction is not exact underlying-value arithmetic |
| [DZS](evidence/DZS-2022.md) | Fiscal-2022 net loss: 37.431 → 41.270 million USD loss magnitude | Fiscal-2021 loss is unchanged; narrative rounding differs from statement precision |

The SunPower 8-K was filed on 24 October 2023 and says the audit committee made its non-reliance determination on 19 October. Neither the committee date nor the filename establishes filing availability. The amended annual report was filed on 18 December. Under our packet-relative active-authority contract, the 25 October cutoff has an eligible withdrawal and no eligible replacement. This is a genuine sourced withdrawal event; the assignment of U follows the declared evaluation contract, not an assertion that every withdrawn number was wrong.

These packets do not contain every intervening public disclosure. Macy's selected annual report refers to an earlier corrective quarterly report. We do not claim to have found the first public correction for every issuer. Historical conclusions are explicitly packet-relative.

## Manual comparison

Rules are defined in [protocol_v1.md](protocol_v1.md); each manually assigned output is in [manual_baseline_trace.csv](manual_baseline_trace.csv). All use the same selected evidence and policy metadata. B1 ignores authority/time; B3 uses latest eligible numerical evidence; B4 also honors policy; B4+W additionally honors an explicit applicable withdrawal. The proposed reference resolver uses scoped authority/status reasoning.

| Analyst-applied rule | Disagreements with provisional key, out of 30 | Main reason |
|---|---:|---|
| B1 context-only | 18 | Unresolved conflicts despite a supplied authority/time policy |
| B3 cutoff-aware latest | 8 | Ignores original-as-filed intent, declared policy ambiguity and withdrawal status |
| B4 policy-aware latest | 1 | Retains a numerical figure after an eligible non-reliance notice |
| B4+W simple withdrawal-aware control | 0 | Handles the only extra status distinction in this packet set |
| Proposed scoped reference resolver | 0 | Same draft decisions as B4+W here |

These counts are agreement with a key drafted by the same analyst who applied the rules. They are **not independent accuracy estimates, trained-model results, or evidence of superiority**. B4+W was added after inspecting the cases; it is an exploratory stronger comparator. All rules share inspected semantic matches and numerical conventions, so extraction/retrieval errors are not tested. The baseline identifiers follow the proposal's family of controls; this pilot does not instantiate every proposed baseline.

No significance test is warranted. There are five issuer clusters, many paired claims, and no independently evaluated model outputs. For the proposal's paired exact sign-test logic, even five unanimous nonzero independent differences give a two-sided p-value of 2/2^5 = 0.0625. Six give 2/2^6 = 0.03125. Six is merely a minimum for the possibility of rejection at 0.05, not a power calculation or adequate study-size recommendation. The scoped resolver and B4+W have no observed manual decision differences here.

## Threats and corrective actions

- **Selection and confirmation bias:** purposive familiar correction events, constructed claims and one analyst. Obtain independent review and broaden screening; never treat paired variants as new families.
- **Contract dependence:** unspecified-policy ambiguity, conservative rounding intervals and active-authority semantics are design conventions. Ask reviewers to challenge them; document revisions before main-study annotation.
- **Incomplete history:** annual packets omit some intervening disclosures. Preserve the packet-relative restriction; collect the full relevant history before open-world historical claims.
- **Limited scope:** U cases cover policy ambiguity, a withdrawal gap and exactness; they do not establish comprehensive coverage of incomparable surviving sources, segment-specific changes or missing evidence.
- **Oracle interpretation:** numbers/context have been inspected. Raw-document extraction and end-to-end retrieval remain separate future conditions.
- **Novelty unresolved:** preliminary related-work inspection is not a completed current survey. A withdrawal flag alone does not justify a novel-algorithm claim.

## Next gates and negative-result path

1. Obtain a competent independent human first pass, preserving prior label exposure, source locators, actual time and disagreements. Adjudicate before calling any label gold.
2. Reach the broader 20-eligible-family/10-issuer screening target and record exclusions prospectively. Keep this pilot's issuers outside the main experiment.
3. Inspect closer released benchmarks and search for equivalent authority/withdrawal protocols. Record inaccessible releases rather than assuming they lack these cases.
4. Look for authentic fact-scoped corrections or incomparable authorities on which the strong control and proposed method could differ. Do not manufacture labels solely to defeat a baseline. A new example is a development case, not a fresh held-out test after inspection.
5. Freeze the contract, annotation procedure and strong comparators, then decide whether implementation and the full collection are feasible.

If stronger simple rules remain sufficient, write a benchmark/measurement study or a documented negative result about their adequacy, subject to a defensible literature gap and adequate evaluation. Do not add unrelated research directions to conceal a tie. If labels cannot be reliably reviewed or public evidence is too sparse, reduce the research claim and reconsider feasibility with the supervisor before expanding.
