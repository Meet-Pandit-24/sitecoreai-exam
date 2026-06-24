import json
with open(r'C:\Projects\SitecoreAI\questions.json', 'r', encoding='utf-8') as f:
    q = json.load(f)
multi = [x for x in q if x['multi']]
print(f'Multi-select: {len(multi)}')
for m in multi[:5]:
    print(f'Q{m["id"]}: answer={m["answer"]}, options={len(m["options"])}')
print(f'Total: {len(q)}')
