# G-OS Theme Maker

A visual GTK4 application for creating GNOME Shell themes without writing CSS by hand.

## Goals

- Visual theme editor for colors, typography, spacing, borders, radii and component states.
- Live GTK preview and an isolated nested GNOME Shell preview backend.
- Property inspector for selecting preview components and editing their theme tokens.
- Theme presets, light/dark variants, JSON project files and GNOME Shell CSS export.
- No changes to the user's active desktop theme during editing.

## Current status

The project is being bootstrapped. The first milestone provides the GTK application shell, editable design tokens, a component preview, project serialization and CSS export. The nested Mutter/GNOME Shell runtime is an explicit integration target; the local GTK preview is not presented as a real Mutter session.

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

Projects are JSON documents with a versioned schema. Exported CSS is intended for GNOME Shell theme development and should be validated against the target GNOME Shell version before installation.
