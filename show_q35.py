import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Projects\SitecoreAI\questions_v3.json', 'r', encoding='utf-8') as f:
    v3 = json.load(f)
with open(r'C:\Projects\SitecoreAI\questions.json', 'r', encoding='utf-8') as f:
    v4 = json.load(f)

def show(label, qlist, qid):
    try:
        q = next(x for x in qlist if x['id'] == qid)
        print(f"\n=== {label} ===")
        print(q['question'][:120])
        for o in q['options']:
            mark = ' [CORRECT]' if o['correct'] else ''
            print(f"  {o['key']}. {o['text'][:70]}{mark}")
        print(f"Answer: {q['answer']}")
    except StopIteration:
        print(f"\n=== {label} === NOT FOUND")

show("V3 Q35", v3, 35)
show("V4 Q35", v4, 35)
show("V3 Q66", v3, 66)
show("V4 Q55", v4, 55)
show("V3 Q77", v3, 77)
show("V4 Q175", v4, 175)
show("V3 Q89", v3, 89)
show("V4 Q161", v4, 161)
show("V3 Q91", v3, 91)
show("V4 Q172", v4, 172)
show("V3 Q150", v3, 150)
show("V4 Q150", v4, 150)
