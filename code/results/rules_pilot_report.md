# Rule-based verifiers on the `pilot` dataset

30 claims from 5 companies.

Check passed: the program reproduces all 150 hand-applied decisions (30 cases x 5 rules) in pilot/manual_baseline_trace.csv.

### B1 context-only (ignores time and policy)

- Accuracy: **12/30 = 40.0%** (18 errors)
- Company-level accuracy (each company weighted equally, 5 companies): 40.0%
- Decisive answers (S or C): 26.7%
- False support (true answer C, predicted S): 0.0%

| Policy | Correct | Total | Accuracy |
|---|---:|---:|---:|
| as_known_packet | 1 | 6 | 17% |
| corrected_named | 5 | 13 | 38% |
| explicit_display_comparison | 1 | 1 | 100% |
| original_as_filed | 3 | 8 | 38% |
| unspecified | 2 | 2 | 100% |

Confusion matrix (rows = correct answer, columns = prediction):

| correct \ predicted | S | C | U | invalid |
|---|---:|---:|---:|---:|
| S | 7 | 0 | 11 | 0 |
| C | 0 | 1 | 7 | 0 |
| U | 0 | 0 | 4 | 0 |

### B3 latest figure before the cutoff (ignores policy)

- Accuracy: **22/30 = 73.3%** (8 errors)
- Company-level accuracy (each company weighted equally, 5 companies): 73.3%
- Decisive answers (S or C): 96.7%
- False support (true answer C, predicted S): 0.0%

| Policy | Correct | Total | Accuracy |
|---|---:|---:|---:|
| as_known_packet | 5 | 6 | 83% |
| corrected_named | 13 | 13 | 100% |
| explicit_display_comparison | 1 | 1 | 100% |
| original_as_filed | 3 | 8 | 38% |
| unspecified | 0 | 2 | 0% |

Confusion matrix (rows = correct answer, columns = prediction):

| correct \ predicted | S | C | U | invalid |
|---|---:|---:|---:|---:|
| S | 13 | 5 | 0 | 0 |
| C | 0 | 8 | 0 | 0 |
| U | 1 | 2 | 1 | 0 |

### B4 policy-aware latest (ignores withdrawal notices)

- Accuracy: **29/30 = 96.7%** (1 errors)
- Company-level accuracy (each company weighted equally, 5 companies): 96.7%
- Decisive answers (S or C): 90.0%
- False support (true answer C, predicted S): 0.0%

| Policy | Correct | Total | Accuracy |
|---|---:|---:|---:|
| as_known_packet | 5 | 6 | 83% |
| corrected_named | 13 | 13 | 100% |
| explicit_display_comparison | 1 | 1 | 100% |
| original_as_filed | 8 | 8 | 100% |
| unspecified | 2 | 2 | 100% |

Confusion matrix (rows = correct answer, columns = prediction):

| correct \ predicted | S | C | U | invalid |
|---|---:|---:|---:|---:|
| S | 18 | 0 | 0 | 0 |
| C | 0 | 8 | 0 | 0 |
| U | 1 | 0 | 3 | 0 |

### B4W policy-aware latest + withdrawal flag

- Accuracy: **30/30 = 100.0%** (0 errors)
- Company-level accuracy (each company weighted equally, 5 companies): 100.0%
- Decisive answers (S or C): 86.7%
- False support (true answer C, predicted S): 0.0%

| Policy | Correct | Total | Accuracy |
|---|---:|---:|---:|
| as_known_packet | 6 | 6 | 100% |
| corrected_named | 13 | 13 | 100% |
| explicit_display_comparison | 1 | 1 | 100% |
| original_as_filed | 8 | 8 | 100% |
| unspecified | 2 | 2 | 100% |

Confusion matrix (rows = correct answer, columns = prediction):

| correct \ predicted | S | C | U | invalid |
|---|---:|---:|---:|---:|
| S | 18 | 0 | 0 | 0 |
| C | 0 | 8 | 0 | 0 |
| U | 0 | 0 | 4 | 0 |

### P scoped reference resolver

- Accuracy: **30/30 = 100.0%** (0 errors)
- Company-level accuracy (each company weighted equally, 5 companies): 100.0%
- Decisive answers (S or C): 86.7%
- False support (true answer C, predicted S): 0.0%

| Policy | Correct | Total | Accuracy |
|---|---:|---:|---:|
| as_known_packet | 6 | 6 | 100% |
| corrected_named | 13 | 13 | 100% |
| explicit_display_comparison | 1 | 1 | 100% |
| original_as_filed | 8 | 8 | 100% |
| unspecified | 2 | 2 | 100% |

Confusion matrix (rows = correct answer, columns = prediction):

| correct \ predicted | S | C | U | invalid |
|---|---:|---:|---:|---:|
| S | 18 | 0 | 0 | 0 |
| C | 0 | 8 | 0 | 0 |
| U | 0 | 0 | 4 | 0 |
