import argparse
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

from pypdf import PdfReader, PdfWriter

"""
Process main.toc to extract the start and the end page of each chapter.
Print the start, end page numbers for each chapter together with the chapter name.
Using i for a chapter index (i=0, ..., n-1), use main.pdf to extract pages for the chapter i.
Name the output files with chapter_names[i].pdf.
Check if the last page of the chapter is empty. If it is, remove it.

Arguments:
--toc-only: only print the start and end page numbers for each chapter
"""

chapter_names = [
    "01-mol-bio.pdf",
    "02-history.pdf",
    "03-genomes.pdf",
    "04-genes.pdf",
    "05-alignment-m.pdf",
    "06-alignment-t.pdf",
    "07-filogeny.pdf"
]


@dataclass
class ChapterRange:
    title: str
    start_page: int  # 1-based page number from TOC
    end_page: int    # 1-based inclusive


def parse_toc(toc_path: Path) -> List[Tuple[str, int]]:
    """Return list of (title, start_page) for each chapter from LaTeX .toc.

    Expects lines like:
      \contentsline {chapter}{\numberline {1}Introduction}{1}{chapter.1}

    We capture the visible title and the starting page number.
    """
    content = toc_path.read_text(encoding="utf-8", errors="ignore")
    # Regex: capture title (group 1) and page (group 2)
    pattern = re.compile(
        r"\\contentsline\s*\{chapter\}\{\s*(?:\\numberline\s*\{[^}]*\})?([^}]*)\}\{(\d+)\}",
        re.MULTILINE,
    )
    chapters: List[Tuple[str, int]] = []
    for match in pattern.finditer(content):
        raw_title = match.group(1).strip()
        # Basic cleanup: strip TeX commands like \textit{...} → content
        title = _strip_latex_commands(raw_title)
        start_page = int(match.group(2))
        chapters.append((title, start_page))
    return chapters


def _strip_latex_commands(s: str) -> str:
    # Remove simple LaTeX commands while keeping their contents: \cmd{X} -> X
    s = re.sub(r"\\[a-zA-Z]+\s*\{([^}]*)\}", r"\\1", s)
    # Remove remaining commands like \emph, \LaTeX
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    # Collapse spaces
    s = re.sub(r"\s+", " ", s).strip()
    return s


def compute_ranges(toc_entries: List[Tuple[str, int]], total_pages: int) -> List[ChapterRange]:
    ranges: List[ChapterRange] = []
    for idx, (title, start) in enumerate(toc_entries):
        if idx + 1 < len(toc_entries):
            end = toc_entries[idx + 1][1] - 1
        else:
            end = total_pages
        if end < start:
            # Guard against malformed TOC; clamp
            end = start
        ranges.append(ChapterRange(title=title, start_page=start, end_page=end))
    return ranges


def is_blank_page(reader: PdfReader, page_index_zero_based: int) -> bool:
    page = reader.pages[page_index_zero_based]
    # If content stream is missing
    try:
        contents = page.get_contents()
        if contents is None:
            return True
    except Exception:
        # Fallback to text extraction if content access fails
        pass
    try:
        text = page.extract_text() or ""
        if text.strip() == "":
            # Heuristic: treat as blank if no text; images won't be detected here
            return True
    except Exception:
        pass
    return False


def split_pdf(
    pdf_path: Path,
    ranges: List[ChapterRange],
    output_dir: Path,
    use_chapter_names: bool,
    only_index: int | None = None,
) -> None:
    reader = PdfReader(str(pdf_path))
    for i, info in enumerate(ranges):
        if only_index is not None and i != only_index:
            continue
        writer = PdfWriter()
        # Convert to 0-based indices for pypdf
        start0 = info.start_page - 1
        end0 = info.end_page - 1
        # Exclude last page if blank
        last_page_to_include = end0
        if is_blank_page(reader, end0):
            last_page_to_include = max(start0, end0 - 1)
        for p in range(start0, last_page_to_include + 1):
            writer.add_page(reader.pages[p])

        if use_chapter_names and i < len(chapter_names):
            filename = chapter_names[i]
        else:
            filename = _sanitize_filename(f"{i+1:02d}-{info.title}.pdf")
        out_path = output_dir / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("wb") as f:
            writer.write(f)


def _sanitize_filename(name: str) -> str:
    name = name.strip()
    # Replace path separators and illegal characters
    name = re.sub(r"[\\/]+", "-", name)
    name = re.sub(r"[^\w\-\. ]+", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def main() -> None:
    parser = argparse.ArgumentParser(description="Split main.pdf into chapter PDFs using main.toc")
    parser.add_argument("--toc", default="main.toc", help="Path to LaTeX .toc file (default: main.toc)")
    parser.add_argument("--pdf", default="main.pdf", help="Path to source PDF (default: main.pdf)")
    parser.add_argument("--output-dir", default=".", help="Directory to write chapter PDFs")
    parser.add_argument("--toc-only", action="store_true", help="Only print chapter ranges; do not write PDFs")
    parser.add_argument("--chapter-index", type=int, default=None, help="If set, only process chapter i (0-based)")
    parser.add_argument("--no-predefined-names", action="store_true", help="Do not use predefined chapter_names; derive from titles")

    args = parser.parse_args()

    toc_path = Path(args.toc)
    pdf_path = Path(args.pdf)
    output_dir = Path(args.output_dir)

    if not toc_path.exists():
        raise FileNotFoundError(f"TOC not found: {toc_path}")
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    toc_entries = parse_toc(toc_path)
    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    ranges = compute_ranges(toc_entries, total_pages)

    # Print ranges
    for idx, r in enumerate(ranges):
        print(f"{idx}: '{r.title}' -> start {r.start_page}, end {r.end_page}")

    if args.toc_only:
        return

    split_pdf(
        pdf_path=pdf_path,
        ranges=ranges,
        output_dir=output_dir,
        use_chapter_names=not args.no_predefined_names,
        only_index=args.chapter_index,
    )


if __name__ == "__main__":
    main()
