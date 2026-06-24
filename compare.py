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

# For each V3 question, find best match in V4
v4_texts = [(q, norm(q['question'])) for q in v4]

matched_v4_ids = set()
v3_only = []      # in V3 but not matched in V4
answer_diffs = [] # same question, different answer

for q3 in v3:
    best_score = 0
    best_v4 = None
    for q4, t4 in v4_texts:
        s = similarity(q3['question'], q4['question'])
        if s > best_score:
            best_score = s
            best_v4 = q4

    if best_score >= 0.80:
        matched_v4_ids.add(best_v4['id'])
        # Check answer difference
        if q3['answer'] != best_v4['answer']:
            answer_diffs.append({
                'v3_id': q3['id'],
                'v4_id': best_v4['id'],
                'question': q3['question'],
                'v3_answer': q3['answer'],
                'v4_answer': best_v4['answer'],
                'similarity': round(best_score, 3)
            })
    else:
        v3_only.append({'score': round(best_score, 3), 'q': q3})

# Questions in V4 not matched from V3 (new in V4)
v4_only = [q for q in v4 if q['id'] not in matched_v4_ids]

print(f"V3 questions: {len(v3)}")
print(f"V4 questions: {len(v4)}")
print(f"Matched (same in both): {len(v3) - len(v3_only)}")
print(f"V3-only (not in V4): {len(v3_only)}")
print(f"V4-only (new in V4): {len(v4_only)}")
print(f"Answer differences: {len(answer_diffs)}")

print("\n--- V3-ONLY QUESTIONS (potential additions) ---")
for item in v3_only:
    print(f"Q{item['q']['id']} (best match score: {item['score']}): {item['q']['question'][:80]}")
    print(f"  Answer: {item['q']['answer']}, Options: {len(item['q']['options'])}")

print("\n--- ANSWER DIFFERENCES ---")
for d in answer_diffs:
    print(f"V3-Q{d['v3_id']} vs V4-Q{d['v4_id']} (sim={d['similarity']})")
    print(f"  Q: {d['question'][:70]}")
    print(f"  V3 answer: {d['v3_answer']}  |  V4 answer: {d['v4_answer']}")

# Save V3-only questions for potential addition
with open(r'C:\Projects\SitecoreAI\v3_only.json', 'w', encoding='utf-8') as f:
    json.dump([x['q'] for x in v3_only], f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(v3_only)} V3-only questions to v3_only.json")
