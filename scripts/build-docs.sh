#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SOURCE="docs/guide-theme-gnome.md"
EPUB="docs/guide-theme-gnome.epub"
PDF="docs/guide-theme-gnome.pdf"

pandoc "$SOURCE" \
  --from=gfm \
  --to=epub3 \
  --metadata title="Créer un thème GNOME complet" \
  --metadata lang=fr \
  --metadata author="G-OS Theme Maker" \
  --toc \
  --output="$EPUB"

pandoc "$SOURCE" \
  --from=gfm \
  --to=html5 \
  --standalone \
  --metadata title="Créer un thème GNOME complet" \
  --css=docs/guide.css \
  --pdf-engine=weasyprint \
  --output="$PDF"

echo "Documentation générée : $EPUB et $PDF"
