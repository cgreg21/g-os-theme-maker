#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Le manuel exporté inclut le parcours débutant, les chapitres illustrés et les références.
SOURCE_FILES=(
  docs/gnome-51/index.md
  docs/gnome-51/00-bien-demarrer.md
  docs/gnome-51/01-creer-premier-theme.md
  docs/gnome-51/02-css-debutant.md
  docs/gnome-51/03-atelier-gnome-shell.md
  docs/gnome-51/04-atelier-gtk.md
  docs/gnome-51/05-libadwaita.md
  docs/gnome-51/06-icones-curseurs-polices-fonds.md
  docs/gnome-51/07-parametres-installation-diagnostic.md
  docs/gnome-51/08-catalogue-pratique-composants.md
  docs/gnome-51/11-applications-gnome.md
  docs/gnome-51/12-inspection-et-diagnostic-css.md
  docs/gnome-51/13-panneau-superieur-shell.md
  docs/gnome-51/14-vue-activites-overview.md
  docs/gnome-51/15-menus-reglages-notifications.md
  docs/gnome-51/16-ecran-verrouillage-gdm.md
  docs/gnome-51/17-osd-dialogues-alt-tab-capture.md
  docs/gnome-51/18-clavier-ibus-accessibilite.md
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

for source in "${SOURCE_FILES[@]}"; do
  if [[ ! -f "$source" ]]; then
    echo "Fichier documentaire absent : $source" >&2
    exit 1
  fi
done

pandoc "${SOURCE_FILES[@]}" --resource-path=docs/gnome-51 --from=gfm --to=epub3 \
  --metadata title="Manuel complet de personnalisation GNOME 51" \
  --metadata lang=fr --metadata author="G-OS Theme Maker" \
  --toc --toc-depth=3 --output=docs/guide-theme-gnome.epub
pandoc "${SOURCE_FILES[@]}" --resource-path=docs/gnome-51 --from=gfm --to=html5 --standalone \
  --metadata title="Manuel complet de personnalisation GNOME 51" \
  --metadata lang=fr --css=docs/guide.css --toc --toc-depth=3 \
  --pdf-engine=weasyprint --output=docs/guide-theme-gnome.pdf
echo "Documentation générée : ${#SOURCE_FILES[@]} sources incluses."
