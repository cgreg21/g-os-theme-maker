# Personnaliser GTK 4 : listes, vues, contrôles et composants adaptatifs

GTK 4 conserve un moteur CSS, mais son arbre de widgets et ses composants ont évolué par rapport à GTK 3. Un sélecteur GTK 3 ne doit jamais être recopié sans vérification dans un thème GTK 4.

Ce chapitre explique comment lire les nœuds CSS et personnaliser les familles de composants GTK 4 les plus courantes.

## 1. Différences importantes avec GTK 3

GTK 4 a fait évoluer plusieurs widgets et leur structure :

- GtkTreeView est remplacé, dans les nouveaux développements, par GtkListView, GtkGridView et GtkColumnView.
- Les conteneurs ont été simplifiés et certains widgets historiques ont disparu ou changé.
- Le rendu et les surfaces de fenêtres ont évolué.
- Certaines propriétés CSS et variables personnalisées dépendent de la version GTK 4.

Le nom de la classe API n'est pas nécessairement le nom du nœud CSS. Il faut inspecter le widget réel.

## 2. Palette et couleurs

Les couleurs nommées restent utilisables pour structurer une feuille de style.

~~~css
@define-color window_bg #f6f5f4;
@define-color window_fg #241f31;
@define-color view_bg #ffffff;
@define-color view_fg #241f31;
@define-color accent #3584e4;
@define-color border #deddda;

window,
.background {
  background-color: @window_bg;
  color: @window_fg;
}

.view {
  background-color: @view_bg;
  color: @view_fg;
}
~~~

GTK 4.16 et les versions ultérieures prennent en charge les propriétés personnalisées et var(). Ne supposez pas que ces mécanismes sont disponibles dans GTK 4.0 à 4.15.

## 3. Fenêtres et barres d'en-tête

Les fenêtres utilisent notamment window et .background. Les barres d'en-tête utilisent headerbar.

~~~css
window,
.background {
  background-color: @window_bg;
  color: @window_fg;
}

headerbar {
  background-color: #ffffff;
  color: @window_fg;
  border-bottom: 1px solid @border;
  padding: 6px;
}

headerbar .title {
  font-weight: 700;
}
~~~

Une application peut utiliser une décoration côté client, une barre d'en-tête personnalisée ou une barre d'outils. Le thème GTK ne peut pas forcer toutes les applications à partager la même structure.

## 4. Boutons, cases et interrupteurs

Les boutons utilisent button. Les cases, radios et interrupteurs possèdent leurs propres nœuds ou classes.

~~~css
button {
  border-radius: 8px;
  padding: 6px 12px;
}

button:hover {
  background-color: #e8e6e3;
}

button:active,
button:checked {
  background-color: #d6d3d0;
}

button:focus {
  outline: 2px solid @accent;
  outline-offset: 2px;
}

checkbutton,
radiobutton,
switch {
  min-width: 20px;
  min-height: 20px;
}
~~~

Inspectez chaque contrôle avant d'ajouter des styles descendants. Les parties internes du widget ne sont pas nécessairement identiques entre les versions.

## 5. Champs et recherche

Les champs les plus courants sont entry, text, textview et searchentry selon les widgets utilisés.

~~~css
entry,
searchentry {
  background-color: @view_bg;
  color: @view_fg;
  border: 1px solid @border;
  border-radius: 8px;
  padding: 7px 10px;
}

entry:focus,
searchentry:focus {
  border-color: @accent;
}

textview text {
  background-color: @view_bg;
  color: @view_fg;
}
~~~

Vérifiez le placeholder, la sélection de texte, le curseur, les erreurs et les champs désactivés. Le contraste du texte sélectionné doit rester suffisant.

## 6. ListView, GridView et ColumnView

GTK 4 fournit plusieurs vues de données :

- GtkListView pour une liste verticale ou horizontale ;
- GtkGridView pour une grille ;
- GtkColumnView pour une vue en colonnes.

Les noms de nœuds et les classes peuvent inclure listview, gridview, columnview, row, header et cell. Le widget peut aussi exposer des classes de style ajoutées par l'application.

~~~css
listview,
gridview,
columnview {
  background-color: @view_bg;
  color: @view_fg;
}

row {
  padding: 8px 10px;
}

row:selected {
  background-color: @accent;
  color: #ffffff;
}

columnview header {
  background-color: @window_bg;
  color: @window_fg;
}
~~~

Cet exemple est volontairement générique. Vérifiez les nœuds et les états avec l'inspecteur GTK avant de l'utiliser. Les classes API GtkListView et GtkColumnView ne garantissent pas à elles seules la présence de ces sélecteurs dans tous les descendants.

Testez une liste vide, une liste longue, une sélection multiple, une ligne avec icône et une ligne avec description.

## 7. Menus et popovers

Les menus GTK 4 utilisent généralement popover et les variantes associées.

~~~css
popover,
popover.background {
  background-color: @view_bg;
  color: @view_fg;
  border: 1px solid @border;
  border-radius: 12px;
}

popover modelbutton {
  border-radius: 7px;
  padding: 7px 10px;
}

popover modelbutton:hover {
  background-color: rgba(53, 132, 228, 0.14);
}
~~~

Vérifiez les menus imbriqués, les cases, les raccourcis, les séparateurs et la navigation clavier. Les menus peuvent être construits par un modèle et ne pas correspondre à une hiérarchie de widgets habituelle.

## 8. Progression et contrôles de valeur

Les familles de contrôles comprennent scale, progressbar, levelbar, spinner, scrollbar et spinbutton.

~~~css
scale trough,
progressbar trough,
levelbar trough {
  border-radius: 999px;
  background-color: #deddda;
}

scale highlight,
progressbar progress,
levelbar block.filled {
  border-radius: 999px;
  background-color: @accent;
}

scrollbar slider {
  border-radius: 999px;
  min-width: 8px;
  min-height: 8px;
}
~~~

Les curseurs doivent rester manipulables à la souris, au clavier et au tactile. Vérifiez les valeurs extrêmes, l'orientation et le focus.

## 9. Défilement, conteneurs et séparateurs

GtkScrolledWindow, GtkScrollbar, GtkBox, GtkGrid, GtkPaned, GtkStack, GtkOverlay, GtkFrame et GtkSeparator structurent les interfaces.

Personnalisez les fonds et les séparateurs avec prudence. Un style trop large sur box ou frame peut modifier des zones sans rapport dans toute l'application. Préférez les classes de style dédiées ajoutées par le composant ou l'application.

## 10. Dialogues et sélecteurs de fichiers

Les dialogues GTK 4 peuvent utiliser GtkDialog, GtkFileChooserDialog, GtkAlertDialog ou des dialogues natifs. Leur rendu dépend aussi de la version de GTK et de la plateforme.

Testez :
- titre et description ;
- boutons de confirmation et d'annulation ;
- focus clavier ;
- erreurs et avertissements ;
- sélection de fichiers ;
- barre latérale et liste de fichiers ;
- contenu long et défilement.

Ne supposez pas qu'un dialogue Libadwaita utilise les mêmes nœuds qu'un GtkDialog standard.

## 11. Variables personnalisées GTK 4.16+

Depuis GTK 4.16, les propriétés CSS personnalisées peuvent faciliter la réutilisation des valeurs.

~~~css
:root {
  --theme-surface: #ffffff;
  --theme-text: #241f31;
  --theme-accent: #3584e4;
}

window {
  background-color: var(--theme-surface);
  color: var(--theme-text);
}

button.suggested-action {
  background-color: var(--theme-accent);
}
~~~

Pour une application utilisant GTK 4.0 à 4.15, préférez les couleurs nommées compatibles et vérifiez la documentation de la version.

## 12. Méthode d'inspection

1. Lancez l'application.
2. Ouvrez l'inspecteur GTK si l'application et la version le permettent.
3. Sélectionnez le widget à personnaliser.
4. Notez son nom de nœud, ses classes et ses états.
5. Repérez les règles CSS qui s'appliquent.
6. Écrivez une règle courte dans une feuille de test.
7. Vérifiez les erreurs et le résultat sur plusieurs tailles de fenêtre.

Ne créez pas une règle sur la base du seul nom de la classe C. Les nœuds CSS sont la référence pour le sélecteur.

## 13. Exercices

### Exercice A — fenêtre

Personnalisez le fond, la barre d'en-tête et le titre d'une application GTK 4.

### Exercice B — liste

Modifiez l'état sélectionné d'une ListView et vérifiez la navigation clavier.

### Exercice C — popover

Personnalisez un menu et vérifiez les sous-menus, séparateurs et raccourcis.

### Exercice D — responsive

Réduisez la largeur de la fenêtre et vérifiez que les contrôles restent accessibles.

## 14. Références

- [Vue d'ensemble CSS GTK 4](https://docs.gtk.org/gtk4/css-overview.html)
- [Référence GTK 4](https://docs.gtk.org/gtk4/)
- [Nouveautés GTK 4](https://docs.gtk.org/gtk4/migrating-3to4.html)
