# 6. Icônes, curseurs, polices, fonds et sons

## 6.1 Contextes d'icônes

Prévoir Applications, Actions, Devices, Places, Status, MimeTypes, Emblems, Categories et éventuellement Panel. Respecter noms Freedesktop, contextes, tailles, types et héritages. Déclarer `hicolor` comme repli. Contrôler icônes manquantes et licences.

## 6.2 Icônes symboliques

Les icônes symboliques sont monochromes et recolorables. Utiliser une grille, une épaisseur de trait constante, des marges optiques et des tracés propres. Ne pas coder de couleur si la recoloration est attendue. Vérifier les variantes RTL.

## 6.3 Curseurs GNOME 51

GNOME 51 introduit le rendu de curseurs à partir de ressources SVG scalables. Cela ne rend pas automatiquement tout thème Xcursor ancien compatible SVG. Respecter rôles, noms, hotspots, tailles et replis. Tester pointeur, aide, main, texte, attente, déplacement, copie, interdiction, redimensionnement et précision.

## 6.4 Polices

Séparer police d'interface, document, monospace, famille, taille, graisse, facteur d'échelle, antialiasing, hinting et fallback Unicode. Installer une police ne signifie pas qu'elle est activée. Respecter licences et couverture des glyphes.

## 6.5 Fonds et verrouillage

Les fonds sont des ressources GNOME choisies par les paramètres, pas des widgets CSS. Prévoir images clair/sombre, formats, ratios, recadrage, multi-écrans, résolution, crédits et licences. Fond bureau, verrouillage et GDM peuvent utiliser des mécanismes distincts.

## 6.6 Sons et autres ressources

Les sons utilisent des thèmes sonores Freedesktop et des préférences système. Les icônes de bureau dépendent d'une extension ou du gestionnaire de fichiers. Les ressources doivent être optionnelles et réellement fournies.

## 6.7 Structure type

```text
Theme/
├── gnome-shell/gnome-shell.css
├── gtk-3.0/gtk.css
├── gtk-4.0/gtk.css
├── icons/Theme/index.theme
├── cursors/Cursor/index.theme
├── cursors/Cursor/cursors/
├── backgrounds/
├── sounds/Theme/index.theme
├── fonts/
└── README.md
```
