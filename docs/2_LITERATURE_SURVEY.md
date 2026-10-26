# Literature survey

Written 26 October 2026. This file has three parts:

1. **Related work section, ready for the paper.** Short-paper length, about 900 words. Cite keys like `[verifin]` match `deliverables/bibliography.tex`.
2. **Comparison table** for the paper or slides.
3. **Reading list in priority order**, with what to look for in each paper. Budget about 15 minutes per paper.

**How these references were checked.** Every reference below was verified against an official record (DOI, ACL Anthology, arXiv or publisher) during the earlier audit; see `deliverables/reference_table.md` for authors, venues and status. On 26 October 2026 we re-confirmed on arXiv that the five closest 2026 papers exist with the titles used here: VeriFin (arXiv:2608.10213), FinGround (2604.23588), FinVerBench (2605.29586), AUDITFLOW (2606.03031) and FinanceBench (2311.11944). Several 2026 papers are **preprints**; cite them as arXiv preprints unless you find a proceedings version. **Before submission, open each link and read at least the abstract of every paper you cite.** Reviewers notice when a citation doesn't say what the paper claims.

---

## Part 1: Related work (paper-ready draft)

> Adapt the wording into your own; do not paste it unchanged into a submission (see the integrity notes in `3_NEXT_STEPS_AND_PUBLICATION_PLAN.md`).

**Numerical reasoning over financial reports.** A large body of work evaluates whether models can extract and compute numbers from financial documents. FinQA [finqa] and TAT-QA [tatqa] introduced expert-annotated questions over report tables and text. ConvFinQA [convfinqa] extended this to conversational chains, MultiHiertt [multihiertt] to multiple hierarchical tables, and DocFinQA [docfinqa] to full-length documents. FinanceReasoning [financereasoning] revisits these tasks with harder, formula-annotated problems, and FinanceBench [financebench] evaluates open-book question answering over public filings. These benchmarks share an assumption: the supplied document or context is the correct source of truth. They test *how* to compute an answer, not *which version* of a disclosed figure should be used when a company has later corrected it.

**Claim verification over financial documents.** FinDVer [findver] evaluates explainable entailment and refutation of claims against long, hybrid financial documents. Three 2026 preprints move closer to our setting. VeriFin [verifin] grounds the operands of LLM-generated claims in XBRL facts and checks them with a solver, returning Verified, Violated or Abstain. FinGround [finground] verifies atomic claims with finance-aware retrieval and, notably, states that when restated figures conflict it *defaults to the most recent filing* and flags the conflict. AUDITFLOW [auditflow] builds executable symbolic environments for checking structured financial reports and separates checker-only gains from agent gains. FinVerBench [finverbench] studies the validity of statement-consistency benchmarks and *excludes* companies whose source facts are inconsistent because of restatements or tagging variations. FAITH [faith] measures intrinsic tabular hallucination in finance. Together these works establish grounding in XBRL, arithmetic checking and abstention as known techniques. However, none of them evaluates the same claim under different, explicitly stated filing-authority policies. Restatements are either resolved by a fixed "latest filing" convention or excluded.

**Temporal reasoning and evidence availability.** Temporal databases distinguish *valid time*, when a fact holds, from *transaction time*, when it was recorded [jensen]. We adapt this to filings: the reporting period, the public-availability date and the retrieval date. Mori et al. [mori] verify temporal claims about economic time series by translating them into temporal logic queries. ChronoFact [chronofact] verifies claims about event chronology using timelines, with supported, refuted and insufficient-evidence labels. In finance, using information that was not yet available is a recognised source of invalid results; Kapoor and Narayanan [kapoor] survey such leakage across ML-based science. These works make "temporal fact-checking" and three-way verdicts established. They do not address corrected accounting figures, where a later document may replace one specific number but leave others unchanged.

**Ambiguity, abstention and retrieval.** AmbiFC [ambifc] shows that claims can be legitimately ambiguous given the evidence and keeps annotation distributions rather than forcing one label. Selective classification [selective] formalises the trade-off between coverage and error when a system may abstain. We follow both: our *Undetermined* label is a correct answer when versions disagree or a figure is withdrawn, and we report coverage alongside accuracy. Retrieval-oriented benchmarks such as T²-RAGBench [t2ragbench] and FinMRAGBench [finmragbench] study evidence retrieval over financial text and tables. RAGTruth [ragtruth] and FActScore [factscore] study hallucination and atomic factuality. Our design gives every method the same evidence packet, so that differences reflect version reasoning rather than retrieval.

**Positioning.** Our work is a benchmark and evaluation study, not a new verification architecture. Its distinguishing property is the *paired, policy-conditioned* design: the same claim and evidence are judged under original-as-filed, corrected and as-known-at-a-cutoff policies. The data comes from authentic SEC restatements and non-reliance notices (Form 8-K Item 4.02), with unchanged-figure and wrong-metric controls. We find that a simple policy-aware rule with a withdrawal flag matches a fuller resolver, and we use the benchmark to measure whether LLM verifiers follow such policies.

---

## Part 2: Comparison table

N = numerical reasoning; A = handles ambiguity or abstains; T = explicit temporal reasoning; V = distinguishes original versus corrected versions; E = all methods given the same evidence. Y = yes; P = partially; ? = not established in what we read (not a claim that it's absent).

| Work | Venue / year | N | A | T | V | E | Key difference from our study |
|---|---|:-:|:-:|:-:|:-:|:-:|---|
| FinQA [finqa] | EMNLP 2021 | Y | – | – | – | Y | One supplied report is assumed correct |
| TAT-QA [tatqa] | ACL 2021 | Y | – | – | – | Y | Same |
| DocFinQA [docfinqa] | ACL 2024 | Y | – | – | – | Y | Long documents, not versions |
| FinDVer [findver] | EMNLP 2024 | Y | ? | P | ? | Y | Single document per claim |
| VeriFin [verifin] | arXiv 2026 | Y | Y | P | ? | Y | Grounds facts; no paired authority policies |
| FinGround [finground] | arXiv 2026 | Y | Y | P | P | Y | Defaults to the latest filing on restatement conflicts |
| FinVerBench [finverbench] | arXiv 2026 | Y | Y | P | P | Y | Excludes restated companies |
| AUDITFLOW [auditflow] | arXiv 2026 | Y | P | P | ? | P | Rule and graph checking, not cross-version |
| ChronoFact [chronofact] | IJCAI 2025 | P | Y | Y | ? | P | Event chronology, not accounting corrections |
| Mori et al. [mori] | FEVER 2022 | Y | P | Y | ? | Y | Economic time series, not competing filings |
| AmbiFC [ambifc] | TACL 2024 | P | Y | P | ? | Y | Ambiguity in general, not financial versions |
| **Ours** | — | Y | Y | Y | Y | Y | Paired policy-conditioned claims from real restatements |

---

## Part 3: Reading list (in priority order)

Read the abstract, the introduction and the dataset/method figure. Note one sentence for each "what to look for".

| # | Paper | Link | What to look for |
|---|---|---|---|
| 1 | FinGround (Guo, Wu, Yiu 2026) | [arXiv:2604.23588](https://arxiv.org/abs/2604.23588) | Section 3.3: the "default to the most recent filing" rule. This is our main motivation; quote it accurately. |
| 2 | VeriFin (Hall, Shome, Eiers 2026) | [arXiv:2608.10213](https://arxiv.org/abs/2608.10213) | How they ground claims in XBRL; their Verified/Violated/Abstain labels |
| 3 | FinVerBench (Panda 2026) | [arXiv:2605.29586](https://arxiv.org/abs/2605.29586) | Where they say restated companies are excluded |
| 4 | FinDVer (Zhao et al., EMNLP 2024) | [ACL Anthology](https://aclanthology.org/2024.emnlp-main.818/) | Task format and labels; how they annotated evidence. Good model for our dataset description. |
| 5 | AUDITFLOW (Wang et al. 2026) | [arXiv:2606.03031](https://arxiv.org/abs/2606.03031) | Checker-only versus agent results; supports "simple rules explain most of the value" |
| 6 | ChronoFact (Barik, Hsu, Lee, IJCAI 2025) | [IJCAI](https://www.ijcai.org/proceedings/2025/893) | Temporal fact verification framing |
| 7 | AmbiFC (Glockner et al., TACL 2024) | [ACL Anthology](https://aclanthology.org/2024.tacl-1.1/) | Why an "ambiguous" label is legitimate |
| 8 | FinQA (Chen et al., EMNLP 2021) | [ACL Anthology](https://aclanthology.org/2021.emnlp-main.300/) | The classic financial numerical QA benchmark |
| 9 | TAT-QA (Zhu et al., ACL 2021) | [ACL Anthology](https://aclanthology.org/2021.acl-long.254/) | Same, with text and tables |
| 10 | FinanceBench (Islam et al. 2023) | [arXiv:2311.11944](https://arxiv.org/abs/2311.11944) | LLMs on real SEC filings; they report frequent errors |
| 11 | Jensen & Snodgrass, Temporal data management (IEEE TKDE 1999) | [DOI](https://doi.org/10.1109/69.755613) | Valid time versus transaction time; cite one sentence |
| 12 | Kapoor & Narayanan, Leakage (Patterns 2023) | [DOI](https://doi.org/10.1016/j.patter.2023.100804) | Why leakage invalidates ML results |
| 13 | Geifman & El-Yaniv, Selective classification (NeurIPS 2017) | [arXiv:1705.08500](https://arxiv.org/abs/1705.08500) | Coverage versus risk; cite for the coverage metric |
| 14 | SEC EDGAR APIs documentation | [SEC](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | What Company Facts contains and its limits; cite in the data section |

Optional if time allows: ConvFinQA, MultiHiertt, DocFinQA, FinanceReasoning, T²-RAGBench, FinMRAGBench, RAGTruth and FActScore (links in `deliverables/reference_table.md`).

**One more search to do before writing.** Spend 30 minutes on Google Scholar and arXiv with these queries, limited to 2025–2026:

- `financial claim verification restatement`
- `LLM financial filings temporal`
- `point-in-time financial data LLM`
- `look-ahead bias LLM financial`

If you find a paper that does the same paired-policy evaluation, tell your supervisor. You'd then reframe the work as an extension or replication rather than a first.
