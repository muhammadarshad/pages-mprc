"""
apply_lazy_nav.py
Replaces the inline <aside class="book-sidebar">...</aside> block in every
HTML page with a single <div id="nav-placeholder"></div> and injects
<script src="loader.js"></script> before </body>.
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

HTML_FILES = [
    'index.html',
    'chapter-1.html',  'chapter-2.html',  'chapter-3.html',
    'chapter-4.html',  'chapter-5.html',  'chapter-6.html',
    'chapter-7.html',  'chapter-8.html',  'chapter-9.html',
    'chapter-10.html', 'chapter-11.html', 'chapter-12.html',
    'chapter-13.html', 'chapter-14.html', 'chapter-15.html',
    'chapter-16.html',
    'philosophical.html', 'mprc-time-definition.html', 'mprc-kinematics.html',
]

# Matches the entire <aside class="book-sidebar"> ... </aside> block
ASIDE_RE = re.compile(
    r'\s*<aside\s+class="book-sidebar">.*?</aside>',
    re.DOTALL
)

PLACEHOLDER = '\n  <div id="nav-placeholder"></div>'
SCRIPT_TAG  = '\n<script src="loader.js"></script>\n'

changed = 0
skipped = 0

for fname in HTML_FILES:
    path = os.path.join(ROOT, fname)
    if not os.path.isfile(path):
        print(f'  MISSING  {fname}')
        skipped += 1
        continue

    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()

    # Replace aside block
    new_src, n_aside = ASIDE_RE.subn(PLACEHOLDER, src)
    if n_aside == 0:
        print(f'  NO ASIDE {fname}')
        skipped += 1
        continue

    # Inject loader script before </body> (only if not already there)
    if 'loader.js' not in new_src:
        new_src = new_src.replace('</body>', SCRIPT_TAG + '</body>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_src)

    print(f'  OK       {fname}  (aside replacements: {n_aside})')
    changed += 1

print(f'\nDone — {changed} files updated, {skipped} skipped.')
