#!/usr/bin/env python3
"""
svg_chart_replacer.py — Replace [chart] placeholders in SVGs with ECharts.

When pptx_to_svg encounters a chart (<p:graphicFrame> with chart URI), it
emits a placeholder rect. This script:
  1. Extracts chart data from the original PPTX
  2. Replaces the placeholder with an ECharts-ready <foreignObject> or
     generates a companion JS init script for the HTML assembly step.

The output is a JSON mapping: { "slide_06": { chart_id, type, data, position } }
which the HTML assembler uses to inject ECharts containers.

Usage:
    python svg_chart_replacer.py <pptx_file> <svg_dir> [-o charts.json]
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
except ImportError:
    print("[ERROR] python-pptx required")
    import sys; sys.exit(1)


def emu_to_px(emu) -> float:
    if emu is None:
        return 0
    return round(int(emu) / 914400 * 96, 1)


# ─────────────────────────────────────────
# Chart type mapping
# ─────────────────────────────────────────

CHART_TYPE_MAP = {
    "COLUMN_CLUSTERED": "bar",
    "COLUMN_STACKED": "bar",
    "COLUMN_STACKED_100": "bar",
    "BAR_CLUSTERED": "bar_horizontal",
    "BAR_STACKED": "bar_horizontal",
    "BAR_STACKED_100": "bar_horizontal",
    "LINE": "line",
    "LINE_MARKERS": "line",
    "LINE_STACKED": "line",
    "AREA": "line",
    "AREA_STACKED": "line",
    "PIE": "pie",
    "PIE_EXPLODED": "pie",
    "DOUGHNUT": "pie",
    "DOUGHNUT_EXPLODED": "pie",
    "XY_SCATTER": "scatter",
    "BUBBLE": "scatter",
    "RADAR": "radar",
    "RADAR_FILLED": "radar",
}


def _resolve_echart_type(pptx_type_str: str) -> str:
    """Map PPTX chart type to ECharts series type."""
    for key, val in CHART_TYPE_MAP.items():
        if key in pptx_type_str:
            return val
    return "bar"


# ─────────────────────────────────────────
# Extract charts from PPTX
# ─────────────────────────────────────────

def extract_charts(pptx_path: str) -> dict:
    """Extract all charts with position, type, and data.

    Returns: {
        slide_num: [{
            "id": "chart-6-1",
            "x": float, "y": float, "w": float, "h": float,
            "echart_type": str,
            "stacked": bool,
            "categories": list,
            "series": [{"name": str, "values": list}],
        }]
    }
    """
    prs = Presentation(pptx_path)
    zf = zipfile.ZipFile(pptx_path)
    ns_c = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
    ns_r = 'http://schemas.openxmlformats.org/package/2006/relationships'

    result = {}
    slide_num = 0

    for slide in prs.slides:
        slide_num += 1
        charts_on_slide = []
        chart_idx = 0

        for shape in slide.shapes:
            if not (hasattr(shape, 'has_chart') and shape.has_chart):
                continue

            chart_idx += 1
            chart = shape.chart
            ct_str = str(chart.chart_type)
            echart_type = _resolve_echart_type(ct_str)
            stacked = "STACKED" in ct_str

            # Position
            x = emu_to_px(shape.left)
            y = emu_to_px(shape.top)
            w = emu_to_px(shape.width)
            h = emu_to_px(shape.height)

            # Extract data via python-pptx
            categories = []
            series_list = []

            try:
                plot = chart.plots[0]
                if hasattr(plot, 'categories') and plot.categories:
                    categories = [str(c) for c in plot.categories]
            except:
                pass

            for s in chart.series:
                sd = {
                    "name": str(s.name) if hasattr(s, 'name') and s.name else f"Series {len(series_list)+1}",
                    "values": []
                }
                try:
                    sd["values"] = [round(float(v), 2) if v is not None else 0 for v in s.values]
                except:
                    pass
                series_list.append(sd)

            # If no categories, try to infer from context (common: years)
            if not categories and series_list and series_list[0]["values"]:
                n = len(series_list[0]["values"])
                # Common pattern: 5 years of data
                if n == 5:
                    categories = ["2021", "2022", "2023", "2024", "2025"]
                elif n == 4:
                    categories = ["Q1", "Q2", "Q3", "Q4"]
                else:
                    categories = [str(i+1) for i in range(n)]

            charts_on_slide.append({
                "id": f"chart-{slide_num}-{chart_idx}",
                "x": x, "y": y, "w": w, "h": h,
                "echart_type": echart_type,
                "stacked": stacked,
                "categories": categories,
                "series": series_list,
                "original_type": ct_str,
            })

        if charts_on_slide:
            result[slide_num] = charts_on_slide

    zf.close()
    return result


# ─────────────────────────────────────────
# Replace [chart] placeholders in SVG
# ─────────────────────────────────────────

def replace_chart_placeholder(svg_content: str, chart_info: dict) -> str:
    """Remove the [chart] placeholder rect+text from SVG (chart rendered as HTML overlay)."""
    # Find and remove the placeholder pattern:
    # <rect ... stroke="#999999" stroke-dasharray="4 4"/>
    # <text ...>[chart]</text>
    # The actual ECharts div is placed as an HTML overlay on top of the SVG.
    placeholder_pattern = (
        r'<rect[^>]*stroke="#999999"[^>]*stroke-dasharray="4 4"[^/]*/>'
        r'\s*<text[^>]*>\[chart\]</text>'
    )

    svg_content = re.sub(placeholder_pattern, '', svg_content, count=1)
    return svg_content


def generate_chart_overlays(charts_for_slide: list[dict]) -> str:
    """Generate absolute-positioned HTML divs for ECharts overlays.

    These divs are placed inside the .slide container, after the <svg>,
    using position:absolute to overlay on top of the SVG at the correct
    coordinates. This avoids foreignObject browser compatibility issues.
    """
    if not charts_for_slide:
        return ""
    parts = []
    for chart in charts_for_slide:
        cid = chart["id"]
        x, y, w, h = chart["x"], chart["y"], chart["w"], chart["h"]
        parts.append(
            f'<div id="{cid}" style="position:absolute;left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px;"></div>'
        )
    return "\n".join(parts)


# ─────────────────────────────────────────
# Generate ECharts init JS
# ─────────────────────────────────────────

CHART_COLORS = ['#051C2C', '#00A9F4', '#2251FF', '#3C96B4', '#AAE6F0', '#AFC3FF']


def generate_echart_init_js(charts: dict) -> str:
    """Generate JavaScript to initialize all ECharts instances."""
    if not charts:
        return ""

    js_parts = ['<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>']
    js_parts.append('<script>')
    js_parts.append('document.addEventListener("DOMContentLoaded", function() {')
    js_parts.append(f'  var C = {json.dumps(CHART_COLORS)};')

    for slide_num, chart_list in charts.items():
        for chart in chart_list:
            cid = chart["id"]
            etype = chart["echart_type"]
            cats = json.dumps(chart["categories"], ensure_ascii=False)
            series_js = []

            for i, s in enumerate(chart["series"]):
                vals = json.dumps(s["values"])
                name = json.dumps(s["name"], ensure_ascii=False)

                if etype == "pie":
                    # Pie: data is [{name, value}]
                    pie_data = [{"name": c, "value": v} for c, v in zip(chart["categories"], s["values"])]
                    series_js.append(
                        f'{{type:"pie",radius:["30%","65%"],data:{json.dumps(pie_data, ensure_ascii=False)},'
                        f'label:{{fontSize:11}},itemStyle:{{borderRadius:4,borderColor:"#fff",borderWidth:2}}}}'
                    )
                elif etype == "line":
                    series_js.append(
                        f'{{name:{name},type:"line",data:{vals},smooth:true,'
                        f'itemStyle:{{color:C[{i}%6]}},lineStyle:{{width:2}}}}'
                    )
                elif etype == "bar_horizontal":
                    series_js.append(
                        f'{{name:{name},type:"bar",data:{vals},'
                        f'stack:{json.dumps("total" if chart["stacked"] else None)},'
                        f'itemStyle:{{color:C[{i}%6]}},barMaxWidth:30}}'
                    )
                else:  # bar (vertical)
                    series_js.append(
                        f'{{name:{name},type:"bar",data:{vals},'
                        f'stack:{json.dumps("total" if chart["stacked"] else None)},'
                        f'itemStyle:{{color:C[{i}%6]}},barMaxWidth:35}}'
                    )

            # Build option
            if etype == "pie":
                option = (
                    f'{{tooltip:{{trigger:"item"}},'
                    f'series:[{",".join(series_js)}]}}'
                )
            elif etype == "bar_horizontal":
                option = (
                    f'{{tooltip:{{trigger:"axis",axisPointer:{{type:"shadow"}}}},'
                    f'grid:{{top:20,right:20,bottom:30,left:70}},'
                    f'xAxis:{{type:"value",axisLabel:{{fontSize:10}}}},'
                    f'yAxis:{{type:"category",data:{cats},axisLabel:{{fontSize:10}}}},'
                    f'series:[{",".join(series_js)}]}}'
                )
            else:
                option = (
                    f'{{tooltip:{{trigger:"axis",axisPointer:{{type:"shadow"}}}},'
                    f'grid:{{top:20,right:20,bottom:30,left:50}},'
                    f'xAxis:{{type:"category",data:{cats},axisLabel:{{fontSize:10}}}},'
                    f'yAxis:{{type:"value",axisLabel:{{fontSize:10}}}},'
                    f'series:[{",".join(series_js)}]}}'
                )

            js_parts.append(f'  var el=document.getElementById("{cid}");')
            js_parts.append(f'  if(el){{var c=echarts.init(el);c.setOption({option});'
                          f'window.addEventListener("resize",function(){{c.resize()}})}}')

    js_parts.append('});')
    js_parts.append('</script>')
    return '\n'.join(js_parts)


# ─────────────────────────────────────────
# CLI
# ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Extract PPTX charts and prepare ECharts replacements")
    parser.add_argument("pptx", help="Input .pptx file")
    parser.add_argument("svg_dir", help="SVG directory to patch")
    parser.add_argument("-o", "--output", default="charts.json", help="Output JSON")
    args = parser.parse_args()

    charts = extract_charts(args.pptx)
    print(f"[INFO] Found charts on {len(charts)} slides: {list(charts.keys())}")

    # Patch SVGs
    svg_dir = Path(args.svg_dir)
    for slide_num, chart_list in charts.items():
        svg_file = svg_dir / f"slide_{slide_num:02d}.svg"
        if not svg_file.exists():
            continue
        content = svg_file.read_text(encoding="utf-8")
        for chart_info in chart_list:
            content = replace_chart_placeholder(content, chart_info)
        svg_file.write_text(content, encoding="utf-8")
        print(f"  Slide {slide_num}: {len(chart_list)} chart(s) replaced")

    # Save JSON
    Path(args.output).write_text(json.dumps(charts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Charts JSON: {args.output}")


if __name__ == "__main__":
    main()
