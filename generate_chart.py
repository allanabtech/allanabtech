import urllib.request
import json
import os
import math

def fetch_top_languages():
    token = os.getenv("GITHUB_TOKEN")
    headers = {"User-Agent": "Mozilla/5.0"}
    if token:
        headers["Authorization"] = f"token {token}"
        
    lang_bytes = {}
    try:
        # Fetch repos
        repos_url = "https://api.github.com/users/allanabtech/repos?per_page=100"
        req = urllib.request.Request(repos_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            repos = json.loads(response.read().decode())
            for r in repos:
                if r.get("fork"):
                    continue
                repo_name = r.get("name")
                # Fetch languages for each repo
                langs_url = f"https://api.github.com/repos/allanabtech/{repo_name}/languages"
                l_req = urllib.request.Request(langs_url, headers=headers)
                try:
                    with urllib.request.urlopen(l_req) as l_resp:
                        langs = json.loads(l_resp.read().decode())
                        for lang, byte_cnt in langs.items():
                            lang_bytes[lang] = lang_bytes.get(lang, 0) + byte_cnt
                except Exception as e:
                    print(f"Skipping repo {repo_name} due to error: {e}")
    except Exception as e:
        print(f"Failed to fetch repositories: {e}")
        
    return lang_bytes

def generate_svg(lang_bytes):
    total = sum(lang_bytes.values())
    if total == 0:
        # Fallback stats
        stats = [("C", 40.0), ("Python", 30.0), ("C++", 15.0), ("TypeScript", 10.0), ("Assembly", 5.0)]
    else:
        sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)[:5]
        stats = [(lang, (bytes_cnt / total) * 100) for lang, bytes_cnt in sorted_langs]

    # Theme colors mapping (base, light/top, dark/left, medium/right)
    theme_colors = {
        "Python":     {"base": "#35E2B5", "top": "#4DF5C9", "left": "#1E9D7A", "right": "#28BFA3"},
        "C":          {"base": "#FF4B72", "top": "#FF7392", "left": "#C72246", "right": "#E83A60"},
        "C++":        {"base": "#FF8DA1", "top": "#FFAEBF", "left": "#D15C71", "right": "#E8748A"},
        "TypeScript": {"base": "#A78BFA", "top": "#C084FC", "left": "#6D28D9", "right": "#8B5CF6"},
        "SQL":        {"base": "#00F0FF", "top": "#64F6FF", "left": "#00A8B5", "right": "#00D2E0"},
        "Assembly":   {"base": "#FBBF24", "top": "#FDE047", "left": "#B45309", "right": "#D97706"},
        "Java":       {"base": "#FB923C", "top": "#FDBA74", "left": "#C2410C", "right": "#EA580C"}
    }
    
    # Fallback colors for unknown languages
    default_colors = {"base": "#94A3B8", "top": "#CBD5E1", "left": "#475569", "right": "#64748B"}

    svg_width = 600
    svg_height = 280

    # Start constructing SVG
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <style>
    .bg {{ fill: #0D080B; rx: 12px; }}
    .grid-line {{ stroke: #3A1024; stroke-width: 0.5; opacity: 0.2; }}
    .label-text {{ font-family: 'Segoe UI', system-ui, sans-serif; font-size: 11px; fill: #E2E8F0; font-weight: 500; }}
    .percentage-text {{ font-family: 'Fira Code', monospace; font-size: 11px; fill: #FF8DA1; font-weight: 600; }}
    .title-text {{ font-family: 'Segoe UI', system-ui, sans-serif; font-size: 14px; font-weight: 700; fill: #FF4B72; letter-spacing: 1px; }}
    
    @keyframes growBar {{
      from {{ transform: scaleY(0); }}
      to {{ transform: scaleY(1); }}
    }}
    .bar-group {{
      transform-origin: bottom;
      animation: growBar 1.5s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }}
  </style>

  <!-- Background -->
  <rect width="{svg_width}" height="{svg_height}" class="bg" />

  <text x="30" y="35" class="title-text">3D LANGUAGE METRICS</text>

  <!-- Isometric Ground Grid -->
  <g class="grid">
"""
    # Drawing isometric grid lines for visual depth
    for i in range(-5, 10):
        # Line type 1
        x1, y1 = 150 + i * 20, 260 - i * 10
        x2, y2 = 450 + i * 20, 110 - i * 10
        svg_content += f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="grid-line" />\n'
        # Line type 2
        x1, y1 = 450 - i * 20, 260 - i * 10
        x2, y2 = 150 - i * 20, 110 - i * 10
        svg_content += f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="grid-line" />\n'

    svg_content += "  </g>\n\n"

    # Bases centers for the 5 isometric columns
    # We stagger them from left-front to right-back
    bases = [
        (130, 200), # Bar 1
        (210, 180), # Bar 2
        (290, 160), # Bar 3
        (370, 140), # Bar 4
        (450, 120)  # Bar 5
    ]

    # Draw the columns
    for idx, (lang, pct) in enumerate(stats):
        if idx >= len(bases):
            break
            
        cx, cy = bases[idx]
        colors = theme_colors.get(lang, default_colors)

        # Scale height based on percentage (max height = 110px)
        max_h = 110
        h = max(10, int((pct / 100.0) * max_h))

        w = 18 # Half-width along X isometric axis
        d = 18 # Half-depth along Y isometric axis

        # Calculate vertices coordinates
        # Base Vertices
        v0 = (cx, cy + d)
        v1 = (cx - w * 0.866, cy + d * 0.5)
        v2 = (cx, cy)
        v3 = (cx + w * 0.866, cy + d * 0.5)

        # Top Vertices (Shifted up by h)
        v4 = (v0[0], v0[1] - h)
        v5 = (v1[0], v1[1] - h)
        v6 = (v2[0], v2[1] - h)
        v7 = (v3[0], v3[1] - h)

        # Define 3D bar group with separate scale transition origin
        svg_content += f'  <!-- 3D Bar for {lang} ({pct:.1f}%) -->\n'
        svg_content += f'  <g class="bar-group" style="transform-origin: {cx}px {cy + d}px;">\n'
        
        # Left Side Face (Dark shade)
        svg_content += f'    <path d="M {v5[0]:.1f},{v5[1]:.1f} L {v1[0]:.1f},{v1[1]:.1f} L {v0[0]:.1f},{v0[1]:.1f} L {v4[0]:.1f},{v4[1]:.1f} Z" fill="{colors["left"]}" />\n'
        
        # Right Side Face (Medium shade)
        svg_content += f'    <path d="M {v4[0]:.1f},{v4[1]:.1f} L {v0[0]:.1f},{v0[1]:.1f} L {v3[0]:.1f},{v3[1]:.1f} L {v7[0]:.1f},{v7[1]:.1f} Z" fill="{colors["right"]}" />\n'
        
        # Top Face (Light top shade)
        svg_content += f'    <path d="M {v6[0]:.1f},{v6[1]:.1f} L {v5[0]:.1f},{v5[1]:.1f} L {v4[0]:.1f},{v4[1]:.1f} L {v7[0]:.1f},{v7[1]:.1f} Z" fill="{colors["top"]}" />\n'
        
        svg_content += "  </g>\n"

        # Text labels - placed above the column tops
        tx = cx
        ty = v6[1] - 12
        svg_content += f'  <g>\n'
        svg_content += f'    <text x="{tx}" y="{ty}" text-anchor="middle" class="label-text">{lang}</text>\n'
        svg_content += f'    <text x="{tx}" y="{ty + 11}" text-anchor="middle" class="percentage-text">{pct:.1f}%</text>\n'
        
        # Draw a small dotted line connecting label to the top face
        svg_content += f'    <line x1="{cx}" y1="{v6[1]}" x2="{tx}" y2="{ty + 13}" stroke="{colors["base"]}" stroke-width="1" stroke-dasharray="2 2" opacity="0.6" />\n'
        svg_content += f'  </g>\n\n'

    svg_content += "</svg>\n"
    return svg_content

if __name__ == "__main__":
    lang_bytes = fetch_top_languages()
    svg_data = generate_svg(lang_bytes)
    
    # Save chart to main folder
    with open("languages-3d.svg", "w", encoding="utf-8") as f:
        f.write(svg_data)
    print("3D languages chart generated successfully.")
