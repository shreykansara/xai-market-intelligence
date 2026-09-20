import re

with open('web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_svg = '''<svg class="omniscope-logo-svg nav-logo-svg" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M18 3L4 10V26L18 33L32 26V10L18 3Z" stroke="#2B374E" stroke-width="1.5" stroke-linejoin="round"/>
    <path d="M18 7L8 12.5V23.5L18 29L28 23.5V12.5L18 7Z" stroke="#3B82F6" stroke-width="2" stroke-linejoin="round"/>
    <path d="M18 12L12 15.5V20.5L18 24L24 20.5V15.5L18 12Z" fill="#2563EB" fill-opacity="0.25" stroke="#60A5FA" stroke-width="1.5" stroke-linejoin="round"/>
    <circle cx="18" cy="18" r="2.5" fill="#F8FAFC"/>
</svg>'''

# Regex to match any <svg class="omniscope-logo-svg[^>]*>...</svg>
pattern = re.compile(r'<svg class="omniscope-logo-svg[^>]*>.*?</svg>', re.DOTALL)

matches = pattern.findall(html)
print(f"Found {len(matches)} old logo SVGs to replace.")

html = pattern.sub(new_svg, html)

# Replace <span class="accent-text">AI</span> with <span class="brand-pill">AI</span>
html = html.replace('<span class="accent-text">AI</span>', '<span class="brand-pill">AI</span>')

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated all logo SVGs and brand pills in web/index.html!")
