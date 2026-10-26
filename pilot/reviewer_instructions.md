# Independent review instructions

Version 1, 26 October 2026. This is a constructed-claim feasibility pilot. Your task is to evaluate claims against specified public disclosures and a declared interpretation policy. The research team's proposed answers are deliberately absent from this pack.

## Before opening the worksheet

Use an alias such as R1; do not enter personal contact details. Record whether you have already seen any draft labels, analyst explanations, or baseline outputs. The repository is public, so receiving this pack does not by itself establish blinding. Avoid the other repository files until you have submitted your first review. You may consult the original SEC documents linked in `source_manifest.csv` and the neutral locators in `source_cards.md`.

Financial-statement reading competence is needed. If a source is inaccessible or a concept exceeds your expertise, record `needs_source` or `needs_expert` and leave the verdict blank. A difficulty completing review is different from a claim whose evidence is genuinely insufficient.

## Evidence contract

Only the documents listed in a case's `packet` determine its label. This is a controlled packet, not a complete reconstruction of public knowledge. You may flag an important missing document, but do not silently add it and change the evidence universe. Source IDs identify exact accessions. A later disclosure's “previously reported” column is historical evidence, not its current corrected value.

Use the metric's statement caption, attribution scope, reporting interval, currency, scale and precision. Fiscal-year names need not equal calendar-year dates. A loss/outflow claim uses a positive magnitude although the corresponding signed income/cash-flow fact is negative. Preserve segment and other economic dimensions. Scenario dimensions in explicit correction tables identify original and adjustment columns; do not mistake them for new companies or independent observations.

For every policy, documents are eligible only if their official SEC filing date is **earlier than** the case cutoff date. This deliberately conservative day-level convention avoids intraday dissemination assumptions. The filename, the audit committee's decision date, the index acceptance display and the date we retrieved a document are not interchangeable. The selected named accessions in the original/corrected/comparison cases are all eligible under this convention.

| Policy | Interpretation |
|---|---|
| `original_as_filed` | What the earlier named accession reported, even if it was subsequently corrected or withdrawn. |
| `corrected_named` | What the specified later accession's revised/restated current column reports for this period. Do not substitute its “previously reported” column. |
| `as_known_packet` | The active authoritative statement within the eligible packet. Honor explicit eligible non-reliance notices covering the statement; a withdrawn figure without an eligible replacement cannot establish the authoritative amount. |
| `unspecified` | Consider both original-as-filed and corrected-state interpretations. This benchmark deliberately treats a divergence between them as ambiguity; flag objections to this convention separately. |
| `explicit_display_comparison` | Perform the stated arithmetic on the two named displayed numbers. This concerns disclosed point values, not exact unrounded underlying economic quantities. |

## Labels

- **S (supported):** the eligible evidence establishes the claim under the selected policy.
- **C (contradicted):** incompatible positive evidence establishes a conflicting value or proposition under that policy. Missing evidence alone does not establish C.
- **U (underdetermined):** the supplied evidence or allowed interpretations do not establish either S or C.

Most claims concern displayed reported numbers. A claim about an **exact unrounded amount** is stronger. Under the pilot's conservative rounding convention, a value displayed to quantum q represents an interval with half-width q/2; it does not establish a single exact underlying value. For XBRL `decimals=d`, q is 10 to the power -d in the base currency unit; inline `scale` determines conversion of displayed digits to base units. Include both endpoints conservatively. Challenge this convention in the notes if the original source specifies a different rounding rule.

## Complete each row

1. Read `claim`, `policy`, `cutoff_date`, metric and exact period together. Do not label from a matching number alone.
2. Open the source documents. Check the statement caption, year column, units, correction note and any applicable non-reliance notice. Source cards are navigation aids, not substitutes for the filings.
3. Fill `review_label` with S, C or U only when you can complete the assessment. In `source_ids_and_locator`, record source ID plus statement/note/row/year; a URL alone is insufficient.
4. Record the actual period and units you checked, any arithmetic, and a short reason. Mark `review_status=complete`, `needs_source`, `needs_expert`, or `needs_contract_clarification`.
5. Measure actual review time. Put initial packet-reading time in `review_session_log.csv`; put incremental per-case time in the worksheet. Do not count the same reading time repeatedly. State interruptions or shared-reading effects.
6. Save your first-pass file before seeing the proposed key. Send it privately to the project owner. Keep disagreements intact; adjudication happens afterwards.

The worksheet has 30 rows but only five issuer/correction families. Do not regard related claims as independent replications. No requested label distribution, desired accuracy or system result is supplied. Your task is to challenge errors as well as confirm claims.

## After submission

The project owner will compare your review with the draft key, preserve both originals and create an adjudication record. The draft key was assistant-authored, so this is a human review of an assistant draft; it is not agreement between two independent human annotators. For human–human agreement, a second human must independently review before discussion. A supervisor may adjudicate unresolved financial-reporting or contract questions. Do not publish reviewer names or contact details without consent.
