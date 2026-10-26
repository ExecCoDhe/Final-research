# Preliminary novelty recheck

Date: 25 October 2026. This is a work log, not a completed new literature review.

## Findings

1. The previously archived FinGround full text, section 3.3, explicitly defaults to the most recent filing date when restated figures conflict and flags the conflict. This narrows novelty; merely noticing conflicting annual figures is not sufficient. The proposal already acknowledges this.
2. The same text identifies `https://github.com/bettyguo/FinGround` as its release. An unauthenticated GitHub repository API lookup on 25 October returned HTTP 404. The repository might be unavailable, private, renamed, or incorrectly linked. This does not establish that its method or benchmark lacks authority-conditioned cases. Release inspection remains pending.
3. The previously archived FinVerBench full text states that companies with source inconsistencies from tagging variations or restatements are discarded. This supports investigating a different evidence regime, but does not establish novelty by itself.
4. The first Plug Power packet is a semantics and acquisition example. The proposal's B4 baseline explicitly handles original-as-filed instructions and historical cutoffs; these six cases are not evidence that B4 fails. No method was run.

## Required before a publication claim

- Inspect available released data/supplements for VeriFin, FinGround, FinDVer, AUDITFLOW, and relevant temporal-verification work; record exact versions and access limitations.
- Search for equivalent original/corrected and historical-cutoff evaluation protocols beyond the source bibliography.
- Find cases involving fact-scoped replacement, incomparable surviving disclosures, or genuine interpretation uncertainty that strong simple rules do not automatically resolve.
- Compare all methods with the same evidence and policy information. Separately report oracle parsing and raw-document conditions.

Provisional claim: the project investigates the adequacy of authority-conditioned financial verification. “First,” “novel algorithm,” and superior performance remain unestablished.

## Pilot update — 26 October 2026

The draft now contains 30 claims across five issuers, including an original SunPower non-reliance 8-K preceding the selected replacement annual report. A stronger simple comparator, B4 plus a reviewed withdrawal-status flag, matches the proposed manual reference decisions throughout the draft set. This is evidence against claiming that these examples establish a need for a complex resolver. It is not an implemented-system comparison.

This update is based on source acquisition and manual rule inspection, not a newly completed literature search. Equivalent withdrawal/status handling in financial and temporal-verification work must be investigated before treating that component as novel. The release-access status recorded above remains the 25 October observation, not a fresh availability check. See `pilot_assessment.md` for the conditional continuation decision.
