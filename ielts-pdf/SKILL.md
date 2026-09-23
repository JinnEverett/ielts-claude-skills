---
name: ielts-pdf
description: |
  Converts an IELTS practice-test PDF (e.g. a Cambridge IELTS book) into markdown, split by skill (listening/reading/writing/speaking), before any other skill reads it. Saves tokens vs. reading a raw PDF and works for both scanned (OCR) and text-based PDFs.
  Triggers: /ielts-pdf, "setup đề", "setup this test", "import Cambridge <N>", "convert this pdf", any time a user points at a .pdf exam book
metadata:
  version: Pro
---

# IELTS PDF — Practice-Test Ingestion

You convert an IELTS practice-test PDF into markdown **before** any grading/analysis work happens, so downstream skills (`ielts-reading`, `ielts-listening`, `ielts-writing`, `ielts-speaking`) read compact text instead of a raw PDF.

**Always run this first when the user hands you a PDF exam book (Cambridge IELTS or similar), even if they didn't explicitly ask for conversion.** Only skip it if a markdown output already exists and is newer than the PDF (the script checks this itself).

---

## Materials Folder Convention

All practice-test source material lives under `D:\Ielts\materials\<Book Name>\` — this is the single place every skill looks. Layout:

```text
materials/
└── Cambridge 18/
    ├── Cambridge 18 - The IELTS Workshop/
    │   ├── Cambridge 18.pdf         # original book (never committed)
    │   └── AUDIO FILES/Test {1-4}/  # real listening audio, if the book included any
    └── md/                          # output of this skill
        ├── listening.md
        ├── reading.md
        ├── writing.md
        └── speaking.md
```

When the user gives you a new PDF that isn't under `materials/` yet, move it there first (`materials/<Book Name>/...`, keeping any bundled audio folder alongside it) before converting — don't leave source books scattered elsewhere in the repo.

## Tool

**Script:** `python3 ~/.claude/skills/shared/pdf_to_md.py`

```bash
python3 ~/.claude/skills/shared/pdf_to_md.py "<path to book.pdf>" --out-dir "materials/<Book Name>/md"
```

- Default output (no `--out-dir`): a `md/` folder next to the PDF itself. Books are usually nested one level deeper than that (`materials/<Book Name>/<Book Name> - .../book.pdf`), so **always pass `--out-dir` explicitly** to land output at the book level: `materials/<Book Name>/md/` — see the layout above.
- Up to 4 output files — `listening.md`, `reading.md`, `writing.md`, `speaking.md` — each grouped by `## Test N`.
- Auto-detects whether the PDF has a real text layer (fast path) or is a scanned image (falls back to OCR via Tesseract).
- Idempotent: if `--out-dir` already has output newer than the PDF, it skips reconversion. Pass `--force` to redo it (e.g. after fixing a bad OCR pass).

## Workflow

### Step 1: Locate the PDF

Check `D:\Ielts\materials\<Book Name>\` first — if the book is already there, use that PDF directly. If the user names a book (e.g. "Cambridge 18") but it's not under `materials/` yet, search common locations (Desktop, Downloads, Documents, the working directory) before asking:

```powershell
Get-ChildItem -Path "$env:USERPROFILE\Desktop","$env:USERPROFILE\Downloads","$env:USERPROFILE\Documents","D:\" -Recurse -Filter "<book name>*.pdf" -ErrorAction SilentlyContinue
```

If found outside `materials/`, move (don't copy) it into `materials/<Book Name>/`, bundled audio folder included, then convert. Only ask the user for a path if nothing turns up.

### Step 2: Check dependencies (first run only)

```bash
python3 -c "import fitz, PIL"
```

If missing:

```bash
python3 -m pip install pymupdf pillow pytesseract
```

OCR also needs the Tesseract binary itself (only required for scanned PDFs — text-based PDFs never touch this):

```bash
# Windows
winget install --id UB-Mannheim.TesseractOCR -e --accept-source-agreements --accept-package-agreements --silent
```

Confirm with the user before installing system-level software (Tesseract), per standard operating caution — everything else (pip packages) is safe to install silently.

### Step 3: Run the conversion

```bash
python3 ~/.claude/skills/shared/pdf_to_md.py "materials/<Book Name>/.../<book>.pdf" --out-dir "materials/<Book Name>/md"
```

Large scanned books (100+ pages) take real time (roughly 5-10 seconds/page under OCR) — run it and let it finish; don't poll aggressively.

### Step 4: Report and hand off

Tell the user what was written (which files, how many pages, whether OCR was used) and flag known OCR blind spots:

- Charts/graphs/diagrams (e.g. Writing Task 1 data) are images — OCR won't capture the numbers, only surrounding captions. Point to the source PDF page (each block has a `<!-- source page N -->` comment) for these.
- Fill-in-the-blank underscores/dots in Listening/Reading question sheets sometimes OCR as garbage characters — the question text itself is still reliable.
- Ambiguous answer-key pages (can't tell Listening vs Reading apart) are dropped rather than misfiled — cross-check the source PDF if a test's answer key seems to be missing from `listening.md`/`reading.md`.

Then proceed with whatever the user actually wants (grade an essay, analyze reading answers, etc.) by reading the relevant generated `.md` file instead of the PDF — that's the whole point.

### Step 5: Keep the repo clean

Practice-test PDFs and their markdown output are copyrighted material — never commit them. The project `.gitignore` already excludes the whole `materials/` folder; that's exactly why every book belongs under it (Step 1) rather than scattered elsewhere in the repo.

---

## Boundaries

- You only convert and route. You don't grade, analyze, or coach — hand off to the relevant sub-skill once the markdown exists.
- Don't re-run OCR on a book that's already converted (check `md/` mtimes) unless asked or the existing output looks broken.
