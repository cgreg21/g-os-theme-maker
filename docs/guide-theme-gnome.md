# Créer un thème GNOME complet

Ce guide décrit les fichiers et les règles utiles pour créer un thème cohérent avec G-OS Theme Maker. Il prend GNOME Shell 51 comme référence et distingue GTK 3, GTK 4 et Libadwaita.

## 1. Comprendre les couches du bureau

Un thème GNOME complet est un ensemble de thèmes séparés. Chaque composant charge ses propres fichiers.

| Couche | Rôle | Dossier exporté |
|---|---|---|
| GNOME Shell | Barre supérieure, vue Activités, dash, menus système, notifications | `gnome-shell/` |
| GTK 3 | Applications encore basées sur GTK 3 | `gtk-3.0/` |
| GTK 4 | Widgets GTK 4 standards | `gtk-4.0/` |
| Libadwaita | Apparence des applications utilisant Libadwaita | `libadwaita/` |
| Icônes | Icônes d'applications, actions et fichiers | `icons/` |
| Curseurs | Pointeurs de souris | `cursors/` |

**Important :** ces couches ne partagent pas un moteur de thème unique. Modifier le CSS de GNOME Shell ne modifie pas les boutons d'une application GTK.

Exemple : la couleur de la barre supérieure est définie dans le CSS Shell. La couleur d'un bouton d'application GTK est définie dans le CSS GTK.

## 2. GNOME Shell 51

GNOME Shell utilise Clutter et le toolkit St. Les éléments de l'interface sont des acteurs St, pas des widgets GTK. Le thème est chargé depuis une feuille de style Shell.

Le thème installé par défaut est construit à partir des sources du dépôt GNOME Shell. La version 51 fournit notamment des feuilles clair, sombre et contraste élevé. Les noms de classes peuvent évoluer entre les versions : il faut donc vérifier les sélecteurs dans la version ciblée. Les sources de thème sont organisées en SCSS puis compilées en CSS pendant la construction ; le CSS livré est le résultat généré, pas le fichier de travail à modifier dans le dépôt GNOME Shell.

### 2.1 Barre supérieure

Sélecteur principal : `#panel`. Les boutons de la barre utilisent notamment `.panel-button`.

```css
#panel {
  background-color: #242424;
  color: #ffffff;
}

#panel .panel-button:hover {
  background-color: #3584e4;
}
```

### 2.2 Vue Activités et dock

Le dash est ciblé par `#dash`. Les éléments du lanceur et leurs états possèdent leurs propres classes.

```css
#dash {
  background-color: #303030;
  border-radius: 16px;
  padding: 8px;
}
```

### 2.3 Menus et réglages rapides

Les menus système utilisent les classes de menus Shell. Les réglages rapides et leurs boutons ont aussi des classes dédiées. Ne pas supposer qu'un sélecteur de menu couvre tous les sous-composants.

```css
.popup-menu-content {
  background-color: #303030;
  color: #ffffff;
  border: 1px solid #454545;
  border-radius: 12px;
}
```

### 2.4 Notifications et dialogues

Les notifications, les dialogues modaux, les fenêtres de saisie et les confirmations de session ont des sélecteurs spécifiques.

```css
.modal-dialog {
  background-color: #303030;
  color: #ffffff;
  border-radius: 12px;
}
```

### 2.5 États interactifs

Les pseudo-classes `:hover`, `:focus`, `:active` et `:checked` permettent de différencier les états.

```css
.button:hover,
.button:focus {
  background-color: #3584e4;
}
```

### 2.6 Clair, sombre et contraste élevé

GNOME Shell 51 fournit des variantes de style clair, sombre et contraste élevé. Un thème complet doit définir une palette lisible pour ces modes. Ne pas simplement inverser toutes les couleurs : vérifier les contrastes, les icônes et les états.

### 2.7 Règle de compatibilité

Ne jamais considérer les sélecteurs comme une API stable entre toutes les versions de Shell. Pour chaque version ciblée :
1. relever les sélecteurs dans le CSS livré avec cette version ;
2. tester le thème dans une session Shell imbriquée ;
3. vérifier barre supérieure, dash, vue Activités, menus, réglages rapides, notifications et dialogues.

## 3. GTK 3

GTK 3 utilise un arbre de nœuds CSS. Les sélecteurs ciblent les noms de nœuds, les classes et les états des widgets.

Le fichier principal d'un thème est `gtk-3.0/gtk.css`. Les couleurs nommées utilisent `@define-color`.

### 3.1 Couleurs et fenêtres

```css
@define-color theme_bg_color #242424;
@define-color theme_fg_color #ffffff;
@define-color theme_selected_bg_color #3584e4;
@define-color theme_selected_fg_color #ffffff;

window {
  background-color: @theme_bg_color;
  color: @theme_fg_color;
}
```

### 3.2 Boutons, champs et menus

```css
button {
  background-color: #303030;
  color: #ffffff;
  border: 1px solid #454545;
  border-radius: 8px;
  padding: 6px 10px;
}

entry {
  background-color: #202020;
  color: #ffffff;
  border: 1px solid #454545;
  border-radius: 6px;
}

popover, menu {
  background-color: #303030;
  color: #ffffff;
}
```

### 3.3 États

```css
button:hover { background-color: #3b3b3b; }
button:active { background-color: #3584e4; }
button:disabled { opacity: 0.5; }
entry:focus { border-color: #3584e4; }
```

Les nœuds CSS réels dépendent du widget. Consulter la documentation GTK du widget avant d'écrire un sélecteur complexe.

## 4. GTK 4

GTK 4 conserve le principe des nœuds CSS, mais son arbre de widgets et certaines propriétés diffèrent de GTK 3. Un thème GTK 3 ne doit pas être copié tel quel dans le dossier GTK 4.

Le point d'entrée du thème est `gtk-4.0/gtk.css`. GTK recherche un fichier correspondant à la version et à la variante, puis peut revenir à une feuille de style de version antérieure.

### 4.1 CSS compatible GTK 4

Pour une feuille de style qui vise aussi les versions GTK 4 anciennes, préférer les propriétés simples et les couleurs nommées.

```css
@define-color theme_bg_color #242424;
@define-color theme_fg_color #ffffff;
@define-color theme_selected_bg_color #3584e4;

window {
  background-color: @theme_bg_color;
  color: @theme_fg_color;
}

button {
  background-color: #303030;
  color: #ffffff;
  border-radius: 8px;
  padding: 6px 10px;
}
```

### 4.2 Propriétés personnalisées depuis GTK 4.16

GTK 4.16 prend en charge les propriétés CSS personnalisées et `var()`. Elles permettent de partager une palette sans répéter les valeurs.

```css
:root {
  --theme-bg: #242424;
  --theme-fg: #ffffff;
  --theme-accent: #3584e4;
}

window {
  background-color: var(--theme-bg);
  color: var(--theme-fg);
}
```

Ne pas placer cette syntaxe dans une feuille destinée à GTK 4.0 à 4.15. Le paquet généré fournit donc une feuille GTK 4 compatible et un fichier moderne séparé à importer si la version le permet.

## 5. Libadwaita

Libadwaita définit l'apparence des applications GNOME modernes. Elle gère notamment le mode clair/sombre, les couleurs d'accent et le contraste élevé.

Un thème GTK classique ne garantit pas la recoloration des applications Libadwaita. Libadwaita n'expose pas une API officielle permettant de remplacer globalement son thème complet. Les feuilles utilisateur sont une personnalisation avancée, qui peut être limitée par l'application.

### 5.1 Variables de couleurs

Depuis GTK 4.16, les variables CSS peuvent être utilisées pour adapter les couleurs de l'interface.

```css
:root {
  --window-bg-color: #242424;
  --window-fg-color: #ffffff;
  --view-bg-color: #202020;
  --view-fg-color: #ffffff;
  --headerbar-bg-color: #303030;
  --headerbar-fg-color: #ffffff;
  --card-bg-color: #303030;
  --card-fg-color: #ffffff;
  --accent-bg-color: #3584e4;
  --accent-fg-color: #ffffff;
}
```

### 5.2 États et accessibilité

Utiliser les classes et variables prévues par Libadwaita. Les styles personnalisés doivent conserver un contraste suffisant en clair, sombre et contraste élevé.

Exemple de couleur d'accent :

```css
:root {
  --accent-bg-color: #3584e4;
  --accent-fg-color: #ffffff;
}
```

Le fichier utilisateur se place dans `~/.config/gtk-4.0/gtk.css` ou est importé depuis ce fichier. Il faut relancer l'application pour vérifier le résultat.

## 6. Icônes

Un thème d'icônes suit la spécification Freedesktop. Il contient un fichier `index.theme` et des répertoires classés par taille et catégorie.

Exemple minimal :

```ini
[Icon Theme]
Name=MonTheme
Comment=Mon thème d'icônes
Inherits=hicolor
Directories=scalable/apps,scalable/actions

[scalable/apps]
Size=48
Type=Scalable
MinSize=16
MaxSize=256
Context=Applications

[scalable/actions]
Size=16
Type=Scalable
MinSize=16
MaxSize=64
Context=Actions
```

Exemple de fichiers : `scalable/apps/org.gnome.Settings.svg` et `scalable/actions/edit-copy-symbolic.svg`.

Préférer SVG pour les icônes vectorielles et respecter les noms d'icônes standards pour permettre les replis vers `hicolor`.

## 7. Curseurs

Un thème de curseurs est un thème séparé, généralement installé dans `icons/NomDuTheme/cursors/` avec son fichier `index.theme`. Les fichiers de curseurs sont des ressources Xcursor, pas des icônes SVG ordinaires.

Exemple de déclaration :

```ini
[Icon Theme]
Name=MonCurseur
Comment=Curseurs personnalisés
Inherits=Adwaita
```

Le thème doit fournir les noms de curseurs attendus, par exemple `left_ptr`, `hand2` et `text`. En l'absence d'un curseur, le thème parent sert de repli.

## 8. Organisation d'un paquet complet

Structure conseillée :

```text
MonTheme/
├── README.md
├── gnome-shell/
│   └── gnome-shell.css
├── gtk-3.0/
│   └── gtk.css
├── gtk-4.0/
│   └── gtk.css
├── libadwaita/
│   └── gtk-4.16.css
├── icons/
│   └── MonTheme/
│       ├── index.theme
│       └── scalable/
└── cursors/
    └── MonCurseur/
        ├── index.theme
        └── cursors/
```

Les dossiers icônes et curseurs sont des emplacements réservés tant que leurs ressources ne sont pas créées. Un export ne doit pas annoncer qu'ils sont complets s'ils ne contiennent pas les fichiers nécessaires.

## 9. Compatibilité et tests

| Cible | Feuille | Points à vérifier |
|---|---|---|
| GNOME Shell 51 | `gnome-shell/gnome-shell.css` | Barre, dash, menus, réglages rapides, notifications, dialogues |
| GTK 3.24 | `gtk-3.0/gtk.css` | Fenêtres, boutons, entrées, listes, menus |
| GTK 4.0 à 4.15 | `gtk-4.0/gtk.css` | Widgets GTK 4 sans variables CSS modernes |
| GTK 4.16 et plus | `libadwaita/gtk-4.16.css` | Variables modernes et styles Libadwaita |
| Icônes | `index.theme` | Tailles, noms, héritage et icônes manquantes |
| Curseurs | `index.theme` et ressources Xcursor | Pointeur, texte, liens, redimensionnement |

Toujours tester dans des applications réelles et dans une session GNOME Shell imbriquée. L'aperçu du Theme Maker ne remplace pas les tests sur chaque version GTK.

## 10. Règles de conception du Theme Maker

1. Conserver une palette commune : fond, surface, texte, texte secondaire, accent et bordure.
2. Générer une feuille distincte pour chaque moteur.
3. Afficher les versions cibles et les limites de compatibilité.
4. Ne jamais appliquer une syntaxe moderne à une cible ancienne.
5. Ne pas promettre une personnalisation Libadwaita universelle.
6. Tester les états normal, survol, actif, focus et désactivé.
7. Vérifier le contraste et les variantes clair, sombre et contraste élevé.
8. Garder les sélecteurs Shell spécifiques à la version et les vérifier dans les sources GNOME.

## Sources officielles et références

- [GNOME Shell 51 – sources du thème](https://sources.debian.org/src/gnome-shell/51.0-2/data/theme/)
- [GTK 3 – CSS Overview](https://gnome.pages.gitlab.gnome.org/gtk/gtk3/css-overview.html)
- [GTK 4 – CSS Overview](https://gnome.pages.gitlab.gnome.org/gtk/gtk4/css-overview.html)
- [GTK 4 – CSS Properties](https://gnome.pages.gitlab.gnome.org/gtk/gtk4/css-properties.html)
- [GTK 4 – CssProvider et chargement des thèmes](https://docs.gtk.org/gtk4/class.CssProvider.html)
- [Libadwaita – Styles and Appearance](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)
- [Libadwaita – CSS Variables](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/css-variables.html)
- [Freedesktop – Icon Theme Specification](https://specifications.freedesktop.org/icon-theme/)
- [GNOME HIG – UI Styling](https://developer.gnome.org/hig/guidelines/ui-styling.html)
