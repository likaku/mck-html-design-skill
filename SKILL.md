---
name: mck-html-design
description: >-
  Create professional, consultant-grade HTML presentations from scratch
  using MckHtmlEngine with McKinsey-style design. Use when user asks to
  create HTML slides, web presentations, browser-based pitch decks, or
  any self-contained HTML presentation. AI calls eng.cover(), eng.donut(),
  eng.timeline() etc — 68 high-level methods across 12 categories
  (structure, data, framework, comparison, narrative, timeline, team,
  charts, images, advanced viz, dashboards, visual storytelling),
  consistent typography, SVG chart rendering, presentation mode with
  keyboard navigation, and production-hardened guard rails.
---

# McKinsey HTML Design Framework

> **Version**: 2.0.0 · **License**: Apache-2.0
>
> **Required tools**: Read, Write, Bash · **Requires**: python3

## Overview

This skill encodes the complete design specification for **professional HTML presentations** — a consultant-grade HTML framework based on McKinsey design principles. It includes:

- **68 layout patterns** across 12 categories (structure, data, framework, comparison, narrative, timeline, team, charts, images, advanced viz, dashboards, visual storytelling)
- **Color system** and strict typography hierarchy
- **SVG-based chart rendering** — donut, pie, gauge, line charts all rendered as crisp SVG
- **Self-contained output** — single HTML file with embedded CSS, JavaScript, fonts
- **Presentation mode** — keyboard navigation (arrow keys, F for fullscreen, Escape to exit)
- **Print support** — clean page breaks for PDF export
- **API-compatible with MckEngine (PPT version)** — same method names, same parameters

---

## When to Use This Skill

Use this skill when users ask to:

1. **Create HTML presentations** — web-based slide decks, browser presentations, HTML pitch decks
2. **Generate slides programmatically** — self-contained HTML files with presentation mode
3. **Apply professional design** — McKinsey consulting style, clean flat design
4. **Build specific slide types** — cover pages, data dashboards, 2×2 matrices, timelines, funnels, team introductions, charts
5. **Need cross-platform output** — HTML works everywhere, no PowerPoint needed

---

## MckHtmlEngine Quick Start

### Setup

No pip install required — pure Python, no external dependencies.

The `mck_html/` package lives inside the skill directory. Before generating any presentation, the AI MUST:

```python
import sys, os
sys.path.insert(0, '/path/to/mck_html_design_skill')
from mck_html import MckHtmlEngine
from mck_html.constants import *  # NAVY, ACCENT_BLUE, etc.
```

### Complete Generation Pattern

Every presentation script follows this exact pattern:

```python
import sys, os
sys.path.insert(0, '/path/to/mck_html_design_skill')
from mck_html import MckHtmlEngine
from mck_html.constants import *

eng = MckHtmlEngine(total_slides=12)

# ── Structure ──
eng.cover(title='Q1 2026 战略回顾', subtitle='董事会汇报', author='战略部', date='2026年3月')
eng.toc(items=[('1', '市场概览', '当前竞争格局'),
               ('2', '财务分析', '收入与增长'),
               ('3', '下一步计划', '战略举措')])
eng.section_divider('第一章', '市场概览', '当前竞争格局分析')

# ── Data ──
eng.big_number(title='年度收入增长显著', number='¥2.8B', unit='年收入',
               description='同比增长23%，超出市场预期')
eng.donut(title='收入构成分析', segments=[
    (0.45, NAVY, '产品销售'),
    (0.30, ACCENT_BLUE, '服务收入'),
    (0.25, ACCENT_GREEN, '订阅收入'),
], center_label='100%', center_sub='总收入')

# ── Framework ──
eng.matrix_2x2(title='战略优先级矩阵', quadrants=[
    ('高优先', '#E3F2FD', '立即执行的关键项目'),
    ('战略储备', '#E8F5E9', '长期价值的投资方向'),
    ('优化空间', '#FFF3E0', '效率提升的潜力区域'),
    ('监控区域', '#FFEBEE', '需要持续关注的风险'),
])

# ── Save ──
eng.save('output/strategy_review.html')
```

### Presentation Mode

The generated HTML file includes:
- **Keyboard navigation**: Arrow keys, Space, PageUp/PageDown
- **Fullscreen**: Press `F` to enter presentation mode, `Escape` to exit
- **Auto-scaling**: Slides scale to fit any screen size
- **Slide counter**: Shows current position in the deck

---

## Color System

| Token | Hex | Usage |
|-------|-----|-------|
| `NAVY` | `#051C2C` | Primary headlines, key shapes |
| `BLACK` | `#000000` | Separator lines |
| `WHITE` | `#FFFFFF` | Text on dark backgrounds |
| `DARK_GRAY` | `#333333` | Body text |
| `MED_GRAY` | `#666666` | Secondary text |
| `LINE_GRAY` | `#CCCCCC` | Separator lines |
| `BG_GRAY` | `#F2F2F2` | Background fills |
| `ACCENT_BLUE` | `#006BA6` | Accent 1 |
| `ACCENT_GREEN` | `#007A53` | Accent 2 |
| `ACCENT_ORANGE` | `#D46A00` | Accent 3 |
| `ACCENT_RED` | `#C62828` | Accent 4 |

Light accent backgrounds: `LIGHT_BLUE`, `LIGHT_GREEN`, `LIGHT_ORANGE`, `LIGHT_RED`.

Paired sets for iteration: `ACCENT_PAIRS = [(ACCENT_BLUE, LIGHT_BLUE), ...]`

---

## Typography

| Level | Size | Font | Color | Usage |
|-------|------|------|-------|-------|
| Cover Title | 44px | Georgia | NAVY | Cover slide only |
| Section Title | 28px | Georgia | NAVY | Section dividers |
| Action Title | 22px | Georgia | BLACK | Content slide titles |
| Sub-header | 18px | Arial | varies | Card/panel headers |
| Emphasis | 16px | Arial | varies | Highlighted text |
| Body | 14px | Arial | DARK_GRAY | Main content |
| Small | 12px | Arial | DARK_GRAY | Secondary content |
| Footnote | 9px | Arial | MED_GRAY | Source, page numbers |

Font stacks:
- Header: `'KaiTi', 'STKaiti', 'SimSun', serif, 'Georgia', 'Times New Roman', serif`
- Body: `'KaiTi', 'STKaiti', 'SimSun', serif, 'Arial', 'Helvetica Neue', sans-serif`

---

## Layout Dimensions

| Element | Value (px) | Notes |
|---------|-----------|-------|
| Slide Width | 1333 | 16:9 aspect ratio |
| Slide Height | 750 | |
| Left Margin (LM) | 80 | |
| Right Margin (RM) | 80 | |
| Content Width (CW) | 1173 | SLIDE_WIDTH - LM - RM |
| Title Top | 15 | Action title position |
| Content Top | 130 | Below title + separator |
| Source Y | 705 | Source attribution line |
| Bottom Bar Y | 620 | Summary bar position |

---

## Complete Method Reference (68 methods)

### Structure (5)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `cover()` | title, subtitle, author, date | Cover slide |
| `section_divider()` | section_label, title, subtitle | Section separator |
| `toc()` | title, items, source | Table of contents |
| `closing()` | title, message, source_text | Thank you / closing |
| `appendix_title()` | title, subtitle | Appendix header |

### Data (6)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `big_number()` | title, number, unit, description, detail_items, source, bottom_bar | Large statistic |
| `two_stat()` | title, stats, detail_items, source | Two statistics side by side |
| `three_stat()` | title, stats, detail_items, source | Three statistics in a row |
| `metric_cards()` | title, cards, source | 3-4 accent-colored cards |
| `data_table()` | title, headers, rows, col_widths, source, bottom_bar | Data table |
| `table_insight()` | title, headers, rows, insights, col_widths, insight_title, source, bottom_bar | Table + insight panel |
| `scorecard()` | title, items, source | Progress bar scorecard |

### Framework (4)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `matrix_2x2()` | title, quadrants, axis_labels, source, bottom_bar | 2×2 matrix |
| `pyramid()` | title, levels, source, bottom_bar | Pyramid layers |
| `process_chevron()` | title, steps, source, bottom_bar | Horizontal process flow |
| `temple()` | title, roof_text, pillar_names, foundation_text, pillar_colors, source | Temple framework |

### Comparison (3)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `side_by_side()` | title, options, source | Two-column comparison |
| `before_after()` | title, before_title, before_points, after_title, after_points, ... | Before/after |
| `swot()` | title, quadrants, source | SWOT analysis |

### Narrative (6)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `executive_summary()` | title, headline, items, source | Navy headline + items |
| `key_takeaway()` | title, left_text, takeaways, source | Analysis + takeaways |
| `four_column()` | title, items, source | Vertical column cards |
| `quote()` | quote_text, attribution | Centered quote |
| `two_column_text()` | title, columns, source | Two text columns |
| `pros_cons()` | title, pros_title, pros, cons_title, cons, conclusion, source | Pros/cons layout |

### Timeline (2)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `timeline()` | title, milestones, source, bottom_bar | Horizontal timeline |
| `vertical_steps()` | title, steps, source, bottom_bar | Top-down steps |

### Team & Case Study (3)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `meet_the_team()` | title, members, source | Team profile cards |
| `case_study()` | title, sections, result_box, source | S/A/R sections |
| `action_items()` | title, actions, source | Action cards |

### Charts (11)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `donut()` | title, segments, center_label, center_sub, legend_x, summary, source | SVG donut chart |
| `pie()` | title, segments, legend_x, summary, source | SVG pie chart |
| `grouped_bar()` | title, categories, series, data, max_val, y_ticks, summary, source | Grouped vertical bars |
| `horizontal_bar()` | title, items, summary, source | Horizontal bars |
| `gauge()` | title, score, benchmarks, source | Semicircle gauge |
| `stacked_bar()` | title, periods, series, data, summary, source | 100% stacked bars |
| `waterfall()` | title, items, max_val, legend_items, summary, source | Waterfall bridge chart |
| `line_chart()` | title, x_labels, y_labels, values, legend_label, summary, source | SVG line chart |
| `pareto()` | title, items, max_val, summary, source | Descending bar chart |
| `stacked_area()` | title, years, series_data, max_val, summary, source | Stacked area/columns |
| `multi_bar_panel()` | title, panels, connectors, footnotes, source | Multi-panel bar charts |

### Images (7)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `content_right_image()` | title, subtitle, bullets, takeaway, image_label, source | Text + right image |
| `full_width_image()` | title, image_label, overlay_text, attribution, source | Edge-to-edge image |
| `three_images()` | title, items, source | Three image columns |
| `image_four_points()` | title, image_label, points, source | Image + 4 corner points |
| `case_study_image()` | title, sections, image_label, kpis, source | Case study + image |
| `quote_bg_image()` | image_label, quote_text, attribution, source | Quote with background |
| `goals_illustration()` | title, goals, image_label, source | Goals + illustration |

### Advanced Viz (7)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `funnel()` | title, stages, source | Top-down funnel |
| `cycle()` | title, phases, right_panel, source | Cycle diagram |
| `venn()` | title, circles, overlap_label, right_text, source | Venn diagram |
| `value_chain()` | title, stages, source, bottom_bar | Horizontal flow |
| `checklist()` | title, columns, col_widths, rows, status_map, source, bottom_bar | Status table |
| `icon_grid()` | title, items, cols, source | Icon card grid |
| `rag_status()` | title, headers, rows, source | RAG status table |

### Dashboards & Special (8)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `kpi_tracker()` | title, kpis, summary, source | KPI progress tracker |
| `bubble()` | title, bubbles, x_label, y_label, legend_items, summary, source | Bubble scatter |
| `risk_matrix()` | title, grid_colors, grid_lights, risks, y_labels, x_labels, notes, source | 3×3 risk heatmap |
| `harvey_ball_table()` | title, criteria, options, scores, legend_text, summary, source | Harvey ball matrix |
| `dashboard_kpi_chart()` | title, kpi_cards, chart_data, summary, source | KPI cards + chart |
| `dashboard_table_chart()` | title, table_data, chart_data, factoids, source | Table + chart dashboard |
| `stakeholder_map()` | title, quadrants, x_label, y_label, summary, source | 2×2 stakeholder map |
| `decision_tree()` | title, root, branches, right_panel, source | Decision tree hierarchy |
| `metric_comparison()` | title, metrics, source | Before/after metrics |
| `agenda()` | title, headers, items, footer_text, source | Meeting agenda |
| `two_col_image_grid()` | title, items, source | 2×2 image-text grid |
| `numbered_list_panel()` | title, items, panel, source | List + side panel |

---

## Production Guard Rails

1. **All text must be HTML-escaped** — use `esc()` helper
2. **Consistent font stacks** — always use `FONT_STACK_HEADER` or `FONT_STACK_BODY`
3. **Color consistency** — always use constants, never hardcode hex values in scripts
4. **Overflow protection** — all text containers use `overflow: hidden`
5. **Dynamic sizing** — card widths and heights adapt to item count
6. **Self-contained output** — no external dependencies in generated HTML
7. **Print-safe** — media queries ensure clean page breaks
8. **Accessible** — semantic HTML structure, readable font sizes
9. **Dynamic title** — toolbar brand and HTML `<title>` automatically use the `cover()` title (newlines collapsed to spaces, HTML entities escaped). No manual title configuration needed

---

## Differences from PPT Version (MckEngine)

| Aspect | PPT (MckEngine) | HTML (MckHtmlEngine) |
|--------|-----------------|---------------------|
| Output format | .pptx (PowerPoint) | .html (single file) |
| Dependencies | python-pptx, lxml | None (pure Python) |
| Charts | BLOCK_ARC native shapes | SVG paths |
| Presentation mode | PowerPoint handles it | Built-in JS navigation |
| Images | Actual image embedding | Gray placeholder boxes |
| File size | 50KB-500KB | 20KB-100KB |
| Viewing | PowerPoint/LibreOffice | Any web browser |
| API | Identical method signatures | Identical method signatures |
