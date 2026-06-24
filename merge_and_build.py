import json, re
from difflib import SequenceMatcher

with open(r'C:\Projects\SitecoreAI\questions_v3.json', 'r', encoding='utf-8') as f:
    v3 = json.load(f)
with open(r'C:\Projects\SitecoreAI\questions.json', 'r', encoding='utf-8') as f:
    v4 = json.load(f)

def norm(s):
    return re.sub(r'\s+', ' ', s.lower().strip())

def similarity(a, b):
    return SequenceMatcher(None, norm(a), norm(b)).ratio()

# Find V3 questions that are NOT in V4 (similarity < 0.80)
v4_norms = [norm(q['question']) for q in v4]

new_from_v3 = []
for q3 in v3:
    best = max(similarity(norm(q3['question']), t) for t in v4_norms)
    if best < 0.80:
        new_from_v3.append(q3)

print(f"V4 base: {len(v4)} questions")
print(f"New from V3 (not in V4): {len(new_from_v3)}")

# Assign new IDs to V3-only questions (starting from 178)
merged = list(v4)
next_id = max(q['id'] for q in v4) + 1
for q3 in new_from_v3:
    new_q = dict(q3)
    new_q['id'] = next_id
    new_q['source'] = 'V3'
    next_id += 1
    merged.append(new_q)

print(f"Merged total: {len(merged)} questions")

with open(r'C:\Projects\SitecoreAI\questions_merged.json', 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
print("Saved questions_merged.json")

# Print sample of added questions
print("\nSample of newly added V3 questions:")
for q in new_from_v3[:10]:
    print(f"  Q{q['id']} -> new ID {q['id']+177}: {q['question'][:70]}")
    print(f"    Answer: {q['answer']}")
