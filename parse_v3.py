import re, json

with open(r'C:\Projects\SitecoreAI\doc_v3_text.txt', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

questions = []
current_q = None
current_opts = []
answer_line = None

for line in lines:
    line = line.strip()
    q_match = re.match(r'^Q(\d+)\.\s+(.+)', line)
    if q_match:
        if current_q and answer_line:
            questions.append({
                'id': current_q['id'],
                'question': current_q['text'],
                'options': current_opts,
                'answer': answer_line,
                'multi': ',' in answer_line
            })
        num = int(q_match.group(1))
        current_q = {'id': num, 'text': q_match.group(2)}
        current_opts = []
        answer_line = None
        continue

    opt_match = re.match(r'^([A-E])\.\s+(.+?)(\s+✓ CORRECT)?$', line)
    if opt_match and current_q:
        current_opts.append({
            'key': opt_match.group(1),
            'text': opt_match.group(2).strip(),
            'correct': bool(opt_match.group(3))
        })
        continue

    ans_match = re.match(r'^Answer:\s+([A-E, ]+)', line)
    if ans_match and current_q:
        answer_line = ans_match.group(1).strip().replace(' ', '')
        continue

if current_q and answer_line:
    questions.append({
        'id': current_q['id'],
        'question': current_q['text'],
        'options': current_opts,
        'answer': answer_line,
        'multi': ',' in answer_line
    })

# Fix correct flags
for q in questions:
    ans_keys = [a.strip() for a in q['answer'].split(',')]
    for opt in q['options']:
        opt['correct'] = opt['key'] in ans_keys

print(f'V3 total questions: {len(questions)}')
with open(r'C:\Projects\SitecoreAI\questions_v3.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)
print('Saved questions_v3.json')
