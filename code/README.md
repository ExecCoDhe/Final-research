# Code: verifying financial claims across original and corrected filings

You don't need to know Python to use this. Each step is a `.bat` file you double-click in Windows Explorer. A black window opens, runs the step and waits for you to press a key.

**One-time setup:** Python 3.11 is already installed on this laptop. If you use another computer, install Python from [python.org](https://www.python.org/downloads/) and tick **"Add Python to PATH"** during installation. Then open a terminal in this folder and run `pip install -r requirements.txt` once.

## The three steps

| Double-click | What it does | Needs internet? | Time |
|---|---|---|---|
| `1_RUN_PILOT_DEMO.bat` | Runs the five rule-based checkers on the 30 hand-checked pilot claims and confirms the program reproduces all 150 hand-made decisions. **Use this in the midterm demo.** | No | 5 seconds |
| `2_BUILD_DATASET.bat` | Downloads free SEC data and automatically builds new test claims from real restatements (40 companies, about 280 claims), then runs the checkers on them. | Yes | 5–15 minutes the first time, about 2 minutes later (downloads are cached) |
| `3_RUN_AI_TEST.bat` | Asks a free AI model (Gemini or Groq) to judge every claim, then scores it. Needs a free key (below). | Yes | About 3 minutes for the pilot; about 30 minutes for 280 claims |

All results land in `results/`. Open `results/SUMMARY.md` for one table comparing every method. You can open it in Notepad, but it looks nicer in Cursor or on GitHub.

## Get a free AI key (5 minutes)

You only need one of these:

- **Gemini (Google):** go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey), sign in with a Google account and click **Create API key**. Copy the key.
- **Groq (runs Llama models):** go to [console.groq.com/keys](https://console.groq.com/keys), sign up and click **Create API Key**. Copy the key.

Open `settings.txt` in Notepad and paste the key after `GEMINI_API_KEY=` or `GROQ_API_KEY=`. Save it. `settings.txt` is excluded from git, so your key is never uploaded to GitHub. Never paste a key into a chat, a slide or the paper.

If the provider says the model name is invalid, run this in a terminal in the `code` folder to see the models your key can use:

```
python run_llm.py --provider gemini --list-models
```

Then change `GEMINI_MODEL=` (or `GROQ_MODEL=`) in `settings.txt` to one of the names it prints.

To see exactly what the AI is asked, without using a key:

```
python run_llm.py --dry-run
```

## What each file is

| File | Purpose |
|---|---|
| `verifier.py` | The core logic: eligibility by date, the five authority policies, rounding intervals, and the five checkers B1, B3, B4, B4W and P |
| `run_rules.py` | Runs the checkers on a dataset and writes accuracy reports |
| `build_dataset.py` | Finds SEC non-reliance notices (8-K Item 4.02), finds the changed net-income figure in SEC Company Facts and generates claims |
| `run_llm.py` | Sends each claim to an AI model under two conditions: `full`, where the policy and cutoff are given, and `bare`, where only the claim and documents are given |
| `scoring.py`, `summarize.py` | Accuracy, accuracy per policy, company-level accuracy, confusion matrices and the combined summary |
| `data/pilot/` | The 30 pilot claims, the 11 filings and the 16 figures in machine-readable form, taken from `../pilot/` |
| `data/auto/` | The automatically built dataset. `families.csv` lists each company with SEC links and blank `check_*` columns for your manual spot-check. |
| `settings.txt` | Your email (the SEC requires it) and AI keys. Private. |

## Important honesty notes for the paper

- **Pilot labels are drafts.** The 30 pilot labels were written by an AI analyst and are still awaiting human review.
- **Automatic labels are "silver".** Rule P computes them, so P scores 100% on that data by construction. The automatic dataset is for testing AI models, not for proving that rule P is good. Before publication you must spot-check a sample against the real filings. Fill in the `check_*` columns in `families.csv`; about 20 families takes 2–3 hours.
- **Limits of SEC Company Facts.** The automatic builder uses entity-wide figures only. A large change (flagged in `families.csv`) might be a merger or reclassification rather than an error correction. Look at those first.
- **Claims from one company are related.** 279 claims from 40 companies are not 279 independent observations. Report company-level accuracy too, which `summarize.py` already does.
