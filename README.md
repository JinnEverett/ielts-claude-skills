# IELTS Claude Skills · vPro

> A set of IELTS prep AI coach skills that run on Claude Code.
> **Persistent data, cross-session memory, a visual dashboard, 8 skills working together.**

---

## What is this

8 [Claude Code Skills](https://docs.claude.com/en/docs/claude-code/skills) that form a complete IELTS prep assistant:

| Skill | What it does | Trigger words |
|-------|------|--------|
| `/ielts` | Entry point + baseline assessment + progress tracking | "I want to prepare for IELTS", "IELTS" |
| `/ielts-writing` | Four-criteria essay grading + rewrite comparison + task analysis + history tracking | "grade my essay", "check this essay for me" |
| `/ielts-reading` | Synonym extraction + True/False/Not Given breakdown + mistake diagnosis + synonym bank | "analyze this reading", "why is this wrong" |
| `/ielts-speaking` | 5 universal stories covering 80% of Part 2 topics + practice tracking | "speaking material", "Part 2 prep" |
| `/ielts-listening` | Listening mistake analysis + intensive listening training + question-type tracking | "listening", "mistakes", "intensive listening" |
| `/ielts-vocab` | Spaced-repetition review + synonym drills + topic vocab packs | "vocab review", "vocabulary", "review" |
| `/ielts-diagnosis` | Data diagnosis + personalized study plan | "diagnosis", "study plan" |
| `/ielts-dashboard` | Visual dashboard (trend charts / radar charts / mistake heatmap) | "dashboard", "show my data" |

**vPro's new features:**

- Data persisted to `~/.ielts/` — cross-session memory

- **Coach memory system:** automatically records your learning preferences, weakness patterns, and strategy feedback, picking up seamlessly next time

- Every essay auto-archived with a scoring history

- Mistake log auto-aggregates high-frequency error tags

- Synonym bank accumulates across essays and is searchable

- Spaced-repetition vocab training (SM-2 algorithm)

- Local HTML dashboard: trend charts / radar charts / mistake distribution

- Data-driven diagnosis + personalized training plan

- One-click backup / restore

---

## Who this is for

- IELTS candidates who want an AI training partner

- Developers already using Claude Code

- Candidates who want progress tracking, a mistake log, and a visual dashboard

---

## Installation

### Prerequisite

You need [Claude Code](https://docs.claude.com/en/docs/claude-code) installed first.

### Steps

```bash
# 1. Enter the project directory

cd ielts-claude-skills

# 2. Copy all skills into the Claude Code skills directory

cp -r ielts ielts-writing ielts-reading ielts-speaking \
      ielts-listening ielts-vocab ielts-diagnosis ielts-dashboard \
      shared dashboard \
      ~/.claude/skills/

# 3. Initialize the data directory

python3 ~/.claude/skills/shared/ielts_cli.py init

# 4. Restart Claude Code
```

Restart Claude Code after installing, then type `/ielts` to use it.

---

## How to use it

### Scenario 1: You don't know where to start and want guidance

```text
You: /ielts
AI: (asks you 3 questions: target score, exam date, what you want to practice today)
   → routes to the right sub-skill
   → automatically saves your profile
```

### Scenario 2: Grade an essay directly

```text
You: /ielts-writing
   [paste the prompt + your essay]
AI:

- Four-criteria scoring (TR / CC / LR / GRA)

- Sentence-level annotation of every issue

- Rewrite at your target band score

- Prioritized list of what to fix first

- Auto-saves to ~/.ielts/writing/
```

### Scenario 3: Analyze reading mistakes

```text
You: /ielts-reading
   [paste the passage + questions + your answers + correct answers]
AI:

- Breaks down the cause of each wrong answer

- Extracts a synonym table → auto-added to your bank

- True/False/Not Given logic analysis
```

### Scenario 4: Analyze listening mistakes

```text
You: /ielts-listening
   [paste the questions + your answers + correct answers]
AI:

- Section-by-section score analysis

- Error classification (spelling / numbers / missed it / distractor)

- Generates intensive-listening tasks
```

### Scenario 5: Vocab review

```text
You: /ielts-vocab
AI:

- Pushes today's due vocab (spaced repetition)

- Synonym drills

- Vocab packs by topic
```

### Scenario 6: View your learning data

```text
You: /ielts-dashboard
AI:

- Generates a local HTML dashboard

- Opens it in your browser automatically

- Writing trend chart / four-skill radar chart / mistake distribution
```

### Scenario 7: Diagnosis + study plan

```text
You: /ielts-diagnosis
AI:

- Reads all historical data

- Generates a diagnosis report

- Builds a daily/weekly training plan
```

---

## File structure

```text
ielts-claude-skills/
├── ielts/SKILL.md              # routing coach

├── ielts-writing/SKILL.md      # essay grading

├── ielts-reading/SKILL.md      # reading analysis

├── ielts-speaking/SKILL.md     # speaking material

├── ielts-listening/SKILL.md    # listening analysis

├── ielts-vocab/SKILL.md        # vocab training

├── ielts-diagnosis/SKILL.md    # diagnosis + study plan

├── ielts-dashboard/SKILL.md    # dashboard generation

├── shared/
│   └── ielts_cli.py            # data layer CLI (Python stdlib)

├── dashboard/
│   └── template.html           # dashboard HTML template

├── README.md
└── LICENSE                     # MIT
```

---

## Data storage

All data is stored under `~/.ielts/`:

```text
~/.ielts/
├── config.json          # user config

├── writing/             # essay history

├── reading/             # reading records

├── listening/           # listening records

├── speaking/            # speaking records

├── errors.json          # mistake log

├── synonyms.json        # synonym bank

├── progress.json        # score trends

├── vocab.json           # vocab + spaced-repetition data

├── memories.json        # coach memory (preferences/weaknesses/strategies)

└── dashboard.html       # generated dashboard
```

**Fully local, no cloud.** Back up with `python3 ~/.claude/skills/shared/ielts_cli.py backup`.

---

## License

[MIT](./LICENSE)

---

## Feedback

Fork from [ielts-claude-skills](https://github.com/YANZHANLIN/ielts-claude-skills). Issues and PRs welcome on your own fork.
