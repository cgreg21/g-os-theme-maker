# Libadwaita 1.10 : variables CSS, classes de style et apparences

Ce chapitre est une référence pratique de la feuille Adwaita fournie avec **Libadwaita 1.10**, la version ciblée par GNOME 51 dans ce manuel. Il complète le chapitre sur les composants Libadwaita en décrivant les couleurs sémantiques, les variables CSS, les classes de style, les préférences d'apparence et le chargement des feuilles applicatives.

Les noms et comportements sont vérifiés dans le tag officiel `1.10.0` de GNOME/libadwaita. Ils ne doivent pas être supposés identiques dans une version antérieure.

## 1. Le rôle de la feuille Adwaita

Libadwaita s'appuie sur GTK 4 et fournit une feuille de style Adwaita commune aux widgets GTK et aux composants Libadwaita.

Cette feuille définit notamment :

- les couleurs de surfaces et de textes ;
- les couleurs d'accent et d'actions sémantiques ;
- les styles des boutons et contrôles ;
- les classes de style publiques ;
- les règles clair, sombre et contraste élevé ;
- les valeurs typographiques ;
- les styles des composants spécialisés.

Une application peut ajouter ses propres règles. Elle ne doit pas considérer les détails SCSS internes de Libadwaita comme une API stable. Les variables et classes documentées sont le point de départ le plus sûr.

Un thème GTK global ne peut pas garantir que chaque application Libadwaita utilisera les mêmes styles personnalisés : les applications peuvent embarquer des feuilles de style, ajouter des classes privées ou dessiner des composants.

## 2. Les variables sémantiques

Les variables sémantiques décrivent le rôle d'une surface ou d'un texte. Elles permettent à la même règle de fonctionner en clair et en sombre.

Exemple :

```css
.my-card {
  background-color: var(--card-bg-color);
  color: var(--card-fg-color);
}
```

Ne remplacez pas systématiquement ces variables par des couleurs codées en dur. Si une application respecte la feuille Adwaita, les variables suivent le mode et les préférences du système.

### Accent

Les variables principales sont :

- `--accent-bg-color` : fond d'accent ;
- `--accent-fg-color` : premier plan sur le fond d'accent ;
- `--accent-color` : variante d'accent destinée à être utilisée comme couleur de premier plan sur une surface neutre.

Les couleurs d'accent nommées disponibles sont :

- `--accent-blue` ;
- `--accent-teal` ;
- `--accent-green` ;
- `--accent-yellow` ;
- `--accent-orange` ;
- `--accent-red` ;
- `--accent-pink` ;
- `--accent-purple` ;
- `--accent-slate`.

La couleur d'accent système peut varier selon la configuration de l'environnement. Utilisez les variables au lieu de supposer que le bleu est toujours l'accent choisi.

### Actions destructives et états

Les familles suivantes possèdent un fond, un premier plan et une couleur autonome :

- `--destructive-bg-color`, `--destructive-fg-color`, `--destructive-color` ;
- `--success-bg-color`, `--success-fg-color`, `--success-color` ;
- `--warning-bg-color`, `--warning-fg-color`, `--warning-color` ;
- `--error-bg-color`, `--error-fg-color`, `--error-color`.

Le fond et le premier plan doivent être utilisés ensemble. La couleur autonome est conçue pour conserver un contraste adapté lorsqu'elle est utilisée comme texte sur une surface neutre.

Exemple :

```css
.status-success {
  background-color: var(--success-bg-color);
  color: var(--success-fg-color);
}

.status-error-label {
  color: var(--error-color);
}
```

N'utilisez pas la couleur destructive pour une action ordinaire. Elle doit signaler une conséquence potentiellement dommageable.

### Fenêtre et vues

Les variables de fenêtre sont :

- `--window-bg-color` ;
- `--window-fg-color`.

Les variables de vue sont :

- `--view-bg-color` ;
- `--view-fg-color`.

La fenêtre est la surface générale de l'application. Une vue de contenu, telle qu'une zone de texte ou une liste, peut posséder un fond distinct.

### Barre d'en-tête

Les variables de barre d'en-tête sont :

- `--headerbar-bg-color` ;
- `--headerbar-fg-color` ;
- `--headerbar-border-color` ;
- `--headerbar-backdrop-color` ;
- `--headerbar-shade-color` ;
- `--headerbar-darker-shade-color`.

Elles servent à adapter la barre d'en-tête, ses états inactifs et ses ombres. Ne remplacez pas toutes ces valeurs par une même couleur si la hiérarchie visuelle doit distinguer une fenêtre active d'une fenêtre inactive.

### Panneaux latéraux

Le panneau latéral principal expose :

- `--sidebar-bg-color` ;
- `--sidebar-fg-color` ;
- `--sidebar-backdrop-color` ;
- `--sidebar-border-color` ;
- `--sidebar-shade-color`.

Le panneau latéral secondaire expose :

- `--secondary-sidebar-bg-color` ;
- `--secondary-sidebar-fg-color` ;
- `--secondary-sidebar-backdrop-color` ;
- `--secondary-sidebar-border-color` ;
- `--secondary-sidebar-shade-color`.

Ces groupes distinguent la navigation principale d'un panneau secondaire. Les deux surfaces peuvent être imbriquées ou adjacentes selon le composant.

### Cartes, dialogues et popovers

Les cartes et listes encadrées utilisent :

- `--card-bg-color` ;
- `--card-fg-color` ;
- `--card-shade-color`.

Les dialogues utilisent :

- `--dialog-bg-color` ;
- `--dialog-fg-color`.

Les popovers utilisent :

- `--popover-bg-color` ;
- `--popover-fg-color` ;
- `--popover-shade-color`.

Les miniatures utilisent :

- `--thumbnail-bg-color` ;
- `--thumbnail-fg-color`.

### Onglets, bascules et aperçu

Les variables complémentaires comprennent :

- `--active-toggle-bg-color` ;
- `--active-toggle-fg-color` ;
- `--overview-bg-color` ;
- `--overview-fg-color`.

Elles servent aux composants et vues qui utilisent ces rôles précis. N'appliquez pas ces variables à des widgets arbitraires sans vérifier le composant.

### Couleurs diverses

Les variables diverses documentées comprennent :

- `--shade-color` ;
- `--scrollbar-outline-color`.

Elles participent à des effets de surface et de défilement.

## 3. Variables typographiques

Libadwaita expose les polices du système à travers quatre variables :

- `--document-font-family` ;
- `--document-font-size` ;
- `--monospace-font-family` ;
- `--monospace-font-size`.

La police de document est destinée aux articles, messages et contenus de lecture. La police monospace est destinée au code, aux journaux et aux commandes.

Exemple :

```css
.article-content {
  font-family: var(--document-font-family);
  font-size: var(--document-font-size);
}

.terminal-output {
  font-family: var(--monospace-font-family);
  font-size: var(--monospace-font-size);
}
```

La classe `.document` utilise la typographie de document et la classe `.monospace` la typographie monospace. Préférez ces conventions aux tailles de police arbitraires.

## 4. Variables auxiliaires : ne pas les remplacer

Libadwaita fournit des variables auxiliaires pour que les composants personnalisés s'adaptent automatiquement au contraste élevé.

Elles sont conçues pour être utilisées, pas redéfinies par un thème.

### Opacités

- `--border-opacity` : opacité courante des bordures ;
- `--dim-opacity` : opacité des contenus atténués ;
- `--disabled-opacity` : opacité des widgets indisponibles.

Les valeurs changent avec le mode contraste élevé. Une règle qui fixe directement `opacity: 0.5` peut donc dégrader ce mode.

### Couleur de bordure

`--border-color` est calculée à partir de `currentColor` et de `--border-opacity`. Elle augmente automatiquement sa visibilité lorsque le contraste élevé est actif.

Exemple :

```css
.custom-separator {
  border-color: var(--border-color);
}
```

### Rayon de fenêtre

`--window-radius` correspond au rayon actuel de la fenêtre, y compris les changements liés à l'état flottant ou maximisé. Cette valeur peut servir à aligner un contour ou un anneau de focus près du bord de la fenêtre.

Ne remplacez pas cette variable par un rayon fixe lorsque le rendu doit suivre les changements de décoration.

## 5. Palette GNOME

La feuille Adwaita expose la palette GNOME sous forme de variables CSS. Chaque famille comprend cinq nuances numérotées.

Familles disponibles :

- bleu : `--blue-1` à `--blue-5` ;
- vert : `--green-1` à `--green-5` ;
- jaune : `--yellow-1` à `--yellow-5` ;
- orange : `--orange-1` à `--orange-5` ;
- rouge : `--red-1` à `--red-5` ;
- violet : `--purple-1` à `--purple-5` ;
- brun : `--brown-1` à `--brown-5` ;
- clair : `--light-1` à `--light-5` ;
- sombre : `--dark-1` à `--dark-5`.

Les nuances ne sont pas une échelle de luminosité universelle utilisable sans vérification. Choisissez une nuance en fonction du contraste, du fond et du rôle visuel.

Exemple :

```css
.brand-mark {
  color: var(--purple-3);
}

.brand-surface {
  background-color: var(--blue-1);
}
```

La palette est une ressource pratique. Pour une action, une alerte ou une surface standard, préférez d'abord la variable sémantique correspondante.

## 6. Classes de style documentées

Les classes de style Adwaita sont des conventions publiques, mais elles ne peuvent pas être appliquées à n'importe quel widget. Chaque classe doit être utilisée sur les types de composants indiqués dans la documentation.

### Boutons

- `.suggested-action` : action principale ou affirmative ;
- `.destructive-action` : action destructive ;
- `.flat` : bouton sans cadre permanent ;
- `.raised` : apparence de bouton relevé dans les contextes adaptés ;
- `.circular` : bouton rond, généralement avec icône ;
- `.pill` : bouton en forme de pilule.

Ces classes peuvent être combinées lorsque la documentation du composant l'autorise. Une classe visuelle ne doit pas changer la sémantique de l'action.

### Groupes de bascules et contrôles liés

- `.flat` et `.round` pour les groupes de bascules ;
- `.linked` pour réunir visuellement des contrôles adjacents ;
- `.toolbar` pour les barres d'outils et leurs règles d'apparence ;
- `.spacer` pour séparer des groupes de contrôles.

Un conteneur `.linked` doit respecter les contraintes de disposition prévues par Adwaita. Des enfants espacés ou des boutons portant certaines classes peuvent casser l'apparence groupée.

### Atténuation

- `.dimmed` : contenu visuellement atténué.

Utilisez la classe sémantique plutôt que de fixer directement l'opacité. La feuille Adwaita peut adapter le rendu au contraste élevé.

### Typographie

- `.title-1` ;
- `.title-2` ;
- `.title-3` ;
- `.title-4` ;
- `.heading` ;
- `.document` ;
- `.body` ;
- `.caption` ;
- `.caption-heading` ;
- `.monospace` ;
- `.numeric`.

Ces classes établissent une hiérarchie typographique cohérente. Elles sont particulièrement utiles pour les titres, descriptions, données numériques, commandes et contenus longs.

### Couleurs sémantiques

- `.accent` ;
- `.success` ;
- `.warning` ;
- `.error`.

Utilisez-les pour les textes ou widgets qui doivent adopter la couleur sémantique correspondante. Une couleur d'état doit toujours rester compréhensible sans dépendre uniquement de sa teinte.

### Listes encadrées et cartes

- `.boxed-list` ;
- `.boxed-list-separate` ;
- `.card` ;
- `.activatable`.

Ces classes servent à structurer des listes et surfaces. Une ligne activable doit conserver un retour visuel clair au survol, au focus et à l'activation.

### Panneaux latéraux et icônes

- `.navigation-sidebar` ;
- `.lowres-icon` ;
- `.icon-dropshadow`.

La classe de navigation latérale doit être appliquée au composant prévu. Les classes d'icônes concernent le rendu des icônes et ne transforment pas une image arbitraire en icône symbolique.

### Sélection, OSD et surfaces

- `.selection-mode` ;
- `.osd` ;
- `.background` ;
- `.view` ;
- `.frame` ;
- `.compact` ;
- `.menu` ;
- `.devel` ;
- `.inline` ;
- `.property`.

Ces classes correspondent à des contextes de composants précis. `.devel` est notamment associé aux présentations de développement. Ne l'utilisez pas pour un style général de production.

### Indicateurs de dépassement

- `.undershoot-top` ;
- `.undershoot-bottom` ;
- `.undershoot-start` ;
- `.undershoot-end`.

Ils représentent les indicateurs de défilement lorsque du contenu dépasse les limites visibles. Ils sont gérés par les widgets qui prennent en charge ces états.

### Classes historiques dépréciées

La documentation Libadwaita 1.10 identifie plusieurs classes historiques comme dépréciées et conservées pour compatibilité :

- `.content` : remplacez-la par `.boxed-list` sur une liste encadrée ;
- `.sidebar` : utilisez `.navigation-sidebar` sur la liste et un séparateur pour la bordure ;
- `.app-notification` : utilisez le composant `AdwToastOverlay` pour les notifications intégrées ;
- `.large-title` : utilisez `.title-1` ;
- `.opaque` ;
- `.dim-label`.

Ne les utilisez pas dans un nouveau code. Pour une application ancienne, vérifiez les composants qui portent ces classes avant de les remplacer : certaines migrations demandent de changer le widget ou la structure, pas seulement le nom de classe.

### Barre d'en-tête plate : dépréciation ciblée

La classe `.flat` n'est pas globalement dépréciée. Elle reste documentée pour les boutons et les groupes de bascules. En revanche, son utilisation sur `AdwHeaderBar` ou `GtkHeaderBar` pour obtenir une barre plate est dépréciée depuis Libadwaita 1.4.

Pour une nouvelle interface, utilisez `AdwToolbarView` et ses barres d'outils. Ne retirez donc pas automatiquement `.flat` des boutons existants : vérifiez le type de composant auquel la classe est appliquée.

## 7. Apparence claire et sombre

L'apparence est pilotée par `AdwStyleManager`. Les valeurs de schéma de couleurs sont :

- `ADW_COLOR_SCHEME_DEFAULT` ;
- `ADW_COLOR_SCHEME_PREFER_LIGHT` ;
- `ADW_COLOR_SCHEME_PREFER_DARK` ;
- `ADW_COLOR_SCHEME_FORCE_LIGHT` ;
- `ADW_COLOR_SCHEME_FORCE_DARK`.

Par défaut, Libadwaita préfère le clair tout en suivant la préférence sombre du système lorsque celle-ci est disponible.

Les modes préférés respectent la préférence système lorsqu'elle existe. Les modes forcés demandent une apparence constante. Le choix de l'application et celui du système doivent être distingués.

Pour un composant personnalisé, utilisez les variables de couleur plutôt que de vérifier manuellement toutes les valeurs de couleur. Pour un dessin programmatique, consultez l'état du StyleManager et les couleurs GTK correspondantes.

## 8. Couleur d'accent personnalisée

Libadwaita suit la couleur d'accent système par défaut. Une application peut la remplacer dans sa feuille CSS :

```css
:root {
  --accent-bg-color: var(--accent-green);
}
```

Si l'accent est remplacé localement sur un widget, redéfinissez également la couleur autonome :

```css
.custom-accent {
  --accent-bg-color: var(--accent-purple);
  --accent-color: oklab(
    from var(--accent-bg-color) var(--standalone-color-oklab)
  );
}
```

Si la couleur d'accent de fond est très claire, choisissez aussi un premier plan sombre :

```css
:root {
  --accent-bg-color: var(--yellow-3);
  --accent-fg-color: rgb(0 0 0 / 80%);
}
```

L'API `AdwStyleManager` continue de retourner la couleur système même si la feuille CSS redéfinit visuellement les variables. Ne confondez donc pas l'accent système exposé par l'API et une surcharge CSS locale.

## 9. Contraste élevé

Le contraste élevé est une préférence indépendante du mode sombre. Les deux peuvent être combinés.

Les widgets GTK et Libadwaita standards adaptent automatiquement leur apparence. Les composants personnalisés qui dessinent directement leur contenu ou qui codent des couleurs arbitraires doivent prévoir leurs variantes.

Bonnes pratiques :

1. Utilisez les variables auxiliaires `--border-color`, `--dim-opacity` et `--disabled-opacity`.
2. Utilisez `.dimmed` au lieu de réduire arbitrairement l'opacité.
3. Conservez des contours de focus visibles.
4. Vérifiez le contraste des textes secondaires et des séparateurs.
5. N'utilisez pas la couleur seule pour différencier les états.
6. Testez le contraste élevé en clair et en sombre.

Les règles personnalisées peuvent utiliser :

```css
@media (prefers-contrast: more) {
  .custom-card {
    border: 2px solid var(--border-color);
  }
}
```

Ne dupliquez pas toute la feuille en mode contraste élevé si seules quelques propriétés doivent changer.

## 10. Feuille CSS applicative et ressources

`AdwApplication` peut charger automatiquement une ressource nommée `style.css`, située sous le chemin de ressources de l'application.

Pour une nouvelle application Libadwaita, placez les règles personnalisées dans une feuille unique `style.css` et utilisez les requêtes de média pour les variantes.

Exemple :

```css
.custom-surface {
  background-color: var(--card-bg-color);
  color: var(--card-fg-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

@media (prefers-color-scheme: dark) {
  .custom-surface {
    box-shadow: 0 2px 8px rgb(0 0 0 / 25%);
  }
}

@media (prefers-contrast: more) {
  .custom-surface {
    border-width: 2px;
  }
}
```

Libadwaita 1.10 prend toujours en charge les ressources conditionnelles `style-dark.css`, `style-hc.css` et `style-hc-dark.css` via `AdwApplication`. Pour une nouvelle application, préférez une feuille `style.css` unique et les requêtes `prefers-color-scheme` et `prefers-contrast`. Les ressources séparées restent valides pour les applications qui en ont besoin ; elles ne doivent pas être présentées comme dépréciées.

Le chargement de `style.css` est lié au chemin de ressources défini par l'application. Une feuille placée dans un dossier arbitraire sur le disque ne sera pas automatiquement chargée par toutes les applications Libadwaita.

## 11. Variables de compatibilité GTK 3

La feuille Libadwaita fournit encore des couleurs nommées historiques pour la compatibilité avec des thèmes GTK 3 :

- `@theme_bg_color` ;
- `@theme_fg_color` ;
- `@theme_base_color` ;
- `@theme_text_color` ;
- `@theme_selected_bg_color` ;
- `@theme_selected_fg_color` ;
- `@insensitive_bg_color` ;
- `@insensitive_fg_color` ;
- `@insensitive_base_color` ;
- `@borders` ;
- les variantes `@theme_unfocused_*` ;
- `@unfocused_insensitive_color` ;
- `@unfocused_borders`.

Ces noms utilisent l'ancienne syntaxe GTK et sont des alias de couleurs d'interface ou des valeurs dérivées. Ils ne récupèrent pas nécessairement les surcharges des nouvelles variables CSS. La documentation recommande de ne pas les utiliser dans les nouveaux styles.

Dans une feuille Libadwaita, préférez `var(--window-bg-color)`, `var(--view-bg-color)`, `var(--accent-bg-color)` et les autres variables sémantiques.

## 12. Exemple complet de thème applicatif

```css
:root {
  --accent-bg-color: var(--accent-purple);
}

.brand-card {
  background-color: var(--card-bg-color);
  color: var(--card-fg-color);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 12px;
}

.brand-card-title {
  font-family: var(--document-font-family);
  font-size: var(--document-font-size);
  font-weight: 700;
}

.brand-card-code {
  font-family: var(--monospace-font-family);
  font-size: var(--monospace-font-size);
}

.brand-card .status-success {
  color: var(--success-color);
}

.brand-card .status-warning {
  color: var(--warning-color);
}

.brand-card .status-error {
  color: var(--error-color);
}

@media (prefers-color-scheme: dark) {
  .brand-card {
    box-shadow: 0 4px 16px rgb(0 0 0 / 22%);
  }
}

@media (prefers-contrast: more) {
  .brand-card {
    border-width: 2px;
  }
}
```

Les classes `.brand-card`, `.brand-card-title` et `.brand-card-code` sont des classes privées de l'application dans cet exemple. Les variables Adwaita sont publiques et fournissent les valeurs adaptées au contexte.

## 13. Méthode de diagnostic

Si une règle ne fonctionne pas :

1. Vérifiez la version Libadwaita réellement chargée par l'application.
2. Vérifiez si l'application utilise le runtime système ou un runtime Flatpak.
3. Inspectez le nœud CSS avec GTK Inspector.
4. Vérifiez les classes du nœud et celles de ses parents.
5. Vérifiez que la feuille `style.css` est embarquée dans les ressources de l'application.
6. Vérifiez que le chemin de ressources de l'application est défini.
7. Vérifiez la variable CSS dans le contexte du nœud.
8. Vérifiez le mode clair/sombre et le contraste élevé.
9. Testez le composant en fenêtre étroite et large.
10. Désactivez temporairement les styles privés de l'application pour isoler la règle.

Pour identifier les versions de développement disponibles :

```bash
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
```

Pour une application Flatpak, vérifiez aussi le runtime indiqué par `flatpak info`. La version installée sur l'hôte ne prouve pas la version chargée dans le bac à sable.

## 14. Sources officielles Libadwaita 1.10.0

- [CSS Variables](https://github.com/GNOME/libadwaita/blob/1.10.0/doc/css-variables.md)
- [Style Classes](https://github.com/GNOME/libadwaita/blob/1.10.0/doc/style-classes.md)
- [Styles & Appearance](https://github.com/GNOME/libadwaita/blob/1.10.0/doc/styles-and-appearance.md)
- [AdwApplication — chargement des ressources](https://github.com/GNOME/libadwaita/blob/1.10.0/src/adw-application.c)
- [AdwStyleManager](https://github.com/GNOME/libadwaita/blob/1.10.0/src/adw-style-manager.h)
- [Feuille Adwaita — couleurs](https://github.com/GNOME/libadwaita/blob/1.10.0/src/stylesheet/_colors.scss)
- [Palette GNOME](https://github.com/GNOME/libadwaita/blob/1.10.0/src/stylesheet/_palette.scss)

Les sources sont épinglées sur Libadwaita 1.10.0. Les classes privées des widgets et les détails SCSS internes peuvent évoluer : utilisez les références documentées et inspectez toujours l'application réelle.
