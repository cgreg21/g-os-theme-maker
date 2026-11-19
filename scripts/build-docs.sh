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
  docs/gnome-51/19-gtk3-theming-detaille.md
  docs/gnome-51/20-gtk4-theming-detaille.md
  docs/gnome-51/21-libadwaita-theming-detaille.md
  docs/gnome-51/22-ressources-icones-curseurs-polices-fonds-sons.md
  docs/gnome-51/23-composants-shell-specialises.md
  docs/gnome-51/24-mutter-fenetres-decorations-ecrans.md
  docs/gnome-51/25-creer-installer-publier-theme.md
  docs/gnome-51/26-comprendre-moteurs-css-gnome.md
  docs/gnome-51/27-construire-theme-shell-scss.md
  docs/gnome-51/28-tests-visuels-regression-maintenance.md
  docs/gnome-51/29-developper-extension-shell.md
  docs/gnome-51/30-css-applications-gresource.md
  docs/gnome-51/31-couleurs-profils-ecrans-rendu.md
  docs/gnome-51/32-themes-icones-freedesktop-detail.md
  docs/gnome-51/33-themes-curseurs-xcursor-detail.md
  docs/gnome-51/34-fontconfig-typographie-detail.md
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
  docs/gnome-51/37-flatpak-themes-sandbox.md
  docs/gnome-51/38-applications-qt-electron.md
  docs/gnome-51/39-thematisation-extensions-shell.md
  docs/gnome-51/40-glossaire-technique.md
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
HTML_OUTPUT="docs/gnome-51/.guide-theme-gnome.html"
pandoc "${SOURCE_FILES[@]}" --resource-path=docs/gnome-51 --from=gfm --to=html5 --standalone \
  --metadata title="Manuel complet de personnalisation GNOME 51" \
  --metadata lang=fr --css=../guide.css --toc --toc-depth=3 \
  --output="$HTML_OUTPUT"
weasyprint "$HTML_OUTPUT" docs/guide-theme-gnome.pdf
rm -f "$HTML_OUTPUT"
echo "Documentation générée : ${#SOURCE_FILES[@]} sources incluses."
