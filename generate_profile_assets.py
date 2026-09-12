"""
generate_profile_assets.py
==========================
Generates three high-end, self-contained animated SVGs for GitHub Profile README:
1. github-contribution-animation.svg: 53x7 grid with diagonal slant reveal, specular glint, and level 3+ outer glow.
2. terminal-card.svg: macOS terminal with ASCII portrait converted from GitHub avatar, animated row-by-row, with $ whoami typewriter footer.
3. info-card.svg: Neofetch-style system info card with staggered slide-in animations and terminal color blocks.
4. Updates README.md to seamlessly embed them side-by-side and centered.
"""

import os
import sys
import math
import random
import io
import requests
from PIL import Image, ImageEnhance

GITHUB_USERNAME = "SonuSharma2"
AVATAR_URL = f"https://avatars.githubusercontent.com/u/47955645?v=4"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------------------
# 1. GENERATE github-contribution-animation.svg
# -------------------------------------------------------------------------
def generate_contribution_svg():
    width = 890
    height = 205
    cols = 53
    rows = 7
    cell_size = 11
    cell_pitch = 14.5
    start_x = 55
    start_y = 56

    # Contribution color palette
    # Level 0 (empty), 1 (low), 2 (medium), 3 (high), 4 (peak)
    colors = {
        0: "#161b22",
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353"
    }

    # Generate realistic pseudo-random contributions clustered into active periods
    random.seed(42)
    weights = [0.42, 0.24, 0.18, 0.11, 0.05]
    grid_levels = []
    for c in range(cols):
        col_levels = []
        for r in range(rows):
            lvl = random.choices([0, 1, 2, 3, 4], weights=weights)[0]
            col_levels.append(lvl)
        grid_levels.append(col_levels)

    # Calculate diagonal delays for "slant reveal"
    # Diagonal index: d = col + (6 - row)
    # Sweeps from bottom-left (col=0, row=6 => d=0) to top-right (col=52, row=0 => d=58)
    max_d = (cols - 1) + (rows - 1)  # 58

    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="contrib-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="50%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#090d16" />
    </linearGradient>

    <!-- Outer Glow for Level 3 & Level 4 Cells -->
    <filter id="glow-l3" x="-80%" y="-80%" width="260%" height="260%">
      <feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#26a641" flood-opacity="0.75" />
    </filter>
    <filter id="glow-l4" x="-100%" y="-100%" width="300%" height="300%">
      <feDropShadow dx="0" dy="0" stdDeviation="3.5" flood-color="#39d353" flood-opacity="0.95" />
      <feDropShadow dx="0" dy="0" stdDeviation="1.5" flood-color="#5eead4" flood-opacity="0.8" />
    </filter>

    <style>
      .bg-card {{
        fill: url(#contrib-bg);
        stroke: #30363d;
        stroke-width: 1.2;
        rx: 12px;
      }}
      .title-text {{
        font-family: 'JetBrains Mono', 'Fira Code', -apple-system, BlinkMacSystemFont, monospace;
        font-size: 13px;
        font-weight: 600;
        fill: #f1f5f9;
        letter-spacing: 0.5px;
      }}
      .stat-counter {{
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 11px;
        fill: #38bdf8;
        font-weight: 500;
      }}
      .axis-label {{
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 9px;
        fill: #64748b;
      }}
      .legend-text {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        fill: #8b949e;
      }}

      /* Base cell transformation */
      .c-cell {{
        transform-box: fill-box;
        transform-origin: center;
        opacity: 0;
      }}

      /* Diagonal Slant Reveal with Specular White/Cyan Glint Flash */
      @keyframes slantRevealL0 {{
        0% {{ opacity: 0; transform: scale(0.2); fill: #ffffff; }}
        30% {{ opacity: 1; transform: scale(1.25); fill: #ffffff; }}
        65% {{ fill: #334155; }}
        100% {{ opacity: 1; transform: scale(1); fill: #161b22; }}
      }}
      @keyframes slantRevealL1 {{
        0% {{ opacity: 0; transform: scale(0.2); fill: #ffffff; }}
        30% {{ opacity: 1; transform: scale(1.3); fill: #ffffff; }}
        65% {{ fill: #2dd4bf; }}
        100% {{ opacity: 1; transform: scale(1); fill: #0e4429; }}
      }}
      @keyframes slantRevealL2 {{
        0% {{ opacity: 0; transform: scale(0.2); fill: #ffffff; }}
        30% {{ opacity: 1; transform: scale(1.35); fill: #ffffff; }}
        65% {{ fill: #38bdf8; }}
        100% {{ opacity: 1; transform: scale(1); fill: #006d32; }}
      }}
      @keyframes slantRevealL3 {{
        0% {{ opacity: 0; transform: scale(0.2); fill: #ffffff; }}
        30% {{ opacity: 1; transform: scale(1.4); fill: #ffffff; }}
        65% {{ fill: #86efac; }}
        100% {{ opacity: 1; transform: scale(1); fill: #26a641; }}
      }}
      @keyframes slantRevealL4 {{
        0% {{ opacity: 0; transform: scale(0.2); fill: #ffffff; }}
        30% {{ opacity: 1; transform: scale(1.5); fill: #ffffff; }}
        65% {{ fill: #a7f3d0; }}
        100% {{ opacity: 1; transform: scale(1); fill: #39d353; }}
      }}
    </style>
  </defs>

  <!-- Card Background -->
  <rect width="{width}" height="{height}" class="bg-card" />

  <!-- Header Section -->
  <g transform="translate(24, 28)">
    <circle cx="4" cy="-2" r="3" fill="#22c55e">
      <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite" />
    </circle>
    <text x="16" y="2" class="title-text">⚡ GitHub Contribution Activity (Live Simulation)</text>
    <text x="{width - 48}" y="2" text-anchor="end" class="stat-counter">1,480+ Commits &amp; Reviews in Last Year</text>
  </g>

  <!-- Month Labels -->
  <g class="axis-label" transform="translate({start_x}, {start_y - 12})">''')

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_step = cols / 12.0
    for m_idx, m_name in enumerate(months):
        mx = int(m_idx * month_step * cell_pitch)
        svg_parts.append(f'    <text x="{mx}">{m_name}</text>')
    svg_parts.append('  </g>')

    # Day of week labels (Mon, Wed, Fri)
    svg_parts.append(f'''  <g class="axis-label" transform="translate(26, {start_y + 8})">
    <text x="0" y="{1 * cell_pitch}">Mon</text>
    <text x="0" y="{3 * cell_pitch}">Wed</text>
    <text x="0" y="{5 * cell_pitch}">Fri</text>
  </g>''')

    # Contribution Grid Cells
    svg_parts.append('  <!-- Contribution Grid Cells -->\n  <g>')
    for c in range(cols):
        for r in range(rows):
            lvl = grid_levels[c][r]
            x = start_x + (c * cell_pitch)
            y = start_y + (r * cell_pitch)
            
            # Diagonal index: sweeps bottom-left to top-right
            d = c + (6 - r)
            delay = round(0.12 + (d * 0.028), 3)
            
            anim_name = f"slantRevealL{lvl}"
            filter_attr = ""
            if lvl == 3:
                filter_attr = 'filter="url(#glow-l3)"'
            elif lvl == 4:
                filter_attr = 'filter="url(#glow-l4)"'

            style_rule = f"animation: {anim_name} 0.55s cubic-bezier(0.16, 1, 0.3, 1) {delay}s forwards;"
            
            svg_parts.append(
                f'    <rect class="c-cell" x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" '
                f'rx="2.5" ry="2.5" {filter_attr} style="{style_rule}" />'
            )
    svg_parts.append('  </g>')

    # Legend at bottom right
    leg_x = width - 180
    leg_y = height - 20
    svg_parts.append(f'''  <!-- Legend Section -->
  <g class="legend-text" transform="translate({leg_x}, {leg_y})">
    <text x="-8" y="8" text-anchor="end">Less</text>
    <rect x="0" y="0" width="9" height="9" rx="1.5" fill="{colors[0]}" stroke="#30363d" stroke-width="0.5" />
    <rect x="13" y="0" width="9" height="9" rx="1.5" fill="{colors[1]}" />
    <rect x="26" y="0" width="9" height="9" rx="1.5" fill="{colors[2]}" />
    <rect x="39" y="0" width="9" height="9" rx="1.5" fill="{colors[3]}" filter="url(#glow-l3)" />
    <rect x="52" y="0" width="9" height="9" rx="1.5" fill="{colors[4]}" filter="url(#glow-l4)" />
    <text x="68" y="8">More</text>
  </g>
</svg>''')

    output_path = os.path.join(OUTPUT_DIR, "github-contribution-animation.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"Generated: {output_path}")


# -------------------------------------------------------------------------
# 2. GENERATE terminal-card.svg
# -------------------------------------------------------------------------
def generate_terminal_card_svg():
    width = 440
    height = 420

    # Fetch avatar image or fallback to sleek geometric portrait
    ascii_rows = []
    target_w = 42
    try:
        res = requests.get(AVATAR_URL, timeout=8)
        if res.status_code == 200:
            img = Image.open(io.BytesIO(res.content)).convert("L")
            # Enhance contrast for sharp ASCII rendering
            img = ImageEnhance.Contrast(img).enhance(1.65)
            target_h = int(target_w * (img.height / img.width) * 0.48)
            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            chars = " .:-=+*#%@"
            for y in range(target_h):
                line = "".join(chars[min(int(img.getpixel((x, y)) / 256 * len(chars)), len(chars) - 1)] for x in range(target_w))
                # Escape xml characters
                escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                ascii_rows.append(escaped_line)
    except Exception as e:
        print(f"Avatar fetch warning: {e}. Using fallback art.")

    if not ascii_rows:
        # Fallback cyberpunk developer avatar mask
        fallback_art = [
            "               .---.              ",
            "              /     \\             ",
            "             | () () |            ",
            "              \\  _  /             ",
            "               `---'              ",
            "            .---------.           ",
            "           / | FRONT | \\          ",
            "          |  |  END  |  |         ",
            "          |  | DEV   |  |         ",
            "          '--'-------'--'         "
        ]
        ascii_rows = [l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") for l in fallback_art]

    # Limit to maximum 19 rows so it fits perfectly in the terminal window
    ascii_rows = ascii_rows[:19]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="term-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="60%" stop-color="#111827" />
      <stop offset="100%" stop-color="#0a0f1d" />
    </linearGradient>

    <!-- Text Neon Gradient -->
    <linearGradient id="ascii-neon" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="50%" stop-color="#818cf8" />
      <stop offset="100%" stop-color="#34d399" />
    </linearGradient>

    <style>
      .term-window {{
        fill: url(#term-bg);
        stroke: #30363d;
        stroke-width: 1.2;
        rx: 12px;
      }}
      .term-title {{
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 11px;
        fill: #8b949e;
        font-weight: 500;
      }}
      .cmd-prompt {{
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 11px;
        fill: #94a3b8;
      }}
      .ascii-line {{
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-size: 9.5px;
        letter-spacing: 1.2px;
        fill: url(#ascii-neon);
        opacity: 0;
        transform: translateY(3px);
      }}
      .cursor-block {{
        fill: #38bdf8;
      }}

      /* Staggered Row Reveal Animation */
      @keyframes revealRow {{
        0% {{
          opacity: 0;
          transform: translateY(3px);
        }}
        100% {{
          opacity: 1;
          transform: translateY(0);
        }}
      }}

      /* Typewriter prompt at bottom */
      @keyframes fadeInFooter {{
        0% {{ opacity: 0; transform: translateY(4px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}

      /* Sweeping / Blinking Terminal Cursor */
      @keyframes blinkCursor {{
        0%, 45% {{ opacity: 1; }}
        50%, 95% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
      }}
    </style>
  </defs>

  <!-- Window Container -->
  <rect width="{width}" height="{height}" class="term-window" />

  <!-- macOS Window Control Buttons -->
  <circle cx="22" cy="19" r="5.5" fill="#ef4444" />
  <circle cx="38" cy="19" r="5.5" fill="#f59e0b" />
  <circle cx="54" cy="19" r="5.5" fill="#10b981" />

  <!-- Window Title -->
  <text x="220" y="23" text-anchor="middle" class="term-title">sonu@avatar: ~ (ascii-portrait)</text>

  <!-- Divider Line -->
  <line x1="0" y1="36" x2="{width}" y2="36" stroke="#21262d" stroke-width="1" />

  <!-- Terminal Command Execution -->
  <g transform="translate(20, 56)">
    <text class="cmd-prompt">
      <tspan fill="#38bdf8">sonu@devbox</tspan><tspan fill="#8b949e">:</tspan><tspan fill="#a855f7">~</tspan><tspan fill="#f1f5f9">$ cat avatar.ascii</tspan>
    </text>
  </g>

  <!-- ASCII Art Rows (Revealed Top to Bottom) -->
  <g transform="translate(20, 72)">'''

    line_spacing = 11.8
    total_reveal_time = 0.2
    for i, row in enumerate(ascii_rows):
        y_pos = (i + 1) * line_spacing
        delay = round(0.2 + (i * 0.055), 3)
        style = f"animation: revealRow 0.22s cubic-bezier(0.16, 1, 0.3, 1) {delay}s forwards;"
        svg += f'\n    <text x="0" y="{y_pos:.1f}" class="ascii-line" style="{style}">{row}</text>'
        total_reveal_time = delay + 0.22

    whoami_delay = round(total_reveal_time + 0.2, 3)
    res_delay = round(whoami_delay + 0.3, 3)
    cursor_delay = round(res_delay + 0.1, 3)

    svg += f'''
  </g>

  <!-- Footer Typewriter Section ($ whoami -> Sonu Sharma) -->
  <g transform="translate(20, 335)">
    <!-- Command Prompt -->
    <text class="cmd-prompt" style="opacity: 0; animation: fadeInFooter 0.3s ease-out {whoami_delay}s forwards;">
      <tspan fill="#38bdf8">sonu@devbox</tspan><tspan fill="#8b949e">:</tspan><tspan fill="#a855f7">~</tspan><tspan fill="#f1f5f9">$ whoami</tspan>
    </text>

    <!-- Response Output -->
    <g transform="translate(0, 22)" style="opacity: 0; animation: fadeInFooter 0.35s ease-out {res_delay}s forwards;">
      <text font-family="'JetBrains Mono', monospace" font-size="12" font-weight="600" fill="#22c55e">
        ➜ Sonu Sharma <tspan fill="#38bdf8" font-size="11" font-weight="500">[Frontend Engineer &amp; UI/UX]</tspan>
      </text>
    </g>

    <g transform="translate(0, 42)" style="opacity: 0; animation: fadeInFooter 0.35s ease-out {res_delay + 0.15:.2f}s forwards;">
      <text font-family="'JetBrains Mono', monospace" font-size="10.5" fill="#94a3b8">
        ⚡ Obsessed with 60fps micro-interactions &amp; testability.
      </text>
      <!-- Blinking Cursor Block -->
      <rect x="355" y="-10" width="7" height="13" class="cursor-block" style="animation: blinkCursor 0.9s step-end infinite; animation-delay: {cursor_delay}s;" />
    </g>
  </g>
</svg>'''

    output_path = os.path.join(OUTPUT_DIR, "terminal-card.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated: {output_path}")


# -------------------------------------------------------------------------
# 3. GENERATE info-card.svg (Neofetch Info Card)
# -------------------------------------------------------------------------
def generate_info_card_svg():
    width = 440
    height = 420

    lines = [
        ("HEADER", "sonu@devbox"),
        ("SEP", "--------------------------------------"),
        ("OS", "OS", "GitHub / Arch Linux (Rolling)", "#f97316", "#e2e8f0"),
        ("HOST", "Host", "Sunway CS / Kathmandu, NP", "#f97316", "#e2e8f0"),
        ("KERNEL", "Kernel", "React 19 / TypeScript 5.8 (Strict)", "#38bdf8", "#e2e8f0"),
        ("ROLE", "Role", "Frontend Engineer & Creative Dev", "#22c55e", "#f1f5f9"),
        ("UPTIME", "Uptime", "5+ Years in Software Engineering", "#a855f7", "#e2e8f0"),
        ("SHELL", "Shell", "zsh 5.9 (spaceship-prompt & starship)", "#f97316", "#e2e8f0"),
        ("STACK", "Stack", "React • TypeScript • Tailwind • GSAP", "#38bdf8", "#38bdf8"),
        ("QUALITY", "Quality", "Playwright • Pytest • Selenium (POM)", "#22c55e", "#4ade80"),
        ("MISSION", "Mission", "\"Zero Bugs, 60fps, Pure Delight\"", "#a855f7", "#c084fc"),
        ("MEMORY", "Memory", "99.4% Caffeine / 0.6% Sleep", "#f97316", "#e2e8f0"),
        ("PORTFOLIO", "Portfolio", "https://sonusharma.com.np", "#38bdf8", "#38bdf8"),
    ]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <!-- Card Gradient -->
    <linearGradient id="info-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="60%" stop-color="#111827" />
      <stop offset="100%" stop-color="#0a0f1d" />
    </linearGradient>

    <style>
      .info-window {{
        fill: url(#info-bg);
        stroke: #30363d;
        stroke-width: 1.2;
        rx: 12px;
      }}
      .info-title {{
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 11px;
        fill: #8b949e;
        font-weight: 500;
      }}
      .term-line {{
        font-family: 'JetBrains Mono', 'Fira Code', -apple-system, monospace;
        font-size: 11.5px;
        opacity: 0;
        transform: translateY(8px);
      }}

      /* Staggered slide up and fade in for terminal neofetch lines */
      @keyframes slideInLine {{
        0% {{
          opacity: 0;
          transform: translateY(8px);
        }}
        100% {{
          opacity: 1;
          transform: translateY(0);
        }}
      }}

      .color-block {{
        opacity: 0;
        transform: scale(0.8);
        transform-box: fill-box;
        transform-origin: center;
      }}
      @keyframes popColorBlock {{
        0% {{ opacity: 0; transform: scale(0.6); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}
    </style>
  </defs>

  <!-- Window Container -->
  <rect width="{width}" height="{height}" class="info-window" />

  <!-- macOS Window Control Buttons -->
  <circle cx="22" cy="19" r="5.5" fill="#ef4444" />
  <circle cx="38" cy="19" r="5.5" fill="#f59e0b" />
  <circle cx="54" cy="19" r="5.5" fill="#10b981" />

  <!-- Window Title -->
  <text x="220" y="23" text-anchor="middle" class="info-title">sonu@system: ~ (neofetch)</text>

  <!-- Divider Line -->
  <line x1="0" y1="36" x2="{width}" y2="36" stroke="#21262d" stroke-width="1" />

  <!-- Content Rows -->
  <g transform="translate(24, 60)">'''

    y_offset = 0
    line_gap = 21
    current_time = 0.15

    for item in lines:
        kind = item[0]
        delay = round(current_time, 3)
        style = f"animation: slideInLine 0.3s cubic-bezier(0.16, 1, 0.3, 1) {delay}s forwards;"

        if kind == "HEADER":
            svg += f'''
    <g class="term-line" style="{style}" transform="translate(0, {y_offset})">
      <text font-weight="700" font-size="13" fill="#38bdf8">{item[1]}</text>
    </g>'''
            y_offset += 16
        elif kind == "SEP":
            svg += f'''
    <g class="term-line" style="{style}" transform="translate(0, {y_offset})">
      <text fill="#475569">{item[1]}</text>
    </g>'''
            y_offset += 20
        else:
            _, label, val, l_col, v_col = item
            svg += f'''
    <g class="term-line" style="{style}" transform="translate(0, {y_offset})">
      <text>
        <tspan fill="{l_col}" font-weight="600">{label}: </tspan>
        <tspan fill="{v_col}">{val}</tspan>
      </text>
    </g>'''
            y_offset += line_gap

        current_time += 0.06

    # Neofetch 8-color test palette strip at bottom
    palette_colors_dark = ["#1e293b", "#ef4444", "#22c55e", "#eab308", "#3b82f6", "#a855f7", "#06b6d4", "#f8fafc"]
    palette_colors_light = ["#475569", "#f87171", "#4ade80", "#fde047", "#60a5fa", "#c084fc", "#22d3ee", "#ffffff"]

    block_w = 21
    block_h = 11
    block_spacing = 26
    strip_y = 350
    strip_delay = round(current_time + 0.1, 3)

    svg += f'''
  </g>

  <!-- Neofetch Color Test Bars -->
  <g transform="translate(24, {strip_y})">'''

    for idx, c in enumerate(palette_colors_dark):
        b_x = idx * block_spacing
        b_delay = round(strip_delay + (idx * 0.03), 3)
        b_style = f"animation: popColorBlock 0.25s ease-out {b_delay}s forwards;"
        svg += f'\n    <rect class="color-block" x="{b_x}" y="0" width="{block_w}" height="{block_h}" rx="2" fill="{c}" style="{b_style}" />'

    for idx, c in enumerate(palette_colors_light):
        b_x = idx * block_spacing
        b_delay = round(strip_delay + 0.2 + (idx * 0.03), 3)
        b_style = f"animation: popColorBlock 0.25s ease-out {b_delay}s forwards;"
        svg += f'\n    <rect class="color-block" x="{b_x}" y="15" width="{block_w}" height="{block_h}" rx="2" fill="{c}" style="{b_style}" />'

    svg += '''
  </g>
</svg>'''

    output_path = os.path.join(OUTPUT_DIR, "info-card.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated: {output_path}")


# -------------------------------------------------------------------------
# 4. INJECT INTO README.md
# -------------------------------------------------------------------------
def inject_into_readme():
    readme_path = os.path.join(OUTPUT_DIR, "README.md")
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} does not exist.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    cards_block = """<!-- ======================================================== -->
<!-- DYNAMIC CYBERPUNK TERMINAL & CONTRIBUTION SECTION -->
<!-- ======================================================== -->
<div align="center">
  <table border="0" cellspacing="0" cellpadding="0" style="border: none; border-collapse: collapse; background: transparent;">
    <tr>
      <td width="50%" align="center" valign="top" style="border: none; padding: 6px;">
        <img src="./terminal-card.svg" width="100%" alt="Sonu's ASCII Portrait Terminal" />
      </td>
      <td width="50%" align="center" valign="top" style="border: none; padding: 6px;">
        <img src="./info-card.svg" width="100%" alt="Sonu's Neofetch System Info" />
      </td>
    </tr>
  </table>
  <br/>
  <img src="./github-contribution-animation.svg" width="100%" alt="Sonu's GitHub Contribution Activity" />
</div>
<!-- ======================================================== -->"""

    # Check if markers already exist
    marker_start = "<!-- DYNAMIC CYBERPUNK TERMINAL & CONTRIBUTION SECTION -->"
    if marker_start in content:
        # Replace existing section
        import re
        content = re.sub(
            r"<!-- ======================================================== -->\s*<!-- DYNAMIC CYBERPUNK TERMINAL & CONTRIBUTION SECTION -->.*?<!-- ======================================================== -->",
            cards_block,
            content,
            flags=re.DOTALL
        )
    else:
        # Inject right above "### 🛠️ Tech Stack & Tooling" or "### 🌌 About Me"
        if "### 🛠️ Tech Stack & Tooling" in content:
            content = content.replace("### 🛠️ Tech Stack & Tooling", f"{cards_block}\n\n---\n\n### 🛠️ Tech Stack & Tooling")
        else:
            content += f"\n\n{cards_block}"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated README.md with injected animated cards!")


# -------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("Generating animated SVGs...")
    generate_contribution_svg()
    generate_terminal_card_svg()
    generate_info_card_svg()
    inject_into_readme()
    print("All tasks completed successfully!")
