#!/usr/bin/env python3
"""
pptx_to_html.py v2 — Pixel-accurate PPTX → HTML replication

Fixes from v1:
  1. Group coordinate transform (chOff/chExt scaling) — properly resolves nested groups
  2. Theme color resolution — reads theme XML and maps scheme colors to RGB
  3. LINE shapes — renders horizontal/vertical/diagonal lines as positioned divs
  4. Better border rendering for cells/boxes

Usage:
    python pptx_to_html.py input.pptx -o output.html
    python pptx_to_html.py input.pptx --slides 1-10
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import zipfile
from io import BytesIO
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

try:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Emu
except ImportError:
    print("[ERROR] python-pptx required: pip install python-pptx")
    sys.exit(1)


# ═══════════════════════════════════════════
# Unit conversion
# ═══════════════════════════════════════════

def emu_to_px(emu) -> float:
    """Convert EMU to pixels (96 dpi)."""
    if emu is None:
        return 0.0
    return round(int(emu) / 914400 * 96, 1)


# ═══════════════════════════════════════════
# Theme color resolver
# ═══════════════════════════════════════════

class ThemeColors:
    """Extracts and resolves theme/scheme colors from a PPTX file."""

    # Mapping from pptx theme_color enum to XML element name
    _THEME_MAP = {
        1: "dk1", 2: "lt1", 3: "dk2", 4: "lt2",
        5: "accent1", 6: "accent2", 7: "accent3", 8: "accent4",
        9: "accent5", 10: "accent6", 11: "hlink", 12: "folHlink",
        # python-pptx uses these names internally
        13: "dk1", 14: "lt1", 15: "dk2", 16: "lt2",
    }
    # Also map string names
    _NAME_MAP = {
        "DARK_1": "dk1", "LIGHT_1": "lt1", "DARK_2": "dk2", "LIGHT_2": "lt2",
        "ACCENT_1": "accent1", "ACCENT_2": "accent2", "ACCENT_3": "accent3",
        "ACCENT_4": "accent4", "ACCENT_5": "accent5", "ACCENT_6": "accent6",
        "HYPERLINK": "hlink", "FOLLOWED_HYPERLINK": "folHlink",
        "BACKGROUND_1": "lt1", "BACKGROUND_2": "lt2",
        "TEXT_1": "dk1", "TEXT_2": "dk2",
    }

    def __init__(self, pptx_path: str):
        self.colors: Dict[str, str] = {}
        self._extract(pptx_path)

    def _extract(self, pptx_path: str):
        """Parse theme XML from the PPTX zip."""
        try:
            zf = zipfile.ZipFile(pptx_path)
            theme_files = sorted(f for f in zf.namelist()
                                 if 'theme' in f.lower() and f.endswith('.xml'))
            if not theme_files:
                return

            ns_a = "http://schemas.openxmlformats.org/drawingml/2006/main"
            tree = ET.parse(BytesIO(zf.read(theme_files[0])))
            root = tree.getroot()

            # Find clrScheme
            for elem in root.iter(f'{{{ns_a}}}clrScheme'):
                for child in elem:
                    tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                    srgb = child.find(f'{{{ns_a}}}srgbClr')
                    sys_clr = child.find(f'{{{ns_a}}}sysClr')
                    if srgb is not None:
                        self.colors[tag] = f"#{srgb.get('val', '000000')}"
                    elif sys_clr is not None:
                        self.colors[tag] = f"#{sys_clr.get('lastClr', '000000')}"
                break  # Use first clrScheme found
            zf.close()
        except Exception:
            pass

    def resolve(self, theme_color_idx) -> Optional[str]:
        """Resolve a theme color index/name to hex RGB."""
        # Try numeric
        if isinstance(theme_color_idx, int):
            name = self._THEME_MAP.get(theme_color_idx)
            if name:
                return self.colors.get(name)

        # Try string enum name
        s = str(theme_color_idx).replace(" ", "").split("(")[0]
        name = self._NAME_MAP.get(s)
        if name:
            return self.colors.get(name)

        return None


# ═══════════════════════════════════════════
# Color extraction
# ═══════════════════════════════════════════

def get_color(color_obj, theme: ThemeColors) -> Optional[str]:
    """Extract hex color, resolving themes."""
    if color_obj is None:
        return None
    try:
        ct = color_obj.type
        if ct is None:
            return None
        ct_str = str(ct)

        # Direct RGB
        if "RGB" in ct_str:
            try:
                return f"#{color_obj.rgb}"
            except:
                return None

        # Theme/Scheme color
        if "SCHEME" in ct_str or "THEME" in ct_str:
            try:
                tc = color_obj.theme_color
                resolved = theme.resolve(tc)
                if resolved:
                    # Apply brightness/tint if present
                    try:
                        brightness = color_obj.brightness
                        if brightness and brightness != 0:
                            resolved = _apply_brightness(resolved, brightness)
                    except:
                        pass
                    return resolved
            except:
                pass

    except (AttributeError, TypeError):
        pass
    return None


def _apply_brightness(hex_color: str, brightness: float) -> str:
    """Apply brightness adjustment to a hex color."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    if brightness > 0:
        # Tint (lighten)
        r = r + (255 - r) * brightness
        g = g + (255 - g) * brightness
        b = b + (255 - b) * brightness
    else:
        # Shade (darken)
        factor = 1 + brightness
        r, g, b = r * factor, g * factor, b * factor
    r, g, b = int(min(255, max(0, r))), int(min(255, max(0, g))), int(min(255, max(0, b)))
    return f"#{r:02X}{g:02X}{b:02X}"


def get_fill(shape, theme: ThemeColors) -> Optional[str]:
    """Get fill color from shape."""
    try:
        fill = shape.fill
        if fill is None or fill.type is None:
            return None
        ft = str(fill.type)
        if 'SOLID' in ft:
            return get_color(fill.fore_color, theme)
        if 'BACKGROUND' in ft:
            return None  # Transparent
    except:
        pass
    return None


def get_line_style(shape, theme: ThemeColors) -> Tuple[Optional[str], float]:
    """Get border color and width."""
    try:
        line = shape.line
        if line is None:
            return None, 0
        w = line.width
        if w is None or w == 0:
            return None, 0
        width_px = emu_to_px(w)
        if width_px < 0.3:
            width_px = 0.5  # minimum visible

        color = None
        try:
            if line.color and line.color.type is not None:
                color = get_color(line.color, theme)
        except:
            pass
        if color is None:
            color = "#000000"  # Default line color is black

        return color, width_px
    except:
        return None, 0


# ═══════════════════════════════════════════
# Group coordinate transform
# ═══════════════════════════════════════════

@dataclass
class AbsoluteRect:
    """Absolutely positioned rectangle in slide pixel coordinates."""
    left: float
    top: float
    width: float
    height: float


def resolve_group_children(group_shape) -> List[Tuple[Any, AbsoluteRect]]:
    """
    Recursively resolve all shapes in a group to absolute slide coordinates.

    Group shapes have their own coordinate space (chOff/chExt).
    Child positions must be transformed:
        abs_x = group.off.x + (child.x - chOff.x) * (ext.cx / chExt.cx)
        abs_y = group.off.y + (child.y - chOff.y) * (ext.cy / chExt.cy)
    """
    results = []
    _resolve_group_recursive(group_shape, results)
    return results


def _resolve_group_recursive(group_shape, results: list,
                              parent_off_x=0, parent_off_y=0,
                              parent_scale_x=1.0, parent_scale_y=1.0):
    """Recursively transform group children to absolute coordinates."""
    ns_a = "http://schemas.openxmlformats.org/drawingml/2006/main"

    # Get group's own transform
    grp_elem = group_shape._element
    # Find grpSpPr/xfrm which has off, ext, chOff, chExt
    xfrm = None
    for tag in [f'{{{ns_a}}}xfrm',
                '{http://schemas.openxmlformats.org/presentationml/2006/main}xfrm']:
        xfrm = grp_elem.find(f'.//{{{ns_a[:-1]}}}grpSpPr/{{{ns_a}}}xfrm')
        if xfrm is not None:
            break

    if xfrm is None:
        # Try different path
        for child in grp_elem:
            if 'grpSpPr' in child.tag:
                xfrm = child.find(f'{{{ns_a}}}xfrm')
                break

    if xfrm is None:
        # Fallback: use shape properties directly
        g_off_x = int(group_shape.left or 0)
        g_off_y = int(group_shape.top or 0)
        for child in group_shape.shapes:
            if child.shape_type == MSO_SHAPE_TYPE.GROUP:
                _resolve_group_recursive(child, results, g_off_x, g_off_y, 1.0, 1.0)
            else:
                rect = AbsoluteRect(
                    left=emu_to_px(int(child.left or 0) + g_off_x),
                    top=emu_to_px(int(child.top or 0) + g_off_y),
                    width=emu_to_px(child.width or 0),
                    height=emu_to_px(child.height or 0),
                )
                results.append((child, rect))
        return

    # Parse transform values
    off_el = xfrm.find(f'{{{ns_a}}}off')
    ext_el = xfrm.find(f'{{{ns_a}}}ext')
    chOff_el = xfrm.find(f'{{{ns_a}}}chOff')
    chExt_el = xfrm.find(f'{{{ns_a}}}chExt')

    g_off_x = int(off_el.get('x', '0')) if off_el is not None else int(group_shape.left or 0)
    g_off_y = int(off_el.get('y', '0')) if off_el is not None else int(group_shape.top or 0)
    g_ext_cx = int(ext_el.get('cx', '1')) if ext_el is not None else int(group_shape.width or 1)
    g_ext_cy = int(ext_el.get('cy', '1')) if ext_el is not None else int(group_shape.height or 1)
    ch_off_x = int(chOff_el.get('x', '0')) if chOff_el is not None else 0
    ch_off_y = int(chOff_el.get('y', '0')) if chOff_el is not None else 0
    ch_ext_cx = int(chExt_el.get('cx', '1')) if chExt_el is not None else g_ext_cx
    ch_ext_cy = int(chExt_el.get('cy', '1')) if chExt_el is not None else g_ext_cy

    # Scale factors for this group
    scale_x = g_ext_cx / ch_ext_cx if ch_ext_cx != 0 else 1.0
    scale_y = g_ext_cy / ch_ext_cy if ch_ext_cy != 0 else 1.0

    for child in group_shape.shapes:
        c_left = int(child.left or 0)
        c_top = int(child.top or 0)
        c_width = int(child.width or 0)
        c_height = int(child.height or 0)

        # Transform to parent (group) coordinate space
        abs_x = g_off_x + (c_left - ch_off_x) * scale_x
        abs_y = g_off_y + (c_top - ch_off_y) * scale_y
        abs_w = c_width * scale_x
        abs_h = c_height * scale_y

        # Apply parent transform chain
        final_x = parent_off_x + (abs_x - parent_off_x) * parent_scale_x if parent_scale_x != 1.0 else abs_x
        final_y = parent_off_y + (abs_y - parent_off_y) * parent_scale_y if parent_scale_y != 1.0 else abs_y

        if child.shape_type == MSO_SHAPE_TYPE.GROUP:
            # For nested groups, override child's position before recursing
            _resolve_group_recursive(child, results,
                                     parent_off_x=0, parent_off_y=0,
                                     parent_scale_x=1.0, parent_scale_y=1.0)
        else:
            rect = AbsoluteRect(
                left=emu_to_px(abs_x),
                top=emu_to_px(abs_y),
                width=emu_to_px(abs_w),
                height=emu_to_px(abs_h),
            )
            results.append((child, rect))


# ═══════════════════════════════════════════
# Text rendering
# ═══════════════════════════════════════════

def render_text_frame(text_frame, theme: ThemeColors) -> str:
    """Render a text frame to HTML with run-level formatting."""
    parts = []
    for para in text_frame.paragraphs:
        runs_html = []
        for run in para.runs:
            text = run.text
            if not text:
                continue
            # Escape
            text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

            styles = []
            f = run.font
            if f.size:
                size_pt = round(f.size / 12700, 1)
                styles.append(f"font-size:{size_pt}pt")
            if f.name and f.name not in ('+mj-lt', '+mn-lt', '+mj-ea', '+mn-ea'):
                styles.append(f"font-family:'{f.name}',Arial,sans-serif")
            if f.bold:
                styles.append("font-weight:bold")
            if f.italic:
                styles.append("font-style:italic")

            color = get_color(f.color, theme) if f.color else None
            if color:
                styles.append(f"color:{color}")

            if styles:
                runs_html.append(f'<span style="{";".join(styles)}">{text}</span>')
            else:
                runs_html.append(text)

        if not runs_html:
            # Empty paragraph — add spacing
            parts.append('<div style="height:4px"></div>')
            continue

        # Alignment
        align = "left"
        try:
            if para.alignment == PP_ALIGN.CENTER:
                align = "center"
            elif para.alignment == PP_ALIGN.RIGHT:
                align = "right"
        except:
            pass

        p_style = f"text-align:{align};line-height:1.3;margin:0"
        # Bullet indent
        if para.level and para.level > 0:
            p_style += f";padding-left:{para.level * 14}px"

        parts.append(f'<div style="{p_style}">{"".join(runs_html)}</div>')

    return "".join(parts)


# ═══════════════════════════════════════════
# Image extraction
# ═══════════════════════════════════════════

def get_image_data_uri(shape) -> Optional[str]:
    """Get base64 data URI for an image shape."""
    try:
        image = shape.image
        ext = (image.ext or "png").lower()
        if ext in ("emf", "wmf"):
            return None
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                "gif": "image/gif", "svg": "image/svg+xml", "tiff": "image/tiff",
                "bmp": "image/bmp"}.get(ext, f"image/{ext}")
        b64 = base64.b64encode(image.blob).decode("ascii")
        return f"data:{mime};base64,{b64}"
    except:
        return None


# ═══════════════════════════════════════════
# Chart extraction for ECharts
# ═══════════════════════════════════════════

def extract_chart(chart) -> Optional[dict]:
    """Extract chart data for ECharts rendering."""
    try:
        ct = str(chart.chart_type)
        categories = []
        series = []

        try:
            plot = chart.plots[0]
            if hasattr(plot, 'categories') and plot.categories:
                categories = [str(c) for c in plot.categories]
        except:
            pass

        for s in chart.series:
            sd = {"name": str(s.name) if hasattr(s, 'name') else "", "values": []}
            try:
                sd["values"] = [float(v) if v is not None else 0 for v in s.values]
            except:
                pass
            series.append(sd)

        echart_type = "bar"
        if "LINE" in ct:
            echart_type = "line"
        elif "PIE" in ct or "DOUGHNUT" in ct:
            echart_type = "pie"
        elif "AREA" in ct:
            echart_type = "line"
        elif "SCATTER" in ct or "BUBBLE" in ct:
            echart_type = "scatter"
        elif "RADAR" in ct:
            echart_type = "radar"

        return {
            "type": echart_type,
            "stacked": "STACKED" in ct,
            "horizontal": "BAR_" in ct,
            "categories": categories,
            "series": series,
        }
    except:
        return None


# ═══════════════════════════════════════════
# Shape → HTML element
# ═══════════════════════════════════════════

def shape_to_element(shape, rect: AbsoluteRect, slide_idx: int, shape_idx: int,
                     theme: ThemeColors) -> str:
    """Convert shape + absolute rect to HTML element."""
    l, t, w, h = rect.left, rect.top, rect.width, rect.height

    # Skip invisible
    if w < 1 and h < 1:
        return ""

    styles = [
        "position:absolute",
        f"left:{l:.1f}px",
        f"top:{t:.1f}px",
        f"width:{w:.1f}px",
        f"height:{h:.1f}px",
    ]

    # Rotation
    rot = shape.rotation if hasattr(shape, 'rotation') and shape.rotation else 0
    if rot:
        styles.append(f"transform:rotate({rot}deg)")

    # Fill
    fill = get_fill(shape, theme)
    if fill:
        styles.append(f"background:{fill}")

    # Border
    line_color, line_w = get_line_style(shape, theme)
    if line_color and line_w > 0:
        styles.append(f"border:{line_w:.1f}px solid {line_color}")

    # ── LINE shape ──
    if shape.shape_type in (9,):  # MSO_SHAPE_TYPE.LINE = 9
        return _render_line(shape, rect, theme)

    # ── PICTURE ──
    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        uri = get_image_data_uri(shape)
        if uri:
            return f'<img src="{uri}" style="{";".join(styles)};object-fit:contain" />'
        return ""

    # ── CHART ──
    if hasattr(shape, 'has_chart') and shape.has_chart:
        data = extract_chart(shape.chart)
        if data:
            cid = f"chart-{slide_idx}-{shape_idx}"
            styles.append("overflow:hidden")
            return (f'<div id="{cid}" style="{";".join(styles)}" '
                    f'data-chart=\'{json.dumps(data, ensure_ascii=False)}\'></div>')

    # ── TABLE ──
    if hasattr(shape, 'has_table') and shape.has_table:
        return _render_table(shape, styles, theme)

    # ── TEXT FRAME ──
    if hasattr(shape, 'has_text_frame') and shape.has_text_frame:
        inner = render_text_frame(shape.text_frame, theme)
        if not inner.replace('<div style="height:4px"></div>', '').strip():
            # Empty text — still render if has fill/border
            if fill or (line_color and line_w > 0):
                return f'<div style="{";".join(styles)}"></div>'
            return ""
        styles.append("overflow:hidden;padding:3px 5px")
        return f'<div style="{";".join(styles)}">{inner}</div>'

    # ── Generic shape with fill/border ──
    if fill or (line_color and line_w > 0):
        return f'<div style="{";".join(styles)}"></div>'

    return ""


def _render_line(shape, rect: AbsoluteRect, theme: ThemeColors) -> str:
    """Render LINE shape as a positioned div."""
    line_color, line_w = get_line_style(shape, theme)
    if not line_color:
        line_color = "#000000"
    if line_w < 0.5:
        line_w = 0.7

    l, t, w, h = rect.left, rect.top, rect.width, rect.height

    if h < 2:
        # Horizontal line
        return (f'<div style="position:absolute;left:{l:.1f}px;top:{t:.1f}px;'
                f'width:{w:.1f}px;height:{line_w:.1f}px;background:{line_color}"></div>')
    elif w < 2:
        # Vertical line
        return (f'<div style="position:absolute;left:{l:.1f}px;top:{t:.1f}px;'
                f'width:{line_w:.1f}px;height:{h:.1f}px;background:{line_color}"></div>')
    else:
        # Diagonal line — use SVG
        return (f'<svg style="position:absolute;left:{l:.1f}px;top:{t:.1f}px;'
                f'width:{w:.1f}px;height:{h:.1f}px;overflow:visible">'
                f'<line x1="0" y1="0" x2="{w}" y2="{h}" '
                f'stroke="{line_color}" stroke-width="{line_w}"/></svg>')


def _render_table(shape, base_styles: list, theme: ThemeColors) -> str:
    """Render table shape."""
    table = shape.table
    html = f'<div style="{";".join(base_styles)};overflow:hidden;padding:0">'
    html += '<table style="width:100%;height:100%;border-collapse:collapse;font-size:10px;table-layout:fixed">'

    for row_idx, row in enumerate(table.rows):
        html += "<tr>"
        for cell in row.cells:
            cs = "padding:3px 6px;border:0.5px solid #bbb;vertical-align:top;overflow:hidden;word-wrap:break-word;"
            # Cell fill
            try:
                cf = cell.fill
                if cf and cf.type is not None and 'SOLID' in str(cf.type):
                    fc = get_color(cf.fore_color, theme)
                    if fc:
                        cs += f"background:{fc};"
                        r, g, b = int(fc[1:3], 16), int(fc[3:5], 16), int(fc[5:7], 16)
                        if r * 0.299 + g * 0.587 + b * 0.114 < 128:
                            cs += "color:#fff;"
            except:
                pass

            text = cell.text.replace("\n", "<br>").replace("&", "&amp;")
            tag = "th" if row_idx == 0 else "td"
            html += f'<{tag} style="{cs}">{text}</{tag}>'
        html += "</tr>"

    html += "</table></div>"
    return html


# ═══════════════════════════════════════════
# Slide → HTML
# ═══════════════════════════════════════════

def render_slide(slide, slide_idx: int, theme: ThemeColors, canvas_w: float, canvas_h: float) -> str:
    """Render a single slide to HTML."""
    html = f'<div class="slide" id="slide-{slide_idx}"'

    # Slide background
    bg = None
    try:
        bg_fill = slide.background.fill
        if bg_fill and bg_fill.type is not None and 'SOLID' in str(bg_fill.type):
            bg = get_color(bg_fill.fore_color, theme)
    except:
        pass
    if bg:
        html += f' style="background:{bg}"'
    html += '>\n'

    # Collect all shapes (flatten groups)
    shape_idx = 0
    for shape in slide.shapes:
        shape_idx += 1

        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            # Resolve group children to absolute coordinates
            children = resolve_group_children(shape)
            for child_shape, child_rect in children:
                shape_idx += 1
                elem = shape_to_element(child_shape, child_rect, slide_idx, shape_idx, theme)
                if elem:
                    html += f"  {elem}\n"
        else:
            # Top-level shape — use its own coordinates
            rect = AbsoluteRect(
                left=emu_to_px(shape.left or 0),
                top=emu_to_px(shape.top or 0),
                width=emu_to_px(shape.width or 0),
                height=emu_to_px(shape.height or 0),
            )
            elem = shape_to_element(shape, rect, slide_idx, shape_idx, theme)
            if elem:
                html += f"  {elem}\n"

    html += f'  <div class="pg">{slide_idx}</div>\n'
    html += '</div>\n'
    return html


# ═══════════════════════════════════════════
# Full document assembly
# ═══════════════════════════════════════════

def build_html(canvas_w: float, canvas_h: float, slides_html: str, has_charts: bool) -> str:
    """Assemble full HTML document."""
    echarts_cdn = ""
    chart_js = ""
    if has_charts:
        echarts_cdn = '<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>'
        chart_js = """
<script>
document.addEventListener('DOMContentLoaded', function() {
  var C = ['#0073B6','#00A9F4','#36B37E','#FFAB00','#FF5630','#6554C0','#172B4D','#8993A4'];
  document.querySelectorAll('[data-chart]').forEach(function(el) {
    var d = JSON.parse(el.getAttribute('data-chart'));
    var chart = echarts.init(el);
    var o = {};
    if (d.type === 'pie') {
      var pd = []; if(d.series[0]) d.categories.forEach(function(c,i){pd.push({name:c,value:d.series[0].values[i]||0})});
      o = {tooltip:{trigger:'item'},legend:{bottom:5,textStyle:{fontSize:9}},series:[{type:'pie',radius:['30%','60%'],data:pd,label:{fontSize:9}}]};
    } else if (d.type === 'line') {
      o = {tooltip:{trigger:'axis'},legend:{bottom:0,textStyle:{fontSize:9}},grid:{top:20,right:15,bottom:35,left:45},
        xAxis:{type:'category',data:d.categories,axisLabel:{fontSize:9}},yAxis:{type:'value',axisLabel:{fontSize:9}},
        series:d.series.map(function(s,i){return{name:s.name,type:'line',data:s.values,smooth:true,itemStyle:{color:C[i%8]}}})};
    } else {
      var horiz = d.horizontal;
      o = {tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},legend:{bottom:0,textStyle:{fontSize:9}},
        grid:{top:20,right:15,bottom:35,left:horiz?70:45},
        xAxis:{type:horiz?'value':'category',data:horiz?null:d.categories,axisLabel:{fontSize:9}},
        yAxis:{type:horiz?'category':'value',data:horiz?d.categories:null,axisLabel:{fontSize:9}},
        series:d.series.map(function(s,i){return{name:s.name,type:'bar',data:s.values,stack:d.stacked?'t':null,itemStyle:{color:C[i%8]},barMaxWidth:35}})};
    }
    chart.setOption(o);
    window.addEventListener('resize',function(){chart.resize()});
  });
});
</script>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={canvas_w:.0f}">
<title>PPTX Replica</title>
{echarts_cdn}
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#2d2d2d;display:flex;flex-direction:column;align-items:center;padding:24px 0;gap:16px;font-family:Arial,'Microsoft YaHei','PingFang SC',sans-serif}}
.slide{{width:{canvas_w:.0f}px;height:{canvas_h:.0f}px;background:#fff;position:relative;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.5);flex-shrink:0}}
.slide img{{display:block}}
.pg{{position:absolute;bottom:4px;right:8px;font-size:8px;color:#999}}
@media print{{body{{background:#fff;padding:0;gap:0}}.slide{{box-shadow:none;page-break-after:always}}.pg{{display:none}}}}
</style>
</head>
<body>
{slides_html}
{chart_js}
</body>
</html>"""


# ═══════════════════════════════════════════
# Main entry
# ═══════════════════════════════════════════

def pptx_to_html(pptx_path: str, output_path: str = None,
                 slide_range: Optional[Tuple[int, int]] = None) -> str:
    """Convert PPTX to HTML."""
    prs = Presentation(pptx_path)
    canvas_w = emu_to_px(prs.slide_width)
    canvas_h = emu_to_px(prs.slide_height)
    print(f"[INFO] Canvas: {canvas_w:.0f} x {canvas_h:.0f} px")

    # Theme colors
    theme = ThemeColors(pptx_path)
    print(f"[INFO] Theme colors: {len(theme.colors)} resolved")
    for k, v in theme.colors.items():
        print(f"  {k}: {v}")

    # Slides
    slides = list(prs.slides)
    total = len(slides)
    start = 1
    if slide_range:
        start, end = slide_range
        slides = slides[start - 1:end]
        print(f"[INFO] Slides {start}-{end} of {total}")
    else:
        print(f"[INFO] All {total} slides")

    has_charts = False
    all_html = []
    for i, slide in enumerate(slides, start):
        s_html = render_slide(slide, i, theme, canvas_w, canvas_h)
        if 'data-chart=' in s_html:
            has_charts = True
        all_html.append(s_html)
        if i % 20 == 0:
            print(f"  ... rendered {i}/{total}")

    final = build_html(canvas_w, canvas_h, "\n".join(all_html), has_charts)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(final, encoding="utf-8")
        kb = len(final.encode()) / 1024
        print(f"[OK] {output_path} ({kb:.0f} KB)")

    return final


def main():
    parser = argparse.ArgumentParser(description="PPTX → HTML pixel-accurate replica (v2)")
    parser.add_argument("input", help="Input .pptx file")
    parser.add_argument("-o", "--output", help="Output .html file")
    parser.add_argument("--slides", help="Slide range: '1-10' or '5'")
    args = parser.parse_args()

    output = args.output or str(Path(args.input).with_suffix(".html"))
    sr = None
    if args.slides:
        if '-' in args.slides:
            a, b = args.slides.split('-')
            sr = (int(a), int(b))
        else:
            n = int(args.slides)
            sr = (n, n)

    pptx_to_html(args.input, output, sr)


if __name__ == "__main__":
    main()
