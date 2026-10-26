# Macy's fiscal 2023 revision packet

Accessed 26 October 2026. Evidence inspection is complete for these selected rows; independent annotation review remains pending. This is a revision for errors described by the issuer as **immaterial misstatements**, not automatically a material restatement.

| ID | Filing | SEC index acceptance (as displayed) | Official filing date |
|---|---|---|---|
| M0 | [2023 Form 10-K](https://www.sec.gov/Archives/edgar/data/794367/000162828024012734/m-20240203.htm), accession 0001628280-24-012734 | 2024-03-22 16:13:42 | 2024-03-22 |
| M1 | [2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/794367/000162828025014315/m-20250201.htm), accession 0001628280-25-014315 | 2025-03-21 16:05:35 | 2025-03-21 |

Reporting interval: **2023-01-29 to 2024-02-03**, a 53-week fiscal year. Amounts below are USD millions; entity is Macy's, Inc. and consolidated subsidiaries.

| Selected row | M0 fiscal-2023 column | M1 fiscal-2023 comparative column |
|---|---:|---:|
| Net income | 105 | 45 |
| Net sales | 23,092 | 23,092 |

Locators: both filings' Consolidated Statements of Income (the fiscal-year columns, not the current-year column in M1). M1 Note 1, **Revision of Consolidated Financial Statements for the Correction of Immaterial Misstatements**, states that historical statements and notes were revised to properly report delivery expense, the related accrual, and tax effects. That note refers to an earlier Form 10-Q filed 12 December 2024; M1 is not claimed to be the first public correction.

Net-income displayed-value change: 45 - 105 = -60 million USD. Net sales are unchanged in the inspected columns. The differing net income plus the explicit revision note supports a revision relationship; API disagreement alone would not.

Inline XBRL: M0 context `c-1`, M1 context `c-4`, both for the exact interval above and without economic segment dimensions. Net income uses `us-gaap:NetIncomeLoss`; net sales use `us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax`. Both have `unitRef=usd`, `scale=6`, `decimals=-6`. The rounded income figures must not be asserted as exact unrounded amounts.

The packet does not include the December 2024 10-Q, so no claim is made about the date the corrected annual number first became public. Pilot policy cases name M0/M1 explicitly; the unspecified-policy cases use the protocol's declared ambiguity convention. Source hashes and index URLs are in `source_manifest.csv`.
