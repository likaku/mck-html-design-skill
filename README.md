<p align="center">
  <h1 align="center">📊 McKinsey HTML Design Skill</h1>
  <p align="center">
    <strong>用 Python 一键生成麦肯锡风格 HTML 演示文稿——68 种布局，零依赖，开箱即用</strong><br/>
    <strong>Generate McKinsey-style HTML presentations with Python — 68 layouts, zero dependencies, ready to use</strong>
  </p>

  <p align="center">

### 社区 / Community

<table>
<tr>
    <td align="center" width="50%" valign="top">
      <strong>微信交流群</strong><br/><br/>
      <img width="180" src="https://github.com/user-attachments/assets/d4eb704e-3825-4380-ac54-2fbbe4c993ce" alt="WeChat Group" />
    </td>
    <td align="center" width="50%" valign="top">
      <strong>Discord</strong><br/><br/>
      <a href="https://discord.gg/SaFybFAT">
        <img src="https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" />
      </a>
      <br/><br/>
      <span>Click to join / 点击加入</span>
    </td>
  </tr>
</table>
    <em>68 layouts · 12 categories · Pure Python · Single-file HTML output</em>
  </p>
</p>

<p align="center">
  <a href="#-核心价值--core-value">核心价值</a> •
  <a href="#-68-种布局方法--68-layout-methods">68 种布局</a> •
  <a href="#-快速开始--quick-start">快速开始</a> •
  <a href="#-changelog--更新日志">更新日志</a>
</p>

---

## 🔥 核心价值 / Core Value

> **一句话 / In one sentence**：你写 Python 调用方法，它输出一个自包含的专业 HTML 演示文稿——无需 PowerPoint，无需前端知识，浏览器打开即可演示。
>
> Write Python method calls, get a self-contained professional HTML presentation — no PowerPoint, no frontend knowledge, open in any browser.

### 它解决什么问题？ / What problem does it solve?

每个人都遇到过：

> 需要一份专业的演示文稿，但不想花时间纠结排版、配色、对齐…
>
> 或者需要**程序化批量生成**报告，但 PowerPoint 太重了…
>
> **68 种布局方法，一行代码一个幻灯片。**

Everyone has been there:

> You need a professional presentation but don't want to fuss over layout, colors, alignment…
>
> Or you need to **programmatically generate** reports at scale, but PowerPoint is too heavy…
>
> **68 layout methods, one line of code per slide.**

### 三大差异化能力 / Three Key Differentiators

| | 手动做 PPT / Manual PPT | 这个 Skill / This Skill |
|---|---|---|
| 🎨 **设计质量** | 取决于个人审美 / Depends on personal taste | 麦肯锡级专业设计 / McKinsey-grade professional design |
| ⚡ **效率** | 每页 15-30 分钟 / 15-30 min per slide | 每页 1 行代码 / 1 line of code per slide |
| 🔄 **可复用** | 手动复制粘贴 / Copy-paste | Python 脚本自动化 / Python script automation |

---

## 📊 68 种布局方法 / 68 Layout Methods

12 大类覆盖所有常见商业演示场景：

12 categories covering all common business presentation scenarios:

| # | 类别 / Category | 方法数 / Methods | 示例 / Examples |
|---|---|---|---|
| 1 | **结构 / Structure** | 5 | `cover()`, `toc()`, `section_divider()`, `closing()`, `appendix_title()` |
| 2 | **数据 / Data** | 7 | `big_number()`, `two_stat()`, `three_stat()`, `data_table()`, `table_insight()` |
| 3 | **框架 / Framework** | 4 | `matrix_2x2()`, `pyramid()`, `process_chevron()`, `temple()` |
| 4 | **对比 / Comparison** | 3 | `side_by_side()`, `before_after()`, `swot()` |
| 5 | **叙事 / Narrative** | 6 | `executive_summary()`, `key_takeaway()`, `quote()`, `four_column()` |
| 6 | **时间线 / Timeline** | 2 | `timeline()`, `vertical_steps()` |
| 7 | **团队 & 案例 / Team & Case** | 3 | `meet_the_team()`, `case_study()`, `action_items()` |
| 8 | **图表 / Charts** | 11 | `donut()`, `pie()`, `grouped_bar()`, `horizontal_bar()`, `gauge()`, `waterfall()` |
| 9 | **图片 / Images** | 7 | `content_right_image()`, `full_width_image()`, `three_images()` |
| 10 | **高级可视化 / Advanced Viz** | 7 | `funnel()`, `cycle()`, `venn()`, `value_chain()`, `icon_grid()` |
| 11 | **仪表盘 / Dashboards** | 8 | `kpi_tracker()`, `bubble()`, `risk_matrix()`, `dashboard_kpi_chart()` |
| 12 | **视觉叙事 / Visual Storytelling** | 5 | `decision_tree()`, `metric_comparison()`, `agenda()`, `two_col_image_grid()` |

---

## 🚀 快速开始 / Quick Start

### 安装 / Installation

**零依赖**——纯 Python 3，无需 pip install 任何包。

**Zero dependencies** — pure Python 3, no pip install needed.

```bash
git clone https://github.com/likaku/mck-html-design-skill.git
```

### 最简示例 / Minimal Example

```python
import sys, os
sys.path.insert(0, '/path/to/mck-html-design-skill')

from mck_html import MckHtmlEngine
from mck_html.constants import *

eng = MckHtmlEngine(total_slides=5)

# 封面
eng.cover(title='Q1 2026 战略回顾', subtitle='董事会汇报', 
          author='战略部', date='2026年3月')

# 目录
eng.toc(items=[
    ('1', '市场概览', '当前竞争格局'),
    ('2', '财务分析', '收入与增长'),
    ('3', '下一步计划', '战略举措'),
])

# 大数字
eng.big_number(title='年度收入增长显著', number='¥2.8B', unit='年收入',
               description='同比增长23%，超出市场预期')

# 甜甜圈图
eng.donut(title='收入构成', segments=[
    (0.45, NAVY, '产品销售'),
    (0.30, ACCENT_BLUE, '服务收入'),
    (0.25, ACCENT_GREEN, '订阅收入'),
], center_label='100%', center_sub='总收入')

# 保存
eng.save('output/my_deck.html')
```

然后在浏览器中打开 `output/my_deck.html` 即可。

Open `output/my_deck.html` in any browser.

### 演示模式 / Presentation Mode

生成的 HTML 内置演示功能：

The generated HTML includes built-in presentation features:

| 快捷键 / Key | 功能 / Action |
|---|---|
| `←` `→` / Arrow keys | 翻页 / Navigate slides |
| `F` | 全屏演示 / Fullscreen mode |
| `Escape` | 退出全屏 / Exit fullscreen |
| `Space` | 下一页 / Next slide |

### 作为 AI Skill 使用 / Use as AI Skill

将仓库放入你的 AI IDE 的 Skills 目录：

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

然后对 AI 说 / Then tell the AI:

> "帮我生成一个 HTML 演示文稿 / Help me create an HTML presentation"

---

## 🎨 设计体系 / Design System

### 颜色 / Colors

| Token | Hex | 用途 / Usage |
|-------|-----|------|
| `NAVY` | `#051C2C` | 主标题、重点形状 / Primary headlines |
| `ACCENT_BLUE` | `#006BA6` | 强调色 1 / Accent 1 |
| `ACCENT_GREEN` | `#007A53` | 强调色 2 / Accent 2 |
| `ACCENT_ORANGE` | `#D46A00` | 强调色 3 / Accent 3 |
| `ACCENT_RED` | `#C62828` | 强调色 4 / Accent 4 |
| `DARK_GRAY` | `#333333` | 正文 / Body text |
| `BG_GRAY` | `#F2F2F2` | 背景填充 / Background |

### 字体 / Typography

| 层级 / Level | 大小 / Size | 字体 / Font |
|---|---|---|
| 封面标题 / Cover Title | 44px | Georgia |
| 章节标题 / Section Title | 28px | Georgia |
| 内容标题 / Action Title | 22px | Georgia |
| 正文 / Body | 14px | Arial |
| 脚注 / Footnote | 9px | Arial |

---

## 📁 项目结构 / Project Structure

```
mck-html-design-skill/
├── SKILL.md                    # Skill 核心定义 / Core skill definition
├── README.md                   # 本文件 / This file
├── LICENSE                     # Apache 2.0
├── NOTICE                      # 署名声明 / Attribution notice
├── mck_html/
│   ├── __init__.py             # 入口 + 版本号 / Entry + version
│   ├── engine.py               # 68 种布局方法 / 68 layout methods
│   ├── core.py                 # 底层 HTML 生成 / Low-level HTML generation
│   └── constants.py            # 颜色、字体、尺寸 / Colors, fonts, sizes
├── examples/
│   ├── minimal_example.py      # 最简示例 / Minimal example
│   ├── full_test.py            # 68 方法全测试 / Full 68-method test
│   └── longevity_weekly.py     # 实战：20页周报 / Real-world: 20-page weekly
└── output/                     # 生成的 HTML / Generated HTML output
```

---

## 🔗 与 PPT 版本的关系 / Relationship with PPT Version

本项目（`mck-html-design-skill`）是 [McKinsey Speech Design Skill](https://github.com/likaku/Mck-speech-design-skill)（PPT 版本）的 **HTML 姊妹项目**，两者共享相同的设计体系和 API 签名。

This project (`mck-html-design-skill`) is the **HTML sibling** of [McKinsey Speech Design Skill](https://github.com/likaku/Mck-speech-design-skill) (PPT version), sharing the same design system and API signatures.

| 对比 / Comparison | PPT 版 (MckEngine) | HTML 版 (MckHtmlEngine) |
|---|---|---|
| 输出格式 / Output | `.pptx` (PowerPoint) | `.html` (单文件 / Single file) |
| 依赖 / Dependencies | python-pptx, lxml | **无 / None** |
| 图表 / Charts | BLOCK_ARC 原生形状 / Native shapes | SVG 路径 / SVG paths |
| 演示 / Presentation | PowerPoint 打开 | 浏览器 + 内置 JS / Browser + built-in JS |
| 文件大小 / File size | 50KB-500KB | 20KB-100KB |
| API | 相同方法签名 / Identical signatures | 相同方法签名 / Identical signatures |

**版本号保持同步** / **Version numbers are kept in sync**：两个项目同时发布，版本号一致。

---

## 📋 Changelog / 更新日志

### v2.0.0 (2026-03-20) — Bug 修复 + 实战验证 + 版本同步

🐛 **Bug 修复 / Bug Fixes**

- **`process_chevron()` 参数格式修复**：`steps` 参数要求三元组 `(label, step_title, description)` 格式，文档已明确。之前传入普通字符串列表会导致 `ValueError: not enough values to unpack` 错误。
  
  Fixed `process_chevron()` `steps` parameter documentation: requires tuple format `(label, step_title, description)`. Passing plain string list previously caused `ValueError: not enough values to unpack`.

  ```python
  # ❌ 错误用法 / Wrong
  steps=['Step 1', 'Step 2', 'Step 3']
  
  # ✅ 正确用法 / Correct
  steps=[
      ('1', 'Step Title', 'Step description here'),
      ('2', 'Step Title', 'Step description here'),
  ]
  ```

🔬 **实战验证 / Real-world Validation**

- 新增 `examples/longevity_weekly.py`：20 页「主动健康×AI 全景情报周报」，使用 12 种不同布局模式，验证复杂中文内容渲染。
  
  Added `examples/longevity_weekly.py`: 20-page "Proactive Health × AI Intelligence Weekly", using 12 different layout patterns, validating complex CJK content rendering.

🔄 **版本同步 / Version Sync**

- 版本号从 v1.0.0 升级到 v2.0.0，与 [McKinsey Speech Design Skill](https://github.com/likaku/Mck-speech-design-skill) v2.0 保持同步。
  
  Version bumped from v1.0.0 to v2.0.0, synced with [McKinsey Speech Design Skill](https://github.com/likaku/Mck-speech-design-skill) v2.0.

### v1.0.0 (2026-03-19) — 初始发布 / Initial Release

- 68 种布局方法，覆盖 12 大类商业演示场景
- 纯 Python 实现，零外部依赖
- SVG 图表渲染（甜甜圈、饼图、仪表盘、折线图）
- 内置演示模式（键盘翻页 + 全屏）
- 自包含 HTML 输出，浏览器打开即用
- 与 MckEngine（PPT 版）API 完全兼容

---

- 68 layout methods across 12 business presentation categories
- Pure Python, zero external dependencies
- SVG chart rendering (donut, pie, gauge, line charts)
- Built-in presentation mode (keyboard navigation + fullscreen)
- Self-contained HTML output, works in any browser
- API-compatible with MckEngine (PPT version)

---

## 💡 为什么做这个 / Why

说到底，做演示文稿这件事的痛点不是「不会做」，而是「太耗时间」。

The pain point of creating presentations isn't "can't do it" — it's "takes too long."

这个 Skill 让你用 Python 脚本**批量、自动化、可复现**地生成专业演示文稿，把时间花在真正重要的事上——**内容本身**。

This Skill lets you generate professional presentations **in batch, automated, reproducible** with Python scripts, so you can focus on what truly matters — **the content itself**.

---

## 🤝 Contributing / 贡献

如果这个 Skill 帮到了你，请 **点个 ⭐ Star**！

If this Skill helped you, please **give it a ⭐ Star**!

有问题或建议？欢迎 [提 Issue](../../issues) 或 [发 PR](../../pulls)。

Questions or suggestions? Feel free to [open an Issue](../../issues) or [submit a PR](../../pulls).

---

## 📄 License

[Apache License 2.0](LICENSE) © 2024-2026 [likaku](https://github.com/likaku)

根据 Apache License 2.0 第 4(d) 条，任何衍生作品或再分发必须包含 [NOTICE](NOTICE) 文件中的署名声明。

Per Section 4(d) of Apache License 2.0, any derivative works or redistributions must include the attribution notice in the [NOTICE](NOTICE) file.
