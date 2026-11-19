# Comprendre et personnaliser la vue Activités de GNOME Shell 51

Ce chapitre explique la vue d'ensemble affichée avec la touche Super ou le bouton Activités. Il distingue les fenêtres, les espaces de travail, la recherche, le Dash et la grille d'applications. Les repères CSS ci-dessous ont été vérifiés dans les sources amont GNOME Shell **51.0**. Ils décrivent l'implémentation de cette version, pas une API stable.

![Capture de l'interface GNOME montrant le Dash](https://help.gnome.org/gnome-help/figures/shell-activities-dash.png)

Sources amont :
- [overview.js](https://github.com/GNOME/gnome-shell/blob/51.0/js/ui/overview.js)
- [overviewControls.js](https://github.com/GNOME/gnome-shell/blob/51.0/js/ui/overviewControls.js)
- [workspacesView.js](https://github.com/GNOME/gnome-shell/blob/51.0/js/ui/workspacesView.js)
- [workspace.js](https://github.com/GNOME/gnome-shell/blob/51.0/js/ui/workspace.js)
- [workspaceThumbnail.js](https://github.com/GNOME/gnome-shell/blob/51.0/js/ui/workspaceThumbnail.js)
- [dash.js](https://github.com/GNOME/gnome-shell/blob/51.0/js/ui/dash.js)
- [appDisplay.js](https://github.com/GNOME/gnome-shell/blob/51.0/js/ui/appDisplay.js)
- [SCSS du Dash](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_dash.scss)
- [SCSS de la grille d'applications](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_app-grid.scss)
- [SCSS des fenêtres](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_window-picker.scss)
- [SCSS de la recherche](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_search-entry.scss)

## 1. La vue Activités n'est pas une fenêtre ordinaire

La vue Activités est une interface du Shell, construite avec St et Clutter. Elle affiche des acteurs représentant les fenêtres, les espaces de travail et les lanceurs. Les fenêtres visibles sont des aperçus des fenêtres existantes : ce ne sont pas des captures d'écran statiques à décorer indépendamment.

Dans GNOME Shell 51.0, `overview.js` instancie un `OverviewActor` et lui associe un `ControlsManager`. Ce dernier assemble les contrôles et les différentes vues. Le CSS change l'apparence des acteurs présents, mais ne réorganise pas à lui seul les interactions ou la logique de navigation.

## 2. Comprendre les zones visuelles

La capture permet de repérer les grandes zones :

- **Panneau supérieur** : reste présent dans la vue et adopte un état de style particulier.
- **Recherche** : champ central permettant de lancer une recherche et d'afficher les résultats des fournisseurs.
- **Aperçus de fenêtres** : représentations interactives des fenêtres du bureau courant.
- **Espaces de travail** : miniatures latérales qui permettent de choisir un bureau et de déplacer des fenêtres.
- **Dash** : barre de favoris et d'applications en cours.
- **Afficher les applications** : bouton du Dash qui ouvre la grille d'applications.

La disposition réelle dépend de la résolution, du nombre de fenêtres, du nombre d'espaces de travail, du nombre d'écrans et de l'état courant de la vue.

## 3. Fond de la vue : `#overviewGroup`

Le SCSS de GNOME Shell 51.0 déclare :

```css
#overviewGroup
```

Ce conteneur reçoit le fond de la vue. Il ne faut pas le confondre avec le fond du bureau, ni avec le fond des fenêtres miniatures.

Exemple :

```css
#overviewGroup {
  background-color: #202735;
}
```

Ce changement est volontairement simple. Si le fond du bureau reste visible ou si un effet de flou est appliqué, cela dépend aussi des acteurs de fond et de la transition pilotés par le Shell. Une couleur CSS sur `#overviewGroup` ne remplace pas la logique d'arrière-plan.

## 4. La recherche : `.search-entry`

Le champ de recherche est créé par `overviewControls.js` avec la classe `search-entry`. Le fichier SCSS correspondant définit sa largeur, ses marges, ses coins arrondis et l'icône interne `.search-entry-icon`.

Exemple :

```css
.search-entry {
  width: 28em;
  border-radius: 999px;
  margin-top: 12px;
  margin-bottom: 8px;
  padding: 8px 14px;
}

.search-entry .search-entry-icon {
  icon-size: 18px;
}
```

La largeur est exprimée en em pour suivre l'échelle typographique. Évitez de fixer une largeur en pixels qui devient trop grande ou trop petite avec une autre échelle d'affichage.

### Les résultats de recherche

Les résultats ne sont pas un simple texte dans le champ. Le code de `search.js` crée des sections et des éléments distincts. Les classes présentes dans le code 51.0 comprennent notamment :

- `.search-display` : conteneur des résultats ;
- `.search-section` : section d'un fournisseur ;
- `.search-section-separator` : séparation entre sections ;
- `.search-section-content` : contenu d'une section ;
- `.list-search-results` : résultats sous forme de liste ;
- `.grid-search-results` : résultats sous forme de grille ;
- `.list-search-result-title` : titre d'un résultat ;
- `.list-search-result-description` : description ;
- `.search-provider-icon` : icône du fournisseur.

Exemple de style léger :

```css
.search-section {
  border-radius: 12px;
  padding: 8px;
}

.list-search-result-title {
  font-weight: 700;
}

.list-search-result-description {
  color: #c7cbd3;
}
```

Ces règles peuvent affecter plusieurs fournisseurs. Vérifiez la lisibilité des descriptions longues et la sélection au clavier. Le thème ne décide pas quels fournisseurs sont installés ni quels résultats ils renvoient.

## 5. Les aperçus de fenêtres : `.window-picker`

Le code de `workspace.js` crée les aperçus de fenêtres. La feuille SCSS `_window-picker.scss` contient les sélecteurs :

- `.window-picker` : zone de présentation des fenêtres ;
- `.window-icon` : icône associée à une fenêtre ;
- `.window-caption` : titre affiché avec l'aperçu ;
- `.window-close` : bouton de fermeture ;
- `.workspace-background` : fond du bureau représenté.

Exemple :

```css
.window-picker {
  spacing: 18px;
}

.window-caption {
  color: #ffffff;
  font-weight: 600;
}

.window-close {
  border-radius: 999px;
}
```

Le moteur St n'implémente pas toutes les propriétés CSS du navigateur. La propriété `spacing` s'applique aux conteneurs St concernés ; elle n'est pas une propriété CSS web générique.

Les aperçus ont des états de survol, de sélection et de focus. Vérifiez le bouton de fermeture, le clic sur l'aperçu, le déplacement par glisser-déposer et la navigation au clavier. N'augmentez pas trop les marges : le gestionnaire de disposition calcule la taille des aperçus selon l'espace disponible.

## 6. Les miniatures d'espaces de travail

Le code de `workspaceThumbnail.js` crée les miniatures et leur conteneur. Les classes repérées dans GNOME Shell 51.0 sont :

- `.workspace-thumbnails` : conteneur de la colonne de miniatures ;
- `.workspace-thumbnail` : miniature individuelle ;
- `.workspace-thumbnail-indicator` : indicateur de l'espace actif ;
- `.placeholder` : emplacement temporaire pendant certaines opérations de déplacement.

Exemple :

```css
.workspace-thumbnails {
  spacing: 12px;
}

.workspace-thumbnail {
  border-radius: 10px;
}

.workspace-thumbnail-indicator {
  border: 2px solid #78aeed;
  border-radius: 12px;
}
```

Ne confondez pas les miniatures latérales avec les grandes surfaces d'espaces de travail qui contiennent les aperçus de fenêtres. Elles sont construites par des classes différentes et leur taille est calculée par le code.

Testez un, deux puis plusieurs espaces de travail. Vérifiez le changement de bureau, le glisser-déposer d'une fenêtre, l'ajout et la suppression dynamique de bureaux et la présence de plusieurs écrans.

## 7. Le Dash : `#dash`

Le Dash est la barre des applications favorites et des applications ouvertes. Le SCSS de GNOME Shell 51.0 définit `#dash`, `.dash-background`, `.dash-item-container`, `.dash-separator` et `.dash-label`.

Exemple :

```css
#dash .dash-background {
  background-color: rgba(24, 28, 36, 0.92);
  border-radius: 20px;
  padding: 12px;
}

#dash .dash-separator {
  background-color: rgba(255, 255, 255, 0.25);
  width: 1px;
}

#dash .dash-label {
  border-radius: 8px;
}
```

Les éléments du Dash utilisent aussi `.overview-tile` et `.overview-icon`. Le SCSS cible explicitement les états `:focus`, `:hover`, `:active` et `:checked`. Il faut donc personnaliser les quatre états, pas seulement l'apparence normale.

```css
#dash .overview-tile:hover .overview-icon {
  background-color: rgba(255, 255, 255, 0.12);
}

#dash .overview-tile:focus .overview-icon {
  outline: 2px solid #78aeed;
  outline-offset: 2px;
}

#dash .overview-tile:active .overview-icon,
#dash .overview-tile:checked .overview-icon {
  background-color: rgba(120, 174, 237, 0.25);
}
```

Le point d'application en cours est représenté par `.app-grid-running-dot`. Il ne faut pas le confondre avec le point d'espace de travail du panneau.

## 8. La grille d'applications

La grille utilise la classe `.icon-grid`. Le SCSS natif lui applique des propriétés St spécifiques :

- `row-spacing` et `column-spacing` pour l'espacement entre les icônes ;
- `max-row-spacing` et `max-column-spacing` pour les limites d'espacement ;
- `page-padding-top`, `page-padding-bottom`, `page-padding-left` et `page-padding-right` pour les marges de page.

Exemple :

```css
.icon-grid {
  row-spacing: 24px;
  column-spacing: 28px;
  max-row-spacing: 40px;
  max-column-spacing: 44px;
  page-padding-top: 28px;
  page-padding-bottom: 28px;
  page-padding-left: 24px;
  page-padding-right: 24px;
}
```

Les icônes et tuiles utilisent notamment `.overview-tile`, `.overview-icon`, `.app-folder`, `.app-grid-running-dot`, `.page-indicator` et `.page-navigation-arrow`.

Exemple :

```css
.overview-tile {
  border-radius: 18px;
  padding: 12px;
}

.overview-tile .overview-icon {
  icon-size: 64px;
}

.app-folder {
  border-radius: 18px;
}

.page-indicator .page-indicator-icon {
  border-radius: 999px;
}
```

Le dimensionnement réel des icônes peut aussi dépendre du code de grille et de l'espace disponible. Une taille très élevée peut provoquer des pages supplémentaires et des déplacements inattendus.

## 9. Les dossiers d'applications

Les dossiers sont ciblés par `.app-folder`. Leur fenêtre développée utilise `.app-folder-dialog` et son conteneur `.app-folder-dialog-container`. Le nom du dossier est géré par `.folder-name-container`, `.folder-name-label` et `.folder-name-entry`.

Exemple :

```css
.app-folder-dialog {
  border-radius: 24px;
  background-color: #292e38;
  color: #f6f5f4;
}

.app-folder-dialog .folder-name-container {
  padding: 24px 32px;
}
```

Le nom et le contenu du dossier sont gérés par les paramètres du Shell. Le CSS ne crée pas de dossier et ne modifie pas l'ordre des applications.

## 10. Les propriétés St qui ne sont pas du CSS de navigateur

La grille d'applications utilise des propriétés propres aux widgets St. Les propriétés `row-spacing`, `column-spacing`, `max-row-spacing`, `page-padding-*` et `icon-size` doivent être vérifiées dans la documentation St correspondant à GNOME Shell 51.

Une feuille qui passe dans un validateur CSS web peut signaler ces propriétés comme inconnues. Cela ne signifie pas qu'elles sont invalides dans St. Inversement, une propriété CSS web acceptée par un navigateur n'est pas nécessairement implémentée par St.

## 11. Méthode d'essai progressive

1. Sauvegardez le thème fonctionnel.
2. Modifiez uniquement le fond de `#overviewGroup`.
3. Ouvrez Activités et contrôlez le contraste.
4. Modifiez la largeur et les marges de `.search-entry`.
5. Ouvrez une recherche avec plusieurs fournisseurs.
6. Ajoutez deux fenêtres puis quatre fenêtres.
7. Testez le titre, la fermeture et le focus des aperçus.
8. Ajoutez plusieurs espaces de travail.
9. Personnalisez le Dash et les états des tuiles.
10. Ouvrez la grille, changez de page et ouvrez un dossier.
11. Répétez à 100 %, 150 % et 200 % d'échelle si disponible.
12. Répétez en session claire, sombre et contraste élevé.

## 12. Problèmes fréquents

**La recherche ne change pas.** Vérifiez que le sélecteur est `.search-entry`, puis inspectez le champ réel. Le style du champ et celui des résultats sont deux parties différentes.

**Les fenêtres débordent.** Réduisez les espacements et les marges. Ne forcez pas des dimensions fixes sur chaque aperçu.

**Les miniatures sont minuscules.** La taille est calculée par le Shell en fonction de l'écran et du nombre de bureaux. Commencez par les espacements et les bordures avant de chercher à forcer la géométrie.

**Le Dash perd son focus.** Contrôlez `:focus` sur la tuile et son enfant `.overview-icon`. Le style du conteneur seul ne suffit pas.

**La grille affiche plusieurs pages.** Le nombre de pages dépend de l'espace disponible, du nombre d'applications et de la géométrie de la grille.

## 13. Exercices

### Exercice A — vue lisible

Changez le fond de la vue, la largeur de recherche et le style du champ. Testez une recherche réelle et le déplacement au clavier.

### Exercice B — fenêtres

Ouvrez trois applications. Personnalisez les titres, le bouton de fermeture et les espacements. Déplacez une fenêtre vers un autre espace de travail.

### Exercice C — Dash

Modifiez le fond, les coins, le séparateur et les états des icônes. Vérifiez que les applications favorites et les applications ouvertes restent identifiables.

### Exercice D — grille

Modifiez les espacements de grille, le style des dossiers et les indicateurs de page. Testez une grille remplie et une grille avec peu d'applications.

## 14. Limites et règles de maintenance

- Les sélecteurs décrivent GNOME Shell 51.0 et peuvent évoluer.
- Une extension peut remplacer le Dash ou ajouter ses propres classes.
- Les thèmes Shell ne stylent pas automatiquement les fenêtres GTK et Libadwaita.
- Les écrans de connexion et de verrouillage ont des contextes et privilèges distincts.
- Les effets de transition et la géométrie sont contrôlés en partie par JavaScript.
- Ne masquez pas les repères de focus et ne réduisez pas les cibles interactives à des tailles difficiles à utiliser.

Pour chaque nouvelle version de GNOME, comparez les fichiers SCSS et JavaScript amont avant de réutiliser les sélecteurs.
