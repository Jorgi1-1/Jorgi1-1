"""Builds the static, animated SVGs used by the profile README.

    python scripts/build_static.py

Outputs assets/hero.svg, assets/pipeline.svg and assets/footer.svg.
"""
from pathlib import Path

from palette import (LIME, MAGENTA, MAUVE, MUTED_TEXT, NEON_WHITE, NIGHT, RIM,
                     SAGE, TOTEM, ZINC, MAUVE_LIT, SAGE_LIT, MAGENTA_LIT)
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


def qull(x, y, size, color=LIME, ground=NIGHT):
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
    name_y = 208
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
    letter_svg = f'    <path fill="url(#shine)" d="{" ".join(letters)}"/>\n' + "\n".join(
        f'    <path class="tube" style="animation-delay:{0.3 + i * 0.09:.2f}s" pathLength="1" d="{d}"/>'
        for i, d in enumerate(letters)
    )

    roles = ["DEVOPS & CLOUD ENGINEER", "FULLSTACK DEVELOPER", "UX/UI DESIGNER"]
    role_colors = [LIME, SAGE_LIT, MAUVE_LIT]
    role_y = 300
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
                   pad, 352, "body-400", 21, MUTED_TEXT)
    meta_left = text("PUEBLA, MX  ·  GMT-6  ·  ES / EN", pad, 412, "mono-400", 14, ZINC, tracking=0.04)
    status = text("OPEN TO FULL-TIME ROLES & FREELANCE", row_right, 412, "mono-500", 14, LIME,
                  anchor="end", tracking=0.04)
    status_w = measure("OPEN TO FULL-TIME ROLES & FREELANCE", "mono-500", 14, 0.04)
    dot_x = row_right - status_w - 16
    url = text("JORGI1-1.GITHUB.IO", pad, 92, "mono-400", 13, ZINC, tracking=0.08)
    index = text("PORTFOLIO / 2026", row_right, 92, "mono-400", 13, ZINC, anchor="end", tracking=0.08)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Jorge Tovar. DevOps and Cloud Engineer, fullstack developer and UX/UI designer.">
  <title>Jorge Tovar: DevOps &amp; Cloud Engineer, Fullstack Developer, UX/UI Designer</title>
  <defs>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
      <stop offset="0" stop-color="{LIME}"/>
      <stop offset="0.42" stop-color="{LIME}"/>
      <stop offset="0.5" stop-color="#f4ffb0"/>
      <stop offset="0.58" stop-color="{LIME}"/>
      <stop offset="1" stop-color="{LIME}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;1 0" keyTimes="0;0.35;1" dur="7s" repeatCount="indefinite"/>
    </linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#ffffff" fill-opacity="0.05"/>
    </pattern>
  </defs>
  <style>
    .tube {{ fill: none; stroke: #f4ffb0; stroke-width: 2px; stroke-linejoin: round; stroke-dasharray: 1 1;
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
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="28" fill="{NIGHT}" stroke="{RIM}"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="28" fill="url(#dots)"/>
  {url}
  {index}
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
  <circle class="pulse" cx="{dot_x:.1f}" cy="407" r="4.5" fill="{LIME}"/>
  {status}
  <g>
{totem}
  </g>
</svg>
"""
    (ASSETS / "hero.svg").write_text(svg)


def pipeline():
    W, H = 1200, 330
    stages = [
        ("01", "DESIGN", "Figma · UX/UI", "Design systems", MAUVE, MAUVE_LIT),
        ("02", "BUILD", "Next.js · TypeScript", "Node.js · PostgreSQL", SAGE, SAGE_LIT),
        ("03", "SECURE", "DevSecOps practice", "Scans in every pipeline", ZINC, NEON_WHITE),
        ("04", "SHIP", "Harness CI/CD", "GitHub Actions", MAGENTA, MAGENTA_LIT),
        ("05", "RUN", "GCP · AWS · GKE", "Terraform · Docker", LIME, LIME),
    ]
    xs = [140 + i * 230 for i in range(5)]
    y = 150
    dur = 10
    track = f'<line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="#ffffff" stroke-opacity="0.14" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>'
    progress = (f'<line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="url(#flow)" stroke-width="2.5" stroke-linecap="round" '
                f'pathLength="1" stroke-dasharray="1 1" class="flow"/>')
    span = xs[-1] - xs[0]
    nodes = []
    for i, (num, name, l1, l2, muted, lit) in enumerate(stages, 1):
        x = xs[i - 1]
        t = (x - xs[0]) / span * 0.7  # pulse runs during first 70% of the loop
        nodes.append(f"""
  <g>
    {text(num, x, y - 50, "mono-400", 13, ZINC, anchor="middle", tracking=0.1)}
    <circle cx="{x}" cy="{y}" r="22" fill="{NIGHT}" stroke="{muted}" stroke-width="2"/>
    <circle cx="{x}" cy="{y}" r="7" fill="{muted}">
      <animate attributeName="fill" values="{muted};{lit};{lit};{muted}" keyTimes="0;{max(t - 0.001, 0):.3f};{min(t + 0.12, 0.97):.3f};1" dur="{dur}s" repeatCount="indefinite"/>
      <animate attributeName="r" values="7;7;10;7;7" keyTimes="0;{max(t - 0.001, 0):.3f};{min(t + 0.03, 0.98):.3f};{min(t + 0.12, 0.99):.3f};1" dur="{dur}s" repeatCount="indefinite"/>
    </circle>
    {text(name, x, y + 66, "display-700", 26, lit, anchor="middle", tracking=0.02)}
    {text(l1, x, y + 96, "body-400", 16, MUTED_TEXT, anchor="middle")}
    {text(l2, x, y + 120, "body-400", 16, MUTED_TEXT, anchor="middle")}
  </g>""")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="How I ship: design, build, secure, ship, run.">
  <title>How I ship: Design, Build, Secure, Ship, Run</title>
  <defs>
    <linearGradient id="flow" x1="{xs[0]}" x2="{xs[-1]}" y1="0" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{MAUVE_LIT}"/><stop offset="0.25" stop-color="{SAGE_LIT}"/>
      <stop offset="0.5" stop-color="{NEON_WHITE}"/><stop offset="0.75" stop-color="{MAGENTA_LIT}"/>
      <stop offset="1" stop-color="{LIME}"/>
    </linearGradient>
  </defs>
  <style>
    .flow {{ animation: flow {dur}s cubic-bezier(.45,0,.55,1) infinite; }}
    @keyframes flow {{ 0% {{ stroke-dashoffset: 1; opacity: 1; }} 70% {{ stroke-dashoffset: 0; opacity: 1; }}
                       88% {{ stroke-dashoffset: 0; opacity: 0; }} 100% {{ stroke-dashoffset: 1; opacity: 0; }} }}
    {REDUCED}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="28" fill="{NIGHT}" stroke="{RIM}"/>
  {text("HOW I SHIP", 56, 56, "mono-500", 13, LIME, tracking=0.12)}
  {text("ONE PERSON, THE WHOLE LIFECYCLE", W - 56, 56, "mono-400", 13, ZINC, anchor="end", tracking=0.08)}
  {track}
  {progress}
  <circle r="5" fill="{NEON_WHITE}">
    <animateMotion path="M{xs[0]} {y}H{xs[-1]}" dur="{dur}s" keyPoints="0;1;1" keyTimes="0;0.7;1" calcMode="spline" keySplines=".45 0 .55 1;0 0 1 1" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.7;0.75;1" dur="{dur}s" repeatCount="indefinite"/>
  </circle>
{''.join(nodes)}
</svg>
"""
    (ASSETS / "pipeline.svg").write_text(svg)


def footer():
    W, H = 1200, 150
    line = "FROM INTERFACE TO INFRASTRUCTURE."
    size = 30
    w = measure(line, "display-900", size, 0.01)
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
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="28" fill="{NIGHT}" stroke="{RIM}"/>
{qull(W / 2 + 26 - w / 2 - 62, 32, 50)}
  {text(line, W / 2 + 26, 76, "display-900", size, LIME, anchor="middle", tracking=0.01)}
  {stripes}
</svg>
"""
    (ASSETS / "footer.svg").write_text(svg)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    hero()
    pipeline()
    footer()
    print("built hero.svg, pipeline.svg, footer.svg")
