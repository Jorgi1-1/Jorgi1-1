"""Text-to-path helpers so every SVG renders the same everywhere.

GitHub serves README images through its camo proxy as <img>, which can't
load web fonts. Converting glyphs to <path> keeps the typography exact.
"""
import re
from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).parent / "fonts"

FONTS = {
    "display-900": "museomoderno-latin-900-normal.woff",
    "display-700": "museomoderno-latin-700-normal.woff",
    "body-400": "schibsted-grotesk-latin-400-normal.woff",
    "body-600": "schibsted-grotesk-latin-600-normal.woff",
    "mono-400": "jetbrains-mono-latin-400-normal.woff",
    "mono-500": "jetbrains-mono-latin-500-normal.woff",
}


@lru_cache(maxsize=None)
def _font(name):
    font = TTFont(FONT_DIR / FONTS[name])
    return font, font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm


def _glyph(cmap, ch):
    return cmap.get(ord(ch)) or cmap.get(ord("?"))


def measure(text, font="body-400", size=16, tracking=0.0):
    """Advance width of `text` in px. `tracking` is in em."""
    f, gs, cmap, upm = _font(font)
    scale = size / upm
    w = 0.0
    for i, ch in enumerate(text):
        w += gs[_glyph(cmap, ch)].width * scale
        if i < len(text) - 1:
            w += tracking * size
    return w


def text_path(text, x, y, font="body-400", size=16, anchor="start", tracking=0.0):
    """Return an SVG path `d` for `text` with its baseline at y."""
    f, gs, cmap, upm = _font(font)
    scale = size / upm
    width = measure(text, font, size, tracking)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    pen = SVGPathPen(gs)
    cursor = x
    for ch in text:
        g = _glyph(cmap, ch)
        tpen = TransformPen(pen, (scale, 0, 0, -scale, cursor, y))
        gs[g].draw(tpen)
        cursor += gs[g].width * scale + tracking * size
    return re.sub(r"\d+\.\d+", lambda m: f"{float(m.group()):.1f}".rstrip("0").rstrip("."), pen.getCommands())


def text(text_, x, y, font="body-400", size=16, fill="#f2f6ff", anchor="start",
         tracking=0.0, extra=""):
    d = text_path(text_, x, y, font, size, anchor, tracking)
    return f'<path d="{d}" fill="{fill}" {extra}/>'
