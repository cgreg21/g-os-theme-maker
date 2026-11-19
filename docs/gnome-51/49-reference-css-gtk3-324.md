# GTK 3.24 : référence CSS complète, propriétés et limites du moteur

Ce chapitre approfondit le moteur CSS de GTK 3.24. Il complète l'atelier pratique GTK 3 en donnant une référence structurée des sélecteurs, des types de valeurs, des propriétés documentées et des extensions GTK historiques.

La référence de propriétés et de sélecteurs est épinglée sur le tag amont **GTK 3.24.52**. Une distribution peut intégrer des correctifs supplémentaires, mais il faut partir de cette version documentée pour comparer les comportements.

GTK 3, GTK 4 et GNOME Shell St sont trois moteurs différents. Une feuille GTK 3 ne doit pas être considérée comme une feuille GTK 4 ancienne, et encore moins comme une feuille GNOME Shell.

## 1. Modèle de style GTK 3

GTK applique les règles CSS à un arbre de nœuds construit par les widgets. Chaque nœud possède un nom, un état et éventuellement des classes de style. Les nœuds enfants sont ordonnés.

Un widget peut exposer plusieurs nœuds internes. Un `GtkScale`, par exemple, expose le nœud `scale`, des nœuds de marques, une piste `trough`, une poignée `slider` et parfois des nœuds `highlight` ou `fill`.

Le sélecteur doit donc viser le nœud CSS, pas le nom de la classe C. Un `GtkButton` expose généralement le nœud `button`.

Pour inspecter un widget :

1. Lancez l'application avec l'inspecteur GTK.
2. Sélectionnez le composant dans l'arbre.
3. Relevez le nom du nœud, son identifiant et ses classes.
4. Relevez les nœuds enfants.
5. Activez les états hover, focus, checked, disabled ou selected.
6. Écrivez une règle courte et vérifiez le résultat.

## 2. Sélecteurs documentés

GTK 3.24.52 documente les familles de sélecteurs suivantes :

- `*` : tous les nœuds ;
- `E` : un nœud nommé `E` ;
- `E.class` : un nœud `E` portant une classe ;
- `E#id` : un nœud `E` portant un nom/identifiant ;
- `:nth-child()` et `:nth-last-child()` ;
- `:first-child`, `:last-child` et `:only-child` ;
- `:link` et `:visited` ;
- `:active`, `:hover` et `:focus` ;
- `:disabled`, `:checked`, `:indeterminate` ;
- `:backdrop` et `:selected` ;
- `:not()` ;
- `:dir(ltr)` et `:dir(rtl)` ;
- `:drop(active)` ;
- les combinateurs descendant, enfant direct, frère général et frère adjacent.

Exemples :

```css
/* Tous les boutons */
button {
  border-radius: 8px;
}

/* Classe de style */
button.suggested-action {
  font-weight: 700;
}

/* Nœud enfant direct */
notebook > header {
  border-bottom: 1px solid @borders;
}

/* État de survol */
button:hover {
  background-color: #e8e6e3;
}

/* État désactivé */
entry:disabled {
  opacity: 0.55;
}

/* Direction du texte */
entry:dir(rtl) {
  text-align: right;
}
```

GTK 3.24 ne prend pas en charge les sélecteurs d'attributs CSS Web. N'écrivez pas de sélecteurs comme `[disabled]` ou `[role="..."]` en supposant qu'ils correspondent aux propriétés internes du widget.

Les pseudo-classes d'état ne peuvent s'appliquer qu'au dernier élément du sélecteur dans le modèle documenté par GTK 3.24. Ne transposez pas automatiquement les règles plus récentes de GTK 4.

## 3. Feuilles de style et importations

Une feuille est composée de règles et de règles `@`. Une règle contient un sélecteur, puis un bloc de déclarations.

GTK 3.24 prend en charge `@import` pour charger une autre feuille :

```css
@import url("common.css");

button {
  border-radius: 8px;
}
```

Les chemins doivent être résolus dans le contexte de la feuille et du thème installés. Vérifiez le résultat après installation, pas seulement dans le répertoire de développement.

Pour éviter les dépendances difficiles à diagnostiquer, gardez une hiérarchie courte et documentez les fichiers importés.

## 4. Types de valeurs et unités

La référence GTK 3.24.52 documente les types suivants :

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

### Pourcentages, angles et durées

- pourcentages `%` ;
- angles `deg`, `grad`, `turn` ;
- durées `s`, `ms`.

### Calculs

GTK 3.24 prend en charge `calc()` pour les types compatibles. Le calcul ne peut pas combiner arbitrairement des grandeurs de nature différente.

```css
.entry {
  min-width: calc(12em + 24px);
  padding: 0.5em 1em;
  transition-duration: calc(100ms + 50ms);
}
```

Les unités physiques utilisent la résolution GTK configurée, notamment via `-gtk-dpi`. La conversion ne doit pas être supposée identique à celle d'un navigateur.

## 5. Couleurs nommées et expressions GTK

GTK 3 utilise les couleurs nommées avec `@define-color`. C'est la méthode historique pour partager une palette.

```css
@define-color gostm_bg #242424;
@define-color gostm_fg #f6f5f4;
@define-color gostm_accent #3584e4;
@define-color gostm_border #5e5c64;

window {
  background-color: @gostm_bg;
  color: @gostm_fg;
}

button.suggested-action {
  background-color: @gostm_accent;
}
```

Les expressions de couleur GTK documentées comprennent :

- `lighter(color)` ;
- `darker(color)` ;
- `shade(color, number)` ;
- `alpha(color, number)` ;
- `mix(color1, color2, number)`.

Exemple :

```css
button:hover {
  background-color: shade(@gostm_accent, 1.12);
}

button:disabled {
  color: alpha(@gostm_fg, 0.55);
}
```

Le facteur de `shade()` est interprété selon la règle GTK : 1 laisse la couleur inchangée, 0 tend vers le noir et 2 vers le blanc. `alpha()` multiplie l'opacité de la couleur ; `mix()` mélange les deux couleurs.

Sur Windows, GTK 3 documente aussi des références aux couleurs système via `-gtk-win32-color()`. Ces expressions sont spécifiques à cette plateforme.

## 6. Images, gradients et ressources

GTK 3.24 accepte plusieurs formes d'image CSS :

- URL d'image ;
- `cross-fade()` ;
- `image()` pour les alternatives et les valeurs de repli ;
- `linear-gradient()` ;
- `repeating-linear-gradient()` ;
- `radial-gradient()` ;
- `repeating-radial-gradient()`.

Exemple de dégradé :

```css
headerbar {
  background-image: linear-gradient(
    to bottom,
    #3d3846,
    #241f31
  );
}
```

Exemple d'image avec valeur de repli :

```css
button {
  background-image: image(
    url("assets/action.svg"),
    url("assets/action.png"),
    #3584e4
  );
}
```

Les formats disponibles dépendent des chargeurs GdkPixbuf installés. PNG, JPEG et SVG sont généralement disponibles, mais la liste exacte dépend de la construction et des dépendances du système.

Les images et les gradients sont des images CSS. Ils ne sont pas des widgets : ils ne fournissent ni interaction ni comportement de contrôle.

## 7. Propriétés de couleur et d'opacité

Les propriétés documentées comprennent :

- `color` ;
- `opacity`.

`color` définit la couleur de premier plan utilisée par le rendu du texte, des icônes et des autres éléments de premier plan. `opacity` contrôle la composition du widget sur son parent.

Exemple :

```css
.dialog-content {
  color: @gostm_fg;
  opacity: 1;
}
```

Une opacité réduite sur un parent affecte également ses descendants. Pour désactiver visuellement un contrôle sans rendre son texte illisible, privilégiez les états et les couleurs adaptés au widget.

## 8. Propriétés typographiques

GTK 3.24 documente :

- `font-family` ;
- `font-size` ;
- `font-style` ;
- `font-variant` ;
- `font-weight` ;
- `font-stretch` ;
- `font-feature-settings` ;
- `font`.

La police par défaut est liée au réglage GTK `gtk-font-name`.

Exemple :

```css
window {
  font-family: "Cantarell", sans-serif;
  font-size: 10pt;
}

.title {
  font-weight: 700;
}

.caption {
  font-size: 0.9em;
  font-style: italic;
}
```

GTK 3 ne fournit pas l'ensemble typographique documenté par GTK 4.23. Ne supposez pas la présence de `font-variation-settings`, des variantes de ligatures modernes ou de toutes les propriétés avancées GTK 4.

## 9. Propriétés de texte et curseur

Les propriétés de texte documentées comprennent :

- `caret-color` ;
- `-gtk-secondary-caret-color` ;
- `letter-spacing` ;
- `text-decoration-line` ;
- `text-decoration-color` ;
- `text-decoration-style` ;
- `text-decoration` ;
- `text-shadow`.

Exemple :

```css
entry {
  caret-color: @gostm_accent;
}

.link {
  text-decoration-line: underline;
  text-decoration-color: @gostm_accent;
}

.warning-label {
  text-shadow: 0 1px 1px alpha(black, 0.25);
}
```

Le style de décoration et les valeurs réellement dessinées dépendent du widget texte. Vérifiez la sélection, le curseur, le texte bidirectionnel et le focus.

## 10. Propriétés d'icônes GTK

GTK 3.24 expose plusieurs propriétés spécifiques :

- `-gtk-icon-source` ;
- `-gtk-icon-transform` ;
- `-gtk-icon-style` ;
- `-gtk-icon-theme` ;
- `-gtk-icon-palette` ;
- `-gtk-icon-shadow` ;
- `-gtk-icon-effect`.

Ces propriétés contrôlent les icônes intégrées ou chargées par les widgets GTK. Leur effet dépend de la façon dont le widget construit et dessine son icône.

Ne confondez pas le style d'une icône symbolique avec une image bitmap. Une image PNG ne devient pas automatiquement recolorable parce qu'une palette symbolique est définie.

GTK 3 utilise le préfixe `-gtk-`. Le Shell St utilise ses propres extensions, dont `-st-icon-style`. Ces deux familles ne sont pas interchangeables.

## 11. Propriétés de taille, marges et padding

Les propriétés de géométrie documentées comprennent :

- `min-width` et `min-height` ;
- `margin-top`, `margin-right`, `margin-bottom`, `margin-left` ;
- `padding-top`, `padding-right`, `padding-bottom`, `padding-left` ;
- `margin` ;
- `padding`.

Les formes abrégées à une, deux, trois ou quatre valeurs suivent la répartition classique des quatre côtés.

```css
button {
  padding: 6px 12px;
  margin: 2px;
}

entry {
  min-width: 180px;
}
```

Le widget peut appliquer des contraintes de taille supplémentaires. Une propriété géométrique ne peut pas obliger un conteneur à violer son propre gestionnaire de disposition.

## 12. Bordures, rayons et images de bordure

GTK 3.24 documente :

- les largeurs de chaque côté et `border-width` ;
- les styles de chaque côté et `border-style` ;
- les couleurs de chaque côté et `border-color` ;
- les quatre rayons de coin et `border-radius` ;
- `border-image-source` ;
- `border-image-repeat` ;
- `border-image-slice` ;
- `border-image-width` ;
- les raccourcis `border-top`, `border-right`, `border-bottom`, `border-left` et `border` ;
- `border-image`.

Exemple :

```css
button {
  border: 1px solid @gostm_border;
  border-radius: 8px;
}

button:focus {
  border-color: @gostm_accent;
}
```

Contrairement à St 51, GTK 3 documente les styles de bordure usuels. Leur rendu peut toutefois dépendre du widget et du moteur de dessin. Testez les styles discontinus sur le composant réel.

## 13. Contours

Les propriétés documentées comprennent :

- `outline-style` ;
- `outline-width` ;
- `outline-color` ;
- `outline-offset` ;
- `outline` ;
- `-gtk-outline-top-left-radius` ;
- `-gtk-outline-top-right-radius` ;
- `-gtk-outline-bottom-right-radius` ;
- `-gtk-outline-bottom-left-radius` ;
- `-gtk-outline-radius`.

Exemple :

```css
button:focus {
  outline: 2px solid @gostm_accent;
  outline-offset: 2px;
}
```

GTK 3 documente des propriétés de rayon de contour propres à GTK. Ne les copiez pas dans St ou GTK 4 sans vérifier la référence du moteur cible.

Conservez un indicateur de focus visible. Un focus invisible rend la navigation clavier difficile et dégrade l'accessibilité.

## 14. Arrière-plans et ombres

Les propriétés documentées comprennent :

- `background-color` ;
- `background-clip` ;
- `background-origin` ;
- `background-size` ;
- `background-position` ;
- `background-repeat` ;
- `background-image` ;
- `background-blend-mode` ;
- `background` ;
- `box-shadow`.

Exemple :

```css
popover.background {
  background-color: @gostm_bg;
  background-image: linear-gradient(
    to bottom,
    #35313d,
    #24212a
  );
  border: 1px solid @gostm_border;
  border-radius: 12px;
  box-shadow: 0 8px 24px alpha(black, 0.35);
}
```

Les propriétés de découpe et d'origine déterminent comment le fond est peint par rapport aux zones de bordure et de padding. Le rendu dépend du widget qui dessine la surface.

## 15. Transitions

GTK 3.24 documente :

- `transition-property` ;
- `transition-duration` ;
- `transition-timing-function` ;
- `transition-delay` ;
- `transition`.

Exemple :

```css
button {
  transition: background-color 140ms ease-in-out,
              border-color 140ms ease-in-out;
}
```

Une transition n'est visible que pour les propriétés que GTK peut interpoler et que le widget actualise. Elle ne remplace pas une animation applicative.

## 16. Animations CSS

GTK 3.24 documente :

- `animation-name` ;
- `animation-duration` ;
- `animation-timing-function` ;
- `animation-iteration-count` ;
- `animation-direction` ;
- `animation-play-state` ;
- `animation-delay` ;
- `animation-fill-mode` ;
- `animation`.

Les animations s'appuient sur des règles `@keyframes`. Exemple :

```css
@keyframes gostm-pulse {
  from {
    opacity: 0.65;
  }

  to {
    opacity: 1;
  }
}

.spinner-decoration {
  animation: gostm-pulse 800ms ease-in-out infinite alternate;
}
```

Ne supposez pas qu'une animation peut être appliquée utilement à n'importe quel widget ou à n'importe quelle propriété. Vérifiez les propriétés animables et le comportement réel du composant.

La prise en charge CSS des animations ne désactive pas les animations programmatiques. Testez les préférences d'accessibilité et les performances.

## 17. Raccourcis clavier et propriétés spécifiques

GTK 3 documente `-gtk-key-bindings` pour associer un nom de jeu de raccourcis à un widget. Cette propriété n'est pas un raccourci CSS de mise en page : elle intervient dans le mécanisme de bindings GTK.

Sur Windows, GTK 3.24 expose également des extensions `-gtk-win32-*` pour accéder à des dimensions, parties et couleurs du thème système Windows. Elles sont spécifiques au backend Windows et ne constituent pas une solution portable pour GNOME Linux.

Ne placez pas ces propriétés dans un thème multiplateforme sans conditionner leur usage au backend concerné.

## 18. Ce que GTK 3.24 ne fournit pas comme GTK 4 moderne

GTK 3.24 ne documente pas le mécanisme de propriétés personnalisées CSS `--nom` et `var()` introduit dans GTK 4.16. Il ne fournit pas non plus le modèle de requêtes de média GTK 4.20 décrit dans le chapitre 42.

Ne comptez donc pas sur :

- les variables CSS personnalisées `--nom` ;
- la fonction `var()` ;
- le sélecteur `:root` comme point d'entrée des variables ;
- les requêtes `@media (prefers-color-scheme: ...)` ;
- les requêtes `prefers-contrast` ;
- les requêtes `prefers-reduced-motion` ;
- les couleurs modernes GTK 4.23 telles que `oklch()` ou `color-mix()` ;
- les propriétés typographiques propres à GTK 4.23.

Pour partager un thème entre GTK 3 et GTK 4, maintenez des feuilles distinctes. Partagez éventuellement les images et les valeurs de palette dans une source de génération commune, mais générez une syntaxe compatible avec chaque moteur.

## 19. Exemple complet de feuille GTK 3

```css
@define-color gostm_bg #242424;
@define-color gostm_surface #303030;
@define-color gostm_fg #f6f5f4;
@define-color gostm_accent #3584e4;
@define-color gostm_border #5e5c64;

window,
.background {
  background-color: @gostm_bg;
  color: @gostm_fg;
}

headerbar {
  background-color: @gostm_surface;
  color: @gostm_fg;
  border-bottom: 1px solid @gostm_border;
}

button {
  background-color: @gostm_surface;
  color: @gostm_fg;
  border: 1px solid @gostm_border;
  border-radius: 8px;
  padding: 6px 12px;
  transition: background-color 140ms ease;
}

button:hover {
  background-color: shade(@gostm_surface, 1.12);
}

button:active,
button:checked {
  background-color: shade(@gostm_surface, 0.92);
}

button:focus {
  outline: 2px solid @gostm_accent;
  outline-offset: 2px;
}

button.suggested-action {
  background-color: @gostm_accent;
  color: white;
  border-color: @gostm_accent;
}

entry {
  background-color: @gostm_surface;
  color: @gostm_fg;
  border: 1px solid @gostm_border;
  border-radius: 7px;
  padding: 6px 8px;
}

entry:focus {
  border-color: @gostm_accent;
}

tooltip {
  background-color: #171717;
  color: white;
}
```

Cette feuille est un exemple de départ. Les nœuds exacts doivent être vérifiés pour chaque application, et les classes `.suggested-action` ou les états peuvent varier selon le composant.

## 20. Diagnostic des erreurs courantes

### Une règle ne change rien

Vérifiez successivement :

1. Le processus est-il réellement GTK 3 ?
2. Le thème est-il chargé par ce processus ?
3. Le sélecteur existe-t-il dans l'arbre ?
4. La classe est-elle présente ?
5. Le widget est-il dans l'état visé ?
6. La propriété est-elle documentée ?
7. Le widget dessine-t-il cette propriété ?

### Une couleur nommée n'est pas résolue

Vérifiez que `@define-color` est déclaré avant son utilisation et que le nom ne comporte pas de faute. Vérifiez aussi le fichier importé et le chemin de l'import.

### Une propriété GTK 4 ne fonctionne pas

Vérifiez la version et le moteur. `var()`, les requêtes de média modernes et les couleurs modernes GTK 4 ne doivent pas être supposées disponibles dans GTK 3.24.

### Le rendu change entre deux applications

Chaque application peut utiliser des classes privées, des providers CSS, des ressources embarquées ou un dessin personnalisé. Un thème GTK ne peut pas uniformiser un composant qui n'expose pas les mêmes nœuds.

## 21. Sources officielles GTK 3.24.52

- [GTK 3.24.52 — CSS Overview](https://github.com/GNOME/gtk/blob/3.24.52/docs/reference/gtk/css-overview.xml)
- [GTK 3.24.52 — CSS Properties](https://github.com/GNOME/gtk/blob/3.24.52/docs/reference/gtk/css-properties.xml)
- [GTK 3.24.52 — sources](https://github.com/GNOME/gtk/tree/3.24.52)
- [GTK 3 — documentation API](https://docs.gtk.org/gtk3/)
- [GTK 3 — lancement et inspection](https://docs.gtk.org/gtk3/running.html)

Les propriétés sont celles documentées par GTK 3.24.52. La prise en charge d'une propriété par le moteur ne garantit pas que tous les widgets l'utilisent : contrôlez toujours le nœud, l'état et le rendu du composant ciblé.
