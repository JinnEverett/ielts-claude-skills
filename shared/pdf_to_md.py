#!/usr/bin/env python3
"""Convert an IELTS practice-test PDF (e.g. Cambridge IELTS N) into markdown,
split by skill (listening / reading / writing / speaking).

Auto-detects whether the PDF has an extractable text layer. If not (scanned
book), falls back to OCR via Tesseract. Classifies each page by skill using
heading heuristics that match the standard Cambridge IELTS practice-book
layout, and tracks the current "Test N" context per page.

Usage:
    python3 pdf_to_md.py <path-to.pdf> [--out-dir DIR] [--zoom 3.0]

Requires: pymupdf, pillow. For scanned PDFs, also: pytesseract + a Tesseract
OCR install (on Windows: `winget install --id UB-Mannheim.TesseractOCR -e`).
"""
import argparse
import os
import re
import sys

TESSERACT_CANDIDATES = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]

SKIP_HEADINGS = re.compile(
    r"^(Contents|Acknowledgements|Introduction|Sample answer sheet)", re.I
)
TEST_RE = re.compile(r"\bTest\s+(\d+)\b")
READING_RE = re.compile(r"READING PASSAGE|Reading Passage", re.I)
WRITING_RE = re.compile(r"WRITING TASK", re.I)
SPEAKING_RE = re.compile(r"\bSPEAKING\b")
LISTENING_PART_RE = re.compile(r"\bPART\s+[1-4]\b", re.I)
LISTENING_HEADING_RE = re.compile(r"^\s*Listening\s*$", re.I | re.M)
AUDIOSCRIPT_RE = re.compile(r"Audioscript", re.I)
SAMPLE_WRITING_RE = re.compile(r"Sample [Ww]riting answer", re.I)
ANSWER_KEY_RE = re.compile(r"answer keys?", re.I)
AK_LISTENING_RE = re.compile(r"^\s*LISTENING\s*$", re.M)
AK_READING_RE = re.compile(r"^\s*READING\s*$", re.M)


def get_tesseract_cmd():
    import shutil

    found = shutil.which("tesseract")
    if found:
        return found
    for path in TESSERACT_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def extract_page_text(doc, i, ocr_zoom):
    import fitz  # pymupdf

    page = doc[i]
    text = page.get_text().strip()
    if len(text) >= 20:
        return text, False

    # Scanned page: fall back to OCR.
    import pytesseract
    from PIL import Image
    import io

    cmd = get_tesseract_cmd()
    if not cmd:
        raise RuntimeError(
            "This PDF looks scanned (no text layer) but Tesseract OCR is not "
            "installed. Install it first, e.g. on Windows: "
            "winget install --id UB-Mannheim.TesseractOCR -e"
        )
    pytesseract.pytesseract.tesseract_cmd = cmd

    mat = fitz.Matrix(ocr_zoom, ocr_zoom)
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(img).strip(), True


def classify_page(text):
    """Returns one of: listening, reading, writing, speaking, skip, unknown."""
    if SKIP_HEADINGS.match(text.strip()):
        return "skip"
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    if ANSWER_KEY_RE.search(text) and ("LISTENING" in text or "READING" in text):
        if AK_LISTENING_RE.search(text) and not AK_READING_RE.search(text):
            return "listening"
        if AK_READING_RE.search(text) and not AK_LISTENING_RE.search(text):
            return "reading"
        # Ambiguous answer-key page: skip rather than misfile.
        return "skip"
    if AUDIOSCRIPT_RE.search(first_line):
        return "listening"
    if SAMPLE_WRITING_RE.search(first_line):
        return "writing"
    if READING_RE.search(text):
        return "reading"
    if WRITING_RE.search(text):
        return "writing"
    if SPEAKING_RE.search(text) or "examiner asks you about" in text.lower():
        return "speaking"
    if LISTENING_PART_RE.search(text) or LISTENING_HEADING_RE.search(text):
        return "listening"
    return "unknown"


def already_converted(pdf_path, out_dir):
    if not os.path.isdir(out_dir):
        return False
    md_files = [f for f in os.listdir(out_dir) if f.endswith(".md")]
    if not md_files:
        return False
    pdf_mtime = os.path.getmtime(pdf_path)
    return all(
        os.path.getmtime(os.path.join(out_dir, f)) >= pdf_mtime for f in md_files
    )


def build(pdf_path, out_dir, ocr_zoom, start=None, end=None, force=False):
    import fitz  # pymupdf

    if not force and start is None and end is None and already_converted(pdf_path, out_dir):
        print(f"Already converted (outputs in {out_dir} are newer than the PDF). Use --force to redo.")
        return

    doc = fitz.open(pdf_path)
    buckets = {"listening": [], "reading": [], "writing": [], "speaking": []}
    current_test = None
    used_ocr_pages = 0

    page_range = range(start or 0, end if end is not None else len(doc))
    last_skill = None
    for i in page_range:
        text, was_ocr = extract_page_text(doc, i, ocr_zoom)
        used_ocr_pages += 1 if was_ocr else 0

        m = TEST_RE.search(text)
        if m:
            n = int(m.group(1))
            # Guard against stray OCR digit errors (e.g. "1" misread as "7"):
            # a genuine test-number change only ever increments by 1.
            if current_test is None or n == current_test or n == current_test + 1:
                current_test = n

        skill = classify_page(text)
        if skill == "skip":
            last_skill = None
            continue
        if skill == "unknown":
            if last_skill is None:
                continue
            skill = last_skill  # continuation of the previous section
        else:
            last_skill = skill

        buckets[skill].append((i, current_test, text))
        print(f"page {i}: test={current_test} skill={skill} ocr={was_ocr}", file=sys.stderr)

    os.makedirs(out_dir, exist_ok=True)
    base_title = os.path.splitext(os.path.basename(pdf_path))[0]

    for skill, pages in buckets.items():
        if not pages:
            continue
        out_path = os.path.join(out_dir, f"{skill}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# {base_title} - {skill.capitalize()}\n\n")
            f.write(
                "> Auto-converted from PDF (native text extraction"
                + (" + OCR" if used_ocr_pages else "")
                + "). Verify important content against the source PDF, "
                "especially charts/diagrams and OCR-only pages.\n\n"
            )
            last_test = None
            for page_i, test_n, text in pages:
                if test_n != last_test:
                    f.write(f"\n## Test {test_n}\n\n" if test_n else "\n## \n\n")
                    last_test = test_n
                f.write(f"<!-- source page {page_i} -->\n\n")
                f.write(text.strip() + "\n\n")
        print(f"wrote {out_path} ({len(pages)} pages)")

    if used_ocr_pages:
        print(f"OCR was used on {used_ocr_pages} page(s).")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf_path")
    ap.add_argument("--out-dir", default=None, help="default: <pdf dir>/md")
    ap.add_argument("--zoom", type=float, default=3.0, help="OCR render zoom")
    ap.add_argument("--start", type=int, default=None, help="debug: first page index (0-based)")
    ap.add_argument("--end", type=int, default=None, help="debug: last page index (exclusive)")
    ap.add_argument("--force", action="store_true", help="reconvert even if up-to-date output exists")
    args = ap.parse_args()

    out_dir = args.out_dir or os.path.join(os.path.dirname(os.path.abspath(args.pdf_path)), "md")
    build(args.pdf_path, out_dir, args.zoom, args.start, args.end, args.force)


if __name__ == "__main__":
    main()
