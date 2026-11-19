#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
SOURCE_FILES=(
  docs/gnome-51/index.md
  docs/gnome-51/01-architecture.md
  docs/gnome-51/02-gnome-shell.md
  docs/gnome-51/03-gtk-libadwaita.md
  docs/gnome-51/04-reference-css.md
  docs/gnome-51/05-parametres-gnome.md
  docs/gnome-51/06-ressources-visuelles.md
  docs/gnome-51/07-extensions-mutter-gdm.md
  docs/gnome-51/08-accessibilite.md
  docs/gnome-51/09-construction-validation.md
  docs/gnome-51/10-sources-et-inventaire.md
)
pandoc "${SOURCE_FILES[@]}" --from=gfm --to=epub3 \
  --metadata title="Manuel complet de personnalisation GNOME 51" \
  --metadata lang=fr --metadata author="G-OS Theme Maker" \
  --toc --toc-depth=3 --output=docs/guide-theme-gnome.epub
pandoc "${SOURCE_FILES[@]}" --from=gfm --to=html5 --standalone \
  --metadata title="Manuel complet de personnalisation GNOME 51" \
  --metadata lang=fr --css=docs/guide.css --toc --toc-depth=3 \
  --pdf-engine=weasyprint --output=docs/guide-theme-gnome.pdf
echo "Documentation générée."
