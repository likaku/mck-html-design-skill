#!/usr/bin/env python3
"""html_quality_checker.py — 8-check HTML quality gate for mck-html-design v3.

Usage:
    python3 html_quality_checker.py <html_file> [--spec-lock <spec_lock.json>]

Exit codes:
    0 — no ERRORs (may have WARNs)
    1 — at least one ERROR
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# ── optional imports ────────────────────────────────────────────────────────

try:
    from bs4 import BeautifulSoup, Tag
    _BS4 = True
except ImportError:
    _BS4 = False

# ── result helpers ──────────────────────────────────────────────────────────

PASS  = "PASS"
WARN  = "WARN"
ERROR = "ERROR"

Result = Tuple[str, str, str]  # (level, check_name, detail)


def _result(level: str, name: str, detail: str = "") -> Result:
    return (level, name, detail)


def _fmt(r: Result) -> str:
    level, name, detail = r
    if detail:
        return f"[{level}] {name}: {detail}"
    return f"[{level}] {name}"


# ── HTML loading ─────────────────────────────────────────────────────────────

def _load(html_path: Path):
    """Return (soup, raw_text). soup is None if bs4 unavailable."""
    raw = html_path.read_text(encoding="utf-8", errors="replace")
    if _BS4:
        soup = BeautifulSoup(raw, "html.parser")
        return soup, raw
    return None, raw


# ── SpecLock loading (lightweight — avoid import cycle with mck_html pkg) ──

def _load_spec(spec_path: Optional[Path]) -> Optional[dict]:
    if spec_path is None:
        return None
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    return data


# ═══════════════════════════════════════════════════════════════════════════
# Check 1: ECharts container id uniqueness
# ═══════════════════════════════════════════════════════════════════════════

def check_echart_id_unique(soup, raw: str) -> Result:
    name = "ECharts容器id唯一性"
    ids = re.findall(r'id=["\']chart-[^"\']*["\']', raw)
    id_values = [re.sub(r'^id=["\']|["\']$', "", s) for s in ids]
    seen = set()
    dupes = []
    for v in id_values:
        if v in seen:
            dupes.append(v)
        seen.add(v)
    if dupes:
        return _result(ERROR, name, f"重复 id: {', '.join(sorted(set(dupes)))}")
    return _result(PASS, name)


# ═══════════════════════════════════════════════════════════════════════════
# Check 2: Slide count vs spec_lock.total_pages
# ═══════════════════════════════════════════════════════════════════════════

def check_slide_count(soup, raw: str, spec: Optional[dict]) -> Result:
    name = "slide数量一致性"
    if spec is None:
        return _result(PASS, name, "（无 spec_lock，跳过）")
    expected = spec.get("total_pages", 0)
    if soup and _BS4:
        slides = soup.find_all(class_="slide")
        actual = len(slides)
    else:
        actual = len(re.findall(r'class=["\'][^"\']*\bslide\b[^"\']*["\']', raw))
    if actual != expected:
        return _result(ERROR, name, f"期望 {expected} 页，实际 {actual} 页")
    return _result(PASS, name)


# ═══════════════════════════════════════════════════════════════════════════
# Check 3: Empty slide detection
# ═══════════════════════════════════════════════════════════════════════════

_EMPTY_THRESHOLD = 100  # chars of inner text

def check_empty_slides(soup, raw: str) -> Result:
    name = "空 slide 检测"
    empty_indices = []
    if soup and _BS4:
        slides = soup.find_all(class_="slide")
        for i, slide in enumerate(slides, 1):
            text = slide.get_text(strip=True)
            if len(text) < _EMPTY_THRESHOLD:
                empty_indices.append(i)
    else:
        # rough fallback: find slide divs and measure inner html length
        blocks = re.split(r'class=["\'][^"\']*\bslide\b', raw)[1:]
        for i, block in enumerate(blocks, 1):
            # grab up to closing </div> (approximate)
            inner = block[:500]
            text = re.sub(r'<[^>]+>', '', inner).strip()
            if len(text) < _EMPTY_THRESHOLD:
                empty_indices.append(i)
    if empty_indices:
        return _result(WARN, name, f"内容过少的 slide: {empty_indices}")
    return _result(PASS, name)


# ═══════════════════════════════════════════════════════════════════════════
# Check 4: ECharts script injection
# ═══════════════════════════════════════════════════════════════════════════

def check_echart_scripts(soup, raw: str) -> Result:
    name = "ECharts脚本注入"
    # find all chart container ids
    container_ids = re.findall(r'id=["\']chart-([^"\']+)["\']', raw)
    if not container_ids:
        return _result(PASS, name, "无 ECharts 容器")
    missing = []
    for cid in container_ids:
        full_id = f"chart-{cid}"
        # look for echarts.init with this id
        pattern = re.escape(full_id)
        if not re.search(pattern, raw[raw.find(f'id="{full_id}"') + 1:] if f'id="{full_id}"' in raw else raw):
            missing.append(full_id)
        # more robust: check that getElementById or querySelector references it in a <script>
        if not re.search(r'(?:getElementById|querySelector)\(["\']' + re.escape(full_id), raw):
            if full_id not in missing:
                missing.append(full_id)
    # de-dup
    missing = list(dict.fromkeys(missing))
    if missing:
        return _result(WARN, name, f"缺少初始化脚本: {missing}")
    return _result(PASS, name)


# ═══════════════════════════════════════════════════════════════════════════
# Check 5: Color compliance (warning only)
# ═══════════════════════════════════════════════════════════════════════════

def _collect_palette_colors(spec: dict) -> set:
    palette = spec.get("color_palette", {})
    colors: set = set()
    for key in ("primary", "secondary", "accent"):
        v = palette.get(key)
        if v:
            colors.add(v.lower())
    for v in palette.get("neutrals", []):
        colors.add(v.lower())
    for v in palette.get("semantic", {}).values():
        colors.add(v.lower())
    canvas = spec.get("canvas", {})
    for key in ("background_color", "brand_color", "accent_color"):
        v = canvas.get(key)
        if v:
            colors.add(v.lower())
    return colors


def check_color_compliance(soup, raw: str, spec: Optional[dict]) -> Result:
    name = "颜色合规性"
    if spec is None:
        return _result(PASS, name, "（无 spec_lock，跳过）")
    allowed = _collect_palette_colors(spec)
    # extract all hex colors from CSS/style attributes
    found_colors = set(c.lower() for c in re.findall(r'#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b', raw))
    unknown = found_colors - allowed
    if unknown:
        return _result(WARN, name, f"发现 {len(unknown)} 个未在 spec_lock 中定义的颜色: {sorted(unknown)[:5]}")
    return _result(PASS, name)


# ═══════════════════════════════════════════════════════════════════════════
# Check 6: Canvas size
# ═══════════════════════════════════════════════════════════════════════════

def check_canvas_size(soup, raw: str, spec: Optional[dict]) -> Result:
    name = "画布尺寸检查"
    if spec is None:
        return _result(PASS, name, "（无 spec_lock，跳过）")
    canvas = spec.get("canvas", {})
    expected_w = canvas.get("width")
    expected_h = canvas.get("height")
    if not expected_w or not expected_h:
        return _result(WARN, name, "spec_lock.canvas 缺少 width/height")

    mismatches = []
    if soup and _BS4:
        slides = soup.find_all(class_="slide")
        for i, slide in enumerate(slides, 1):
            style = slide.get("style", "")
            w_match = re.search(r'width\s*:\s*(\d+)px', style)
            h_match = re.search(r'height\s*:\s*(\d+)px', style)
            if w_match and int(w_match.group(1)) != expected_w:
                mismatches.append(f"slide {i} width={w_match.group(1)}px (期望 {expected_w}px)")
            if h_match and int(h_match.group(1)) != expected_h:
                mismatches.append(f"slide {i} height={h_match.group(1)}px (期望 {expected_h}px)")
    else:
        # regex fallback: check for explicit wrong sizes
        w_vals = set(re.findall(r'width\s*:\s*(\d+)px', raw))
        h_vals = set(re.findall(r'height\s*:\s*(\d+)px', raw))
        bad_w = [v for v in w_vals if int(v) not in (expected_w,)]
        bad_h = [v for v in h_vals if int(v) not in (expected_h,)]
        if bad_w:
            mismatches.append(f"意外宽度: {bad_w[:3]}")
        if bad_h:
            mismatches.append(f"意外高度: {bad_h[:3]}")

    if mismatches:
        return _result(ERROR, name, "; ".join(mismatches[:3]))
    return _result(PASS, name)


# ═══════════════════════════════════════════════════════════════════════════
# Check 7: Non-canonical font-family
# ═══════════════════════════════════════════════════════════════════════════

# Canonical font names that are acceptable
_CANONICAL_FONT_KEYWORDS = {
    "georgia", "arial", "helvetica", "sans-serif", "serif",
    "kaiti", "stkaiti", "simsun", "times new roman",
    "monospace", "courier", "inherit", "initial", "unset",
}

def check_font_family(soup, raw: str) -> Result:
    name = "字体检查"
    font_decls = re.findall(r'font-family\s*:\s*([^;}"\']+)', raw, re.IGNORECASE)
    non_canonical = []
    for decl in font_decls:
        fonts = [f.strip().strip("'\"").lower() for f in decl.split(",")]
        bad = [f for f in fonts if f and not any(kw in f for kw in _CANONICAL_FONT_KEYWORDS)]
        if bad:
            non_canonical.extend(bad)
    non_canonical = list(dict.fromkeys(non_canonical))
    if non_canonical:
        return _result(WARN, name, f"非规范字体: {non_canonical[:5]}")
    return _result(PASS, name)


# ═══════════════════════════════════════════════════════════════════════════
# Check 8: overflow:hidden on .slide
# ═══════════════════════════════════════════════════════════════════════════

def check_overflow_hidden(soup, raw: str) -> Result:
    name = "overflow hidden 缺失"
    missing_indices = []
    if soup and _BS4:
        slides = soup.find_all(class_="slide")
        for i, slide in enumerate(slides, 1):
            style = slide.get("style", "")
            if "overflow" not in style.lower():
                missing_indices.append(i)
    else:
        # Check if any slide-style block is missing overflow
        # rough: just check if there's any overflow:hidden/overflow:auto in the file
        if not re.search(r'overflow\s*:\s*hidden', raw, re.IGNORECASE):
            return _result(WARN, name, "全局未发现 overflow:hidden 声明")
        return _result(PASS, name)

    if missing_indices:
        n = len(missing_indices)
        indices_str = str(missing_indices[:5]) + ("..." if n > 5 else "")
        return _result(WARN, name, f"{n} 个 slide 缺少 overflow:hidden — 索引 {indices_str}")
    return _result(PASS, name)


# ═══════════════════════════════════════════════════════════════════════════
# Runner
# ═══════════════════════════════════════════════════════════════════════════

def run_checks(html_path: Path, spec_path: Optional[Path]) -> List[Result]:
    soup, raw = _load(html_path)
    spec = _load_spec(spec_path)

    results: List[Result] = [
        check_echart_id_unique(soup, raw),
        check_slide_count(soup, raw, spec),
        check_empty_slides(soup, raw),
        check_echart_scripts(soup, raw),
        check_color_compliance(soup, raw, spec),
        check_canvas_size(soup, raw, spec),
        check_font_family(soup, raw),
        check_overflow_hidden(soup, raw),
    ]
    return results


def print_report(results: List[Result]) -> int:
    pass_n = warn_n = error_n = 0
    for r in results:
        print(_fmt(r))
        if r[0] == PASS:
            pass_n += 1
        elif r[0] == WARN:
            warn_n += 1
        else:
            error_n += 1
    print("---")
    print(f"总计: {pass_n} PASS / {warn_n} WARN / {error_n} ERROR")
    return 1 if error_n > 0 else 0


def main() -> None:
    parser = argparse.ArgumentParser(description="McKinsey HTML quality checker")
    parser.add_argument("html_file", help="Path to the HTML file to check")
    parser.add_argument("--spec-lock", dest="spec_lock", default=None,
                        help="Path to spec_lock.json")
    args = parser.parse_args()

    html_path = Path(args.html_file)
    if not html_path.exists():
        print(f"ERROR: HTML file not found: {html_path}", file=sys.stderr)
        sys.exit(2)

    spec_path = Path(args.spec_lock) if args.spec_lock else None
    if spec_path is not None and not spec_path.exists():
        print(f"ERROR: spec_lock file not found: {spec_path}", file=sys.stderr)
        sys.exit(2)

    results = run_checks(html_path, spec_path)
    exit_code = print_report(results)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
