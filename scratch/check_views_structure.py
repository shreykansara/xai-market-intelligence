from html.parser import HTMLParser

VOID_TAGS = {'meta', 'link', 'img', 'br', 'hr', 'input', 'source'}

class DetailedParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        attrs_dict = dict(attrs)
        line, col = self.getpos()
        self.stack.append((tag, attrs_dict.get('id', ''), attrs_dict.get('class', ''), line))
    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        line, col = self.getpos()
        if not self.stack:
            print(f"Line {line}: Unexpected closing </{tag}> (empty stack)")
            return
        popped = self.stack.pop()
        if popped[0] != tag:
            print(f"Line {line}: MISMATCH: Expected </{popped[0]}> (opened at line {popped[3]} id='{popped[1]}' class='{popped[2]}'), but found </{tag}>")

with open('web/index.html', 'r', encoding='utf-8') as f:
    p = DetailedParser()
    p.feed(f.read())
