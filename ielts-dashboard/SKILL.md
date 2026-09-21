---
name: ielts-dashboard
description: |
  IELTS learning data visualization dashboard. Generates a local HTML page showing writing score trends, a four-skill radar chart, an error heatmap, synonym stats, and the exam countdown.
  Triggers: /ielts-dashboard, "dashboard", "show my data", "open the data panel"
metadata:
  version: Pro
---

# IELTS Dashboard — Learning Data Visualization

You're responsible for generating and opening the local IELTS learning data dashboard.

**Your job is simple: call the CLI to generate the dashboard HTML, then open it.**

---

## Execution Flow

### Step 1: Make sure data is initialized

```bash
python3 ~/.claude/skills/shared/ielts_cli.py init
```

### Step 2: Generate the dashboard

```bash
python3 ~/.claude/skills/shared/ielts_cli.py dashboard
```

### Step 3: Open it in the browser

```bash
open ~/.ielts/dashboard.html
```

### Step 4: Tell the user

```markdown
✅ Dashboard generated and opened!

📊 In your browser you can see:

- Writing score trend chart (last 10 essays)

- Four-skill radar chart (current vs. target)

- Top 10 frequent errors

- Synonym bank stats

- Vocabulary review overview

- Days until exam + daily recommendations

Path: `~/.ielts/dashboard.html`
To refresh: just reload the page in your browser to see the latest data.

💾 Tip: run `python3 ~/.claude/skills/shared/ielts_cli.py backup` to back up all your data.
```

---

## Troubleshooting

### If the browser doesn't open automatically

Tell the user to open it manually:

```bash
open ~/.ielts/dashboard.html
```

### If there's no data yet

Remind the user:

```text
There's no data in the dashboard yet. Go do a practice session first:

- Grade an essay → /ielts-writing

- Analyze a reading passage → /ielts-reading

- Analyze a listening test → /ielts-listening

Once you have data, come back to `/ielts-dashboard`.
```

---

## Boundaries

- You only generate the dashboard — you don't analyze the data (that's `/ielts-diagnosis`'s job)

- Data is sourced from the JSON files under `~/.ielts/`

- The dashboard is pure static HTML — no server needed
