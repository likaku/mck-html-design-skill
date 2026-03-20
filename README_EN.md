<p align="center">
  <h1 align="center">📊 McKinsey HTML Design Skill</h1>
  <p align="center">
    <strong>Generate McKinsey-style HTML presentations with Python — 68 layouts, zero dependencies, ready to use</strong>
  </p>

  <p align="center">

### Community

<table>
<tr>
    <td align="center" width="50%" valign="top">
      <strong>WeChat Group</strong><br/><br/>
      <img width="180" src="https://github.com/user-attachments/assets/d4eb704e-3825-4380-ac54-2fbbe4c993ce" alt="WeChat Group" />
    </td>
    <td align="center" width="50%" valign="top">
      <strong>Discord</strong><br/><br/>
      <a href="https://discord.gg/SaFybFAT">
        <img src="https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" />
      </a>
      <br/><br/>
      <span>Click to join</span>
    </td>
  </tr>
</table>
    <em>68 layouts · 12 categories · Pure Python · Single-file HTML output</em>
  </p>
</p>

<p align="center">
  <a href="#-core-value">Core Value</a> •
  <a href="#-68-layout-methods">68 Layouts</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-changelog">Changelog</a> •
  <a href="./README.md">中文</a>
</p>

---

## 🔗 Sister Project

| Project | Output Format | Link |
|---------|--------------|------|
| **McKinsey PPT Design Skill** | `.pptx` (PowerPoint) | [🔗 GitHub](https://github.com/likaku/Mck-ppt-design-skill) |
| **McKinsey HTML Design Skill** | `.html` (Browser) | 📍 You are here |

Both projects share the same design system and API signatures, with synchronized version numbers.

---

## 🔥 Core Value

> **In one sentence**: Write Python method calls, get a self-contained professional HTML presentation — no PowerPoint, no frontend knowledge, open in any browser.

### What problem does it solve?

Everyone has been there:

> You need a professional presentation but don't want to fuss over layout, colors, alignment…
>
> Or you need to **programmatically generate** reports at scale, but PowerPoint is too heavy…
>
> **68 layout methods, one line of code per slide.**

### Three Key Differentiators

| | Manual PPT | This Skill |
|---|---|---|
| 🎨 **Design Quality** | Depends on personal taste | McKinsey-grade professional design |
| ⚡ **Efficiency** | 15-30 min per slide | 1 line of code per slide |
| 🔄 **Reusable** | Copy-paste | Python script automation |

---

## 📊 68 Layout Methods

12 categories covering all common business presentation scenarios:

| # | Category | Methods | Examples |
|---|---|---|---|
| 1 | **Structure** | 5 | `cover()`, `toc()`, `section_divider()`, `closing()`, `appendix_title()` |
| 2 | **Data** | 7 | `big_number()`, `two_stat()`, `three_stat()`, `data_table()`, `table_insight()` |
| 3 | **Framework** | 4 | `matrix_2x2()`, `pyramid()`, `process_chevron()`, `temple()` |
| 4 | **Comparison** | 3 | `side_by_side()`, `before_after()`, `swot()` |
| 5 | **Narrative** | 6 | `executive_summary()`, `key_takeaway()`, `quote()`, `four_column()` |
| 6 | **Timeline** | 2 | `timeline()`, `vertical_steps()` |
| 7 | **Team & Case** | 3 | `meet_the_team()`, `case_study()`, `action_items()` |
| 8 | **Charts** | 11 | `donut()`, `pie()`, `grouped_bar()`, `horizontal_bar()`, `gauge()`, `waterfall()` |
| 9 | **Images** | 7 | `content_right_image()`, `full_width_image()`, `three_images()` |
| 10 | **Advanced Viz** | 7 | `funnel()`, `cycle()`, `venn()`, `value_chain()`, `icon_grid()` |
| 11 | **Dashboards** | 8 | `kpi_tracker()`, `bubble()`, `risk_matrix()`, `dashboard_kpi_chart()` |
| 12 | **Visual Storytelling** | 5 | `decision_tree()`, `metric_comparison()`, `agenda()`, `two_col_image_grid()` |

---

## 🚀 Quick Start

### Installation

**Zero dependencies** — pure Python 3, no pip install needed.

```bash
git clone https://github.com/likaku/mck-html-design-skill.git
```

### Minimal Example

```python
import sys, os
sys.path.insert(0, '/path/to/mck-html-design-skill')

from mck_html import MckHtmlEngine
from mck_html.constants import *

eng = MckHtmlEngine(total_slides=5)

# Cover
eng.cover(title='Q1 2026 Strategy Review', subtitle='Board Presentation', 
          author='Strategy Team', date='March 2026')

# Table of Contents
eng.toc(items=[
    ('1', 'Market Overview', 'Current competitive landscape'),
    ('2', 'Financial Analysis', 'Revenue and growth'),
    ('3', 'Next Steps', 'Strategic initiatives'),
])

# Big Number
eng.big_number(title='Significant Annual Revenue Growth', number='$2.8B', unit='Annual Revenue',
               description='23% YoY growth, exceeding market expectations')

# Donut Chart
eng.donut(title='Revenue Composition', segments=[
    (0.45, NAVY, 'Product Sales'),
    (0.30, ACCENT_BLUE, 'Service Revenue'),
    (0.25, ACCENT_GREEN, 'Subscription Revenue'),
], center_label='100%', center_sub='Total Revenue')

# Save
eng.save('output/my_deck.html')
```

Then open `output/my_deck.html` in any browser.

### Presentation Mode

The generated HTML includes built-in presentation features:

| Key | Action |
|---|---|
| `←` `→` Arrow keys | Navigate slides |
| `F` | Fullscreen mode |
| `Escape` | Exit fullscreen |
| `Space` | Next slide |

### Use as AI Skill

Place the repo in your AI IDE's Skills directory:

```
your-project/
├── .skills/
│   └── mck-html-design-skill/
│       ├── SKILL.md
│       ├── mck_html/
│       ├── examples/
│       └── ...
└── ...
```

Then tell the AI:

> "Help me create an HTML presentation"

---

## 🎨 Design System

### Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `NAVY` | `#051C2C` | Primary headlines, key shapes |
| `ACCENT_BLUE` | `#006BA6` | Accent 1 |
| `ACCENT_GREEN` | `#007A53` | Accent 2 |
| `ACCENT_ORANGE` | `#D46A00` | Accent 3 |
| `ACCENT_RED` | `#C62828` | Accent 4 |
| `DARK_GRAY` | `#333333` | Body text |
| `BG_GRAY` | `#F2F2F2` | Background fill |

### Typography

| Level | Size | Font |
|---|---|---|
| Cover Title | 44px | Georgia |
| Section Title | 28px | Georgia |
| Action Title | 22px | Georgia |
| Body | 14px | Arial |
| Footnote | 9px | Arial |

---

## 📁 Project Structure

```
mck-html-design-skill/
├── SKILL.md                    # Core skill definition
├── README.md                   # 中文文档
├── README_EN.md                # English documentation (this file)
├── LICENSE                     # Apache 2.0
├── NOTICE                      # Attribution notice
├── mck_html/
│   ├── __init__.py             # Entry point + version
│   ├── engine.py               # 68 layout methods
│   ├── core.py                 # Low-level HTML generation
│   └── constants.py            # Colors, fonts, sizes
├── examples/
│   ├── minimal_example.py      # Minimal example
│   ├── full_test.py            # Full 68-method test
│   └── longevity_weekly.py     # Real-world: 20-page weekly
└── output/                     # Generated HTML output
```

---

## 🔄 Comparison with PPT Version

| Aspect | PPT Version ([MckEngine](https://github.com/likaku/Mck-ppt-design-skill)) | HTML Version (MckHtmlEngine) |
|---|---|---|
| Output | `.pptx` (PowerPoint) | `.html` (Single file) |
| Dependencies | python-pptx, lxml | **None** |
| Charts | BLOCK_ARC native shapes | SVG paths |
| Presentation | Open in PowerPoint | Browser + built-in JS |
| File size | 50KB-500KB | 20KB-100KB |
| API | Identical method signatures | Identical method signatures |

**Version numbers are kept in sync**: both projects release simultaneously with matching versions.

---

## 📋 Changelog

### v2.0.0 (2026-03-20) — Bug Fix + Real-world Validation + Version Sync

🐛 **Bug Fixes**

- **`process_chevron()` parameter format fix**: The `steps` parameter requires tuple format `(label, step_title, description)`. Documentation has been clarified. Previously, passing a plain string list caused `ValueError: not enough values to unpack`.

  ```python
  # ❌ Wrong
  steps=['Step 1', 'Step 2', 'Step 3']
  
  # ✅ Correct
  steps=[
      ('1', 'Step Title', 'Step description here'),
      ('2', 'Step Title', 'Step description here'),
  ]
  ```

🔬 **Real-world Validation**

- Added `examples/longevity_weekly.py`: A 20-page "Proactive Health × AI Intelligence Weekly" using 12 different layout patterns, validating complex CJK content rendering.

🔄 **Version Sync**

- Version bumped from v1.0.0 to v2.0.0, synced with [McKinsey PPT Design Skill](https://github.com/likaku/Mck-ppt-design-skill) v2.0.

### v1.0.0 (2026-03-19) — Initial Release

- 68 layout methods across 12 business presentation categories
- Pure Python, zero external dependencies
- SVG chart rendering (donut, pie, gauge, line charts)
- Built-in presentation mode (keyboard navigation + fullscreen)
- Self-contained HTML output, works in any browser
- API-compatible with MckEngine (PPT version)

---

## 💡 Why

The pain point of creating presentations isn't "can't do it" — it's "takes too long."

This Skill lets you generate professional presentations **in batch, automated, reproducible** with Python scripts, so you can focus on what truly matters — **the content itself**.

---

## 🤝 Contributing

If this Skill helped you, please **give it a ⭐ Star**!

Questions or suggestions? Feel free to [open an Issue](../../issues) or [submit a PR](../../pulls).

---

## 📄 License

[Apache License 2.0](LICENSE) © 2024-2026 [likaku](https://github.com/likaku)

Per Section 4(d) of Apache License 2.0, any derivative works or redistributions must include the attribution notice in the [NOTICE](NOTICE) file.
