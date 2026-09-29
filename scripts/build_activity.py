"""Builds assets/activity.svg from live GitHub data.

    GITHUB_TOKEN=... python scripts/build_activity.py
    python scripts/build_activity.py --sample   # offline preview

Runs every day in .github/workflows/refresh-activity.yml.
Private contributions show up as anonymous counts when the profile
setting "Include private contributions" is on.
"""
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

from palette import LIME, MUTED_TEXT, NEON_WHITE, NIGHT, RIM, ZINC
from svgtext import measure, text

LOGIN = os.environ.get("PROFILE_LOGIN", "Jorgi1-1")
ASSETS = Path(__file__).resolve().parent.parent / "assets"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
  }
}
"""


def fetch():
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def sample():
    import random
    random.seed(4)
    weeks = []
    for w in range(53):
        days = []
        for d in range(7):
            n = random.choice([0, 0, 0, 1, 2, 3, 5, 8]) if d not in (0, 6) else random.choice([0, 0, 1])
            day = date(2025, 9, 28).toordinal() + w * 7 + d
            days.append({"contributionCount": n, "date": date.fromordinal(day).isoformat()})
        weeks.append({"contributionDays": days})
    return {
        "followers": {"totalCount": 12},
        "repositories": {"totalCount": 9, "nodes": [
            {"stargazerCount": 2, "languages": {"edges": [
                {"size": 90000, "node": {"name": "TypeScript", "color": "#3178c6"}},
                {"size": 30000, "node": {"name": "CSS", "color": "#663399"}},
                {"size": 12000, "node": {"name": "HCL", "color": "#844FBA"}},
                {"size": 8000, "node": {"name": "Python", "color": "#3572A5"}},
                {"size": 4000, "node": {"name": "Dockerfile", "color": "#384d54"}}]}}]},
        "contributionsCollection": {"contributionCalendar": {
            "totalContributions": sum(d["contributionCount"] for w in weeks for d in w["contributionDays"]),
            "weeks": weeks}},
    }


def streaks(days):
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    # Today may still be empty; don't break the streak for it.
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    for c in reversed(tail):
        if not c:
            break
        current += 1
    return current, longest


def build(user):
    W, H = 1200, 440
    pad = 56
    cc = user["contributionsCollection"]
    cal = cc["contributionCalendar"]
    # With "Include private contributions" on, the calendar already counts
    # private work (anonymized), so the total matches the profile graph.
    total = cal["totalContributions"]
    weeks = cal["weeks"][-53:]
    days = [d for w in weeks for d in w["contributionDays"]]
    current, longest = streaks(days)
    active_days = sum(1 for d in days if d["contributionCount"])

    langs = Counter()
    colors = {}
    stars = 0
    for repo in user["repositories"]["nodes"]:
        stars += repo["stargazerCount"]
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] += e["size"]
            colors[e["node"]["name"]] = e["node"]["color"] or ZINC

    kpis = [
        (f"{total:,}", "CONTRIBUTIONS / YEAR"),
        (f"{active_days}", "ACTIVE DAYS"),
        (f"{longest}", "LONGEST STREAK"),
        (f"{user['repositories']['totalCount']}", "PUBLIC REPOS"),
    ]
    parts = []
    kx = pad
    for value, label in kpis:
        parts.append(text(value, kx, 136, "display-900", 52, LIME if kx == pad else NEON_WHITE))
        parts.append(text(label, kx, 164, "mono-400", 12, ZINC, tracking=0.1))
        kx += max(measure(value, "display-900", 52), measure(label, "mono-400", 12, 0.1)) + 48

    # Languages: a single stacked bar with a legend underneath (top 5).
    grand = sum(langs.values()) or 1
    top = [(n, v) for n, v in langs.most_common(5) if v / grand >= 0.01]
    lang_total = sum(v for _, v in top) or 1
    lx0, lx1 = kx + 16, W - pad
    lw = lx1 - lx0
    if top and lw > 180:
        parts.append(text("LANGUAGES", lx0, 88, "mono-500", 12, ZINC, tracking=0.1))
        x = lx0
        segs = []
        for name, size in top:
            w = lw * size / lang_total
            segs.append(f'<rect x="{x:.1f}" y="104" width="{max(w - 3, 1):.1f}" height="10" rx="3" fill="{colors[name]}"/>')
            x += w
        parts.append("".join(segs))
        ly = 142
        x = lx0
        for name, size in top:
            label = f"{name} {size / lang_total:.0%}"
            wlab = measure(label, "body-400", 14) + 18
            if x + wlab > lx1:
                x = lx0
                ly += 22
            parts.append(f'<circle cx="{x + 4:.1f}" cy="{ly - 5}" r="4" fill="{colors[name]}"/>')
            parts.append(text(label, x + 14, ly, "body-400", 14, MUTED_TEXT))
            x += wlab + 12

    # Contribution heatmap.
    cell, gap = 17, 4
    gx = (W - (len(weeks) * (cell + gap) - gap)) / 2
    gy = 222
    levels = [0, 0.3, 0.52, 0.76, 1.0]
    peak = max((d["contributionCount"] for d in days), default=0) or 1
    rects = []
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            wd = date.fromisoformat(d["date"]).weekday()  # Mon=0
            row = (wd + 1) % 7  # Sun first, like GitHub
            c = d["contributionCount"]
            lvl = 0 if c == 0 else min(4, 1 + int(3 * c / peak + 0.5))
            x = gx + wi * (cell + gap)
            y = gy + row * (cell + gap)
            if lvl == 0:
                rects.append(f'<rect x="{x:.0f}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="#ffffff" fill-opacity="0.05"/>')
            else:
                rects.append(f'<rect x="{x:.0f}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{LIME}" fill-opacity="{levels[lvl]}"/>')
    grid_bottom = gy + 7 * (cell + gap) - gap
    legend_y = grid_bottom + 34
    legend = [text("LESS", W - pad - 168, legend_y, "mono-400", 11, ZINC, tracking=0.1)]
    for i, o in enumerate(levels):
        fill = 'fill="#ffffff" fill-opacity="0.05"' if i == 0 else f'fill="{LIME}" fill-opacity="{o}"'
        legend.append(f'<rect x="{W - pad - 128 + i * 16}" y="{legend_y - 11}" width="12" height="12" rx="3" {fill}/>')
    legend.append(text("MORE", W - pad, legend_y, "mono-400", 11, ZINC, anchor="end", tracking=0.1))
    updated = text(f"LAST 12 MONTHS  ·  CURRENT STREAK {current}  ·  UPDATED {date.today():%Y-%m-%d}",
                   pad, legend_y, "mono-400", 11, ZINC, tracking=0.08)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub activity: {total} contributions in the last year.">
  <title>GitHub activity for {LOGIN}</title>
  <style>
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="28" fill="{NIGHT}" stroke="{RIM}"/>
  {text("ACTIVITY", pad, 60, "mono-500", 13, LIME, tracking=0.12)}
  {text("AUTO-UPDATED DAILY BY GITHUB ACTIONS", W - pad, 60, "mono-400", 13, ZINC, anchor="end", tracking=0.08)}
  {''.join(parts)}
  {''.join(rects)}
  {''.join(legend)}
  {updated}
</svg>
"""
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "activity.svg").write_text(svg)
    print(f"built activity.svg: {total} contributions, {len(langs)} languages")


if __name__ == "__main__":
    build(sample() if "--sample" in sys.argv else fetch())
