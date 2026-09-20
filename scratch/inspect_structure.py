with open('web/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

open_divs = 0
for idx, line in enumerate(lines, 1):
    opens = line.count('<div')
    closes = line.count('</div')
    open_divs += (opens - closes)
    if 1040 <= idx <= 1420:
        if opens > 0 or closes > 0:
            print(f"Line {idx:4d} (+{opens}/-{closes}) -> open_divs={open_divs:2d} | {line.strip()[:70]}")
