# Your practical next steps

Updated 26 October 2026. Keep the final proposal as the blueprint. The current deliverable is a **30-case draft pilot across five issuers**, with original-source links and a manual comparison of reference rules. No verifier has been built, no model experiment has run, and no independent human review has been completed.

## 1. Download the review pack

Open [Download reviewer_pack.zip](https://raw.githubusercontent.com/Shreya732-debug/Research-Work/main/pilot/reviewer_pack.zip). In Windows, right-click the downloaded ZIP and choose **Extract All**. The extracted folder contains instructions, a blank worksheet, neutral source locators, document metadata, and a time log.

If the link opens a GitHub preview instead, use **Download raw file**. The separate [full pilot bundle](https://raw.githubusercontent.com/Shreya732-debug/Research-Work/main/pilot/pilot_bundle.zip) includes provisional answers and analysis. **Do not send the full bundle to the independent reviewer before their first pass.**

## 2. Arrange the independent review — your hands-on task

Ask your faculty supervisor, a finance/accounting faculty member, or another person competent in reading financial statements to review the pack. A friend who can only match numbers is insufficient for attribution, restatement and non-reliance questions. If you cannot find a qualified reviewer, tell your supervisor that the pilot is awaiting review; do not substitute an AI answer for independent human validation.

You can send this message yourself:

> I am preparing a B.Tech research pilot on financial-claim verification across disclosure versions and historical cutoffs. Could you independently review these 30 short claims using the linked SEC filings? Please use only the attached reviewer pack on your first pass, record your evidence and actual time, and declare whether you have seen our proposed labels. The project needs critical review, including corrections and ambiguities; no particular answers are expected.

Send **reviewer_pack.zip** and agree on a realistic return date. The time needed is currently unknown; ask them to time the first six cases and then estimate the remaining work. Participation, available time, actual subject expertise and supervisory approval require real people; I cannot provide those on their behalf or certify that they worked independently.

You may practice reviewing cases yourself. If you have already seen the labels, record that exposure. Your practice remains useful but does not count as blinded independent review.

## 3. Open and complete the files

The reviewer should read `reviewer_instructions.md` and `source_cards.md` first. Markdown files open as plain text in Notepad or in GitHub; no coding tools are needed.

In Excel, choose **Data → From Text/CSV**, select `reviewer_worksheet.csv`, choose UTF-8 and comma separation, and import `issuer_cik`, case IDs and date columns as **Text**. This preserves leading zeros and exact dates. In Google Sheets, use **File → Import → Upload** and turn off automatic conversion of text to numbers/dates if that option is offered. Use an institution-approved account if required.

Leave the claim and policy columns unchanged. Fill the blank review columns, use an alias such as R1, and cite the exact source/note/row/year. Record uncertain expertise or inaccessible documents in review status rather than guessing. Log shared reading time separately in `review_session_log.csv`.

Open the SEC links in a normal browser. Use Ctrl+F for the statement/note names in the source cards, then check the year column and units. If SEC access fails, try the filing's index link; otherwise mark `needs_source` and tell me the source ID. Do not replace a filing with an uncited web summary.

Save the first-pass worksheet as **reviewer_R1_v1.csv** using CSV UTF-8, and keep an unchanged copy. Return it with the time log. The CSV format stores values rather than workbook formatting; that is expected.

## 4. Return the review for adjudication

Upload the completed CSV and time log in this chat. Remove names, emails and other personal details first. Tell me if the reviewer saw any draft labels before finishing. Do not manually force their answers to match ours.

I can then check completeness, compare proposed and reviewed answers, assemble a disagreement table, and help produce a versioned adjudicated pilot. A real supervisor/reviewer must decide unresolved accounting or interpretation questions. For a disagreement, retain the draft answer, independent answer, cited evidence, adjudicator alias and reason for the final decision. Do not erase the original disagreement.

One human review of an assistant draft is useful validation, but it is **not human–human inter-annotator agreement**. If the paper reports that statistic, arrange a second independent human first pass before either sees the other's answers. With five related issuer groups, any agreement estimate is exploratory.

## 5. Meet the supervisor after review

Bring the original proposal, [pilot assessment](pilot_assessment.md), reviewed worksheet and unresolved cases. Ask the supervisor to confirm the project timetable, available reviewers, institutional requirements, and contribution/authorship expectations. Choose a target venue after assessing the evidence and current related work; publication is not assured by combining topics.

The immediate scientific decision is whether the data support a distinctive benchmark or an advantage beyond strong simple rules. In this draft, a simple policy-aware rule plus a withdrawal flag already matches the proposed resolver. Do not add explainability, conformal prediction or another component solely to make the title broader; each addition needs a separate question and evaluation.

## What I can continue doing

I can expand the candidate-source screening, inspect closer literature and available benchmark releases, maintain the evidence and adjudication records, and design the next comparison. Those are research tasks, not work you need to do manually because I cannot access a person. The broader acquisition target is still 20 eligible correction families across at least 10 issuers; the current five families do not satisfy it.

Do not start the proposed 600-claim collection, pay for model APIs, train a model or install a research software stack yet. After the pilot review and broader screening gate, we can freeze the evaluation contract and decide what implementation is justified. **Your immediate action is to arrange one competent independent review and return the completed worksheet.**
