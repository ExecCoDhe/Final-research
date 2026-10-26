# Package validation — 26 October 2026

Document/data checks passed: 30 unique aligned case IDs; six cases per each of five issuer families; draft labels 18 S, eight C, four U; 11 primary filing records; 24 selected numeric-context records; all packet source IDs resolve; fact intervals match selected claim intervals; inspected units resolve to USD; inline signs/scales reproduce recorded signed values; named-source cutoffs follow official filing dates; reconciliation arithmetic agrees; manual disagreement counts are 18/8/1/0/0; reviewer labels and identity fields are blank; local Markdown links resolve.

`git diff --check` passed before packaging. ZIP integrity is checked after archive creation. The reviewer ZIP includes only the seven files under `review_packet/`; it excludes the provisional key, interpretive evidence notes, numerical spot-check values, protocol examples, baseline outputs and assessment. Source metadata and neutral locators remain available to the reviewer.

These checks concern package consistency and provenance. They do not constitute independent human validation, a model run, hypothesis testing or completion of the broader screening gate. No research implementation is included.
