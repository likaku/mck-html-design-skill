"""PPTX Analyzer — extract design features from PowerPoint files to auto-infer spec_lock.

This module bridges the ppt-master input pipeline with mck-html-design output.
It parses a .pptx file and extracts canvas, colors, typography, charts, images,
and per-slide content to generate a spec_lock.json draft.

Dependency:
    pip install python-pptx
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from pptx import Presentation
    from pptx.enum.chart import XL_CHART_TYPE
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    from pptx.util import Emu, Pt
except ImportError:
    raise ImportError("[ERROR] python-pptx is required. Install with: pip install python-pptx")

from .spec_lock import CanvasFormat, SpecLock


# ─────────────────────────────────────────────
# Confidence-tagged inference result
# ─────────────────────────────────────────────

@dataclass
class InferredField:
    """A single inferred design parameter with confidence metadata."""
    value: Any
    confidence: float  # 0.0 - 1.0
    source: str        # "pptx_theme" | "pptx_statistics" | "heuristic" | "default"
    reason: str        # Human-readable explanation


# ─────────────────────────────────────────────
# Chart type mapping: python-pptx → ECharts
# ─────────────────────────────────────────────

_CHART_TYPE_MAP: Dict[int, str] = {}

def _populate_chart_map() -> None:
    """Map XL_CHART_TYPE enum values to ECharts method names."""
    mapping = {
        # Bar / Column
        "COLUMN_CLUSTERED": "echart_grouped_bar",
        "COLUMN_STACKED": "echart_stacked_bar",
        "COLUMN_STACKED_100": "echart_stacked_bar",
        "BAR_CLUSTERED": "echart_horizontal_bar",
        "BAR_STACKED": "echart_horizontal_bar",
        "BAR_STACKED_100": "echart_horizontal_bar",
        # Line
        "LINE": "echart_line_chart",
        "LINE_MARKERS": "echart_line_chart",
        "LINE_STACKED": "echart_line_chart",
        # Pie / Donut
        "PIE": "echart_donut",
        "PIE_EXPLODED": "echart_donut",
        "DOUGHNUT": "echart_donut",
        "DOUGHNUT_EXPLODED": "echart_donut",
        # Area
        "AREA": "echart_line_chart",
        "AREA_STACKED": "echart_line_chart",
        # Scatter / Bubble
        "XY_SCATTER": "echart_bubble",
        "BUBBLE": "echart_bubble",
        # Radar
        "RADAR": "echart_radar",
        "RADAR_FILLED": "echart_radar",
    }
    for name, echart_type in mapping.items():
        try:
            val = getattr(XL_CHART_TYPE, name)
            _CHART_TYPE_MAP[val] = echart_type
        except AttributeError:
            pass

_populate_chart_map()


# ─────────────────────────────────────────────
# Core analyzer
# ─────────────────────────────────────────────

class PptxAnalyzer:
    """Analyze a PPTX file and extract design features for spec_lock generation."""

    def __init__(self, pptx_path: str | Path):
        self.path = Path(pptx_path)
        if not self.path.exists():
            raise FileNotFoundError(f"PPTX not found: {self.path}")
        self.prs = Presentation(str(self.path))
        self._font_counter: Counter = Counter()
        self._font_size_counter: Counter = Counter()
        self._title_size_counter: Counter = Counter()
        self._colors_found: List[str] = []
        self._charts_by_slide: Dict[int, List[dict]] = {}
        self._image_count_by_slide: Dict[int, int] = {}
        self._text_density_by_slide: Dict[int, int] = {}
        self._shape_count_by_slide: Dict[int, int] = {}
        self._slide_titles: Dict[int, str] = {}
        self._analyzed = False

    def analyze(self) -> "PptxAnalyzer":
        """Run full analysis pass over all slides."""
        for slide_idx, slide in enumerate(self.prs.slides, 1):
            self._analyze_slide(slide_idx, slide)
        self._analyzed = True
        return self

    def _analyze_slide(self, idx: int, slide: object) -> None:
        """Analyze a single slide for all features."""
        text_len = 0
        shape_count = 0
        image_count = 0
        charts = []

        for shape in self._iter_shapes(slide.shapes):
            shape_count += 1

            # Text analysis
            if getattr(shape, "has_text_frame", False):
                tf = shape.text_frame
                text = tf.text.strip()
                text_len += len(text)

                # Collect font info
                for para in tf.paragraphs:
                    for run in para.runs:
                        if run.font.name:
                            self._font_counter[run.font.name] += 1
                        if run.font.size:
                            size_pt = int(run.font.size / 12700)  # EMU to pt
                            self._font_size_counter[size_pt] += 1
                        if run.font.color and run.font.color.type is not None:
                            try:
                                rgb = run.font.color.rgb
                                if rgb:
                                    self._colors_found.append(f"#{rgb}")
                            except (AttributeError, TypeError):
                                pass

                # Check if this is a title placeholder
                try:
                    ph_fmt = shape.placeholder_format
                    if ph_fmt is not None:
                        ph_idx = ph_fmt.idx
                        if ph_idx in (0, 1, 15):  # title or center title
                            self._slide_titles[idx] = text[:100]
                            for para in tf.paragraphs:
                                for run in para.runs:
                                    if run.font.size:
                                        self._title_size_counter[int(run.font.size / 12700)] += 1
                except (ValueError, AttributeError):
                    pass

            # Chart analysis
            if getattr(shape, "has_chart", False):
                chart_info = self._extract_chart_info(shape, idx)
                if chart_info:
                    charts.append(chart_info)

            # Image analysis
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                image_count += 1

        self._text_density_by_slide[idx] = text_len
        self._shape_count_by_slide[idx] = shape_count
        self._image_count_by_slide[idx] = image_count
        if charts:
            self._charts_by_slide[idx] = charts

    def _iter_shapes(self, shapes: object):
        """Recursively flatten grouped shapes."""
        for shape in shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
                yield from self._iter_shapes(shape.shapes)
            else:
                yield shape

    def _extract_chart_info(self, shape: object, slide_idx: int) -> Optional[dict]:
        """Extract chart type and basic data info from a chart shape."""
        try:
            chart = shape.chart
            chart_type_val = chart.chart_type
            echart_method = _CHART_TYPE_MAP.get(chart_type_val, "echart_grouped_bar")

            # Extract chart title if available
            title = ""
            try:
                if chart.has_title:
                    title = chart.chart_title.text_frame.text.strip()
            except Exception:
                pass

            # Count data series
            series_count = 0
            try:
                series_count = len(chart.series)
            except Exception:
                pass

            return {
                "engine": "echarts",
                "type": echart_method.replace("echart_", ""),
                "method": echart_method,
                "title": title or f"Chart on slide {slide_idx}",
                "interactive": True,
                "height": 380,
                "series_count": series_count,
                "original_chart_type": str(chart_type_val),
            }
        except Exception:
            return None

    # ─────────────────────────────────────────
    # Inference methods
    # ─────────────────────────────────────────

    def infer_canvas(self) -> InferredField:
        """Infer canvas format from slide dimensions."""
        w_emu = self.prs.slide_width
        h_emu = self.prs.slide_height
        ratio = w_emu / h_emu

        # Match to closest CanvasFormat
        best_fmt = "ppt169"
        best_diff = float("inf")
        for fmt in CanvasFormat:
            fmt_ratio = fmt.width / fmt.height
            diff = abs(ratio - fmt_ratio)
            if diff < best_diff:
                best_diff = diff
                best_fmt = fmt.name

        confidence = 0.95 if best_diff < 0.05 else 0.7
        fmt_obj = CanvasFormat[best_fmt]

        return InferredField(
            value={"format": best_fmt, "width": fmt_obj.width, "height": fmt_obj.height,
                   "background_color": "#FFFFFF", "brand_color": "#172B4D", "accent_color": "#00AEEF"},
            confidence=confidence,
            source="pptx_theme",
            reason=f"Slide aspect ratio {ratio:.3f} → best match: {best_fmt} (diff={best_diff:.3f})"
        )

    def infer_typography(self) -> InferredField:
        """Infer typography from font statistics."""
        # Most common font
        if self._font_counter:
            top_font = self._font_counter.most_common(1)[0][0]
        else:
            top_font = "KaiTi"

        # Title size
        if self._title_size_counter:
            title_size = self._title_size_counter.most_common(1)[0][0]
        else:
            title_size = 28

        # Body size (median of all non-title sizes)
        if self._font_size_counter:
            sizes = sorted(self._font_size_counter.elements())
            body_size = sizes[len(sizes) // 2] if sizes else 16
        else:
            body_size = 16

        small_size = max(body_size - 4, 10)

        # Build web-safe font stack with CJK fallback
        cjk_fonts = ["KaiTi", "STKaiti", "Noto Serif SC", "Microsoft YaHei", "SimHei"]
        latin_fonts = ["Arial", "Helvetica", "sans-serif"]
        if top_font not in cjk_fonts and top_font not in latin_fonts:
            font_stack = f"'{top_font}', " + ", ".join(f"'{f}'" for f in cjk_fonts[:2]) + ", " + ", ".join(latin_fonts)
        else:
            font_stack = ", ".join(f"'{f}'" for f in cjk_fonts[:3]) + ", " + ", ".join(latin_fonts)

        confidence = 0.8 if self._font_counter else 0.4

        return InferredField(
            value={
                "font_family": font_stack,
                "title_size": title_size,
                "body_size": body_size,
                "small_size": small_size,
                "h1_size": title_size + 4,
                "h2_size": title_size,
                "h3_size": body_size + 2,
                "line_height": 1.6,
                "detected_fonts": dict(self._font_counter.most_common(5)),
            },
            confidence=confidence,
            source="pptx_statistics",
            reason=f"Top font: {top_font} ({self._font_counter.get(top_font, 0)} uses), "
                   f"title_size={title_size}pt, body_size={body_size}pt"
        )

    def infer_color_palette(self) -> InferredField:
        """Infer color palette from theme and text colors."""
        # Try to extract theme colors
        theme_colors = self._extract_theme_colors()

        # Combine with text color statistics
        color_counter = Counter(self._colors_found)
        top_colors = [c for c, _ in color_counter.most_common(10)]

        # Determine primary/secondary/accent
        primary = theme_colors.get("dk1", "#172B4D")
        secondary = theme_colors.get("accent1", "#0073B6")
        accent = theme_colors.get("accent2", "#00AEEF")

        # Build neutral ramp
        neutrals = ["#FFFFFF", "#F5F7FA", "#E2E8F0", "#8993A4", "#2C3E50"]

        # Chart series colors from accents
        chart_series = [
            theme_colors.get(f"accent{i}", c)
            for i, c in enumerate(["#0073B6", "#00AEEF", "#36B37E", "#FFAB00", "#FF5630", "#6554C0"], 1)
        ]

        confidence = 0.85 if theme_colors else 0.5

        return InferredField(
            value={
                "primary": primary,
                "secondary": secondary,
                "accent": accent,
                "neutrals": neutrals,
                "semantic": {
                    "success": "#36B37E",
                    "warning": "#FFAB00",
                    "danger": "#FF5630",
                    "info": "#0065FF",
                },
                "chart_series": chart_series[:6],
                "detected_colors": top_colors[:10],
            },
            confidence=confidence,
            source="pptx_theme" if theme_colors else "default",
            reason=f"Theme colors extracted: {len(theme_colors)}, text colors found: {len(set(self._colors_found))}"
        )

    def _extract_theme_colors(self) -> Dict[str, str]:
        """Extract theme colors from the slide master."""
        colors = {}
        try:
            from lxml import etree
            theme_xml = self.prs.slide_masters[0].slide_layouts[0].slide_master.element
            # Navigate to theme color definitions
            ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
            for color_name in ["dk1", "dk2", "lt1", "lt2", "accent1", "accent2",
                               "accent3", "accent4", "accent5", "accent6"]:
                elems = theme_xml.findall(f".//a:{color_name}//a:srgbClr", ns)
                if elems:
                    colors[color_name] = f"#{elems[0].get('val', '000000')}"
                else:
                    # Try system color
                    sys_elems = theme_xml.findall(f".//a:{color_name}//a:sysClr", ns)
                    if sys_elems:
                        colors[color_name] = f"#{sys_elems[0].get('lastClr', '000000')}"
        except Exception:
            pass
        return colors

    def infer_page_charts(self) -> InferredField:
        """Infer chart configuration per page."""
        page_charts = {}
        for slide_idx, charts in self._charts_by_slide.items():
            # Use the first/primary chart on each slide
            chart = charts[0]
            page_charts[str(slide_idx)] = {
                "engine": chart["engine"],
                "type": chart["type"],
                "method": chart["method"],
                "title": chart["title"],
                "interactive": True,
                "height": 380,
                "animation": True,
            }

        confidence = 0.9 if page_charts else 1.0  # no charts is certain too

        return InferredField(
            value=page_charts,
            confidence=confidence,
            source="pptx_statistics",
            reason=f"Found {len(page_charts)} slides with charts"
        )

    def infer_page_rhythm(self) -> InferredField:
        """Infer page rhythm (anchor/dense/breathing) based on content density."""
        total = len(self.prs.slides)
        rhythms = {}

        for i in range(1, total + 1):
            shapes = self._shape_count_by_slide.get(i, 0)
            text_len = self._text_density_by_slide.get(i, 0)
            has_chart = i in self._charts_by_slide
            title = self._slide_titles.get(i, "")

            # Heuristic rules
            if i == 1 or i == total:
                rhythms[str(i)] = "anchor"  # cover and closing
            elif shapes <= 3 and text_len < 100:
                rhythms[str(i)] = "anchor"  # section divider
            elif text_len < 200 and not has_chart:
                rhythms[str(i)] = "breathing"
            else:
                rhythms[str(i)] = "dense"

        return InferredField(
            value=rhythms,
            confidence=0.6,
            source="heuristic",
            reason=f"Classified {total} pages: "
                   f"{sum(1 for v in rhythms.values() if v == 'anchor')} anchor, "
                   f"{sum(1 for v in rhythms.values() if v == 'dense')} dense, "
                   f"{sum(1 for v in rhythms.values() if v == 'breathing')} breathing"
        )

    def infer_audience(self) -> InferredField:
        """Infer target audience from content keywords."""
        all_text = " ".join(
            self._slide_titles.get(i, "") for i in range(1, len(self.prs.slides) + 1)
        )

        # Simple keyword matching
        executive_kw = ["战略", "董事", "汇报", "决策", "规划", "愿景", "strategy", "board", "executive"]
        operational_kw = ["执行", "操作", "培训", "流程", "SOP", "implementation", "training"]
        investor_kw = ["投资", "融资", "IPO", "估值", "investor", "fundraising"]

        exec_score = sum(1 for kw in executive_kw if kw in all_text)
        ops_score = sum(1 for kw in operational_kw if kw in all_text)
        inv_score = sum(1 for kw in investor_kw if kw in all_text)

        if exec_score >= ops_score and exec_score >= inv_score:
            role = "executive"
        elif inv_score >= ops_score:
            role = "investor"
        else:
            role = "operational"

        confidence = 0.5 + min(max(exec_score, ops_score, inv_score) * 0.1, 0.4)

        return InferredField(
            value={"role": role, "context": "", "core_message": ""},
            confidence=confidence,
            source="heuristic",
            reason=f"Keyword scores: executive={exec_score}, operational={ops_score}, investor={inv_score}"
        )

    def infer_style(self) -> InferredField:
        """Infer presentation style."""
        # Check for consulting patterns (structured, data-heavy)
        chart_count = sum(len(c) for c in self._charts_by_slide.values())
        total_slides = len(self.prs.slides)
        data_ratio = chart_count / max(total_slides, 1)

        if data_ratio > 0.3:
            style_type = "mckinsey"
            reason = f"High chart density ({data_ratio:.0%})"
        elif data_ratio > 0.1:
            style_type = "mixed"
            reason = f"Moderate chart density ({data_ratio:.0%})"
        else:
            style_type = "creative"
            reason = f"Low chart density ({data_ratio:.0%})"

        return InferredField(
            value={"type": style_type, "tone": "formal", "density": "dense"},
            confidence=0.5,
            source="heuristic",
            reason=reason
        )

    # ─────────────────────────────────────────
    # Full inference → SpecLock
    # ─────────────────────────────────────────

    def to_spec_lock(self, project_name: Optional[str] = None) -> SpecLock:
        """Run all inferences and produce a SpecLock object."""
        if not self._analyzed:
            self.analyze()

        canvas = self.infer_canvas()
        typo = self.infer_typography()
        colors = self.infer_color_palette()
        charts = self.infer_page_charts()
        rhythm = self.infer_page_rhythm()
        audience = self.infer_audience()
        style = self.infer_style()

        name = project_name or self.path.stem

        return SpecLock(
            canvas=canvas.value,
            typography=typo.value,
            color_palette=colors.value,
            page_layouts={},  # To be filled by Strategist
            page_rhythm=rhythm.value,
            page_charts=charts.value,
            total_pages=len(self.prs.slides),
            project_name=name,
            audience=audience.value,
            style=style.value,
            images={"strategy": "placeholder", "assets": [], "constraints": {}},
            icons={"library": "lucide", "method": "svg_inline", "inventory": []},
            html_constraints={
                "responsive": False,
                "css_framework": "none",
                "js_allowed": ["echarts"],
                "accessibility": "AA",
                "print_friendly": False,
                "animation_allowed": True,
            },
            page_data={},
            forbidden=[
                "External CDN links (all assets must be inline)",
                "iframe elements",
                "Inline event handlers (onclick etc.)",
                "Colors not in color_palette",
            ],
            metadata={
                "schema_version": "2.0",
                "source_file": str(self.path.name),
                "source_slides": len(self.prs.slides),
                "confirmed_by_user": False,
                "inference_confidence": {
                    "canvas": canvas.confidence,
                    "typography": typo.confidence,
                    "color_palette": colors.confidence,
                    "page_charts": charts.confidence,
                    "page_rhythm": rhythm.confidence,
                    "audience": audience.confidence,
                    "style": style.confidence,
                },
            },
        )

    def summary(self) -> str:
        """Return a human-readable summary of the analysis."""
        if not self._analyzed:
            self.analyze()

        total = len(self.prs.slides)
        charts_total = sum(len(c) for c in self._charts_by_slide.values())
        images_total = sum(self._image_count_by_slide.values())
        top_fonts = self._font_counter.most_common(3)

        lines = [
            f"📊 PPTX Analysis: {self.path.name}",
            f"  Slides: {total}",
            f"  Charts: {charts_total} (on {len(self._charts_by_slide)} slides)",
            f"  Images: {images_total}",
            f"  Top fonts: {', '.join(f'{f}({n})' for f, n in top_fonts)}",
            f"  Slide titles (first 5):",
        ]
        for i in range(1, min(6, total + 1)):
            title = self._slide_titles.get(i, "(no title)")
            lines.append(f"    Slide {i}: {title}")

        return "\n".join(lines)
