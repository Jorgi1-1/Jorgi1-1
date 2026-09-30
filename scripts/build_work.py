"""Builds browser-framed previews of shipped sites: assets/work/<name>.svg.

    python scripts/build_work.py

Screenshots live next to them as JPGs and are embedded as data URIs,
because README images are served as <img> and can't load other files.
"""
import base64
from pathlib import Path

from palette import GOLD, LABEL, MINT_LIT, PEACH_LIT, SKY_LIT, card
from svgtext import text

WORK = Path(__file__).resolve().parent.parent / "assets" / "work"

SITES = [
    ("kanso", "kansostudio.com.mx", "OWN STUDIO"),
    ("ceas", "ceas.com.mx", "CLIENT REDESIGN"),
]


def build(name, domain, tag):
    jpg = WORK / f"{name}.jpg"
    data = base64.b64encode(jpg.read_bytes()).decode()
    from PIL import Image  # size of the shot decides the frame height
    w_img, h_img = Image.open(jpg).size
    W = 800
    bar = 52
    inset = 14
    shot_w = W - 2 * inset
    shot_h = round(h_img * shot_w / w_img)
    H = bar + shot_h + inset
    dots = "".join(f'<circle cx="{30 + i * 18}" cy="{bar / 2}" r="5" fill="{c}"/>'
                   for i, c in enumerate((PEACH_LIT, GOLD, MINT_LIT)))
    url_box = (f'<rect x="{W / 2 - 150}" y="{bar / 2 - 14}" width="300" height="28" rx="14" '
               f'fill="#ffffff" fill-opacity="0.05" stroke="#ffffff" stroke-opacity="0.08"/>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Screenshot of {domain}">
  <title>{domain}</title>
  {card(W, H, rx=22)}
  {dots}
  {url_box}
  {text(domain, W / 2, bar / 2 + 5, "mono-400", 13, SKY_LIT, anchor="middle", tracking=0.02)}
  {text(tag, W - 28, bar / 2 + 4, "mono-500", 11, LABEL, anchor="end", tracking=0.12)}
  <clipPath id="shot"><rect x="{inset}" y="{bar}" width="{shot_w}" height="{shot_h}" rx="12"/></clipPath>
  <image x="{inset}" y="{bar}" width="{shot_w}" height="{shot_h}" clip-path="url(#shot)" preserveAspectRatio="xMidYMin slice"
         href="data:image/jpeg;base64,{data}" xlink:href="data:image/jpeg;base64,{data}"/>
</svg>
"""
    (WORK / f"{name}.svg").write_text(svg)


if __name__ == "__main__":
    for site in SITES:
        build(*site)
    print("built", ", ".join(s[0] for s in SITES))
