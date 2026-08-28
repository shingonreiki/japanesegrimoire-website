#!/bin/bash
# Laedt die Site-Bilder beim Build (noch nicht alle im Repo).
set -e
mkdir -p public/images
SOURCES="https://snazzy-bubblegum-db4b1b.netlify.app https://japanesegrimoire.com"
FILES="logo.webp hero-bg.webp glimpse-1-start-here.webp glimpse-2-living-roots.webp glimpse-3-first-touch.webp mark-hosak.webp logo.png"
for f in $FILES; do
  if [ -s "public/images/$f" ]; then echo "exists: $f"; continue; fi
  ok=""
  for s in $SOURCES; do
    if curl -fsSL "$s/images/$f" -o "public/images/$f"; then ok=1; echo "fetched: $f from $s"; break; fi
  done
  if [ -z "$ok" ]; then echo "FAILED to fetch $f" >&2; exit 1; fi
done
echo "build done"
