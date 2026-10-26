# Results summary

Accuracy = share of claims answered with the correct label (S, C or U). Company-level accuracy weights every company equally, because claims about the same company are not independent. 'Same as newest-wins' is how often an AI model gives the same label as rule B3, which always trusts the newest figure before the cutoff; a high value in the 'bare' condition means the model silently assumes that convention.

## Dataset: pilot

| Method | Claims | Accuracy | Company-level | Decisive (S/C) | Same as newest-wins | Correct per policy |
|---|---:|---:|---:|---:|---:|---|
| B1 context-only (ignores time and policy) | 30 | 40.0% | 40.0% | 27% |  | as_known_packet 1/6; corrected_named 5/13; explicit_display_comparison 1/1; original_as_filed 3/8; unspecified 2/2 |
| B3 latest figure before the cutoff (ignores policy) | 30 | 73.3% | 73.3% | 97% |  | as_known_packet 5/6; corrected_named 13/13; explicit_display_comparison 1/1; original_as_filed 3/8; unspecified 0/2 |
| B4 policy-aware latest (ignores withdrawal notices) | 30 | 96.7% | 96.7% | 90% |  | as_known_packet 5/6; corrected_named 13/13; explicit_display_comparison 1/1; original_as_filed 8/8; unspecified 2/2 |
| B4W policy-aware latest + withdrawal flag | 30 | 100.0% | 100.0% | 87% |  | as_known_packet 6/6; corrected_named 13/13; explicit_display_comparison 1/1; original_as_filed 8/8; unspecified 2/2 |
| P scoped reference resolver | 30 | 100.0% | 100.0% | 87% |  | as_known_packet 6/6; corrected_named 13/13; explicit_display_comparison 1/1; original_as_filed 8/8; unspecified 2/2 |

## Dataset: auto

| Method | Claims | Accuracy | Company-level | Decisive (S/C) | Same as newest-wins | Correct per policy |
|---|---:|---:|---:|---:|---:|---|
| B1 context-only (ignores time and policy) | 279 | 42.7% | 42.6% | 14% |  | as_known_packet 40/120; corrected_named 39/79; original_as_filed 0/40; unspecified 40/40 |
| B3 latest figure before the cutoff (ignores policy) | 279 | 57.0% | 57.0% | 100% |  | as_known_packet 80/120; corrected_named 79/79; original_as_filed 0/40; unspecified 0/40 |
| B4 policy-aware latest (ignores withdrawal notices) | 279 | 85.7% | 85.7% | 86% |  | as_known_packet 80/120; corrected_named 79/79; original_as_filed 40/40; unspecified 40/40 |
| B4W policy-aware latest + withdrawal flag | 279 | 100.0% | 100.0% | 71% |  | as_known_packet 120/120; corrected_named 79/79; original_as_filed 40/40; unspecified 40/40 |
| P scoped reference resolver | 279 | 100.0% | 100.0% | 71% |  | as_known_packet 120/120; corrected_named 79/79; original_as_filed 40/40; unspecified 40/40 |
