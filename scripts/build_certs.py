"""Builds assets/certs.svg: an editorial table of credentials.

    python scripts/build_certs.py

All credentials are public on Credly.
"""
from pathlib import Path

from palette import CREAM, GOLD, LABEL, MUTED_TEXT, card
from svgtext import measure, text

ASSETS = Path(__file__).resolve().parent.parent / "assets"

HARNESS = [
    # track, developer, administrator
    ("Continuous Integration", "Jun 2024", "Dec 2024"),
    ("Continuous Delivery & GitOps", "Jul 2024", "Feb 2025"),
    ("Cloud & AI Cost Management", "Oct 2024", "Jul 2025"),
]
GOOGLE = [("Cloud Digital Leader", "Valid until Jul 2029")]

HAIR = 'stroke="#ffffff" stroke-opacity="0.09"'


def build():
    W = 1200
    pad = 64
    parts = []
    total = len(HARNESS) * 2 + len(GOOGLE)

    # Right: the table.
    x0 = 384
    x_dev = 846
    x_adm = W - pad
    y = 100
    parts.append(text("Harness Certified Expert", x0, y, "body-600", 14, MUTED_TEXT))
    parts.append(text("Developer", x_dev, y, "body-400", 14, LABEL, anchor="end"))
    parts.append(text("Administrator", x_adm, y, "body-400", 14, LABEL, anchor="end"))
    y += 22
    parts.append(f'<line x1="{x0}" y1="{y}" x2="{x_adm}" y2="{y}" {HAIR}/>')
    for track, dev, adm in HARNESS:
        y += 50
        parts.append(text(track, x0, y - 4, "body-600", 20, CREAM))
        parts.append(text(dev, x_dev, y - 4, "mono-400", 15, CREAM, anchor="end"))
        parts.append(text(adm, x_adm, y - 4, "mono-400", 15, CREAM, anchor="end"))
        y += 18
        parts.append(f'<line x1="{x0}" y1="{y}" x2="{x_adm}" y2="{y}" {HAIR}/>')

    y += 52
    parts.append(text("Google Cloud", x0, y, "body-600", 14, MUTED_TEXT))
    y += 22
    parts.append(f'<line x1="{x0}" y1="{y}" x2="{x_adm}" y2="{y}" {HAIR}/>')
    for name, note in GOOGLE:
        y += 50
        parts.append(text(name, x0, y - 4, "body-600", 20, CREAM))
        parts.append(text(note, x_adm, y - 4, "mono-400", 15, CREAM, anchor="end"))
        y += 18
        parts.append(f'<line x1="{x0}" y1="{y}" x2="{x_adm}" y2="{y}" {HAIR}/>')

    H = round(y + 64)

    # Left: one large numeral and a short caption, centred on the table.
    block_h = 150 + 22 + 56
    top = (H - block_h) / 2 + 6
    parts.append(text(str(total), pad - 6, top + 140, "display-900", 190, GOLD))
    parts.append(text("credentials", pad, top + 186, "body-600", 22, CREAM))
    parts.append(text("Harness and Google Cloud,", pad, top + 218, "body-400", 16, MUTED_TEXT))
    parts.append(text("all verifiable on Credly.", pad, top + 242, "body-400", 16, MUTED_TEXT))
    assert measure(str(total), "display-900", 190) < x0 - pad

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Certifications: Harness Certified Expert in Continuous Integration, Continuous Delivery and GitOps, and Cloud and AI Cost Management, each at Developer and Administrator level; Google Cloud Digital Leader.">
  <title>Certifications</title>
  {card(W, H)}
  {''.join(parts)}
</svg>
"""
    (ASSETS / "certs.svg").write_text(svg)
    print("built certs.svg")


if __name__ == "__main__":
    build()
