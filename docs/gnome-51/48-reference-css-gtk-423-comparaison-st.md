# GTK 4.23 : propriétés CSS, unités et différences avec St

Ce chapitre décrit le périmètre CSS documenté par **GTK 4.23**, la génération utilisée par la plateforme GNOME 51. Il complète les ateliers GTK 4 et les chapitres sur les variables et requêtes de média.

Il sert aussi de guide de portage entre une feuille GNOME Shell (St) et une feuille GTK. Les deux moteurs utilisent des concepts CSS communs, mais ils n'interprètent pas les mêmes propriétés et ne ciblent pas le même arbre.

La référence de propriétés est basée sur le fichier officiel `docs/reference/gtk/css-properties.md` du tag GTK `4.23.1`, et la référence des sélecteurs sur `docs/reference/gtk/css-overview.md` du même tag.

## 1. GTK CSS n'est pas le CSS d'un navigateur

GTK applique les feuilles de style à un arbre de nœuds CSS construit par les widgets. Un widget peut exposer plusieurs nœuds : un curseur de valeur, par exemple, contient une piste, une poignée et éventuellement des marques.

Le CSS agit donc sur les éléments exposés par le widget et non directement sur les classes C ou les noms d'objets supposés.

Dans une feuille GTK :

- le nom du nœud est écrit comme un type de sélecteur, par exemple `button` ;
- une classe de style commence par un point, par exemple `.suggested-action` ;
- un nom de widget utilisé comme identifiant est précédé de `#` ;
- les pseudo-classes représentent les états GTK ;
- les relations parent/enfant et frères ciblent l'arbre CSS.

Exemple :

```css
button.suggested-action {
  border-radius: 10px;
}

headerbar button:hover {
  background-color: alpha(currentColor, 0.10);
}

entry:focus {
  border-color: @accent_color;
}
```

Le nom du widget API `GtkButton` n'est pas le sélecteur habituel : le nœud CSS correspondant est généralement `button`.

## 2. Sélecteurs GTK 4.23

La documentation GTK 4.23 répertorie les familles de sélecteurs suivantes :

- sélecteur universel `*` ;
- nom de nœud `E` ;
- classe `E.class` ;
- identifiant `E#id` ;
- enfants structurels `:nth-child()`, `:nth-last-child()`, `:first-child`, `:last-child`, `:only-child` ;
- états `:link`, `:visited`, `:active`, `:hover`, `:focus`, `:disabled`, `:checked`, `:indeterminate`, `:backdrop`, `:selected` ;
- focus étendu `:focus-within` et `:focus-visible` ;
- direction `:dir(ltr)` et `:dir(rtl)` ;
- glisser-déposer `:drop(active)` ;
- négation `:not()` ;
- racine `:root` ;
- combinateurs descendant, enfant direct, frère général et frère adjacent.

GTK attribue un sens propre à certains états. Par exemple, `:focus-within` et `:focus-visible` sont appliqués au widget ayant le focus et à ses ancêtres selon les règles GTK ; leur portée n'est pas strictement identique à celle d'un navigateur.

Ne supposez pas la prise en charge des sélecteurs d'attributs HTML. GTK cible les nœuds et les classes de style qu'exposent ses widgets.

## 3. Types de valeurs et unités

GTK 4.23 documente les types de valeurs suivants.

### Longueurs

- `px` ;
- `pt` ;
- `em` ;
- `ex` ;
- `rem` ;
- `pc` ;
- `in` ;
- `cm` ;
- `mm`.

Les unités physiques sont converties en pixels avec la résolution configurée dans GTK, notamment via `-gtk-dpi`. Cette conversion ne suit pas exactement la convention fixe de 96 DPI des navigateurs.

`em` et `ex` sont résolus selon la taille de police applicable. Pour `font-size`, la référence est la taille héritée. `rem` se réfère à la taille initiale GTK, ce qui n'est pas strictement identique à la définition Web.

### Pourcentages, angles et durées

GTK 4.23 prend également en charge :

- les pourcentages `%` ;
- les angles `deg`, `rad`, `grad`, `turn` ;
- les durées `s` et `ms`.

Les pourcentages ne sont pas universellement applicables : chaque propriété définit son propre type de valeur et son contexte de calcul.

### Calculs

`calc()` peut être utilisé avec les types compatibles. Toutes les opérations ne sont pas valides : une longueur et une durée ne peuvent pas être additionnées comme si elles étaient de même nature.

Exemple :

```css
.example {
  padding: calc(8px + 0.5em);
  min-width: calc(12rem - 16px);
  transition-duration: calc(100ms + 50ms);
}
```

N'appliquez pas ces exemples à St. Le moteur St 51 ne dispose pas du même système de types et ne prend pas en charge `calc()` comme GTK 4.23.

## 4. Propriétés personnalisées et variables

GTK prend en charge les propriétés CSS personnalisées depuis GTK 4.16. Elles sont disponibles dans GTK 4.23.

```css
:root {
  --gostm-surface: #242424;
  --gostm-text: #f6f5f4;
  --gostm-accent: #3584e4;
  --gostm-radius: 12px;
}

window {
  background-color: var(--gostm-surface);
  color: var(--gostm-text);
}

button.suggested-action {
  background-color: var(--gostm-accent);
  border-radius: var(--gostm-radius);
}
```

Une valeur de repli peut être fournie :

```css
button {
  color: var(--gostm-text, white);
}
```

Les variables suivent la cascade et l'héritage CSS. Une variable définie sur un conteneur peut donc fournir une variante locale à ses descendants.

Pour un thème GTK moderne, préférez les variables personnalisées aux anciennes règles `@define-color` lorsque la version minimale ciblée est GTK 4.16 ou plus récente.

**Attention :** les propriétés personnalisées et `var()` ne sont pas une fonctionnalité du moteur St 51. Elles ne doivent pas être placées dans une feuille de thème GNOME Shell en supposant qu'elles seront évaluées.

## 5. Couleurs modernes

GTK 4.23 accepte plusieurs syntaxes de couleur CSS modernes, notamment :

- `rgb()` et `rgba()` ;
- `hsl()` ;
- `hwb()` ;
- `oklab()` et `oklch()` ;
- `color()` ;
- `color-mix()` ;
- les couleurs relatives ;
- `calc()` dans les expressions de couleur.

Exemple :

```css
:root {
  --gostm-accent: oklch(62% 0.19 255);
  --gostm-accent-hover: color-mix(in oklab, var(--gostm-accent), white 14%);
}

button.suggested-action {
  background-color: var(--gostm-accent);
}

button.suggested-action:hover {
  background-color: var(--gostm-accent-hover);
}
```

Les anciennes expressions GTK `lighter()`, `darker()`, `shade()`, `alpha()` et `mix()` sont encore documentées, mais sont considérées comme historiques au profit des mécanismes CSS standard modernes.

La fonction `st-mix()` du Shell n'est pas la fonction `mix()` de GTK. Les noms et les règles d'arguments sont spécifiques au moteur.

## 6. Couleurs nommées historiques

GTK accepte encore les couleurs définies avec `@define-color` :

```css
@define-color legacy_accent #3584e4;

button {
  background-color: @legacy_accent;
}
```

Cette syntaxe reste utile dans les feuilles anciennes et dans les versions GTK 3. Pour une feuille GTK 4.23 nouvelle, privilégiez :

- les propriétés personnalisées CSS ;
- `:root` ;
- `var()`.

Les couleurs nommées historiques et les propriétés personnalisées ne sont pas interchangeables dans toutes les versions. Si GTK 3.24 est une cible, gardez une feuille distincte ou une stratégie de compatibilité testée.

## 7. Images et icônes GTK

GTK étend la syntaxe CSS des images pour les icônes de thème et le recoloriage.

### Icône de thème

`-gtk-icontheme(nom)` recherche une icône dans le thème d'icônes GTK.

### Recoloriage

`-gtk-recolor(uri, palette)` applique une palette à une image. La palette peut nommer les couleurs `success`, `warning` et `error`.

Exemple de palette :

```css
.example {
  -gtk-icon-palette: success #2ec27e, warning #f6d32d, error #e01b24;
}
```

### Ressources haute densité

`-gtk-scaled(image1, image2)` permet de fournir une ressource normale et une ressource haute résolution.

### Propriétés d'icône GTK

GTK 4.23 documente notamment :

- `-gtk-icon-source` ;
- `-gtk-icon-size` ;
- `-gtk-icon-style` ;
- `-gtk-icon-transform` ;
- `-gtk-icon-palette` ;
- `-gtk-icon-shadow` ;
- `-gtk-icon-filter` ;
- `-gtk-icon-weight`.

Ces propriétés concernent les icônes intégrées ou chargées par les widgets. Elles ne garantissent pas le recoloriage d'une image arbitraire dessinée par l'application.

Les propriétés `-gtk-*` sont propres à GTK. Ne les recopiez pas dans St : ce moteur utilise ses propres propriétés, par exemple `-st-icon-style`.

## 8. Typographie GTK

GTK 4.23 prend en charge un ensemble typographique plus large que le sous-ensemble interprété par St 51.

Les propriétés documentées comprennent :

- `font-family` ;
- `font-size` ;
- `font-style` ;
- `font-variant` ;
- `font-weight` ;
- `font-stretch` ;
- `font-kerning` ;
- `font-variant-ligatures` ;
- `font-variant-position` ;
- `font-variant-caps` ;
- `font-variant-numeric` ;
- `font-variant-alternates` ;
- `font-variant-east-asian` ;
- `font-feature-settings` ;
- `font-variation-settings` ;
- `font` ;
- `letter-spacing` ;
- `line-height` ;
- `text-transform`.

Exemple :

```css
.heading {
  font-family: "Cantarell", sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  font-kerning: normal;
  font-variant-ligatures: common-ligatures;
  line-height: 1.2;
  letter-spacing: 0.01em;
}
```

Le rendu réel dépend de Pango, des polices installées et des fonctionnalités disponibles dans la police. Une propriété reconnue ne peut pas créer un glyphe ou un axe variable absent du fichier de police.

## 9. Texte, caret et décoration

GTK 4.23 documente notamment :

- `color` ;
- `caret-color` ;
- `-gtk-secondary-caret-color` ;
- `text-decoration-line` ;
- `text-decoration-color` ;
- `text-decoration-style` ;
- `text-decoration` ;
- `text-shadow`.

La décoration de texte GTK dispose de propriétés séparées pour la ligne, la couleur et le style. Elle ne doit pas être confondue avec la propriété `text-decoration` plus limitée interprétée dans St 51.

Exemple :

```css
.link-label {
  color: #3584e4;
  text-decoration-line: underline;
  text-decoration-color: currentColor;
  text-decoration-style: dotted;
}
```

GTK permet des styles de soulignement tels que pointillé ou discontinu selon la propriété et le widget. Le Shell St 51 ne reproduit pas ce niveau de détail pour les styles de bordure ou de contour.

## 10. Transformation et filtres

GTK 4.23 documente :

- `transform` ;
- `transform-origin` ;
- `filter` ;
- `opacity`.

Exemple :

```css
.icon-preview {
  opacity: 0.9;
  transform: scale(1.05);
  transform-origin: center;
}
```

Les transformations et filtres ne remplacent pas les propriétés de mise en page du widget. Une transformation visuelle peut déplacer ou agrandir le rendu sans modifier les contraintes de mesure qui organisent les autres widgets.

Vérifiez le rognage, les zones de clic, les animations et le rendu haute densité.

## 11. Bordures, arrière-plans et ombres

GTK 4.23 prend en charge les familles usuelles de bordures, rayons, arrière-plans, images et ombres :

- largeur, style et couleur des quatre bordures ;
- rayons des quatre coins ;
- `border-image` et ses sous-propriétés ;
- `outline`, son style, sa largeur, sa couleur et son décalage ;
- couleur, image, position, répétition, taille, origine et découpe de l'arrière-plan ;
- `background-blend-mode` ;
- `box-shadow`.

Les propriétés sont interprétées selon le contexte du widget et le type de valeur. GTK accepte notamment les styles de bordure discontinus, contrairement à St 51 où les mots-clés de style autres que `solid` sont traités comme un trait plein.

Exemple :

```css
.card {
  background-color: color-mix(in srgb, #ffffff 94%, #3584e4);
  border: 1px solid alpha(currentColor, 0.16);
  border-radius: 14px;
  box-shadow: 0 4px 16px alpha(black, 0.12);
}

.card:focus-within {
  outline: 2px solid #3584e4;
  outline-offset: 3px;
}
```

Toutes ces propriétés ne sont pas nécessairement pertinentes pour chaque nœud. Inspectez le composant et vérifiez son dessin.

## 12. Transitions et animations

GTK 4.23 documente les transitions CSS :

- `transition-property` ;
- `transition-duration` ;
- `transition-timing-function` ;
- `transition-delay` ;
- `transition`.

Les animations CSS documentées comprennent :

- `animation-name` ;
- `animation-duration` ;
- `animation-timing-function` ;
- `animation-iteration-count` ;
- `animation-direction` ;
- `animation-play-state` ;
- `animation-delay` ;
- `animation-fill-mode` ;
- `animation`.

Une animation CSS ne doit pas remplacer une animation métier gérée par le code. Pour l'accessibilité, vérifiez aussi la préférence de réduction des mouvements et le comportement réel du widget.

Les animations CSS GTK et les animations de GNOME Shell sont deux systèmes distincts. La propriété `transition-duration` interprétée par St n'est pas un substitut au moteur complet de transitions et d'animations GTK.

## 13. Espacement des layouts GTK

GTK documente `border-spacing`. Cette propriété est utilisée par certains gestionnaires de disposition, notamment `GtkBoxLayout`, `GtkGridLayout` et `GtkCenterLayout`.

Exemple :

```css
.example-layout {
  border-spacing: 8px;
}
```

Cette propriété n'est pas un remplacement universel de `spacing` dans toutes les API. Le widget ou le gestionnaire de disposition doit explicitement la prendre en compte.

À l'inverse, la propriété St `spacing` est une extension du Shell et ne doit pas être copiée dans une feuille GTK en supposant qu'elle aura le même effet.

## 14. Comparer GTK 4.23 et St 51

Les deux moteurs partagent quelques propriétés courantes, mais leurs périmètres diffèrent.

### Valeurs et unités

GTK 4.23 accepte les longueurs, les pourcentages, les angles, les durées et `calc()`. St 51 accepte un sous-ensemble de longueurs et de durées interprétées par ses accesseurs, mais pas le système général de types GTK.

GTK 4.23 prend en charge `rem`. Le convertisseur de longueurs St 51 ne l'interprète pas comme une unité reconnue.

### Variables

GTK 4.23 prend en charge `--nom`, `var()` et les valeurs de repli. St 51 ne fournit pas ce mécanisme CSS de propriétés personnalisées.

### Couleurs

GTK 4.23 prend en charge les couleurs modernes, dont `oklch()`, `color()` et `color-mix()`. St 51 expose notamment `rgba()`, `st-mix()`, `st-lighten()`, `st-darken()`, `-st-accent-color` et `-st-accent-fg-color`.

### Bordures

GTK 4.23 interprète les styles de bordure documentés, notamment les styles pointillés et discontinus. St 51 traite les styles non solides comme des bordures pleines.

### Icônes

GTK utilise les propriétés `-gtk-icon-*`. St utilise ses propriétés propres, notamment `-st-icon-style` et des propriétés internes aux widgets Shell.

### Animation

GTK 4.23 documente transitions et animations CSS. St 51 ne fournit pas un moteur CSS complet équivalent : le thème peut fournir une durée de transition, mais le composant doit exploiter cette information.

### Arbres de composants

GTK cible des nœuds CSS décrits par chaque widget GTK. St cible des acteurs Clutter et des widgets St. Un sélecteur ne peut pas être transposé d'un arbre à l'autre sans inspection.

## 15. Exemple de portage : bouton du Shell vers GTK

Feuille St :

```css
.panel-button {
  color: white;
  background-color: st-mix(#3584e4, #ffffff, 0.15);
  padding: 6px 10px;
  border-radius: 8px;
  transition-duration: 120ms;
}
```

Version GTK 4.23 :

```css
button.gostm-panel-action {
  color: white;
  background-color: color-mix(in oklab, #3584e4, white 15%);
  padding: 6px 10px;
  border-radius: 8px;
  transition: background-color 120ms ease;
}
```

Ce portage change volontairement :

- le sélecteur, car le nœud GTK doit être un bouton avec la classe ajoutée par l'application ;
- la fonction de couleur, car `st-mix()` est propre à St ;
- la transition, car GTK utilise une déclaration de transition CSS complète ;
- le contexte de rendu, car un bouton GTK n'est pas un acteur du panneau Shell.

Ce code n'est pas destiné à styliser le panneau GNOME Shell. Il montre comment traduire une intention visuelle vers le moteur GTK.

## 16. Exemple de feuille GTK 4.23 maintenable

```css
:root {
  --gostm-surface: #242424;
  --gostm-surface-raised: #303030;
  --gostm-text: #f6f5f4;
  --gostm-accent: oklch(62% 0.19 255);
  --gostm-radius: 12px;
}

window {
  background-color: var(--gostm-surface);
  color: var(--gostm-text);
}

headerbar {
  background-color: var(--gostm-surface-raised);
  color: var(--gostm-text);
}

button.gostm-action {
  background-color: var(--gostm-accent);
  border-radius: var(--gostm-radius);
  transition: background-color 140ms ease;
}

button.gostm-action:hover {
  background-color: color-mix(in oklab, var(--gostm-accent), white 12%);
}

button.gostm-action:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 3px;
}

@media (prefers-reduced-motion: reduce) {
  button.gostm-action {
    transition: none;
  }
}
```

Cet exemple suppose GTK 4.23. Il utilise les propriétés personnalisées, les couleurs modernes et les requêtes de média disponibles dans cette génération.

## 17. Vérification et diagnostic

Pour valider une feuille :

1. Identifiez la version GTK réelle du processus.
2. Ouvrez GTK Inspector.
3. Sélectionnez le widget et examinez son arbre CSS.
4. Vérifiez le nœud, les classes et les états.
5. Consultez les providers CSS et les règles actives.
6. Testez une seule propriété à la fois.
7. Vérifiez les avertissements CSS dans le terminal.
8. Testez clair, sombre, contraste élevé et réduction des mouvements.
9. Testez les facteurs d'échelle et les langues RTL.
10. Vérifiez l'application réelle, pas seulement une maquette isolée.

Pour identifier la bibliothèque de développement :

```bash
pkg-config --modversion gtk4
```

Pour identifier le paquet d'une application Flatpak, inspectez son runtime : la version GTK de l'hôte ne garantit pas celle du processus Flatpak.

## 18. Références officielles GTK 4.23.1

- [GTK 4.23.1 — CSS Properties](https://github.com/GNOME/gtk/blob/4.23.1/docs/reference/gtk/css-properties.md)
- [GTK 4.23.1 — CSS Overview](https://github.com/GNOME/gtk/blob/4.23.1/docs/reference/gtk/css-overview.md)
- [GTK 4.23.1 — sources](https://github.com/GNOME/gtk/tree/4.23.1)
- [Documentation CSS GTK 4](https://docs.gtk.org/gtk4/css-properties.html)
- [GTK 4 — inspection et débogage](https://docs.gtk.org/gtk4/running.html)
- [GNOME Shell 51.0 — interprétation St](https://github.com/GNOME/gnome-shell/blob/51.0/src/st/st-theme-node.c)

Les sources du dépôt sont épinglées sur GTK 4.23.1 et GNOME Shell 51.0. Une version ultérieure peut ajouter, retirer ou modifier une propriété : vérifiez toujours la version réellement utilisée par l'application.
