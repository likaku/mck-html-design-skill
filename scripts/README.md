# mck-html-design Input Ingest Scripts

Ported from [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) — adapted for mck-html-design v3.
Port date: 2026-05-10

These scripts convert various source documents into Markdown for downstream HTML generation by the mck-html-design skill.

> **Python version note:** These scripts use Python 3.10+ type hint syntax (`X | Y` unions).
> Use `python3.11` (available at `/Users/kaku/.local/bin/python3.11`) to run them.
> The system `python3` (3.9.6) will fail with a SyntaxError.

---

## Scripts

### `pdf_to_md.py` — PDF → Markdown

Extracts text, images, and tables from PDF files using PyMuPDF.
Features: font-size-based heading detection, bold/italic, list detection, table extraction, image filtering, header/footer removal.

**Usage:**
```bash
python3.11 scripts/pdf_to_md.py input.pdf
python3.11 scripts/pdf_to_md.py input.pdf -o output.md
python3.11 scripts/pdf_to_md.py ./pdfs_dir/
python3.11 scripts/pdf_to_md.py ./pdfs_dir/ -o ./markdown_out/
python3.11 scripts/pdf_to_md.py input.pdf --images none   # skip images
python3.11 scripts/pdf_to_md.py input.pdf --images all    # extract all images
```

**Dependencies (under python3.11):**
| Package | Status (python3.11) | Install |
|---------|---------------------|---------|
| `PyMuPDF` (fitz) | ❌ missing | `python3.11 -m pip install PyMuPDF` |

---

### `doc_to_md.py` — DOCX/ODT/RTF → Markdown

Converts Word documents and other formats. Uses python-docx as primary backend with Pandoc as fallback for complex formats.

**Usage:**
```bash
python3.11 scripts/doc_to_md.py input.docx
python3.11 scripts/doc_to_md.py input.docx -o output.md
python3.11 scripts/doc_to_md.py ./docs_dir/
python3.11 scripts/doc_to_md.py input.docx --backend pandoc  # force Pandoc
```

**Dependencies (under python3.11):**
| Package | Status (python3.11) | Install |
|---------|---------------------|---------|
| `python-docx` (docx) | ❌ missing | `python3.11 -m pip install python-docx` |
| `pandoc` (CLI, fallback) | ✅ installed | `brew install pandoc` |

---

### `excel_to_md.py` — XLSX/XLS → Markdown

Converts Excel workbooks to Markdown tables. Supports merged cells, date formatting, booleans, and multi-sheet workbooks.

**Usage:**
```bash
python3.11 scripts/excel_to_md.py input.xlsx
python3.11 scripts/excel_to_md.py input.xlsx -o output.md
python3.11 scripts/excel_to_md.py input.xlsx --max-rows 100 --max-cols 20
```

**Dependencies (under python3.11):**
| Package | Status (python3.11) | Install |
|---------|---------------------|---------|
| `openpyxl` | ❌ missing | `python3.11 -m pip install openpyxl` |

---

### `web_to_md.py` — URL → Markdown

Fetches a web page and converts HTML content to Markdown. Supports image downloading, metadata extraction, and TLS fingerprint bypass for blocked sites (e.g. WeChat articles).

**Usage:**
```bash
python3.11 scripts/web_to_md.py https://example.com/article
python3.11 scripts/web_to_md.py https://url1 https://url2
python3.11 scripts/web_to_md.py -f urls.txt
python3.11 scripts/web_to_md.py https://example.com -o output.md
```

**Dependencies (under python3.11):**
| Package | Status (python3.11) | Install |
|---------|---------------------|---------|
| `requests` | ❌ missing | `python3.11 -m pip install requests` |
| `beautifulsoup4` (bs4) | ❌ missing | `python3.11 -m pip install beautifulsoup4` |
| `Pillow` (PIL, optional — WebP conversion) | ❌ missing | `python3.11 -m pip install Pillow` |
| `curl_cffi` (optional — TLS bypass for WeChat etc.) | ❌ missing | `python3.11 -m pip install curl_cffi` |

---

## Summary: Dependency Status

**Runtime:** Must use `python3.11` (`/Users/kaku/.local/bin/python3.11`). System `python3` (3.9) cannot parse the syntax.

**Install all dependencies for python3.11 at once:**
```bash
python3.11 -m pip install PyMuPDF python-docx openpyxl requests beautifulsoup4 Pillow
# Optional (for WeChat/blocked-site fetching):
python3.11 -m pip install curl_cffi
```

**After installing, all 4 scripts will run immediately.**

| Script | Core deps under python3.11 | Ready? |
|--------|---------------------------|--------|
| `pdf_to_md.py` | PyMuPDF | after `pip install PyMuPDF` |
| `doc_to_md.py` | python-docx, pandoc (installed) | after `pip install python-docx` |
| `excel_to_md.py` | openpyxl | after `pip install openpyxl` |
| `web_to_md.py` | requests, beautifulsoup4 | after `pip install requests beautifulsoup4` |

---

## Source

Ported from: https://github.com/hugohe3/ppt-master/tree/main/skills/ppt-master/scripts/source_to_md
