"""Builds assets/certs.svg: Harness track x level matrix plus Google Cloud.

    python scripts/build_certs.py

Credentials are listed in CERTS below; all are public on Credly.
"""
from pathlib import Path

from palette import (CREAM, GOLD, LABEL, MINT_LIT, MUTED_TEXT, PEACH_LIT, SKY_LIT, card)
from svgtext import measure, text

ASSETS = Path(__file__).resolve().parent.parent / "assets"

HARNESS = [
    # track, color, developer date, administrator date
    ("Continuous Integration", SKY_LIT, "Jun 2024", "Dec 2024"),
    ("Continuous Delivery & GitOps", MINT_LIT, "Jul 2024", "Feb 2025"),
    ("Cloud & AI Cost Management", PEACH_LIT, "Oct 2024", "Jul 2025"),
]
GOOGLE = [
    ("Cloud Digital Leader", "Google Cloud Certified", "Valid until Jul 2029", "seal"),
]

SHIELD = "M4 0H28Q32 0 32 4V19Q32 30 16 38Q0 30 0 19V4Q0 0 4 0Z"
STAR = "M5 0L6.2 3.4L9.8 3.5L7 5.7L8 9.2L5 7.2L2 9.2L3 5.7L0.2 3.5L3.8 3.4Z"


def shield(x, y, color, stars):
    st = "".join(
        f'<path d="{STAR}" transform="translate({16 - 6 * stars + 1 + i * 12} 13)" fill="{GOLD}"/>'
        for i in range(stars))
    return (f'<g transform="translate({x} {y})"><path d="{SHIELD}" fill="{color}" fill-opacity="0.16" '
            f'stroke="{color}" stroke-width="2"/>{st}</g>')


def build():
    W, H = 1200, 470
    pad = 56
    parts = [
        text("CERTIFICATIONS", pad, 60, "mono-500", 13, GOLD, tracking=0.12),
        text("7 CREDENTIALS  ·  VERIFIED ON CREDLY", W - pad, 60, "mono-400", 13, LABEL, anchor="end", tracking=0.08),
    ]

    # Harness matrix
    col_dev, col_adm = 470, 640
    parts += [
        text("HARNESS CERTIFIED EXPERT", pad, 118, "mono-500", 12, MUTED_TEXT, tracking=0.1),
        text("DEVELOPER", col_dev, 118, "mono-400", 12, LABEL, tracking=0.1),
        text("ADMINISTRATOR", col_adm, 118, "mono-400", 12, LABEL, tracking=0.1),
    ]
    row_y = 150
    for track, color, dev, adm in HARNESS:
        parts.append(f'<rect x="{pad}" y="{row_y}" width="{760 - pad}" height="78" rx="16" fill="#ffffff" fill-opacity="0.03" stroke="#ffffff" stroke-opacity="0.06"/>')
        parts.append(f'<rect x="{pad}" y="{row_y + 18}" width="4" height="42" rx="2" fill="{color}"/>')
        parts.append(text(track, pad + 24, row_y + 46, "body-600", 20, CREAM))
        for cx, date, stars in ((col_dev, dev, 1), (col_adm, adm, 2)):
            parts.append(shield(cx, row_y + 20, color, stars))
            parts.append(text(date, cx + 46, row_y + 45, "mono-400", 14, MUTED_TEXT))
        row_y += 94

    # Google Cloud column
    gx = 800
    parts.append(f'<line x1="{gx - 20}" y1="100" x2="{gx - 20}" y2="{row_y - 16}" stroke="#ffffff" stroke-opacity="0.08"/>')
    parts.append(text("GOOGLE CLOUD", gx + 4, 118, "mono-500", 12, MUTED_TEXT, tracking=0.1))
    gy = 150
    col_w = W - pad - gx
    card_h = (row_y - 16 - 150 - 16 * (len(GOOGLE) - 1)) / len(GOOGLE)
    cx = gx + col_w / 2
    for name, kind, date, icon in GOOGLE:
        parts.append(f'<rect x="{gx}" y="{gy}" width="{col_w}" height="{card_h:.0f}" rx="16" fill="#ffffff" fill-opacity="0.03" stroke="#ffffff" stroke-opacity="0.06"/>')
        sy = gy + 78
        parts.append(f'<circle cx="{cx}" cy="{sy}" r="40" fill="none" stroke="{GOLD}" stroke-width="2"/>'
                     f'<circle cx="{cx}" cy="{sy}" r="29" fill="{GOLD}" fill-opacity="0.14" stroke="{GOLD}" stroke-width="1.4" stroke-dasharray="2 4"/>'
                     f'<path d="{STAR}" transform="translate({cx - 10} {sy - 10}) scale(2)" fill="{GOLD}"/>')
        parts.append(text(name, cx, gy + 162, "body-600", 21, CREAM, anchor="middle"))
        parts.append(text(kind, cx, gy + 188, "body-400", 15, MUTED_TEXT, anchor="middle"))
        parts.append(text(date.upper(), cx, gy + card_h - 26, "mono-400", 12, LABEL, anchor="middle", tracking=0.08))
        gy += card_h + 16

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Certifications: six Harness Certified Expert credentials (Continuous Integration, Continuous Delivery and GitOps, Cloud and AI Cost Management, each at Developer and Administrator level), plus Google Cloud Digital Leader.">
  <title>Certifications</title>
  {card(W, H)}
  {''.join(parts)}
</svg>
"""
    (ASSETS / "certs.svg").write_text(svg)
    print("built certs.svg")


if __name__ == "__main__":
    build()
