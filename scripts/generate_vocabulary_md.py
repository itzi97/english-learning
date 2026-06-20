import json

with open('vocabulary.json', encoding='utf-8') as f:
    words = json.load(f)

lines = [
    '# \U0001f4d6 Vocabulary\n',
    'Words I\'ve had trouble understanding while reading, with definitions and context.\n',
    '| Page | Word | Definition | Example Sentence | Source |',
    '|------|------|------------|-----------------|--------|',
]

for w in words:
    page = w.get('page') or '\u2014'
    word = w.get('word', '')
    definition = w.get('definition', '')
    example = w.get('example', '')
    source = w.get('source', '')
    lines.append(f'| {page} | {word} | {definition} | "{example}" | *{source}* |')

lines += [
    '',
    '---',
    '',
    '> Add new words to `vocabulary.json` \u2014 this file is auto-generated from it.'
]

with open('vocabulary.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print(f'Generated vocabulary.md with {len(words)} words.')
