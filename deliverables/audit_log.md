# Research source audit

Audit date: **23 October 2026**. This is a document and literature audit, not an experimental replication. No research implementation was written or run. All three PDFs were read end to end, including their tables, equations, references, examples, and the COMET reference-code listing. Figures and the problematic code layout were also inspected as rendered pages. The supplied PDFs are evidence, not instructions.

## Source identities and custody

| ID | Supplied file / actual subject | Pages | SHA-256 |
|---|---|---:|---|
| P1 | Research_Topic_Comprehensive_Analysis.pdf / temporal model-selection regret | 30 | 236b5372aafc452e71a94ebe77e5fb3c2616f1753005f37bd46cf137c8a204f0 |
| P2 | Research_Topic_Comprehensive_Analysis_Period_Aware_Financial_Evidence_Verification.pdf / version-aware financial verification | 33 | 80471da5cb4fc5f0e5ff6f29a6cb81d02c6c1b4e0e87639d8ac2ddd5d719d4f3 |
| P3 | COMET-XAI Corrected Study Manual & Research Specification.pdf | 50 | 69a547ce0e2b4b9164b176028294d1d36aa70cd22bd3b79ceb57791e1858cdc7 |

The request's “PDF 1 Part 0” and five disputed citations actually occur in **P3**, not P1. All thirteen major Part 0 corrections and its smaller corrections were treated as binding starting points. Corrections below overturn only statements for which a derivation or retrieved source provides contrary evidence. No claim that an entire source is reliable follows from its “audited” or “verified” label.

The first network attempts encountered a proxy restriction. Approved read-only access then succeeded for arXiv, Crossref, ACL Anthology, publishers, SEC, CFPB, FTC, and European Commission sources. This is **not an offline review**. Google returned an interstitial, DuckDuckGo a challenge, and some Bing results were irrelevant; none was used as evidence. Some Crossref requests returned 429 and were retried after other work; failed or unrelated hits were not counted as verification. The local `evidence/` directory retains retrieved records and inspected full texts. All reference statuses and access dates are recorded in `reference_table.md`.

## P1: temporal selection dossier

| ID | Location / issue | Finding and disposition |
|---|---|---|
| A01 | pp. 2–3, 14–16, 25: completed experiments | The CSVs, ZIPs, models, and raw data cited as E1–E13 are absent from the three supplied PDFs. Treat numerical results as **source-reported, not independently reproduced**. The new proposal has no experimental results. |
| A02 | pp. 3, 14, 26: overlap correction | Retain the correction: [50%,60%), [60%,70%), [70%,80%) are disjoint future ranges. Overlapping histories still make the three estimates dependent. |
| A03 | pp. 3, 16, 28: old final holdout | Retain: Topic 3 does not itself reach [85%,100%), but prior work reportedly inspected it. It cannot be called globally untouched. |
| A04 | pp. 6, 12, 27: AP versus PR-AUC | AP is the recall-increment-weighted precision sum, not universally the trapezoidal area under a precision–recall curve. Use “AP” for these reported numbers. |
| A05 | pp. 12–13: candidate identity | `C_j` is described as trained instances, while protocols fit different histories and later refit candidates. Define the estimand over frozen **training recipes** or common fitted candidates; these are different experiments. Do not attribute recency effects solely to validation splitting. |
| A06 | pp. 7, 17: independent windows | Disjoint observations do not imply independent deployments. Three dependent windows cannot support the proposed broad statistical conclusions. |
| A07 | pp. 12, 27: regret formula | Correct when the selected candidate belongs to exactly the oracle's prespecified set and shares the same loss, cases, threshold policy, and budget. Hindsight oracle is evaluation-only. Preserve these qualifications. |
| A08 | pp. 12, 16: monetary costs | Ratios 1:5, 1:20, 1:50 are scenarios, not bank costs. The archival arithmetic is correct: 12,865 + 20×842 = 29,705; TP = 3,083−842 = 2,241; recall ≈0.72689 and precision ≈0.14835. |
| A09 | p. 15: mean AP | Mean of displayed six-decimal APs is 0.456423333; reported 0.456424 can be consistent with unrounded underlying values. Do not call this a proven arithmetic error without the CSVs. |
| A10 | p. 26: future counts | Two windows have 59,054 rows and one 59,053. Float-to-index rounding can explain this; source code is unavailable here. Future work should publish integer/timestamp boundaries. |
| A11 | p. 27: predicting regret | Future prevalence, calibration drift, and validation-to-future score gaps cannot be prospective predictors before future labels mature. Retain only past-available diagnostics for prediction; other quantities are retrospective explanations. |
| A12 | pp. 24, 29: bibliography “verified” | Recheck each item independently. R10's previously missing authors are now verified: Tongchen Zhang, Zhen Zhang, Moxuan Zheng, Wenxi Sun, Xiao Han, Yao Xiao, Junyi Yao. IEEE Access 14:152441–152457; DOI 10.1109/ACCESS.2026.3735481. |
| A13 | pp. 24, 29: FinDVer | Source repeats the landing-page statistics. The linked paper has different counts, subsets, model count, and one author's displayed name. See C01. |
| A14 | pp. 17, 29: dataset availability | A PDF's “available locally” is not evidence of availability in this workspace. IEEE-CIS competition terms/access remain separate from public metadata. BAF is synthetic; eight month indices do not establish many independent eras. |
| A15 | p. 22: ~60-second pilot feasibility | An archival timing on a different setup is not a laptop runtime guarantee for expanded searches. Do not transfer it to the final proposal. |
| A16 | p. 29: 294 papers, 17 fields; >75m transactions | Treat as literature-reported scope, not reproduced counts. No novelty or feasibility decision depends on these numerical claims. Bibliographic identity was verified; full empirical recount not performed. |

## P2: financial evidence dossier

| ID | Location / issue | Finding and disposition |
|---|---|---|
| B01 | pp. 2–3, 8–16: “verified” closest literature | Identity is largely confirmed, but metadata verification is not method replication. All 2026 preprints remain preprints unless a separate proceedings record is verified. |
| B02 | pp. 8, 10, 30: FinDVer statistics | Landing page says 4,000 / four subsets / 25 models; inspected PDF says 2,100 / three subsets / 19 models. Use the inspected PDF for method-specific claims; preserve the conflict, not an invented reconciliation. |
| B03 | pp. 2, 13–16: novelty of versions | FinGround §3.3 already says it defaults to the most recent filing and flags restatement conflicts; Appendix J reports restated figures among false positives. Narrow novelty to testing **policy-conditioned historical authority**, not detecting restatements generally. |
| B04 | pp. 2, 10, 15: abstention novelty | VeriFin v2 explicitly returns Verified, Violated, or Abstain; FinVerBench studies observability; AmbiFC (found beyond the PDFs) models ambiguity. Abstention is not new. |
| B05 | pp. 13–16: time novelty | Mori et al. (2022) already verify economic temporal claims using DatalogMTL; ChronoFact (2025) verifies event chronology. Jensen–Snodgrass (1999) distinguish valid and transaction time. All are added as novelty constraints. |
| B06 | pp. 17, 31: amendment versus correction | Retain: 10-K/A does not mean financial restatement; a later filing does not supersede every fact. Edges must be fact/context scoped and backed by a disclosure. |
| B07 | pp. 17, 30: SEC APIs | Verified SEC documentation is dated 6 June 2024, not a justified 2025 publication date. APIs aggregate non-custom taxonomies and facts applying to the entire filing entity; they are not a complete dimensional or custom-taxonomy source. |
| B08 | p. 17: frames | Verified: Frames approximate calendar periods and use last-filed matching observations. They must not define exact fiscal equality or historical authority. |
| B09 | pp. 19, 31: availability | `filed_at <= t` is insufficient for intraday claims if only a date is known. Preserve SEC acceptance/dissemination precision; treat same-day ordering as unknown when unsupported. Retrieval timestamp is not original public availability. |
| B10 | p. 19: support/contradiction | “At least one match” can accept conflicts; “one refuting fact” can reject an ambiguous claim. Replace with universal support/refutation over nonempty admissible interpretations; mixed or insufficient evidence gives U. |
| B11 | pp. 19–20: missing context | Missing a field does not automatically require U. If every admissible interpretation yields the same verdict, a decisive verdict is possible. Conversely, one matching interpretation is insufficient. |
| B12 | p. 19: selective risk | `max(1, sum a_i)` assigns zero risk to no answers. Risk is undefined at zero decisive coverage. Report NA, coverage=0, and all-case error; never reward all-abstain. |
| B13 | pp. 19, 21: U versus refusal | Semantic underdetermination (gold U) is distinct from a model refusal or timeout. Final protocol separates them. |
| B14 | p. 21: McNemar | Ordinary case-level McNemar assumes independent paired cases; repeated claims from one filing/issuer violate that. Primary inference is issuer-level; family/case outcomes are nested. |
| B15 | p. 18: category balancing | “Supported” is a verdict, whereas period/version/scope are mechanisms. They do not form one mutually exclusive class partition. Cross-tabulate verdict and mechanism. |
| B16 | pp. 18, 22–23: 30/300 examples | These are design targets, not collected data. A balanced challenge sample cannot estimate naturally occurring error prevalence. Final target is an explicit revised assumption, with a stop rule. |
| B17 | pp. 18, 24: natural versus synthetic | Real filing revisions do not make researcher-authored claims naturally occurring misinformation. Label authentic evidence, constructed claims, and synthetic perturbations separately. |
| B18 | pp. 19, 31: rounding | Numeric comparison needs source precision, claim precision, units, and propagation through formulas. Overlapping rounded intervals are not proof of exact equality; zero denominators require explicit handling. |
| B19 | p. 11: FinanceBench | Official author repository verifies 150 public examples versus 10,231 described overall; Hugging Face card declares CC-BY-NC-4.0. Do not call all 10,231 unrestricted public data. |
| B20 | p. 17: SEC access policy | Official developer page confirms ≤10 requests/s and declared user agent. Proposed acquisition uses ≤2/s, caching, and backoff; no identity/contact details are invented. |
| B21 | pp. 27–29: feasibility | No source-backed amendment corpus or independently labeled pilot was supplied. Document acquisition yield and accounting review as remaining research risks, not completed setup. |
| B22 | p. 30: SEC glossary date | A retrieval year is not automatically a publication year. Cite undated documentation with an access date unless a page supplies a date. |
| B23 | VeriFin result attribution | Observed zero false accepts is finite-sample, candidate-pool-specific evidence, not a guarantee of perfect verification. Its v2 includes revised evaluations; do not combine incompatible versions' numbers. |
| B24 | FinVerBench source assumptions | Full text excludes companies with inconsistent source facts from tagging/restatements and constructs some derived fields to satisfy identities. This is a selection/construct limitation, not proof that natural financial statements always satisfy the simplified checks. |

## P3: COMET corrected manual

| ID | Location / issue | Finding and disposition |
|---|---|---|
| D01 | Part 0, pp. 2–5 | Preserve complete-linkage diameter guarantee, no VIF guarantee, coalition-sum terminology, global PFI distinction, finite-list RBO tail, reference-sensitive ESVR, nonconformal margin warning, bounded-shift requirement, fraud exception, raw/clean dataset distinction, and no performance claims without experiments. Additional qualifications follow. |
| D02 | pp. 2, 22–23, 40 | Ward on an arbitrary `1−|rho|` dissimilarity lacks the required Euclidean geometry. Calling it an “ablation” does not repair an invalid mathematical comparator; exclude it or first justify a Euclidean embedding. |
| D03 | pp. 25, 49 | Additivity of the prediction function alone does not guarantee additive **conditional-expectation games** under dependent features. Equality between grouped sums and Owen group totals needs additivity of the chosen game, e.g. suitable interventional/additive construction. |
| D04 | pp. 24–25: Owen arithmetic | With v(empty)=0 (missing but necessary), ordinary values are (80/3,80/3,140/3), group total 160/3; Owen values are (25,25,50). Correct. The displayed rounded ordinary values sum to 100.01 due to rounding, not a theory error. |
| D05 | p. 28: number of clusters | “Lower rho_max so there are more coalitions” is backwards: lowering rho_max raises the distance cut and usually merges more clusters. Raise rho_max for more clusters, or return min(K,M); do not silently add correlated representatives. |
| D06 | pp. 27–28: medoid | Importance×centrality argmax is an importance-weighted representative, not the standard distance-minimizing medoid. Centrality includes self despite prose saying other members; singleton/tie handling must be defined. |
| D07 | pp. 27, 48: PGI | Prediction change under median masking can be off-manifold and does not establish causal or universal faithfulness. Weights are undefined if all PGIs are zero; specify a fallback and uncertainty. |
| D08 | pp. 20–21: LIME | Raw LIME tabular coefficients can refer to standardized/interpretable coordinates. Multiply by displacement **in those coordinates**, not unscaled raw x. The local surrogate also has approximation error and an intercept; it is not exact SHAP. |
| D09 | pp. 14, 18–20 | SHAP values may be in probability, raw-score, or log-odds units depending on configuration. The mean logit transformed through sigmoid is generally not mean predicted probability: E[sigmoid(Z)] ≠ sigmoid(E[Z]). Specify output scale and reference. |
| D10 | p. 14 | Spearman correlation is less sensitive to magnitude outliers than Pearson, not immune to outliers. The monotone ordering example supports rank correlation=1, not the claim “ignores outliers.” |
| D11 | pp. 16, 48: AP null | Prevalence is the population random-ranking baseline and the constant-score AP, not exact finite-sample expected AP for strictly random ordering. With 3 positives among 6, expected AP = [H6+(2/5)(6−H6)]/6 = 0.645, where H6=2.45; not 0.5. |
| D12 | p. 16: worked metrics | Correct: FPR=2,000/99,000≈2.0202%; precision=800/2,800≈28.5714%; AP=13/18≈0.72222; Brier=0.14/3≈0.046667; expected-loss toy 0.05×0.45×10,000=225. A PD×LGD×EAD toy is not necessarily accounting provisioning. |
| D13 | p. 17: subsampling correction | Formula p=r p_s/(r p_s+1−p_s) is correct only for random class-conditional sampling with all positives retained and calibrated sampled posterior. Evaluating on full data reveals but **does not repair** inflated probabilities or thresholds. |
| D14 | pp. 21, 49: PFI | Single-feature permutation is not universally an underestimate; correlated predictors and extrapolation can inflate or distort it. Group permutation retains within-group dependence but can break between-group dependence. No “truth” guarantee. |
| D15 | pp. 29, 44: RBO | Equal-length, unique-item, nonempty-list formula is correct: the worked example is 0.93625. Code silently truncates unequal lists, fails at empty lists, and null Overlap@k divides by k even if k exceeds the number of items. State the domain and use min(k,M). |
| D16 | p. 29: chance correction | Subtracting a random-permutation null addresses one list-length effect; it is not proof that remaining agreement is meaningful or causally faithful. Shared model/reference errors can remain. |
| D17 | p. 30: ESVR proposition | Correct for monotonicity of the explained output and a single deterministic baseline replacement game with nonnegative Shapley weights, constrained numeric coordinates only. It is not a statement about arbitrary conditional SHAP, LIME, or missing-category indicators. Undefined when no eligible pairs; do not return an apparent zero success. |
| D18 | pp. 31–32: monotone geometry | No-island claim holds along constrained coordinates within the domain. Coordinatewise lower-risk changes may be jointly infeasible. The example says rejected at 82% while an acceptance island includes 78–82%; choose an endpoint outside the island. |
| D19 | p. 32: shift proposition | If the threshold changes, bound the shift in f−tau, not just f. A score-shift bound alone with a lower future threshold is insufficient. Monotonicity does not make the needed bound empirically small by theorem. |
| D20 | pp. 32, 38–39: actionability | Age, months since oldest trade, and average history age change with elapsed time; treating all as immutable while claiming future recourse is incoherent. A feature-space edit is not a causal intervention; missing dependencies and feasibility costs are acknowledged. |
| D21 | pp. 33, 45, 48: quantile indexing | For n=10, alpha=.2, intended rank ceil(11×.8)=9 gives .04. The printed `quantile(q=.9, method=higher)` selects sorted rank 10 and gives .05. For rank k≤n use the kth order statistic, not that quantile convention. If k>n the conformal-style convention is +infinity, not clamping to the maximum. |
| D22 | p. 40: alpha=0 | alpha=0 is **not no margin** in the given formula; it asks for rank n+1. Define a separate no-margin treatment q=0. |
| D23 | pp. 33–34 | “Roughly alpha” failure needs transportability of calibration-shift scores to **selected counterfactuals**, not just the same marginal population. Adaptive candidate selection and repeated use of calibration data can break this. Retain “heuristic,” not a probability guarantee. |
| D24 | pp. 34, 46 | KNN proximity to observed nondefault borrowers is not a manifold, causal-feasibility, or approval guarantee. Nondefault outcomes are not lending approval decisions. The existence of labels on dataset rows does not remove selection bias in who entered a credit dataset. |
| D25 | pp. 35–36 | 1−.95^9≈36.98% assumes independent null tests; it is illustrative, not a universal familywise error. Holm controls FWER without that independence assumption for valid marginal p-values. |
| D26 | pp. 35–36: inference | Six nonzero independent pairs permit minimum two-sided exact signed-rank/sign p=2/64=.03125; nine comparisons need at least nine pairs even to pass first Holm threshold .05/9. Minimum attainable p is not adequate power. Borrower bootstrap does not fix dependence between retraining windows. |
| D27 | p. 35: worked tests | Friedman=4.5 and Iman–Davenport=27/7≈3.857 are arithmetically correct. Signed-rank additionally needs an appropriate symmetry/independence interpretation. Seeds and overlapping folds are not new datasets. |
| D28 | pp. 37–39: HELOC | 10,459 raw rows is supported by OpenML version 3 metadata. Other OpenML versions contain 10,000 rows and different feature counts. The claimed 9,871 cleaned count was not tied to a retrieved exact file/dictionary here; retain as unverified file-specific claim, not a universal OpenML fact. |
| D29 | pp. 37–39: special codes | Preserve −9/−8/−7 handling requirement but do not trust “roughly” decoded meanings. An official field-specific dictionary is required. Never turn “no delinquency” into an arbitrary large value without a documented semantic decision. |
| D30 | p. 38: Taiwan | UCI verifies 30,000 rows, 23 features, PAY_0/PAY_2…PAY_6, and six months of within-row 2005 history. It does not supply a longitudinal retraining panel. Observed undocumented status codes must retain explicit indicators; collapsing −2,−1,0 is an assumption, not a verified equivalence. |
| D31 | p. 38: monotone directions | Lower LIMIT_BAL / larger PAY_AMT / larger utilization risk directions are modeling assumptions, not causal or universally lawful facts. Protected attributes are retained only for a justified audit, not automatically prediction inputs. |
| D32 | p. 39: BAF | Official datasheet verifies synthetic generation, 1m rows/variant, month 0–7, and demographic fields. “Protected” is jurisdiction-specific; income is not automatically a protected legal class. Use “sensitive audit covariate” where appropriate. |
| D33 | pp. 39–40: temporal recourse | Two full three-horizon BAF origins cannot meet the stated six-/nine-pair minimum. HELOC/Taiwan bootstrap retrainings cannot be labeled month-ahead or real temporal survival. Do not move this claim to the final study. |
| D34 | pp. 6, 39–40: fraud recourse | Part 0 says credit-only recourse; later text allows false-positive BAF recourse. Evaluation-time true labels cannot be used to identify deployable “safe” recipients. Drop this branch; no evasion guidance. |
| D35 | pp. 4, 6, 40: notice feature budget | ECOA/Reg B does not mandate four reasons or four model features. FCRA score-factor limits apply to particular disclosures, not a general model-feature budget. “K in {4,5} for compliance” is unsupported. |
| D36 | pp. 4, 37: sex/marital/age | Excluding sex/marital status is a prudent research choice. The legal statement must retain specific Reg B exceptions and permitted handling of marital-property rights and age. Taiwan data are not automatically governed by US ECOA. |
| D37 | pp. 4, 6: EU law | Preserve Annex III 5(b)'s fraud exception; do not extend it to exemption from the whole AI Act. Generic financial-document verification is not automatically Annex III creditworthiness scoring. Article 86 explanation rights are distinct from recourse. |
| D38 | pp. 10–11: disputed references | Johansson target-class title not located; excluded. arXiv:2609.39877 is sole-author Shahin Jabbari, not Pawelczyk. Stow, BioMark, SHAP-McNemar identities verified; see reference register. |
| D39 | p. 10: Stow | The “not Kendall tau” wording is too strong: the publisher abstract explicitly reports Kendall tau in addition to ESCR, WRD, entropy. Mean .309/.158/.153 are author-reported, not replicated. |
| D40 | pp. 8, 11: publication years | Wachter's preprint is 2017; Harvard JOLT 31(2):841–887 is 2018. Rawal arXiv first posted 2020, later 2021 publication. Pawelczyk preprint 2022 / ICLR 2023. Distinguish versions. |
| D41 | pp. 41–47: “corrected reference code” | Visual inspection confirms inconsistent indentation and line wrapping within executable statements; do not present it as a tested runnable package. No code executed, repaired, or supplied in this task. |
| D42 | pp. 42–47: remaining guards | Constant correlations are silently filled although prose says drop constants; zero-feature case, empty candidates/reference, <5 neighbors, invalid tau_safe outside (0,1), missing/NaN shifts, zero MAD scales, and empty TRV denominator need specification. These are static-audit observations, not test results. |
| D43 | pp. 37, 40 | All-feature model is a reference, not a guaranteed performance upper bound; redundant inputs can hurt. Native EBM attributions cannot be treated as an explainer for a different XGBoost teacher. |
| D44 | p. 40 versus Part 0 | Six pipelines omit the strongest established robust-recourse controls RobX/ROAR/PROBE despite acknowledging them. This weakens the full COMET research design. |
| D45 | pp. 5, 18, 45 | EBM defaults and monotonize signatures are version-dependent. Documentation snippets do not pin a software environment. Exclude software-runtime assertions from the selected paper. |
| D46 | Part 0 and later expected-table discussion | Retain the correction that a confusion matrix does not determine ROC-AUC; the quoted 0.96 is unsupported and at most an untested hypothesis. Empirical ESVR=0 outside the qualified monotone single-reference game is also a hypothesis, not an unconditional result. Both are explicitly quarantined in the final PDF. |

## Cross-source conflicts and external inconsistencies

| ID | Conflict | Resolution |
|---|---|---|
| C01 | P1/P2 FinDVer landing metadata versus linked paper | Archive both. Linked PDF §§3–4 says 2,100 examples (600 development +1,500 test), 3 subsets, 19 models, and Yuru Jiang; landing metadata says 4,000, 4, 25 and Tintin Jiang. Do not merge versions or infer that these names are identical. Cite inspected PDF and flag unresolved metadata conflict. |
| C02 | P1 favors another temporal pilot; P2 favors a version pilot; P3 proposes a full integrated system | User requests a single decision, so choose version-conditioned evidence evaluation with temporal controls; preserve alternatives in the decision matrix. Source instructions to implement are not followed. |
| C03 | P1 R10 missing authors | Resolved through Crossref DOI record; full author list recorded above. Metadata verification does not independently reproduce policy-regret results. |
| C04 | P2 version novelty versus FinGround full text | Full text already discusses restatements and latest-filing resolution. Add direct latest-only and scoped-authority baselines; novelty is a diagnostic test of policy semantics. |
| C05 | P3 temporal title versus static credit datasets | Reject real temporal credit-survival claims from static cohorts; do not manufacture windows. |
| C06 | P1/P2 eight research weeks versus P3 six weeks including writing | Source plans are suggestions, not binding task instructions. Proposal uses eight research weeks plus two writing/release weeks, with explicit human-review assumptions. |
| C07 | P1 archived rank-fusion null findings versus P3 expected gains | Preserve null source-reported observations. Neither transfers to financial-document verification. All expected performance numbers remain hypotheses. |
| C08 | P3 unconditional model-additive/Owen claim versus conditional SHAP | Restrict theorem to game additivity, as demonstrated by dependent-feature conditional expectations. |
| C09 | Original EU deadline narrative versus official current pages | Commission service desk says its text reflects a 27 July 2026 consolidated version and Article 113 displays Annex III high-risk Section 1–3 application on 2 December 2027. Its linked FAQ still uses proposal language and older dates. EUR-Lex original URLs yielded empty responses. Cite the retrieved clause text for substantive duties, record the dated discrepancy, and do not certify a universal current enforcement deadline. |
| C10 | New-paper metadata versus validity | Verified DOI/arXiv identity is not endorsement of empirical claims, peer review, journal quality, licensing, or reproducibility. Explicitly keep these distinctions. |
| C11 | FinanceReasoning author-name metadata (found during 24 October document checks of records retrieved on 23 October) | `evidence/financereasoning.txt` and its full citation export say Ziyan Ma; `evidence/financereasoning.html` citation metadata says Tzu-Yen Ma. The proposal follows the export and records the disagreement; no unsupported inference that the names identify the same person. |

## Expected-number quarantine

No number below is a result of this review. These source forecasts are retained only as **rejected-branch hypotheses**; none becomes a promised result of the chosen proposal.

| Original forecast | Correct treatment |
|---|---|
| RBO 0.82–0.94 | H-C1: finite-list, chance-adjusted agreement might reach this range under a specified metric; raw and null-adjusted values must not be confused. |
| ESVR 8–22% | H-C2: unconstrained models might exhibit this rate under one defined reference game; not observed. |
| max VIF >14 | H-C3: redundant selections might exceed 14; empirical, not guaranteed. |
| selected VIF <2 | H-C4: selected subsets might meet this target; complete linkage does not prove it. |
| TRV >90% | H-C5: validity might exceed .90 at stated coverage/cost on a suitable dataset; no conformal guarantee. |
| 45–60% invalidation | H-C6: unconstrained recourse invalidation might lie in this interval; unmeasured. |
| +25% TRV | H-C7: ambiguous between relative percent and percentage points; do not test until defined. Illustrative clarified target would be +25 percentage points, explicitly a new assumption. |
| near-zero AP cost | H-C8: monotonicity might preserve AP within a prespecified margin; no “near-zero” result exists. |
| empirical ESVR=0; ROC-AUC 0.96 | H-C12/H-C13: zero sign violations are a theorem only under the qualified reference-game conditions; deployment-wide zero is untested. ROC-AUC 0.96 cannot be derived from a single confusion matrix and remains unsupported. |
| best rho_max=.65–.75; insensitive k0 | H-C9/H-C10: tuning/sensitivity hypotheses, not design guarantees. |
| BILL_AMT correlation ≈.80–.95; expected twin groups | Unverified dataset-specific empirical claims; calculate on a specified clean training split before use. Not established population properties. |
| 30/300 cases; 300–500 rejected applicants; five companies | Sampling/resource design targets, not measured yields or effect sizes. Replaced by transparent gated targets for the selected study. |

## Checks that were retained

The sigmoid/logit examples, LIME toy slope 0.60/0.52≈1.153846, complete-linkage toy merges, two-variable VIF values, Owen factorial weights, centrality products, RRF toy ordering, RBO tail correction, PAVA toy pooling, MAD cost 3.7+2=5.7, KNN composite costs 4.4 and 5.75, and Holm worked decisions are arithmetically consistent at displayed precision. The ordinary Shapley game requires v(empty)=0; several examples use synthetic numbers and remain explicitly labeled as such. No illustrative number was promoted to experimental evidence.

## Remaining verification limits

The exact Johansson title was not found in the searched records; absence is not proof of nonexistence. HELOC's 9,871 cleaned-row claim and field-specific special-code dictionary were not independently tied to the same version. Source experimental artifacts were not supplied. The current EU transition date remains subject to the official-page inconsistency described above. SHAP-McNemar publisher full text was blocked, although DOI metadata was verified. Proposed natural amendment yield, expert agreement, and baseline performance are untested by design. These limitations are stated in the PDF; they do not justify inventing supporting evidence.

## Final document checks — 24 October 2026

The proposal was typeset with XeLaTeX as a 44-page PDF, with a linked table of contents, 48 bibliography entries, numbered tables and a pipeline figure. Citation destinations, page references, embedded fonts, extracted text, and representative rendered pages were checked. No research implementation, model training, experiment, or deployment was performed. LaTeX and PDF utilities were used only to prepare and validate the requested documents.

Final specification checks kept unresolved operand interpretations in the admissible set (with an unbounded interval), preventing accidental support from dropping incomplete alternatives. Distinct symbols are used for the authority graph, issuer count, accounting concept, and sign-test planning probability. Score totals, example arithmetic, subsampling correction, and the minimum attainable sign-test p-values were checked. Sample-size, coverage, cost, and workload figures remain assumptions or hypotheses. The natural correction corpus and independent reviewer are future study requirements, not acquired resources.
