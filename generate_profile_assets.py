"""
generate_profile_assets.py
==========================
Generates the exact viral Cyberpunk animated GitHub profile setup,
customized 100% comprehensively according to Sonu Sharma's official CV:
1. github-contribution-animation.svg (850x165): 53x7 calendar with diagonal wave sweep, specular glints, and neon glow.
2. terminal-card.svg (840x875): macOS terminal with circular ASCII portrait of Sonu, row-by-row reveal, sweeping cursor, and whoami footer.
3. info-card.svg (480x460): Neofetch-style terminal info card reflecting Sonu's QA & Test Automation expertise, skills, tools, and highlights.
4. README.md: Full comprehensive portfolio and CV integration.
"""

import os
import sys
import math
import random
import io
import requests

try:
    from PIL import Image, ImageEnhance  # type: ignore
except ImportError:
    Image = None
    ImageEnhance = None

GITHUB_USERNAME = "SonuSharma2"
FULL_NAME = "Sonu Sharma"
AVATAR_URL = "https://avatars.githubusercontent.com/u/47955645?v=4"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# -------------------------------------------------------------------------
# 1. GENERATE github-contribution-animation.svg
# -------------------------------------------------------------------------
def generate_contribution_svg():
    width = 850
    height = 165
    cols = 53
    rows = 7

    colors = {
        0: "#161b22",
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353"
    }
    flash_colors = {
        0: "#30363d",
        1: "#57ffb0",
        2: "#57ffb0",
        3: "#8dffcc",
        4: "#b5ffd9"
    }

    random.seed(1337)
    weights = [0.42, 0.22, 0.18, 0.12, 0.06]
    grid = []
    for c in range(cols):
        col_lvls = [random.choices([0, 1, 2, 3, 4], weights=weights)[0] for _ in range(rows)]
        grid.append(col_lvls)

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
<filter id="cellglow" x="-70%" y="-70%" width="240%" height="240%">
  <feGaussianBlur stdDeviation="2" result="blur"/>
  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
</defs>
<rect width="{width}" height="{height}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
<text x="34" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Jan</text>
<text x="90" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Feb</text>
<text x="160" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Mar</text>
<text x="216" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Apr</text>
<text x="286" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">May</text>
<text x="342" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Jun</text>
<text x="398" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Jul</text>
<text x="468" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Aug</text>
<text x="524" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Sep</text>
<text x="594" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Oct</text>
<text x="650" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Nov</text>
<text x="720" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">Dec</text>
<text x="8" y="38" fill="#8b949e" font-size="9" font-family="system-ui,sans-serif">Mon</text>
<text x="8" y="66" fill="#8b949e" font-size="9" font-family="system-ui,sans-serif">Wed</text>
<text x="8" y="94" fill="#8b949e" font-size="9" font-family="system-ui,sans-serif">Fri</text>''')

    start_x = 34
    start_y = 28
    cell_pitch_x = 15
    cell_pitch_y = 14
    max_d = (cols - 1) + (rows - 1)

    for c in range(cols):
        for r in range(rows):
            lvl = grid[c][r]
            x = start_x + (c * cell_pitch_x)
            y = start_y + (r * cell_pitch_y)
            color = colors[lvl]
            flash = flash_colors[lvl]

            d = c + (6 - r)
            t1 = round((d / float(max_d)) * 0.40, 4)
            t2 = round(t1 + 0.0120, 4)
            t3 = round(t1 + 0.0500, 4)

            filter_attr = ' filter="url(#cellglow)"' if lvl >= 3 else ''

            if lvl == 0:
                svg.append(f'<rect id="s{c}_{r}" x="{x}" y="{y}" width="11" height="11" rx="2" fill="{color}" opacity="0">')
                svg.append(f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{t1:.4f};{t2:.4f};1" dur="7.0s" repeatCount="indefinite"/>')
                svg.append('</rect>')
            else:
                svg.append(f'<rect id="s{c}_{r}" x="{x}" y="{y}" width="11" height="11" rx="2" fill="{color}" opacity="0"{filter_attr}>')
                svg.append(f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{t1:.4f};{t2:.4f};1" dur="7.0s" repeatCount="indefinite"/>')
                svg.append(f'<animate attributeName="fill" values="{color};{color};{flash};{color}" keyTimes="0;{t1:.4f};{t2:.4f};{t3:.4f}" dur="7.0s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.1 0 0.2 1;0.4 0 0.6 1"/>')
                svg.append('</rect>')
                svg.append(f'<rect x="{x+2}" y="{y+2}" width="4" height="2" rx="1" fill="white" opacity="0" pointer-events="none">')
                svg.append(f'<animate attributeName="opacity" values="0;0;0.55;0" keyTimes="0;{t1:.4f};{t2:.4f};{t3:.4f}" dur="7.0s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0 0 0.3 1;0.5 0 1 1"/>')
                svg.append('</rect>')

    svg.append('</svg>')
    output_path = os.path.join(OUTPUT_DIR, "github-contribution-animation.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {output_path}")


# -------------------------------------------------------------------------
# 2. GENERATE terminal-card.svg
# -------------------------------------------------------------------------
def generate_terminal_card_svg():
    width = 840
    height = 875
    W = 100
    H = 53

    ascii_rows = []
    local_avatar = None
    for cand in ["avatar.png", "avatar.jpg", "profile.jpg", "photo.jpg"]:
        cand_p = os.path.join(OUTPUT_DIR, cand)
        if os.path.exists(cand_p):
            local_avatar = cand_p
            break

    try:
        if local_avatar and Image is not None:
            img = Image.open(local_avatar).convert("L")
        elif Image is not None:
            res = requests.get(AVATAR_URL, timeout=8)
            if res.status_code == 200:
                img = Image.open(io.BytesIO(res.content)).convert("L")
            else:
                img = None
        else:
            img = None

        if img is not None:
            img = ImageEnhance.Contrast(img).enhance(1.8)
            img = img.resize((W, H), Image.Resampling.LANCZOS)
            chars = " .:-=+*sS%#@"

            for y in range(H):
                row = []
                ny = (y - (H / 2.0)) / (H / 2.0 * 0.94)
                for x in range(W):
                    nx = (x - (W / 2.0)) / (W / 2.0 * 0.94)
                    dist = math.sqrt(nx * nx + ny * ny)
                    if dist > 1.04:
                        row.append('#')
                    elif dist > 0.98:
                        row.append('@')
                    else:
                        val = img.getpixel((x, y))
                        char_idx = min(int(val / 256.0 * len(chars)), len(chars) - 1)
                        row.append(chars[char_idx])
                row_str = "".join(row).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                ascii_rows.append(row_str)
    except Exception as e:
        print(f"Notice during image conversion: {e}")

    if len(ascii_rows) < H:
        ascii_rows = []
        for y in range(H):
            row = []
            ny = (y - (H / 2.0)) / (H / 2.0 * 0.94)
            for x in range(W):
                nx = (x - (W / 2.0)) / (W / 2.0 * 0.94)
                dist = math.sqrt(nx * nx + ny * ny)
                if dist > 1.04:
                    row.append('#')
                elif dist > 0.98:
                    row.append('@')
                else:
                    row.append('.' if (x + y) % 2 == 0 else ' ')
            ascii_rows.append("".join(row))

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#111722"/>
    <stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
</defs>
<!-- card background -->
<rect width="{width}" height="{height}" rx="12" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="none" stroke="#30363d" stroke-width="1"/>
<!-- title bar separator -->
<line x1="0" y1="30" x2="{width}" y2="30" stroke="#30363d"/>
<!-- macOS window buttons -->
<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>
<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>
<!-- window title -->
<text x="420.0" y="19.0" fill="#7d8590" font-size="12" text-anchor="middle">{GITHUB_USERNAME}@github: ~$ ./portrait.sh</text>
<!-- ASCII art rows -->''')

    row_dur = 0.11
    row_height = 15.0
    start_y = 37.0

    for i, row_text in enumerate(ascii_rows):
        start_time = round(i * row_dur, 3)
        end_time = round((i + 1) * row_dur, 3)
        row_y = start_y + (i * row_height)
        text_y = row_y + 11.1
        cursor_y = row_y + 1.0

        svg.append(f'<clipPath id="r{i}"><rect x="20" y="{row_y:.1f}" height="15" width="0"><animate attributeName="width" from="0" to="800" begin="{start_time:.3f}s" dur="{row_dur}s" fill="freeze"/></rect></clipPath>')
        svg.append(f'<g clip-path="url(#r{i})"><text xml:space="preserve" x="20" y="{text_y:.1f}" fill="#c9d1d9" font-size="12.9" textLength="800" lengthAdjust="spacing">{row_text}</text></g>')
        svg.append(f'<rect y="{cursor_y:.1f}" width="8" height="13" fill="#c9d1d9" opacity="0"><animate attributeName="x" from="20" to="820" begin="{start_time:.3f}s" dur="{row_dur}s" fill="freeze"/><set attributeName="opacity" to="0.85" begin="{start_time:.3f}s"/><set attributeName="opacity" to="0" begin="{end_time:.3f}s"/></rect>')

    svg.append(f'''<!-- footer separator -->
<line x1="0" y1="832.0" x2="{width}" y2="832.0" stroke="#30363d"/>
<!-- whoami line -->
<text x="20" y="851.0" fill="#7d8590" font-size="13">{GITHUB_USERNAME}@github:~$ whoami <tspan fill="#c9d1d9">{FULL_NAME}</tspan></text>
<!-- blinking cursor -->
<rect x="280" y="838.0" width="8" height="14" fill="#c9d1d9">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>
</rect>
</svg>''')

    output_path = os.path.join(OUTPUT_DIR, "terminal-card.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated: {output_path}")


# -------------------------------------------------------------------------
# 3. GENERATE info-card.svg (ACCORDING TO CV)
# -------------------------------------------------------------------------
def generate_info_card_svg():
    width = 480
    height = 460

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#111722"/>
    <stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
</defs>

<!-- card background -->
<rect width="{width}" height="{height}" rx="12" fill="url(#ibg)"/>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="none" stroke="#30363d"/>

<!-- title bar -->
<line x1="0" y1="30" x2="{width}" y2="30" stroke="#30363d"/>
<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>
<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>
<text x="240" y="19" fill="#7d8590" font-size="12" text-anchor="middle">{GITHUB_USERNAME}@github: ~$ neofetch</text>

<!-- ── ROW 0: identity header ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="60" font-size="14" font-weight="700">
    <tspan fill="#3fb950">{GITHUB_USERNAME}</tspan>
    <tspan fill="#7d8590">@</tspan>
    <tspan fill="#22d3ee">github</tspan>
  </text>
  <line x1="160" y1="56" x2="460" y2="56" stroke="#30363d" stroke-opacity="0.8"/>
  <animate attributeName="opacity" from="0" to="1" begin="0.15s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.15s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── ROW 2: Role ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="104" fill="#ffa657" font-size="12.5" font-weight="700">Role</text>
  <text x="112" y="104" fill="#c9d1d9" font-size="12.5">QA &amp; Automation Engineer</text>
  <animate attributeName="opacity" from="0" to="1" begin="0.27s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.27s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── ROW 3: Focus ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="125" fill="#ffa657" font-size="12.5" font-weight="700">Focus</text>
  <text x="112" y="125" fill="#c9d1d9" font-size="12.5">Selenium, Playwright, Pytest, POM</text>
  <animate attributeName="opacity" from="0" to="1" begin="0.33s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.33s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── ROW 4: College ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="146" fill="#ffa657" font-size="12.5" font-weight="700">College</text>
  <text x="112" y="146" fill="#c9d1d9" font-size="12.5">BSc (Hons) CS, Sunway (3.46 GPA)</text>
  <animate attributeName="opacity" from="0" to="1" begin="0.39s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.39s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── SECTION: Stack ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="177" fill="#58a6ff" font-size="12.5" font-weight="700">&#8212; Stack</text>
  <line x1="72" y1="173" x2="460" y2="173" stroke="#30363d" stroke-opacity="0.8"/>
  <animate attributeName="opacity" from="0" to="1" begin="0.51s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.51s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── ROW: Automation ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="198" fill="#ffa657" font-size="12.5" font-weight="700">Automation</text>
  <text x="112" y="198" fill="#c9d1d9" font-size="12.5">Selenium (Python), Playwright, Pytest</text>
  <animate attributeName="opacity" from="0" to="1" begin="0.57s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.57s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── ROW: Testing ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="219" fill="#ffa657" font-size="12.5" font-weight="700">Testing</text>
  <text x="112" y="219" fill="#c9d1d9" font-size="12.5">Manual, Functional, API (Postman), JMeter</text>
  <animate attributeName="opacity" from="0" to="1" begin="0.63s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.63s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── ROW: Tools ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="240" fill="#ffa657" font-size="12.5" font-weight="700">Tools</text>
  <text x="112" y="240" fill="#c9d1d9" font-size="12.5">ClickUp, Jira, Trello, Git, GitHub</text>
  <animate attributeName="opacity" from="0" to="1" begin="0.69s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.69s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── ROW: Languages ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="261" fill="#ffa657" font-size="12.5" font-weight="700">Languages</text>
  <text x="112" y="261" fill="#c9d1d9" font-size="12.5">Python, C, HTML5, CSS3, MySQL</text>
  <animate attributeName="opacity" from="0" to="1" begin="0.75s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.75s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── ROW: Process ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="282" fill="#ffa657" font-size="12.5" font-weight="700">Process</text>
  <text x="112" y="282" fill="#c9d1d9" font-size="12.5">SDLC, STLC, Agile (Scrum), POM</text>
  <animate attributeName="opacity" from="0" to="1" begin="0.81s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.81s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── SECTION: Highlights ── -->
<g opacity="0" transform="translate(0,5)">
  <text x="20" y="313" fill="#58a6ff" font-size="12.5" font-weight="700">&#8212; Highlights</text>
  <line x1="112" y1="309" x2="460" y2="309" stroke="#30363d" stroke-opacity="0.8"/>
  <animate attributeName="opacity" from="0" to="1" begin="0.87s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.87s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── BULLET 1 ── -->
<g opacity="0" transform="translate(0,5)">
  <circle cx="23" cy="329" r="2.5" fill="#3fb950"/>
  <text x="34" y="333" fill="#c9d1d9" font-size="12.5">QA Automation on Chatboq.com SaaS AI Platform</text>
  <animate attributeName="opacity" from="0" to="1" begin="0.93s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.93s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── BULLET 2 ── -->
<g opacity="0" transform="translate(0,5)">
  <circle cx="23" cy="354" r="2.5" fill="#3fb950"/>
  <text x="34" y="358" fill="#c9d1d9" font-size="12.5">E2E Page Object Model Suites @ SauceDemo-Automation</text>
  <animate attributeName="opacity" from="0" to="1" begin="0.99s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="0.99s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── BULLET 3 ── -->
<g opacity="0" transform="translate(0,5)">
  <circle cx="23" cy="379" r="2.5" fill="#3fb950"/>
  <text x="34" y="383" fill="#c9d1d9" font-size="12.5">Web &amp; Mobile Functional/UI Testing @ Heal Home Care</text>
  <animate attributeName="opacity" from="0" to="1" begin="1.05s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="1.05s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>

<!-- ── BULLET 4 ── -->
<g opacity="0" transform="translate(0,5)">
  <circle cx="23" cy="404" r="2.5" fill="#3fb950"/>
  <text x="34" y="408" fill="#c9d1d9" font-size="12.5">HackerRank Certified · Blockchain Project with 150+ Users</text>
  <animate attributeName="opacity" from="0" to="1" begin="1.11s" dur="0.4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="1.11s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
</g>
</svg>'''

    output_path = os.path.join(OUTPUT_DIR, "info-card.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated: {output_path}")


# -------------------------------------------------------------------------
# 4. INJECT INTO README.md (COMPREHENSIVE CV INTEGRATION)
# -------------------------------------------------------------------------
def inject_into_readme():
    readme_path = os.path.join(OUTPUT_DIR, "README.md")
    content = f'''<p align="center">
  <img src="github-contribution-animation.svg" alt="GitHub Contribution Graph" width="850"/>
</p>

<table>
  <tr>
    <td valign="centre"><img src="terminal-card.svg" alt="ASCII Portrait" width="400"/></td>
    <td valign="top"><img src="info-card.svg" alt="Info Card" width="500"/></td>
  </tr>
</table>

<!-- HERO SECTION -->
<div align="center">
  <h3><strong>QA &amp; Test Automation Engineer | Software Quality &amp; Web Applications</strong></h3>
  <p><i>Building robust test automation frameworks with Selenium, Playwright &amp; Python | Ensuring zero-defect releases.</i></p>

  <p>
    <a href="mailto:sonushar059@gmail.com"><img src="https://img.shields.io/badge/Email-sonushar059%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
    <a href="https://github.com/{GITHUB_USERNAME}"><img src="https://img.shields.io/badge/GitHub-{GITHUB_USERNAME}-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
    <a href="https://github.com/{GITHUB_USERNAME}/SauceDemo-Automation"><img src="https://img.shields.io/badge/Project-SauceDemo--Automation-38BDF8?style=for-the-badge&logo=selenium&logoColor=white" alt="SauceDemo Automation" /></a>
    <a href="https://github.com/{GITHUB_USERNAME}/Internet-Voting"><img src="https://img.shields.io/badge/Project-Ethereum--Voting-8A2BE2?style=for-the-badge&logo=ethereum&logoColor=white" alt="Ethereum Voting" /></a>
  </p>
  
  <img src="https://komarev.com/ghpvc/?username={GITHUB_USERNAME}&color=00FFCC&style=flat-square" alt="Visitor Counter" />
</div>

<br/>

<!-- ================= PROFESSIONAL EXPERIENCE ================= -->
## 💼 Professional Experience

### 🧪 **QA Intern** — [Brahmabyte Lab](https://brahmabytelab.com/) *(March 2026 – June 2026)*
- **Platform**: [Chatboq.com](https://chatboq.com/) (SaaS-based AI chatbot platform)
- Performed regression, functional, UI/UX, and validation testing across multiple modules including Inbox, Tickets, Visitors, Clients, Billing, and AI modules.
- Formulated and executed structured test cases; logged defects in **ClickUp** with actionable reproduction steps, severity, and priority metrics.
- Developed and maintained automated test suites utilizing **Python**, **Playwright**, and **Selenium** with the **Page Object Model (POM)** architecture to optimize test coverage and speed.
- Inspected frontend DOM elements (HTML/CSS) to verify responsive layouts and UI integrity.

### 📱 **QA Assistant** — [Heal Home Care](https://www.healhomecare.com/) *(Nov 2023 – Feb 2025)*
- Tested web platform and mobile application features, identifying and documenting functional, responsive, and UI defects.
- Documented defects in **ClickUp** with granular reproduction steps, annotated screenshots, and verification notes.
- Partnered directly with developers to test bug fixes and validate features prior to production releases.
- Maintained regular website updates and suggested user experience (UX) refinements.

### 🌐 **Web Designer (WordPress)** — [Freelancer Unit Pvt. Ltd.](https://freelancernepal.com.np/) *(August 2022 – Sep 2023)*
- Engineered and maintained custom WordPress web platforms tailored to client requirements.
- Validated UI/UX designs and application requirements to ensure technical feasibility and cross-browser usability.
- Executed quality and functionality pre-deployment checks before pushing to production.

---

<!-- ================= TECHNICAL SKILLS ================= -->
## 🛠️ Technical Competencies

| Domain | Skills & Tooling |
| :--- | :--- |
| **Test Automation** | `Selenium WebDriver (Python)` • `Playwright` • `Pytest` • `Page Object Model (POM)` |
| **Manual & API Testing** | `Functional Testing` • `UI/UX Testing` • `Regression Testing` • `Postman (API)` • `JMeter` |
| **Testing Methodologies** | `STLC` • `SDLC` • `Agile (Scrum)` • `Defect Lifecycle Management` • `Test Case Design` |
| **Languages & Web** | `Python` • `C` • `HTML5` • `CSS3` • `JavaScript` |
| **Databases** | `MySQL (CRUD Operations, Relational Schema Management)` |
| **Productivity & Dev Tools** | `ClickUp` • `Jira` • `Trello` • `Git` • `GitHub` • `Figma` • `Notion` • `VS Code` |

---

<!-- ================= FEATURED PROJECTS ================= -->
## 🚀 Featured Projects

<table>
  <tr>
    <td width="50%" valign="top">
      <h3 align="center">🧪 <a href="https://github.com/SonuSharma2/SauceDemo-Automation">SauceDemo Automation Framework</a></h3>
      <p>End-to-end automation test suite built using <b>Selenium</b>, <b>Python</b>, and <b>Pytest</b> following the <b>Page Object Model (POM)</b> design pattern for login, product sorting, and checkout workflows.</p>
      <p align="center"><code>Selenium</code> • <code>Python</code> • <code>Pytest</code> • <code>POM</code></p>
    </td>
    <td width="50%" valign="top">
      <h3 align="center">🗳️ <a href="https://github.com/SonuSharma2/Internet-Voting">Blockchain-Based Internet Voting System</a></h3>
      <p>Decentralized digital voting application engineered on the <b>Ethereum Blockchain</b> ensuring immutable and tamper-proof electoral processes. Successfully verified through pilot testing with <b>150+ participants</b>.</p>
      <p align="center"><code>Ethereum</code> • <code>Smart Contracts</code> • <code>Solidity</code> • <code>Web3</code></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3 align="center">🚌 <a href="https://github.com/SonuSharma2/BusTicketBooking-System">Bus Ticket Booking System</a></h3>
      <p>Desktop application architected in <b>Java</b> utilizing OOP principles and file persistence. Features real-time seat inventory tracking, schedule administration, fare calculation, and ticket management.</p>
      <p align="center"><code>Java</code> • <code>OOP</code> • <code>File I/O</code> • <code>Data Structures</code></p>
    </td>
    <td width="50%" valign="top">
      <h3 align="center">🔒 <a href="https://github.com/SonuSharma2/ImageSteganography">Image Steganography Cryptosystem</a></h3>
      <p>Cryptographic tool built with <b>Python</b> and <b>Flask</b> that conceals confidential text data within image pixels using the <b>Least Significant Bit (LSB)</b> algorithm with zero visual degradation.</p>
      <p align="center"><code>Python</code> • <code>Flask</code> • <code>Pillow</code> • <code>LSB Cryptography</code></p>
    </td>
  </tr>
</table>

---

<!-- ================= EDUCATION & CERTIFICATIONS ================= -->
## 🎓 Education & Certifications

### 📚 Education
- 🎓 **Bachelor in Computer Science (Hons)** *(2018 – 2022)*
  - **Institution**: Sunway International Business School, IUKL, Nepal
  - **Academic Score**: **3.46 GPA**
- 🏫 **+2 Higher Secondary**, NEB Board *(2015 – 2017)*
  - **Institution**: St. Lawrence College, Kathmandu, Nepal (66.4%)
- 🏫 **School Leaving Certificate (SLC)**, NEB Board *(2015)*
  - **Institution**: Shubharambha Secondary School, Kathmandu, Nepal (75%)

### 📜 Certifications & Workshops
- 🐍 **Python (Basic) Certificate** — HackerRank
- 🐙 **Git & GitHub Workshop**
- 🤖 **Robotics & Microcontrollers Workshop on Arduino**

---

<div align="center">
  <p><i>📍 Kathmandu, Nepal &nbsp;•&nbsp; ✉️ <a href="mailto:sonushar059@gmail.com">sonushar059@gmail.com</a></i></p>
</div>
'''
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated README.md with 100% comprehensive CV integration!")


# -------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------
if __name__ == "__main__":
    generate_contribution_svg()
    generate_terminal_card_svg()
    generate_info_card_svg()
    inject_into_readme()
    print("All tasks completed successfully according to CV!")
