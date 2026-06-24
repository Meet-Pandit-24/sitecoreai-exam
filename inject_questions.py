import json

with open(r'C:\Projects\SitecoreAI\questions_merged.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

questions_js = json.dumps(questions, ensure_ascii=False)

with open(r'C:\Projects\SitecoreAI\exam-enhanced.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('""" + questions_js + """', questions_js)

with open(r'C:\Projects\SitecoreAI\exam-enhanced.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Injected {len(questions)} questions into exam-enhanced.html")
print(f"File size: {len(html):,} bytes")
