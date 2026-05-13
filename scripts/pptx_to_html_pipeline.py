#!/usr/bin/env python3
"""
pptx_to_html_pipeline.py — Complete PPTX → HTML conversion pipeline.

One-command pipeline that chains all steps:
  1. pptx_to_svg  — Pixel-accurate OOXML → SVG conversion
  2. svg_harness  — Enforce consistent layout (fonts, lines, footer, overflow)
  3. svg_chart_replacer — Replace chart placeholders with ECharts
  4. HTML assembly — Combine SVGs + ECharts JS into single HTML file

Usage:
    python pptx_to_html_pipeline.py input.pptx [-o output.html] [--slides 1-10]

This is the top-level entry point for the mck-html-design skill.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

# Ensure script directory is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pptx_to_svg import convert_pptx_to_svg
from pptx_to_svg.converter import ConvertOptions
from svg_chart_replacer import extract_charts, replace_chart_placeholder, generate_echart_init_js, generate_chart_overlays, generate_chart_overlays

# svg_harness was removed (superseded by cg_mckinsey design_spec templates).
# The harness step is now a no-op; keeping the pipeline functional without it.
try:
    from svg_harness import process_directory as apply_harness
except ImportError:
    apply_harness = None


def pipeline(
    pptx_path: str,
    output_path: str,
    slide_range: tuple[int, int] | None = None,
    embed_images: bool = True,
) -> None:
    """Run the full PPTX → HTML pipeline."""

    pptx = Path(pptx_path)
    if not pptx.exists():
        print(f"[ERROR] File not found: {pptx_path}")
        sys.exit(1)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Use a temp directory for intermediate SVGs
    with TemporaryDirectory(prefix="mck_pipeline_") as tmp:
        svg_dir = Path(tmp) / "svg_output"

        # ─── Step 1: PPTX → SVG ───
        print(f"[1/4] Converting PPTX → SVG...")
        options = ConvertOptions(
            embed_images=embed_images,
            inheritance_mode="flat",
        )
        result = convert_pptx_to_svg(pptx, svg_dir, options)
        total_slides = len(result.slides)
        print(f"       {total_slides} slides, canvas {result.canvas_px[0]:.0f}×{result.canvas_px[1]:.0f}")

        # ─── Step 2: Harness (optional) ───
        actual_svg_dir = svg_dir / "svg"
        if apply_harness is not None:
            print(f"[2/4] Applying layout harness...")
            apply_harness(actual_svg_dir)
        else:
            print(f"[2/4] Harness skipped (svg_harness not installed)")

        # ─── Step 3: Chart replacement ───
        print(f"[3/4] Extracting charts → ECharts...")
        charts = extract_charts(str(pptx))
        for slide_num, chart_list in charts.items():
            svg_file = actual_svg_dir / f"slide_{slide_num:02d}.svg"
            if svg_file.exists():
                content = svg_file.read_text(encoding="utf-8")
                for chart_info in chart_list:
                    content = replace_chart_placeholder(content, chart_info)
                svg_file.write_text(content, encoding="utf-8")
        chart_count = sum(len(v) for v in charts.values())
        print(f"       {chart_count} charts on {len(charts)} slides")

        # ─── Step 4: HTML Assembly ───
        print(f"[4/4] Assembling HTML...")
        svg_files = sorted(actual_svg_dir.glob("slide_*.svg"))

        # Apply slide range filter
        if slide_range:
            start, end = slide_range
            svg_files = [f for f in svg_files
                        if start <= int(f.stem.replace("slide_", "")) <= end]

        slides_html = []
        for f in svg_files:
            slide_num_str = f.stem.replace("slide_", "").lstrip("0") or "0"
            sn = int(slide_num_str)
            svg_text = f.read_text(encoding="utf-8")
            overlay = generate_chart_overlays(charts.get(sn, []))
            slides_html.append(
                f'<div class="slide" style="position:relative">'
                f'{svg_text}{overlay}</div>'
            )

        # Generate ECharts JS for included slides
        if slide_range:
            charts_subset = {int(k): v for k, v in charts.items()
                          if slide_range[0] <= int(k) <= slide_range[1]}
        else:
            charts_subset = {int(k): v for k, v in charts.items()}

        echart_js = generate_echart_init_js(charts_subset)

        canvas_w = result.canvas_px[0]
        canvas_h = result.canvas_px[1]

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={canvas_w:.0f}">
<title>{pptx.stem}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#1a1a2e;display:flex;flex-direction:column;align-items:center;padding:30px 0;gap:20px;font-family:Arial,KaiTi,STKaiti,sans-serif}}
.slide{{width:{canvas_w:.0f}px;height:{canvas_h:.0f}px;background:#fff;box-shadow:0 4px 24px rgba(0,0,0,.5);overflow:hidden;position:relative}}
.slide svg{{display:block;width:{canvas_w:.0f}px;height:{canvas_h:.0f}px}}
@media print{{body{{background:#fff;padding:0;gap:0}}.slide{{box-shadow:none;page-break-after:always}}}}
</style>
</head>
<body>
{chr(10).join(slides_html)}
{echart_js}
</body>
</html>"""

        output.write_text(html, encoding="utf-8")
        size_kb = len(html.encode("utf-8")) / 1024
        slide_count = len(slides_html)
        print(f"\n[OK] {output}")
        print(f"     {slide_count} slides | {chart_count} ECharts | {size_kb:.0f} KB")


def main():
    parser = argparse.ArgumentParser(
        description="PPTX → HTML pipeline (SVG + ECharts)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pptx_to_html_pipeline.py deck.pptx
  python pptx_to_html_pipeline.py deck.pptx -o output/deck.html
  python pptx_to_html_pipeline.py deck.pptx --slides 1-20
        """,
    )
    parser.add_argument("pptx", help="Input .pptx file")
    parser.add_argument("-o", "--output", help="Output .html (default: same name)")
    parser.add_argument("--slides", help="Slide range: '1-10' or '5'")
    parser.add_argument("--no-embed", action="store_true", help="Don't embed images (use external files)")

    args = parser.parse_args()

    output = args.output or str(Path(args.pptx).with_suffix(".html"))

    slide_range = None
    if args.slides:
        if '-' in args.slides:
            a, b = args.slides.split('-')
            slide_range = (int(a), int(b))
        else:
            n = int(args.slides)
            slide_range = (n, n)

    pipeline(args.pptx, output, slide_range, embed_images=not args.no_embed)


if __name__ == "__main__":
    main()
