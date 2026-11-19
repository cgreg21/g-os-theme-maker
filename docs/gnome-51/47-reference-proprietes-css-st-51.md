# Référence des propriétés CSS réellement interprétées par St dans GNOME Shell 51

Ce chapitre complète le catalogue de sélecteurs et le fonctionnement de la cascade. Il répond à une question plus précise : **quelles propriétés le code de St lit-il réellement, quelles valeurs accepte-t-il et quelles syntaxes CSS du Web ne faut-il pas supposer compatibles ?**

La référence est établie à partir de `src/st/st-theme-node.c` du tag officiel GNOME Shell `51.0`, en particulier les fonctions qui interprètent les déclarations de géométrie, d'arrière-plan, de typographie, d'ombres et de couleurs.

Une propriété présente dans une feuille SCSS n'est pas nécessairement interprétée par St. Inversement, certaines propriétés ne sont pas des propriétés CSS Web standard, mais sont lues explicitement par le Shell ou par un widget St.

## 1. Comment lire cette référence

Il faut distinguer trois niveaux :

1. **Analyse CSS** : le parseur accepte ou rejette la syntaxe.
2. **Interprétation St** : `StThemeNode` lit une déclaration et convertit sa valeur en couleur, longueur, police, ombre ou autre donnée.
3. **Utilisation par le widget** : le composant doit demander cette donnée et l'utiliser dans son calcul de taille ou son dessin.

Une déclaration peut donc être analysée sans avoir d'effet visuel. Par exemple, une propriété personnalisée peut être conservée dans le nœud et consultable par un widget, sans que St lui-même sache comment la dessiner.

Les propriétés répertoriées ci-dessous sont celles dont l'interprétation est identifiable dans le code 51.0. Cette liste n'est pas une promesse de prise en charge de toutes les variantes de la spécification CSS.

## 2. Unités de longueur

Le convertisseur de longueurs de St traite les unités suivantes :

- `px` : pixels CSS convertis avec le facteur d'échelle du thème ;
- `pt` : points typographiques, convertis avec la résolution du contexte ;
- `in` : pouces ;
- `cm` : centimètres ;
- `mm` : millimètres ;
- `pc` : picas ;
- `em` : taille de police de référence ;
- `ex` : approximation de la moitié de la taille de police.

La valeur numérique sans unité est acceptée uniquement lorsqu'elle vaut zéro. Une longueur non nulle sans unité est ignorée et peut produire un avertissement.

Exemples :

```css
.panel-button {
  padding: 6px;
  border-radius: 8px;
  margin-top: 0;
  font-size: 1.1em;
}
```

Les pourcentages ne sont pas pris en charge comme longueurs génériques par le convertisseur géométrique de St 51.0. Une règle comme `padding: 5%` ne doit donc pas être utilisée comme si elle avait le comportement d'un navigateur.

Les dimensions issues de `StThemeNode` sont converties en pixels physiques et tiennent compte du facteur d'échelle. Il ne faut pas confondre ces valeurs internes avec les pixels logiques d'une maquette.

## 3. Dimensions et contraintes de taille

Les propriétés interprétées dans le calcul géométrique sont :

- `width` ;
- `height` ;
- `min-width` ;
- `min-height` ;
- `max-width` ;
- `max-height` ;
- `-st-natural-width` ;
- `-st-natural-height`.

Les dimensions peuvent être des longueurs reconnues ou `auto`. La valeur `auto` remet la dimension concernée à son état non fixé.

Le code applique des relations spécifiques :

- `width` fournit une valeur par défaut à la largeur naturelle, minimale et maximale si ces valeurs ne sont pas définies séparément ;
- `height` suit la même logique pour la hauteur ;
- `min-width` et `min-height` peuvent relever la taille naturelle ;
- les ajustements finaux sont réalisés par les fonctions de calcul de taille de `StThemeNode`.

Exemple :

```css
.search-entry {
  min-width: 220px;
  max-width: 420px;
  height: 36px;
}
```

Les propriétés `-st-natural-width` et `-st-natural-height` sont des extensions internes. Elles ne sont pas des propriétés CSS standard à réutiliser dans GTK ou dans un navigateur.

Ne supposez pas que `width: 100%` fonctionne dans St comme dans une page Web : les longueurs en pourcentage ne sont pas prises en charge par le chemin de conversion utilisé pour ces dimensions.

## 4. Marges et espacements internes

St interprète les propriétés suivantes :

- `margin`, `margin-top`, `margin-right`, `margin-bottom`, `margin-left` ;
- `padding`, `padding-top`, `padding-right`, `padding-bottom`, `padding-left`.

Les formes abrégées à une, deux, trois ou quatre valeurs suivent la répartition CSS classique :

```css
/* Même valeur sur les quatre côtés */
.example-a { padding: 8px; }

/* Haut/bas puis gauche/droite */
.example-b { padding: 6px 12px; }

/* Haut, gauche/droite, bas */
.example-c { padding: 4px 10px 8px; }

/* Haut, droite, bas, gauche */
.example-d { padding: 4px 8px 10px 12px; }
```

Les formes latérales sont également prises en charge :

```css
.example {
  padding-left: 12px;
  margin-bottom: 6px;
}
```

Pour les formes abrégées, St 51.0 est volontairement permissif : si certaines valeurs ne sont pas reconnues, il peut conserver les termes qu'il comprend au lieu de rejeter toute la déclaration. Ne prenez pas cette tolérance pour une validation stricte de la syntaxe.

## 5. Bordures : largeur, couleur et rayon

Les familles interprétées comprennent :

- `border` ;
- `border-top`, `border-right`, `border-bottom`, `border-left` ;
- `border-width` et ses variantes latérales ;
- `border-color` et ses variantes latérales ;
- `border-radius` ;
- `border-radius-topleft`, `border-radius-topright`, `border-radius-bottomright`, `border-radius-bottomleft`.

Exemple :

```css
.quick-settings-button {
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 12px;
}

.quick-settings-button:active {
  border-color: #78aeed;
  border-radius: 10px;
}
```

Les rayons peuvent être définis avec une à quatre longueurs. Les longueurs sont converties par le moteur St ; il ne faut pas supposer que toutes les syntaxes avancées de rayon du CSS Web sont disponibles.

### Styles de bordure : limite importante

Dans St 51.0, `solid` est le seul style de bordure réellement dessiné comme style distinct. Les mots-clés `dotted`, `dashed`, `double`, `groove`, `ridge`, `inset` et `outset` sont acceptés dans le traitement de la déclaration, mais traités comme `solid`.

Par conséquent, ceci ne produit pas une vraie bordure en tirets :

```css
/* Dans St 51.0, le style sera traité comme solid */
.example {
  border: 2px dashed white;
}
```

Pour créer un contour décoratif, utilisez une image de bordure si le composant la prend en charge, ou construisez un élément visuel adapté. Ne promettez jamais un motif pointillé ou discontinu avec `border-style` dans St 51.0.

## 6. Contours externes

Les propriétés interprétées sont :

- `outline` ;
- `outline-color` ;
- `outline-width`.

Exemple :

```css
.button:focus {
  outline: 2px solid #78aeed;
}
```

Comme pour les bordures, le parseur de contour traite les styles autres que `solid` comme un contour plein. Les mots-clés décoratifs ne produisent donc pas les motifs correspondants.

Le contour ne remplace pas une vérification d'accessibilité. Testez le contraste du focus sur les fonds clair et sombre et vérifiez que le contour n'est pas rogné par le conteneur parent.

## 7. Arrière-plans : couleur et image

St interprète la famille `background` et plusieurs propriétés associées :

- `background` ;
- `background-color` ;
- `background-image` ;
- `background-position` ;
- `background-repeat` ;
- `background-size`.

Les variantes internes effectivement lues par le code incluent notamment :

- `background-color` ;
- `background-image` ;
- `background-position` ;
- `background-repeat` ;
- `background-size`.

Exemple de base :

```css
.overview {
  background-color: #171a21;
  background-image: url("images/overview-background.png");
  background-position: 0px 0px;
  background-repeat: repeat;
  background-size: cover;
}
```

Les chemins d'image sont résolus par rapport à la feuille de style qui porte la déclaration. Utilisez des chemins relatifs corrects et livrez les fichiers dans le thème ou l'extension. Un chemin valide dans l'arborescence de développement peut devenir invalide après installation.

### Limites de répétition et de taille

Le code de St 51.0 ne reproduit pas tout le modèle d'arrière-plan du Web :

- `background-repeat` n'active la répétition que pour la valeur `repeat` ;
- les autres valeurs ne forment pas une matrice complète de modes de répétition ;
- `background-size` interprète `cover`, `contain`, `auto` et des dimensions fixes reconnues ;
- les dimensions fixes doivent être des nombres convertibles en longueurs St ;
- les positions sont traitées comme deux longueurs.

Ne comptez pas sur `repeat-x`, `repeat-y`, `space`, `round`, les positions en pourcentage ou les syntaxes multiples complexes comme dans un navigateur.

## 8. Dégradés St

Le moteur expose des propriétés internes de dégradé :

- `-st-gradient-direction` ;
- `-st-gradient-start` ;
- `-st-gradient-end`.

Les directions interprétées dans le code sont :

- `vertical` ;
- `horizontal` ;
- `radial` ;
- `none`.

Exemple :

```css
.panel {
  -st-gradient-direction: vertical;
  -st-gradient-start: #303846;
  -st-gradient-end: #171b23;
}
```

Ce mécanisme est spécifique à St. Il ne faut pas le confondre avec la syntaxe moderne `linear-gradient()` ou `radial-gradient()` des navigateurs.

## 9. Couleurs et fonctions spécifiques à St

St interprète les couleurs CSS classiques prises en charge par son parseur, ainsi que :

- `transparent` ;
- `rgba(...)` ;
- `-st-accent-color` ;
- `-st-accent-fg-color` ;
- `st-transparentize(...)` ;
- `st-mix(...)` ;
- `st-lighten(...)` ;
- `st-darken(...)`.

Exemples :

```css
.button {
  background-color: st-mix(#3584e4, #ffffff, 0.15);
  color: -st-accent-fg-color;
}

.button:hover {
  background-color: st-lighten(-st-accent-color, 10%);
}

.button:active {
  background-color: st-darken(-st-accent-color, 10%);
}
```

Ces fonctions sont des extensions St, pas des fonctions CSS web portables. Ne les copiez pas dans une feuille GTK ou Libadwaita sans vérifier le moteur destinataire.

Le code interprète également `warning-color`, `error-color` et `success-color` pour construire les couleurs utilisées par les icônes symboliques. Leur présence ne signifie pas que tout widget affiche automatiquement ces couleurs.

## 10. Ombres

Les propriétés d'ombre lues par les accesseurs de St comprennent :

- `box-shadow` ;
- `text-shadow` ;
- `-st-background-image-shadow`.

Exemple :

```css
.popup-menu {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

.popup-menu-item {
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.25);
}
```

St accepte les décalages horizontaux et verticaux obligatoires, puis le flou et l'étalement. La couleur et le mot-clé `inset` peuvent être placés avec plus de souplesse que ne l'exige la grammaire stricte du CSS.

Limites explicites du code :

- les valeurs de flou négatives sont refusées ;
- les valeurs d'étalement négatives sont refusées ;
- les valeurs supplémentaires sont ignorées avec avertissement ;
- `text-shadow` ne prend pas en charge `inset` ;
- `-st-background-image-shadow` ne prend pas en charge `inset`.

Une ombre n'est visible que si le widget appelle le chemin de rendu correspondant. L'existence de la propriété ne force pas tous les acteurs à dessiner une ombre.

## 11. Typographie

St interprète les propriétés suivantes :

- `font` ;
- `font-family` ;
- `font-size` ;
- `font-weight` ;
- `font-style` ;
- `font-variant` ;
- `font-feature-settings` ;
- `letter-spacing`.

### Famille

La famille peut être donnée sous forme de mots non cités ou de chaînes entre guillemets, avec des familles séparées par des virgules.

```css
.shell-label {
  font-family: "Cantarell", "Noto Sans", sans-serif;
}
```

Les noms contenant des espaces doivent être cités. Une liste mal formée peut être ignorée.

### Taille

Le code traite les tailles absolues, les unités reconnues, les pourcentages relatifs à la taille de police héritée et les mots-clés :

- `xx-small` ;
- `x-small` ;
- `small` ;
- `medium` ;
- `large` ;
- `x-large` ;
- `xx-large` ;
- `smaller` ;
- `larger`.

```css
.shell-label {
  font-size: 1.1em;
}
```

### Graisse

Le code accepte les valeurs numériques génériques et les mots-clés :

- `normal` ;
- `bold` ;
- `bolder` ;
- `lighter`.

L'implémentation transmet la valeur à Pango et ne limite pas strictement les nombres à l'intervalle normatif 100–900.

### Style et variante

`font-style` accepte `normal`, `oblique` et `italic`.

`font-variant` accepte `normal` et `small-caps`.

### Fonctionnalités OpenType

`font-feature-settings` est exposée sous forme de chaîne par St. Sa prise en charge effective dépend de Pango et de la police chargée.

### Espacement des lettres

`letter-spacing` est interprété comme une longueur. La valeur retournée est en pixels physiques.

## 12. Alignement et décoration du texte

Les propriétés interprétées sont :

- `text-align` ;
- `text-decoration`.

`text-align` accepte :

- `start` ;
- `end` ;
- `left` ;
- `right` ;
- `center` ;
- `justify` ;
- `inherit`.

`text-decoration` accepte les indicateurs :

- `none` ;
- `underline` ;
- `overline` ;
- `line-through` ;
- `blink` ;
- `inherit`.

Exemples :

```css
.search-result-title {
  text-align: start;
  text-decoration: none;
}

.link-like-label {
  text-decoration: underline;
}
```

L'effet final dépend du widget texte et de la façon dont il transmet ces propriétés à Pango ou au rendu Clutter.

## 13. Icônes et couleurs sémantiques

La propriété `-st-icon-style` accepte trois valeurs :

- `requested` : style demandé par l'appelant ;
- `regular` : icône régulière ;
- `symbolic` : icône symbolique.

Exemple :

```css
.status-icon {
  -st-icon-style: symbolic;
}
```

Les couleurs des icônes symboliques peuvent être construites à partir de :

- `color` pour la couleur de premier plan ;
- `warning-color` ;
- `error-color` ;
- `success-color`.

Ces propriétés sont utilisées par le mécanisme de couleurs d'icônes de St. Elles ne changent pas automatiquement le contenu d'une image PNG ou d'une icône non symbolique.

## 14. Durée de transition

St interprète `transition-duration` comme une durée. L'accesseur la convertit en millisecondes et la multiplie par le facteur de ralentissement configuré dans `St.Settings`.

Exemple :

```css
.panel-button {
  transition-duration: 150ms;
}
```

Cette propriété ne transforme pas à elle seule tous les changements de style en animations. Le widget doit gérer le changement de nœud de thème et exploiter la durée calculée.

Les animations globales de GNOME et les transitions CSS d'un navigateur sont des mécanismes distincts.

## 15. Bordures par image

St expose la propriété `border-image`. Dans le code 51.0, le premier terme doit être une URL, suivie de zéro à quatre valeurs numériques génériques qui définissent les découpes de l'image.

Exemple de principe :

```css
.decorative-frame {
  border-image: url("images/frame.png") 12 12 12 12;
}
```

Les pourcentages ne sont pas pris en charge comme découpes. Les valeurs doivent être des nombres sans unité, pas des longueurs CSS arbitraires.

La ressource doit exister et être résolue relativement à la feuille de style. Testez le résultat sur des tailles de widgets très différentes : une image de bordure adaptée à un menu court peut être inadaptée à un panneau large.

## 16. Propriétés qui ne doivent pas être présumées compatibles

Les syntaxes suivantes ne doivent pas être utilisées en supposant une compatibilité complète avec le navigateur :

- longueurs en pourcentage pour la géométrie ;
- unités viewport comme `vw` et `vh` ;
- variables personnalisées CSS `var(--nom)` ;
- fonctions modernes `calc()`, `min()`, `max()`, `clamp()` ;
- fonctions de dégradé CSS Web ;
- modes de répétition d'arrière-plan autres que `repeat` ;
- positions d'arrière-plan complexes ou en pourcentage ;
- styles de bordure discontinus ;
- propriétés de grille ou flexbox Web ;
- transitions génériques de toutes les propriétés ;
- filtres graphiques CSS Web.

Cette liste est une liste de précaution, pas une affirmation que chaque chaîne sera toujours rejetée au niveau du parseur. La règle est plus précise : **si le code St 51.0 n'interprète pas la propriété ou si le widget ne la consomme pas, ne comptez pas sur elle pour le rendu**.

## 17. Exemple de feuille robuste pour St

Cet exemple utilise des familles de propriétés effectivement interprétées par St 51.0 :

```css
.panel-button {
  color: #f6f5f4;
  background-color: rgba(255, 255, 255, 0.06);
  padding: 6px 10px;
  margin: 2px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  transition-duration: 120ms;
}

.panel-button:hover {
  background-color: rgba(255, 255, 255, 0.12);
}

.panel-button:active {
  background-color: st-darken(#3584e4, 12%);
  border-color: #78aeed;
}

.panel-button:focus {
  outline: 2px solid #78aeed;
}

.panel-button:insensitive {
  opacity: 0.5;
}
```

Le sélecteur doit correspondre à un acteur réellement présent. Les valeurs de style doivent être testées sur l'acteur et les états concernés. Ce code n'est pas un composant autonome : il ne crée ni bouton ni comportement interactif.

## 18. Méthode de vérification dans le code

Pour confirmer une propriété douteuse dans la version ciblée :

1. Ouvrir le tag GNOME Shell `51.0`.
2. Consulter `src/st/st-theme-node.c`.
3. Rechercher le nom de propriété avec `grep`.
4. Repérer l'accesseur qui lit la déclaration.
5. Examiner le convertisseur de valeur appelé.
6. Vérifier si le widget concerné utilise l'accesseur.
7. Tester une feuille minimale sur une session de test.

Commandes utiles après avoir cloné le dépôt source :

```bash
git checkout 51.0
grep -nE 'border|background|font|shadow|transition-duration' src/st/st-theme-node.c
grep -RIn --include='*.c' --include='*.h' 'get_theme_node' src/st
```

Pour les extensions, vérifiez également si le code GJS applique un style en ligne ou modifie dynamiquement les classes de l'acteur.

## 19. Sources officielles

- [GNOME Shell 51.0 — st-theme-node.c](https://github.com/GNOME/gnome-shell/blob/51.0/src/st/st-theme-node.c)
- [GNOME Shell 51.0 — st-theme-node.h](https://github.com/GNOME/gnome-shell/blob/51.0/src/st/st-theme-node.h)
- [St.ThemeNode — API 51](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/class.ThemeNode.html)
- [St.Theme — API 51](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/class.Theme.html)
- [St.Widget — API 51](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/class.Widget.html)

Le tag `51.0` est utilisé afin que les résultats soient reproductibles. Lors d'une mise à niveau de GNOME Shell, réexaminez le code source de St avant de réutiliser cette référence.
