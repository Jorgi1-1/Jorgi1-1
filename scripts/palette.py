"""Profile palette "Noche": night navy grounds with warm gold light.

Matches the Qull avatar (assets/avatar). The old portfolio token names are
kept as aliases so the generators read the same.
"""

# Grounds
NAVY_TOP = "#1f2c47"
NAVY = "#131c30"
NAVY_DEEP = "#080c17"
NIGHT = NAVY             # card ground
BODY = "#0b0f1a"         # Qull's ink body on navy
RIM = "#ffffff14"

# Light
GOLD = "#ffd88a"
GOLD_SOFT = "#fff1cf"
AMBER = "#ffb347"
CREAM = "#f3ead8"
MUTED_TEXT = "#aab4c8"
LABEL = "#7f8aa3"

# Accents (muted on the totem, lit in use)
PEACH, PEACH_LIT = "#b98a74", "#ffb99a"
SKY, SKY_LIT = "#6d84b8", "#a9c1ff"
MINT, MINT_LIT = "#5b9488", "#8fe0cb"

# Aliases used by the generators
LIME = GOLD
NEON_WHITE = CREAM
ZINC = LABEL
MAUVE, MAUVE_LIT = PEACH, PEACH_LIT
SAGE, SAGE_LIT = SKY, SKY_LIT
MAGENTA, MAGENTA_LIT = MINT, MINT_LIT

TOTEM = [(PEACH, PEACH_LIT), (GOLD, GOLD), (SKY, SKY_LIT), (MINT, MINT_LIT)]


def card(w, h, rx=28):
    """Card ground: a quiet navy fade and a neutral hairline."""
    return f"""<defs>
    <linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{NAVY_TOP}"/>
      <stop offset="1" stop-color="{NAVY}"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="url(#card)" stroke="{RIM}"/>"""
