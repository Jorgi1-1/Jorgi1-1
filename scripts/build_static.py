"""Builds the static, animated SVGs used by the profile README.

    python scripts/build_static.py

Outputs assets/hero.svg, assets/pipeline.svg and assets/footer.svg.
"""
from pathlib import Path

from palette import (BODY, GOLD_SOFT, LIME, MAGENTA, MAUVE, MUTED_TEXT, NEON_WHITE, NIGHT,
                     SAGE, TOTEM, ZINC, MAUVE_LIT, SAGE_LIT, MAGENTA_LIT, card)
from svgtext import measure, text, text_path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# Qull, the portfolio's resident ink drop, in its rest pose (viewBox -4 -8 108 108).
QULL = {
    "body": "M57 5.36C58.01 5.43 62.18 14.48 65 19.4C68.14 24.87 72.51 30.48 75 36.68C77.56 43.06 79.34 50.31 80 57.2C80.65 63.99 81.13 71.94 79 77.72C77.1 82.88 73.52 87.79 69 90.68C64.07 93.83 56.35 94.83 50 95C43.68 95.17 35.92 94.72 31 91.76C26.47 89.03 22.89 83.9 21 78.8C18.94 73.24 19.16 65.67 20 59.36C20.84 53.07 22.94 46.45 26 41C28.99 35.68 34.09 31.13 38 26.96C41.4 23.34 45.19 20.42 48 17.24C50.9 13.96 56.03 5.3 57 5.36Z",
    "eyes": "M36.8 61A4.2 6.6 0 1 1 45.2 61A4.2 6.6 0 1 1 36.8 61ZM55.3 60.3A3.7 6 0 1 1 62.7 60.3A3.7 6 0 1 1 55.3 60.3Z",
    "mouth": "M48.7 69.5A1.8 1.35 0 1 1 52.3 69.5A1.8 1.35 0 1 1 48.7 69.5Z",
    "limbs": "M7.21 69.02A8.3 11.5 10 1 1 23.56 71.9A8.3 11.5 10 1 1 7.21 69.02ZM76.44 71.9A8.3 11.5 -10 1 1 92.79 69.02A8.3 11.5 -10 1 1 76.44 71.9ZM36.25 85.75L41.75 85.75A6.75 6.75 0 0 1 41.75 99.25L36.25 99.25A6.75 6.75 0 0 1 36.25 85.75ZM58.25 85.75L63.75 85.75A6.75 6.75 0 0 1 63.75 99.25L58.25 99.25A6.75 6.75 0 0 1 58.25 85.75Z",
    "spark": "M52 0C55 33 67 45 100 52C66 55 55 67 47 100C45 66 33 55 0 48C34 44 46 33 52 0Z",
}

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def qull(x, y, size, color=LIME, ground=BODY):
    """Qull standing in a square box of `size` px whose top-left is (x, y)."""
    s = size / 108
    return f"""
  <g transform="translate({x:.1f} {y:.1f}) scale({s:.4f}) translate(4 8)">
    <g class="qull-bob">
      <path d="{QULL['limbs']}" fill="{ground}" stroke="{color}" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="{QULL['body']}" fill="{ground}" stroke="{color}" stroke-width="2.6" stroke-linejoin="round"/>
      <path class="qull-eyes" d="{QULL['eyes']}" fill="{color}"/>
      <path d="{QULL['mouth']}" fill="{color}"/>
      <g transform="translate(22 7) rotate(10) scale(0.18) translate(-50 -50)">
        <path class="qull-spark" d="{QULL['spark']}" fill="{color}"/>
      </g>
    </g>
  </g>"""


def hero():
    W, H = 1200, 470
    pad = 64
    totem_x = W - pad - 14
    row_right = totem_x - 44

    # Name row: JORGE flush left, TOVAR flush right, Qull in between.
    base = 100
    wj = measure("JORGE", "display-900", base, -0.01)
    wt = measure("TOVAR", "display-900", base, -0.01)
    avail = row_right - pad
    size = avail / ((wj + wt) / base + 1.05)
    name_y = 196
    letters = []
    cx = pad
    for word, start in (("JORGE", pad), ("TOVAR", row_right - measure("TOVAR", "display-900", size, -0.01))):
        cx = start
        for ch in word:
            d = text_path(ch, cx, name_y, "display-900", size)
            letters.append(d)
            cx += measure(ch, "display-900", size) - 0.01 * size
    qsize = size * 1.02
    qx = pad + measure("JORGE", "display-900", size, -0.01) + (avail - measure("JORGE", "display-900", size, -0.01) - measure("TOVAR", "display-900", size, -0.01) - qsize) / 2
    qy = name_y - qsize * 0.93

    # The fill is always there, so the name reads even where SVG animation
    # doesn't run (thumbnails, throttled tabs). A neon outline traces over it.
    letter_svg = f'    <path fill="{LIME}" d="{" ".join(letters)}"/>\n' + "\n".join(
        f'    <path class="tube" style="animation-delay:{0.3 + i * 0.09:.2f}s" pathLength="1" d="{d}"/>'
        for i, d in enumerate(letters)
    )

    roles = ["DEVOPS & CLOUD ENGINEER", "FULLSTACK DEVELOPER", "UX/UI DESIGNER"]
    role_colors = [NEON_WHITE] * 3
    role_y = 290
    role_size = 50
    role_svg = "\n".join(
        f'    <g class="role role-{i}">{text(r, pad, role_y, "display-700", role_size, c, tracking=0.01)}</g>'
        for i, (r, c) in enumerate(zip(roles, role_colors))
    )

    stripe_h = (H - 2 * 56 - 3 * 10) / 4
    totem = "\n".join(
        f'    <rect class="stripe s{i}" x="{totem_x}" y="{56 + i * (stripe_h + 10):.1f}" width="14" height="{stripe_h:.1f}" rx="7" fill="{muted}" style="--lit:{lit}"/>'
        for i, (muted, lit) in enumerate(TOTEM)
    )

    tagline = text("From interface to infrastructure. I design it, build it, and keep it running.",
                   pad, 342, "body-400", 21, MUTED_TEXT)
    meta_left = text("Puebla, Mexico  ·  jorgi1-1.github.io", pad, 414, "body-400", 16, MUTED_TEXT)
    status_txt = "Open to full-time roles and freelance"
    status = text(status_txt, row_right, 414, "body-600", 16, LIME, anchor="end")
    dot_x = row_right - measure(status_txt, "body-600", 16) - 14

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Jorge Tovar. DevOps and Cloud Engineer, fullstack developer and UX/UI designer.">
  <title>Jorge Tovar: DevOps &amp; Cloud Engineer, Fullstack Developer, UX/UI Designer</title>
  <defs>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
      <stop offset="0" stop-color="{LIME}"/>
      <stop offset="0.42" stop-color="{LIME}"/>
      <stop offset="0.5" stop-color="{GOLD_SOFT}"/>
      <stop offset="0.58" stop-color="{LIME}"/>
      <stop offset="1" stop-color="{LIME}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;1 0" keyTimes="0;0.35;1" dur="7s" repeatCount="indefinite"/>
    </linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#ffffff" fill-opacity="0.05"/>
    </pattern>
  </defs>
  <style>
    .tube {{ fill: none; stroke: {GOLD_SOFT}; stroke-width: 2px; stroke-linejoin: round; stroke-dasharray: 1 1;
            stroke-dashoffset: 1; filter: drop-shadow(0 0 4px {LIME}); animation: tube 9s cubic-bezier(.6,0,.2,1) infinite; }}
    @keyframes tube {{ 0% {{ stroke-dashoffset: 1; opacity: 1; }} 16% {{ stroke-dashoffset: 0; opacity: 1; }}
                       26%, 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
    .role {{ opacity: 0; animation: role 9s infinite; }}
    .role-0 {{ opacity: 1; animation-delay: 0s; }}
    .role-1 {{ animation-delay: 3s; }}
    .role-2 {{ animation-delay: 6s; }}
    @keyframes role {{ 0% {{ opacity: 0; transform: translateY(10px); }} 5%, 30% {{ opacity: 1; transform: none; }}
                       35%, 100% {{ opacity: 0; transform: translateY(-8px); }} }}
    .role-0 {{ animation-name: role0; }}
    @keyframes role0 {{ 0%, 30% {{ opacity: 1; transform: none; }} 35%, 95% {{ opacity: 0; transform: translateY(-8px); }} 100% {{ opacity: 1; transform: none; }} }}
    .stripe {{ animation: lit 8s infinite; }}
    .s1 {{ animation-delay: 2s; }} .s2 {{ animation-delay: 4s; }} .s3 {{ animation-delay: 6s; }}
    @keyframes lit {{ 0%, 22%, 100% {{ fill-opacity: 1; filter: none; }} 6%, 16% {{ fill: var(--lit); filter: drop-shadow(0 0 6px var(--lit)); }} }}
    .qull-bob {{ animation: bob 3.2s ease-in-out infinite; }}
    @keyframes bob {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2.5px); }} }}
    .qull-eyes {{ transform-box: fill-box; transform-origin: center; animation: blink 5s infinite; }}
    @keyframes blink {{ 0%, 90%, 100% {{ transform: scaleY(1); }} 94% {{ transform: scaleY(0.1); }} }}
    .qull-spark {{ transform-box: fill-box; transform-origin: center; animation: spin 6s linear infinite; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    .pulse {{ animation: pulse 2s ease-in-out infinite; }}
    @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
    {REDUCED}
  </style>
  {card(W, H)}
  <g>
{letter_svg}
  </g>
{qull(qx, qy, qsize)}
  <g>
{role_svg}
  </g>
  {tagline}
  <line x1="{pad}" y1="384" x2="{row_right}" y2="384" stroke="#ffffff" stroke-opacity="0.08"/>
  {meta_left}
  <circle class="pulse" cx="{dot_x:.1f}" cy="408.5" r="4" fill="{LIME}"/>
  {status}
  <g>
{totem}
  </g>
</svg>
"""
    (ASSETS / "hero.svg").write_text(svg)


def pipeline():
    W, H = 1200, 300
    stages = [
        ("01", "Design", "Figma, UX/UI", "design systems"),
        ("02", "Build", "Next.js, TypeScript", "Node.js, PostgreSQL"),
        ("03", "Secure", "DevSecOps practice,", "scans in every pipeline"),
        ("04", "Ship", "Harness CI/CD", "GitHub Actions"),
        ("05", "Run", "GCP, AWS, GKE", "Terraform, Docker"),
    ]
    pad = 64
    col = (W - 2 * pad) / len(stages)
    xs = [pad + i * col for i in range(len(stages))]
    y = 132
    dur = 10
    end_x = xs[-1] + col - 24
    track = f'<line x1="{xs[0]}" y1="{y}" x2="{end_x}" y2="{y}" stroke="#ffffff" stroke-opacity="0.12"/>'
    progress = (f'<line x1="{xs[0]}" y1="{y}" x2="{end_x}" y2="{y}" stroke="{LIME}" stroke-width="1.5" '
                f'pathLength="1" stroke-dasharray="1 1" class="flow"/>')
    span = end_x - xs[0]
    nodes = []
    for i, (num, name, l1, l2) in enumerate(stages):
        x = xs[i]
        t = (x - xs[0]) / span * 0.7  # the light passes during the first 70% of the loop
        on = f"0;{max(t - 0.001, 0):.3f};{min(t + 0.14, 0.97):.3f};1"
        nodes.append(f"""
  <g>
    {text(num, x, y - 26, "mono-400", 13, ZINC)}
    <rect x="{x - 0.5}" y="{y - 7}" width="9" height="14" rx="1.5" fill="{ZINC}">
      <animate attributeName="fill" values="{ZINC};{LIME};{LIME};{ZINC}" keyTimes="{on}" dur="{dur}s" repeatCount="indefinite"/>
    </rect>
    {text(name, x, y + 52, "body-600", 22, NEON_WHITE)}
    {text(l1, x, y + 82, "body-400", 15, MUTED_TEXT)}
    {text(l2, x, y + 104, "body-400", 15, MUTED_TEXT)}
  </g>""")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="How I ship: design, build, secure, ship, run.">
  <title>How I ship: Design, Build, Secure, Ship, Run</title>
  <style>
    .flow {{ animation: flow {dur}s cubic-bezier(.45,0,.55,1) infinite; }}
    @keyframes flow {{ 0% {{ stroke-dashoffset: 1; opacity: 1; }} 70% {{ stroke-dashoffset: 0; opacity: 1; }}
                       88% {{ stroke-dashoffset: 0; opacity: 0; }} 100% {{ stroke-dashoffset: 1; opacity: 0; }} }}
    {REDUCED}
  </style>
  {card(W, H)}
  {text("How I ship", pad, 58, "body-600", 16, MUTED_TEXT)}
  {track}
  {progress}
{''.join(nodes)}
</svg>
"""
    (ASSETS / "pipeline.svg").write_text(svg)


def footer():
    W, H = 1200, 140
    line = "From interface to infrastructure."
    size = 30
    w = measure(line, "display-700", size)
    stripes = "".join(
        f'<rect x="{W / 2 - 66 + i * 34}" y="104" width="28" height="6" rx="3" fill="{muted}"/>'
        for i, (muted, _) in enumerate(TOTEM)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="From interface to infrastructure.">
  <title>From interface to infrastructure.</title>
  <style>
    .qull-bob {{ animation: bob 3.2s ease-in-out infinite; }}
    @keyframes bob {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
    .qull-eyes {{ transform-box: fill-box; transform-origin: center; animation: blink 5s infinite; }}
    @keyframes blink {{ 0%, 90%, 100% {{ transform: scaleY(1); }} 94% {{ transform: scaleY(0.1); }} }}
    .qull-spark {{ transform-box: fill-box; transform-origin: center; animation: spin 6s linear infinite; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    {REDUCED}
  </style>
  {card(W, H)}
{qull(W / 2 + 26 - w / 2 - 66, 40, 52)}
  {text(line, W / 2 + 26, 84, "display-700", size, LIME, anchor="middle")}
</svg>
"""
    (ASSETS / "footer.svg").write_text(svg)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    hero()
    pipeline()
    footer()
    print("built hero.svg, pipeline.svg, footer.svg")
