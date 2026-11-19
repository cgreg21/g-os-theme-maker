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


## 15. Préparer une application de laboratoire GTK 4

Travaillez d'abord sur une application de test, pas sur toutes les applications de la session. Conservez une copie du thème de départ et modifiez une seule famille de composants à la fois.

Une organisation simple permet de séparer la feuille principale et les ressources :

~~~text
~/.themes/Theme-Laboratoire/
└── gtk-4.0/
    ├── gtk.css
    ├── gtk-dark.css
    └── assets/
~~~

Vérifiez que l'application utilise réellement GTK 4. Certaines applications possèdent plusieurs exécutables ou peuvent être distribuées dans un environnement isolé. La présence d'un dossier gtk-4.0 ne prouve pas que le processus le charge.

Lancez l'application depuis un terminal de test et conservez les avertissements CSS. Un thème peut sembler correct tout en produisant des erreurs qui ne concernent que des composants rarement affichés.

## 16. Comprendre les limites du thème GTK 4

GTK 4 a déplacé ou supprimé plusieurs responsabilités historiques. Les applications peuvent construire leurs interfaces avec des widgets personnalisés, des textures, des rendus dessinés ou des composants Libadwaita.

Avant de chercher un sélecteur, déterminez si l'élément est :
- un widget GTK avec un nœud CSS ;
- un widget personnalisé qui expose ses propres classes ;
- un contenu dessiné sans nœud CSS indépendant ;
- une ressource image ;
- une surface appartenant à un autre processus ou à un autre moteur.

Le CSS ne peut pas recolorer de manière fiable chaque pixel d'un contenu dessiné ou d'une image. Il ne remplace pas non plus la logique de disposition de l'application.

Si un composant ne réagit pas au thème, inspectez son arbre et ses ressources avant de multiplier les sélecteurs.

## 17. Atelier : ListView, GridView et ColumnView

Les vues GTK 4 réutilisent souvent leurs éléments. Le contenu visible peut être détruit puis reconstruit au fil du défilement. Une règle CSS doit donc rester correcte pour chaque élément réutilisé.

Préparez une liste contenant :
- des lignes simples ;
- des lignes avec icône ;
- un titre et un sous-titre ;
- des éléments désactivés ;
- une sélection ;
- une liste vide ;
- suffisamment d'éléments pour faire défiler le contenu.

Vérifiez ensuite :
1. Le rendu d'une ligne au repos.
2. Le survol si le composant l'expose.
3. La sélection au pointeur.
4. La sélection au clavier.
5. Le focus de la vue et celui de la ligne.
6. Le défilement jusqu'à la fin.
7. La réutilisation des lignes lors du défilement.
8. Les textes longs et les icônes absentes.

Pour GridView, ajoutez des cellules de proportions différentes et vérifiez l'alignement. Pour ColumnView, testez les en-têtes, le redimensionnement, le tri et les colonnes étroites.

N'imposez pas une hauteur fixe à toutes les lignes si leur contenu peut s'étendre. Une ligne contenant une description ou un libellé traduit peut nécessiter davantage d'espace.

## 18. Atelier : sélections et états des contrôles

Pour chaque bouton, case, interrupteur et contrôle de valeur, testez les états réellement accessibles dans l'application.

- normal ;
- survol ;
- pressé ;
- actif ou coché ;
- sélectionné ;
- focalisé au clavier ;
- désactivé ;
- en attente si le composant présente cet état.

Un état coché n'est pas nécessairement identique à un état pressé. Une sélection de ligne n'est pas nécessairement un focus clavier. Évitez de donner le même style à tous ces états.

Exemple de distinction :

~~~css
button:hover {
  background-color: #e8e6e3;
}

button:active {
  background-color: #d6d3d0;
}

button:focus {
  outline: 2px solid @accent;
  outline-offset: 2px;
}

button:disabled {
  opacity: 0.55;
}
~~~

Validez la prise en charge de chaque pseudo-classe avec la version GTK ciblée. Ne copiez pas les pseudo-classes de navigateur sans vérifier le moteur GTK.

## 19. Atelier : menus, popovers et modèles d'actions

Les menus GTK 4 peuvent être générés à partir de modèles. Leur contenu et leur structure ne sont pas nécessairement ceux d'un menu construit manuellement.

Testez :
- action simple ;
- action avec icône ;
- élément coché ;
- sous-menu ;
- séparateur ;
- raccourci affiché ;
- libellé long ;
- menu près du bord de la fenêtre ;
- menu ouvert après redimensionnement.

Contrôlez le focus, la sélection, le contraste et la fermeture. Vérifiez aussi les menus contextuels et les menus de barre d'en-tête, qui peuvent être construits par des chemins différents.

Un popover peut être repositionné automatiquement selon l'espace disponible. N'utilisez pas une marge ou une largeur fixe qui le ferait sortir de la fenêtre.

## 20. Comprendre l'interface adaptative

La mise en page responsive relève d'abord de l'application. Un thème peut ajuster les couleurs, bordures et espacements, mais il ne doit pas supposer qu'il peut convertir une navigation latérale en menu ou déplacer les contrôles.

Testez chaque application à plusieurs largeurs :
- fenêtre large ;
- fenêtre intermédiaire ;
- fenêtre étroite ;
- fenêtre très basse ;
- fenêtre maximisée ;
- fenêtre non maximisée.

À chaque largeur, vérifiez les titres, les barres d'en-tête, les panneaux latéraux, les listes, les boutons et les menus. Les libellés ne doivent pas se chevaucher et les contrôles ne doivent pas disparaître sous une surface.

Pour les composants qui changent de présentation, comparez les états avant et après le breakpoint. Une règle CSS ne doit pas supposer que le même descendant existe dans les deux présentations.

## 21. Tester le défilement et les contenus volumineux

Préparez des contenus plus longs que la fenêtre. Vérifiez que le défilement reste naturel et que les barres ou indicateurs ne masquent pas le contenu.

Scénarios :
- liste longue ;
- texte multiligne ;
- grille de nombreuses cellules ;
- vue avec plusieurs colonnes ;
- panneau latéral défilant ;
- fenêtre redimensionnée pendant le défilement.

Testez les orientations horizontale et verticale. Une barre de défilement trop fine ou trop transparente peut être difficile à repérer, mais une barre trop épaisse peut réduire la place utile.

Ne confondez pas le défilement d'un widget et celui de la fenêtre. Inspectez le conteneur qui possède réellement le défilement.

## 22. Tester les dialogues et les sélecteurs

Les dialogues peuvent provenir de GTK, de Libadwaita ou d'une implémentation spécifique à l'application. Identifiez leur origine avant de choisir les sélecteurs.

Pour un sélecteur de fichiers, contrôlez :
- emplacement courant ;
- barre latérale ;
- liste ou grille ;
- sélection d'un fichier ;
- sélection d'un dossier ;
- filtre de type ;
- nom de fichier ;
- boutons ouvrir et annuler ;
- état d'erreur ;
- navigation clavier.

Vérifiez les chemins longs, les noms accentués et les dossiers contenant beaucoup d'éléments. Un style de sélection doit rester visible dans la liste et la grille.

Pour un dialogue d'alerte, vérifiez le titre, le texte, l'ordre des actions, l'action par défaut et le focus. Les boutons destructifs doivent être identifiables et ne pas être confondus avec une confirmation neutre.

## 23. Diagnostic des règles qui ne s'appliquent pas

Quand une règle GTK 4 ne produit aucun effet, procédez par étapes :

1. Confirmez la version de GTK du processus.
2. Confirmez que le thème utilisateur est chargé.
3. Ouvrez le composant concerné dans l'inspecteur.
4. Sélectionnez le nœud CSS réel.
5. Relevez ses classes et ses parents.
6. Vérifiez les pseudo-classes dans l'état problématique.
7. Consultez les avertissements du moteur.
8. Testez une propriété simple et évidente.
9. Recherchez les fournisseurs ajoutés par l'application.
10. Retirez la règle temporaire après le diagnostic.

Un nom de classe C n'est pas automatiquement un sélecteur CSS. De même, le nom d'une propriété GTK 3 n'est pas une garantie de compatibilité GTK 4.

Si l'inspecteur ne permet pas d'examiner un élément dessiné, cherchez le point d'entrée dans le code de l'application. Il peut ne pas exister de nœud CSS modifiable.

## 24. Vérifier les variantes claires et sombres

Testez les deux variantes sur les mêmes composants et avec les mêmes données. Les contrôles qui semblent corrects sur une fenêtre claire peuvent devenir invisibles dans un dialogue sombre.

Vérifiez séparément :
- surfaces de fenêtre et de contenu ;
- headerbar ;
- cartes ;
- popovers ;
- sélection ;
- focus ;
- texte secondaire ;
- icônes ;
- avertissements et erreurs ;
- champs désactivés ;
- infobulles.

Si une application choisit sa variante en fonction de la préférence système, testez le changement réel de préférence et le redémarrage éventuel du processus. Ne supposez pas que toutes les applications basculent instantanément.

## 25. Vérifier l'accessibilité et les langues

Parcourez les interfaces au clavier. Vérifiez que le focus reste visible et que les contrôles ne dépendent pas uniquement du survol.

Testez également :
- texte agrandi ;
- contraste renforcé lorsque disponible ;
- navigation au clavier sans souris ;
- libellés longs ;
- accents et caractères non latins ;
- langue RTL ;
- boutons et icônes directionnels ;
- dialogues contenant du texte long.

Ne retournez pas toutes les icônes en RTL. Seules les icônes dont le sens est directionnel doivent être adaptées.

Le CSS ne corrige pas un nom accessible manquant, un rôle erroné ou un ordre de navigation incohérent. Ces problèmes doivent être corrigés dans le widget ou l'application.

## 26. Fiche de validation GTK 4

~~~text
Application et version :
Version GTK observée :
Version Libadwaita éventuelle :
Distribution et session :
Thème et variante :
Fournisseurs CSS propres à l'application :
Fenêtre et headerbar :
Boutons et contrôles :
ListView :
GridView :
ColumnView :
Menus et popovers :
Navigation adaptative :
Défilement :
Dialogues et sélecteurs :
États de focus et sélection :
Clavier et accessibilité :
Langue et RTL :
Avertissements CSS :
Sélecteurs et propriétés modifiés :
Captures de référence :
Anomalies :
Conclusion : validé / partiel / à corriger
~~~

Une validation sérieuse doit couvrir plusieurs applications GTK 4. Le même moteur CSS peut être utilisé par des interfaces très différentes ; ne généralisez pas un sélecteur observé dans une seule application.

## 27. Ouvrir l'inspecteur GTK 4 et isoler une règle

Lorsque l'application accepte l'inspecteur GTK, vous pouvez le demander au démarrage sans modifier sa configuration permanente :

~~~bash
GTK_DEBUG=interactive nom_application
~~~

Remplacez `nom_application` par la commande réelle de l'application. Cette variable ne fonctionne que si le programme utilise GTK et si l'inspecteur est disponible dans sa construction. Si l'application est déjà ouverte, fermez-la puis relancez-la depuis le terminal pour que la variable soit prise en compte.

Pour une application Flatpak, transmettez la variable à l'environnement du bac à sable :

~~~bash
flatpak run --env=GTK_DEBUG=interactive identifiant.application
~~~

Remplacez l'identifiant par celui du paquet installé. Si l'inspecteur n'apparaît pas, vérifiez d'abord que le programme utilise GTK 4, que la variable a été transmise au bon processus et que la version distribuée autorise l'inspection. L'absence de l'inspecteur ne prouve pas que le CSS utilisateur est ignoré.

Dans l'inspecteur :

1. Sélectionnez le widget dans l'arbre des objets.
2. Repérez le nœud CSS correspondant, ses classes et ses ancêtres.
3. Examinez les propriétés calculées et les règles concurrentes.
4. Activez l'état pertinent lorsque l'inspecteur le permet ; sinon, reproduisez-le dans l'interface.
5. Modifiez une seule déclaration temporaire et observez précisément le résultat.
6. Retirez l'essai, puis reportez uniquement la règle validée dans le thème.

Pour un diagnostic fiable, consignez la version GTK, le nom du processus, le nœud CSS, les classes, l'état observé et le fournisseur qui gagne la cascade. Une capture de l'inspecteur seule ne remplace pas ces informations : le même widget peut changer d'arbre ou de classes selon l'application et son état.

N'activez pas l'inspecteur ou les variables de débogage globalement pour toute la session. Lancez uniquement l'application concernée avec l'environnement de diagnostic, puis fermez-la à la fin du test.
