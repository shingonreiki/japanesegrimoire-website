#!/usr/bin/env python3
"""Convert a source image into hero (1600x900) and card (800x450) WebP for an article slug.
Usage: python3 _tools/img.py <source.png> <slug>"""
import sys, os
from PIL import Image
src, slug = sys.argv[1], sys.argv[2]
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public', 'images', 'blog')
os.makedirs(out, exist_ok=True)
im = Image.open(src).convert('RGB')
w, h = im.size; th = int(w * 9 / 16)
if th <= h: top = (h - th) // 2; im = im.crop((0, top, w, top + th))
im.resize((1600, 900), Image.LANCZOS).save(os.path.join(out, slug + '.webp'), 'WEBP', quality=80, method=6)
im.resize((800, 450), Image.LANCZOS).save(os.path.join(out, slug + '-card.webp'), 'WEBP', quality=78, method=6)
print('ok', slug)
