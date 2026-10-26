# SunPower fiscal 2022 correction and withdrawal packet

Accessed 26 October 2026. Draft evidence packet; independent review pending.

| ID | Source | Official filing date | SEC index accepted display | SEC submissions API accepted UTC |
|---|---|---|---|---|
| SP0 | [Original 10-K](https://www.sec.gov/Archives/edgar/data/867773/000086777323000026/spwr-20230101.htm), 0000867773-23-000026 | 2023-03-10 | 2023-03-09 20:40:40 | 2023-03-10T01:40:40.000Z |
| SPW | [8-K Item 4.02](https://www.sec.gov/Archives/edgar/data/867773/000086777323000089/spwr-20231018.htm), 0000867773-23-000089 | 2023-10-24 | 2023-10-24 16:10:16 | 2023-10-24T20:10:16.000Z |
| SP1 | [Amended 10-K/A](https://www.sec.gov/Archives/edgar/data/867773/000086777323000117/spwr-20230101.htm), 0000867773-23-000117 | 2023-12-18 | 2023-12-18 08:17:05 | 2023-12-18T13:17:05.000Z |

The API timestamps come from [SEC submissions](https://data.sec.gov/submissions/CIK0000867773.json). Acceptance is not proof of exact public dissemination. The pilot uses date-separated cutoffs, not intraday claims.

Reporting interval: **2022-01-03 through 2023-01-01**. Primary metric: **net income (loss) attributable to stockholders**, not net income before attribution to noncontrolling interests. Units: USD thousands.

| Selected row | Originally reported | Adjustment | As restated |
|---|---:|---:|---:|
| Net income attributable to stockholders | 56,037 | -13,188 | 42,849 |
| Consolidated net income before noncontrolling-interest attribution — a different metric | 60,463 | -13,188 | 47,275 |

Locators: SP0 Consolidated Statements of Operations; SP1 Note 2, **Summary of Restatement – Consolidated Statements of Operations**, fiscal-year-ended January 1, 2023 column group, printed pages 88–89. The explanatory note identifies consignment microinverter inventory errors and expense reclassifications among the correction matters. 56,037 - 13,188 = 42,849 thousand USD.

## Contemporaneous withdrawal evidence

SPW Item 4.02 says that on **19 October 2023** the audit committee determined that the audited financial statements in the annual report filed **10 March 2023**, and specified 2023 quarterly statements, **“should no longer be relied upon.”** The 8-K was filed on **24 October**, not on the board-decision date or the `20231018` date embedded in its filename. It states that restatements are planned, and does not provide a replacement for the selected full-year numerical value.

At cutoff 2023-10-18, only SP0 is eligible in this packet. At cutoff 2023-10-25, SPW is eligible and withdraws reliance on SP0, while SP1 is still future evidence. Under the protocol's reliable-as-known contract, there is then no eligible authoritative replacement for this amount. This creates underdetermination; it does not establish that every old number was numerically wrong. An original-as-filed question still concerns what SP0 historically reported.

This is a packet-relative chronology, not a certification that no other public source reported a correction earlier. Unlike using SP1's later explanatory note to label the gap, SPW supplies contemporaneous evidence.

## Context and precision

Stockholder income is tagged `us-gaap:NetIncomeLoss` in these filings. SP0 context `i6bdb448be729485fba3279dca1fb0400_D20220103-20230101`; SP1 context `c-1`; units `usd`, scale 3, decimals -3. SP1 contexts `c-117` and `c-118` represent previously reported and adjustment scenarios. They are not extra independent economic observations.

The tag name must be interpreted with the actual statement caption and noncontrolling-interest reconciliation. The displayed corrected amount is USD 42.849 million; at the documented precision a conservative underlying-value interval is [42,848,500, 42,849,500] USD. A claim of exact unrounded equality is not established by the report.

Full source URLs, file/index hashes, and metadata are in `source_manifest.csv` and `fact_spotchecks.csv`.
