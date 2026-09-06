import os
from PIL import Image, ImageDraw

def generate_favicons():
    web_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'web')
    os.makedirs(web_dir, exist_ok=True)

    # 1. Write favicon.svg
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="14" fill="#050505"/>
  <circle cx="32" cy="32" r="26" stroke="#00FF66" stroke-width="2" stroke-dasharray="4 3" opacity="0.6"/>
  <circle cx="32" cy="32" r="20" stroke="#00FF66" stroke-width="3" fill="none"/>
  <circle cx="32" cy="32" r="12" stroke="#00E5FF" stroke-width="2" fill="none"/>
  <circle cx="32" cy="32" r="4" fill="#00FF66"/>
  <line x1="32" y1="4" x2="32" y2="60" stroke="#00FF66" stroke-width="1.5" opacity="0.5"/>
  <line x1="4" y1="32" x2="60" y2="32" stroke="#00FF66" stroke-width="1.5" opacity="0.5"/>
  <circle cx="48" cy="32" r="3" fill="#00E5FF"/>
  <circle cx="32" cy="16" r="3" fill="#00FF66"/>
  <circle cx="21" cy="43" r="3" fill="#10B981"/>
</svg>'''

    svg_path = os.path.join(web_dir, 'favicon.svg')
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Generated {svg_path}")

    # 2. Draw PIL Image for PNG and ICO (High-Res 256x256 scaled down for clean anti-aliasing)
    size = 256
    img = Image.new("RGBA", (size, size), (5, 5, 5, 255))
    draw = ImageDraw.Draw(img)

    center = size // 2
    r_outer = int(size * 0.40)
    r_mid = int(size * 0.30)
    r_inner = int(size * 0.18)
    r_center = int(size * 0.06)

    # Colors
    c_green = (0, 255, 102, 255)
    c_cyan = (0, 229, 255, 255)
    c_green_alpha = (0, 255, 102, 120)
    c_emerald = (16, 185, 129, 255)

    # Crosshairs
    draw.line([(center, 16), (center, size - 16)], fill=c_green_alpha, width=4)
    draw.line([(16, center), (size - 16, center)], fill=c_green_alpha, width=4)

    # Concentric circles
    draw.ellipse([center - r_outer, center - r_outer, center + r_outer, center + r_outer], outline=c_green_alpha, width=6)
    draw.ellipse([center - r_mid, center - r_mid, center + r_mid, center + r_mid], outline=c_green, width=10)
    draw.ellipse([center - r_inner, center - r_inner, center + r_inner, center + r_inner], outline=c_cyan, width=8)

    # Center dot
    draw.ellipse([center - r_center, center - r_center, center + r_center, center + r_center], fill=c_green)

    # Vector nodes
    node_r = 10
    # Right node
    draw.ellipse([center + r_mid - node_r, center - node_r, center + r_mid + node_r, center + node_r], fill=c_cyan)
    # Top node
    draw.ellipse([center - node_r, center - r_mid - node_r, center + node_r, center - r_mid + node_r], fill=c_green)
    # Bottom left node
    bx = int(center - r_mid * 0.5)
    by = int(center + r_mid * 0.7)
    draw.ellipse([bx - node_r, by - node_r, bx + node_r, by + node_r], fill=c_emerald)

    # Save PNG
    png_path = os.path.join(web_dir, 'favicon.png')
    img_png = img.resize((64, 64), Image.Resampling.LANCZOS)
    img_png.save(png_path, 'PNG')
    print(f"Generated {png_path}")

    # Save ICO (multi-size: 16x16, 32x32, 48x48)
    ico_path = os.path.join(web_dir, 'favicon.ico')
    img.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print(f"Generated {ico_path}")

if __name__ == '__main__':
    generate_favicons()
