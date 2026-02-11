"""
Paper Index Builder
====================
Extracts metadata (title, authors, year) from each PDF in the collection
and generates:
    paper_index.json  - Machine-readable index keyed by filename
    paper_index.md    - Human-readable markdown table with Harvard references

Usage:
    python build_paper_index.py             # Build from scratch
    python build_paper_index.py --update    # Only process new PDFs

Outputs include an extraction_confidence field (high/medium/low) so you
know which entries to review manually.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PDF_DIR = Path(__file__).parent
INDEX_JSON = PDF_DIR / "paper_index.json"
INDEX_MD = PDF_DIR / "paper_index.md"

ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})")
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")

# Titles that PDF metadata often defaults to (treat as junk)
JUNK_TITLES = {
    "", "untitled", "title", "microsoft word", "manuscript",
    "arxiv", "paper", "document", "pdf", "none",
}

# Conference/venue keywords for Harvard references
VENUE_KEYWORDS = {
    "neurips": "NeurIPS",
    "nips": "NeurIPS",
    "icml": "ICML",
    "iclr": "ICLR",
    "cvpr": "CVPR",
    "iccv": "ICCV",
    "eccv": "ECCV",
    "aaai": "AAAI",
    "ijcai": "IJCAI",
    "emnlp": "EMNLP",
    "acl": "ACL",
    "naacl": "NAACL",
    "corl": "CoRL",
    "icra": "ICRA",
    "iros": "IROS",
    "rss": "RSS",
    "openreview": "OpenReview",
}


# ---------------------------------------------------------------------------
# Title Extraction (cascade)
# ---------------------------------------------------------------------------
def _title_from_metadata(doc: fitz.Document) -> str | None:
    """Strategy 1: PDF metadata title field."""
    title = (doc.metadata.get("title") or "").strip()
    if not title:
        return None
    # Reject junk
    if title.lower() in JUNK_TITLES:
        return None
    # Reject if it looks like a filename
    if title.endswith(".pdf") or title.endswith(".docx"):
        return None
    # Reject very short or very long titles
    if len(title) < 8 or len(title) > 300:
        return None
    return title


def _title_from_font_size(doc: fitz.Document) -> str | None:
    """Strategy 2: Find the largest font on page 1 and collect those spans."""
    try:
        page = doc[0]
        blocks = page.get_text("dict")["blocks"]
    except Exception:
        return None

    # Collect all spans with their font sizes
    spans = []
    for block in blocks:
        if block.get("type") != 0:  # text blocks only
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                size = span.get("size", 0)
                if text and size > 0:
                    spans.append((size, text, span.get("origin", (0, 0))))

    if not spans:
        return None

    max_size = max(s[0] for s in spans)
    # Only use this if the largest font is meaningfully bigger than body text
    sizes = sorted(set(s[0] for s in spans))
    if len(sizes) < 2 or max_size < 14:
        return None

    # Collect text at the largest font size, in order of appearance
    # Stop if we hit something that looks like an author line or abstract
    title_parts = []
    for size, text, origin in spans:
        if abs(size - max_size) < 0.5:
            # Skip arxiv headers, dates, copyright
            lower = text.lower()
            if any(skip in lower for skip in [
                "arxiv:", "preprint", "published", "copyright",
                "proceedings", "conference", "workshop",
                "under review", "submitted",
            ]):
                continue
            title_parts.append(text)

    if not title_parts:
        return None

    title = " ".join(title_parts).strip()
    # Clean up multiple spaces
    title = re.sub(r"\s+", " ", title)

    if len(title) < 8 or len(title) > 300:
        return None

    return title


def _title_from_text_heuristic(text: str) -> str | None:
    """Strategy 3: Longest line before 'Abstract', skipping junk headers."""
    header = text[:3000]
    lines = [line.strip() for line in header.split("\n") if line.strip()]

    # Skip known junk patterns at the start
    skip_patterns = [
        r"^arxiv:\d",
        r"^\d{4}\.\d{4,5}",
        r"^preprint",
        r"^published",
        r"^proceedings",
        r"^\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
        r"^(january|february|march|april|may|june|july|august|september|october|november|december)",
        r"^copyright",
        r"^under review",
        r"^\d+$",  # just a number
        r"^https?://",
    ]

    title_candidates = []
    for line in lines[:20]:
        lower = line.lower()
        # Stop at abstract
        if re.match(r"^abstract\b", lower):
            break
        # Skip junk
        if any(re.match(pat, lower) for pat in skip_patterns):
            continue
        # Skip very short lines (page numbers, single words)
        if len(line) < 10:
            continue
        # Skip lines that look like author lists (contain @, many commas)
        if "@" in line or line.count(",") > 3:
            continue
        title_candidates.append(line)

    if not title_candidates:
        return None

    # Pick the longest candidate
    best = max(title_candidates, key=len)
    if len(best) < 10:
        return None

    return best[:200]


def _title_from_filename(filename: str) -> str:
    """Strategy 4: Clean up the filename as a fallback."""
    name = Path(filename).stem
    # Strip version suffixes
    name = re.sub(r"v\d+$", "", name).strip()
    # Strip trailing (1), (2) etc.
    name = re.sub(r"\s*\(\d+\)$", "", name).strip()
    # Replace underscores with spaces
    name = name.replace("_", " ")
    return name


def extract_title(doc: fitz.Document, text: str, filename: str) -> tuple[str, str]:
    """
    Extract title using cascade of strategies.
    Returns (title, confidence) where confidence is 'high', 'medium', or 'low'.
    """
    # Strategy 1: PDF metadata
    title = _title_from_metadata(doc)
    if title:
        return title, "high"

    # Strategy 2: Font-size heuristic
    title = _title_from_font_size(doc)
    if title:
        return title, "high"

    # Strategy 3: Text heuristic
    title = _title_from_text_heuristic(text)
    if title:
        return title, "medium"

    # Strategy 4: Filename fallback
    return _title_from_filename(filename), "low"


# ---------------------------------------------------------------------------
# Author Extraction (cascade)
# ---------------------------------------------------------------------------
def _parse_author_string(raw: str) -> list[str]:
    """Parse an author string into individual names."""
    if not raw or raw.strip().lower() in ("unknown", ""):
        return []
    # Split on semicolons, ' and ', '&', or ' , ' patterns
    raw = raw.replace(" and ", ";").replace("&", ";").replace(" AND ", ";")
    parts = re.split(r"[;]", raw)
    authors = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Handle comma-separated lists (but not "Last, First" format)
        # If there are many commas, it's probably a list
        if part.count(",") > 2:
            sub_parts = part.split(",")
            for sp in sub_parts:
                sp = sp.strip()
                if sp and len(sp) > 1:
                    authors.append(sp)
        else:
            if part and len(part) > 1:
                authors.append(part)
    return authors


def _authors_from_metadata(doc: fitz.Document) -> list[str] | None:
    """Strategy 1: PDF metadata author field."""
    raw = (doc.metadata.get("author") or "").strip()
    if not raw:
        return None
    authors = _parse_author_string(raw)
    if authors:
        return authors
    return None


def _authors_from_text(text: str, title: str) -> list[str] | None:
    """Strategy 2: Lines between title and abstract at intermediate position."""
    header = text[:3000]
    lines = [line.strip() for line in header.split("\n") if line.strip()]

    # Find the title position (approximate match)
    title_lower = title.lower()[:50]
    title_idx = None
    for i, line in enumerate(lines):
        if title_lower in line.lower():
            title_idx = i
            break

    if title_idx is None:
        title_idx = 0

    # Find abstract position
    abstract_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^abstract\b", line.lower()):
            abstract_idx = i
            break

    if abstract_idx is None:
        abstract_idx = min(title_idx + 10, len(lines))

    # Look between title and abstract for author-like lines
    candidate_lines = lines[title_idx + 1 : abstract_idx]

    # Author lines typically: contain names (capitalized words), may have
    # superscript numbers, affiliations mixed in
    # Simple heuristic: lines with 2+ capitalized words, no common section headers
    author_parts = []
    for line in candidate_lines[:5]:
        lower = line.lower()
        # Skip affiliation / institution lines
        if any(kw in lower for kw in [
            "university", "institute", "department", "lab",
            "research", "google", "meta", "nvidia", "microsoft",
            "openai", "deepmind", "berkeley", "stanford", "mit",
            "@", "email", "correspond",
        ]):
            continue
        # Skip lines that are mostly numbers or very short
        if len(line) < 5:
            continue
        # Check if it has capitalized words that look like names
        words = line.split()
        cap_words = [w for w in words if w[0].isupper() and w.isalpha()]
        if len(cap_words) >= 2:
            # Clean up: remove superscript numbers, asterisks
            cleaned = re.sub(r"[0-9∗†‡§¶∥★,]+", " ", line)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            if cleaned:
                author_parts.append(cleaned)

    if not author_parts:
        return None

    # Join and parse
    raw = ", ".join(author_parts)
    authors = _parse_author_string(raw)
    return authors if authors else None


def extract_authors(doc: fitz.Document, text: str, title: str) -> list[str]:
    """Extract authors with cascade. Returns list of author names."""
    authors = _authors_from_metadata(doc)
    if authors:
        return authors

    authors = _authors_from_text(text, title)
    if authors:
        return authors

    return ["Unknown"]


# ---------------------------------------------------------------------------
# Year Extraction (cascade)
# ---------------------------------------------------------------------------
def _year_from_arxiv_in_filename(filename: str) -> int | None:
    """Strategy 1: Arxiv ID in filename (YYMM → year)."""
    m = ARXIV_ID_RE.search(filename)
    if m:
        yymm = m.group(1)[:4]
        yy = int(yymm[:2])
        year = 2000 + yy if yy < 50 else 1900 + yy
        return year
    return None


def _year_from_filename_explicit(filename: str) -> int | None:
    """Strategy 2: Explicit year in filename like _2024 or _2023."""
    m = re.search(r"[_\s(]?((?:19|20)\d{2})[_\s).]", filename)
    if m:
        return int(m.group(1))
    return None


def _year_from_arxiv_in_text(text: str) -> int | None:
    """Strategy 3: Arxiv ID in the PDF text."""
    header = text[:3000]
    m = ARXIV_ID_RE.search(header)
    if m:
        yy = int(m.group(1)[:2])
        return 2000 + yy if yy < 50 else 1900 + yy
    return None


def _year_from_text_context(text: str) -> int | None:
    """Strategy 4: Year near 'Published'/'Proceedings' in text."""
    header = text[:5000].lower()
    for keyword in ["published", "proceedings", "conference", "journal", "accepted"]:
        idx = header.find(keyword)
        if idx >= 0:
            snippet = header[idx : idx + 100]
            m = YEAR_RE.search(snippet)
            if m:
                year = int(m.group(0))
                if 1990 <= year <= 2030:
                    return year
    return None


def extract_year(text: str, filename: str) -> int | None:
    """Extract publication year with cascade."""
    year = _year_from_arxiv_in_filename(filename)
    if year:
        return year

    year = _year_from_filename_explicit(filename)
    if year:
        return year

    year = _year_from_arxiv_in_text(text)
    if year:
        return year

    year = _year_from_text_context(text)
    if year:
        return year

    return None


# ---------------------------------------------------------------------------
# Short Title for Graph Labels
# ---------------------------------------------------------------------------
def make_short_title(title: str, max_len: int = 40) -> str:
    """Create a short title suitable for graph node labels (~40 chars)."""
    if not title:
        return "Unknown"

    # If title has a colon, take the part before it
    if ":" in title:
        before_colon = title.split(":")[0].strip()
        if len(before_colon) >= 8:
            title = before_colon

    # If still too long, truncate at word boundary
    if len(title) <= max_len:
        return title

    truncated = title[:max_len]
    # Try to break at a word boundary
    last_space = truncated.rfind(" ")
    if last_space > max_len // 2:
        truncated = truncated[:last_space]

    return truncated.rstrip() + "..."


# ---------------------------------------------------------------------------
# Harvard Reference
# ---------------------------------------------------------------------------
def _detect_venue(filename: str, text: str) -> str | None:
    """Detect conference/journal venue from filename or text."""
    combined = (filename + " " + text[:3000]).lower()
    for keyword, venue in VENUE_KEYWORDS.items():
        if keyword in combined:
            return venue
    return None


def _format_author_harvard(authors: list[str]) -> str:
    """Format authors for Harvard reference style."""
    if not authors or authors == ["Unknown"]:
        return "Unknown"

    def _surname(name: str) -> str:
        """Extract surname (last word) from a name."""
        parts = name.strip().split()
        if not parts:
            return name
        # If comma format "Surname, First", take first part
        if "," in name:
            return parts[0].rstrip(",")
        return parts[-1]

    def _initials(name: str) -> str:
        """Extract initials from first/middle names."""
        parts = name.strip().split()
        if not parts:
            return ""
        if "," in name:
            # "Surname, First Middle" format
            after_comma = name.split(",", 1)[1].strip().split()
            return "".join(p[0].upper() + "." for p in after_comma if p)
        # "First Middle Surname" format
        return "".join(p[0].upper() + "." for p in parts[:-1] if p)

    first = authors[0]
    surname = _surname(first)
    initials = _initials(first)

    if len(authors) == 1:
        return f"{surname}, {initials}" if initials else surname
    elif len(authors) == 2:
        s2 = _surname(authors[1])
        i2 = _initials(authors[1])
        a1 = f"{surname}, {initials}" if initials else surname
        a2 = f"{s2}, {i2}" if i2 else s2
        return f"{a1} and {a2}"
    else:
        return f"{surname}, {initials} et al." if initials else f"{surname} et al."


def build_harvard_reference(
    title: str, authors: list[str], year: int | None,
    filename: str, text: str
) -> str:
    """Build a Harvard-style reference string."""
    author_str = _format_author_harvard(authors)
    year_str = str(year) if year else "n.d."

    # Detect source
    arxiv_id = ARXIV_ID_RE.search(filename)
    venue = _detect_venue(filename, text)

    if arxiv_id:
        source = f"arXiv preprint arXiv:{arxiv_id.group(1)}"
        url = f"https://arxiv.org/abs/{arxiv_id.group(1)}"
        return f"{author_str} ({year_str}) '{title}'. {source}. Available at: {url}."
    elif venue:
        return f"{author_str} ({year_str}) '{title}'. In: {venue}."
    else:
        return f"{author_str} ({year_str}) '{title}'."


# ---------------------------------------------------------------------------
# Main Processing
# ---------------------------------------------------------------------------
def process_pdf(pdf_path: Path) -> dict:
    """Extract all metadata from a single PDF."""
    filename = pdf_path.name

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as e:
        print(f"  [WARN] Could not open {filename}: {e}")
        return {
            "title": _title_from_filename(filename),
            "title_short": make_short_title(_title_from_filename(filename)),
            "authors": ["Unknown"],
            "year": None,
            "arxiv_id": ARXIV_ID_RE.search(filename).group(1) if ARXIV_ID_RE.search(filename) else None,
            "harvard_reference": f"Unknown (n.d.) '{_title_from_filename(filename)}'.",
            "extraction_confidence": "low",
        }

    # Extract text from first few pages (enough for metadata)
    try:
        pages = doc[:min(3, len(doc))]
        text = "\n".join(page.get_text() for page in pages)
    except Exception:
        text = ""

    title, confidence = extract_title(doc, text, filename)
    authors = extract_authors(doc, text, title)
    year = extract_year(text, filename)
    arxiv_m = ARXIV_ID_RE.search(filename)
    arxiv_id = arxiv_m.group(1) if arxiv_m else None

    # If no arxiv in filename, check text
    if not arxiv_id:
        text_arxiv = ARXIV_ID_RE.search(text[:3000])
        if text_arxiv:
            arxiv_id = text_arxiv.group(1)

    short = make_short_title(title)
    harvard = build_harvard_reference(title, authors, year, filename, text)

    # Adjust confidence based on what we found
    if authors == ["Unknown"] and confidence == "high":
        confidence = "medium"
    if year is None and confidence != "low":
        confidence = "medium" if confidence == "high" else confidence

    doc.close()

    return {
        "title": title,
        "title_short": short,
        "authors": authors,
        "year": year,
        "arxiv_id": arxiv_id,
        "harvard_reference": harvard,
        "extraction_confidence": confidence,
    }


def build_index(update_only: bool = False):
    """Build or update the paper index."""
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print("No PDFs found in", PDF_DIR)
        sys.exit(1)

    # Load existing index if updating
    existing = {}
    if update_only and INDEX_JSON.exists():
        try:
            existing = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
            print(f"Loaded existing index with {len(existing)} entries.")
        except Exception as e:
            print(f"  [WARN] Could not load existing index: {e}")

    print(f"Found {len(pdf_files)} PDFs in {PDF_DIR}\n")

    index = {}
    new_count = 0
    skip_count = 0

    for pdf in pdf_files:
        if update_only and pdf.name in existing:
            index[pdf.name] = existing[pdf.name]
            skip_count += 1
            continue

        print(f"  Processing {pdf.name}...")
        entry = process_pdf(pdf)
        index[pdf.name] = entry
        new_count += 1

    if update_only:
        print(f"\nProcessed {new_count} new PDFs, kept {skip_count} existing entries.")
    else:
        print(f"\nProcessed {new_count} PDFs.")

    # Write JSON
    INDEX_JSON.write_text(
        json.dumps(index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {INDEX_JSON}")

    # Write Markdown
    _write_markdown(index)
    print(f"Wrote {INDEX_MD}")

    # Summary
    counts = {"high": 0, "medium": 0, "low": 0}
    for entry in index.values():
        c = entry.get("extraction_confidence", "low")
        counts[c] = counts.get(c, 0) + 1

    print(f"\nConfidence breakdown:")
    print(f"  High:   {counts['high']}")
    print(f"  Medium: {counts['medium']}")
    print(f"  Low:    {counts['low']}")

    if counts["low"] > 0:
        print(f"\n  {counts['low']} entries marked 'low' confidence - review these in paper_index.md")


def _write_markdown(index: dict):
    """Write the markdown index file."""
    lines = [
        "# Paper Index",
        "",
        f"**{len(index)} papers** indexed.",
        "",
        "## Full Index",
        "",
        "| # | Short Title | Authors | Year | Confidence | Harvard Reference |",
        "|---|-------------|---------|------|------------|-------------------|",
    ]

    needs_review = []

    for i, (filename, entry) in enumerate(sorted(index.items()), 1):
        short = entry.get("title_short", "?")
        authors = ", ".join(entry.get("authors", ["Unknown"])[:2])
        if len(entry.get("authors", [])) > 2:
            authors += " et al."
        year = entry.get("year") or "?"
        confidence = entry.get("extraction_confidence", "low")
        harvard = entry.get("harvard_reference", "")

        # Escape pipes in the Harvard reference
        harvard_escaped = harvard.replace("|", "\\|")

        lines.append(
            f"| {i} | {short} | {authors} | {year} | {confidence} | {harvard_escaped} |"
        )

        if confidence == "low":
            needs_review.append((filename, entry))

    if needs_review:
        lines.extend([
            "",
            "## Needs Review",
            "",
            "These entries have low extraction confidence and may need manual correction:",
            "",
        ])
        for filename, entry in needs_review:
            lines.append(f"- **{filename}**: `{entry.get('title', '?')}`")

    lines.append("")
    INDEX_MD.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build paper index from PDFs")
    parser.add_argument(
        "--update", action="store_true",
        help="Only process new PDFs, keep existing entries",
    )
    args = parser.parse_args()
    build_index(update_only=args.update)
