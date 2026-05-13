"""McKinsey HTML Presentation Framework — High-level Layout Function Library.

Usage:
    from mck_html import MckHtmlEngine
    eng = MckHtmlEngine(total_slides=30)
    eng.cover(title='My Title', subtitle='Subtitle')
    eng.toc(items=[('1','Topic','Description'), ...])
    eng.save('output/my_deck.html')

ECharts integration (opt-in, enabled by default):
    eng = MckHtmlEngine(total_slides=12, use_echarts=True)
    eng.echart_grouped_bar(...)  # interactive Apache ECharts chart
    eng.grouped_bar(...)         # original SVG chart (still available)

v3 spec_lock integration:
    from mck_html import SpecLock, CanvasFormat, create_default_spec
    spec = create_default_spec(format='ppt169', project_name='demo', total_pages=10)
    spec.to_json('projects/demo/spec_lock.json')
"""
from .engine import MckHtmlEngine
from .constants import *
from .echarts_charts import (
    EChartsMixin,
    MCK_DARK, MCK_LIGHT, MCK_MID, MCK_PALE, MCK_VLIGHT,
    # Legacy aliases
    ACCENT_1, ACCENT_2, ACCENT_3, ACCENT_4, ACCENT_5, ACCENT_6,
    CHART_PALETTE,
    ECHARTS_CDN,
)
from .spec_lock import SpecLock, CanvasFormat, create_default_spec
from .pptx_analyzer import PptxAnalyzer, InferredField

__version__ = '3.1.0'
