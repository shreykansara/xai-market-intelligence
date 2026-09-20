import re

with open('web/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Replace drop-shadow glow filters
css = re.sub(r'filter:\s*drop-shadow\([^)]*rgba\(0,\s*255,\s*102[^)]*\)\);?', 'filter: none;', css)
css = re.sub(r'filter:\s*drop-shadow\([^)]*rgba\(0,\s*229,\s*255[^)]*\)\);?', 'filter: none;', css)

# 2. Replace glowing box shadows
css = re.sub(r'box-shadow:\s*0\s+0\s+\d+px\s+rgba\(0,\s*255,\s*102,[^;)]+\);?', 'box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);', css)
css = re.sub(r'box-shadow:\s*0\s+0\s+\d+px\s+rgba\(0,\s*229,\s*255,[^;)]+\);?', 'box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);', css)
css = re.sub(r',\s*0\s+0\s+\d+px\s+rgba\(0,\s*255,\s*102,[^;)]+\)', '', css)
css = re.sub(r',\s*0\s+0\s+\d+px\s+rgba\(0,\s*229,\s*255,[^;)]+\)', '', css)

# 3. Replace background and border rgba(0, 255, 102, ...)
css = re.sub(r'rgba\(0,\s*255,\s*102,\s*([0-9.]+)\)', r'rgba(16, 185, 129, \1)', css)
# 4. Replace background and border rgba(0, 229, 255, ...)
css = re.sub(r'rgba\(0,\s*229,\s*255,\s*([0-9.]+)\)', r'rgba(59, 130, 246, \1)', css)

# 5. Clean text glows
css = re.sub(r'text-shadow:\s*0\s+0\s+\d+px[^;]+;', 'text-shadow: none;', css)

with open('web/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Cleaned all neon glows and replaced with subtle institutional financial tints!")
