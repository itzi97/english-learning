import json
import os
import re

with open('vocabulary.json', encoding='utf-8') as f:
    words = json.load(f)


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def build_table_lines(word_list, include_source_col=True):
    if include_source_col:
        headers = [
            '| Page | Word | Definition | Example Sentence | Source |',
            '|------|------|------------|-----------------|--------|',
        ]
    else:
        headers = [
            '| Page | Word | Definition | Example Sentence |',
            '|------|------|------------|-----------------|',
        ]
    rows = []
    for w in word_list:
        page = w.get('page') or '\u2014'
        word = w.get('word', '')
        definition = w.get('definition', '')
        example = w.get('example', '')
        source = w.get('source', '')
        if include_source_col:
            rows.append(f'| {page} | {word} | {definition} | "{example}" | *{source}* |')
        else:
            rows.append(f'| {page} | {word} | {definition} | "{example}" |')
    return headers + rows


# Generate combined vocabulary.md
lines = [
    '# \U0001f4d6 Vocabulary\n',
    'All words logged across every book, with definitions and context.\n',
]
lines += build_table_lines(words, include_source_col=True)
lines += [
    '',
    '---',
    '',
    '> Add new words to `vocabulary.json` \u2014 this file is auto-generated from it.',
]
with open('vocabulary.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print(f'Generated vocabulary.md with {len(words)} words.')


# Generate per-book markdown files in vocabulary/
os.makedirs('vocabulary', exist_ok=True)

books = {}
for w in words:
    source = w.get('source', 'Unknown')
    books.setdefault(source, []).append(w)

for source, book_words in books.items():
    slug = slugify(source)
    filename = f'vocabulary/{slug}.md'
    author = book_words[0].get('author') or ''
    author_line = f'*{author}*  \n' if author else ''
    lines = [
        f'# \U0001f4d6 {source}\n',
        f'{author_line}',
        f'Words logged while reading this book.\n',
    ]
    lines += build_table_lines(book_words, include_source_col=False)
    lines += [
        '',
        '---',
        '',
        '> Auto-generated from `vocabulary.json`. Do not edit manually.',
    ]
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'Generated {filename} with {len(book_words)} words.')


# Update vocabulary/README.md with an index of all book files
index_lines = [
    '# \U0001f4da Vocabulary by Book\n',
    'Auto-generated index of per-book vocabulary files.\n',
    '| Book | Author | Words |',
    '|------|--------|-------|',
]
for source, book_words in books.items():
    slug = slugify(source)
    author = book_words[0].get('author') or '\u2014'
    count = len(book_words)
    index_lines.append(f'| [{source}]({slug}.md) | {author} | {count} |')
index_lines += [
    '',
    '---',
    '',
    '> Auto-generated from `vocabulary.json`. Do not edit manually.',
]
with open('vocabulary/README.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(index_lines) + '\n')
print('Generated vocabulary/README.md index.')
