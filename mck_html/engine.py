"""MckHtmlEngine — The HTML presentation engine with high-level layout methods.

Usage:
    eng = MckHtmlEngine(total_slides=30)
    eng.cover(title='Title', subtitle='Sub')
    eng.toc(items=[('1','Topic','Desc'), ...])
    eng.save('output/deck.html')

Every layout method creates one slide and auto-increments page numbers.
API is identical to MckEngine (PPT version) — same method names, same parameters.
Output is a self-contained HTML file instead of .pptx.
"""
import os
import math

from .constants import *
from .core import (
    get_base_css, get_presentation_js,
    esc, div, span, _style,
    make_slide, add_action_title, add_source, add_page_number,
    add_bottom_bar, add_oval, add_hline, add_rect,
    add_image_placeholder, add_text,
    make_donut_svg, make_pie_svg, make_gauge_svg, make_harvey_ball_html,
)


class MckHtmlEngine:
    """HTML Presentation engine with high-level layout methods.
    API-compatible with MckEngine (PPT version)."""

    def __init__(self, total_slides=30):
        self._slides = []
        self._page = 0
        self.total = total_slides
        self._cover_title = ''

    # ─── internal ──────────────────────────────
    def _ns(self):
        """Increment page counter, return current page number."""
        self._page += 1
        return self._page

    def _add_slide(self, html):
        """Store a completed slide HTML.
        Note: html is already wrapped by make_slide. We post-process
        to inject page number badge into the wrapper."""
        self._slides.append(html)

    def _footer(self, source=None):
        """Generate source + page number HTML."""
        parts = []
        if source:
            parts.append(add_source(source))
        parts.append(add_page_number(self._page, self.total))
        return '\n'.join(parts)

    def _abs(self, left, top, width, height, content='', bg='transparent',
             extra_style='', cls=''):
        """Create an absolutely positioned div."""
        cls_attr = f' class="{cls}"' if cls else ''
        return f'<div{cls_attr} style="position:absolute; left:{left}px; top:{top}px; width:{width}px; height:{height}px; background:{bg}; {extra_style}">{content}</div>'

    def _text(self, left, top, width, height, text, font_size=BODY_SIZE,
              color=DARK_GRAY, bold=False, align='left', font_family=None,
              valign='top', line_height=1.35):
        """Absolutely positioned text box."""
        if font_family is None:
            font_family = FONT_STACK_BODY
        weight = 'bold' if bold else 'normal'
        lines = text if isinstance(text, list) else [text]
        content = '<br>'.join(esc(str(l)) for l in lines)
        va_css = ''
        if valign == 'middle':
            va_css = 'display:flex; align-items:center; justify-content:' + ('center' if align == 'center' else 'flex-start' if align == 'left' else 'flex-end') + ';'
        elif valign == 'bottom':
            va_css = 'display:flex; align-items:flex-end;'
        return f'<div style="position:absolute; left:{left}px; top:{top}px; width:{width}px; height:{height}px; font-size:{font_size}px; color:{color}; font-weight:{weight}; font-family:{font_family}; text-align:{align}; line-height:{line_height}; overflow:hidden; {va_css}">{content}</div>'

    def _oval(self, left, top, letter, bg=NAVY, fg=WHITE, size=45):
        """Absolutely positioned oval label."""
        return f'<div style="position:absolute; left:{left}px; top:{top}px; width:{size}px; height:{size}px; border-radius:50%; background:{bg}; color:{fg}; display:flex; align-items:center; justify-content:center; font-size:{max(size//3,12)}px; font-weight:bold; font-family:Arial,sans-serif;">{esc(str(letter))}</div>'

    def _hline(self, left, top, width, color=BLACK, thickness=0.5):
        """Absolutely positioned horizontal line."""
        return f'<div style="position:absolute; left:{left}px; top:{top}px; width:{width}px; height:{thickness}px; background:{color}"></div>'

    # ═══════════════════════════════════════════
    # STRUCTURE LAYOUTS
    # ═══════════════════════════════════════════

    def cover(self, title, subtitle='', author='', date=''):
        """Cover Slide — title, subtitle, author, date, accent line."""
        # Store title for toolbar / <title> tag (collapse newlines to space)
        self._cover_title = title.replace('\n', ' ') if isinstance(title, str) else str(title)
        p = self._ns()
        parts = []
        # Top accent line
        parts.append(self._abs(0, 0, SLIDE_WIDTH, 5, bg=NAVY))
        # Title
        lines = title.split('\n') if isinstance(title, str) else [title]
        n_lines = len(lines) if isinstance(lines, list) else 1
        title_h = 80 + 65 * max(n_lines - 1, 0)
        parts.append(self._text(100, 120, 1100, title_h, title,
                                font_size=COVER_TITLE_SIZE, color=NAVY, bold=True,
                                font_family=FONT_STACK_HEADER))
        sub_y = 120 + title_h + 30
        if subtitle:
            parts.append(self._text(100, sub_y, 1100, 80, subtitle,
                                    font_size=SUB_HEADER_SIZE, color=DARK_GRAY))
            sub_y += 100
        else:
            sub_y += 20
        y = sub_y + 30
        if author:
            parts.append(self._text(100, y, 1100, 50, author,
                                    font_size=BODY_SIZE, color=MED_GRAY))
            y += 80
        if date:
            parts.append(self._text(100, y, 1100, 50, date,
                                    font_size=BODY_SIZE, color=MED_GRAY))
        # Bottom accent line
        parts.append(self._hline(100, 680, 400, NAVY, 2))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def section_divider(self, section_label, title, subtitle=''):
        """Section Divider — navy left bar, large title."""
        p = self._ns()
        parts = []
        parts.append(self._abs(0, 0, 60, SLIDE_HEIGHT, bg=NAVY))
        parts.append(self._text(120, 200, 1000, 80, section_label,
                                font_size=SUB_HEADER_SIZE, color=MED_GRAY,
                                font_family=FONT_STACK_HEADER))
        parts.append(self._text(120, 280, 1000, 120, title,
                                font_size=SECTION_TITLE_SIZE, color=NAVY, bold=True,
                                font_family=FONT_STACK_HEADER))
        if subtitle:
            parts.append(self._text(120, 420, 1000, 60, subtitle,
                                    font_size=BODY_SIZE, color=DARK_GRAY))
        parts.append(add_page_number(p, self.total))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def toc(self, title='目录', items=None, source=''):
        """Table of Contents — numbered items with descriptions."""
        p = self._ns()
        parts = [add_action_title(title)]
        iy = 150
        for num, item_title, desc in (items or []):
            parts.append(self._oval(LM, iy, str(num)))
            parts.append(self._text(LM + 70, iy, 400, 40, item_title,
                                    font_size=SUB_HEADER_SIZE, color=NAVY, bold=True))
            parts.append(self._text(550, iy + 5, 650, 40, desc,
                                    font_size=BODY_SIZE, color=MED_GRAY))
            iy += 70
            parts.append(self._hline(LM, iy, CW, LINE_GRAY))
            iy += 30
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def closing(self, title, message='', source_text=''):
        """Closing / Thank You slide."""
        p = self._ns()
        parts = []
        parts.append(self._abs(0, 0, SLIDE_WIDTH, 5, bg=NAVY))
        parts.append(self._text(150, 200, 1030, 100, title,
                                font_size=SECTION_TITLE_SIZE, color=NAVY, bold=True,
                                font_family=FONT_STACK_HEADER, align='center'))
        parts.append(self._hline(550, 330, 230, NAVY, 1.5))
        if message:
            parts.append(self._text(150, 380, 1030, 200, message,
                                    font_size=SUB_HEADER_SIZE, color=DARK_GRAY,
                                    align='center'))
        parts.append(self._hline(LM, 680, CW, NAVY, 2))
        if source_text:
            parts.append(self._text(100, 620, 1100, 40, source_text,
                                    font_size=SMALL_SIZE, color=MED_GRAY, align='center'))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def appendix_title(self, title, subtitle=''):
        """Appendix Title — centered title with accent lines."""
        p = self._ns()
        parts = []
        parts.append(self._abs(0, 0, SLIDE_WIDTH, 5, bg=NAVY))
        parts.append(self._text(100, 250, 1130, 100, title,
                                font_size=36, color=NAVY, bold=True,
                                font_family=FONT_STACK_HEADER, align='center'))
        parts.append(self._hline(550, 380, 230, NAVY, 1.5))
        if subtitle:
            parts.append(self._text(100, 420, 1130, 50, subtitle,
                                    font_size=BODY_SIZE, color=MED_GRAY, align='center'))
        parts.append(add_page_number(p, self.total))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # DATA LAYOUTS
    # ═══════════════════════════════════════════

    def big_number(self, title, number, unit='', description='',
                   detail_items=None, source='', bottom_bar=None):
        """Big Number — large stat with context."""
        p = self._ns()
        parts = [add_action_title(title)]
        # Navy big number box
        box_w = 350
        parts.append(self._abs(LM, CONTENT_TOP + 10, box_w, 180, bg=NAVY))
        parts.append(self._text(LM + 20, CONTENT_TOP + 20, box_w - 40, 80,
                                str(number), font_size=COVER_TITLE_SIZE, color=WHITE,
                                bold=True, font_family=FONT_STACK_HEADER, align='center'))
        if unit:
            parts.append(self._text(LM + 20, CONTENT_TOP + 100, box_w - 40, 70,
                                    unit, font_size=SMALL_SIZE, color=WHITE, align='center'))
        if description:
            desc = description if isinstance(description, list) else [description]
            parts.append(self._text(500, CONTENT_TOP + 20, 750, 250, desc,
                                    font_size=BODY_SIZE))
        if detail_items:
            parts.append(self._abs(LM, 450, CW, 220, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 460, 180, 40, '详细说明',
                                    font_size=BODY_SIZE, color=NAVY, bold=True))
            parts.append(self._text(LM + 30, 510, CW - 60, 140, detail_items,
                                    font_size=BODY_SIZE))
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def two_stat(self, title, stats, detail_items=None, source=''):
        """Two-Stat Comparison — two big numbers side by side."""
        p = self._ns()
        parts = [add_action_title(title)]
        sw_stat = 550
        sg = 73
        for i, (big, label, is_navy) in enumerate(stats):
            sx = LM + (sw_stat + sg) * i
            fill = NAVY if is_navy else BG_GRAY
            bc = WHITE if is_navy else NAVY
            sc = WHITE if is_navy else DARK_GRAY
            parts.append(self._abs(sx, 150, sw_stat, 200, bg=fill))
            parts.append(self._text(sx + 30, 160, sw_stat - 60, 90,
                                    str(big), font_size=COVER_TITLE_SIZE, color=bc,
                                    bold=True, font_family=FONT_STACK_HEADER, align='center'))
            parts.append(self._text(sx + 30, 260, sw_stat - 60, 50,
                                    label, font_size=BODY_SIZE, color=sc, align='center'))
        if detail_items:
            parts.append(self._text(LM, 400, CW, 250, detail_items, font_size=BODY_SIZE))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def three_stat(self, title, stats, detail_items=None, source=''):
        """Three-Stat — three big numbers in a row."""
        p = self._ns()
        parts = [add_action_title(title)]
        sw = 350
        sg = int((CW - sw * 3) / 2)
        for i, (big, label, is_navy) in enumerate(stats):
            sx = LM + (sw + sg) * i
            fill = NAVY if is_navy else BG_GRAY
            bc = WHITE if is_navy else NAVY
            sc = WHITE if is_navy else DARK_GRAY
            parts.append(self._abs(sx, 140, sw, 180, bg=fill))
            parts.append(self._text(sx + 20, 150, sw - 40, 70,
                                    str(big), font_size=SECTION_TITLE_SIZE, color=bc,
                                    bold=True, font_family=FONT_STACK_HEADER, align='center'))
            parts.append(self._text(sx + 20, 225, sw - 40, 60,
                                    label, font_size=SMALL_SIZE, color=sc, align='center'))
        if detail_items:
            parts.append(self._text(LM, 380, CW, 250, detail_items, font_size=BODY_SIZE))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def metric_cards(self, title, cards, source=''):
        """Metric Cards — 3-4 accent-colored cards."""
        p = self._ns()
        parts = [add_action_title(title)]
        n = len(cards)
        card_w = int((CW - 20 * (n - 1)) / n)
        card_g = 20
        for i, card in enumerate(cards):
            if len(card) == 5:
                letter, ctitle, desc, accent, light = card
            else:
                letter, ctitle, desc = card[:3]
                accent, light = ACCENT_PAIRS[i % len(ACCENT_PAIRS)]
            cx = LM + (card_w + card_g) * i
            parts.append(self._abs(cx, CONTENT_TOP + 10, card_w, 480, bg=light))
            parts.append(self._abs(cx, CONTENT_TOP + 10, card_w, 6, bg=accent))
            parts.append(self._oval(cx + card_w // 2 - 22, CONTENT_TOP + 30, str(letter), bg=accent))
            parts.append(self._text(cx + 20, CONTENT_TOP + 90, card_w - 40, 40,
                                    ctitle, font_size=SUB_HEADER_SIZE, color=accent,
                                    bold=True, align='center'))
            parts.append(self._hline(cx + 40, CONTENT_TOP + 140, card_w - 80, LINE_GRAY))
            desc_items = desc if isinstance(desc, list) else [desc]
            parts.append(self._text(cx + 20, CONTENT_TOP + 160, card_w - 40, 250,
                                    desc_items, font_size=BODY_SIZE, align='center'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def data_table(self, title, headers, rows, col_widths=None, source='',
                   bottom_bar=None):
        """Data Table — header row + data rows with separators.
        Auto-downsizes font when rows are dense."""
        p = self._ns()
        parts = [add_action_title(title)]
        n = len(headers)
        if col_widths is None:
            col_widths = [int(CW / n)] * n
        hdr_y = CONTENT_TOP + 10
        cx = LM
        for hdr, cw in zip(headers, col_widths):
            parts.append(self._text(cx, hdr_y, cw, 40, hdr,
                                    font_size=BODY_SIZE, color=MED_GRAY, bold=True))
            cx += cw
        parts.append(self._hline(LM, hdr_y + 45, CW, BLACK, 1))
        row_y = hdr_y + 55
        avail_h = (SOURCE_Y - 10) - row_y
        row_h = min(95, int(avail_h / max(len(rows), 1)))
        # Font downgrade: BODY → SMALL → 13px based on row density
        if row_h < 35:
            cell_fs = 13
        elif row_h < 50:
            cell_fs = SMALL_SIZE
        else:
            cell_fs = SMALL_SIZE
        for ri, row in enumerate(rows):
            cx = LM
            for val, cw in zip(row, col_widths):
                parts.append(self._text(cx, row_y, cw, row_h, val, font_size=cell_fs))
                cx += cw
            row_y += row_h
            parts.append(self._hline(LM, row_y, CW, LINE_GRAY))
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def table_insight(self, title, headers, rows, insights,
                      col_widths=None, insight_title='启示：',
                      source='', bottom_bar=None):
        """Table+Insight — left data table + right insight panel."""
        p = self._ns()
        parts = [add_action_title(title)]
        table_w = 720
        chevron_zone = 70
        insight_w = CW - table_w - chevron_zone
        n_cols = len(headers)
        if col_widths is None:
            col_widths = [int(table_w / n_cols)] * n_cols
        # Table headers
        hdr_y = CONTENT_TOP + 10
        cx = LM
        for hdr, cw in zip(headers, col_widths):
            parts.append(self._text(cx, hdr_y, cw, 40, hdr,
                                    font_size=BODY_SIZE, color=BLACK, bold=True))
            cx += cw
        parts.append(self._hline(LM, hdr_y + 45, table_w, BLACK, 1))
        # Table rows — with font downgrade for dense tables
        row_start = hdr_y + 55
        avail_h = (BOTTOM_BAR_Y - 15 if bottom_bar else SOURCE_Y - 10) - row_start
        n_rows = len(rows)
        row_h = min(155, int(avail_h / max(n_rows, 1)))
        # Font downgrade when rows are dense
        if row_h < 45:
            fs_first = BODY_SIZE
            fs_rest = SMALL_SIZE
        else:
            fs_first = SUB_HEADER_SIZE
            fs_rest = BODY_SIZE
        for ri, row in enumerate(rows):
            ry = row_start + row_h * ri
            cx = LM
            for ci, (val, cw) in enumerate(zip(row, col_widths)):
                fb = True if ci == 0 else False
                fs = fs_first if ci == 0 else fs_rest
                fc = BLACK if ci == 0 else DARK_GRAY
                parts.append(self._text(cx, ry, cw, row_h, val, font_size=fs,
                                        color=fc, bold=fb, valign='middle'))
                cx += cw
            parts.append(self._hline(LM, ry + row_h, table_w, LINE_GRAY))
        # Chevron
        chev_x = LM + table_w
        content_mid = CONTENT_TOP + int(avail_h * 0.42)
        parts.append(self._text(chev_x, content_mid, chevron_zone, 50,
                                '▶', font_size=24, color=DARK_GRAY, align='center',
                                valign='middle'))
        # Insight panel
        insight_x = LM + table_w + chevron_zone
        insight_top = CONTENT_TOP + 10
        insight_bottom = (BOTTOM_BAR_Y - 15 if bottom_bar else SOURCE_Y - 10) + 5
        parts.append(self._abs(insight_x - 10, insight_top - 10,
                               insight_w + 20, insight_bottom - insight_top + 20, bg=BG_GRAY))
        parts.append(self._text(insight_x, insight_top + 10, insight_w, 45,
                                insight_title, font_size=SUB_HEADER_SIZE, color=BLACK, bold=True))
        bullet_y = insight_top + 65
        for ii, ins in enumerate(insights):
            parts.append(self._text(insight_x, bullet_y, 25, 30, '•',
                                    font_size=BODY_SIZE, color=BLACK, bold=True))
            parts.append(self._text(insight_x + 30, bullet_y, insight_w - 35, 60,
                                    ins, font_size=BODY_SIZE, color=DARK_GRAY))
            bullet_y += 80
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def scorecard(self, title, items, source=''):
        """Scorecard — items with progress bars."""
        p = self._ns()
        parts = [add_action_title(title)]
        headers = ['技术领域', '评分', '成熟度']
        parts.append(self._text(LM, CONTENT_TOP + 10, 400, 40, headers[0],
                                font_size=BODY_SIZE, color=MED_GRAY, bold=True))
        parts.append(self._text(500, CONTENT_TOP + 10, 150, 40, headers[1],
                                font_size=BODY_SIZE, color=MED_GRAY, bold=True))
        parts.append(self._text(700, CONTENT_TOP + 10, 550, 40, headers[2],
                                font_size=BODY_SIZE, color=MED_GRAY, bold=True))
        parts.append(self._hline(LM, CONTENT_TOP + 55, CW, BLACK, 1))
        bar_max = 500
        ry = CONTENT_TOP + 70
        for name, score, pct in items:
            parts.append(self._text(LM, ry, 400, 50, name, font_size=BODY_SIZE))
            parts.append(self._text(500, ry, 150, 50, score,
                                    font_size=BODY_SIZE, color=NAVY, bold=True))
            parts.append(self._abs(700, ry + 10, bar_max, 30, bg=BG_GRAY))
            bc = NAVY if pct >= 0.7 else ACCENT_ORANGE if pct >= 0.5 else ACCENT_RED
            parts.append(self._abs(700, ry + 10, int(bar_max * pct), 30, bg=bc))
            ry += 55
            parts.append(self._hline(LM, ry, CW, LINE_GRAY))
            ry += 10
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # FRAMEWORK LAYOUTS
    # ═══════════════════════════════════════════

    def matrix_2x2(self, title, quadrants, axis_labels=None, source='',
                   bottom_bar=None):
        """2×2 Matrix — four quadrants."""
        p = self._ns()
        parts = [add_action_title(title)]
        grid_l = LM + 180
        grid_t = 150
        cell_w = 450
        cell_h = 220
        if axis_labels:
            parts.append(self._text(LM, grid_t + cell_h - 30, 160, 80,
                                    axis_labels[1], font_size=BODY_SIZE, color=NAVY,
                                    bold=True, align='center'))
            parts.append(self._text(grid_l + cell_w - 50, grid_t + 2 * cell_h + 15,
                                    350, 40, axis_labels[0],
                                    font_size=BODY_SIZE, color=NAVY, bold=True, align='center'))
        for qi, (label, bg, desc) in enumerate(quadrants):
            row, col = qi // 2, qi % 2
            qx = grid_l + col * (cell_w + 15)
            qy = grid_t + row * (cell_h + 15)
            parts.append(self._abs(qx, qy, cell_w, cell_h, bg=bg))
            parts.append(self._text(qx + 20, qy + 10, cell_w - 40, 35,
                                    label, font_size=BODY_SIZE, color=NAVY, bold=True))
            parts.append(self._text(qx + 20, qy + 50, cell_w - 40, cell_h - 60,
                                    desc, font_size=SMALL_SIZE, color=DARK_GRAY))
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def pyramid(self, title, levels, source='', bottom_bar=None):
        """Pyramid — top-down widening layers."""
        p = self._ns()
        parts = [add_action_title(title)]
        for i, (label, desc, w) in enumerate(levels):
            w_px = int(w * 100)
            lx = int(SLIDE_WIDTH / 2 - w_px / 2)
            ly = 150 + 115 * i
            h = 90
            fill = NAVY if i == 0 else BG_GRAY
            tc = WHITE if i == 0 else NAVY
            dc = WHITE if i == 0 else DARK_GRAY
            parts.append(self._abs(lx, ly, w_px, h, bg=fill))
            parts.append(self._text(lx + 20, ly + 5, 250, 35,
                                    label, font_size=BODY_SIZE, color=tc, bold=True))
            parts.append(self._text(lx + 280, ly + 5, w_px - 300, 80,
                                    desc, font_size=SMALL_SIZE, color=dc))
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def process_chevron(self, title, steps, source='', bottom_bar=None):
        """Process Chevron — horizontal step flow with arrows."""
        p = self._ns()
        parts = [add_action_title(title)]
        n = len(steps)
        step_w = 260
        gap = int((CW - step_w * n) / max(n - 1, 1))
        for i, (label, stitle, desc) in enumerate(steps):
            sx = LM + (step_w + gap) * i
            is_last = (i == n - 1)
            fill = NAVY if is_last else BG_GRAY
            tc = WHITE if is_last else NAVY
            parts.append(self._abs(sx, 150, step_w, 100, bg=fill))
            obg = WHITE if is_last else NAVY
            ofg = NAVY if is_last else WHITE
            parts.append(self._oval(sx + 10, 155, str(label), bg=obg, fg=ofg))
            parts.append(self._text(sx + 65, 155, step_w - 80, 90,
                                    stitle, font_size=SUB_HEADER_SIZE, color=tc,
                                    bold=True, valign='middle'))
            parts.append(self._text(sx + 10, 270, step_w - 20, 200,
                                    desc, font_size=BODY_SIZE, align='center'))
            if i < n - 1:
                parts.append(self._text(sx + step_w + 5, 170, gap - 10, 50,
                                        '→', font_size=24, color=NAVY, bold=True, align='center'))
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def temple(self, title, roof_text, pillar_names, foundation_text,
               pillar_colors=None, source=''):
        """Temple / House Framework — roof + pillars + foundation."""
        p = self._ns()
        parts = [add_action_title(title)]
        parts.append(self._abs(LM, CONTENT_TOP + 10, CW, 80, bg=NAVY))
        parts.append(self._text(LM + 30, CONTENT_TOP + 10, CW - 60, 80,
                                roof_text, font_size=SUB_HEADER_SIZE, color=WHITE,
                                bold=True, valign='middle', align='center'))
        n = len(pillar_names)
        if pillar_colors is None:
            pillar_colors = [pair[0] for pair in ACCENT_PAIRS[:n]]
        ppw = int((CW - 20 * (n - 1)) / n)
        ppg = 20
        for i, (name, color) in enumerate(zip(pillar_names, pillar_colors)):
            ppx = LM + (ppw + ppg) * i
            parts.append(self._abs(ppx, 250, ppw, 280, bg=BG_GRAY))
            parts.append(self._abs(ppx, 250, ppw, 6, bg=color))
            parts.append(self._text(ppx + 15, 270, ppw - 30, 80,
                                    name, font_size=BODY_SIZE, color=color,
                                    bold=True, align='center'))
        parts.append(self._abs(LM, 550, CW, 80, bg=NAVY))
        parts.append(self._text(LM + 30, 550, CW - 60, 80,
                                foundation_text, font_size=BODY_SIZE, color=WHITE,
                                bold=True, valign='middle', align='center'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # COMPARISON LAYOUTS
    # ═══════════════════════════════════════════

    def side_by_side(self, title, options, source=''):
        """Side-by-Side Comparison — two columns with navy headers."""
        p = self._ns()
        parts = [add_action_title(title)]
        cw_col = 550
        cg = 73
        for i, (otitle, pts) in enumerate(options):
            cx = LM + (cw_col + cg) * i
            parts.append(self._abs(cx, CONTENT_TOP + 10, cw_col, 60, bg=NAVY))
            parts.append(self._text(cx + 15, CONTENT_TOP + 10, cw_col - 30, 60,
                                    otitle, font_size=SUB_HEADER_SIZE, color=WHITE,
                                    bold=True, valign='middle', align='center'))
            parts.append(self._abs(cx, CONTENT_TOP + 70, cw_col, 420, bg=BG_GRAY))
            pts_list = pts if isinstance(pts, list) else [pts]
            parts.append(self._text(cx + 30, CONTENT_TOP + 90, cw_col - 60, 380,
                                    pts_list, font_size=BODY_SIZE))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def before_after(self, title, before_title, before_points,
                     after_title, after_points, source='',
                     corner_label='', bottom_bar=None,
                     left_summary='', right_summary='',
                     right_summary_color=None):
        """Before/After — vertical divider with arrow."""
        p = self._ns()
        parts = [add_action_title(title)]
        if right_summary_color is None:
            right_summary_color = ACCENT_RED
        ct = CONTENT_TOP + 15
        left_x = LM
        left_w = 550
        right_x = LM + 623
        right_w = 550
        line_x = left_x + left_w + 36
        # Vertical divider
        parts.append(self._abs(line_x, ct, 1, 480, bg=BLACK))
        # Circle with >
        parts.append(f'<div style="position:absolute; left:{line_x - 25}px; top:{ct + 200}px; width:50px; height:50px; border-radius:50%; background:{BLACK}; color:{WHITE}; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:bold;">&gt;</div>')
        # Left
        parts.append(self._text(left_x, ct, left_w, 50, before_title,
                                font_size=EMPHASIS_SIZE, color=BLACK, bold=True))
        if isinstance(before_points, list) and before_points and isinstance(before_points[0], str):
            parts.append(self._text(left_x, ct + 60, left_w, 400, before_points,
                                    font_size=SMALL_SIZE))
        elif isinstance(before_points, list):
            parts.append(self._text(left_x, ct + 60, left_w, 400, before_points,
                                    font_size=SMALL_SIZE))
        if left_summary:
            parts.append(self._text(left_x, 580, left_w, 35, left_summary,
                                    font_size=SMALL_SIZE, color=DARK_GRAY, bold=True))
        # Right
        parts.append(self._text(right_x, ct, right_w, 50, after_title,
                                font_size=EMPHASIS_SIZE, color=BLACK, bold=True))
        if isinstance(after_points, list) and after_points and isinstance(after_points[0], str):
            parts.append(self._text(right_x, ct + 60, right_w, 400, after_points,
                                    font_size=SMALL_SIZE))
        elif isinstance(after_points, list):
            parts.append(self._text(right_x, ct + 60, right_w, 400, after_points,
                                    font_size=SMALL_SIZE))
        if right_summary:
            parts.append(self._text(right_x, 580, right_w, 35, right_summary,
                                    font_size=SMALL_SIZE, color=right_summary_color, bold=True))
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def swot(self, title, quadrants, source=''):
        """SWOT Analysis — 2×2 colored grid."""
        p = self._ns()
        parts = [add_action_title(title)]
        cell_w = int(CW / 2 - 10)
        cell_h = 230
        grid_t = 120
        for qi, (label, accent, bg, pts) in enumerate(quadrants):
            row, col = qi // 2, qi % 2
            qx = LM + col * (cell_w + 15)
            qy = grid_t + row * (cell_h + 10)
            parts.append(self._abs(qx, qy, cell_w, cell_h, bg=bg))
            parts.append(self._abs(qx, qy, cell_w, 6, bg=accent))
            parts.append(self._text(qx + 20, qy + 15, cell_w - 40, 35,
                                    label, font_size=EMPHASIS_SIZE, color=accent, bold=True))
            pts_list = pts if isinstance(pts, list) else [pts]
            parts.append(self._text(qx + 20, qy + 55, cell_w - 40, cell_h - 70,
                                    pts_list, font_size=BODY_SIZE, color=DARK_GRAY))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # NARRATIVE LAYOUTS
    # ═══════════════════════════════════════════

    def executive_summary(self, title, headline, items, source=''):
        """Executive Summary — navy headline + numbered items."""
        p = self._ns()
        parts = [add_action_title(title)]
        parts.append(self._abs(LM, CONTENT_TOP + 10, CW, 100, bg=NAVY))
        parts.append(self._text(LM + 30, CONTENT_TOP + 10, CW - 60, 100,
                                headline, font_size=SUB_HEADER_SIZE, color=WHITE,
                                bold=True, valign='middle'))
        iy = CONTENT_TOP + 150
        avail_h = SOURCE_Y - 20 - iy
        item_h = min(75, int(avail_h / max(len(items), 1)))
        for num, ititle, desc in items:
            parts.append(self._oval(LM, iy, str(num)))
            parts.append(self._text(LM + 60, iy, 350, 50, ititle,
                                    font_size=BODY_SIZE, color=NAVY, bold=True))
            parts.append(self._text(500, iy, 750, 50, desc, font_size=BODY_SIZE))
            iy += item_h
            parts.append(self._hline(LM, iy, CW, LINE_GRAY))
            iy += 15
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def key_takeaway(self, title, left_text, takeaways, source=''):
        """Key Takeaway — left analysis + right gray panel."""
        p = self._ns()
        parts = [add_action_title(title)]
        left_w = 750
        parts.append(self._text(LM, CONTENT_TOP + 10, left_w, 40, '协同机制分析',
                                font_size=SUB_HEADER_SIZE, color=NAVY, bold=True))
        parts.append(self._hline(LM, CONTENT_TOP + 60, left_w, LINE_GRAY))
        parts.append(self._text(LM, CONTENT_TOP + 80, left_w, 400,
                                left_text, font_size=BODY_SIZE))
        tk_x = 900
        tk_w = 350
        parts.append(self._abs(tk_x, CONTENT_TOP + 10, tk_w, 520, bg=BG_GRAY))
        parts.append(self._text(tk_x + 20, CONTENT_TOP + 30, tk_w - 40, 40,
                                'Key Takeaways', font_size=BODY_SIZE, color=NAVY, bold=True))
        parts.append(self._hline(tk_x + 20, CONTENT_TOP + 80, tk_w - 40, LINE_GRAY))
        parts.append(self._text(tk_x + 20, CONTENT_TOP + 100, tk_w - 40, 400,
                                takeaways, font_size=BODY_SIZE))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def four_column(self, title, items, source=''):
        """Four-Column Overview — vertical cards."""
        p = self._ns()
        parts = [add_action_title(title)]
        n = len(items)
        col_w = int((CW - 20 * (n - 1)) / n)
        col_g = 20
        for i, (num, ctitle, desc) in enumerate(items):
            cx = LM + (col_w + col_g) * i
            parts.append(self._abs(cx, CONTENT_TOP + 10, col_w, 520, bg=BG_GRAY))
            parts.append(self._oval(cx + col_w // 2 - 22, CONTENT_TOP + 25, str(num)))
            parts.append(self._text(cx + 15, CONTENT_TOP + 90, col_w - 30, 50,
                                    ctitle, font_size=SUB_HEADER_SIZE, color=NAVY,
                                    bold=True, align='center'))
            parts.append(self._hline(cx + 30, CONTENT_TOP + 150, col_w - 60, LINE_GRAY))
            desc_items = desc if isinstance(desc, list) else [desc]
            parts.append(self._text(cx + 15, CONTENT_TOP + 165, col_w - 30, 340,
                                    desc_items, font_size=BODY_SIZE, align='center'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def quote(self, quote_text, attribution=''):
        """Quote Slide — centered quote with accent lines."""
        p = self._ns()
        parts = []
        parts.append(self._abs(0, 0, SLIDE_WIDTH, 5, bg=NAVY))
        parts.append(self._hline(550, 200, 230, NAVY, 1.5))
        parts.append(self._text(150, 250, 1030, 250, quote_text,
                                font_size=24, color=DARK_GRAY, align='center'))
        parts.append(self._hline(550, 530, 230, NAVY, 1.5))
        if attribution:
            parts.append(self._text(150, 560, 1030, 50, attribution,
                                    font_size=BODY_SIZE, color=MED_GRAY, align='center'))
        parts.append(add_page_number(p, self.total))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def two_column_text(self, title, columns, source=''):
        """Two-Column Text — lettered columns with bullet lists."""
        p = self._ns()
        parts = [add_action_title(title)]
        cw_col = 550
        cg = 73
        for i, (letter, ctitle, points) in enumerate(columns):
            cx = LM + (cw_col + cg) * i
            parts.append(self._oval(cx, 150, letter))
            parts.append(self._text(cx + 60, 150, cw_col - 60, 40,
                                    ctitle, font_size=SUB_HEADER_SIZE, color=NAVY, bold=True))
            parts.append(self._hline(cx, 200, cw_col, LINE_GRAY))
            pts = points if isinstance(points, list) else [points]
            parts.append(self._text(cx, 220, cw_col, 400, pts, font_size=BODY_SIZE))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def pros_cons(self, title, pros_title, pros, cons_title, cons,
                  conclusion=None, source=''):
        """Pros/Cons — two-column layout."""
        p = self._ns()
        parts = [add_action_title(title)]
        hw = 550
        parts.append(self._text(LM, 150, hw, 40, pros_title,
                                font_size=SUB_HEADER_SIZE, color=NAVY, bold=True))
        parts.append(self._hline(LM, 200, hw, NAVY))
        parts.append(self._text(LM, 220, hw, 250, pros, font_size=BODY_SIZE))
        cx = LM + hw + 73
        parts.append(self._text(cx, 150, hw, 40, cons_title,
                                font_size=SUB_HEADER_SIZE, color=DARK_GRAY, bold=True))
        parts.append(self._hline(cx, 200, hw, DARK_GRAY))
        parts.append(self._text(cx, 220, hw, 250, cons, font_size=BODY_SIZE))
        if conclusion:
            label, text = conclusion
            parts.append(self._abs(LM, 520, CW, 150, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 530, 150, 40, label,
                                    font_size=BODY_SIZE, color=NAVY, bold=True))
            parts.append(self._text(LM + 30, 580, CW - 60, 60, text,
                                    font_size=BODY_SIZE))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # TIMELINE & STEPS
    # ═══════════════════════════════════════════

    def timeline(self, title, milestones, source='', bottom_bar=None):
        """Timeline / Roadmap — horizontal line with milestone nodes."""
        p = self._ns()
        parts = [add_action_title(title)]
        line_w = 1070
        parts.append(self._abs(LM + 50, 300, line_w, 2, bg=LINE_GRAY))
        n = len(milestones)
        spacing = int(line_w / max(n - 1, 1))
        for i, (label, desc) in enumerate(milestones):
            mx = LM + 50 + spacing * i
            is_last = (i == n - 1)
            bg = NAVY if is_last else ACCENT_BLUE
            parts.append(self._oval(mx - 22, 277, str(i + 1), bg=bg))
            parts.append(self._text(mx - 100, 200, 200, 50, label,
                                    font_size=SUB_HEADER_SIZE, color=NAVY, bold=True, align='center'))
            parts.append(self._text(mx - 100, 350, 200, 150, desc,
                                    font_size=BODY_SIZE, align='center'))
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def vertical_steps(self, title, steps, source='', bottom_bar=None):
        """Vertical Steps — top-down numbered steps."""
        p = self._ns()
        parts = [add_action_title(title)]
        n_steps = len(steps)
        start_y = CONTENT_TOP + 10
        bottom_limit = BOTTOM_BAR_Y - 15 if bottom_bar else SOURCE_Y - 10
        avail = bottom_limit - start_y
        step_h = min(110, int(avail / max(n_steps, 1)))
        for i, (num, stitle, desc) in enumerate(steps):
            iy = start_y + step_h * i
            parts.append(self._oval(LM, iy + 5, str(num)))
            parts.append(self._text(LM + 60, iy, 300, int(step_h * 0.55),
                                    stitle, font_size=SUB_HEADER_SIZE, color=NAVY, bold=True))
            parts.append(self._text(450, iy, 800, int(step_h * 0.55),
                                    desc, font_size=BODY_SIZE))
            parts.append(self._hline(LM, iy + int(step_h * 0.75), CW, LINE_GRAY))
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # TEAM & CASE STUDY
    # ═══════════════════════════════════════════

    def meet_the_team(self, title, members, source=''):
        """Meet the Team — profile cards in a row."""
        p = self._ns()
        parts = [add_action_title(title)]
        n = len(members)
        cw_card = int((CW - 20 * (n - 1)) / n)
        cg = 20
        for i, (name, role, bio) in enumerate(members):
            cx = LM + (cw_card + cg) * i
            parts.append(self._abs(cx, 150, cw_card, 500, bg=BG_GRAY))
            parts.append(self._oval(cx + cw_card // 2 - 50, 170, name[0], size=100))
            parts.append(self._text(cx + 15, 290, cw_card - 30, 40,
                                    name, font_size=SUB_HEADER_SIZE, color=NAVY,
                                    bold=True, align='center'))
            parts.append(self._text(cx + 15, 340, cw_card - 30, 40,
                                    role, font_size=BODY_SIZE, color=MED_GRAY, align='center'))
            parts.append(self._hline(cx + 30, 390, cw_card - 60, LINE_GRAY))
            bio_items = bio.split('\n') if isinstance(bio, str) else bio
            parts.append(self._text(cx + 15, 410, cw_card - 30, 200,
                                    bio_items, font_size=BODY_SIZE, align='center'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def case_study(self, title, sections, result_box=None, source=''):
        """Case Study — S/A/R or custom sections."""
        p = self._ns()
        parts = [add_action_title(title)]
        n = len(sections)
        sw_sec = int((CW - 20 * (n - 1)) / n)
        sg = 20
        for i, (letter, stitle, desc) in enumerate(sections):
            sx = LM + (sw_sec + sg) * i
            is_last = (i == n - 1)
            fill = NAVY if is_last else BG_GRAY
            tc = WHITE if is_last else NAVY
            dc = WHITE if is_last else DARK_GRAY
            obg = WHITE if is_last else NAVY
            ofg = NAVY if is_last else WHITE
            parts.append(self._abs(sx, 150, sw_sec, 300, bg=fill))
            parts.append(self._oval(sx + 15, 165, letter, bg=obg, fg=ofg))
            parts.append(self._text(sx + 15, 220, sw_sec - 30, 80,
                                    stitle, font_size=BODY_SIZE, color=tc, bold=True, align='center'))
            desc_items = desc.split('\n') if isinstance(desc, str) else desc
            parts.append(self._text(sx + 15, 310, sw_sec - 30, 100,
                                    desc_items, font_size=BODY_SIZE, color=dc, align='center'))
        if result_box:
            label, text = result_box
            parts.append(self._abs(LM, 500, CW, 150, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 510, 150, 40, label,
                                    font_size=BODY_SIZE, color=NAVY, bold=True))
            parts.append(self._text(LM + 30, 560, CW - 60, 60, text,
                                    font_size=BODY_SIZE))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def action_items(self, title, actions, source=''):
        """Action Items — cards with timeline + owner."""
        p = self._ns()
        parts = [add_action_title(title)]
        n = len(actions)
        cw_card = int((CW - 20 * (n - 1)) / n)
        cg = 20
        for i, (atitle, timeline_str, desc, owner) in enumerate(actions):
            cx = LM + (cw_card + cg) * i
            parts.append(self._abs(cx, 150, cw_card, 60, bg=NAVY))
            parts.append(self._text(cx + 15, 150, cw_card - 30, 60,
                                    atitle, font_size=BODY_SIZE, color=WHITE, bold=True,
                                    valign='middle', align='center'))
            parts.append(self._abs(cx, 210, cw_card, 40, bg=BG_GRAY))
            parts.append(self._text(cx + 15, 210, cw_card - 30, 40,
                                    timeline_str, font_size=BODY_SIZE, color=NAVY, bold=True,
                                    valign='middle', align='center'))
            desc_items = desc.split('\n') if isinstance(desc, str) else desc
            parts.append(self._text(cx + 15, 270, cw_card - 30, 200,
                                    desc_items, font_size=BODY_SIZE, align='center'))
            parts.append(self._hline(cx + 30, 490, cw_card - 60, LINE_GRAY))
            parts.append(self._text(cx + 15, 510, cw_card - 30, 40,
                                    f'负责人：{owner}', font_size=BODY_SIZE, color=MED_GRAY, align='center'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # CHART LAYOUTS
    # ═══════════════════════════════════════════

    def donut(self, title, segments, center_label='', center_sub='',
              legend_x=None, summary=None, source=''):
        """Donut Chart — SVG ring segments."""
        p = self._ns()
        parts = [add_action_title(title)]
        svg = make_donut_svg(segments, cx=160, cy=160, outer_r=140, inner_r=85,
                             center_label=center_label, center_sub=center_sub)
        parts.append(f'<div style="position:absolute; left:{LM + 80}px; top:{CONTENT_TOP + 20}px">{svg}</div>')
        lgx = 700
        for i, (pct, color, label) in enumerate(segments):
            ly = 180 + i * 80
            parts.append(self._abs(lgx, ly + 5, 30, 30, bg=color))
            parts.append(self._text(lgx + 45, ly, 300, 40,
                                    f'{esc(label)}  {int(pct * 100)}%',
                                    font_size=EMPHASIS_SIZE, color=DARK_GRAY, bold=True))
        if summary:
            parts.append(self._abs(lgx, 530, 450, 80, bg=BG_GRAY))
            parts.append(self._text(lgx + 20, 530, 410, 80, summary,
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def pie(self, title, segments, legend_x=None, summary=None, source=''):
        """Pie Chart — SVG solid sectors."""
        p = self._ns()
        parts = [add_action_title(title)]
        svg = make_pie_svg(segments, cx=140, cy=140, radius=130)
        parts.append(f'<div style="position:absolute; left:{LM + 80}px; top:{CONTENT_TOP + 20}px">{svg}</div>')
        lgx = 700
        for i, seg in enumerate(segments):
            pct, color, label = seg[0], seg[1], seg[2]
            sub_label = seg[3] if len(seg) > 3 else ''
            ly = 180 + i * 90
            parts.append(self._abs(lgx, ly + 5, 30, 30, bg=color))
            parts.append(self._text(lgx + 45, ly, 350, 30, label,
                                    font_size=EMPHASIS_SIZE, color=DARK_GRAY, bold=True))
            if sub_label:
                parts.append(self._text(lgx + 45, ly + 30, 350, 30, sub_label,
                                        font_size=13, color=MED_GRAY))
        if summary:
            parts.append(self._abs(LM, 560, CW, 80, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 560, CW - 60, 80, summary,
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def grouped_bar(self, title, categories, series, data, max_val=None,
                    y_ticks=None, summary=None, source=''):
        """Grouped Bar Chart — vertical bars grouped by category."""
        p = self._ns()
        parts = [add_action_title(title)]
        cl = LM + 80
        cb = 500
        ct = 160
        ch = cb - ct
        cr = 1150
        cww = cr - cl
        if max_val is None:
            max_val = max(max(row) for row in data) * 1.15
        # Legend
        for ci, (sname, scolor) in enumerate(series):
            lx = LM + 800 + 180 * ci
            parts.append(self._abs(lx, 125, 20, 20, bg=scolor))
            parts.append(self._text(lx + 30, 120, 120, 30, sname,
                                    font_size=SMALL_SIZE, color=DARK_GRAY))
        # X-axis
        parts.append(self._hline(cl, cb, cww, BLACK, 0.5))
        # Bars
        nd = len(categories)
        nc = len(series)
        gw = int(cww / nd)
        bw = 35
        bgp = 5
        gbw = bw * nc + bgp * (nc - 1)
        for di, cat in enumerate(categories):
            gx = cl + gw * di + int((gw - gbw) / 2)
            for ci in range(nc):
                val = data[di][ci]
                bh = int(ch * val / max_val) if max_val else 0
                bx = gx + (bw + bgp) * ci
                by = cb - bh
                if val > 0:
                    parts.append(self._abs(bx, by, bw, bh, bg=series[ci][1]))
                    if val >= 50:
                        parts.append(self._text(bx - 5, by - 25, bw + 10, 25,
                                                str(val), font_size=FOOTNOTE_SIZE,
                                                color=DARK_GRAY, align='center'))
            parts.append(self._text(cl + gw * di, cb + 5, gw, 30,
                                    cat, font_size=BODY_SIZE, color=DARK_GRAY, align='center'))
        if summary:
            parts.append(self._abs(LM, 600, CW, 80, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 600, 150, 80, summary[0],
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
            parts.append(self._text(LM + 200, 600, CW - 230, 80, summary[1],
                                    font_size=BODY_SIZE, color=DARK_GRAY, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def horizontal_bar(self, title, items, summary=None, source=''):
        """Horizontal Bar Chart — labeled bars with percentage."""
        p = self._ns()
        parts = [add_action_title(title)]
        lbl_w = 200
        bar_x = LM + 220
        bar_mw = 750
        rh = 65
        sy = 160
        for i, (name, val, bcolor) in enumerate(items):
            ry = sy + rh * i
            bw = int(bar_mw * val / 100)
            tc = NAVY if i == 0 else DARK_GRAY
            bld = (i == 0)
            parts.append(self._text(LM, ry, lbl_w, rh, name,
                                    font_size=BODY_SIZE, color=tc, bold=bld, valign='middle'))
            parts.append(self._abs(bar_x, ry + 12, bar_mw, 40, bg=BG_GRAY))
            parts.append(self._abs(bar_x, ry + 12, bw, 40, bg=bcolor))
            parts.append(self._text(bar_x + bar_mw + 20, ry, 100, rh,
                                    f'{val}%', font_size=BODY_SIZE, color=tc, bold=bld, valign='middle'))
            if i < len(items) - 1:
                parts.append(self._hline(LM, ry + rh, bar_mw + 250, LINE_GRAY, 0.25))
        if summary:
            parts.append(self._abs(LM, 580, CW, 90, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 580, 150, 90, summary[0],
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
            parts.append(self._text(LM + 200, 580, CW - 230, 90, summary[1],
                                    font_size=BODY_SIZE, color=DARK_GRAY, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def gauge(self, title, score, benchmarks=None, source=''):
        """Gauge — semicircle rainbow arc with center score."""
        p = self._ns()
        parts = [add_action_title(title)]
        svg = make_gauge_svg(score, cx=200, cy=180, radius=150)
        parts.append(f'<div style="position:absolute; left:{SLIDE_WIDTH // 2 - 200}px; top:{CONTENT_TOP + 30}px">{svg}</div>')
        if benchmarks:
            bsy = 530
            for i, (label, val, color) in enumerate(benchmarks):
                bx = LM + 50 + i * 250
                parts.append(self._abs(bx, bsy, 8, 60, bg=color))
                parts.append(self._text(bx + 20, bsy, 200, 30, label,
                                        font_size=SMALL_SIZE, color=MED_GRAY))
                parts.append(self._text(bx + 20, bsy + 30, 200, 30, val,
                                        font_size=22, color=color, bold=True,
                                        font_family=FONT_STACK_HEADER))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # IMAGE LAYOUTS
    # ═══════════════════════════════════════════

    def content_right_image(self, title, subtitle, bullets, takeaway='',
                            image_label='Image', source=''):
        """Content + Right Image."""
        p = self._ns()
        parts = [add_action_title(title)]
        left_w = 650
        parts.append(self._text(LM, CONTENT_TOP, left_w, 40, subtitle,
                                font_size=SUB_HEADER_SIZE, color=NAVY, bold=True))
        parts.append(self._text(LM, CONTENT_TOP + 50, left_w, 350, bullets,
                                font_size=BODY_SIZE))
        if takeaway:
            parts.append(self._abs(LM, 550, left_w, 80, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 550, left_w - 60, 80, takeaway,
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
        img_x = LM + left_w + 30
        img_w = CW - left_w - 30
        parts.append(f'<div class="image-placeholder" style="position:absolute; left:{img_x}px; top:{CONTENT_TOP}px; width:{img_w}px; height:420px"><span>[ {esc(image_label)} ]</span></div>')
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def full_width_image(self, title, image_label, overlay_text='', attribution='',
                         source=''):
        """Full-Width Image — edge-to-edge image with text overlay."""
        p = self._ns()
        parts = []
        parts.append(f'<div class="image-placeholder" style="position:absolute; left:0; top:0; width:{SLIDE_WIDTH}px; height:650px"><span>[ {esc(image_label)} ]</span></div>')
        parts.append(self._abs(0, 400, SLIDE_WIDTH, 200, bg=NAVY,
                               extra_style='opacity:0.7'))
        if overlay_text:
            parts.append(self._text(LM, 410, CW, 80, overlay_text,
                                    font_size=SECTION_TITLE_SIZE, color=WHITE, bold=True,
                                    align='center', valign='middle'))
        if attribution:
            parts.append(self._text(LM, 490, CW, 40, attribution,
                                    font_size=BODY_SIZE, color=LINE_GRAY, align='center'))
        if source:
            parts.append(add_source(source))
        parts.append(add_page_number(p, self.total))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def three_images(self, title, items, source=''):
        """Three Images — three image+caption columns."""
        p = self._ns()
        parts = [add_action_title(title)]
        col_w = 370
        gap = 35
        img_h = 250
        ty = 130
        for i, (cap_title, desc, img_label) in enumerate(items):
            cx = LM + i * (col_w + gap)
            parts.append(f'<div class="image-placeholder" style="position:absolute; left:{cx}px; top:{ty}px; width:{col_w}px; height:{img_h}px"><span>[ {esc(img_label)} ]</span></div>')
            parts.append(self._text(cx, ty + img_h + 15, col_w, 35,
                                    cap_title, font_size=EMPHASIS_SIZE, color=NAVY, bold=True))
            parts.append(self._text(cx, ty + img_h + 55, col_w, 100,
                                    desc, font_size=BODY_SIZE, color=DARK_GRAY))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # ADVANCED LAYOUTS
    # ═══════════════════════════════════════════

    def funnel(self, title, stages, source=''):
        """Funnel — top-down narrowing bars."""
        p = self._ns()
        parts = [add_action_title(title)]
        max_w = 800
        fy = 160
        for i, (name, count, pct) in enumerate(stages):
            w = int(max_w * pct)
            fx = int(SLIDE_WIDTH / 2 - w / 2)
            fill = NAVY if i == 0 else BG_GRAY
            tc = WHITE if i == 0 else NAVY
            parts.append(self._abs(fx, fy, w, 100, bg=fill))
            parts.append(self._text(fx + 20, fy, w - 40, 100, name,
                                    font_size=SUB_HEADER_SIZE, color=tc, bold=True,
                                    valign='middle', align='center'))
            parts.append(self._text(fx + w + 30, fy + 20, 300, 50,
                                    f'{count} ({int(pct * 100)}%)',
                                    font_size=BODY_SIZE, color=NAVY, bold=True))
            fy += 120
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def cycle(self, title, phases, right_panel=None, source=''):
        """Cycle Diagram — rectangular nodes with arrows."""
        p = self._ns()
        parts = [add_action_title(title)]
        box_w, box_h = 220, 120
        for i, (label, px, py) in enumerate(phases):
            fill = NAVY if i == 0 else BG_GRAY
            tc = WHITE if i == 0 else NAVY
            parts.append(self._abs(LM + int(px * 100), int(py * 100), box_w, box_h, bg=fill))
            parts.append(self._text(LM + int(px * 100) + 10, int(py * 100) + 10,
                                    box_w - 20, box_h - 20, label,
                                    font_size=SUB_HEADER_SIZE, color=tc, bold=True,
                                    align='center', valign='middle'))
        if right_panel:
            pt, pp = right_panel
            parts.append(self._abs(850, 150, 400, 500, bg=BG_GRAY))
            parts.append(self._text(880, 170, 340, 40, pt,
                                    font_size=BODY_SIZE, color=NAVY, bold=True))
            pp_list = pp if isinstance(pp, list) else [pp]
            parts.append(self._text(880, 230, 340, 350, pp_list, font_size=BODY_SIZE))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def venn(self, title, circles, overlap_label='', right_text=None, source=''):
        """Venn Diagram — overlapping rectangles."""
        p = self._ns()
        parts = [add_action_title(title)]
        for i, circ in enumerate(circles):
            label, points = circ[0], circ[1]
            cx_val, cy_val, cw, ch_val = int(circ[2] * 100), int(circ[3] * 100), int(circ[4] * 100), int(circ[5] * 100)
            is_overlap = (i == len(circles) - 1 and overlap_label)
            fill = NAVY if is_overlap else BG_GRAY
            fc = WHITE if is_overlap else NAVY
            parts.append(self._abs(cx_val, cy_val, cw, ch_val, bg=fill))
            parts.append(self._text(cx_val + 20, cy_val + 20, cw - 40, 40,
                                    label, font_size=SUB_HEADER_SIZE, color=fc, bold=True))
            if points:
                pts_list = points if isinstance(points, list) else [points]
                parts.append(self._text(cx_val + 20, cy_val + 70, cw - 40, ch_val - 90,
                                        pts_list, font_size=BODY_SIZE,
                                        color=fc if is_overlap else DARK_GRAY))
        if right_text:
            parts.append(self._text(900, 200, 350, 400, right_text, font_size=BODY_SIZE))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def value_chain(self, title, stages, source='', bottom_bar=None):
        """Value Chain / Horizontal Flow — stages with arrows."""
        p = self._ns()
        parts = [add_action_title(title)]
        n = len(stages)
        arrow_w = 35
        stage_w = int((CW - arrow_w * (n - 1)) / n)
        stage_y = CONTENT_TOP + 10
        stage_h = (BOTTOM_BAR_Y - 15 - stage_y) if bottom_bar else (SOURCE_Y - 15 - stage_y)
        for i, (stitle, desc, color) in enumerate(stages):
            sx = LM + i * (stage_w + arrow_w)
            parts.append(self._abs(sx, stage_y, stage_w, stage_h, bg=WHITE,
                                   extra_style=f'border-top: 6px solid {color}'))
            parts.append(self._oval(sx + 10, stage_y + 20, str(i + 1), bg=color, size=40))
            parts.append(self._text(sx + 60, stage_y + 20, stage_w - 70, 40,
                                    stitle, font_size=BODY_SIZE, color=color, bold=True,
                                    valign='middle'))
            desc_items = desc if isinstance(desc, list) else [desc]
            parts.append(self._text(sx + 10, stage_y + 80, stage_w - 20, stage_h - 90,
                                    desc_items, font_size=SMALL_SIZE, align='center'))
            if i < n - 1:
                ax = sx + stage_w + 2
                parts.append(self._text(ax, stage_y + stage_h // 2 - 20, arrow_w - 5, 40,
                                        '→', font_size=20, color=LINE_GRAY, align='center'))
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def checklist(self, title, columns, col_widths, rows, status_map=None,
                  source='', bottom_bar=None):
        """Checklist / Status table."""
        p = self._ns()
        parts = [add_action_title(title)]
        if status_map is None:
            status_map = {
                'active':  ('→ 活跃', ACCENT_GREEN, LIGHT_GREEN),
                'risk':    ('△ 困难', ACCENT_ORANGE, LIGHT_ORANGE),
                'pending': ('○ 早期', MED_GRAY, BG_GRAY),
                'done':    ('✓ 完成', ACCENT_BLUE, LIGHT_BLUE),
            }
        # Convert Inches to px if needed
        cw_px = [int(w * 100) if isinstance(w, float) else w for w in col_widths]
        hx = LM
        hy = CONTENT_TOP + 10
        for label, w in zip(columns, cw_px):
            parts.append(self._text(hx, hy, w, 35, label,
                                    font_size=SMALL_SIZE, color=NAVY, bold=True))
            hx += w
        total_w = sum(cw_px)
        parts.append(self._hline(LM, hy + 35, total_w, BLACK, 0.75))
        bottom_limit = BOTTOM_BAR_Y - 10 if bottom_bar else SOURCE_Y - 5
        avail = bottom_limit - (hy + 50)
        row_h = min(85, int(avail / max(len(rows), 1)))
        for i, row in enumerate(rows):
            *data_vals, status_key = row
            ry = hy + 50 + i * row_h
            st_label, st_color, st_bg = status_map.get(status_key, ('?', MED_GRAY, BG_GRAY))
            if i % 2 == 0:
                parts.append(self._abs(LM, ry, total_w, row_h, bg='#FAFAFA'))
            rx = LM
            for vi, w in enumerate(cw_px[:-1]):
                val = data_vals[vi] if vi < len(data_vals) else ''
                parts.append(self._text(rx, ry, w, row_h, val,
                                        font_size=SMALL_SIZE, valign='middle'))
                rx += w
            status_w = cw_px[-1]
            parts.append(self._abs(rx + 10, ry + 12, status_w - 20, row_h - 24, bg=st_bg))
            parts.append(self._text(rx + 10, ry, status_w - 20, row_h, st_label,
                                    font_size=SMALL_SIZE, color=st_color, bold=True,
                                    align='center', valign='middle'))
        if bottom_bar:
            parts.append(add_bottom_bar(bottom_bar[0], bottom_bar[1]))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def icon_grid(self, title, items, cols=3, source=''):
        """Icon Grid — grid of icon cards."""
        p = self._ns()
        parts = [add_action_title(title)]
        celw = int(CW / cols - 15)
        celh = 220
        ty = 130
        for i, (ititle, desc, color) in enumerate(items):
            col = i % cols
            row = i // cols
            ix = LM + col * (celw + 15)
            iy = ty + row * (celh + 10)
            parts.append(self._abs(ix, iy, celw, celh, bg=WHITE,
                                   extra_style=f'border-top: 6px solid {color}'))
            parts.append(self._oval(ix + 30, iy + 25, ititle[0], bg=color, size=60))
            parts.append(self._text(ix + 110, iy + 25, celw - 130, 40,
                                    ititle, font_size=EMPHASIS_SIZE, color=color, bold=True,
                                    valign='middle'))
            parts.append(self._text(ix + 30, iy + 100, celw - 60, 100,
                                    desc, font_size=BODY_SIZE, color=DARK_GRAY))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def rag_status(self, title, headers, rows, source=''):
        """RAG Status — table with red/amber/green status dots."""
        p = self._ns()
        parts = [add_action_title(title)]
        n = len(headers)
        col_w = int(CW / n)
        hx = LM
        for h in headers:
            parts.append(self._text(hx, 150, col_w, 40, h,
                                    font_size=BODY_SIZE, color=MED_GRAY, bold=True))
            hx += col_w
        parts.append(self._hline(LM, 200, CW, BLACK, 1))
        ry = 220
        for row in rows:
            name = row[0]
            status_color = row[1]
            values = row[2:-1]
            note = row[-1]
            parts.append(self._text(LM, ry, col_w, 60, name, font_size=BODY_SIZE))
            parts.append(self._oval(LM + col_w + 30, ry + 5, '', bg=status_color, size=35))
            cx = LM + col_w * 2
            for val in values:
                parts.append(self._text(cx, ry, col_w, 60, val, font_size=BODY_SIZE))
                cx += col_w
            parts.append(self._text(cx, ry, col_w, 60, note, font_size=BODY_SIZE))
            ry += 70
            parts.append(self._hline(LM, ry, CW, LINE_GRAY))
            ry += 15
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # ADDITIONAL CHART LAYOUTS
    # ═══════════════════════════════════════════

    def stacked_bar(self, title, periods, series, data, summary=None, source=''):
        """Stacked Bar Chart — 100% stacked vertical bars.
        periods: list[str] x-labels. series: list of (name, color).
        data: list[list[int]] — percentages, data[period_idx][series_idx].
        """
        p = self._ns()
        parts = [add_action_title(title)]
        cl = LM + 80
        cb = 500
        ct = 160
        ch = cb - ct
        cr = 1150
        cww = cr - cl
        np_ = len(periods)
        bw = 120
        sbs = int(cww / np_)
        # Legend
        for ci, (sname, scolor) in enumerate(series):
            lx = LM + 800 + 180 * ci
            parts.append(self._abs(lx, 125, 20, 20, bg=scolor))
            parts.append(self._text(lx + 30, 120, 120, 30, sname,
                                    font_size=SMALL_SIZE, color=DARK_GRAY))
        # Y-axis ticks
        for tk in [0, 25, 50, 75, 100]:
            ty = cb - int(ch * tk / 100)
            parts.append(self._text(LM, ty - 15, 70, 30, f'{tk}%',
                                    font_size=FOOTNOTE_SIZE, color=MED_GRAY, align='right'))
            if tk > 0:
                parts.append(self._hline(cl, ty, cww, LINE_GRAY, 0.25))
        parts.append(self._hline(cl, cb, cww, BLACK, 0.5))
        # Bars
        for pi, period in enumerate(periods):
            bx = cl + sbs * pi + int((sbs - bw) / 2)
            cum = 0
            for ci in range(len(series)):
                val = data[pi][ci]
                sh_ = int(ch * val / 100)
                sy = cb - int(ch * (cum + val) / 100)
                if val > 0:
                    parts.append(self._abs(bx, sy, bw, sh_, bg=series[ci][1]))
                    if sh_ >= 40:
                        lc = WHITE if ci < 2 else DARK_GRAY
                        parts.append(self._text(bx, sy, bw, sh_, f'{val}%',
                                                font_size=11, color=lc, bold=True,
                                                align='center', valign='middle'))
                cum += val
            parts.append(self._text(cl + sbs * pi, cb + 5, sbs, 30, period,
                                    font_size=BODY_SIZE, color=DARK_GRAY, align='center'))
        if summary:
            parts.append(self._abs(LM, 600, CW, 80, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 600, 150, 80, summary[0],
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
            parts.append(self._text(LM + 200, 600, CW - 230, 80, summary[1],
                                    font_size=BODY_SIZE, color=DARK_GRAY, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def waterfall(self, title, items, max_val=None, legend_items=None,
                  summary=None, source=''):
        """Waterfall Chart — bridge from start to end.
        items: list of (label, value, type) — type: 'base'|'up'|'down'.
        """
        p = self._ns()
        parts = [add_action_title(title)]
        if legend_items:
            for li, (ln, lc) in enumerate(legend_items):
                lx = LM + 800 + li * 130
                parts.append(self._abs(lx, 125, 20, 20, bg=lc))
                parts.append(self._text(lx + 25, 120, 80, 30, ln,
                                        font_size=11, color=DARK_GRAY))
        cl = LM + 30
        cb = 500
        ct = 230
        ch = cb - ct
        if max_val is None:
            max_val = max(abs(v) for _, v, _ in items) * 1.3
        bw = 120
        gp = 40
        running = 0
        prev_top = 0
        for i, (label, val, typ) in enumerate(items):
            bx = cl + i * (bw + gp)
            if typ == 'base':
                bh = int(ch * val / max_val)
                bt = cb - bh
                color = NAVY
                running = val
            elif typ == 'up':
                bh = int(ch * val / max_val)
                bt = cb - int(ch * running / max_val) - bh
                color = ACCENT_GREEN
                running += val
            else:
                bh = int(ch * abs(val) / max_val)
                bt = cb - int(ch * running / max_val)
                color = ACCENT_RED
                running += val
            parts.append(self._abs(bx, bt, bw, bh, bg=color))
            if i > 0:
                parts.append(self._hline(bx - gp, prev_top, gp + 5, LINE_GRAY, 0.75))
            prev_top = bt if typ != 'down' else bt + bh
            vs = f'+{val}' if val > 0 and typ != 'base' else str(val)
            parts.append(self._text(bx, bt - 35, bw, 30, vs,
                                    font_size=BODY_SIZE, color=DARK_GRAY, bold=True,
                                    align='center', font_family=FONT_STACK_HEADER))
            parts.append(self._text(bx, cb + 5, bw, 50, label,
                                    font_size=11, color=MED_GRAY, align='center'))
        parts.append(self._hline(cl, cb, 1150, LINE_GRAY, 0.5))
        if summary:
            parts.append(self._abs(LM, 620, CW, 60, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 620, CW - 60, 60, summary,
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def line_chart(self, title, x_labels, y_labels, values, legend_label='',
                   summary=None, source=''):
        """Line Chart — SVG polyline with dots.
        x_labels: list[str], y_labels: list[str], values: list[float] 0.0-1.0 normalized.
        """
        p = self._ns()
        parts = [add_action_title(title)]
        cl = LM + 80
        cr = LM + CW - 150
        cw_ = cr - cl
        ct = 160
        cb = 520
        ch = cb - ct
        # Legend
        if legend_label:
            parts.append(self._abs(LM + 900, 125, 30, 15, bg=NAVY))
            parts.append(self._text(LM + 940, 120, 150, 30, legend_label,
                                    font_size=11, color=NAVY, bold=True))
        # Y-axis
        for i, yl in enumerate(y_labels):
            yy = cb - int(ch * i / (len(y_labels) - 1))
            parts.append(self._text(LM, yy - 12, 70, 24, yl,
                                    font_size=FOOTNOTE_SIZE, color=MED_GRAY, align='right'))
            if i > 0:
                parts.append(self._hline(cl, yy, cw_, '#E8E8E8', 0.25))
        # X-axis labels
        npt = len(x_labels)
        for i, xl in enumerate(x_labels):
            xx = cl + int(cw_ * i / (npt - 1))
            parts.append(self._text(xx - 30, cb + 5, 60, 25, xl,
                                    font_size=FOOTNOTE_SIZE, color=MED_GRAY, align='center'))
        # SVG line chart
        points = []
        for j in range(len(values)):
            x = cl + int(cw_ * j / (npt - 1))
            y = cb - int(ch * values[j])
            points.append((x, y))
        polyline = ' '.join(f'{x},{y}' for x, y in points)
        dots = ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="{NAVY}" />' for x, y in points)
        svg = f'''<svg style="position:absolute; left:0; top:0; width:{SLIDE_WIDTH}px; height:{SLIDE_HEIGHT}px; pointer-events:none">
            <polyline points="{polyline}" fill="none" stroke="{NAVY}" stroke-width="2.5"/>
            {dots}
        </svg>'''
        parts.append(svg)
        parts.append(self._hline(cl, cb, cw_, BLACK, 0.5))
        if summary:
            parts.append(self._abs(LM, 570, CW, 70, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 570, CW - 60, 70, summary,
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def pareto(self, title, items, max_val=None, summary=None, source=''):
        """Pareto Chart — descending bars with value/pct labels.
        items: list of (label, value).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        total = sum(v for _, v in items)
        if max_val is None:
            max_val = max(v for _, v in items) * 1.15
        cl = LM + 100
        cb = 550
        ct = 180
        ch = cb - ct
        cw_ = 900
        n = len(items)
        gap = 15
        bw = int((cw_ - gap * (n - 1)) / n)
        for i, (label, val) in enumerate(items):
            bx = cl + i * (bw + gap)
            bh = int(ch * val / max_val)
            bt = cb - bh
            parts.append(self._abs(bx, bt, bw, bh, bg=NAVY))
            parts.append(self._text(bx, bt - 25, bw, 22, str(val),
                                    font_size=11, color=DARK_GRAY, bold=True, align='center'))
            pct_ = val / total if total else 0
            parts.append(self._text(bx, bt - 48, bw, 22, f'{int(pct_ * 100)}%',
                                    font_size=FOOTNOTE_SIZE, color=MED_GRAY, align='center'))
            parts.append(self._text(bx, cb + 5, bw, 35, label,
                                    font_size=10, color=MED_GRAY, align='center'))
        parts.append(self._hline(cl, cb, cw_, BLACK, 0.5))
        if summary:
            parts.append(self._abs(LM, 600, CW, 60, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 600, CW - 60, 60, summary,
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def kpi_tracker(self, title, kpis, summary=None, source=''):
        """KPI Tracker — progress bars with status dots.
        kpis: list of (name, pct_float, detail, status_key).
        status_key: 'on'|'risk'|'off'.
        """
        p = self._ns()
        parts = [add_action_title(title)]
        sc_map = {
            'on': (ACCENT_GREEN, '达标'),
            'risk': (ACCENT_ORANGE, '关注'),
            'off': (ACCENT_RED, '滞后'),
        }
        # Headers
        hy = 130
        parts.append(self._text(LM, hy, 350, 35, 'KPI指标',
                                font_size=SMALL_SIZE, color=MED_GRAY, bold=True))
        parts.append(self._text(LM + 350, hy, 600, 35, '进度',
                                font_size=SMALL_SIZE, color=MED_GRAY, bold=True))
        parts.append(self._text(LM + 950, hy, 120, 35, '达成率',
                                font_size=SMALL_SIZE, color=MED_GRAY, bold=True, align='center'))
        parts.append(self._text(LM + 1070, hy, 100, 35, '状态',
                                font_size=SMALL_SIZE, color=MED_GRAY, bold=True, align='center'))
        parts.append(self._hline(LM, hy + 35, CW, BLACK, 0.75))
        bar_x = LM + 350
        bar_mw = 580
        bar_h = 25
        rh = 80
        for i, (name, pct_, detail, status) in enumerate(kpis):
            ry = 190 + i * rh
            parts.append(self._text(LM, ry, 330, rh, name,
                                    font_size=BODY_SIZE, color=DARK_GRAY, bold=True, valign='middle'))
            parts.append(self._abs(bar_x, ry + int((rh - bar_h) / 2), bar_mw, bar_h, bg=BG_GRAY))
            color, label = sc_map.get(status, (MED_GRAY, '?'))
            fw = int(bar_mw * min(pct_, 1.0))
            parts.append(self._abs(bar_x, ry + int((rh - bar_h) / 2), fw, bar_h, bg=color))
            parts.append(self._text(LM + 950, ry, 120, rh,
                                    f'{int(min(pct_, 1.0) * 100)}%',
                                    font_size=EMPHASIS_SIZE, color=DARK_GRAY, bold=True,
                                    align='center', valign='middle'))
            dsz = 15
            parts.append(self._abs(LM + 1080, ry + int((rh - dsz) / 2), dsz, dsz, bg=color))
            parts.append(self._text(LM + 1100, ry, 70, rh, label,
                                    font_size=11, color=color, valign='middle'))
            if i < len(kpis) - 1:
                parts.append(self._hline(LM, ry + rh, CW, LINE_GRAY, 0.25))
        if summary:
            parts.append(self._abs(LM, 600, CW, 70, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 600, 150, 70, '总结',
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
            parts.append(self._text(LM + 200, 600, CW - 230, 70, summary,
                                    font_size=BODY_SIZE, color=DARK_GRAY, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def bubble(self, title, bubbles, x_label='', y_label='',
               legend_items=None, summary=None, source=''):
        """Bubble / Scatter — positioned circles on XY plane.
        bubbles: list of (x_pct, y_pct, size_inches, label, color).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        cl = LM + 120
        cb = 550
        ct = 160
        cw_ = 900
        ch = cb - ct
        # Legend
        if legend_items:
            for li, (ln, lc) in enumerate(legend_items):
                lx = LM + 720 + li * 85
                parts.append(self._abs(lx, 125, 15, 15, bg=lc))
                parts.append(self._text(lx + 20, 120, 55, 30, ln,
                                        font_size=10, color=DARK_GRAY))
        # Axes
        parts.append(self._hline(cl, cb, cw_, BLACK, 0.5))
        parts.append(self._abs(cl, ct, 1, ch, bg=BLACK))
        if x_label:
            parts.append(self._text(cl + cw_ // 2 - 100, cb + 15, 200, 30, x_label,
                                    font_size=11, color=MED_GRAY, align='center'))
        if y_label:
            parts.append(self._text(LM, ct + ch // 2 - 50, 100, 100, y_label,
                                    font_size=11, color=MED_GRAY, align='center', valign='middle'))
        # Bubbles
        for xp, yp, sz, lb, color in bubbles:
            sz_px = int(sz * 100)
            bx = cl + int(cw_ * xp) - sz_px // 2
            by = cb - int(ch * yp) - sz_px // 2
            tc = WHITE if color != LINE_GRAY else DARK_GRAY
            parts.append(f'<div style="position:absolute; left:{bx}px; top:{by}px; width:{sz_px}px; height:{sz_px}px; border-radius:50%; background:{color}; display:flex; align-items:center; justify-content:center; font-size:{FOOTNOTE_SIZE}px; color:{tc}; font-weight:bold; font-family:Arial,sans-serif;">{esc(lb)}</div>')
        if summary:
            parts.append(self._abs(LM, 600, CW, 60, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 600, CW - 60, 60, summary,
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def risk_matrix(self, title, grid_colors, grid_lights, risks,
                    y_labels=None, x_labels=None, notes=None, source=''):
        """Risk Matrix — 3×3 heatmap grid with risk labels.
        grid_colors: 3×3 list of dot color strings.
        grid_lights: 3×3 list of cell bg color strings.
        risks: list of (row, col, name).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        gl = LM + 180
        gt = 150
        gcw = 300
        gch = 110
        if y_labels is None:
            y_labels = ['高概率', '中概率', '低概率']
        if x_labels is None:
            x_labels = ['低影响', '中影响', '高影响']
        for r in range(3):
            parts.append(self._text(LM, gt + r * gch, 160, gch, y_labels[r],
                                    font_size=13, color=DARK_GRAY, bold=True,
                                    align='right', valign='middle'))
        for c in range(3):
            parts.append(self._text(gl + c * gcw, gt - 35, gcw, 30, x_labels[c],
                                    font_size=13, color=DARK_GRAY, bold=True, align='center'))
        for r in range(3):
            for c in range(3):
                cx = gl + c * gcw
                cy = gt + r * gch
                parts.append(self._abs(cx, cy, gcw - 5, gch - 5, bg=grid_lights[r][c]))
                parts.append(self._abs(cx + 10, cy + 10, 20, 20, bg=grid_colors[r][c]))
        for r, c, name in risks:
            parts.append(self._text(gl + c * gcw + 40, gt + r * gch + 25,
                                    gcw - 60, 60, name,
                                    font_size=13, color=DARK_GRAY, bold=True, valign='middle'))
        if notes:
            parts.append(self._abs(LM, 510, CW, 160, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 515, 150, 30, '应对措施',
                                    font_size=BODY_SIZE, color=NAVY, bold=True))
            notes_list = notes if isinstance(notes, list) else [notes]
            parts.append(self._text(LM + 30, 550, CW - 60, 110, notes_list,
                                    font_size=BODY_SIZE, color=DARK_GRAY))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def harvey_ball_table(self, title, criteria, options, scores,
                          legend_text=None, summary=None, source=''):
        """Harvey Ball Table — matrix with Harvey Ball indicators.
        criteria: list[str] row labels. options: list[str] column headers.
        scores: list[list[int]] — scores[row][col], 0-4.
        """
        p = self._ns()
        parts = [add_action_title(title)]
        c1w = 280
        colw = 250
        rh = 60
        tl = LM
        ty = 130
        parts.append(self._text(tl, ty, c1w, rh, '评估维度',
                                font_size=13, color=NAVY, bold=True, valign='middle'))
        for j, opt in enumerate(options):
            parts.append(self._text(tl + c1w + j * colw, ty, colw, rh, opt,
                                    font_size=13, color=NAVY, bold=True,
                                    align='center', valign='middle'))
        total_w = c1w + len(options) * colw
        parts.append(self._hline(tl, ty + rh, total_w, BLACK, 0.75))
        for i, cr in enumerate(criteria):
            ry = ty + rh + 5 + i * rh
            parts.append(self._text(tl, ry, c1w, rh, cr,
                                    font_size=BODY_SIZE, color=DARK_GRAY, valign='middle'))
            for j in range(len(options)):
                bx = tl + c1w + j * colw + int((colw - 35) / 2)
                by = ry + int((rh - 35) / 2)
                parts.append(f'<div style="position:absolute; left:{bx}px; top:{by}px">{make_harvey_ball_html(scores[i][j])}</div>')
            if i < len(criteria) - 1:
                parts.append(self._hline(tl, ry + rh, total_w, LINE_GRAY, 0.25))
        # Legend
        lgy = ty + rh + len(criteria) * rh + 30
        parts.append(self._hline(tl, lgy - 10, total_w, BLACK, 0.5))
        if legend_text:
            lx = tl
            for item in legend_text:
                parts.append(self._text(lx, lgy, 220, 30, item,
                                        font_size=11, color=MED_GRAY))
                lx += 240
        if summary:
            parts.append(self._abs(LM, 580, CW, 80, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 580, CW - 60, 80, summary,
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def stacked_area(self, title, years, series_data, max_val=None,
                     summary=None, source=''):
        """Stacked Area Chart — stacked columns for area approximation.
        years: list[str] x-labels.
        series_data: list of (name, values:list[int], color).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        cl = LM + 100
        cb = 530
        ct = 160
        cw_ = 950
        ch = cb - ct
        if max_val is None:
            max_val = max(sum(sd[1][yi] for sd in series_data)
                         for yi in range(len(years))) * 1.15
        # Legend
        for i, (name, _, color) in enumerate(series_data):
            lgx = LM + 800 + i * 150
            parts.append(self._abs(lgx, 125, 25, 20, bg=color))
            parts.append(self._text(lgx + 35, 120, 100, 30, name,
                                    font_size=11, color=DARK_GRAY))
        # Y-axis
        for i in range(5):
            val = max_val * i / 4
            yy = cb - int(ch * i / 4)
            parts.append(self._text(LM, yy - 10, 80, 20, f'¥{int(val)}',
                                    font_size=FOOTNOTE_SIZE, color=MED_GRAY, align='right'))
            if i > 0:
                parts.append(self._hline(cl, yy, cw_, '#E8E8E8', 0.25))
        npt = len(years)
        col_w = int(cw_ / npt)
        for yi in range(npt):
            cum = 0
            for si, (name, values, color) in enumerate(series_data):
                val = values[yi]
                bh = int(ch * val / max_val)
                base_h = int(ch * cum / max_val)
                bx = cl + int(cw_ * yi / npt)
                by = cb - base_h - bh
                parts.append(self._abs(bx + 5, by, col_w - 10, bh, bg=color))
                cum += val
            total = sum(sd[1][yi] for sd in series_data)
            th = int(ch * total / max_val)
            parts.append(self._text(cl + int(cw_ * yi / npt), cb - th - 25,
                                    col_w, 20, f'¥{total}',
                                    font_size=10, color=DARK_GRAY, bold=True, align='center'))
            parts.append(self._text(cl + int(cw_ * yi / npt), cb + 5,
                                    col_w, 20, years[yi],
                                    font_size=10, color=MED_GRAY, align='center'))
        parts.append(self._hline(cl, cb, cw_, BLACK, 0.5))
        if summary:
            parts.append(self._abs(LM, 570, CW, 80, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 570, 150, 80, '趋势分析',
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
            parts.append(self._text(LM + 200, 570, CW - 230, 80, summary,
                                    font_size=BODY_SIZE, color=DARK_GRAY, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # DASHBOARDS & SPECIAL LAYOUTS
    # ═══════════════════════════════════════════

    def dashboard_kpi_chart(self, title, kpi_cards, chart_data=None,
                            summary=None, source=''):
        """Dashboard KPI + Chart — top KPI cards + bottom mini chart.
        kpi_cards: list of (value, label, detail, accent_color).
        chart_data: dict with 'labels','actual','target','max_val','legend'.
        """
        p = self._ns()
        parts = [add_action_title(title)]
        n = len(kpi_cards)
        dkw = int(CW / n - 15)
        dkh = 110
        dky = 120
        for i, (val, label, detail, color) in enumerate(kpi_cards):
            cx = LM + i * (dkw + 15)
            parts.append(self._abs(cx, dky, dkw, dkh, bg=WHITE,
                                   extra_style=f'border-top: 6px solid {color}'))
            parts.append(self._text(cx + 20, dky + 15, dkw - 40, 45, val,
                                    font_size=24, color=color, bold=True,
                                    font_family=FONT_STACK_HEADER))
            parts.append(self._text(cx + 20, dky + 60, 150, 20, label,
                                    font_size=11, color=MED_GRAY))
            parts.append(self._text(cx + 180, dky + 60, dkw - 200, 20, detail,
                                    font_size=10, color=ACCENT_GREEN, align='right'))
        if chart_data:
            dcy = 260
            dch = 250
            dcl = LM + 50
            dcb = dcy + dch
            labels = chart_data.get('labels', [])
            actual = chart_data.get('actual', [])
            target = chart_data.get('target', [])
            mv = chart_data.get('max_val', max(actual + target) * 1.15 if actual or target else 1)
            dbw = 60
            dpg = 15
            dgw = dbw * 2 + dpg
            dmgp = 50
            for i in range(len(labels)):
                gx = dcl + i * (dgw + dmgp)
                for j, (vals, color) in enumerate([(actual, NAVY), (target, BG_GRAY)]):
                    bx = gx + j * (dbw + dpg)
                    val_num = vals[i] if i < len(vals) else 0
                    bh = int(dch * val_num / mv) if mv else 0
                    bt = dcb - bh
                    parts.append(self._abs(bx, bt, dbw, bh, bg=color))
                parts.append(self._text(gx, dcb + 3, dgw, 20, labels[i],
                                        font_size=FOOTNOTE_SIZE, color=MED_GRAY, align='center'))
            parts.append(self._hline(dcl, dcb, 1050, LINE_GRAY, 0.5))
            legend = chart_data.get('legend', [('实际', NAVY), ('目标', BG_GRAY)])
            for li, (ln, lc) in enumerate(legend):
                lx = LM + 900 + li * 130
                parts.append(self._abs(lx, dcy, 30, 15, bg=lc))
                parts.append(self._text(lx + 40, dcy - 2, 80, 20, ln,
                                        font_size=FOOTNOTE_SIZE, color=DARK_GRAY))
        if summary:
            parts.append(self._abs(LM, 560, CW, 90, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 560, 150, 90, '关键发现',
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
            summary_items = summary if isinstance(summary, list) else [summary]
            parts.append(self._text(LM + 200, 560, CW - 230, 90, summary_items,
                                    font_size=BODY_SIZE, color=DARK_GRAY, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def dashboard_table_chart(self, title, table_data, chart_data=None,
                              factoids=None, source=''):
        """Dashboard Table + Chart — left table + right mini chart + bottom facts.
        table_data: dict with 'headers','col_widths','rows'.
        chart_data: dict with 'title','items':(name, value).
        factoids: list of (value, label, color).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        td = table_data or {}
        headers = td.get('headers', [])
        col_widths = td.get('col_widths', [])
        rows = td.get('rows', [])
        # Convert Inches to px if float
        col_widths_px = [int(w * 100) if isinstance(w, float) else w for w in col_widths]
        dlw = sum(col_widths_px) if col_widths_px else 620
        dty = 130
        dhx = LM
        for ci, (cn, cw) in enumerate(zip(headers, col_widths_px)):
            parts.append(self._text(dhx, dty, cw, 30, cn,
                                    font_size=SMALL_SIZE, color=NAVY, bold=True))
            dhx += cw
        parts.append(self._hline(LM, dty + 30, dlw, BLACK, 0.75))
        for ri, row in enumerate(rows):
            ry = dty + 40 + ri * 50
            rx = LM
            for ci, (val, cw) in enumerate(zip(row, col_widths_px)):
                fc = DARK_GRAY
                if ci == 2 and '+' in str(val):
                    fc = ACCENT_GREEN
                parts.append(self._text(rx, ry, cw, 40, str(val),
                                        font_size=BODY_SIZE, color=fc, valign='middle'))
                rx += cw
            if ri < len(rows) - 1:
                parts.append(self._hline(LM, ry + 45, dlw, LINE_GRAY, 0.25))
        if chart_data:
            dcx = LM + dlw + 50
            dcrw = CW - dlw - 50
            parts.append(self._text(dcx, 130, dcrw, 30, chart_data.get('title', ''),
                                    font_size=SMALL_SIZE, color=NAVY, bold=True))
            parts.append(self._hline(dcx, 160, dcrw, BLACK, 0.5))
            items = chart_data.get('items', [])
            bmw = 350
            mx = max((v for _, v in items), default=1)
            for i, (rg, rev) in enumerate(items):
                by = 175 + i * 45
                bw = int(bmw * rev / mx)
                parts.append(self._text(dcx, by, 80, 30, rg,
                                        font_size=11, color=MED_GRAY, valign='middle'))
                bc = NAVY if i == 0 else ACCENT_BLUE
                parts.append(self._abs(dcx + 90, by, bw, 30, bg=bc))
        if factoids:
            dfy = 520
            nf = len(factoids)
            dfcw = int(CW / nf - 15)
            dfch = 100
            for i, (val, label, color) in enumerate(factoids):
                fx = LM + i * (dfcw + 15)
                parts.append(self._abs(fx, dfy, dfcw, dfch, bg=BG_GRAY,
                                       extra_style=f'border-left: 6px solid {color}'))
                parts.append(self._text(fx + 20, dfy + 10, dfcw - 30, 50, val,
                                        font_size=24, color=color, bold=True))
                parts.append(self._text(fx + 20, dfy + 60, dfcw - 30, 30, label,
                                        font_size=11, color=MED_GRAY))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def stakeholder_map(self, title, quadrants, x_label='影响力 →',
                        y_label='关注度 ↑', summary=None, source=''):
        """Stakeholder Map — 2×2 quadrant with stakeholder lists.
        quadrants: list of 4 (label_cn, label_en, bg_color, members:list[str]).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        sgl = LM + 200
        sgt = 150
        sgcw = 450
        sgch = 180
        for qi, (lcn, len_, bgc, members) in enumerate(quadrants):
            r, c = qi // 2, qi % 2
            qx = sgl + c * sgcw
            qy = sgt + r * sgch
            parts.append(self._abs(qx, qy, sgcw - 5, sgch - 5, bg=bgc))
            parts.append(self._text(qx + 15, qy + 10, sgcw - 30, 35,
                                    f'{lcn} ({len_})',
                                    font_size=13, color=NAVY, bold=True))
            for ni, name in enumerate(members):
                parts.append(self._oval(qx + 20, qy + 55 + ni * 40, name[0], size=30))
                parts.append(self._text(qx + 60, qy + 50 + ni * 40, 250, 35, name,
                                        font_size=BODY_SIZE, color=DARK_GRAY))
        parts.append(self._text(LM, sgt + sgch - 30, 180, 60, y_label,
                                font_size=SMALL_SIZE, color=MED_GRAY, align='center', valign='middle'))
        parts.append(self._text(sgl + sgcw - 50, sgt + 2 * sgch + 10, 250, 30, x_label,
                                font_size=SMALL_SIZE, color=MED_GRAY, align='center'))
        if summary:
            parts.append(self._abs(LM, 550, CW, 80, bg=BG_GRAY))
            parts.append(self._text(LM + 30, 550, CW - 60, 80, summary,
                                    font_size=BODY_SIZE, color=NAVY, bold=True, valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def decision_tree(self, title, root, branches, right_panel=None, source=''):
        """Decision Tree — root → L1 → L2 hierarchy with connector lines.
        root: (label,).
        branches: list of (L1_title, L1_metric, L1_color, children:list[(name, metric)]).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        L0x = LM + 30
        L0y = 250
        L0w = 220
        L0h = 120
        parts.append(self._abs(L0x, L0y, L0w, L0h, bg=NAVY))
        parts.append(self._text(L0x, L0y, L0w, L0h, root[0],
                                font_size=EMPHASIS_SIZE, color=WHITE, bold=True,
                                align='center', valign='middle'))
        L1x = L0x + L0w + 60
        L1w = 200
        L1h = 90
        for i, (l1_title, l1_metric, l1_color, children) in enumerate(branches):
            L1y = 150 + i * 220
            # Connector L0 -> L1
            conn_s = L0y + L0h // 2
            conn_e = L1y + L1h // 2
            mid_x = L0x + L0w + 30
            parts.append(self._hline(L0x + L0w, conn_s, mid_x - L0x - L0w, LINE_GRAY, 1))
            vy_top = min(conn_s, conn_e)
            vy_h = abs(conn_e - conn_s)
            if vy_h > 0:
                parts.append(self._abs(mid_x, vy_top, 1, vy_h, bg=LINE_GRAY))
            parts.append(self._hline(mid_x, conn_e, L1x - mid_x, LINE_GRAY, 1))
            parts.append(self._abs(L1x, L1y, L1w, L1h, bg=l1_color))
            parts.append(self._text(L1x, L1y, L1w, 50, l1_title,
                                    font_size=BODY_SIZE, color=WHITE, bold=True,
                                    align='center', valign='middle'))
            parts.append(self._text(L1x, L1y + 45, L1w, 40, l1_metric,
                                    font_size=SUB_HEADER_SIZE, color=WHITE, bold=True,
                                    align='center', valign='middle'))
            # L2 children
            L2x = L1x + L1w + 60
            L2w = 200
            L2h = 65
            for li, (c_name, c_metric) in enumerate(children):
                L2y = L1y - 30 + li * 80
                c_start = L1y + L1h // 2
                c_end = L2y + L2h // 2
                mid_x2 = L1x + L1w + 30
                parts.append(self._hline(L1x + L1w, c_start, mid_x2 - L1x - L1w, LINE_GRAY, 0.5))
                vy2_top = min(c_start, c_end)
                vy2_h = abs(c_end - c_start)
                if vy2_h > 0:
                    parts.append(self._abs(mid_x2, vy2_top, 1, vy2_h, bg=LINE_GRAY))
                parts.append(self._hline(mid_x2, c_end, L2x - mid_x2, LINE_GRAY, 0.5))
                parts.append(self._abs(L2x, L2y, L2w, L2h, bg=BG_GRAY))
                parts.append(self._text(L2x + 10, L2y, int(L2w * 0.6), L2h, c_name,
                                        font_size=SMALL_SIZE, color=DARK_GRAY, valign='middle'))
                parts.append(self._text(L2x + int(L2w * 0.6), L2y, int(L2w * 0.4), L2h, c_metric,
                                        font_size=BODY_SIZE, color=NAVY, bold=True,
                                        align='center', valign='middle'))
        if right_panel:
            pt, pp = right_panel
            L3x = L1x + L1w + 60 + 200 + 40
            L3w = CW - (L3x - LM)
            if L3w > 50:
                parts.append(self._abs(L3x, 120, L3w, 450, bg=BG_GRAY))
                parts.append(self._text(L3x + 15, 130, L3w - 30, 30, pt,
                                        font_size=BODY_SIZE, color=NAVY, bold=True))
                pp_list = pp if isinstance(pp, list) else [pp]
                parts.append(self._text(L3x + 15, 170, L3w - 30, 350, pp_list,
                                        font_size=SMALL_SIZE, color=DARK_GRAY))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def metric_comparison(self, title, metrics, source=''):
        """Metric Comparison — before/after row cards with delta badges.
        metrics: list of (label, before_val, after_val, delta_str).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        rh = 95
        mcw = 400
        bx = LM + 50
        ax = LM + 650
        dx = ax + mcw + 30
        parts.append(self._text(bx, 130, mcw, 30, '之前',
                                font_size=13, color=MED_GRAY, align='center'))
        parts.append(self._text(ax, 130, mcw, 30, '之后',
                                font_size=13, color=MED_GRAY, align='center'))
        parts.append(self._text(dx, 130, 150, 30, '变化',
                                font_size=13, color=MED_GRAY, align='center'))
        for i, (label, before, after, delta) in enumerate(metrics):
            ry = 180 + i * rh
            parts.append(self._abs(bx, ry, mcw, rh - 10, bg=BG_GRAY))
            parts.append(self._text(bx + 20, ry, 150, rh - 10, label,
                                    font_size=SMALL_SIZE, color=MED_GRAY, valign='middle'))
            parts.append(self._text(bx + 180, ry, 200, rh - 10, before,
                                    font_size=22, color=DARK_GRAY, bold=True,
                                    align='center', valign='middle'))
            # Arrow
            parts.append(self._text(bx + mcw + 10, ry, 150, rh - 10, '→',
                                    font_size=24, color=LINE_GRAY,
                                    align='center', valign='middle'))
            parts.append(self._abs(ax, ry, mcw, rh - 10, bg=LIGHT_BLUE))
            parts.append(self._text(ax + 20, ry, 150, rh - 10, label,
                                    font_size=SMALL_SIZE, color=ACCENT_BLUE, valign='middle'))
            parts.append(self._text(ax + 180, ry, 200, rh - 10, after,
                                    font_size=22, color=NAVY, bold=True,
                                    align='center', valign='middle'))
            is_pos = delta.startswith('+')
            dc = ACCENT_GREEN if is_pos else ACCENT_RED
            parts.append(self._abs(dx + 10, ry + 15, 120, rh - 35, bg=dc))
            parts.append(self._text(dx + 10, ry + 15, 120, rh - 35, delta,
                                    font_size=EMPHASIS_SIZE, color=WHITE, bold=True,
                                    align='center', valign='middle'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def agenda(self, title, headers, items, footer_text='', source=''):
        """Agenda — table-style meeting agenda.
        headers: list of (label, width_inches_float).
        items: list of (*values, item_type) — type: 'key'|'normal'|'break'.
        """
        p = self._ns()
        parts = [add_action_title(title)]
        hy = 130
        hx = LM
        # Convert Inches to px
        header_widths = [(label, int(w * 100) if isinstance(w, float) else w) for label, w in headers]
        for label, w in header_widths:
            parts.append(self._text(hx, hy, w, 35, label,
                                    font_size=13, color=NAVY, bold=True))
            hx += w
        total_w = sum(w for _, w in header_widths)
        parts.append(self._hline(LM, hy + 35, total_w, BLACK, 0.75))
        rh = 55
        status_w = header_widths[-1][1] if header_widths else 150
        data_headers = header_widths[:-1]
        for i, item in enumerate(items):
            *vals, itype = item
            ry = 180 + i * rh
            if itype == 'break':
                parts.append(self._abs(LM, ry, total_w, rh, bg=BG_GRAY))
            elif itype == 'key':
                parts.append(self._abs(LM, ry, 6, rh, bg=ACCENT_BLUE))
            rx = LM
            for vi, (_, w) in enumerate(data_headers):
                val = vals[vi] if vi < len(vals) else ''
                fc = MED_GRAY if itype == 'break' else DARK_GRAY
                bld = (itype == 'key')
                parts.append(self._text(rx, ry, w, rh, val,
                                        font_size=BODY_SIZE, color=fc, bold=bld, valign='middle'))
                rx += w
            if itype == 'key':
                parts.append(self._abs(rx + 10, ry + 12, 100, rh - 24, bg=LIGHT_BLUE))
                parts.append(self._text(rx + 10, ry, 100, rh, '★ 重点',
                                        font_size=11, color=ACCENT_BLUE, bold=True,
                                        align='center', valign='middle'))
            if i < len(items) - 1:
                parts.append(self._hline(LM, ry + rh, total_w, LINE_GRAY, 0.25))
        if footer_text:
            parts.append(self._text(LM, 610, CW, 30, footer_text,
                                    font_size=10, color=MED_GRAY))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # ADDITIONAL IMAGE LAYOUTS
    # ═══════════════════════════════════════════

    def image_four_points(self, title, image_label, points, source=''):
        """Image + 4 Points — center image with 4 corner cards.
        points: list of 4 (point_title, description, accent_color).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        img_w = 500
        img_h = 240
        img_x = int(SLIDE_WIDTH / 2 - img_w / 2)
        parts.append(f'<div class="image-placeholder" style="position:absolute; left:{img_x}px; top:280px; width:{img_w}px; height:{img_h}px"><span>[ {esc(image_label)} ]</span></div>')
        card_w = 520
        positions = [
            (LM + 50, 130),
            (LM + CW - card_w - 50, 130),
            (LM + 50, 550),
            (LM + CW - card_w - 50, 550),
        ]
        accents = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED]
        for i, (pt_title, desc, *rest) in enumerate(points):
            color = rest[0] if rest else accents[i % 4]
            px, py = positions[i]
            parts.append(self._oval(px, py + 8, str(i + 1), bg=color))
            parts.append(self._text(px + 55, py, 150, 35, pt_title,
                                    font_size=EMPHASIS_SIZE, color=color, bold=True))
            parts.append(self._text(px + 55, py + 35, card_w - 55, 35, desc,
                                    font_size=BODY_SIZE, color=DARK_GRAY))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def case_study_image(self, title, sections, image_label, kpis=None, source=''):
        """Case Study with Image — left text sections + right image + KPIs.
        sections: list of (label, text, accent_color).
        kpis: list of (value, label) or None.
        """
        p = self._ns()
        parts = [add_action_title(title)]
        lw = 650
        ty = 140
        for i, (label, text, color) in enumerate(sections):
            parts.append(self._abs(LM, ty, 6, 100, bg=color))
            parts.append(self._text(LM + 20, ty, 120, 30, label,
                                    font_size=EMPHASIS_SIZE, color=color, bold=True))
            parts.append(self._text(LM + 20, ty + 35, lw - 30, 65, text,
                                    font_size=BODY_SIZE, color=DARK_GRAY))
            ty += 130
        rx = LM + lw + 30
        rw = CW - lw - 30
        parts.append(f'<div class="image-placeholder" style="position:absolute; left:{rx}px; top:140px; width:{rw}px; height:250px"><span>[ {esc(image_label)} ]</span></div>')
        if kpis:
            kpw = int(rw / len(kpis))
            for i, (val, label) in enumerate(kpis):
                kx = rx + i * kpw
                parts.append(self._abs(kx, 420, kpw - 10, 120, bg=BG_GRAY))
                parts.append(self._text(kx, 425, kpw - 10, 60, val,
                                        font_size=SECTION_TITLE_SIZE, color=NAVY, bold=True,
                                        font_family=FONT_STACK_HEADER, align='center'))
                parts.append(self._text(kx, 485, kpw - 10, 40, label,
                                        font_size=SMALL_SIZE, color=MED_GRAY, align='center'))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def quote_bg_image(self, image_label, quote_text, attribution='', source=''):
        """Quote with Background Image — image top + quote bottom."""
        p = self._ns()
        parts = []
        parts.append(f'<div class="image-placeholder" style="position:absolute; left:0; top:0; width:{SLIDE_WIDTH}px; height:350px"><span>[ {esc(image_label)} ]</span></div>')
        parts.append(self._abs(0, 350, SLIDE_WIDTH, 400, bg=WHITE))
        ln_x = LM + 100
        ln_w = CW - 200
        parts.append(self._hline(ln_x, 390, ln_w, NAVY, 1))
        parts.append(self._text(LM + 150, 410, CW - 300, 140, quote_text,
                                font_size=24, color=NAVY, bold=True,
                                align='center', valign='middle'))
        if attribution:
            parts.append(self._text(LM + 150, 550, CW - 300, 40, attribution,
                                    font_size=BODY_SIZE, color=MED_GRAY, align='center'))
        parts.append(self._hline(ln_x, 600, ln_w, NAVY, 1))
        if source:
            parts.append(add_source(source))
        parts.append(add_page_number(p, self.total))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def goals_illustration(self, title, goals, image_label, source=''):
        """Goals with Illustration — left numbered goals + right image.
        goals: list of (goal_title, description, accent_color).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        lw = 650
        ty = 140
        for i, (gtitle, desc, color) in enumerate(goals):
            parts.append(self._abs(LM, ty, 6, 80, bg=color))
            parts.append(self._oval(LM + 25, ty + 15, str(i + 1), bg=color))
            parts.append(self._text(LM + 80, ty, lw - 100, 35, gtitle,
                                    font_size=EMPHASIS_SIZE, color=color, bold=True))
            parts.append(self._text(LM + 80, ty + 35, lw - 100, 45, desc,
                                    font_size=BODY_SIZE, color=DARK_GRAY))
            ty += 120
        rx = LM + lw + 30
        rw = CW - lw - 30
        parts.append(f'<div class="image-placeholder" style="position:absolute; left:{rx}px; top:140px; width:{rw}px; height:480px"><span>[ {esc(image_label)} ]</span></div>')
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # ADDITIONAL SPECIAL LAYOUTS
    # ═══════════════════════════════════════════

    def two_col_image_grid(self, title, items, source=''):
        """Two-Column Image + Text Grid — 2×2 image-text cards.
        items: list of (card_title, description, accent_color, image_label).
        """
        p = self._ns()
        parts = [add_action_title(title)]
        gcw = int(CW / 2 - 15)
        gch = 220
        imgw = 280
        imgh = 180
        ty = 130
        for i, (ctitle, desc, color, img_label) in enumerate(items):
            col = i % 2
            row = i // 2
            cx = LM + col * (gcw + 15)
            cy = ty + row * (gch + 10)
            parts.append(self._abs(cx, cy, gcw, gch, bg=WHITE))
            parts.append(f'<div class="image-placeholder" style="position:absolute; left:{cx + 15}px; top:{cy + 15}px; width:{imgw}px; height:{imgh}px"><span>[ {esc(img_label)} ]</span></div>')
            tx = cx + imgw + 30
            tw = gcw - imgw - 45
            parts.append(self._abs(tx - 5, cy, 6, gch, bg=color))
            parts.append(self._text(tx + 10, cy + 20, tw, 35, ctitle,
                                    font_size=EMPHASIS_SIZE, color=color, bold=True))
            parts.append(self._text(tx + 10, cy + 60, tw, 120, desc,
                                    font_size=BODY_SIZE, color=DARK_GRAY))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def numbered_list_panel(self, title, items, panel=None, source=''):
        """Numbered List + Side Panel — left numbered list + right accent panel.
        items: list of (item_title, description).
        panel: dict with 'subtitle','big_number','big_label','metrics':list[(label,value)].
        """
        p = self._ns()
        parts = [add_action_title(title)]
        nlw = 750
        nty = 130
        for i, (ititle, desc) in enumerate(items):
            ry = nty + i * 85
            parts.append(self._oval(LM, ry + 5, str(i + 1)))
            parts.append(self._text(LM + 60, ry, nlw - 60, 30, ititle,
                                    font_size=15, color=NAVY, bold=True))
            parts.append(self._text(LM + 60, ry + 35, nlw - 60, 40, desc,
                                    font_size=BODY_SIZE, color=DARK_GRAY))
            if i < len(items) - 1:
                parts.append(self._hline(LM + 60, ry + 80, nlw - 80, LINE_GRAY, 0.25))
        if panel:
            nrx = LM + nlw + 30
            nrw = CW - nlw - 30
            parts.append(self._abs(nrx, 130, nrw, 480, bg=NAVY))
            if 'subtitle' in panel:
                parts.append(self._text(nrx + 30, 160, nrw - 60, 30, panel['subtitle'],
                                        font_size=BODY_SIZE, color=LINE_GRAY))
            if 'big_number' in panel:
                parts.append(self._text(nrx + 30, 180, nrw - 60, 60, panel['big_number'],
                                        font_size=36, color=WHITE, bold=True, align='center'))
            if 'big_label' in panel:
                parts.append(self._text(nrx + 30, 250, nrw - 60, 30, panel['big_label'],
                                        font_size=13, color=LINE_GRAY, align='center'))
            parts.append(self._hline(nrx + 30, 310, nrw - 60, '#334455', 0.5))
            metrics = panel.get('metrics', [])
            for mi, (label, val) in enumerate(metrics):
                my = 340 + mi * 70
                parts.append(self._text(nrx + 30, my, nrw - 60, 30, label,
                                        font_size=11, color='#AAAAAA'))
                parts.append(self._text(nrx + 30, my + 30, nrw - 60, 30, val,
                                        font_size=SUB_HEADER_SIZE, color=WHITE, bold=True))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    def multi_bar_panel(self, title, panels, connectors=None, footnotes=None, source=''):
        """Multi-Bar-Panel Chart — 2-3 side-by-side bar chart panels.
        panels: list[dict] each with 'title','unit','legend','categories','values',
                'bar_color','cagr','highlight_idx','highlight_color','value_format'.
        """
        import re
        p = self._ns()
        parts = [add_action_title(title)]
        n_panels = len(panels)
        panel_gap = 25
        total_gap = panel_gap * max(n_panels - 1, 0)
        pw = int((CW - total_gap) / n_panels)
        title_area_top = CONTENT_TOP
        title_area_h = 65
        unit_row_y = title_area_top + title_area_h + 2
        chart_top = unit_row_y + 55
        chart_bot = 585
        chart_h = chart_bot - chart_top
        xaxis_y = chart_bot + 2
        footnote_y = 625
        for pi, panel_data in enumerate(panels):
            px = LM + pi * (pw + panel_gap)
            bar_color = panel_data.get('bar_color', NAVY)
            hl_color = panel_data.get('highlight_color', ACCENT_BLUE)
            hl_idx = set(panel_data.get('highlight_idx', []))
            values = panel_data['values']
            categories = panel_data['categories']
            n_bars = len(values)
            max_val = max(values) if values else 1
            vfmt = panel_data.get('value_format', '{:,.0f}')
            # Panel title with number prefix
            ptitle = panel_data['title']
            # Parse **bold** in title
            segments = re.split(r'(\*\*.*?\*\*)', ptitle)
            title_html = f'<b>{pi + 1}.</b> '
            for seg in segments:
                if seg.startswith('**') and seg.endswith('**'):
                    title_html += f'<b>{esc(seg[2:-2])}</b>'
                elif seg:
                    title_html += esc(seg)
            parts.append(f'<div style="position:absolute; left:{px}px; top:{title_area_top}px; width:{pw}px; height:{title_area_h}px; font-size:{SUB_HEADER_SIZE}px; color:{BLACK}; font-family:{FONT_STACK_BODY}; line-height:1.2; overflow:hidden">{title_html}</div>')
            # Unit + legend
            unit = panel_data.get('unit', '')
            legend = panel_data.get('legend', '')
            ul_text = unit
            if legend:
                ul_text = f'{unit}          {legend}'
            if ul_text:
                parts.append(self._text(px, unit_row_y, pw, 25, ul_text,
                                        font_size=SMALL_SIZE, color=MED_GRAY))
            # CAGR annotations
            cagr_list = panel_data.get('cagr', [])
            bar_area_w = pw - 15
            bar_x_start = px + 5
            bar_spacing = int(bar_area_w / n_bars) if n_bars else 1
            bar_w = int(bar_spacing * 0.72)
            bar_gap_w = int(bar_spacing * 0.28)
            scale_range = max_val if max_val > 0 else 1
            usable_h = int(chart_h * 0.82)
            for ci, cagr in enumerate(cagr_list):
                rate = cagr['rate']
                c_start = cagr['start']
                c_end = cagr['end']
                rate_color = ACCENT_RED if rate.lstrip().startswith('-') else ACCENT_GREEN
                # Bar top Y for start/end
                def _bar_top(idx):
                    v = values[idx]
                    ratio = v / scale_range if scale_range > 0 else 0
                    bh = int(usable_h * ratio)
                    if bh < 5:
                        bh = 5
                    return chart_bot - bh
                start_top = _bar_top(c_start)
                end_top = _bar_top(c_end)
                sx_c = bar_x_start + bar_spacing * c_start + bar_gap_w // 2 + bar_w // 2
                ex_c = bar_x_start + bar_spacing * c_end + bar_gap_w // 2 + bar_w // 2
                arrow_off = 27
                sy = start_top - arrow_off
                ey = end_top - arrow_off
                mid_x = (sx_c + ex_c) // 2
                label_y = min(sy, ey) - 28
                parts.append(self._text(mid_x - 90, label_y, 180, 25, rate,
                                        font_size=EMPHASIS_SIZE, color=rate_color, bold=True,
                                        align='center'))
                # Arrow line using SVG
                parts.append(f'<svg style="position:absolute; left:0; top:0; width:{SLIDE_WIDTH}px; height:{SLIDE_HEIGHT}px; pointer-events:none"><line x1="{sx_c}" y1="{sy}" x2="{ex_c}" y2="{ey}" stroke="{rate_color}" stroke-width="2" marker-end="url(#arrowhead-{pi}-{ci})"/><defs><marker id="arrowhead-{pi}-{ci}" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{rate_color}"/></marker></defs></svg>')
            # Bars
            for bi, val in enumerate(values):
                bx = bar_x_start + bar_spacing * bi + bar_gap_w // 2
                ratio = val / scale_range if scale_range > 0 else 0
                bh = int(usable_h * ratio)
                if bh < 5:
                    bh = 5
                by = chart_bot - bh
                bc = hl_color if bi in hl_idx else bar_color
                parts.append(self._abs(bx, by, bar_w, bh, bg=bc))
                val_text = vfmt.format(val)
                parts.append(self._text(bx - 8, by - 22, bar_w + 16, 22, val_text,
                                        font_size=SMALL_SIZE, color=BLACK, align='center'))
            # X-axis labels
            for bi, cat in enumerate(categories):
                bx = bar_x_start + bar_spacing * bi + bar_gap_w // 2
                parts.append(self._text(bx - 5, xaxis_y, bar_w + 10, 22, cat,
                                        font_size=SMALL_SIZE, color=DARK_GRAY, align='center'))
        # Footnotes
        if footnotes:
            for fi, fn in enumerate(footnotes):
                parts.append(self._text(LM, footnote_y + 18 * fi, CW, 18, fn,
                                        font_size=FOOTNOTE_SIZE, color=MED_GRAY))
        parts.append(self._footer(source))
        self._add_slide(make_slide('\n'.join(parts), f'slide-{p}'))
        return self

    # ═══════════════════════════════════════════
    # SAVE
    # ═══════════════════════════════════════════

    def save(self, outpath):
        """Save presentation as a self-contained HTML file with PPT-browsing experience."""
        outdir = os.path.dirname(outpath)
        if outdir:
            os.makedirs(outdir, exist_ok=True)

        total = self._page

        # Inject slide-number badges into each slide-wrapper
        processed_slides = []
        for i, slide_html in enumerate(self._slides):
            badge = f'<div class="slide-number-badge">{i+1} / {total}</div>'
            # Insert badge right after <div class="slide-wrapper...">
            injected = slide_html.replace(
                '<div class="slide">',
                f'{badge}\n    <div class="slide">',
                1
            )
            processed_slides.append(injected)

        brand = self._cover_title or 'Presentation'
        # Escape HTML entities in title
        brand_safe = brand.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        toolbar_html = f'''<div class="toolbar">
    <span class="toolbar-brand">{brand_safe}</span>
    <button data-mode="scroll" class="active" onclick="setViewMode('scroll')" title="上下滚动浏览">📜 滚动</button>
    <span class="separator"></span>
    <button data-mode="page" onclick="setViewMode('page')" title="点击翻页浏览">📄 翻页</button>
    <span class="separator"></span>
    <button data-mode="presentation" onclick="setViewMode('presentation')" title="全屏演示 (F)">🖥 演示</button>
</div>'''

        nav_html = f'''<div class="nav-bar">
    <button onclick="prevSlide()" title="上一页 (←)">‹</button>
    <span class="slide-counter">1 / {total}</span>
    <button onclick="nextSlide()" title="下一页 (→)">›</button>
</div>'''

        progress_html = '<div class="progress-bar" style="width:0%"></div>'

        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{brand_safe}</title>
    <style>
{get_base_css()}
    </style>
</head>
<body class="scroll-mode">
{toolbar_html}
{progress_html}
<div class="presentation">
{''.join(processed_slides)}
</div>
{nav_html}
{get_presentation_js()}
</body>
</html>'''

        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        size = os.path.getsize(outpath)
        print(f"✅ Saved: {outpath} ({self._page} slides, {size:,} bytes)")
        return outpath
