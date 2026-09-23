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

## Tool

**Script:** `python3 ~/.claude/skills/shared/pdf_to_md.py`

```bash
python3 ~/.claude/skills/shared/pdf_to_md.py "<path to book.pdf>"
```

- Default output: a `md/` folder next to the PDF, with up to 4 files — `listening.md`, `reading.md`, `writing.md`, `speaking.md` — each grouped by `## Test N`.
- Auto-detects whether the PDF has a real text layer (fast path) or is a scanned image (falls back to OCR via Tesseract).
- Idempotent: if the `md/` output is already newer than the PDF, it skips reconversion. Pass `--force` to redo it (e.g. after fixing a bad OCR pass).
- `--out-dir DIR` to control output location if you don't want it next to the PDF.

## Workflow

### Step 1: Locate the PDF

If the user names a book (e.g. "Cambridge 18") but not a path, search for it before asking:

```bash
python3 -c "import glob,itertools" ; # or just search the working dir / common folders
```

In practice: check the current project directory and common download locations for a file matching the name. Only ask the user for the path if you can't find it.

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
python3 ~/.claude/skills/shared/pdf_to_md.py "<path to book.pdf>"
```

Large scanned books (100+ pages) take real time (roughly 5-10 seconds/page under OCR) — run it and let it finish; don't poll aggressively.

### Step 4: Report and hand off

Tell the user what was written (which files, how many pages, whether OCR was used) and flag known OCR blind spots:

- Charts/graphs/diagrams (e.g. Writing Task 1 data) are images — OCR won't capture the numbers, only surrounding captions. Point to the source PDF page (each block has a `<!-- source page N -->` comment) for these.
- Fill-in-the-blank underscores/dots in Listening/Reading question sheets sometimes OCR as garbage characters — the question text itself is still reliable.
- Ambiguous answer-key pages (can't tell Listening vs Reading apart) are dropped rather than misfiled — cross-check the source PDF if a test's answer key seems to be missing from `listening.md`/`reading.md`.

Then proceed with whatever the user actually wants (grade an essay, analyze reading answers, etc.) by reading the relevant generated `.md` file instead of the PDF — that's the whole point.

### Step 5: Keep the repo clean

Practice-test PDFs and their markdown output are copyrighted material — never commit them. The project `.gitignore` already excludes `*.pdf` and any `Cambridge*/` folder; if the book lives somewhere else, make sure its containing folder isn't tracked either.

---

## Boundaries

- You only convert and route. You don't grade, analyze, or coach — hand off to the relevant sub-skill once the markdown exists.
- Don't re-run OCR on a book that's already converted (check `md/` mtimes) unless asked or the existing output looks broken.
