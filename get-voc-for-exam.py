import json
import os
import random
import re

# Directory containing the JSON files
VOC_DIR = 'page/voc'
LEVELS = range(1, 7)
RESULT_COUNT = 100
TERM_PATTERN = re.compile(r'^[a-z]+$')  # Only lowercase English letters

result = {level: [] for level in LEVELS}
all_terms = []

# Collect all valid terms from all levels
for level in LEVELS:
    file_path = os.path.join(VOC_DIR, f'level-{level}.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # data is a list of lists, each containing dictionary objects
        for word_list in data:
            if isinstance(word_list, list):
                for word_dict in word_list:
                    if isinstance(word_dict, dict):
                        term = word_dict.get('term', '')
                        if term and TERM_PATTERN.fullmatch(term):
                            all_terms.append((level, term))

# Randomly select 100 unique terms
selected = random.sample(all_terms, min(RESULT_COUNT, len(all_terms)))

# Organize by level
for level, term in selected:
    result[level].append(term)

# Save to JSON
with open('selected_terms.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)