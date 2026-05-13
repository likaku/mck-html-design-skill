"""ECharts Chart Module for MckHtmlEngine.

Replaces the 11 SVG-drawn chart methods with interactive Apache ECharts 5.x
equivalents, plus 3 new chart types not available in the original SVG engine.

Color palette: Office Blue Theme Accent 1-6 (derived from Kaku's design token
standard, validated against echarts-mck-demo.html on 2026-05-09).

Usage (from engine.py or any script):
    from mck_html.echarts_charts import EChartsMixin
    # MckHtmlEngine already inherits this mixin if echarts is enabled.
    eng = MckHtmlEngine(total_slides=12, use_echarts=True)
    eng.echart_grouped_bar(...)
    eng.echart_line_chart(...)

Design principles
-----------------
1. All chart containers use width:100% / height defined per chart type.
2. ECharts is injected once per HTML file via _ensure_echarts_injected().
3. Office Accent palette is the DEFAULT; callers can override per series.
4. Font stacks match FONT_STACK_HEADER / FONT_STACK_BODY from constants.py.
5. Tooltip, legend, axis labels all receive the Mck font family.
6. Negative values always use ACCENT_RED (#C62828); totals use MCK_DARK.
"""

import json
import html as _html_mod
from .constants import (
    FONT_STACK_BODY, FONT_STACK_HEADER,
    NAVY, WHITE, DARK_GRAY, MED_GRAY, LINE_GRAY, BG_GRAY,
    ACCENT_RED,
    BODY_SIZE, SMALL_SIZE, FOOTNOTE_SIZE,
)

# ═══════════════════════════════════════════
# McKINSEY ORIGINAL CHART PALETTE
# Extracted from 4 McKinsey reference slides (2026-05-09 analysis)
#
# PRIMARY DARK  (#172B4D): Deep navy-black. Used for base/2019/Increase bars.
#   NOT pure black (#000), NOT Office #1F3864. Saturated cold navy.
#
# PRIMARY LIGHT (#00AEEF): Vivid cyan-blue. Used for highlight/2020/Life/Total.
#   Cooler than Office #00B0F0. High saturation, clean sky-cyan.
#
# SECONDARY MID (#0073B6): Cobalt blue. 3rd series in line/scatter charts.
#
# DESIGN RULES from McKinsey slides:
#   - Most charts use ONLY 2 fills: dark + light
#   - NO rounded bar corners (sharp rectangles)
#   - Bar labels: same color as bar (above) or white (inside dark bars)
#   - NO gradients on bars, NO drop shadows
# ═══════════════════════════════════════════
MCK_DARK   = '#172B4D'   # Primary dark  — deep navy-black (base/2019/increase)
MCK_LIGHT  = '#00AEEF'   # Primary light — vivid cyan-blue (highlight/2020/total)
MCK_MID    = '#0073B6'   # Secondary     — cobalt blue (3rd series)
MCK_PALE   = '#9DC3E6'   # Tertiary      — pale blue (4th series)
MCK_VLIGHT = '#C9E5F5'   # Very light    — near-white blue (donut inner ring)

# Legacy aliases (kept for backward compatibility with scripts using ACCENT_1-6)
ACCENT_1 = MCK_DARK
ACCENT_2 = MCK_LIGHT
ACCENT_3 = MCK_MID
ACCENT_4 = MCK_PALE
ACCENT_5 = '#BDD7EE'
ACCENT_6 = '#E8F4FC'

# Ordered palette for automatic series color assignment
CHART_PALETTE = [MCK_DARK, MCK_LIGHT, MCK_MID, MCK_PALE, MCK_VLIGHT, '#E8F4FC']

# CDN URL — pinned version for reproducibility
ECHARTS_CDN = 'https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js'

# Google Fonts — Noto Serif SC (Chinese serif, matches KaiTi fallback chain)
NOTO_SERIF_SC_CSS = (
    "https://fonts.googleapis.com/css2?"
    "family=Noto+Serif+SC:wght@400;700&display=swap"
)


def _esc(text):
    return _html_mod.escape(str(text))


def _json(obj):
    """Compact JSON with no extra whitespace for embedding in HTML."""
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))


def _font_body():
    return FONT_STACK_BODY


def _font_header():
    return FONT_STACK_HEADER


# ═══════════════════════════════════════════
# SHARED ECHARTS OPTION FRAGMENTS
# ═══════════════════════════════════════════

def _base_text_style():
    return {
        'fontFamily': _font_body(),
        'color': DARK_GRAY,
        'fontSize': BODY_SIZE,
    }


def _tooltip():
    return {
        'backgroundColor': WHITE,
        'borderColor': LINE_GRAY,
        'borderWidth': 1,
        'textStyle': {
            'color': DARK_GRAY,
            'fontSize': SMALL_SIZE,
            'fontFamily': _font_body(),
        },
        'extraCssText': (
            'box-shadow:0 4px 12px rgba(0,0,0,0.12);border-radius:2px;'
        ),
    }


def _legend():
    return {
        'bottom': 4,
        'textStyle': {
            'color': MED_GRAY,
            'fontSize': SMALL_SIZE,
            'fontFamily': _font_body(),
        },
        'itemWidth': 14,
        'itemHeight': 10,
    }


def _axis_x(data):
    return {
        'type': 'category',
        'data': data,
        'axisLine': {'lineStyle': {'color': LINE_GRAY}},
        'axisTick': {'show': False},
        'axisLabel': {
            'color': MED_GRAY,
            'fontSize': SMALL_SIZE,
            'fontFamily': _font_body(),
        },
    }


def _axis_y(fmt=''):
    return {
        'type': 'value',
        'axisLabel': {
            'formatter': fmt,
            'color': MED_GRAY,
            'fontSize': SMALL_SIZE,
            'fontFamily': _font_body(),
        },
        'axisLine': {'show': False},
        'axisTick': {'show': False},
        'splitLine': {'lineStyle': {'color': BG_GRAY}},
    }


def _grid(left='3%', right='4%', bottom='14%', top='8%'):
    return {
        'left': left, 'right': right,
        'bottom': bottom, 'top': top,
        'containLabel': True,
    }


# ═══════════════════════════════════════════
# SLIDE WRAPPER HELPER
# ═══════════════════════════════════════════

def _chart_slide(chart_id, option_dict, height_px, title, source, summary,
                 extra_html_before='', extra_html_after=''):
    """
    Build the HTML for one ECharts chart wrapped in McKinsey slide chrome.

    Returns:
        (slide_body_html: str, init_script: str)
        slide_body_html  — goes inside the <slide> div
        init_script      — <script> block to run after page load
    """
    option_json = _json(option_dict)

    slide_body = f"""
{extra_html_before}
<div id="{chart_id}" style="width:100%;height:{height_px}px;"></div>
{extra_html_after}
"""

    init_script = f"""
(function(){{
  var el = document.getElementById('{chart_id}');
  if (!el) return;
  var c = echarts.init(el);
  c.setOption({option_json});
  window.addEventListener('resize', function(){{ c.resize(); }});
}})();
"""
    return slide_body, init_script


# ═══════════════════════════════════════════
# ECHARTS MIXIN
# Attach to MckHtmlEngine via multiple inheritance.
# ═══════════════════════════════════════════

class EChartsMixin:
    """
    Drop-in mixin for MckHtmlEngine that adds ECharts-powered chart methods.

    Each method mirrors the signature of its SVG counterpart where possible,
    so existing presentation scripts can swap `eng.donut(...)` for
    `eng.echart_donut(...)` with minimal changes.

    New chart types with no SVG equivalent are also included:
    - echart_rose()       — Nightingale/rose chart
    - echart_radar()      — Radar/spider chart
    - echart_nested_donut() — Dual-ring donut

    ECHARTS INJECTION
    -----------------
    The first call to any echart_* method automatically injects the ECharts
    CDN <script> tag and Google Fonts <link> into the final HTML.
    This is handled by _ensure_echarts_injected() and _flush_echarts_scripts().
    """

    _echarts_injected: bool = False
    _echarts_scripts: list  # accumulates per-chart init scripts

    def _ensure_echarts_injected(self):
        """Mark that ECharts CDN must be included in the final HTML output."""
        if not hasattr(self, '_echarts_injected'):
            self._echarts_injected = False
        if not hasattr(self, '_echarts_scripts'):
            self._echarts_scripts = []
        self._echarts_injected = True

    def _push_echart_script(self, script: str):
        if not hasattr(self, '_echarts_scripts'):
            self._echarts_scripts = []
        self._echarts_scripts.append(script)

    def _next_chart_id(self):
        return f'ec_{self._page}_{len(getattr(self, "_echarts_scripts", []))}'

    # ── Helpers shared across chart methods ──────────────────

    def _ec_slide(self, content_html, title, source, summary, chart_id,
                  option, height_px=360):
        """Create one full slide with ECharts chart embedded."""
        self._ensure_echarts_injected()
        _, init_script = _chart_slide(chart_id, option, height_px,
                                      title, source, summary)
        self._push_echart_script(init_script)
        return content_html

    # ══════════════════════════════════════════════════════════
    # CHART METHODS
    # ══════════════════════════════════════════════════════════

    def echart_grouped_bar(self, title, categories, series_names, data,
                           y_fmt='{c}', summary='', source='', height=340):
        """
        Grouped vertical bar chart.

        Parameters
        ----------
        title : str
        categories : list[str]   — x-axis labels
        series_names : list[str] — legend labels, one per series
        data : list[list[num]]   — data[i] = values for series_names[i]
        y_fmt : str              — ECharts label formatter string (default '{c}')
        summary : str            — bottom insight text
        source : str
        height : int             — chart height in px
        """
        p = self._ns()
        cid = f'ec_gbar_{p}'
        series = []
        for i, (name, vals) in enumerate(zip(series_names, data)):
            color = CHART_PALETTE[i % len(CHART_PALETTE)]
            series.append({
                'name': name,
                'type': 'bar',
                'barGap': '10%',
                'barMaxWidth': 56,
                'data': vals,
                'itemStyle': {'color': color, 'borderRadius': [2, 2, 0, 0]},
                'label': {
                    'show': True, 'position': 'top',
                    'formatter': y_fmt,
                    'fontSize': SMALL_SIZE,
                    'color': color,
                    'fontFamily': _font_body(),
                },
            })
        option = {
            'animation': True,
            'animationDuration': 700,
            'textStyle': _base_text_style(),
            'grid': _grid(),
            'tooltip': {**_tooltip(), 'trigger': 'axis',
                        'axisPointer': {'type': 'shadow'}},
            'legend': _legend(),
            'xAxis': _axis_x(categories),
            'yAxis': _axis_y(),
            'series': series,
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    def echart_horizontal_bar(self, title, items, summary='', source='',
                               height=320):
        """
        Horizontal bar chart.

        Parameters
        ----------
        items : list[tuple(label, value, color?)]
            color is optional; if omitted, auto-assigned from CHART_PALETTE.
        """
        p = self._ns()
        cid = f'ec_hbar_{p}'
        labels = [_esc(it[0]) for it in items]
        vals = []
        for i, it in enumerate(items):
            color = it[2] if len(it) > 2 else CHART_PALETTE[i % len(CHART_PALETTE)]
            vals.append({'value': it[1], 'itemStyle': {
                'color': color, 'borderRadius': [0, 2, 2, 0]}})
        option = {
            'animation': True,
            'animationDuration': 700,
            'textStyle': _base_text_style(),
            'grid': _grid(left='5%', right='10%', bottom='5%', top='3%'),
            'tooltip': {**_tooltip(), 'trigger': 'axis'},
            'xAxis': {
                'type': 'value',
                'axisLabel': {
                    'color': MED_GRAY, 'fontSize': SMALL_SIZE,
                    'fontFamily': _font_body(),
                },
                'axisLine': {'show': False},
                'axisTick': {'show': False},
                'splitLine': {'lineStyle': {'color': BG_GRAY}},
            },
            'yAxis': {
                'type': 'category', 'data': labels,
                'axisLine': {'show': False},
                'axisTick': {'show': False},
                'axisLabel': {
                    'color': DARK_GRAY, 'fontSize': SMALL_SIZE,
                    'fontFamily': _font_body(),
                },
            },
            'series': [{
                'type': 'bar', 'data': vals, 'barMaxWidth': 32,
                'label': {
                    'show': True, 'position': 'right', 'formatter': '{c}',
                    'fontSize': SMALL_SIZE, 'color': MED_GRAY,
                    'fontFamily': _font_body(),
                },
            }],
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    def echart_stacked_bar(self, title, periods, series_names, data,
                            summary='', source='', height=320):
        """100% stacked bar chart."""
        p = self._ns()
        cid = f'ec_sbar_{p}'
        series = []
        for i, (name, vals) in enumerate(zip(series_names, data)):
            color = CHART_PALETTE[i % len(CHART_PALETTE)]
            s = {
                'name': name, 'type': 'bar', 'stack': 'total',
                'barMaxWidth': 64, 'data': vals,
                'itemStyle': {'color': color},
            }
            if i == len(series_names) - 1:
                s['label'] = {
                    'show': True, 'position': 'inside',
                    'formatter': '{c}%', 'fontSize': SMALL_SIZE,
                    'color': WHITE, 'fontFamily': _font_body(),
                }
            series.append(s)
        option = {
            'animation': True, 'animationDuration': 700,
            'textStyle': _base_text_style(),
            'grid': _grid(),
            'tooltip': {**_tooltip(), 'trigger': 'axis',
                        'axisPointer': {'type': 'shadow'}},
            'legend': _legend(),
            'xAxis': _axis_x(periods),
            'yAxis': {**_axis_y('{value}%'), 'max': 100},
            'series': series,
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    def echart_line_chart(self, title, x_labels, series_names, data,
                           smooth=True, show_area=True,
                           summary='', source='', height=340):
        """Multi-series line chart with optional area fill."""
        p = self._ns()
        cid = f'ec_line_{p}'
        series = []
        for i, (name, vals) in enumerate(zip(series_names, data)):
            color = CHART_PALETTE[i % len(CHART_PALETTE)]
            s = {
                'name': name, 'type': 'line', 'smooth': smooth,
                'data': vals,
                'lineStyle': {'color': color, 'width': 2.5},
                'itemStyle': {'color': color},
                'symbolSize': 6,
            }
            if show_area and i == 0:
                import re
                r, g, b = (
                    int(color[1:3], 16),
                    int(color[3:5], 16),
                    int(color[5:7], 16),
                )
                s['areaStyle'] = {'color': {
                    'type': 'linear', 'x': 0, 'y': 0, 'x2': 0, 'y2': 1,
                    'colorStops': [
                        {'offset': 0, 'color': f'rgba({r},{g},{b},0.18)'},
                        {'offset': 1, 'color': f'rgba({r},{g},{b},0)'},
                    ],
                }}
            series.append(s)
        option = {
            'animation': True, 'animationDuration': 700,
            'textStyle': _base_text_style(),
            'grid': _grid(),
            'tooltip': {**_tooltip(), 'trigger': 'axis'},
            'legend': _legend(),
            'xAxis': {**_axis_x(x_labels), 'boundaryGap': False},
            'yAxis': _axis_y(),
            'series': series,
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    def echart_donut(self, title, segments, center_label='', center_sub='',
                     summary='', source='', height=320):
        """
        Donut (ring) chart.

        Parameters
        ----------
        segments : list[tuple(value, color?, label)]
            color is optional. If omitted, uses CHART_PALETTE in order.
        """
        p = self._ns()
        cid = f'ec_donut_{p}'
        pie_data = []
        for i, seg in enumerate(segments):
            if len(seg) == 3:
                val, color, label = seg
            else:
                val, label = seg[0], seg[-1]
                color = CHART_PALETTE[i % len(CHART_PALETTE)]
            pie_data.append({
                'value': val, 'name': _esc(str(label)),
                'itemStyle': {'color': color},
            })
        option = {
            'animation': True, 'animationDuration': 700,
            'textStyle': _base_text_style(),
            'tooltip': {**_tooltip(), 'trigger': 'item'},
            'legend': _legend(),
            'series': [{
                'type': 'pie',
                'radius': ['40%', '70%'],
                'center': ['50%', '48%'],
                'avoidLabelOverlap': False,
                'label': {
                    'show': True,
                    'formatter': '{b}\n{d}%',
                    'fontSize': SMALL_SIZE,
                    'fontFamily': _font_body(),
                    'color': DARK_GRAY,
                },
                'labelLine': {'lineStyle': {'color': LINE_GRAY}},
                'emphasis': {
                    'label': {'show': True, 'fontSize': BODY_SIZE,
                              'fontWeight': 'bold'},
                    'itemStyle': {'shadowBlur': 12,
                                  'shadowColor': 'rgba(0,0,0,0.15)'},
                },
                'data': pie_data,
            }],
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    def echart_waterfall(self, title, items, summary='', source='', height=380):
        """
        Waterfall bridge chart.

        Parameters
        ----------
        items : list[tuple(label, value, is_total?)]
            is_total defaults to False. First and last items are typically total.
        """
        p = self._ns()
        cid = f'ec_wf_{p}'
        labels = [_esc(str(it[0])) for it in items]
        values = [it[1] for it in items]
        is_total = [len(it) > 2 and it[2] for it in items]

        bases = [0]
        run = values[0]
        for i in range(1, len(values) - 1):
            bases.append(run if values[i] >= 0 else run + values[i])
            run += values[i]
        bases.append(0)

        colors = [
            MCK_DARK if is_total[i] else (MCK_MID if values[i] >= 0 else ACCENT_RED)
            for i in range(len(values))
        ]

        option = {
            'animation': True, 'animationDuration': 700,
            'textStyle': _base_text_style(),
            'grid': _grid(bottom='16%'),
            'tooltip': {**_tooltip(), 'trigger': 'axis',
                        'axisPointer': {'type': 'shadow'}},
            'xAxis': {**_axis_x(labels),
                      'axisLabel': {
                          'color': DARK_GRAY, 'fontSize': SMALL_SIZE,
                          'fontFamily': _font_body(), 'interval': 0,
                      }},
            'yAxis': _axis_y(),
            'series': [
                {'name': '_base', 'type': 'bar', 'stack': 'wf',
                 'data': bases,
                 'itemStyle': {'color': 'transparent'}, 'silent': True},
                {'name': '值', 'type': 'bar', 'stack': 'wf',
                 'barMaxWidth': 64,
                 'data': [
                     {'value': abs(v),
                      'itemStyle': {'color': colors[i],
                                    'borderRadius': [2, 2, 0, 0]}}
                     for i, v in enumerate(values)
                 ],
                 'label': {
                     'show': True, 'position': 'top',
                     'fontSize': SMALL_SIZE, 'fontFamily': _font_body(),
                     'color': DARK_GRAY,
                 }},
            ],
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    def echart_bubble(self, title, bubbles, x_label='', y_label='',
                      summary='', source='', height=400):
        """
        Bubble scatter chart.

        Parameters
        ----------
        bubbles : list[dict]  each dict: {name, x, y, size, color?}
        """
        p = self._ns()
        cid = f'ec_bubble_{p}'
        series = []
        for i, b in enumerate(bubbles):
            color = b.get('color', CHART_PALETTE[i % len(CHART_PALETTE)])
            series.append({
                'type': 'scatter',
                'name': _esc(b['name']),
                'data': [[b['x'], b['y'], b['size']]],
                'symbolSize': '(function(v){return Math.sqrt(v[2])*4.8})',
                'itemStyle': {'color': color, 'opacity': 0.85},
                'label': {
                    'show': True, 'formatter': _esc(b['name']),
                    'position': 'right',
                    'fontSize': SMALL_SIZE, 'fontFamily': _font_body(),
                    'color': DARK_GRAY,
                },
                'emphasis': {
                    'itemStyle': {'opacity': 1, 'shadowBlur': 10,
                                  'shadowColor': 'rgba(0,0,0,0.2)'},
                },
            })
        option = {
            'animation': True, 'animationDuration': 700,
            'textStyle': _base_text_style(),
            'grid': _grid(),
            'tooltip': {**_tooltip(), 'trigger': 'item'},
            'xAxis': {
                'type': 'value',
                'name': _esc(x_label), 'nameLocation': 'end',
                'nameTextStyle': {'color': MED_GRAY, 'fontSize': SMALL_SIZE,
                                  'fontFamily': _font_body()},
                'axisLabel': {'color': MED_GRAY, 'fontSize': SMALL_SIZE},
                'axisLine': {'lineStyle': {'color': LINE_GRAY}},
                'axisTick': {'show': False},
                'splitLine': {'lineStyle': {'color': BG_GRAY}},
            },
            'yAxis': {
                'type': 'value',
                'name': _esc(y_label), 'nameLocation': 'end',
                'nameTextStyle': {'color': MED_GRAY, 'fontSize': SMALL_SIZE,
                                  'fontFamily': _font_body()},
                'axisLabel': {'color': MED_GRAY, 'fontSize': SMALL_SIZE},
                'axisLine': {'show': False},
                'axisTick': {'show': False},
                'splitLine': {'lineStyle': {'color': BG_GRAY}},
            },
            'series': series,
        }
        # NOTE: symbolSize function cannot be JSON-serialized normally.
        # We post-process the JSON to replace the string with a real function.
        option_json = _json(option).replace(
            '"(function(v){return Math.sqrt(v[2])*4.8})"',
            'function(v){return Math.sqrt(v[2])*4.8}'
        )

        self._ensure_echarts_injected()
        cid_safe = _esc(cid)
        init_script = f"""
(function(){{
  var el = document.getElementById('{cid_safe}');
  if (!el) return;
  var c = echarts.init(el);
  c.setOption({option_json});
  window.addEventListener('resize', function(){{ c.resize(); }});
}})();
"""
        self._push_echart_script(init_script)
        # Build slide using engine's internal helpers
        from .core import make_slide, add_action_title, add_source, add_page_number
        from .constants import CONTENT_TOP, LM, CW
        parts = []
        parts.append(add_action_title(title))
        if summary:
            parts.append(self._summary_bar(summary))
        parts.append(
            f'<div style="position:absolute;left:{LM}px;top:{CONTENT_TOP}px;'
            f'width:{CW}px;height:{height}px;">'
            f'<div id="{cid}" style="width:100%;height:100%;"></div></div>'
        )
        if source:
            parts.append(add_source(source))
        parts.append(add_page_number(p, getattr(self, 'total', 30)))
        self._add_slide(make_slide('\n'.join(parts)))
        return self

    def echart_gauge(self, title, score, max_val=100,
                     summary='', source='', height=280):
        """Semicircle gauge chart."""
        p = self._ns()
        cid = f'ec_gauge_{p}'
        option = {
            'animation': True, 'animationDuration': 700,
            'textStyle': _base_text_style(),
            'series': [{
                'type': 'gauge',
                'startAngle': 200, 'endAngle': -20,
                'min': 0, 'max': max_val,
                'pointer': {
                    'icon': 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                    'length': '55%', 'width': 8,
                    'offsetCenter': [0, '5%'],
                    'itemStyle': {'color': NAVY},
                },
                'progress': {
                    'show': True, 'roundCap': True, 'width': 18,
                    'itemStyle': {'color': {
                        'type': 'linear', 'x': 0, 'y': 0, 'x2': 1, 'y2': 0,
                        'colorStops': [
                            {'offset': 0, 'color': MCK_DARK},
                            {'offset': 1, 'color': MCK_LIGHT},
                        ],
                    }},
                },
                'axisLine': {'lineStyle': {'width': 18, 'color': [[1, BG_GRAY]]}},
                'axisTick': {'show': False},
                'splitLine': {'length': 10, 'lineStyle': {'width': 2, 'color': '#999'}},
                'axisLabel': {
                    'distance': -40, 'color': MED_GRAY,
                    'fontSize': SMALL_SIZE, 'fontFamily': _font_body(),
                },
                'anchor': {
                    'show': True, 'showAbove': True, 'size': 18,
                    'itemStyle': {'borderWidth': 8, 'borderColor': NAVY},
                },
                'title': {
                    'show': True, 'offsetCenter': [0, '75%'],
                    'fontSize': BODY_SIZE,
                    'fontFamily': _font_header(),
                    'color': MED_GRAY,
                },
                'detail': {
                    'valueAnimation': True,
                    'fontSize': 38,
                    'fontFamily': _font_header(),
                    'offsetCenter': [0, '38%'],
                    'color': NAVY,
                    'formatter': '{value}',
                },
                'data': [{'value': score, 'name': title}],
            }],
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    def echart_radar(self, title, indicators, series_data,
                     summary='', source='', height=320):
        """
        Radar / spider chart. NEW — no SVG equivalent.

        Parameters
        ----------
        indicators : list[dict]  each: {'name': str, 'max': int}
        series_data : list[dict] each: {'name': str, 'data': list[num],
                                        'color': str (optional)}
        """
        p = self._ns()
        cid = f'ec_radar_{p}'
        series = []
        for i, sd in enumerate(series_data):
            color = sd.get('color', CHART_PALETTE[i % len(CHART_PALETTE)])
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            series.append({
                'type': 'radar', 'name': _esc(sd['name']),
                'data': [{'value': sd['data'], 'name': _esc(sd['name'])}],
                'lineStyle': {'color': color, 'width': 2},
                'itemStyle': {'color': color},
                'areaStyle': {'color': f'rgba({r},{g},{b},0.12)'},
            })
        option = {
            'animation': True, 'animationDuration': 700,
            'textStyle': _base_text_style(),
            'tooltip': {**_tooltip(), 'trigger': 'item'},
            'legend': _legend(),
            'radar': {
                'indicator': [
                    {'name': _esc(ind['name']), 'max': ind['max']}
                    for ind in indicators
                ],
                'radius': '62%', 'center': ['50%', '52%'],
                'axisName': {
                    'color': DARK_GRAY, 'fontSize': SMALL_SIZE,
                    'fontFamily': _font_body(),
                },
                'splitLine': {'lineStyle': {'color': [LINE_GRAY]}},
                'splitArea': {'show': False},
            },
            'series': series,
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    def echart_rose(self, title, items, summary='', source='', height=320):
        """
        Nightingale / rose chart. NEW — no SVG equivalent.

        Parameters
        ----------
        items : list[tuple(value, label, color?)]
        """
        p = self._ns()
        cid = f'ec_rose_{p}'
        pie_data = []
        for i, it in enumerate(items):
            val, label = it[0], it[1]
            color = it[2] if len(it) > 2 else CHART_PALETTE[i % len(CHART_PALETTE)]
            pie_data.append({
                'value': val, 'name': _esc(str(label)),
                'itemStyle': {'color': color},
            })
        option = {
            'animation': True, 'animationDuration': 700,
            'textStyle': _base_text_style(),
            'tooltip': {**_tooltip(), 'trigger': 'item'},
            'series': [{
                'type': 'pie',
                'radius': ['15%', '70%'],
                'center': ['50%', '50%'],
                'roseType': 'area',
                'itemStyle': {'borderRadius': 4},
                'label': {
                    'show': True, 'fontSize': SMALL_SIZE,
                    'fontFamily': _font_body(), 'color': DARK_GRAY,
                },
                'data': pie_data,
            }],
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    def echart_nested_donut(self, title, outer_data, inner_data,
                             summary='', source='', height=360):
        """
        Nested dual-ring donut. NEW — no SVG equivalent.

        Parameters
        ----------
        outer_data : list[tuple(value, label, color?)]
        inner_data : list[tuple(value, label, color?)]
        """
        p = self._ns()
        cid = f'ec_ndonut_{p}'

        def _build_pie_data(data, palette_offset=0):
            out = []
            for i, it in enumerate(data):
                val, label = it[0], it[1]
                color = it[2] if len(it) > 2 \
                    else CHART_PALETTE[(i + palette_offset) % len(CHART_PALETTE)]
                out.append({'value': val, 'name': _esc(str(label)),
                            'itemStyle': {'color': color}})
            return out

        option = {
            'animation': True, 'animationDuration': 700,
            'textStyle': _base_text_style(),
            'tooltip': {**_tooltip(), 'trigger': 'item'},
            'legend': _legend(),
            'series': [
                {'name': '外环', 'type': 'pie',
                 'radius': ['52%', '72%'], 'center': ['50%', '48%'],
                 'label': {'show': True, 'formatter': '{b}\n{d}%',
                            'fontSize': SMALL_SIZE, 'fontFamily': _font_body()},
                 'labelLine': {'lineStyle': {'color': LINE_GRAY}},
                 'data': _build_pie_data(outer_data)},
                {'name': '内环', 'type': 'pie',
                 'radius': ['22%', '44%'], 'center': ['50%', '48%'],
                 'label': {'show': False},
                 'emphasis': {'label': {'show': True, 'fontSize': BODY_SIZE,
                                         'fontFamily': _font_body()}},
                 'data': _build_pie_data(inner_data, palette_offset=1)},
            ],
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    def echart_pareto(self, title, items, summary='', source='', height=340):
        """
        Pareto chart (descending bars + cumulative % line).

        Parameters
        ----------
        items : list[tuple(label, value)]  — sorted descending by value preferred
        """
        p = self._ns()
        cid = f'ec_pareto_{p}'
        labels = [_esc(str(it[0])) for it in items]
        counts = [it[1] for it in items]
        total = sum(counts) or 1
        cum, cum_pcts = 0, []
        for v in counts:
            cum += v
            cum_pcts.append(round(cum / total * 100, 1))

        bar_data = [
            {'value': v, 'itemStyle': {
                'color': MCK_MID if i < max(1, len(counts) // 3)
                else (ACCENT_4 if i < len(counts) * 2 // 3 else ACCENT_6),
                'borderRadius': [2, 2, 0, 0],
            }}
            for i, v in enumerate(counts)
        ]

        option = {
            'animation': True, 'animationDuration': 700,
            'textStyle': _base_text_style(),
            'grid': _grid(bottom='16%'),
            'tooltip': {**_tooltip(), 'trigger': 'axis',
                        'axisPointer': {'type': 'cross'}},
            'legend': _legend(),
            'xAxis': {**_axis_x(labels),
                      'axisLabel': {
                          'color': DARK_GRAY, 'fontSize': SMALL_SIZE,
                          'fontFamily': _font_body(), 'interval': 0,
                      }},
            'yAxis': [
                _axis_y(),
                {'type': 'value', 'min': 0, 'max': 100,
                 'axisLabel': {'formatter': '{value}%', 'color': ACCENT_RED,
                               'fontSize': SMALL_SIZE, 'fontFamily': _font_body()},
                 'axisLine': {'show': False}, 'axisTick': {'show': False},
                 'splitLine': {'show': False}},
            ],
            'series': [
                {'name': '数量', 'type': 'bar', 'barMaxWidth': 56,
                 'data': bar_data,
                 'label': {'show': True, 'position': 'top', 'formatter': '{c}',
                            'fontSize': SMALL_SIZE, 'fontFamily': _font_body(),
                            'color': MED_GRAY}},
                {'name': '累计占比', 'type': 'line', 'yAxisIndex': 1,
                 'smooth': False, 'data': cum_pcts,
                 'lineStyle': {'color': ACCENT_RED, 'width': 2},
                 'itemStyle': {'color': ACCENT_RED}, 'symbolSize': 6,
                 'markLine': {
                     'silent': True,
                     'lineStyle': {'color': ACCENT_RED, 'type': 'dashed',
                                   'width': 1.5},
                     'data': [{'yAxis': 80, 'yAxisIndex': 1,
                                'label': {'formatter': '80%',
                                           'color': ACCENT_RED,
                                           'fontSize': SMALL_SIZE,
                                           'fontFamily': _font_body()}}],
                 }},
            ],
        }
        slide_html = self._build_echart_slide(
            cid, option, height, title, source, summary)
        self._add_slide(slide_html)
        return self

    # ═══════════════════════════════════
    # INTERNAL BUILD HELPER
    # ═══════════════════════════════════

    def _summary_bar(self, text):
        """McKinsey-style insight badge (navy background strip)."""
        return (
            f'<div style="position:absolute;left:80px;top:110px;'
            f'background:{NAVY};color:#fff;'
            f'font-size:{SMALL_SIZE}px;'
            f'font-family:{_font_body()};'
            f'padding:5px 14px;border-radius:2px;line-height:1.35;">'
            f'{_esc(text)}</div>'
        )

    def _build_echart_slide(self, cid, option, height, title, source, summary):
        """
        Build a complete slide div containing an ECharts chart.
        Handles injection bookkeeping, script accumulation, and
        calls the engine's make_slide() core helper.
        """
        from .core import (
            make_slide, add_action_title, add_source, add_page_number,
        )
        from .constants import CONTENT_TOP, LM, CW

        self._ensure_echarts_injected()
        option_json = _json(option)
        cid_safe = _esc(cid)

        init_script = f"""
(function(){{
  var el = document.getElementById('{cid_safe}');
  if (!el) return;
  var c = echarts.init(el);
  c.setOption({option_json});
  window.addEventListener('resize', function(){{ c.resize(); }});
}})();
"""
        self._push_echart_script(init_script)

        # Compute top offset: if summary badge present, push chart down a bit
        chart_top = CONTENT_TOP + (30 if summary else 0)
        avail_h = min(height, 750 - chart_top - 50)

        parts = [add_action_title(title)]
        if summary:
            parts.append(self._summary_bar(summary))
        parts.append(
            f'<div style="position:absolute;left:{LM}px;top:{chart_top}px;'
            f'width:{CW}px;height:{avail_h}px;">'
            f'<div id="{cid}" style="width:100%;height:100%;"></div>'
            f'</div>'
        )
        if source:
            parts.append(add_source(source))
        parts.append(add_page_number(self._page, getattr(self, 'total', 30)))

        return make_slide('\n'.join(parts))
