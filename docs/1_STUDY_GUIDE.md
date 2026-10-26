# Study guide: what this project is, from absolute zero

Written 26 October 2026 for the midterm review. It assumes no background in finance or machine learning.

**How to use this guide**

- **2 minutes:** read Section 1.
- **30 minutes before the midterm:** read Sections 1, 4, 5 and 9 (the likely questions).
- **Full understanding (about 2 hours):** read everything once, in order. Each section only uses ideas explained earlier.

---

## 1. The whole project in one paragraph

Companies publish yearly financial reports, and sometimes they later discover mistakes and publish corrected numbers. Then one sentence such as *"SunPower earned \$56.0 million in 2022"* can be **true** about the original report, **false** about the corrected accounts, and **undecidable** on a date when the company had said "don't trust our old numbers" but hadn't yet published new ones. Today's fact-checking systems and AI chatbots usually just grab a number, often the newest one, without asking *which version the question is about*. Our project builds a **test set (benchmark)** of such claims from real US company filings, labels each claim under clearly stated rules, and measures how well simple programs and AI language models handle it. We are not inventing a clever new algorithm. Our contribution is the careful test, the automatic way of building it from free public data, and the measurements.

---

## 2. Finance fundamentals (only what this project needs)

### 2.1 What a financial report says

A company's yearly report contains three main tables. You only need the first, plus one line of the third.

1. **Income statement** (also called "statement of operations"). It shows how much money the company made in a year:
   - **Revenue** (also "sales" or "net sales"): money received from customers. Macy's fiscal 2023 net sales were \$23,092 million.
   - **Expenses**: salaries, rent, taxes and so on.
   - **Net income** = revenue minus all expenses. If it is negative, it is called a **net loss**. Plug Power had a net loss of \$85.465 million in 2019.
2. **Balance sheet**: what the company owns and owes on one day. It isn't used in our project.
3. **Cash-flow statement**: actual cash in and out. We use one line, **net cash used in investing activities** (cash spent on equipment and so on), as an "unchanged" example.

**Variants of "net income" that are different numbers.** Mixing them up is a classic error, and our test includes traps for it:

| Variant | Meaning | Example in our data |
|---|---|---|
| Net income (consolidated) | Profit of the whole group, including parts owned by outside partners | SunPower: \$60.463M |
| Net income **attributable to stockholders** (or "to the Company") | The part that belongs to the company's own shareholders | SunPower: \$56.037M |
| Net income attributable to **common** stockholders | After paying preferred shareholders too | Plug: \$85.555M loss (not the same as the \$85.465M loss) |
| Income from **continuing operations** | Profit excluding businesses being sold or closed | Tupperware: \$155.6M, while total net income was \$18.6M |

### 2.2 The fiscal year is not always the calendar year

A **fiscal year** is the company's accounting year. Macy's "fiscal 2023" ran from **29 January 2023 to 3 February 2024** (53 weeks). SunPower's fiscal 2022 ran from 3 January 2022 to 1 January 2023. So "2023" alone is ambiguous, and the project always stores the exact start and end dates.

### 2.3 Who publishes these reports: the SEC and EDGAR

- The **SEC** (Securities and Exchange Commission) is the US stock-market regulator, roughly like SEBI in India.
- Every listed US company must file reports on the SEC's free public website, **EDGAR**.
- Each company has an ID called a **CIK**. Plug Power's is 0001093691.
- Each filing has an ID called an **accession number**, for example 0000867773-23-000026. Think of it as the filing's serial number.
- Each filing has an **official filing date**, the day it became public.

**Types of filings ("forms") you'll meet:**

| Form | Plain meaning |
|---|---|
| **10-K** | The yearly report, audited by an external accounting firm |
| **10-Q** | The quarterly report (not used much in our project) |
| **10-K/A** | An *amended* 10-K: the company re-files the yearly report with changes. Not every amendment changes numbers; some only fix a signature or add a section. |
| **8-K** | A "current report" announcing an important event |
| **8-K Item 4.02** | A specific 8-K section titled *"Non-Reliance on Previously Issued Financial Statements"*: the official warning that earlier statements **"should no longer be relied upon"** because they contain errors |

### 2.4 Restatements and revisions: when companies correct numbers

When a company finds an error in old statements:

- A **restatement** (informally "Big R") is for serious (material) errors. The company usually first files an **8-K Item 4.02** warning, then re-publishes corrected statements, often in a 10-K/A. Examples in our data: SunPower, DZS and Shake Shack.
- A **revision** ("little r") is for smaller (immaterial) errors. There's no warning notice; the corrected old numbers simply appear in the *comparative columns* of the next year's report. Macy's fiscal 2023 is our example. Its net income was originally \$105M and later shown as \$45M, because delivery expenses and the related accrual had not been reported properly.

Corrected reports often show a reconciliation table like this one (SunPower, USD thousands):

| Row | As previously reported | Adjustment | As restated |
|---|---:|---:|---:|
| Net income attributable to stockholders | 56,037 | (13,188) | 42,849 |

Important: the corrected document still prints the **old** number (56,037) in its "previously reported" column. A careless system that searches for "56,037" inside the corrected document will find it and wrongly conclude the old number is still valid. This is a deliberate trap in our test.

**A correction is scoped.** It changes particular numbers, not the whole report. Plug Power's restatement changed its net loss but **not** its investing cash flow (\$14.244M in both versions). A system that assumes "the amendment changed everything" makes mistakes on such unchanged lines. Our test contains these unchanged controls.

### 2.5 Units, signs and rounding

- Tables say **"in thousands"** or **"in millions"**. "56,037" in a table "in thousands" means \$56,037,000 = \$56.037 million.
- **Parentheses mean negative**: "(85,465)" is a loss of \$85,465 thousand. Our claims speak of a "net loss of \$85.465 million", meaning the size of the loss, which is a positive number.
- **Rounding.** A figure shown as \$56.037 million (rounded to the nearest thousand dollars) only tells you the true amount lies between \$56.0365M and \$56.0375M. So:
  - The claim "net income was \$56.037 million" is consistent with the report.
  - The claim "net income was **exactly** \$42,849,000 with no rounding" **cannot be proven** from a figure rounded to thousands. The honest answer is "undetermined". Pilot case P018 tests exactly this.

### 2.6 XBRL: how computers read these reports

Since about 2009, US filings carry **XBRL** tags: invisible machine-readable labels attached to each number. A tag records:

- the **concept**, for example `us-gaap:NetIncomeLoss` (us-gaap is the standard dictionary of accounting concepts),
- the **period**, for example 2022-01-03 to 2023-01-01,
- the **unit** (USD) and the **precision**, such as `decimals=-3`, meaning rounded to thousands,
- the **dimension**, if any, such as "As previously reported" versus "As restated".

The SEC offers a free web service called **Company Facts** that returns every tagged number a company ever filed, with the accession number and filing date of each filing that reported it. This is what makes our automatic dataset possible. For SunPower's fiscal 2022 net income, Company Facts returns two entries: 56,037,000 from the 10-K of 10 March 2023, and 42,849,000 from the 10-K/A of 18 December 2023. Our code saw exactly that.

### 2.7 Three different "times"

This idea is central, and it comes from database research (Jensen and Snodgrass, 1999):

1. **Reporting period:** the year the numbers are *about* (fiscal 2022).
2. **Availability time:** when a document *became public* (filed 10 March 2023).
3. **Retrieval time:** when *we* downloaded it (October 2026).

If you ask "what was known about fiscal 2022 on 1 June 2023?", you must use only documents available before 1 June 2023, even though today we can download the later correction. Using later information to answer an earlier-dated question is called **look-ahead bias** or **temporal leakage**. It is a famous source of fake-good results in finance research, such as trading strategies that secretly use corrected data that didn't exist yet.

---

## 3. AI and machine-learning fundamentals (only what this project needs)

### 3.1 Machine learning in one minute

**Machine learning (ML)** means a program learns patterns from examples instead of following hand-written rules. For example, show it thousands of emails labelled "spam" or "not spam" and it learns to label new emails.

**Our project currently trains no model.** It has two kinds of "verifiers":

- **Rule-based programs** (Python code with explicit if/else logic). These act as baselines and as the reference.
- **AI language models (LLMs)** used as-is through free online services. We *test* them; we don't train them. This is called **evaluation**, and it's a completely normal, publishable kind of ML research.

### 3.2 What an LLM is

A **large language model (LLM)**, such as ChatGPT, Gemini or Llama, is a program trained on huge amounts of internet text to predict the next word. That makes it good at answering questions in plain language. Important weaknesses for us:

- **Hallucination:** it can state wrong numbers confidently.
- **Memorisation:** it may "remember" a company's numbers from its training data instead of reading the documents we give it.
- **Defaults:** when unsure, it may simply prefer the newest number, or the one that matches the claim.

You talk to an LLM through a **prompt**: the instructions plus the question. Through an **API** (a web address that programs can call), our script sends each claim and its documents and gets back an answer. **Temperature 0** means "always give the most likely answer", which makes results repeatable.

### 3.3 Fact verification (claim verification)

**Fact verification** is an established research task. Given a **claim** and **evidence**, the system outputs whether the evidence supports it. The classic dataset is FEVER (2018), with labels *Supported / Refuted / Not Enough Info*. Our three labels follow the same idea:

- **S = Supported:** the figure that the policy selects agrees with the claim.
- **C = Contradicted:** that figure is clearly different. Note that "I couldn't find it" is *not* C.
- **U = Undetermined:** the evidence can't settle it under the rules. Examples are a question that is ambiguous between versions, a withdrawn number with no replacement yet, or rounding that prevents a decision.

### 3.4 Benchmarks, labels and annotation

- A **benchmark** is a fixed test set plus a scoring method, used to compare systems fairly. Examples are FinQA and FinDVer, and ours.
- A **gold label** is the correct answer, decided carefully by people.
- **Annotation** is the work of producing labels. **Inter-annotator agreement** measures whether two independent people give the same labels. Reviewers care about this because it shows the task is well defined.
- A **silver label** is produced automatically by rules. It's cheaper but must be spot-checked by people. Our automatic dataset has silver labels.
- **Blind review** means the reviewer labels without seeing our answers first, so they aren't influenced.

### 3.5 Baselines and ablations

- A **baseline** is a simple method that a new method or claim must beat or be compared against. Without baselines, a number like "80% accuracy" means nothing. Our baselines are B1, B3, B4 and B4W (Section 4.4).
- A **strong baseline** is a simple method that is actually hard to beat. Reviewers reject papers that only beat weak baselines.
- An **ablation** removes one component to see how much it mattered. For example, B4 versus B4W shows exactly what the withdrawal flag contributes.

### 3.6 How results are measured

- **Accuracy** is the share of claims with the correct label. 29/30 = 96.7%.
- A **confusion matrix** is a table of *correct answer* versus *predicted answer*. It shows which mistakes happen, for example "says S when the answer is C".
- **False support** is saying "supported" when the truth is "contradicted". This is the most dangerous error, because it confirms false information.
- **Coverage** is the share of claims where the system gives a decisive answer (S or C) rather than U. A system that always says U is never wrong in a dangerous way but is useless, so we report both.
- **Per-company (issuer-level) accuracy.** Six claims about the same company share the same documents, so they aren't six independent tests. We therefore also average accuracy per company. With only 5 companies, no statistical significance can be claimed. The proposal targets 40 or more companies for that reason.
- **Statistical significance** answers "could this difference be luck?". The proposal plans a **sign test** over companies: for each company, which method made fewer errors? You need at least 6 companies with a difference before any result can be called significant at the 5% level. You don't need the maths for the midterm; just know that **the company is the unit of evidence, not the claim**.

### 3.7 Data leakage

**Leakage** means the test accidentally contains information the system shouldn't have. Examples:

- A future correction is used to answer a past-dated question (temporal leakage).
- Near-identical claims appear in both development and test data.
- Rules are tuned while looking at the test answers.

The proposal's defences: split by whole company, freeze the rules before looking at test data, and record each document's availability date.

---

## 4. What exactly this project does

### 4.1 The research question

> When the same financial claim is judged under different, explicitly stated "authority policies" (original report, corrected report, or what was knowable at a date), do verification systems, including modern AI models, give the right answer? Or do they fall back on a default such as "the newest number wins"?

**Why it matters:**

- **AI financial assistants** answer questions about company numbers. If they quote a superseded figure, or the corrected figure when the user asked about the original report, users are misled.
- **Historical analysis and backtesting** must use the numbers available *at the time*. Using later corrected numbers creates look-ahead bias.
- **Close prior work shows the gap.** FinGround (2026), a recent financial fact-checker, states that when restated figures conflict it **defaults to the most recent filing** and flags the conflict. FinVerBench (2026) **discards** companies with restatements. So restatements are known to be a problem, but no benchmark we found tests the *same claim under different version policies*.

### 4.2 The task: inputs and output

Every test case contains:

1. **A claim** (one sentence), for example "For fiscal 2022 SunPower's net income attributable to stockholders was USD 56.037 million."
2. **An authority policy** that says which version counts (table below).
3. **A cutoff date.** Documents filed **on or after** this date are treated as not yet existing. A document counts only from the day *after* its filing date, because we don't trust exact filing times within a day.
4. **An evidence packet**: the same fixed set of documents for every method, sometimes including documents filed after the cutoff as a temptation.

The output is **S, C or U**.

**The five authority policies**, using SunPower, whose original figure was \$56.037M, then a warning notice on 24 Oct 2023, then a corrected figure of \$42.849M on 18 Dec 2023:

| Policy | Question it represents | Claim "\$56.037M" | Claim "\$42.849M" |
|---|---|---|---|
| `original_as_filed` | "What did the original report say?" | **S** (it did say that) | **C** |
| `corrected_named` | "What do the corrected accounts say?" | **C** | **S** |
| `as_known_packet`, cutoff 18 Oct 2023 | "What was reliably known on that date?" Only the original existed. | **S** | **C** |
| `as_known_packet`, cutoff 25 Oct 2023 | The warning exists, the replacement doesn't yet | **U** (withdrawn, no replacement) | **U** |
| `as_known_packet`, cutoff 19 Dec 2023 | The correction exists | **C** | **S** |
| `unspecified` | The claim doesn't say which version | **U** (the versions disagree) | **U** |
| `explicit_display_comparison` | "Subtracting figure A from figure B gives X" | Arithmetic on displayed numbers | |

### 4.3 The labelling rule, including rounding

1. Turn the claim into a range. "\$56.037 million" covers [56.0365, 56.0375]. A claim of an *exact* amount is a single point.
2. Turn each admissible source figure into a range using its precision.
3. Apply the rule:
   - **S** if *every* admissible interpretation lies inside the claim's range,
   - **C** if *every* one lies completely outside it,
   - **U** otherwise, including when there's no admissible figure at all.

This "every interpretation must agree" rule is what produces U for unspecified policies: the original says yes and the correction says no.

### 4.4 The five rule-based methods we compare

Each one deliberately ignores something, so the comparison shows which piece of information matters:

| Method | What it does | What it ignores |
|---|---|---|
| **B1 context-only** | Looks at every matching number in the packet (right company, metric and year) | Dates *and* policy. If two versions disagree it says U. |
| **B3 cutoff-aware latest** | Takes the newest figure filed before the cutoff | The policy. This is the "newest number wins" default, like FinGround's. |
| **B4 policy-aware latest** | Follows the policy (original, corrected or ambiguous); otherwise newest before the cutoff | Warning notices (8-K Item 4.02) |
| **B4W** | B4 plus a check: if an eligible warning notice withdrew the chosen figure and no replacement exists, answer U | — |
| **P reference resolver** | Full logic: date filter, explicit correction links, withdrawals, every admissible interpretation | — |

Next we add **AI models** (Gemini, Llama) to this table under two conditions:

- **full:** the model is told the policy, the cutoff and the rules.
- **bare:** the model sees only the claim and the documents, as a normal user would ask. This reveals its default assumption.

### 4.5 The 30-case hand-checked pilot (done before this guide)

An AI research assistant (earlier in this project) read 11 real SEC filings of 5 companies and wrote 30 claims, 6 per company. Every number has an exact source, filing date and a SHA-256 fingerprint of the downloaded file. The five companies:

| Company | What happened | Special lesson in this family |
|---|---|---|
| **Plug Power, fiscal 2019** | Restated in its 2020 10-K: net loss \$85.465M → \$83.743M | Investing cash flow is *unchanged* (\$14.244M): a correction is scoped. "Attributable to common stockholders" (\$85.555M) is a different row. |
| **Macy's, fiscal 2023** | Immaterial *revision* in the next year's 10-K: net income \$105M → \$45M | No warning notice. Fiscal year ends Feb 2024. Net sales unchanged (\$23,092M). |
| **SunPower, fiscal 2022** | 8-K Item 4.02 warning (24 Oct 2023), then 10-K/A: \$56.037M → \$42.849M | **The only withdrawal gap** (between the warning and the correction). Stockholder income versus consolidated income. The exact-amount rounding trap (P018). |
| **Tupperware, fiscal 2021** | Restated in the 2022 10-K: net income \$18.6M → \$15.6M | The continuing-operations trap (\$151.0M). Displayed-value arithmetic: 15.6 − 18.6 = −3.0 (P024). |
| **DZS, fiscal 2022** | 10-K/A: net loss \$37.431M → \$41.270M | Fiscal 2021 is unchanged. The as-known cutoff before and after the amendment. |

The draft labels are 18 S, 8 C and 4 U. **They are drafts.** No independent human has reviewed them yet (see the next steps document).

### 4.6 What we built in this session: working code

Everything is in `code/` (instructions in `code/README.md`):

1. **`verifier.py`** turns the five rules into a program. On the pilot it reproduces **all 150 hand-made decisions** (30 cases × 5 rules) in `pilot/manual_baseline_trace.csv`. This validates both the code and the hand analysis.
2. **`build_dataset.py`** builds a larger dataset automatically from free SEC data:
   1. It uses SEC full-text search to find 8-K filings from 2019–2024 containing "should no longer be relied upon" (2,228 search hits; the search service returned the first 1,600). It keeps those filed under Item 4.02 and excludes SPAC shell companies, which leaves about 520 companies.
   2. For each company it downloads Company Facts and looks for a fiscal year whose **net income changed** in a later 10-K or 10-K/A, **with the warning notice dated in between**.
   3. It drops changes larger than 3×, which usually mean a merger rather than a correction. We caught Innovex this way: "\$0.6M → \$73.9M" was a merger, not an error fix. It flags changes over 30% for a human to check.
   4. It writes 6–7 claims per company using the same templates as the pilot, plus an "unchanged figure" control when available, and labels them with rule P (silver labels).
   - **Result:** 40 companies and 279 claims (119 S, 80 C, 80 U) in about 5 minutes. Companies include Discover Financial, Shake Shack, TransUnion, Lovesac, DigitalOcean, Emergent BioSolutions and MARA.
   - **Spot-check:** we opened Shake Shack's real 8-K. It says the fiscal 2022 statements "should no longer be relied upon" because income-tax expense was overstated, which matches the change from a \$24.091M loss to a \$21.229M loss and the unchanged revenue.
3. **`run_llm.py`** sends each claim to a free AI model and scores the answers. It's ready to run but needs a free API key (5 minutes to get; see `code/README.md`).
4. **`midterm/Midterm_Presentation.pptx`**: 15 slides with speaker notes, generated from the actual results.

### 4.7 Results so far

| Method | Pilot (30 claims, draft labels) | Automatic (279 claims, silver labels) |
|---|---:|---:|
| B1 context-only | 40.0% | 42.7% |
| B3 newest-before-cutoff | 73.3% | 57.0% |
| B4 policy-aware | 96.7% | 85.7% |
| B4W policy-aware + warning flag | 100% | 100% |
| P reference resolver | 100% | 100%\* |

\* By construction: the automatic labels *are* rule P's answers. This column only shows how much each simpler rule loses.

**How to read this:**

- **Ignoring time and policy (B1)** fails whenever two versions exist.
- **"Newest number wins" (B3)** fails *every* "what did the original report say?" question and every ambiguous question. This is exactly the default described in FinGround.
- **Ignoring warning notices (B4)** fails the withdrawal-gap cases. That's 1 in the pilot and 40 in the automatic set, because the automatic set adds a gap case for every company.
- **The honest key finding:** the simple B4W rule already equals the full resolver P. So we **cannot claim a new, better algorithm**. The proposal itself predicted this risk and planned for it.

### 4.8 So what is the paper's contribution?

1. **A benchmark** where the same claim is judged under different authority policies, built from real SEC restatements, with controls for unchanged figures, wrong-metric traps and rounding.
2. **A reproducible pipeline** that anyone can rerun from free SEC data to make more cases.
3. **An evaluation of AI language models.** Do they pick the right version when told the policy? What do they assume when not told? Do they respect the cutoff date, or use future documents? Do they fall for "previously reported" columns? This is the main new *measurement*, and the next step.

This is a **dataset and evaluation paper**, a well-accepted paper type at workshops such as FNP and FinNLP, which explicitly invite "resources, benchmarks and negative results".

---

## 5. Why we changed topic (likely the first question at the midterm)

You previously proposed **explainable AI (XAI) for financial fraud detection**. The repository contains a source audit (`deliverables/audit_log.md`) of three research dossiers:

- **P1:** temporal model selection for fraud detection.
- **P2:** period-aware financial evidence verification. This became the current project.
- **P3:** "COMET-XAI", explainable AI plus counterfactual "recourse" for credit and fraud.

The audit scored ten candidate directions (proposal Appendix A, "decision matrix"). The XAI options scored lowest:

- Full COMET-XAI scored 48/100 and the all-in-one XAI merger 32/100. The chosen direction scored 79/100.

The reasons, in plain words:

1. **Not novel enough.** Grouped SHAP explanations, rank fusion of feature importances and robust recourse are already published (groupShapley 2021, RRF 2009, BioMark 2026, RobX 2022, ROAR 2021 and others).
2. **The data couldn't support the claims.** Credit datasets (HELOC, Taiwan) are single snapshots with no real time dimension, and the fraud dataset (BAF) is synthetic. So claims about explanations staying valid "over time" couldn't be tested honestly.
3. **Some legal claims were wrong.** For example, "the law requires four reasons, so use four features" isn't what Regulation B says.
4. **Many promised numbers were untested guesses.** The audit "quarantined" them (proposal Appendix E).

The new topic keeps the **finance + AI** theme, uses **real public data**, has **one clear testable question**, and needs **no GPU**. Prof. Gupta still needs to approve the change; see the next steps document.

---

## 6. Tour of the repository (what to open, what to skip)

| Path | What it is | Do you need to read it? |
|---|---|---|
| `docs/1_STUDY_GUIDE.md` | This guide | Yes |
| `docs/2_LITERATURE_SURVEY.md` | Literature survey, ready to adapt for the paper | Yes, before writing |
| `docs/3_NEXT_STEPS_AND_PUBLICATION_PLAN.md` | Exact steps, timeline and venues | Yes |
| `midterm/Midterm_Presentation.pptx` | Midterm slides with speaker notes | Yes |
| `code/` | Working code; start with `code/README.md` | Run the `.bat` files |
| `code/results/SUMMARY.md` | All results in one table | Yes |
| `code/data/auto/families.csv` | The 40 automatic companies with SEC links and blank check columns | Yes, for spot-checking |
| `deliverables/final_proposal.pdf` | The 44-page research plan written earlier by AI | Skim the abstract, Sections 1, 2 and 6, and the Table 8 targets. Very dense. |
| `deliverables/audit_log.md` | Corrections found in the 3 earlier dossiers | Only for "why we changed" |
| `deliverables/reference_table.md` | Every reference with its verification status | When citing |
| `pilot/README.md`, `pilot/pilot_assessment.md` | Pilot status and honest assessment | Skim |
| `pilot/protocol_v1.md` | Exact labelling rules | Reference |
| `pilot/pilot_cases_draft.csv` | The 30 claims with draft labels | Open in Excel |
| `pilot/evidence/*.md` | One page per company with exact sources | Read SunPower as an example |
| `pilot/review_packet/` and `reviewer_pack.zip` | What to send an independent reviewer (no answers inside) | Send to the reviewer |
| `pilot/source_manifest.csv`, `fact_spotchecks.csv` | Filing IDs, dates, file fingerprints, exact XBRL tags | Reference only |

---

## 7. Limitations (say these yourself before someone else does)

1. **Labels aren't independently reviewed yet.** The pilot labels were drafted by one AI analyst, and the automatic labels come from our own rule. The fix is a human spot-check plus an independent reviewer (next steps document).
2. **Small and purposive.** 5 hand-picked pilot companies, 40 automatic ones. These aren't random samples, so we can't claim how common such errors are in the real world.
3. **Constructed claims.** The claim sentences are written by us from templates. They're not real misinformation found online.
4. **Company Facts limits.** It only covers whole-company figures and standard tags. Mergers or reclassifications can look like corrections, which we filter and flag. The warning notice's exact coverage (which years it withdraws) is assumed and needs a human check.
5. **No algorithmic novelty.** A simple rule (B4W) equals the full resolver. We say so openly; the contribution is the benchmark and the AI evaluation.
6. **Only US filings, annual net income, English.**

Stating limitations clearly is *required* in ACL-style papers and makes reviewers trust you more.

---

## 8. One worked example end to end (practise explaining this)

**Case P016 (SunPower).**

- Claim: "SunPower's net income attributable to stockholders was \$56.037 million as reported by the active authoritative statements in the packet."
- Policy: as-known. Cutoff: 25 Oct 2023.
- Packet: SP0 (10-K, filed 10 Mar 2023, \$56.037M), SPW (8-K Item 4.02, filed 24 Oct 2023), SP1 (10-K/A, filed 18 Dec 2023, \$42.849M).

Here is how each step goes:

1. **Which documents exist before 25 Oct?** SP0 (10 Mar) and SPW (24 Oct). SP1 (18 Dec) is in the future, so it's ignored.
2. **Does an eligible correction replace SP0?** No, SP1 isn't eligible yet.
3. **Does an eligible warning withdraw SP0?** Yes, SPW says the 10-K filed 10 March "should no longer be relied upon".
4. **Active figures left?** None.
5. **Therefore U.**

What each method answers:

- **B3** takes the newest figure before the cutoff, SP0's \$56.037M, and says **S**. Wrong: it trusts a withdrawn number.
- **B4** also says **S**, because it ignores warnings.
- **B4W and P** say **U**. Correct.
- **An AI model** will see SP1 in the packet too. Does it wrongly use the future correction and say C? That's exactly what our AI experiment measures.

---

## 9. Questions you'll probably be asked, with answers

**Q1. What is your project in one line?**
A benchmark and evaluation of whether fact-checkers and AI models pick the right *version* of a financial number when companies correct their reports.

**Q2. Where is the machine learning?**
We evaluate large language models (Gemini, Llama), which is a standard ML evaluation study. We also build a reproducible dataset, which is core ML infrastructure work. Training a model isn't needed to answer the research question. The rule-based methods are baselines, which every ML paper needs.

**Q3. Why not just always use the newest number?**
Because the question may be about the original report, for example "what did they tell investors in March?", or about a past date, as in backtesting. On our data, "newest wins" gets only 57–73% right and fails every original-report question.

**Q4. What is new compared to existing work?**
Existing benchmarks assume one correct document (FinQA, FinDVer), or pick the latest filing (FinGround), or drop restated companies (FinVerBench). We test the *same claim under different explicit version policies* using real restatements. We don't claim a new algorithm.

**Q5. Why should we trust your labels?**
Every number links to the exact SEC filing. The code reproduces the hand analysis exactly. Next, an independent reviewer checks the pilot, and we hand-check a sample of the automatic dataset (Shake Shack is already checked).

**Q6. Why did your simple rule score 100%?**
On the automatic data, because the labels come from the reference rule. That dataset is meant for testing AI models, not our rules. On the pilot, it's because the cases mostly need date, policy and warning handling, which B4W has. That's an honest finding: simple explicit rules suffice, and the open question is whether AI models get it right.

**Q7. How big is the dataset? Is it enough?**
Currently 30 hand-checked claims plus 279 automatic claims from 40 companies. The builder can easily produce more by searching more notices. For statistics we count companies, not claims. 40 companies is enough for a workshop benchmark paper. The proposal targets 50 companies and 600 claims for a full version.

**Q8. Why SEC data and not Indian (NSE/BSE) data?**
The SEC gives free, structured, machine-readable (XBRL) data with exact filing dates and official non-reliance notices. Indian XBRL filings exist on the MCA and NSE but are harder to access in bulk. Extending to India is good future work.

**Q9. What's the difference between a restatement and an amendment?**
An amendment (10-K/A) is a re-filed report, and it may only change text. A restatement is a correction of numbers because of an error. They often coincide but not always, which is why our rules use explicit correction links rather than "the newer document wins".

**Q10. What does "undetermined" mean, and isn't that a cop-out?**
U is a correct answer when the evidence genuinely can't decide: an ambiguous question, a withdrawn figure with no replacement, or rounding. We also measure coverage (how often a method decides), so a method that always says U doesn't look good.

**Q11. What is data leakage here?**
Using a correction filed *after* the cutoff to answer a question about an earlier date. Our cutoff rule and the packets that include future documents test exactly that.

**Q12. What is the next step, and when will you finish?**
Run free AI models (Gemini, Llama) in both conditions, hand-check about 20 companies, get an independent review of the pilot, then write a 4–8 page paper. Target: FNP 2027 workshop at EACL, deadline 15 December 2026.

**Q13. What will you do if AI models do perfectly?**
That is still a publishable finding: explicit policies make the task solvable, and the bare condition shows what goes wrong without them. The risk section of the proposal pre-plans this "negative result" route.

**Q14. Did you use AI to do this work?**
Answer honestly. AI assistants helped with the literature audit, drafting and code. We checked the outputs: the code reproduces the hand analysis, the sources are linked, and the references were verified. We'll disclose AI assistance as the venue's policy requires. (See the integrity notes in the next steps document.)

---

## 10. Glossary

| Term | Meaning |
|---|---|
| 10-K / 10-Q / 10-K/A / 8-K | Yearly report / quarterly report / amended yearly report / event report (Section 2.3) |
| Item 4.02 | The 8-K section announcing that old statements "should no longer be relied upon" |
| Accession number | Unique ID of one SEC filing |
| Ablation | Removing one component to measure its effect |
| API | A web address a program calls to get data or an AI answer |
| As-known policy | Judge using only documents public before the cutoff, honouring corrections and warnings |
| Authority policy | The rule saying which version of a figure counts |
| Baseline | A simple comparison method |
| Benchmark | A fixed test set plus scoring, for comparing systems |
| CIK | The SEC's company ID |
| Company Facts | The free SEC web service listing every XBRL number a company filed |
| Confusion matrix | Table of correct versus predicted labels |
| Coverage | Share of decisive answers (S or C) |
| Cutoff date | Documents filed on or after it are treated as not yet public |
| EDGAR | The SEC's public filing website |
| Evidence packet | The fixed documents given to every method for a claim |
| False support | Predicting S when the truth is C |
| Fiscal year | The company's accounting year; may not match the calendar year |
| Gold / silver label | Human-verified / rule-generated correct answer |
| Hallucination | An AI stating false information confidently |
| Issuer | The company that files the reports |
| Leakage / look-ahead bias | Using information that wasn't available yet |
| LLM | Large language model (ChatGPT, Gemini, Llama…) |
| Net income / net loss | Profit or loss after all expenses |
| Noncontrolling interest | The share of a subsidiary owned by outsiders; why "attributable to stockholders" differs from consolidated net income |
| Prompt | The instructions and question sent to an LLM |
| Restatement / revision | Correction of material / immaterial errors in past statements |
| S / C / U | Supported / Contradicted / Undetermined |
| SEC | US Securities and Exchange Commission |
| Sign test | A simple significance test counting which method wins per company |
| Temperature | LLM randomness setting; 0 means repeatable |
| XBRL | Machine-readable tags on numbers in filings |
