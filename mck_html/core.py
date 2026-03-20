"""Low-level HTML rendering primitives for McKinsey HTML Presentation Framework.

All HTML generation, CSS styling, and layout helpers happen here.
Higher-level code should use these helpers to build slides.
"""
import html as html_module
from .constants import *


# ═══════════════════════════════════════════
# CSS FRAMEWORK
# ═══════════════════════════════════════════

def get_base_css():
    """Return the complete CSS stylesheet for McKinsey HTML presentations."""
    return f"""
/* ══════════════════════════════════════════════════════
   McKinsey HTML Presentation Framework — Base Stylesheet
   16:9 Slide-Browsing Experience
   ══════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');

:root {{
    --slide-w: {SLIDE_WIDTH};
    --slide-h: {SLIDE_HEIGHT};
    --slide-ratio: calc(9 / 16);
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{
    font-size: 16px;  /* Normal browser default */
    scroll-behavior: smooth;
}}

body {{
    font-family: Arial, 'Helvetica Neue', sans-serif;
    color: {DARK_GRAY};
    background: #1a1a2e;
    overflow-x: hidden;
    font-size: 16px;
}}

/* Slide internal font context — isolated from page-level styles */
.slide {{
    font-family: {FONT_STACK_BODY};
    font-size: {BODY_SIZE}px;
    color: {DARK_GRAY};
}}

/* ── Scroll Mode: each slide is a 16:9 card ── */
body.scroll-mode {{
    background: #1a1a2e;
    overflow-y: auto;
}}

body.scroll-mode .presentation {{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0 100px 0;
    gap: 32px;
}}

body.scroll-mode .slide-wrapper {{
    width: 90vw;
    max-width: 1200px;
    aspect-ratio: 16 / 9;
    position: relative;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35), 0 2px 8px rgba(0,0,0,0.2);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    scroll-snap-align: center;
}}

body.scroll-mode .slide-wrapper:hover {{
    transform: scale(1.005);
    box-shadow: 0 12px 48px rgba(0,0,0,0.45), 0 4px 12px rgba(0,0,0,0.3);
}}

body.scroll-mode .slide {{
    position: absolute;
    top: 0;
    left: 0;
    width: {SLIDE_WIDTH}px;
    height: {SLIDE_HEIGHT}px;
    transform-origin: top left;
    background: {WHITE};
    overflow: hidden;
}}

/* Slide number badge in scroll mode */
body.scroll-mode .slide-number-badge {{
    position: absolute;
    top: 12px;
    right: 12px;
    background: rgba(0,0,0,0.55);
    color: white;
    font-size: 12px;
    font-family: Arial, sans-serif;
    padding: 4px 10px;
    border-radius: 12px;
    z-index: 10;
    pointer-events: none;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
}}

/* ── Presentation (Fullscreen) Mode ── */
body.presentation-mode {{
    background: black;
    overflow: hidden;
}}

body.presentation-mode .presentation {{
    width: 100vw;
    height: 100vh;
    position: relative;
}}

body.presentation-mode .slide-wrapper {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: none;
    border-radius: 0;
    box-shadow: none;
    overflow: hidden;
}}

body.presentation-mode .slide-wrapper.active {{
    display: flex;
    align-items: center;
    justify-content: center;
}}

body.presentation-mode .slide {{
    position: absolute;
    width: {SLIDE_WIDTH}px;
    height: {SLIDE_HEIGHT}px;
    transform-origin: center center;
    background: {WHITE};
    overflow: hidden;
}}

body.presentation-mode .slide-number-badge {{
    display: none;
}}

/* ── Page (Click-through) Mode ── */
body.page-mode {{
    background: #1a1a2e;
    overflow: hidden;
}}

body.page-mode .presentation {{
    width: 100vw;
    height: 100vh;
    position: relative;
}}

body.page-mode .slide-wrapper {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: none;
    overflow: hidden;
}}

body.page-mode .slide-wrapper.active {{
    display: flex;
    align-items: center;
    justify-content: center;
}}

body.page-mode .slide {{
    position: absolute;
    width: {SLIDE_WIDTH}px;
    height: {SLIDE_HEIGHT}px;
    transform-origin: center center;
    background: {WHITE};
    overflow: hidden;
    border-radius: 4px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}}

body.page-mode .slide-number-badge {{
    display: none;
}}

/* ── Print ── */
@media print {{
    body {{ background: white !important; }}
    .slide-wrapper {{
        width: 100% !important;
        max-width: none !important;
        aspect-ratio: 16 / 9 !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        page-break-after: always;
        margin: 0 !important;
    }}
    .slide {{
        page-break-after: always;
    }}
    .toolbar, .nav-controls {{ display: none !important; }}
}}

/* ── Typography ── */
.title-cover {{
    font-family: {FONT_STACK_HEADER};
    font-size: {COVER_TITLE_SIZE}px;
    font-weight: bold;
    color: {NAVY};
    line-height: 1.2;
}}

.title-section {{
    font-family: {FONT_STACK_HEADER};
    font-size: {SECTION_TITLE_SIZE}px;
    font-weight: bold;
    color: {NAVY};
    line-height: 1.2;
}}

.title-action {{
    font-family: {FONT_STACK_HEADER};
    font-size: {ACTION_TITLE_SIZE}px;
    font-weight: bold;
    color: {BLACK};
    line-height: 1.15;
}}

.text-subheader {{
    font-size: {SUB_HEADER_SIZE}px;
    font-weight: bold;
    line-height: 1.3;
}}

.text-emphasis {{
    font-size: {EMPHASIS_SIZE}px;
    font-weight: bold;
    line-height: 1.3;
}}

.text-body {{
    font-size: {BODY_SIZE}px;
    line-height: 1.5;
    color: {DARK_GRAY};
}}

.text-small {{
    font-size: {SMALL_SIZE}px;
    line-height: 1.4;
    color: {DARK_GRAY};
}}

.text-footnote {{
    font-size: {FOOTNOTE_SIZE}px;
    color: {MED_GRAY};
    line-height: 1.3;
}}

/* ── Common Elements ── */
.action-title-bar {{
    position: absolute;
    left: {LM}px;
    top: {TITLE_TOP}px;
    width: {CW}px;
    height: {TITLE_H}px;
    display: flex;
    align-items: flex-end;
    padding-bottom: 8px;
}}

.action-title-bar::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 0.5px;
    background: {BLACK};
}}

.source-line {{
    position: absolute;
    left: {LM}px;
    top: {SOURCE_Y}px;
    font-size: {FOOTNOTE_SIZE}px;
    color: {MED_GRAY};
}}

.page-number {{
    position: absolute;
    right: {RM}px;
    bottom: 15px;
    font-size: {FOOTNOTE_SIZE}px;
    color: {MED_GRAY};
    text-align: right;
}}

.oval-label {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    background: {NAVY};
    color: {WHITE};
    font-size: 14px;
    font-weight: bold;
    font-family: Arial, sans-serif;
    flex-shrink: 0;
}}

.hline {{
    height: 0.5px;
    background: {BLACK};
}}

.hline-gray {{
    height: 0.5px;
    background: {LINE_GRAY};
}}

.bottom-bar {{
    position: absolute;
    left: {LM}px;
    top: {BOTTOM_BAR_Y}px;
    width: {CW}px;
    height: {BOTTOM_BAR_H}px;
    background: {BG_GRAY};
    display: flex;
    align-items: center;
    padding: 0 20px;
    gap: 15px;
}}

.bottom-bar .bar-label {{
    font-size: {BODY_SIZE}px;
    font-weight: bold;
    color: {NAVY};
    white-space: nowrap;
}}

.bottom-bar .bar-text {{
    font-size: {BODY_SIZE}px;
    color: {DARK_GRAY};
}}

/* ── Image Placeholder ── */
.image-placeholder {{
    background: #D9D9D9;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}}

.image-placeholder::before,
.image-placeholder::after {{
    content: '';
    position: absolute;
    background: #BBBBBB;
}}

.image-placeholder::before {{
    width: 100%;
    height: 0.5px;
    top: 50%;
}}

.image-placeholder::after {{
    width: 0.5px;
    height: 100%;
    left: 50%;
}}

.image-placeholder span {{
    color: #999999;
    font-size: {SMALL_SIZE}px;
    z-index: 1;
    background: #D9D9D9;
    padding: 2px 8px;
}}

/* ── Charts & Visualization ── */
.bar-chart-container {{
    position: relative;
}}

.bar {{
    position: absolute;
    bottom: 0;
}}

.donut-chart {{
    position: relative;
}}

.legend-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}}

.legend-swatch {{
    width: 20px;
    height: 20px;
    flex-shrink: 0;
}}

/* ── Harvey Ball ── */
.harvey-ball {{
    width: 35px;
    height: 35px;
    border-radius: 50%;
    border: 1px solid {NAVY};
    position: relative;
    overflow: hidden;
    background: {BG_GRAY};
}}

.harvey-fill {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: {NAVY};
}}

/* ── Top Toolbar ── */
.toolbar {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 48px;
    background: rgba(15, 15, 30, 0.92);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    z-index: 2000;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 0 20px;
}}

.toolbar-brand {{
    position: absolute;
    left: 20px;
    color: rgba(255,255,255,0.5);
    font-size: 12px;
    font-family: Arial, sans-serif;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.toolbar button {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.75);
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    font-family: Arial, sans-serif;
    transition: all 0.15s ease;
    display: flex;
    align-items: center;
    gap: 5px;
}}

.toolbar button:hover {{
    background: rgba(255,255,255,0.15);
    color: white;
}}

.toolbar button.active {{
    background: rgba(255,255,255,0.2);
    color: white;
    border-color: rgba(255,255,255,0.3);
}}

.toolbar .separator {{
    width: 1px;
    height: 20px;
    background: rgba(255,255,255,0.12);
    margin: 0 6px;
}}

/* ── Bottom Navigation Bar (for page/presentation mode) ── */
.nav-bar {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 52px;
    background: rgba(15, 15, 30, 0.92);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: none;
    align-items: center;
    justify-content: center;
    gap: 16px;
    z-index: 2000;
    border-top: 1px solid rgba(255,255,255,0.08);
}}

body.page-mode .nav-bar,
body.presentation-mode .nav-bar {{
    display: flex;
}}

.nav-bar button {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.75);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
}}

.nav-bar button:hover {{
    background: rgba(255,255,255,0.2);
    color: white;
}}

.nav-bar .slide-counter {{
    color: rgba(255,255,255,0.7);
    font-size: 14px;
    font-family: Arial, sans-serif;
    min-width: 80px;
    text-align: center;
}}

/* ── Progress Bar ── */
.progress-bar {{
    position: fixed;
    top: 48px;
    left: 0;
    height: 3px;
    background: {ACCENT_BLUE};
    z-index: 2001;
    transition: width 0.3s ease;
    border-radius: 0 2px 2px 0;
}}

body.scroll-mode .progress-bar {{
    display: block;
}}

/* Scroll mode top padding for toolbar */
body.scroll-mode .presentation {{
    padding-top: 80px !important;
}}

/* Hide toolbar in fullscreen presentation */
body.presentation-mode .toolbar {{
    display: none;
}}
"""


def get_presentation_js():
    """Return JavaScript for slide navigation — supports scroll, page, and presentation modes."""
    return """
<script>
(function() {
    const SLIDE_W = """ + str(SLIDE_WIDTH) + """;
    const SLIDE_H = """ + str(SLIDE_HEIGHT) + """;
    const wrappers = document.querySelectorAll('.slide-wrapper');
    const slides = document.querySelectorAll('.slide-wrapper > .slide');
    const totalSlides = wrappers.length;
    let currentSlide = 0;
    let currentMode = 'scroll'; // 'scroll' | 'page' | 'presentation'

    /* ── Scaling logic: fit slide inside its wrapper ── */
    function scaleAllSlides() {
        wrappers.forEach((wrapper, i) => {
            const slide = slides[i];
            if (!slide) return;
            let containerW, containerH;
            if (currentMode === 'scroll') {
                containerW = wrapper.offsetWidth;
                containerH = wrapper.offsetHeight;
            } else {
                containerW = window.innerWidth;
                containerH = window.innerHeight;
            }
            if (containerW === 0 || containerH === 0) return;
            const scaleX = containerW / SLIDE_W;
            const scaleY = containerH / SLIDE_H;
            const scale = Math.min(scaleX, scaleY);
            slide.style.transform = `scale(${scale})`;
            // Center the slide
            const offsetX = (containerW - SLIDE_W * scale) / 2;
            const offsetY = (containerH - SLIDE_H * scale) / 2;
            slide.style.left = offsetX + 'px';
            slide.style.top = offsetY + 'px';
            slide.style.transformOrigin = 'top left';
        });
    }

    /* ── Show specific slide (page & presentation modes) ── */
    function showSlide(n) {
        wrappers.forEach(w => w.classList.remove('active'));
        currentSlide = ((n % totalSlides) + totalSlides) % totalSlides;
        wrappers[currentSlide].classList.add('active');
        scaleAllSlides();
        updateCounter();
        updateProgress();
    }

    /* ── Update page counter ── */
    function updateCounter() {
        const counters = document.querySelectorAll('.slide-counter');
        counters.forEach(c => c.textContent = (currentSlide + 1) + ' / ' + totalSlides);
    }

    /* ── Update progress bar ── */
    function updateProgress() {
        const bar = document.querySelector('.progress-bar');
        if (!bar) return;
        if (currentMode === 'scroll') {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            bar.style.width = pct + '%';
        } else {
            const pct = totalSlides > 1 ? (currentSlide / (totalSlides - 1)) * 100 : 100;
            bar.style.width = pct + '%';
        }
    }

    /* ── Mode switching ── */
    function setMode(mode) {
        const body = document.body;
        body.classList.remove('scroll-mode', 'page-mode', 'presentation-mode');
        currentMode = mode;
        body.classList.add(mode + '-mode');

        // Update toolbar buttons
        document.querySelectorAll('.toolbar button[data-mode]').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });

        if (mode === 'scroll') {
            wrappers.forEach(w => w.classList.remove('active'));
            // Scroll to current slide
            if (wrappers[currentSlide]) {
                setTimeout(() => {
                    wrappers[currentSlide].scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 50);
            }
        } else {
            showSlide(currentSlide);
        }

        requestAnimationFrame(() => scaleAllSlides());
    }

    /* ── Detect which slide is centered in scroll mode ── */
    function detectCurrentSlideInScroll() {
        if (currentMode !== 'scroll') return;
        const viewCenter = window.scrollY + window.innerHeight / 2;
        let closest = 0;
        let minDist = Infinity;
        wrappers.forEach((w, i) => {
            const rect = w.getBoundingClientRect();
            const center = window.scrollY + rect.top + rect.height / 2;
            const dist = Math.abs(center - viewCenter);
            if (dist < minDist) {
                minDist = dist;
                closest = i;
            }
        });
        currentSlide = closest;
        updateCounter();
        updateProgress();
    }

    /* ── Keyboard navigation ── */
    document.addEventListener('keydown', function(e) {
        if (currentMode === 'scroll') {
            if (e.key === 'f' || e.key === 'F') {
                e.preventDefault();
                setMode('presentation');
            }
            return;
        }
        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
            e.preventDefault();
            if (currentSlide < totalSlides - 1) showSlide(currentSlide + 1);
        } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
            e.preventDefault();
            if (currentSlide > 0) showSlide(currentSlide - 1);
        } else if (e.key === 'Escape') {
            e.preventDefault();
            setMode('scroll');
        } else if (e.key === 'f' || e.key === 'F') {
            e.preventDefault();
            if (currentMode === 'page') setMode('presentation');
            else if (currentMode === 'presentation') setMode('page');
        }
    });

    /* ── Click slide to enter page mode ── */
    wrappers.forEach((w, i) => {
        w.addEventListener('click', () => {
            if (currentMode === 'scroll') {
                currentSlide = i;
                setMode('page');
            }
        });
    });

    /* ── Resize handler ── */
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(scaleAllSlides, 50);
    });

    /* ── Scroll handler ── */
    let scrollTimer;
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(detectCurrentSlideInScroll, 100);
        updateProgress();
    }, { passive: true });

    /* ── Expose global functions ── */
    window.setViewMode = setMode;
    window.prevSlide = function() { if (currentSlide > 0) showSlide(currentSlide - 1); };
    window.nextSlide = function() { if (currentSlide < totalSlides - 1) showSlide(currentSlide + 1); };

    /* ── Initialize ── */
    setMode('scroll');
    requestAnimationFrame(scaleAllSlides);
    // Re-scale after fonts/images load
    window.addEventListener('load', () => {
        scaleAllSlides();
        updateProgress();
    });
})();
</script>
"""


# ═══════════════════════════════════════════
# HTML ELEMENT HELPERS
# ═══════════════════════════════════════════

def esc(text):
    """HTML-escape text."""
    if isinstance(text, list):
        return '<br>'.join(html_module.escape(str(t)) for t in text)
    return html_module.escape(str(text))


def _style(**kwargs):
    """Build inline CSS style string from keyword args."""
    parts = []
    for k, v in kwargs.items():
        prop = k.replace('_', '-')
        parts.append(f'{prop}: {v}')
    return '; '.join(parts)


def div(content='', cls='', style='', **extra):
    """Create a div element."""
    attrs = ''
    if cls:
        attrs += f' class="{cls}"'
    if style:
        attrs += f' style="{style}"'
    for k, v in extra.items():
        attrs += f' {k.replace("_", "-")}="{v}"'
    return f'<div{attrs}>{content}</div>'


def span(content='', cls='', style=''):
    """Create a span element."""
    attrs = ''
    if cls:
        attrs += f' class="{cls}"'
    if style:
        attrs += f' style="{style}"'
    return f'<span{attrs}>{content}</span>'


# ═══════════════════════════════════════════
# SLIDE-LEVEL HELPERS (used by all layouts)
# ═══════════════════════════════════════════

def make_slide(content, slide_id='', page_num=0, total=0):
    """Wrap content in a slide-wrapper > slide structure for 16:9 scaling."""
    id_attr = f' id="{slide_id}"' if slide_id else ''
    return f'''<div class="slide-wrapper"{id_attr}>
    <div class="slide">
{content}
    </div>
</div>
'''


def add_action_title(text):
    """White background action title bar + separator line."""
    return f'''<div class="action-title-bar">
    <div class="title-action">{esc(text)}</div>
</div>'''


def add_source(text, y=None):
    """Footnote-sized source attribution at bottom."""
    style = f'top: {y}px' if y else ''
    return f'<div class="source-line" style="{style}">{esc(text)}</div>'


def add_page_number(num, total):
    """Page number in bottom-right corner."""
    return f'<div class="page-number">{num}/{total}</div>'


def add_bottom_bar(label, text, y=None):
    """Gray summary bar at bottom with bold label + description."""
    style = f'top: {y}px' if y else ''
    return f'''<div class="bottom-bar" style="{style}">
    <span class="bar-label">{esc(label)}</span>
    <span class="bar-text">{esc(text)}</span>
</div>'''


def add_oval(letter, bg=NAVY, fg=WHITE, size=45):
    """Add a circle label with a letter/number."""
    return f'''<span class="oval-label" style="background:{bg}; color:{fg}; width:{size}px; height:{size}px; font-size:{max(size//3, 12)}px">{esc(str(letter))}</span>'''


def add_hline(color=BLACK, width='100%', thickness='0.5px'):
    """Draw a horizontal line."""
    return f'<div style="width:{width}; height:{thickness}; background:{color}"></div>'


def add_rect(width, height, color, content='', extra_style=''):
    """Add a colored rectangle div."""
    return f'<div style="width:{width}; height:{height}; background:{color}; {extra_style}">{content}</div>'


def add_image_placeholder(width, height, label='Image'):
    """Gray box placeholder for images."""
    return f'''<div class="image-placeholder" style="width:{width}; height:{height}">
    <span>[ {esc(label)} ]</span>
</div>'''


def add_text(text, font_size=BODY_SIZE, color=DARK_GRAY, bold=False,
             align='left', font_family=None, line_height=1.5):
    """Create styled text element."""
    if font_family is None:
        font_family = FONT_STACK_BODY
    weight = 'bold' if bold else 'normal'
    lines = text if isinstance(text, list) else [text]
    content = '<br>'.join(esc(str(l)) for l in lines)
    return f'<div style="font-size:{font_size}px; color:{color}; font-weight:{weight}; font-family:{font_family}; text-align:{align}; line-height:{line_height}">{content}</div>'


def make_donut_svg(segments, cx=120, cy=120, outer_r=100, inner_r=65,
                   center_label='', center_sub=''):
    """Create an SVG donut chart.
    segments: list of (pct_float, color, label)
    """
    paths = []
    import math
    start_angle = -90  # Start from top (12 o'clock)

    for pct, color, label in segments:
        sweep = pct * 360
        end_angle = start_angle + sweep

        # Convert to radians
        s_rad = math.radians(start_angle)
        e_rad = math.radians(end_angle)

        # Outer arc
        ox1, oy1 = cx + outer_r * math.cos(s_rad), cy + outer_r * math.sin(s_rad)
        ox2, oy2 = cx + outer_r * math.cos(e_rad), cy + outer_r * math.sin(e_rad)
        # Inner arc
        ix1, iy1 = cx + inner_r * math.cos(e_rad), cy + inner_r * math.sin(e_rad)
        ix2, iy2 = cx + inner_r * math.cos(s_rad), cy + inner_r * math.sin(s_rad)

        large_arc = 1 if sweep > 180 else 0

        path = (f'M {ox1:.1f} {oy1:.1f} '
                f'A {outer_r} {outer_r} 0 {large_arc} 1 {ox2:.1f} {oy2:.1f} '
                f'L {ix1:.1f} {iy1:.1f} '
                f'A {inner_r} {inner_r} 0 {large_arc} 0 {ix2:.1f} {iy2:.1f} Z')
        paths.append(f'<path d="{path}" fill="{color}" />')
        start_angle = end_angle

    center_html = ''
    if center_label:
        center_html += f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" font-size="24" font-weight="bold" fill="{WHITE}" font-family="Georgia, serif">{esc(center_label)}</text>'
    if center_sub:
        center_html += f'<text x="{cx}" y="{cy + 22}" text-anchor="middle" dominant-baseline="central" font-size="12" fill="{WHITE}" font-family="Arial, sans-serif">{esc(center_sub)}</text>'

    svg_w = cx * 2 + 20
    svg_h = cy * 2 + 20
    return f'''<svg viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" xmlns="http://www.w3.org/2000/svg">
    {''.join(paths)}
    {center_html}
</svg>'''


def make_pie_svg(segments, cx=120, cy=120, radius=110):
    """Create an SVG pie chart.
    segments: list of (pct_float, color, label, sub_label)
    """
    import math
    paths = []
    start_angle = -90

    for pct, color, *_ in segments:
        sweep = pct * 360
        end_angle = start_angle + sweep

        s_rad = math.radians(start_angle)
        e_rad = math.radians(end_angle)

        x1, y1 = cx + radius * math.cos(s_rad), cy + radius * math.sin(s_rad)
        x2, y2 = cx + radius * math.cos(e_rad), cy + radius * math.sin(e_rad)

        large_arc = 1 if sweep > 180 else 0
        path = (f'M {cx} {cy} '
                f'L {x1:.1f} {y1:.1f} '
                f'A {radius} {radius} 0 {large_arc} 1 {x2:.1f} {y2:.1f} Z')
        paths.append(f'<path d="{path}" fill="{color}" />')
        start_angle = end_angle

    svg_w = cx * 2 + 20
    svg_h = cy * 2 + 20
    return f'''<svg viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" xmlns="http://www.w3.org/2000/svg">
    {''.join(paths)}
</svg>'''


def make_gauge_svg(score, cx=200, cy=180, radius=150):
    """Create an SVG gauge (semicircle) chart.
    score: int 0-100
    """
    import math
    segs = [(0.40, ACCENT_RED), (0.30, ACCENT_ORANGE), (0.30, ACCENT_GREEN)]
    inner_r = radius - 15
    paths = []
    start_angle = 180  # Start from left (9 o'clock)

    for pct, color in segs:
        sweep = pct * 180
        end_angle = start_angle + sweep

        s_rad = math.radians(start_angle)
        e_rad = math.radians(end_angle)

        ox1, oy1 = cx + radius * math.cos(s_rad), cy + radius * math.sin(s_rad)
        ox2, oy2 = cx + radius * math.cos(e_rad), cy + radius * math.sin(e_rad)
        ix1, iy1 = cx + inner_r * math.cos(e_rad), cy + inner_r * math.sin(e_rad)
        ix2, iy2 = cx + inner_r * math.cos(s_rad), cy + inner_r * math.sin(s_rad)

        large_arc = 1 if sweep > 180 else 0
        path = (f'M {ox1:.1f} {oy1:.1f} '
                f'A {radius} {radius} 0 {large_arc} 1 {ox2:.1f} {oy2:.1f} '
                f'L {ix1:.1f} {iy1:.1f} '
                f'A {inner_r} {inner_r} 0 {large_arc} 0 {ix2:.1f} {iy2:.1f} Z')
        paths.append(f'<path d="{path}" fill="{color}" />')
        start_angle = end_angle

    # Center score
    center = f'''<circle cx="{cx}" cy="{cy}" r="70" fill="{WHITE}" />
    <text x="{cx}" y="{cy - 5}" text-anchor="middle" dominant-baseline="central" font-size="44" font-weight="bold" fill="{NAVY}" font-family="Georgia, serif">{score}</text>
    <text x="{cx}" y="{cy + 25}" text-anchor="middle" font-size="14" fill="{MED_GRAY}" font-family="Arial, sans-serif">/ 100</text>'''

    return f'''<svg viewBox="0 0 {cx*2+20} {cy+40}" width="{cx*2+20}" height="{cy+40}" xmlns="http://www.w3.org/2000/svg">
    {''.join(paths)}
    {center}
</svg>'''


def make_harvey_ball_html(score, size=35):
    """Create a Harvey Ball indicator (0=empty ... 4=full)."""
    score = max(0, min(4, round(score)))
    if score == 0:
        return f'<div style="width:{size}px;height:{size}px;border-radius:50%;border:1px solid {NAVY};background:{BG_GRAY}"></div>'
    if score == 4:
        return f'<div style="width:{size}px;height-:{size}px;border-radius:50%;background:{NAVY}"></div>'

    # Use conic-gradient for partial fills
    degrees = score * 90
    return f'<div style="width:{size}px;height:{size}px;border-radius:50%;border:1px solid {NAVY};background:conic-gradient({NAVY} {degrees}deg, {BG_GRAY} {degrees}deg)"></div>'
