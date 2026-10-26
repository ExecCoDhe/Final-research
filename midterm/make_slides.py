"""Build the midterm presentation from the latest results.

Run:  python make_slides.py   (after code/1_RUN_PILOT_DEMO.bat and 2_BUILD_DATASET.bat)
"""

import glob
import os
import sys

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from common import RESULTS_DIR, read_csv  # noqa: E402
from scoring import score  # noqa: E402

NAVY = RGBColor(0x1F, 0x2A, 0x44)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
GREY = RGBColor(0x55, 0x5F, 0x6D)
LIGHT = RGBColor(0xEE, 0xF4, 0xF3)
RED = RGBColor(0xB4, 0x23, 0x18)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def rule_stats(dataset):
    path = os.path.join(RESULTS_DIR, f"rules_{dataset}.csv")
    if not os.path.exists(path):
        return None
    rows = read_csv(path)
    return {rule: score(rows, rule) for rule in ["B1", "B3", "B4", "B4W", "P"]}, len(rows), len({r["family_id"] for r in rows})


def add_text(slide, text, left, top, width, height, size=20, color=NAVY, bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.word_wrap = True
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        p.text = line
        p.alignment = align
        p.space_after = Pt(8)
        for run in p.runs:
            run.font.size = Pt(size)
            run.font.color.rgb = color
            run.font.bold = bold
    return box


def new_slide(title, notes=""):
    slide = prs.slides.add_slide(BLANK)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    add_text(slide, title, 0.5, 0.2, 12.3, 0.8, size=30, color=WHITE, bold=True)
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


def bullets(slide, items, left=0.6, top=1.4, width=12.1, height=5.6, size=20):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.word_wrap = True
    for i, item in enumerate(items):
        level = 1 if item.startswith("  ") else 0
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        p.text = ("• " if level == 0 else "– ") + item.strip()
        p.level = level
        p.space_after = Pt(10)
        for run in p.runs:
            run.font.size = Pt(size - 2 * level)
            run.font.color.rgb = NAVY if level == 0 else GREY
    return box


def card(slide, left, top, width, height, heading, body, fill=LIGHT, heading_color=TEAL, size=16):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = heading_color
    frame = shape.text_frame
    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.TOP
    frame.margin_left = frame.margin_right = Inches(0.25)
    frame.margin_top = Inches(0.2)
    p = frame.paragraphs[0]
    p.text = heading
    p.alignment = PP_ALIGN.LEFT
    p.space_after = Pt(10)
    p.runs[0].font.size = Pt(size + 2)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = heading_color
    for line in body if isinstance(body, list) else [body]:
        q = frame.add_paragraph()
        q.text = line
        q.alignment = PP_ALIGN.LEFT
        q.space_after = Pt(6)
        for run in q.runs:
            run.font.size = Pt(size)
            run.font.color.rgb = NAVY
    return shape


def table(slide, rows, left, top, width, col_widths, size=14, height=0.45):
    shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(left), Inches(top), Inches(width), Inches(height * len(rows)))
    tbl = shape.table
    for j, w in enumerate(col_widths):
        tbl.columns[j].width = Inches(w)
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            cell = tbl.cell(i, j)
            cell.text = str(value)
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(size)
                    run.font.bold = i == 0
                    run.font.color.rgb = WHITE if i == 0 else NAVY
            cell.fill.solid()
            cell.fill.fore_color.rgb = TEAL if i == 0 else (LIGHT if i % 2 else WHITE)
    return tbl


def accuracy_chart(slide, stats, left, top, width, height, title):
    names = ["B1 context only", "B3 latest", "B4 policy-aware", "B4W + withdrawal", "P reference"]
    data = CategoryChartData()
    data.categories = names
    data.add_series("Accuracy (%)", [round(100 * stats[r]["accuracy"], 1) for r in ["B1", "B3", "B4", "B4W", "P"]])
    chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(left), Inches(top),
                                   Inches(width), Inches(height), data).chart
    chart.has_legend = False
    chart.has_title = True
    chart.chart_title.text_frame.text = title
    chart.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(16)
    chart.value_axis.maximum_scale = 115
    chart.value_axis.major_unit = 20
    chart.value_axis.has_major_gridlines = False
    chart.value_axis.minimum_scale = 0
    chart.value_axis.tick_labels.font.size = Pt(12)
    chart.category_axis.tick_labels.font.size = Pt(12)
    plot = chart.plots[0]
    plot.has_data_labels = True
    plot.data_labels.number_format = '0.0"%"'
    plot.data_labels.number_format_is_linked = False
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.font.size = Pt(13)
    plot.series[0].format.fill.solid()
    plot.series[0].format.fill.fore_color.rgb = TEAL


pilot = rule_stats("pilot")
auto = rule_stats("auto")
if not pilot:
    sys.exit("Run code/1_RUN_PILOT_DEMO.bat first.")
pilot_stats, pilot_n, pilot_companies = pilot

# 1. Title
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()
add_text(s, "Which Number Counts?", 0.8, 1.6, 11.7, 1.0, size=44, color=WHITE, bold=True)
add_text(s, "Verifying financial claims when companies correct their published reports",
         0.8, 2.6, 11.7, 1.0, size=26, color=RGBColor(0xB8, 0xE0, 0xDA))
add_text(s, ["Midterm review, B.Tech Major Project",
             "Shreya  |  [Your name]",
             "Supervisor: Prof. Rahul Gupta, Department of Information Technology, Delhi Technological University"],
         0.8, 4.4, 11.7, 2.0, size=20, color=WHITE)
s.notes_slide.notes_text_frame.text = (
    "Good morning. Our project asks a simple question: when a company publishes a financial number and "
    "later corrects it, which number should a fact-checking system, or an AI chatbot, treat as true? "
    "We will show the problem, what we built so far, our first results, and our plan to publish.")

# 2. Why we changed topic
s = new_slide("Why we changed from 'Explainable AI for fraud detection'",
              "Our earlier idea was explainable AI for financial fraud detection. When we audited it, we found three "
              "problems: the main ideas such as SHAP, LIME and grouped explanations are already well studied; the "
              "public credit datasets are static or synthetic, so the time-based claims could not be tested honestly; "
              "and several legal claims in the original plan, such as a required four-feature explanation, turned out "
              "to be wrong. The new topic keeps the finance domain but uses real public data and has a clear yes/no "
              "research question that can be tested on a laptop.")
card(s, 0.6, 1.5, 5.9, 5.3, "Old idea: XAI for fraud and credit",
     ["• SHAP, LIME and grouped explanations are already well studied",
      "• Credit datasets (HELOC, Taiwan) are static and fraud data (BAF) is synthetic, so real 'over time' claims can't be tested",
      "• Legal claims (e.g. 'law requires 4 reasons') were not supported by the regulation text",
      "• High risk of being judged 'not novel'"], fill=RGBColor(0xFB, 0xEE, 0xEC), heading_color=RED, size=19)
card(s, 6.8, 1.5, 5.9, 5.3, "New idea: version-aware claim verification",
     ["• Same domain (finance + AI), so our earlier reading still helps",
      "• Uses real, free, public data: US SEC filings",
      "• One clear, testable question with a measurable answer",
      "• No GPU and no paid data needed",
      "• A known gap: even recent systems simply take the latest number"], size=19)

# 3. The problem in one example
s = new_slide("The problem in one real example: SunPower, fiscal 2022",
              "This is a real case. SunPower published its annual report in March 2023 saying it earned 56.0 million "
              "dollars for stockholders. In October 2023 it filed a notice saying investors should no longer rely on "
              "that report. In December 2023 it filed a corrected report saying 42.8 million. Now take the sentence "
              "'SunPower earned 56.0 million in 2022'. Is it true? It depends on what you mean: it is true about the "
              "original report, false about the corrected accounts, and on 25 October 2023 nobody could know the "
              "right number yet. A fact checker has to know WHICH version the question is about.")
steps = [("10 Mar 2023", "Annual report (10-K)", "Net income: $56.037 M"),
         ("24 Oct 2023", "Warning notice (8-K Item 4.02)", "'Should no longer be relied upon'"),
         ("18 Dec 2023", "Corrected report (10-K/A)", "Net income: $42.849 M")]
for i, (when, what, value) in enumerate(steps):
    card(s, 0.6 + i * 4.2, 1.5, 3.9, 2.0, when, [what, value], size=16)
add_text(s, "Claim: \"SunPower earned $56.037 M for stockholders in fiscal 2022.\"  Is it true?", 0.6, 3.8, 12, 0.6, size=20, bold=True)
table(s, [["The question really means…", "Correct answer"],
          ["What did the ORIGINAL report say?", "S: supported"],
          ["What do the CORRECTED accounts say?", "C: contradicted"],
          ["What was reliably known on 25 Oct 2023?", "U: undetermined (withdrawn, no replacement yet)"]],
      0.6, 4.4, 12.1, [7.0, 5.1], size=16)

# 4. Basic concepts
s = new_slide("Five terms you need (no finance background assumed)",
              "Quick vocabulary. The SEC is the US regulator; every listed company must file reports on its public "
              "website called EDGAR. A 10-K is the yearly report. A 10-K/A is an amended version. An 8-K with "
              "Item 4.02 is the official warning that old statements are wrong. A restatement is the correction "
              "itself. XBRL is the machine-readable tagging inside these reports, which is what lets our code read "
              "numbers automatically.")
table(s, [["Term", "Plain meaning"],
          ["SEC / EDGAR", "US market regulator and its free public website of company filings"],
          ["10-K", "A company's official yearly financial report (audited)"],
          ["10-K/A", "An amended (corrected) version of a 10-K"],
          ["8-K Item 4.02", "Official notice: 'our earlier statements should no longer be relied upon'"],
          ["Restatement", "Re-publishing old numbers after finding an error"],
          ["XBRL", "Machine-readable tags on each number (concept, period, unit), so code can read filings"]],
      0.6, 1.5, 12.1, [3.0, 9.1], size=17, height=0.62)

# 5. Task definition
s = new_slide("Our task, precisely",
              "Formally, the system receives four things: the claim sentence, an authority policy that says which "
              "version counts, a cutoff date, and a fixed packet of documents. It must answer S, C or U. The same "
              "packet is given to every method, so differences come from reasoning, not from better searching.")
card(s, 0.6, 1.5, 5.6, 5.2, "Input",
     ["1. Claim: 'Company X earned $Y M in year Z'",
      "2. Authority policy: original / corrected / as-known-at-cutoff / unspecified",
      "3. Cutoff date: documents filed on or after it don't count",
      "4. Evidence packet: the same filings for every method"])
card(s, 6.6, 1.5, 6.1, 5.2, "Output: one label",
     ["S = Supported by the figure the policy selects",
      "C = Contradicted (figure is clearly different)",
      "U = Undetermined (ambiguous, withdrawn, or rounding prevents a decision)",
      "",
      "Rounding rule: '$56.037 M' means anything in [56.0365, 56.0375]",
      "Errors are counted per company, not just per claim"])

# 6. Related work
s = new_slide("What already exists, and the gap",
              "Many datasets test whether AI can do financial maths, such as FinQA and TAT-QA, or check claims against "
              "one document, such as FinDVer. Recent 2026 systems such as VeriFin and FinGround check numbers against "
              "XBRL. But FinGround explicitly picks the most recent filing when numbers conflict, and FinVerBench "
              "throws away companies with restatements. No benchmark we found asks the same claim under different "
              "versions of the truth. That is our gap.")
table(s, [["Work (year)", "What it does", "What it misses for us"],
          ["FinQA, TAT-QA (2021)", "Numerical questions on financial reports", "Assume one correct document"],
          ["FinDVer (EMNLP 2024)", "Verify claims against a long financial document", "Single document, no versions"],
          ["VeriFin (2026)", "Checks LLM financial claims against XBRL with a solver", "No original-vs-corrected policies"],
          ["FinGround (2026)", "Grounds claims; flags restatement conflicts", "Defaults to the LATEST filing"],
          ["FinVerBench (2026)", "Benchmarks statement-consistency checking", "Excludes restated companies"],
          ["ChronoFact (IJCAI 2025)", "Timeline-based fact verification", "Events, not corrected accounts"],
          ["AmbiFC (TACL 2024)", "Claims with ambiguous evidence", "Not financial versions"]],
      0.6, 1.4, 12.1, [3.2, 4.8, 4.1], size=14, height=0.62)

# 7. Work done
auto_line = (f"Automatic dataset builder: {auto[2]} companies, {auto[1]} claims from real SEC restatements"
             if auto else "Automatic dataset builder from SEC data")
s = new_slide("Work completed so far",
              "Here is what is done. We audited three earlier research directions and verified 48 references "
              "against official records. We built a 30-claim pilot by hand from 11 real SEC filings of five "
              "companies. We wrote working Python code that turns the rules into a program, reproduces every hand "
              "decision, and automatically builds a much larger dataset from free SEC data.")
bullets(s, ["Literature audit: 3 candidate directions compared; 48 references checked against official records",
            "Written protocol: 5 authority policies, rounding rules, leakage controls (44-page proposal)",
            f"Hand-checked pilot: {pilot_n} claims, {pilot_companies} companies, 11 SEC filings, with exact sources",
            "Working code (Python):",
            "  5 rule-based verifiers that reproduce all 150 hand-made decisions exactly",
            "  " + auto_line,
            "  AI-model test harness for free models (Gemini, Llama via Groq): ready to run",
            "Verified the closest competing papers exist (arXiv) and identified target venues"], size=19)

# 8. Methods compared
s = new_slide("The methods we compare",
              "We compare simple rules that each ignore one thing. B1 ignores dates and policies. B3 always takes the "
              "newest number before the cutoff, like FinGround's default. B4 respects the policy but ignores warning "
              "notices. B4W adds a check for warning notices. P is our full reference resolver. Next we add AI "
              "language models to the same table.")
table(s, [["Method", "Uses dates?", "Uses policy?", "Uses warning notices?", "Idea"],
          ["B1 context-only", "No", "No", "No", "Any matching number in the documents"],
          ["B3 latest-before-cutoff", "Yes", "No", "No", "Newest number wins (like FinGround's default)"],
          ["B4 policy-aware", "Yes", "Yes", "No", "Respects original / corrected question"],
          ["B4W + withdrawal flag", "Yes", "Yes", "Yes", "Also notices '8-K Item 4.02'"],
          ["P reference resolver", "Yes", "Yes", "Yes", "Full scoped correction logic"],
          ["AI models (next step)", "?", "?", "?", "Gemini / Llama, with and without the policy"]],
      0.6, 1.5, 12.1, [3.0, 1.6, 1.6, 2.2, 3.7], size=15, height=0.65)

# 9. Pilot results
s = new_slide(f"Result 1: hand-checked pilot ({pilot_n} claims, {pilot_companies} companies)",
              "On the 30 hand-checked claims, ignoring time and policy gives only 40 percent. Always taking the latest "
              "number gives 73 percent: it fails every 'what did the original report say' question. Adding the policy "
              "fixes almost everything; only the SunPower warning-notice case fails. Adding the warning flag reaches "
              "100 percent. Our code reproduces every decision made by hand, which validates the implementation.")
accuracy_chart(s, pilot_stats, 0.5, 1.3, 7.6, 5.8, "Accuracy against draft labels")
card(s, 8.4, 1.5, 4.4, 5.4, "What this shows",
     ["• Ignoring which version is asked about gives wrong answers",
      "• 'Latest number wins' fails every 'original report' question",
      "• Warning notices (8-K 4.02) matter: B4 misses the SunPower gap",
      "• Code reproduces all 150 hand decisions",
      "• Labels are drafts awaiting human review"], size=15)

# 10. Auto dataset results
if auto:
    auto_stats, auto_n, auto_companies = auto
    s = new_slide(f"Result 2: automatic SEC dataset ({auto_n} claims, {auto_companies} companies)",
                  "Our builder read 1,600 SEC search results from 2019 to 2024 containing the phrase 'should no "
                  "longer be relied upon', kept official Item 4.02 notices from real operating companies, about 520 "
                  "companies, and stopped after finding 40 whose annual net income was later corrected, for example Shake Shack, Discover, "
                  "TransUnion and Lovesac. We checked Shake Shack's notice by hand: it matches. The same pattern "
                  "appears at scale. Important: these labels are produced by rule P, so P is 100 percent by design. "
                  "This dataset is for testing AI models, and we will hand-check a sample.")
    accuracy_chart(s, auto_stats, 0.5, 1.3, 7.6, 5.8, "Accuracy against silver (rule-generated) labels")
    card(s, 8.4, 1.5, 4.4, 5.4, "What this shows",
         ["• Pipeline finds real restatements automatically from free SEC data",
          "• 'Latest wins' fails all 'original report' and 'unspecified' claims",
          f"• Ignoring warnings fails {auto_stats['B4']['errors']} of {auto_n} claims",
          "• P = 100% by construction (silver labels)",
          "• Spot-check: Shake Shack 8-K confirmed"], size=15)

# Optional: AI model results, added automatically once code/3_RUN_AI_TEST.bat has been run
llm_rows = [["Model and condition", "Dataset", "Claims", "Accuracy", "Wrong policy answers"]]
for path in sorted(glob.glob(os.path.join(RESULTS_DIR, "llm_*.csv"))):
    if path.endswith("_report.csv"):
        continue
    preds = read_csv(path)
    stats = score(preds, "prediction")
    if not stats:
        continue
    _, dataset, rest = os.path.basename(path)[:-4].split("_", 2)
    worst = min(stats["by_policy"].items(), key=lambda kv: kv[1][0] / kv[1][1])
    llm_rows.append([rest.replace("_", " "), dataset, stats["n"], f"{stats['accuracy']:.1%}",
                     f"weakest: {worst[0]} ({worst[1][0]}/{worst[1][1]})"])
if len(llm_rows) > 1:
    s = new_slide("Result 3: free AI language models on the same claims",
                  "These are the first AI model results. 'full' means the model was told the policy and cutoff; "
                  "'bare' means it only saw the claim and documents. The last column shows the policy where each "
                  "model made the most mistakes. Explain one concrete example of a wrong answer from the results "
                  "file in code/results.")
    table(s, llm_rows, 0.6, 1.5, 12.1, [4.2, 1.4, 1.3, 1.6, 3.6], size=15, height=0.6)

# 11. Key insight
s = new_slide("Key insight: we contribute a benchmark, not a new algorithm",
              "An important honest finding: a simple policy-aware rule plus a warning-notice flag already matches our "
              "full resolver. So we will not claim a new algorithm. Our contribution is the benchmark itself, the "
              "evaluation protocol, and testing whether modern AI models handle these version questions. That is "
              "publishable as a dataset and evaluation paper.")
card(s, 0.6, 1.5, 12.1, 2.2, "Finding",
     ["A simple rule (policy-aware + warning flag) is as good as our full resolver on all current cases. "
      "So claiming a 'novel algorithm' would be dishonest and reviewers would reject it."], size=18)
card(s, 0.6, 4.0, 12.1, 2.8, "Therefore our paper's contribution",
     ["1. A new benchmark: the same claim judged under different authority policies, built from real SEC restatements",
      "2. An automatic, reproducible pipeline that anyone can rerun from free SEC data",
      "3. An evaluation of AI language models: do they pick the right version of a number, with and without instructions?"], size=17)

# 12. Next steps
s = new_slide("Next steps (in order)",
              "Next we run the AI models, which needs only a free key and the scripts we already have. Then we "
              "hand-check a sample of the automatic dataset, about 20 companies, using the SEC links in the "
              "spreadsheet. Then we write a 4 to 8 page paper. Our target is the FNP 2027 workshop at EACL, "
              "deadline 15 December 2026, with Indian Springer and IEEE conferences as backups.")
table(s, [["When", "Task", "Output"],
          ["Week 1", "Run 2 free AI models (Gemini, Llama) on pilot + 279 claims, with and without policy", "AI accuracy table"],
          ["Week 1–2", "Hand-check 20 companies' numbers and warning notices against SEC links", "Verified 'gold' subset"],
          ["Week 2", "Ask Prof. Gupta / a finance faculty to review 30 pilot labels", "Independent review"],
          ["Week 3", "Error analysis: where and why AI models fail", "Figures + examples"],
          ["Week 3–5", "Write paper (ACL 4–8 pages), internal review, submit", "Submission"]],
      0.6, 1.5, 12.1, [1.6, 7.3, 3.2], size=15, height=0.7)

# 13. Publication plan
s = new_slide("Publication plan",
              "Venues. The best fit is FNP, the Financial Narrative Processing workshop at EACL 2027. It explicitly "
              "invites datasets, benchmarks and negative results, and short papers of four pages. Deadline "
              "15 December 2026. Backups: SANKALP 2027, an IEEE conference at IIIT Gwalior, deadline 30 November; and "
              "BDA 2027 at NIT Warangal, Springer LNCS, deadline 15 February 2027. Deadlines must be re-checked on "
              "the official sites.")
table(s, [["Venue", "Type / indexing", "Deadline", "Why"],
          ["FNP 2027 @ EACL 2027", "ACL workshop (ACL Anthology)", "15 Dec 2026", "Financial NLP; accepts datasets and short papers"],
          ["SANKALP 2027 (IIITM Gwalior)", "IEEE conference", "30 Nov 2026", "Nearest deadline; broad AI scope"],
          ["BDA 2027 (NIT Warangal)", "Springer LNCS (Scopus)", "15 Feb 2027", "Backup with more time"],
          ["ICAIF 2027 / FinNLP 2027", "ACM / ACL, top venues", "~Aug 2027 (TBA)", "Stretch goal for extended version"]],
      0.6, 1.5, 12.1, [3.4, 3.0, 2.0, 3.7], size=15, height=0.7)
add_text(s, "Deadlines checked on 26 Oct 2026; confirm on official websites before submitting.", 0.6, 5.4, 12, 0.5, size=14, color=GREY)

# 14. Limitations
s = new_slide("Limitations we are aware of",
              "We are honest about limitations: pilot labels are drafts and need a human review; automatic labels "
              "come from our rules; claims from one company are related, so we report company-level results; and "
              "our builder uses whole-company figures only, so mergers can look like corrections, which is why we "
              "filter extreme changes and hand-check a sample.")
bullets(s, ["Pilot labels were drafted by one analyst, so they need independent human review",
            "Automatic labels are 'silver' (from rule P), so we will hand-check a sample of about 20 companies",
            "Claims about the same company are not independent: we report company-level accuracy",
            "SEC Company Facts gives whole-company figures only; mergers can mimic corrections (filtered and flagged)",
            "US companies and net income only, for now; segments and quarterly data are future work"], size=19)

# 15. Thanks
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()
add_text(s, "Thank you. Questions?", 0.8, 2.6, 11.7, 1.2, size=44, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text(s, "Code and data: github.com/Shreya732-debug/Research-Work", 0.8, 4.0, 11.7, 0.8, size=20,
         color=RGBColor(0xB8, 0xE0, 0xDA), align=PP_ALIGN.CENTER)

out = os.path.join(HERE, "Midterm_Presentation.pptx")
prs.save(out)
print(f"Saved {out} ({len(prs.slides)} slides)")
