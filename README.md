<p align="center">
  <h1 align="center">📊 McKinsey HTML Design Skill</h1>
  <p align="center">
    <strong>用 Python 一键生成麦肯锡风格 HTML 演示文稿——68 种布局，零依赖，开箱即用</strong>
  </p>

  <p align="center">

### 社区

<table>
<tr>
    <td align="center" width="50%" valign="top">
      <strong>微信交流群</strong><br/><br/>
      <img width="180" src="https://github.com/user-attachments/assets/d4eb704e-3825-4380-ac54-2fbbe4c993ce" alt="WeChat Group" />
    </td>
    <td align="center" width="50%" valign="top">
      <strong>Discord</strong><br/><br/>
      <a href="https://discord.gg/SaFybFAT">
        <img src="https://img.shields.io/badge/Discord-加入社区-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" />
      </a>
      <br/><br/>
      <span>点击上方按钮加入</span>
    </td>
  </tr>
</table>
    <em>68 种布局 · 12 大类 · 纯 Python · 单文件 HTML 输出</em>
  </p>
</p>

<p align="center">
  <a href="#-核心价值">核心价值</a> •
  <a href="#-68-种布局方法">68 种布局</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-changelog">更新日志</a> •
  <a href="./README_EN.md">English</a>
</p>

---

## 🔗 姊妹项目

| 项目 | 输出格式 | 链接 |
|-------|---------|------|
| **McKinsey PPT Design Skill** | `.pptx` (PowerPoint) | [🔗 GitHub](https://github.com/likaku/Mck-ppt-design-skill) |
| **McKinsey HTML Design Skill** | `.html` (浏览器) | 📍 你在这里 |

两个项目共享相同的设计体系和 API 签名，版本号保持同步。

---

## 🔥 核心价值

> **一句话**：你写 Python 调用方法，它输出一个自包含的专业 HTML 演示文稿——无需 PowerPoint，无需前端知识，浏览器打开即可演示。

### 它解决什么问题？

每个人都遇到过：

> 需要一份专业的演示文稿，但不想花时间纠结排版、配色、对齐…
>
> 或者需要**程序化批量生成**报告，但 PowerPoint 太重了…
>
> **68 种布局方法，一行代码一个幻灯片。**

### 三大差异化能力

| | 手动做 PPT | 这个 Skill |
|---|---|---|
| 🎨 **设计质量** | 取决于个人审美 | 麦肯锡级专业设计 |
| ⚡ **效率** | 每页 15-30 分钟 | 每页 1 行代码 |
| 🔄 **可复用** | 手动复制粘贴 | Python 脚本自动化 |

---

## 📊 68 种布局方法

12 大类覆盖所有常见商业演示场景：

| # | 类别 | 方法数 | 示例 |
|---|---|---|---|
| 1 | **结构** | 5 | `cover()`, `toc()`, `section_divider()`, `closing()`, `appendix_title()` |
| 2 | **数据** | 7 | `big_number()`, `two_stat()`, `three_stat()`, `data_table()`, `table_insight()` |
| 3 | **框架** | 4 | `matrix_2x2()`, `pyramid()`, `process_chevron()`, `temple()` |
| 4 | **对比** | 3 | `side_by_side()`, `before_after()`, `swot()` |
| 5 | **叙事** | 6 | `executive_summary()`, `key_takeaway()`, `quote()`, `four_column()` |
| 6 | **时间线** | 2 | `timeline()`, `vertical_steps()` |
| 7 | **团队 & 案例** | 3 | `meet_the_team()`, `case_study()`, `action_items()` |
| 8 | **图表** | 11 | `donut()`, `pie()`, `grouped_bar()`, `horizontal_bar()`, `gauge()`, `waterfall()` |
| 9 | **图片** | 7 | `content_right_image()`, `full_width_image()`, `three_images()` |
| 10 | **高级可视化** | 7 | `funnel()`, `cycle()`, `venn()`, `value_chain()`, `icon_grid()` |
| 11 | **仪表盘** | 8 | `kpi_tracker()`, `bubble()`, `risk_matrix()`, `dashboard_kpi_chart()` |
| 12 | **视觉叙事** | 5 | `decision_tree()`, `metric_comparison()`, `agenda()`, `two_col_image_grid()` |

---

## 🚀 快速开始

### 安装

**零依赖**——纯 Python 3，无需 pip install 任何包。

```bash
git clone https://github.com/likaku/mck-html-design-skill.git
```

### 最简示例

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

### 演示模式

生成的 HTML 内置演示功能：

| 快捷键 | 功能 |
|---|---|
| `←` `→` 方向键 | 翻页 |
| `F` | 全屏演示 |
| `Escape` | 退出全屏 |
| `Space` | 下一页 |

### 作为 AI Skill 使用

将仓库放入你的 AI IDE 的 Skills 目录：

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

然后对 AI 说：

> "帮我生成一个 HTML 演示文稿"

---

## 🎨 设计体系

### 颜色

| Token | Hex | 用途 |
|-------|-----|------|
| `NAVY` | `#051C2C` | 主标题、重点形状 |
| `ACCENT_BLUE` | `#006BA6` | 强调色 1 |
| `ACCENT_GREEN` | `#007A53` | 强调色 2 |
| `ACCENT_ORANGE` | `#D46A00` | 强调色 3 |
| `ACCENT_RED` | `#C62828` | 强调色 4 |
| `DARK_GRAY` | `#333333` | 正文 |
| `BG_GRAY` | `#F2F2F2` | 背景填充 |

### 字体

| 层级 | 大小 | 字体 |
|---|---|---|
| 封面标题 | 44px | Georgia |
| 章节标题 | 28px | Georgia |
| 内容标题 | 22px | Georgia |
| 正文 | 14px | Arial |
| 脚注 | 9px | Arial |

---

## 📁 项目结构

```
mck-html-design-skill/
├── SKILL.md                    # Skill 核心定义
├── README.md                   # 中文文档（本文件）
├── README_EN.md                # English documentation
├── LICENSE                     # Apache 2.0
├── NOTICE                      # 署名声明
├── mck_html/
│   ├── __init__.py             # 入口 + 版本号
│   ├── engine.py               # 68 种布局方法
│   ├── core.py                 # 底层 HTML 生成
│   └── constants.py            # 颜色、字体、尺寸
├── examples/
│   ├── minimal_example.py      # 最简示例
│   ├── full_test.py            # 68 方法全测试
│   └── longevity_weekly.py     # 实战：20页周报
└── output/                     # 生成的 HTML
```

---

## 🔄 与 PPT 版本对比

| 对比 | PPT 版 ([MckEngine](https://github.com/likaku/Mck-ppt-design-skill)) | HTML 版 (MckHtmlEngine) |
|---|---|---|
| 输出格式 | `.pptx` (PowerPoint) | `.html` (单文件) |
| 依赖 | python-pptx, lxml | **无** |
| 图表 | BLOCK_ARC 原生形状 | SVG 路径 |
| 演示 | PowerPoint 打开 | 浏览器 + 内置 JS |
| 文件大小 | 50KB-500KB | 20KB-100KB |
| API | 相同方法签名 | 相同方法签名 |

**版本号保持同步**：两个项目同时发布，版本号一致。

---

## 📋 Changelog

### v2.0.0 (2026-03-20) — Bug 修复 + 实战验证 + 版本同步

🐛 **Bug 修复**

- **`process_chevron()` 参数格式修复**：`steps` 参数要求三元组 `(label, step_title, description)` 格式，文档已明确。之前传入普通字符串列表会导致 `ValueError: not enough values to unpack` 错误。

  ```python
  # ❌ 错误用法
  steps=['Step 1', 'Step 2', 'Step 3']
  
  # ✅ 正确用法
  steps=[
      ('1', 'Step Title', 'Step description here'),
      ('2', 'Step Title', 'Step description here'),
  ]
  ```

🔬 **实战验证**

- 新增 `examples/longevity_weekly.py`：20 页「主动健康×AI 全景情报周报」，使用 12 种不同布局模式，验证复杂中文内容渲染。

🔄 **版本同步**

- 版本号从 v1.0.0 升级到 v2.0.0，与 [McKinsey PPT Design Skill](https://github.com/likaku/Mck-ppt-design-skill) v2.0 保持同步。

### v1.0.0 (2026-03-19) — 初始发布

- 68 种布局方法，覆盖 12 大类商业演示场景
- 纯 Python 实现，零外部依赖
- SVG 图表渲染（甜甜圈、饼图、仪表盘、折线图）
- 内置演示模式（键盘翻页 + 全屏）
- 自包含 HTML 输出，浏览器打开即用
- 与 MckEngine（PPT 版）API 完全兼容

---

## 💡 为什么做这个

说到底，做演示文稿这件事的痛点不是「不会做」，而是「太耗时间」。

这个 Skill 让你用 Python 脚本**批量、自动化、可复现**地生成专业演示文稿，把时间花在真正重要的事上——**内容本身**。

---

## 🤝 贡献

如果这个 Skill 帮到了你，请 **点个 ⭐ Star**！

有问题或建议？欢迎 [提 Issue](../../issues) 或 [发 PR](../../pulls)。

---

## 📄 License

[Apache License 2.0](LICENSE) © 2024-2026 [likaku](https://github.com/likaku)

根据 Apache License 2.0 第 4(d) 条，任何衍生作品或再分发必须包含 [NOTICE](NOTICE) 文件中的署名声明。
