# Rule-based verifiers on the `auto` dataset

279 claims from 40 companies.

### B1 context-only (ignores time and policy)

- Accuracy: **119/279 = 42.7%** (160 errors)
- Company-level accuracy (each company weighted equally, 40 companies): 42.6%
- Decisive answers (S or C): 14.0%
- False support (true answer C, predicted S): 0.0%

| Policy | Correct | Total | Accuracy |
|---|---:|---:|---:|
| as_known_packet | 40 | 120 | 33% |
| corrected_named | 39 | 79 | 49% |
| original_as_filed | 0 | 40 | 0% |
| unspecified | 40 | 40 | 100% |

Confusion matrix (rows = correct answer, columns = prediction):

| correct \ predicted | S | C | U | invalid |
|---|---:|---:|---:|---:|
| S | 39 | 0 | 80 | 0 |
| C | 0 | 0 | 80 | 0 |
| U | 0 | 0 | 80 | 0 |

### B3 latest figure before the cutoff (ignores policy)

- Accuracy: **159/279 = 57.0%** (120 errors)
- Company-level accuracy (each company weighted equally, 40 companies): 57.0%
- Decisive answers (S or C): 100.0%
- False support (true answer C, predicted S): 0.0%

| Policy | Correct | Total | Accuracy |
|---|---:|---:|---:|
| as_known_packet | 80 | 120 | 67% |
| corrected_named | 79 | 79 | 100% |
| original_as_filed | 0 | 40 | 0% |
| unspecified | 0 | 40 | 0% |

Confusion matrix (rows = correct answer, columns = prediction):

| correct \ predicted | S | C | U | invalid |
|---|---:|---:|---:|---:|
| S | 79 | 40 | 0 | 0 |
| C | 0 | 80 | 0 | 0 |
| U | 40 | 40 | 0 | 0 |

### B4 policy-aware latest (ignores withdrawal notices)

- Accuracy: **239/279 = 85.7%** (40 errors)
- Company-level accuracy (each company weighted equally, 40 companies): 85.7%
- Decisive answers (S or C): 85.7%
- False support (true answer C, predicted S): 0.0%

| Policy | Correct | Total | Accuracy |
|---|---:|---:|---:|
| as_known_packet | 80 | 120 | 67% |
| corrected_named | 79 | 79 | 100% |
| original_as_filed | 40 | 40 | 100% |
| unspecified | 40 | 40 | 100% |

Confusion matrix (rows = correct answer, columns = prediction):

| correct \ predicted | S | C | U | invalid |
|---|---:|---:|---:|---:|
| S | 119 | 0 | 0 | 0 |
| C | 0 | 80 | 0 | 0 |
| U | 40 | 0 | 40 | 0 |

### B4W policy-aware latest + withdrawal flag

- Accuracy: **279/279 = 100.0%** (0 errors)
- Company-level accuracy (each company weighted equally, 40 companies): 100.0%
- Decisive answers (S or C): 71.3%
- False support (true answer C, predicted S): 0.0%

| Policy | Correct | Total | Accuracy |
|---|---:|---:|---:|
| as_known_packet | 120 | 120 | 100% |
| corrected_named | 79 | 79 | 100% |
| original_as_filed | 40 | 40 | 100% |
| unspecified | 40 | 40 | 100% |

Confusion matrix (rows = correct answer, columns = prediction):

| correct \ predicted | S | C | U | invalid |
|---|---:|---:|---:|---:|
| S | 119 | 0 | 0 | 0 |
| C | 0 | 80 | 0 | 0 |
| U | 0 | 0 | 80 | 0 |

### P scoped reference resolver

- Accuracy: **279/279 = 100.0%** (0 errors)
- Company-level accuracy (each company weighted equally, 40 companies): 100.0%
- Decisive answers (S or C): 71.3%
- False support (true answer C, predicted S): 0.0%

| Policy | Correct | Total | Accuracy |
|---|---:|---:|---:|
| as_known_packet | 120 | 120 | 100% |
| corrected_named | 79 | 79 | 100% |
| original_as_filed | 40 | 40 | 100% |
| unspecified | 40 | 40 | 100% |

Confusion matrix (rows = correct answer, columns = prediction):

| correct \ predicted | S | C | U | invalid |
|---|---:|---:|---:|---:|
| S | 119 | 0 | 0 | 0 |
| C | 0 | 80 | 0 | 0 |
| U | 0 | 0 | 80 | 0 |
