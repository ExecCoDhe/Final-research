# Pilot within the final proposal

Updated 26 October 2026. **Thirty draft cases across five issuers are ready for independent review.** No model has been run and the labels are not independently adjudicated.

The [44-page final proposal](../deliverables/final_proposal.pdf) remains the blueprint. Its page 20, Table 8 specifies an excluded pilot of five issuers and 30 claims; page 30 specifies the week-two feasibility milestone. This pilot tests acquisition, the interpretation contract and annotation feasibility. It is not a standalone 30-case publication benchmark.

## Start here

- **Project owner:** [hands-on steps](user_hands_on.md) and [pilot assessment](pilot_assessment.md).
- **Independent reviewer:** [download the reviewer pack](https://raw.githubusercontent.com/Shreya732-debug/Research-Work/main/pilot/reviewer_pack.zip). It omits provisional answers, analyst reasons and baseline outputs. Send this pack before the reviewer reads the rest of the repository; record any prior exposure.
- **Full archive:** [download the pilot bundle](https://raw.githubusercontent.com/Shreya732-debug/Research-Work/main/pilot/pilot_bundle.zip), including draft labels and analysis. Do not send it to a reviewer before their first pass.

## Files and status

| File | Purpose |
|---|---|
| [protocol_v1.md](protocol_v1.md) | Evidence contract, policies, precision, reference rules and gates |
| [pilot_cases_draft.csv](pilot_cases_draft.csv) | Current 30-case file; all labels await independent review |
| [source_manifest.csv](source_manifest.csv) | 11 SEC filings, accessions, dates, exact acceptance displays, source/index links and retrieval hashes |
| [supplementary_resources.csv](supplementary_resources.csv) | Original Plug XBRL and supplementary SEC API snapshots |
| [fact_spotchecks.csv](fact_spotchecks.csv) | 24 selected numerical facts with exact contexts, dimensions, scale and precision |
| [screening_log.csv](screening_log.csv) | Five accepted correction families; limitations and counting rules |
| [manual_baseline_trace.csv](manual_baseline_trace.csv) | Analyst-applied reference-rule decisions; not measured model outputs |
| [review_packet](review_packet) | Blank reviewer worksheet, instructions, time log, neutral source cards and metadata |
| [pilot_audit_log.md](pilot_audit_log.md) | Label-critical distinctions, limitations and checks |
| [novelty_recheck.md](novelty_recheck.md) | Preliminary related-work status; novelty remains unestablished |

Evidence records: [Plug Power](evidence/PLUG-2019.md), [Macy's](evidence/MACYS-2023.md), [SunPower](evidence/SUNPOWER-2022.md), [Tupperware](evidence/TUPPERWARE-2021.md), [DZS](evidence/DZS-2022.md). They include researcher interpretations, so they are outside the independent first-pass pack. The older [six Plug cases](first_family_claims.csv) are retained for link continuity and are included in the current 30; they are not extra observations.

## What the pilot currently tells us

Version and cutoff choices change several provisional verdicts. A SunPower non-reliance notice supplies a contemporaneous withdrawal-before-replacement example. However, a simple policy-aware rule plus a withdrawal flag agrees with the proposed reference resolver throughout this draft set. The pilot therefore does not establish algorithmic superiority. See the assessment for the manual disagreement counts and limitations.

Independent review, adjudication, actual annotation time, broader acquisition and a completed novelty check remain pending. The broader 20-family/10-issuer screening gate is **not met**. Thirty related claims represent only five correction families. All pilot issuers must remain outside the eventual main study. The proposed 600-claim study is conditional on these gates.

No research software or model implementation was created. Document extraction, CSV formatting and archive utilities were used only to prepare and check these research materials.
