# Next steps and publication plan

Written 26 October 2026 (Monday). Midterm: Wednesday 28 October. Team: you and Shreya. Supervisor: Prof. Rahul Gupta (IT, DTU).

**The plan in one line:** present the midterm with the slides and working demo → get Prof. Gupta's approval for the topic change → run free AI models → hand-check 20 companies → write a 4-page paper → submit to **FNP 2027 (EACL workshop), deadline 15 December 2026**. If it's rejected, revise and submit to **BDA 2027 (Springer LNCS), deadline 15 February 2027**.

Expected effort after the midterm: about **5–7 hours per person per week for 7 weeks**.

---

## A. Before the midterm (next 48 hours, about 4 hours each)

| # | Task | Who | Time | How |
|---|---|---|---|---|
| 1 | Read the study guide, Sections 1, 4, 5 and 9 | Both | 60 min | `docs/1_STUDY_GUIDE.md` |
| 2 | Put your name on slide 1 | You | 2 min | Open `midterm/Midterm_Presentation.pptx`, edit "[Your name]" |
| 3 | Rehearse with the speaker notes. Split it: you do slides 1–8, Shreya 9–15 | Both | 60 min | In PowerPoint: View → Notes. The notes are written in simple, speakable language. |
| 4 | Practise the live demo | You | 10 min | Double-click `code/1_RUN_PILOT_DEMO.bat`. It runs in 5 seconds and prints the accuracy table plus "Check passed". Show this during slide 9. |
| 5 | **Strongly recommended:** add a real AI result | You | 20 min | Get a free Gemini key (`code/README.md`), paste it into `code/settings.txt`, double-click `code/3_RUN_AI_TEST.bat`, choose `gemini` and `pilot`. Then double-click `midterm/REBUILD_SLIDES.bat`, which adds a "Result 3: AI models" slide automatically. |
| 6 | Upload the work to GitHub so both of you have it | You or Shreya | 10 min | See the commands in Section G. `settings.txt` (your key) is excluded automatically. |
| 7 | Prepare the topic-change explanation | Both | 15 min | Study guide Section 5 and slide 2 |

If something breaks before the midterm, the slides and the pilot demo work **without** internet or an AI key.

---

## B. At the midterm or right after: what to ask Prof. Gupta

You changed the topic from XAI fraud detection, so you need his explicit agreement. Ask these five questions directly:

1. **Approval:** "Can we continue with this topic instead of the XAI fraud project?"
2. **Venue:** "We're targeting the FNP 2027 workshop at EACL (deadline 15 Dec) or, as a backup, an IEEE or Springer conference. Is that acceptable, or do you prefer a Scopus-indexed Indian conference?" Some departments only count Scopus or IEEE publications.
3. **Reviewer:** "Could you, or a colleague who knows accounting, review 30 short claims for about 2 hours?" Send them `pilot/reviewer_pack.zip`, which contains no answers. One independent human review makes the labels far more credible.
4. **Authorship:** "Would you like to be a co-author?" Supervisors are normally the last author. This also means he'll review the draft, which raises acceptance chances.
5. **DTU requirements:** the format of the midterm and final reports, and any plagiarism-check (Turnitin) rules.

---

## C. The 7-week plan to submission

| Week (2026) | Goal | Tasks | Who | Hours each |
|---|---|---|---|---|
| **1:** 29 Oct – 4 Nov | AI results | Get the Gemini and Groq keys. Run `3_RUN_AI_TEST.bat` for both providers on `pilot` and `auto`. Both conditions run automatically. That's 4 runs, about 30 minutes each, unattended. Send the reviewer pack to the reviewer. | You run; Shreya sends the pack | 3 |
| **2:** 5 – 11 Nov | Verified subset | Open `code/data/auto/families.csv` in Excel. For 20 families (10 each), click the SEC links and confirm three things: the original value, the corrected value, and that the 8-K notice covers that fiscal year. Fill `check_*` with Y/N. Check flagged rows first. Remove or fix bad families. | Split 10/10 | 4–5 |
| **3:** 12 – 18 Nov | Analysis | Read the AI models' wrong answers (the `reason` column in `code/results/llm_*.csv`). Group them: used a future document; chose the latest instead of the original; fell for a "previously reported" column; wrong metric; rounding. Count each type. Merge in the reviewer's pilot feedback. | Both | 5 |
| **4:** 19 – 25 Nov | First draft | Write the paper on Overleaf using the ACL template (Section D). You write Data and Results; Shreya writes Introduction and Related Work (adapt `docs/2_LITERATURE_SURVEY.md` in your own words). | Split | 7 |
| **5:** 26 Nov – 2 Dec | Feedback | Send the draft to Prof. Gupta. Run one extra model if time allows, for example a small Llama 8B, to show the effect of model size. | Both | 4 |
| **6:** 3 – 9 Dec | Polish | Revise from feedback. Check the page limit, anonymity, Limitations section, references and figures. Prepare the anonymous code and data link. | Both | 5 |
| **7:** 10 – 15 Dec | Submit | Submit by **12 December** (3-day buffer) on the FNP submission site. | You | 2 |

**After submission:** FNP notification is 5 January 2027. If accepted, prepare the camera-ready version (due 19 January) and register. If rejected, use the reviews to revise and submit to BDA 2027 (15 February 2027, Springer LNCS, 16 pages, so you can add more detail).

**Deliberately not doing these, to save time:** the full 600-claim study from the proposal, training any model, paid AI services, building a website or app, adding the XAI or fraud components back, and quarterly or segment-level data. Mention them as future work.

---

## D. What the paper should look like

**Format:** the ACL template on Overleaf. Search "ACL Rolling Review template" in the Overleaf gallery. A **short paper is 4 pages** plus unlimited references and a mandatory Limitations section. Submissions are anonymous: no names, no "our DTU lab", and anonymised links.

**Working title:** *Which Number Counts? A Policy-Conditioned Benchmark for Verifying Financial Claims Across Restatements*

| Section | Length | Content | Where the material already is |
|---|---|---|---|
| Abstract | 150 words | Problem, benchmark, main AI finding | Write last |
| 1 Introduction | 0.6 page | The SunPower example; why "newest wins" is wrong for some questions; 3 contributions | Study guide 1 and 4.1; slides 3 and 11 |
| 2 Related work | 0.5 page | Four paragraphs plus the gap | `docs/2_LITERATURE_SURVEY.md` |
| 3 Task | 0.5 page | Inputs, the 4–5 policies, S/C/U, rounding rule | Study guide 4.2–4.3; `pilot/protocol_v1.md` |
| 4 Dataset | 0.7 page | Pilot (hand-checked) plus automatic SEC pipeline; statistics table; human-verification results | Study guide 4.5–4.6; `code/data/auto/families.csv` |
| 5 Experiments | 0.3 page | Rules B1–P; 2–3 LLMs × {full, bare}; metrics | Study guide 4.4 |
| 6 Results | 0.9 page | Main table (from `code/results/SUMMARY.md`); a per-policy chart; error types with 2 examples | Week 3 analysis |
| 7 Conclusion | 0.2 page | What we found; future work | — |
| Limitations | Unlimited | Study guide Section 7 | Study guide 7 |
| Ethics statement | Short | Public data only; no personal data; labels aren't accusations of misconduct | Proposal Section 13 |

**The main results table should have these rows:** the five rules plus each LLM under each condition. Columns: overall accuracy, company-level accuracy, accuracy per policy, false-support rate, and "same as newest-wins" for the bare condition. `summarize.py` already produces all of these.

---

## E. How to maximise the chance of acceptance

Honest odds: workshops like FNP typically accept roughly half of submissions. There's **no guarantee**; nobody can promise acceptance. These things move the odds most:

1. **A clear, honest contribution.** Say "benchmark + evaluation", not "novel algorithm". Reviewers punish over-claiming much more than modest claims.
2. **A concrete motivating example** in the first paragraph (SunPower). Reviewers decide quickly.
3. **A human-verified subset.** Report "20 of 40 families checked by hand; X% confirmed". This is the single biggest credibility boost.
4. **More than one AI model**, for example Gemini plus Llama, under both conditions, with **error analysis showing real wrong answers**.
5. **Released code and data.** Use an anonymous link for review (for example anonymous.4open.science, which mirrors a GitHub repo anonymously) and the real GitHub after acceptance.
6. **Strong baselines are included.** The B4 and B4W rules show you aren't just beating a weak method.
7. **Clear limitations** (study guide Section 7).
8. **The supervisor reads the draft** before submission.
9. **No sloppiness.** Correct citations, consistent numbers between text and tables, figures readable in black and white, and within the page limit.

---

## F. Integrity: important because AI assisted this work

- **You must understand and stand behind every sentence and number.** Read the study guide fully and rerun the code yourself.
- **Write the paper in your own words.** Don't paste AI-generated paragraphs unchanged, including those in `docs/2_LITERATURE_SURVEY.md`. DTU's plagiarism checks and the reviewers both matter.
- **Disclose AI assistance** as the venue requires. ACL venues require authors to take full responsibility, don't allow AI as an author, and ask for disclosure of substantial AI use. Read the current FNP/EACL call for the exact wording and add an acknowledgement if required.
- **Never claim a review that didn't happen.** If no independent reviewer checks the pilot, say "labels drafted by the authors". If you check 20 families, say exactly 20.
- **Never invent results.** All AI-model numbers must come from `code/results/` files produced by actually running the scripts.
- **Keep API keys private.** They live only in `code/settings.txt`, which git ignores.

---

## G. Uploading to GitHub

The repository belongs to Shreya's GitHub account (`Shreya732-debug/Research-Work`). To upload today's work, either Shreya adds you as a collaborator (GitHub → repository → Settings → Collaborators), or she runs these commands on her laptop after copying the folders. In a terminal inside the `Research-Work` folder:

```
git add code docs midterm README.md
git commit -m "Add working verifier code, automatic SEC dataset, study guide and midterm slides"
git push
```

`code/settings.txt` and `code/cache/` are excluded automatically by `code/.gitignore`.

---

## H. If something goes wrong

| Problem | What to do |
|---|---|
| `python` is not recognised | Reinstall Python from python.org with "Add Python to PATH" ticked |
| The AI provider says the model name is invalid | Run `python run_llm.py --provider gemini --list-models` in `code/`, then copy a name into `settings.txt` |
| "Rate limit" messages | Normal on free tiers; the script waits and retries. Raise `SECONDS_BETWEEN_CALLS` to 10 in `settings.txt`. |
| The SEC download fails | Check `SEC_EMAIL` in `settings.txt`, wait 10 minutes and rerun. Downloads are cached, so reruns are fast. |
| A hand-checked family is wrong | Note it in `check_notes`. Delete that family's rows from the three files in `code/data/auto/`, or ask an AI assistant to add an exclusion list to `build_dataset.py`. |
| The AI models score near 100% | That's still a result: explicit policies make the task solvable. Emphasise the bare condition and the error types. The proposal's "negative result" route applies. |
| The reviewer doesn't reply | Proceed with your own blind double-check: Shreya labels 30 pilot claims without looking at the answers, then compare. Report it honestly as "author double-annotation". |
