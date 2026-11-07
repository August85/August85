"""Generates the SVG images used in the profile README.

Run: python3 assets/build.py   (writes assets/matrix.svg and assets/career.svg)
Edit CAREER below when something changes.
"""
import random
from pathlib import Path

OUT = Path(__file__).parent

# ---------------------------------------------------------------- matrix banner

def matrix():
    rnd = random.Random(85)
    W, H, STEP, TAIL = 880, 190, 22, 12
    glyphs = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFZ:+=*"
    cols = []
    for i, x in enumerate(range(11, W, STEP)):
        dur = rnd.uniform(5, 11)
        delay = -rnd.uniform(0, dur)
        size = rnd.choice([13, 14, 15, 16])
        dim = rnd.uniform(0.35, 0.8)
        chars = []
        for k in range(TAIL):
            y = k * (size + 3)
            op = 0.08 + 0.92 * (k / (TAIL - 1)) ** 1.6
            cls = ' class="h"' if k == TAIL - 1 else ""
            chars.append(f'<text x="{x}" y="{y}" fill-opacity="{op:.2f}"{cls}>{rnd.choice(glyphs)}</text>')
        span = TAIL * (size + 3)
        cols.append(
            f'<g class="c" style="font-size:{size}px;opacity:{dim:.2f};'
            f'animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s;--from:-{span}px;--to:{H + 20}px">'
            + "".join(chars) + "</g>"
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Abhimanyu Katyayan">
<style>
  .c {{ fill:#22c55e; font-family:"MS Gothic","Osaka-Mono",ui-monospace,Menlo,Consolas,monospace; animation-name:fall; animation-timing-function:linear; animation-iteration-count:infinite; }}
  .h {{ fill:#d9ffe4; }}
  @keyframes fall {{ from {{ transform:translateY(var(--from)); }} to {{ transform:translateY(var(--to)); }} }}
  .name {{ font:700 38px -apple-system,"Segoe UI",Helvetica,Arial,sans-serif; fill:#f0fff4; letter-spacing:.5px; }}
  .sub {{ font:500 15px ui-monospace,Menlo,Consolas,monospace; fill:#4ade80; }}
  .cur {{ animation:blink 1.1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity:0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .c, .cur {{ animation:none; }} }}
</style>
<defs>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <radialGradient id="v" cx="50%" cy="50%" r="60%">
    <stop offset="0" stop-color="#05080a" stop-opacity=".92"/>
    <stop offset=".55" stop-color="#05080a" stop-opacity=".55"/>
    <stop offset="1" stop-color="#05080a" stop-opacity="0"/>
  </radialGradient>
</defs>
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="#05080a"/>
  {"".join(cols)}
  <rect width="{W}" height="{H}" fill="url(#v)"/>
</g>
<text class="name" x="{W/2}" y="92" text-anchor="middle">Abhimanyu Katyayan</text>
<text class="sub" x="{W/2}" y="126" text-anchor="middle">&gt; distinguished engineer · ai plumber · polyglot builder<tspan class="cur">_</tspan></text>
</svg>
'''
    (OUT / "matrix.svg").write_text(svg, encoding="utf-8")


# ---------------------------------------------------------------- career timeline

# (company, colour, era label, [(role, start, end)]) ; years as decimals, None = present
CAREER = [
    ("Savitribai Phule Pune Univ.", "#8b949e", "CS foundations", [("BE, Computer Science", 2004.5, 2008.5)]),
    ("Diebold", "#f59e0b", "ATMs &amp; mobile", [
        ("Software Engineer", 2009.17, 2012.17),
        ("Senior Software Engineer", 2012.17, 2013.5)]),
    ("Ugam", "#a855f7", "Big data, NLP &amp; ML at scale", [
        ("Product Engineer", 2013.5, 2015.25),
        ("Tech Lead", 2015.25, 2018.25),
        ("Associate Technical Architect", 2018.25, 2019.38)]),
    ("Walmart Global Tech India", "#0ea5e9", "Cloud data platforms", [
        ("Staff Software Engineer", 2019.38, 2022.38),
        ("Principal Software Engineer", 2022.38, 2023.83)]),
    ("Walmart Global Tech, Bay Area", "#2563eb", "GenAI &amp; AI agents", [
        ("Principal Software Engineer", 2024.42, 2026.67),
        ("Distinguished Engineer", 2026.67, None)]),
]
NOW = 2026.85


def career():
    W, LEFT, RIGHT, TOP, ROW = 880, 270, 850, 58, 30
    Y0, Y1 = 2004, 2027
    sx = lambda y: LEFT + (y - Y0) / (Y1 - Y0) * (RIGHT - LEFT)
    roles = [(c, col, r, s, e if e else NOW) for c, col, _, rs in CAREER for r, s, e in rs]
    roles.reverse()  # latest on top: a climbing staircase
    n = len(roles)
    plot_bottom = TOP + n * ROW
    H = plot_bottom + 118

    out = []
    # year grid
    for y in range(Y0, Y1 + 1):
        x = sx(y)
        major = y % 2 == 0
        out.append(f'<line class="{"g" if major else "g2"}" x1="{x:.1f}" y1="{TOP - 8}" x2="{x:.1f}" y2="{plot_bottom}"/>')
        if major:
            out.append(f'<text class="yr" x="{x:.1f}" y="{plot_bottom + 18}" text-anchor="middle">{y}</text>')
    # rows
    for i, (comp, col, role, s, e) in enumerate(roles):
        y = TOP + i * ROW
        delay = 0.15 + (n - 1 - i) * 0.18
        cur = e == NOW
        out.append(f'<text class="role{" cur" if cur else ""}" x="{LEFT - 14}" y="{y + 13}" text-anchor="end">{role}</text>')
        out.append(f'<text class="comp" x="{LEFT - 14}" y="{y + 25}" text-anchor="end">{comp}</text>')
        x0, x1 = sx(s), sx(e)
        out.append(f'<rect class="bar" style="animation-delay:{delay:.2f}s" x="{x0:.1f}" y="{y + 5}" width="{max(x1 - x0, 4):.1f}" height="16" rx="5" fill="{col}"/>')
        if cur:
            out.append(f'<circle class="pulse" cx="{x1:.1f}" cy="{y + 13}" r="6" fill="{col}"/>')
            out.append(f'<circle cx="{x1:.1f}" cy="{y + 13}" r="4" fill="{col}"/>')
            out.append(f'<text class="now" x="{x1 + 10:.1f}" y="{y + 17}">now</text>')
    # era band
    by = plot_bottom + 38
    out.append(f'<text class="lbl" x="{LEFT - 14}" y="{by + 15}" text-anchor="end">Focus</text>')
    for k, (comp, col, era, rs) in enumerate(CAREER):
        s = rs[0][1]
        e = rs[-1][2] or NOW
        x0, x1 = sx(s), sx(e)
        out.append(f'<rect class="era" style="animation-delay:{1.9 + k * 0.15:.2f}s" x="{x0:.1f}" y="{by}" width="{x1 - x0:.1f}" height="22" rx="6" fill="{col}"/>')
    # era labels underneath, staggered so they never collide
    for k, (comp, col, era, rs) in enumerate(CAREER):
        s = rs[0][1]
        e = rs[-1][2] or NOW
        cx = (sx(s) + sx(e)) / 2
        ly = by + 42 + (k % 2) * 18
        anchor = "end" if k == len(CAREER) - 1 else "middle"
        lx = sx(e) if anchor == "end" else cx
        out.append(f'<text class="era-t" x="{lx:.1f}" y="{ly}" text-anchor="{anchor}" fill="{col}">{era}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Career timeline, 2004 to today">
<style>
  :root {{ --fg:#1f2328; --mute:#59636e; --grid:#d8dee4; --grid2:#eef1f4; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --fg:#e6edf3; --mute:#9198a1; --grid:#30363d; --grid2:#21262d; }} }}
  text {{ font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif; }}
  .title {{ font-size:17px; font-weight:700; fill:var(--fg); }}
  .hint {{ font-size:12px; fill:var(--mute); }}
  .role {{ font-size:13px; font-weight:600; fill:var(--fg); }}
  .role.cur {{ fill:#2563eb; }}
  .comp, .yr, .lbl {{ font-size:11px; fill:var(--mute); }}
  .now {{ font-size:11px; font-weight:700; fill:#2563eb; }}
  .era-t {{ font-size:12px; font-weight:600; }}
  .g {{ stroke:var(--grid); stroke-width:1; }}
  .g2 {{ stroke:var(--grid2); stroke-width:1; }}
  .bar, .era {{ transform-box:fill-box; transform-origin:left center; animation:grow .9s cubic-bezier(.2,.8,.2,1) both; }}
  .era {{ opacity:.85; }}
  @keyframes grow {{ from {{ transform:scaleX(0); }} to {{ transform:scaleX(1); }} }}
  .pulse {{ transform-box:fill-box; transform-origin:center; animation:pulse 2s ease-out infinite; }}
  @keyframes pulse {{ 0% {{ transform:scale(.7); opacity:.7; }} 100% {{ transform:scale(2.4); opacity:0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .bar, .era, .pulse {{ animation:none; }} }}
</style>
<text class="title" x="{LEFT - 14}" y="24" text-anchor="end">17+ years</text>
<text class="hint" x="{LEFT}" y="24">from ATM software to AI agents</text>
{chr(10).join(out)}
</svg>
'''
    (OUT / "career.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    matrix()
    career()
    print("wrote matrix.svg and career.svg")
