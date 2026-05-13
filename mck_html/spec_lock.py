"""SpecLock — immutable per-project design contract for mck-html-design v3."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from .constants import (
    NAVY, WHITE, ACCENT_BLUE,
    SLIDE_WIDTH, SLIDE_HEIGHT,
    ACTION_TITLE_SIZE, BODY_SIZE, SMALL_SIZE,
    FONT_STACK_HEADER, FONT_STACK_BODY,
    DARK_GRAY, MED_GRAY, LINE_GRAY, BG_GRAY,
    ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED,
)


# ─────────────────────────────────────────────
# Canvas formats
# ─────────────────────────────────────────────

class CanvasFormat(Enum):
    ppt169     = (1333, 750)   # 16:9 PPT 演示文稿
    story      = (1080, 1920)  # 9:16 短视频/Story
    xhs        = (1242, 1660)  # 3:4 小红书图文
    wechat     = (1080, 1080)  # 1:1 朋友圈/方图
    wechat_hdr = (900,  383)   # 2.35:1 公众号头图

    @property
    def width(self) -> int:
        return self.value[0]

    @property
    def height(self) -> int:
        return self.value[1]


# ─────────────────────────────────────────────
# SpecLock dataclass
# ─────────────────────────────────────────────

@dataclass
class SpecLock:
    """Serialisable design contract for a single HTML presentation project.

    v2 schema: adds audience, style, images, icons, html_constraints,
    page_data, forbidden, and metadata fields for the enhanced pipeline
    (ppt-master integration + ECharts).
    """

    # ── v1 fields (backward-compatible) ──────────

    canvas: Dict = field(default_factory=dict)
    """width, height, format, background_color, brand_color, accent_color"""

    typography: Dict = field(default_factory=dict)
    """font_family, title_size, body_size, small_size, h1_size, h2_size, h3_size, line_height"""

    color_palette: Dict = field(default_factory=dict)
    """primary, secondary, accent, neutrals (list), semantic (dict), chart_series (list)"""

    page_layouts: Dict[str, str] = field(default_factory=dict)
    """page_num (str) → layout method name (str)"""

    page_rhythm: Dict[str, str] = field(default_factory=dict)
    """page_num (str) → "anchor" | "dense" | "breathing" """

    page_charts: Dict[str, dict] = field(default_factory=dict)
    """page_num (str) → chart config dict {engine, type, title, interactive, height, ...}"""

    total_pages: int = 0
    project_name: str = "untitled"

    # ── v2 fields (new, defaults to empty for backward-compat) ──

    audience: Dict = field(default_factory=dict)
    """role (executive|operational|investor|external), context, core_message"""

    style: Dict = field(default_factory=dict)
    """type (mckinsey|brand|creative|mixed), tone, density"""

    images: Dict = field(default_factory=dict)
    """strategy (none|user_provided|ai_generated|placeholder), assets (list), constraints"""

    icons: Dict = field(default_factory=dict)
    """library (lucide|heroicons|phosphor|custom), method (svg_inline|icon_font), inventory (list)"""

    html_constraints: Dict = field(default_factory=dict)
    """responsive, css_framework, js_allowed, accessibility, print_friendly, animation_allowed"""

    page_data: Dict[str, dict] = field(default_factory=dict)
    """page_num (str) → method kwargs dict for Executor (content extracted from source)"""

    forbidden: List[str] = field(default_factory=list)
    """List of forbidden patterns/practices for this project"""

    metadata: Dict = field(default_factory=dict)
    """created_at, schema_version, confirmed_by_user, source_file, etc."""

    # ── serialisation ──────────────────────────

    @classmethod
    def from_dict(cls, d: dict) -> "SpecLock":
        return cls(
            canvas=d.get("canvas", {}),
            typography=d.get("typography", {}),
            color_palette=d.get("color_palette", {}),
            page_layouts=d.get("page_layouts", {}),
            page_rhythm=d.get("page_rhythm", {}),
            page_charts=d.get("page_charts", {}),
            total_pages=d.get("total_pages", 0),
            project_name=d.get("project_name", "untitled"),
            # v2 fields
            audience=d.get("audience", {}),
            style=d.get("style", {}),
            images=d.get("images", {}),
            icons=d.get("icons", {}),
            html_constraints=d.get("html_constraints", {}),
            page_data=d.get("page_data", {}),
            forbidden=d.get("forbidden", []),
            metadata=d.get("metadata", {}),
        )

    def to_dict(self) -> dict:
        d = {
            "schema_version": "2.0",
            "canvas": self.canvas,
            "typography": self.typography,
            "color_palette": self.color_palette,
            "page_layouts": self.page_layouts,
            "page_rhythm": self.page_rhythm,
            "page_charts": self.page_charts,
            "total_pages": self.total_pages,
            "project_name": self.project_name,
        }
        # v2 fields: only include if non-empty (backward-compat)
        if self.audience:
            d["audience"] = self.audience
        if self.style:
            d["style"] = self.style
        if self.images:
            d["images"] = self.images
        if self.icons:
            d["icons"] = self.icons
        if self.html_constraints:
            d["html_constraints"] = self.html_constraints
        if self.page_data:
            d["page_data"] = self.page_data
        if self.forbidden:
            d["forbidden"] = self.forbidden
        if self.metadata:
            d["metadata"] = self.metadata
        return d

    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def from_json(cls, path: str | Path) -> "SpecLock":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)

    # ── validation ─────────────────────────────

    def validate(self) -> List[str]:
        """Return list of validation error strings (empty list = valid)."""
        errors: List[str] = []

        # canvas
        for key in ("width", "height", "format", "background_color", "brand_color", "accent_color"):
            if key not in self.canvas:
                errors.append(f"canvas missing key: {key}")

        if "format" in self.canvas:
            fmt = self.canvas["format"]
            valid_formats = [f.name for f in CanvasFormat]
            if fmt not in valid_formats:
                errors.append(f"canvas.format '{fmt}' not in {valid_formats}")

        # typography
        for key in ("font_family", "title_size", "body_size", "small_size"):
            if key not in self.typography:
                errors.append(f"typography missing key: {key}")

        # color_palette
        for key in ("primary", "secondary", "accent"):
            if key not in self.color_palette:
                errors.append(f"color_palette missing key: {key}")

        # total_pages
        if self.total_pages < 1:
            errors.append(f"total_pages must be >= 1, got {self.total_pages}")

        # page_layouts consistency
        for page_num in self.page_layouts:
            try:
                n = int(page_num)
            except ValueError:
                errors.append(f"page_layouts key '{page_num}' is not an integer string")
                continue
            if n < 1 or n > self.total_pages:
                errors.append(f"page_layouts key {page_num} out of range [1, {self.total_pages}]")

        # page_rhythm values
        valid_rhythms = {"anchor", "dense", "breathing"}
        for page_num, rhythm in self.page_rhythm.items():
            if rhythm not in valid_rhythms:
                errors.append(f"page_rhythm[{page_num}] = '{rhythm}' not in {valid_rhythms}")

        return errors


# ─────────────────────────────────────────────
# Factory: McKinsey defaults
# ─────────────────────────────────────────────

# McKinsey brand colours (task spec values)
_MCK_PRIMARY   = "#172B4D"   # deep navy
_MCK_SECONDARY = "#0073B6"   # mid blue
_MCK_ACCENT    = "#00AEEF"   # sky blue


def create_default_spec(
    format: str = "ppt169",
    project_name: str = "untitled",
    total_pages: int = 10,
) -> SpecLock:
    """Return a SpecLock pre-filled with McKinsey design defaults."""
    fmt = CanvasFormat[format]

    return SpecLock(
        canvas={
            "width": fmt.width,
            "height": fmt.height,
            "format": format,
            "background_color": WHITE,
            "brand_color": _MCK_PRIMARY,
            "accent_color": _MCK_ACCENT,
        },
        typography={
            "font_family": FONT_STACK_BODY,
            "title_size": ACTION_TITLE_SIZE,
            "body_size": BODY_SIZE,
            "small_size": SMALL_SIZE,
        },
        color_palette={
            "primary":   _MCK_PRIMARY,
            "secondary": _MCK_SECONDARY,
            "accent":    _MCK_ACCENT,
            "neutrals": [WHITE, BG_GRAY, LINE_GRAY, MED_GRAY, DARK_GRAY],
            "semantic": {
                "success": ACCENT_GREEN,
                "warning": ACCENT_ORANGE,
                "danger":  ACCENT_RED,
                "info":    ACCENT_BLUE,
            },
        },
        page_layouts={},
        page_rhythm={},
        page_charts={},
        total_pages=total_pages,
        project_name=project_name,
    )
