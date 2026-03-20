"""McKinsey Design System — Color palette, typography, and layout constants for HTML output."""

# ═══════════════════════════════════════════
# COLOR PALETTE (CSS hex strings)
# ═══════════════════════════════════════════

# Primary colors
NAVY       = '#051C2C'
BLACK      = '#000000'
WHITE      = '#FFFFFF'

# Gray scale
DARK_GRAY  = '#333333'
MED_GRAY   = '#666666'
LINE_GRAY  = '#CCCCCC'
BG_GRAY    = '#F2F2F2'

# Accent colors (for 3+ parallel items)
ACCENT_BLUE   = '#006BA6'
ACCENT_GREEN  = '#007A53'
ACCENT_ORANGE = '#D46A00'
ACCENT_RED    = '#C62828'

# Light accent backgrounds
LIGHT_BLUE    = '#E3F2FD'
LIGHT_GREEN   = '#E8F5E9'
LIGHT_ORANGE  = '#FFF3E0'
LIGHT_RED     = '#FFEBEE'

# Paired accent sets: (accent, light_bg) for easy iteration
ACCENT_PAIRS = [
    (ACCENT_BLUE,   LIGHT_BLUE),
    (ACCENT_GREEN,  LIGHT_GREEN),
    (ACCENT_ORANGE, LIGHT_ORANGE),
    (ACCENT_RED,    LIGHT_RED),
]

# ═══════════════════════════════════════════
# SLIDE DIMENSIONS (CSS units)
# ═══════════════════════════════════════════

SLIDE_WIDTH   = 1333    # px (13.333in × 100)
SLIDE_HEIGHT  = 750     # px (7.5in × 100)
SLIDE_ASPECT  = '16 / 9'

# Margins (px)
LM = 80   # Left margin
RM = 80   # Right margin
CW = 1173  # Content width = SLIDE_WIDTH - LM - RM

# ═══════════════════════════════════════════
# VERTICAL GRID (px)
# ═══════════════════════════════════════════

TITLE_TOP       = 15     # Action title top
TITLE_H         = 90     # Action title height
TITLE_LINE_Y    = 105    # Separator under title
CONTENT_TOP     = 130    # Content area start
SOURCE_Y        = 705    # Source attribution line
PAGE_NUM_X      = 1220   # Page number left
BOTTOM_BAR_Y    = 620    # Default bottom summary bar
BOTTOM_BAR_H    = 65     # Bottom bar height

# ═══════════════════════════════════════════
# TYPOGRAPHY (CSS)
# ═══════════════════════════════════════════

COVER_TITLE_SIZE   = 44
SECTION_TITLE_SIZE = 28
ACTION_TITLE_SIZE  = 22
SUB_HEADER_SIZE    = 18
EMPHASIS_SIZE      = 16
BODY_SIZE          = 14
SMALL_SIZE         = 12
FOOTNOTE_SIZE      = 9

FONT_HEADER = "'Georgia', 'Times New Roman', serif"
FONT_BODY   = "'Arial', 'Helvetica Neue', sans-serif"
FONT_EA     = "'KaiTi', 'STKaiti', 'SimSun', serif"

# Combined font stacks for CSS
FONT_STACK_HEADER = f"{FONT_EA}, {FONT_HEADER}"
FONT_STACK_BODY   = f"{FONT_EA}, {FONT_BODY}"
