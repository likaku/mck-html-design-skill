# MCK HTML Design — PPTX→HTML Replica Pipeline
# ═══════════════════════════════════════════════════════════════
#
# One-command conversion: PPTX → pixel-accurate HTML + interactive ECharts
#
# Pipeline:
#   PPTX → pptx_to_svg (OOXML精确解析) → svg_harness (规范化) → ECharts替换 → 单HTML
#
# Usage:
#   python scripts/pptx_to_html_pipeline.py <input.pptx> [-o output.html] [--slides 1-10]
#
# ═══════════════════════════════════════════════════════════════

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    pptx_to_html_pipeline.py                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: pptx_to_svg/          (200KB, 5640行)              │
│  ├── ooxml_loader.py           读取 OOXML zip               │
│  ├── shape_walker.py           递归解析 shape tree + group  │
│  ├── txbody_to_svg.py          文本渲染 (含继承链)           │
│  ├── color_resolver.py         主题色/tint/shade 解析       │
│  ├── fill_to_svg.py            填充 (solid/gradient/pattern)│
│  ├── ln_to_svg.py              线条/边框                    │
│  ├── prstgeom_to_svg.py        预置几何形状                  │
│  ├── pic_to_svg.py             图片提取/base64              │
│  ├── tbl_to_svg.py             表格渲染                     │
│  ├── slide_to_svg.py           主渲染逻辑                   │
│  └── converter.py              顶层协调器                   │
│                                                             │
│  Step 2: svg_harness.py                                     │
│  ├── 字体统一 (中文楷体/英文Georgia+Arial)                    │
│  ├── TopLine/BottomLine 保证                                │
│  ├── Footer (页码/source/logo) 一致性                       │
│  ├── Overflow clip-path 防文字溢出                           │
│  └── Body boundary 内容边界保护                             │
│                                                             │
│  Step 3: svg_chart_replacer.py                              │
│  ├── 提取 PPTX 图表数据 (类型/categories/series)            │
│  ├── SVG [chart] 占位符 → <foreignObject> + ECharts div     │
│  └── 生成 ECharts 初始化 JS                                 │
│                                                             │
│  Step 4: HTML Assembly                                      │
│  └── SVG slides + ECharts CDN + init JS → 单文件 HTML       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Harness 规则 (mck_layout_harness.yaml)

| 规则 | 值 | 说明 |
|------|-----|------|
| Canvas | 1280×720px | 16:9 |
| Left/Right margin | 58.2px | 内容安全区 |
| TopLine | y=124.1px | 标题区/内容区分界 |
| BottomLine | y=677.6px | 内容区/footer 分界 |
| 中文字体 | KaiTi, STKaiti, 楷体 | 所有中文 |
| 英文标题 | Georgia | majorLatin |
| 英文正文 | Arial | minorLatin |
| Footer source | (58.2, 682.6) | 左下角 |
| Footer 页码 | (1221.8, 692.6) | 右下角 |
| Footer logo | (1124.4, 695.1) | McKinsey & Company |

## 依赖

- python-pptx
- lxml (通常随 python-pptx 安装)
- 浏览器中需要网络加载 ECharts CDN (或离线内嵌)

## 文件清单

```
scripts/
├── pptx_to_html_pipeline.py    ← 顶层入口 (一键运行)
├── svg_harness.py              ← 规范化后处理
├── svg_chart_replacer.py       ← 图表 → ECharts
├── pptx_to_svg/                ← OOXML→SVG 引擎 (from ppt-master)
│   ├── __init__.py
│   ├── converter.py
│   ├── ooxml_loader.py
│   ├── shape_walker.py
│   ├── slide_to_svg.py
│   ├── txbody_to_svg.py
│   ├── color_resolver.py
│   ├── fill_to_svg.py
│   ├── ln_to_svg.py
│   ├── pic_to_svg.py
│   ├── prstgeom_to_svg.py
│   ├── tbl_to_svg.py
│   ├── custgeom_to_svg.py
│   ├── effect_to_svg.py
│   └── emu_units.py
├── ppt_to_md.py                ← PPTX→Markdown (内容提取)
├── pptx_to_html.py             ← 早期直接转换版本 (deprecated)
└── ...

templates/
└── mck_layout_harness.yaml     ← 版式规则配置
```
