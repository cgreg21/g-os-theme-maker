# G-OS Theme Maker

A visual GTK4 application for creating GNOME Shell themes without writing CSS by hand.

## Goals

- Visual theme editor for colors, typography, spacing, borders, radii and component states.
- Live GTK preview and an isolated nested GNOME Shell preview that loads the current generated stylesheet.
- Property inspector for selecting preview components and editing their theme tokens.
- JSON project files, generic CSS export, GNOME Shell export and complete Shell/GTK 3/GTK 4/Libadwaita theme package export.
- No changes to the user's active desktop theme during editing.

## Current status

The project is being bootstrapped. The first milestone provides the GTK application shell, editable design tokens, a component preview, project serialization and CSS export. The nested preview starts GNOME Shell through a private D-Bus session, a temporary XDG data/config directory and a temporary dconf profile. A small temporary extension loads the generated stylesheet without changing the active desktop settings. The temporary extension watches its stylesheet directory and reloads the theme automatically whenever the editor changes CSS. The local GTK preview remains separate from the real Shell preview.

## Requirements

- Python 3.11+
- GTK 4
- PyGObject
- PyGObject GTK4 typelib

On Debian/Ubuntu:

```sh
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0
python3 -m g_os_theme_maker
```

## Development

```sh
python3 -m unittest discover -s tests -v
python3 -m g_os_theme_maker
```

## Project format

Projects are JSON documents with a versioned schema. The GNOME Shell export creates a theme directory containing `gnome-shell/gnome-shell.css` and a short installation note. Copy the generated theme directory to `~/.themes/`, then select it with GNOME Tweaks or the User Themes extension. CSS selectors can vary by GNOME Shell release; review the theme in a nested session before using it on your desktop. The generic CSS export remains available separately.

## Documentation

Le guide français décrit GNOME Shell 51, GTK 3.24, GTK 4, Libadwaita, les icônes, les curseurs et les limites de compatibilité. Formats disponibles : [Markdown](docs/guide-theme-gnome.md), [EPUB](docs/guide-theme-gnome.epub) et [PDF](docs/guide-theme-gnome.pdf). Les deux formats téléchargeables sont régénérés automatiquement à chaque modification du guide. Pour les construire localement : `bash scripts/build-docs.sh` (Pandoc et WeasyPrint requis).
