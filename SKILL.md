---
name: mck-html-design
description: >-
  PPTX conversion toolkit: (1) Extract SVG skeleton templates from client PPTX
  files for ppt-master layout creation, (2) Convert existing PPTX decks to
  browsable single-file HTML with ECharts chart replacement.
  Also includes MckHtmlEngine (68 layout methods) as a backup/advanced mode
  for direct HTML slide generation.
version: 4.0.0
license: Apache-2.0
required_tools: Read, Write, Bash
requires: python3.11+
---

# mck-html-design — PPTX Conversion Toolkit

> **Version**: 4.0.0 · **License**: Apache-2.0
>
> **Required tools**: Read, Write, Bash · **Requires**: python3.11+

---

## Overview

This skill provides two core capabilities for working with PowerPoint files:

1. **PPTX → SVG Template Extraction** — pixel-accurate conversion of PPTX slides into clean SVG skeletons, used to create new layout templates for `ppt-master`
2. **PPTX → HTML Conversion** — one-command pipeline that converts any PPTX deck into a self-contained, browsable HTML file with optional ECharts chart replacement

Additionally, **MckHtmlEngine** (68 layout methods) is preserved as a backup/advanced mode for programmatic HTML slide generation.

---

## When to Use This Skill

| Scenario | Use Case |
|----------|----------|
| **Extract templates from client PPTX** | Use `pptx_to_svg` engine to generate skeleton SVGs → add to `ppt-master/templates/layouts/` |
| **Convert PPTX to HTML for review** | Use `pptx_to_html_pipeline.py` for a single browsable HTML file |
| **Replace PPTX charts with interactive ECharts** | Pipeline Step 3 auto-detects and replaces chart placeholders |
| **Programmatic HTML slides (advanced)** | Use MckHtmlEngine directly (68 methods, 12 categories) |

### When NOT to use this skill

- **Creating new consulting-style presentations** → Use `ppt-master` with `cg_mckinsey` templates instead. The sub-agent writes SVG+HTML directly using the 40 skeleton templates and design_spec.
- **McKinsey template/harness workflow** → Deprecated. Use `ppt-master` cg_mckinsey design_spec.

---

## Core Use Case 1: PPTX → SVG Template Extraction

Extract layout structures from client PPTX decks to create new skeleton templates for `ppt-master`.

### Quick Start

```bash
cd /Users/kaku/.workbuddy/skills/mck-html-design/scripts
python3.11 -c "
from pptx_to_svg.converter import convert_pptx_to_svg, ConvertOptions
opts = ConvertOptions(embed_images=False, inheritance_mode='flat')
result = convert_pptx_to_svg('input.pptx', 'output_dir/', opts)
print(f'{len(result.slides)} slides → {result.canvas_px[0]:.0f}x{result.canvas_px[1]:.0f}')
"
```

### pptx_to_svg Engine Architecture

```
scripts/pptx_to_svg/
├── __init__.py           # Public API: convert_pptx_to_svg()
├── converter.py          # Core: ConvertOptions, slide iteration, canvas detection
├── ooxml_loader.py       # OOXML XML parsing (slide XML, theme, slideMaster)
├── shape_walker.py       # Walk sp/grpSp/pic/tbl shapes recursively
├── slide_to_svg.py       # Orchestrate per-slide SVG generation
├── fill_to_svg.py        # solidFill / gradFill / pattFill → SVG fill
├── ln_to_svg.py          # Line/border → SVG stroke attributes
├── txbody_to_svg.py      # Text body → SVG <text>/<tspan>
├── pic_to_svg.py         # Pictures → SVG <image> (base64 or external)
├── tbl_to_svg.py         # Tables → SVG <rect>+<text> grid
├── prstgeom_to_svg.py    # Preset geometries (200+ OOXML shapes)
├── custgeom_to_svg.py    # Custom geometry paths → SVG <path>
├── color_resolver.py     # Theme/scheme color resolution
├── emu_units.py          # EMU ↔ px conversion
└── effect_to_svg.py      # Shadow/glow/reflection effects
```

### Template Extraction Workflow

1. Run `convert_pptx_to_svg()` on client PPTX
2. Review generated SVGs for clean layout structures
3. Simplify SVGs into skeleton templates (remove specific content, keep layout geometry)
4. Place in `ppt-master/templates/layouts/<template_name>/`
5. Register in `layouts_index.json`
6. Write a `design_spec.md` following cg_mckinsey as the reference model

---

## Core Use Case 2: PPTX → HTML Conversion

Convert any existing PPTX file into a browsable single-file HTML document.

### Quick Start

```bash
cd /Users/kaku/.workbuddy/skills/mck-html-design/scripts
python3.11 pptx_to_html_pipeline.py input.pptx -o output.html
python3.11 pptx_to_html_pipeline.py input.pptx --slides 1-10  # subset
```

### Pipeline Steps

| Step | Description | Script |
|------|-------------|--------|
| 1/4 | PPTX → SVG (pixel-accurate) | `pptx_to_svg/` engine |
| 2/4 | Layout harness (optional, skipped if not installed) | `svg_harness.py` (removed) |
| 3/4 | Chart extraction → ECharts replacement | `svg_chart_replacer.py` |
| 4/4 | HTML assembly (single file, embedded CSS/JS) | inline in pipeline |

### Output Features

- Self-contained single HTML file
- Dark background with centered slides
- Print-friendly CSS (`@media print`) for PDF export
- ECharts 5.x interactive charts (hover tooltips, animations)
- Correct canvas sizing from source PPTX

### Chart Replacement

`svg_chart_replacer.py` auto-detects OOXML chart objects in the PPTX and replaces them with interactive ECharts 5.x instances:

```python
from svg_chart_replacer import extract_charts, replace_chart_placeholder
charts = extract_charts("deck.pptx")
# Returns {slide_num: [chart_info, ...]}
```

---

## Advanced Mode: MckHtmlEngine (Backup)

> **Status**: Preserved for backward compatibility and advanced use cases.
> For new consulting-style presentations, use `ppt-master` with `cg_mckinsey` templates.

The engine provides 68 high-level methods across 12 categories for programmatic HTML slide generation:

| Category | Methods | Examples |
|----------|---------|----------|
| Structure | cover, toc, section_break, end_slide | Title pages, navigation |
| Data | metrics, kpi_cards, gauges, sparklines | Numeric displays |
| Framework | matrix_2x2, matrix_3x3, gartner_quadrant | Strategy frameworks |
| Comparison | side_by_side, feature_comparison, before_after | Comparative layouts |
| Narrative | three_point, waterfall, flow | Story flow |
| Timeline | horizontal_timeline, milestone_tracker, roadmap | Time-based |
| Team | org_chart, team_showcase, profile_cards | People |
| Charts | donut, pie, bar, line, area (SVG + ECharts) | Data visualization |
| Images | full_bleed, side_image, image_grid | Visual |
| Advanced Viz | funnel, pyramid, scatter, bubble | Complex charts |
| Dashboards | multi_metric, executive_summary | Dashboards |
| Visual Story | hero, quote, full_width_story | Editorial |

### Usage

```python
import sys
sys.path.insert(0, '/Users/kaku/.workbuddy/skills/mck-html-design')
from mck_html import MckHtmlEngine

eng = MckHtmlEngine(total_slides=12)
eng.cover(title='Title', subtitle='Subtitle')
eng.echart_grouped_bar(title='Revenue', ...)
eng.save('output.html')
```

### ECharts Integration (echart_* methods)

For interactive/data-heavy charts, prefer `echart_*` methods over SVG versions:
- `echart_grouped_bar`, `echart_stacked_bar`, `echart_line`, `echart_area`
- `echart_donut`, `echart_pie`, `echart_radar`, `echart_waterfall`
- `echart_scatter`, `echart_bubble`, `echart_funnel`, `echart_treemap`

### Color Palette (Office Accent)

| Token | Hex | Usage |
|-------|-----|-------|
| ACCENT_1 | #1F3864 | Primary / base bars |
| ACCENT_2 | #00B0F0 | Third series / sky blue |
| ACCENT_3 | #0070C0 | Main highlight |
| ACCENT_4 | #4BACC6 | Secondary series / teal |
| ACCENT_5 | #9DC3E6 | Lower priority / pale blue |
| ACCENT_6 | #BDD7EE | Background / lightest |
| ACCENT_RED | #C62828 | Warnings/negatives ONLY |

---

## Source-to-Markdown Scripts

This skill includes convenience copies of source-to-markdown conversion scripts:

| Input | Script |
|-------|--------|
| PDF | `scripts/pdf_to_md.py` |
| DOCX | `scripts/doc_to_md.py` |
| Excel/CSV | `scripts/excel_to_md.py` |
| PPTX | `scripts/ppt_to_md.py` |
| Web/URL | `scripts/web_to_md.py` |

> **Note**: The **canonical source** for these scripts is `ppt-master/scripts/source_to_md/`.
> The copies here are kept for backward compatibility. Do not modify these — update the ppt-master versions instead.

All scripts require `python3.11+` (path: `/Users/kaku/.local/bin/python3.11`).

---

## Quality Assurance

### HTML Quality Checker

```bash
python3.11 scripts/html_quality_checker.py output.html [--spec-lock spec_lock.json]
```

Checks: text overflow, column alignment, font consistency, color compliance, ECharts rendering, responsive scaling, contrast ratio, multi-canvas support.

---

## File Structure

```
mck-html-design/
├── SKILL.md                          # This file
├── mck_html/                         # MckHtmlEngine package (backup/advanced)
│   ├── __init__.py
│   ├── engine.py                     # 68 layout methods
│   ├── core.py                       # Layout primitives
│   ├── echarts_charts.py             # ECharts 5.x integration
│   ├── constants.py                  # Color palette, typography
│   └── spec_lock.py                  # Design contract (spec_lock.json)
├── scripts/
│   ├── pptx_to_svg/                  # PPTX→SVG engine (14 modules)
│   ├── pptx_to_html_pipeline.py      # One-command PPTX→HTML
│   ├── svg_chart_replacer.py         # ECharts chart replacement
│   ├── html_quality_checker.py       # QA checker
│   ├── project_manager.py            # Project scaffolding
│   ├── pdf_to_md.py                  # Source conversion (see note above)
│   ├── doc_to_md.py
│   ├── excel_to_md.py
│   ├── ppt_to_md.py
│   └── web_to_md.py
├── examples/                         # Usage examples
│   ├── minimal_example.py
│   ├── longevity_weekly.py
│   └── full_test.py
└── templates/                        # (Cleared — old McKinsey templates removed in v4.0)
```

---

## Changelog

### v4.0.0 (2026-05)
- **Removed** old McKinsey template files (consulting_narrative_methodology.py, industry_trend_profile.py, STYLE_GUIDE.md, mck_layout_harness.yaml)
- **Removed** svg_harness.py (layout enforcement now handled by ppt-master cg_mckinsey design_spec)
- **Refocused** skill on two core use cases: PPTX→SVG extraction and PPTX→HTML conversion
- **Marked** MckHtmlEngine as backup/advanced mode
- **Pipeline**: svg_harness step now gracefully skips if not installed
- New consulting-style presentations should use `ppt-master` with `cg_mckinsey` templates (40 skeleton SVGs + design_spec)
