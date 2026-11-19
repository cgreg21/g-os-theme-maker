# Personnaliser GTK 3 : fenêtres, listes, menus et widgets historiques

GTK 3 reste utilisé par de nombreuses applications, y compris des applications GNOME anciennes et des outils tiers. Son thème CSS est distinct de celui de GNOME Shell et de GTK 4.

Ce chapitre propose une méthode pratique pour personnaliser les composants GTK 3. Les nœuds CSS dépendent du widget et de sa version : inspectez toujours l'arbre réel avant de créer une règle spécifique.

## 1. Où placer les fichiers du thème

Un thème GTK 3 utilisateur peut être organisé ainsi :

~~~text
~/.themes/MonTheme/
└── gtk-3.0/
    ├── gtk.css
    ├── gtk-dark.css
    └── assets/
~~~

Le fichier gtk.css contient le style principal. gtk-dark.css peut fournir des règles spécifiques à la variante sombre. Le thème doit être installé dans le répertoire utilisateur pour éviter de modifier les fichiers système.

Le nom du thème et sa disponibilité dépendent de la configuration GNOME et de la distribution. Le CSS GTK 3 n'est pas chargé par GNOME Shell.

## 2. Palette de couleurs

GTK 3 utilise des couleurs nommées avec @define-color. Définissez d'abord une palette cohérente, puis réutilisez ces noms dans les composants.

~~~css
@define-color theme_bg_color #f6f5f4;
@define-color theme_fg_color #241f31;
@define-color theme_base_color #ffffff;
@define-color theme_text_color #241f31;
@define-color theme_selected_bg_color #3584e4;
@define-color theme_selected_fg_color #ffffff;
@define-color borders #deddda;
@define-color insensitive_fg_color #77767b;
~~~

Les noms traditionnels theme_bg_color et theme_fg_color sont courants dans GTK 3, mais une application peut utiliser ses propres couleurs. Ne supposez pas qu'une seule variable couvre toutes les surfaces.

## 3. Fenêtres et arrière-plans

Les nœuds window et .background représentent les surfaces principales.

~~~css
window,
.background {
  background-color: @theme_bg_color;
  color: @theme_fg_color;
}

window:backdrop {
  background-color: #eeeeec;
}
~~~

L'état backdrop correspond à une fenêtre inactive. Il doit rester lisible, sans donner l'impression que son contenu est désactivé.

## 4. Barres d'en-tête et titres

Les barres d'en-tête utilisent généralement headerbar et .titlebar. Les applications peuvent ajouter des classes pour leurs variantes.

~~~css
headerbar,
headerbar.titlebar {
  background-color: #ffffff;
  color: @theme_fg_color;
  border-bottom: 1px solid @borders;
  padding: 6px;
}

headerbar .title {
  font-weight: 700;
}
~~~

Ne supposez pas que toutes les fenêtres ont une headerbar. Certaines applications utilisent une barre d'outils classique ou une décoration de fenêtre différente.

## 5. Boutons et actions

Les boutons utilisent button. Les classes .flat, .suggested-action et .destructive-action permettent de distinguer les usages.

~~~css
button {
  background-color: #ffffff;
  color: @theme_fg_color;
  border: 1px solid @borders;
  border-radius: 8px;
  padding: 6px 12px;
}

button:hover {
  background-color: #f0efed;
}

button:active,
button:checked {
  background-color: #deddda;
}

button:focus {
  outline: 2px solid @theme_selected_bg_color;
  outline-offset: 2px;
}

button:disabled {
  color: @insensitive_fg_color;
}

button.suggested-action {
  background-color: @theme_selected_bg_color;
  color: @theme_selected_fg_color;
  border-color: @theme_selected_bg_color;
}

button.destructive-action {
  background-color: #c01c28;
  color: #ffffff;
}
~~~

Une action suggérée et une action destructive doivent être immédiatement différenciables. Conservez les états hover, active, focus, checked et disabled.

## 6. Champs de saisie et vues de texte

Les champs courants utilisent entry, textview et spinbutton. Le contenu d'une vue texte peut nécessiter un sélecteur descendant text.

~~~css
entry,
spinbutton {
  background-color: @theme_base_color;
  color: @theme_text_color;
  border: 1px solid @borders;
  border-radius: 7px;
  padding: 6px 8px;
}

entry:focus,
spinbutton:focus {
  border-color: @theme_selected_bg_color;
}

textview text {
  background-color: @theme_base_color;
  color: @theme_text_color;
}
~~~

Vérifiez les champs de recherche, de mot de passe, les champs numériques et les champs intégrés à une barre d'en-tête. Certains possèdent des classes spécifiques.

## 7. Listes et GtkTreeView

GTK 3 utilise encore GtkTreeView dans de nombreuses applications. Le nœud CSS courant est treeview.view.

~~~css
treeview.view {
  background-color: @theme_base_color;
  color: @theme_text_color;
}

treeview.view:selected {
  background-color: @theme_selected_bg_color;
  color: @theme_selected_fg_color;
}

treeview.view header button {
  background-color: @theme_bg_color;
  border-radius: 0;
}
~~~

Une liste peut contenir des lignes, des colonnes, des en-têtes triables, des icônes et des cellules éditables. Vérifiez le survol, la sélection, le focus, les lignes alternées et les colonnes étroites.

Ne remplacez pas les styles de toutes les listes avec une règle trop large si l'application contient une vue arborescente, une liste de fichiers et une liste de préférences.

## 8. Onglets GTK 3

GtkNotebook utilise notebook et ses onglets sont exposés sous header et tab.

~~~css
notebook > header {
  background-color: @theme_bg_color;
  border-bottom: 1px solid @borders;
}

notebook > header tab {
  padding: 8px 12px;
}

notebook > header tab:checked {
  color: @theme_selected_bg_color;
  border-bottom: 2px solid @theme_selected_bg_color;
}
~~~

Les onglets peuvent être positionnés en haut, en bas, à gauche ou à droite. Vérifiez chaque orientation et les onglets qui débordent.

## 9. Menus, popovers et infobulles

Les menus traditionnels et les popovers ne sont pas la même chose. Ils peuvent avoir des nœuds CSS distincts.

~~~css
menu,
.menu {
  background-color: @theme_base_color;
  color: @theme_text_color;
  border: 1px solid @borders;
}

menuitem {
  padding: 6px 10px;
}

menuitem:hover {
  background-color: @theme_selected_bg_color;
  color: @theme_selected_fg_color;
}

popover,
popover.background {
  background-color: @theme_base_color;
  color: @theme_text_color;
  border: 1px solid @borders;
  border-radius: 12px;
}

tooltip {
  background-color: #242424;
  color: #ffffff;
}
~~~

Les menus peuvent contenir des cases, des radios, des raccourcis, des icônes et des sous-menus. Vérifiez la lisibilité des raccourcis et les états sélectionnés.

## 10. Curseurs, barres de progression et défilement

Les widgets de valeur utilisent des nœuds spécifiques.

~~~css
scale trough,
progressbar trough,
levelbar trough {
  background-color: #deddda;
  border-radius: 999px;
}

scale highlight,
progressbar progress,
levelbar block.filled {
  background-color: @theme_selected_bg_color;
  border-radius: 999px;
}

scrollbar slider {
  background-color: #9a9996;
  border-radius: 999px;
  min-width: 8px;
  min-height: 8px;
}
~~~

La structure interne varie selon le widget et l'orientation. Inspectez scale, progressbar, levelbar et scrollbar séparément. Ne supprimez pas les poignées ni les zones de saisie.

## 11. Infobars et messages

GtkInfoBar expose généralement infobar et des classes sémantiques telles que .info, .warning, .error ou .question.

~~~css
infobar {
  border-radius: 8px;
  padding: 8px;
}

infobar.warning {
  background-color: #f9f06b;
  color: #241f31;
}

infobar.error {
  background-color: #c01c28;
  color: #ffffff;
}
~~~

Les messages doivent conserver leur texte et leur icône. La couleur seule ne suffit pas à signaler une erreur.

## 12. Sélecteur de fichiers

Le sélecteur de fichiers peut afficher une barre latérale, une liste, une grille, un chemin et un aperçu. Les nœuds exacts dépendent de la version de GTK et du mode de présentation.

Ne ciblez pas tout le sélecteur avec une règle window générique. Inspectez les éléments réellement exposés, puis personnalisez séparément la barre latérale, les fichiers, la sélection et les boutons.

## 13. Vérifier et diagnostiquer

- Lancez l'application avec GTK_DEBUG=interactive si elle prend en charge l'inspecteur GTK.
- Repérez le nœud CSS, ses classes et ses états.
- Vérifiez les avertissements CSS dans le terminal.
- Testez la variante claire et la variante sombre.
- Comparez une application GTK 3 et une application GTK 4 : leurs styles ne sont pas interchangeables.

Exemple de lancement avec une feuille de thème de test :

~~~bash
GTK_THEME=Adwaita:dark nom-de-lapplication
~~~

GTK_THEME force un thème GTK pour le processus de test. Il ne garantit pas que l'application ignore ses styles internes.

## 14. Exercices

1. Créez une palette avec @define-color.
2. Personnalisez une fenêtre, une headerbar et ses boutons.
3. Personnalisez une TreeView avec un état sélectionné visible.
4. Ajoutez un focus visible à un champ.
5. Testez un menu, un popover et une infobulle.
6. Vérifiez les états inactifs et les messages d'erreur.

## 15. Références

- [Vue d'ensemble CSS GTK 3](https://docs.gtk.org/gtk3/css-overview.html)
- [Référence des widgets GTK 3](https://docs.gtk.org/gtk3/)
- [Inspecteur GTK](https://docs.gtk.org/gtk3/running.html)


## 16. Construire un environnement de test GTK 3 isolé

Ne commencez pas par remplacer le thème utilisé pour toute la session. Préparez un thème de travail et lancez une application de test dans un processus séparé.

Arborescence minimale :

~~~text
~/.themes/Theme-Laboratoire/
└── gtk-3.0/
    ├── gtk.css
    ├── gtk-dark.css
    └── assets/
~~~

Créez d'abord une copie du fichier CSS de départ. Conservez une version connue comme fonctionnelle afin de pouvoir comparer le résultat et revenir en arrière.

Pour tester une application avec un thème explicite :

~~~bash
GTK_THEME=Theme-Laboratoire:dark application
~~~

Remplacez application par le nom réel de l'exécutable. La variante sombre est demandée si elle est disponible. Ce mécanisme ne garantit pas qu'une application ne charge pas ensuite ses propres fournisseurs CSS.

Si l'application est lancée depuis un environnement isolé, tel qu'un bac à sable, vérifiez que le thème est effectivement accessible à ce processus. Un chemin présent sur l'hôte n'est pas nécessairement visible dans le conteneur.

## 17. Comprendre la cascade des fournisseurs GTK 3

GTK peut recevoir des règles CSS depuis plusieurs fournisseurs. Le thème du système, les feuilles chargées par l'application et les fournisseurs ajoutés par le code peuvent entrer en concurrence.

Quand une règle ne produit aucun effet, ne modifiez pas immédiatement sa spécificité. Procédez dans cet ordre :

1. Vérifiez que le processus utilise GTK 3 et non GTK 4.
2. Vérifiez le nom du thème réellement chargé.
3. Confirmez que le fichier CSS est lu sans erreur.
4. Inspectez le nœud et son chemin dans l'arbre.
5. Vérifiez ses classes et pseudo-classes au moment du test.
6. Recherchez une règle plus prioritaire ou un fournisseur ajouté par l'application.
7. Modifiez une seule propriété puis relancez le test.

Les règles chargées par une application peuvent volontairement différer du thème global. Un composant qui conserve une couleur propre à l'application n'indique donc pas forcément que le thème utilisateur est absent.

### Distinguer les causes

- Une règle inconnue dans les journaux indique souvent une propriété ou un sélecteur non pris en charge.
- Une règle valide qui ne cible aucun nœud indique généralement un sélecteur incorrect.
- Une règle qui cible le nœud mais perd face à une autre déclaration demande une inspection de la cascade.
- Une apparence qui ne change qu'après redémarrage peut indiquer que le fournisseur CSS est chargé au démarrage.

Ne corrigez pas un problème de chargement par une multiplication de sélecteurs avec !important. Cela rend la maintenance plus difficile et peut casser les états internes.

## 18. Inspecter les composants GTK 3 dans leurs états réels

Un widget doit être inspecté dans plusieurs états. La structure CSS peut évoluer lorsque l'utilisateur ouvre un menu, sélectionne une ligne ou déclenche une validation.

Pour chaque composant, notez :
- le type de widget ;
- le nom du nœud CSS ;
- le chemin des nœuds parents ;
- les classes de style ;
- les pseudo-classes actives ;
- les propriétés qui ont un effet visible ;
- les règles qui semblent prioritaires.

Inspectez notamment :
- bouton normal, survolé, actif, focalisé et désactivé ;
- entrée vide, remplie, sélectionnée et en erreur ;
- ligne de TreeView normale, survolée, sélectionnée et focalisée ;
- menu ouvert, sous-menu ouvert et élément coché ;
- onglet actif et inactif ;
- infobar d'information, d'avertissement et d'erreur ;
- barre de défilement au repos et pendant le déplacement.

Ne déduisez pas les états à partir d'une capture statique. Activez réellement le contrôle et observez les changements de classes.

## 19. Atelier : personnaliser une TreeView sans perdre ses fonctions

GtkTreeView reste présent dans des applications GTK 3 anciennes. Son apparence peut dépendre de l'en-tête, des lignes, des cellules et des éditeurs intégrés.

Commencez par un style limité :

~~~css
treeview.view {
  background-color: @theme_base_color;
  color: @theme_text_color;
}

treeview.view:selected {
  background-color: @theme_selected_bg_color;
  color: @theme_selected_fg_color;
}

treeview.view header button {
  border-radius: 0;
  border-bottom: 1px solid @borders;
}
~~~

Procédure :
1. Ouvrez une vue avec plusieurs colonnes.
2. Cliquez sur un en-tête triable.
3. Sélectionnez une ligne.
4. Déplacez le focus avec le clavier.
5. Testez une sélection multiple si l'application la permet.
6. Éditez une cellule si cette fonction existe.
7. Redimensionnez les colonnes.
8. Faites défiler une liste longue.
9. Vérifiez les lignes contenant une icône et un texte secondaire.

Vérifiez aussi le contraste des lignes sélectionnées lorsque la fenêtre perd le focus. Une sélection inactive doit rester identifiable sans ressembler à une ligne désactivée.

Si un éditeur de cellule devient illisible, inspectez le widget d'édition créé dans la cellule. Il peut s'agir d'un champ différent de la cellule affichée au repos.

## 20. Atelier : menus, sous-menus et popovers

Les menus sont souvent créés à la demande. Il faut les ouvrir pendant l'inspection pour observer leurs nœuds.

Testez un menu contenant :
- une action simple ;
- une action avec icône ;
- une case à cocher ;
- un choix radio ;
- un raccourci clavier ;
- un séparateur ;
- un sous-menu ;
- un libellé long.

Vérifiez la navigation au clavier, le survol, l'élément actif, l'état coché et la fermeture du menu. Une règle de survol ne doit pas masquer l'état sélectionné ou désactivé.

Les popovers sont attachés à un contrôle et peuvent être positionnés différemment selon l'espace disponible. Testez-les près des bords de la fenêtre et lorsque celle-ci est redimensionnée.

## 21. Atelier : onglets, boîtes de dialogue et fenêtres secondaires

Les applications GTK 3 peuvent combiner GtkNotebook, dialogues modaux et fenêtres secondaires.

Pour les onglets, vérifiez :
- onglet actif et inactif ;
- focus clavier ;
- fermeture d'un onglet ;
- débordement de la barre ;
- libellé long ;
- icône ou indicateur d'état.

Pour les dialogues, vérifiez :
- titre et texte descriptif ;
- bouton par défaut ;
- action destructive ;
- bouton désactivé ;
- contenu défilant ;
- fermeture par Échap lorsqu'elle est autorisée ;
- focus initial et retour du focus à la fenêtre parente.

Ne forcez pas tous les dialogues à la même taille. La géométrie dépend du contenu et du comportement de l'application.

## 22. Vérifier les champs, validations et erreurs

Les champs de saisie doivent être testés avec des données représentatives, pas uniquement à vide.

Scénarios :
- champ vide ;
- texte court et texte long ;
- accents et caractères non latins ;
- sélection partielle ;
- curseur en début et fin ;
- saisie en lecture seule ;
- champ désactivé ;
- erreur de validation ;
- texte d'aide ;
- mot de passe avec contrôle de visibilité.

Conservez un contraste distinct pour le texte, le curseur, la sélection et le placeholder. Un placeholder n'est pas un remplacement du libellé du champ.

Les erreurs doivent rester identifiables par leur texte ou leur icône. Ne colorez pas uniquement la bordure en rouge si le message associé n'est pas visible.

## 23. Vérifier les barres de défilement et les contrôles de valeur

Les barres de défilement, échelles et barres de progression ont des parties internes. Les règles génériques doivent être validées en orientation horizontale et verticale.

Testez :
- barre verticale dans une liste ;
- barre horizontale dans une vue large ;
- curseur de volume ;
- échelle avec graduations ;
- progression indéterminée ;
- progression terminée ;
- contrôle désactivé.

Ne supprimez pas les zones de saisie ni les poignées. Une poignée étroite peut être difficile à saisir, particulièrement sur un écran tactile ou à fort facteur d'échelle.

Une barre de progression indéterminée doit rester visuellement animée si l'application utilise cet état. Ne remplacez pas une progression par une surface statique.

## 24. Contrôler les variantes claires et sombres

Une feuille sombre ne se résume pas à inverser le fond et le texte. Les couleurs de sélection, les bordures, les infobulles et les messages sémantiques doivent être contrôlés indépendamment.

Pour chaque composant, vérifiez :
- fond et texte au repos ;
- sélection ;
- focus ;
- survol ;
- désactivation ;
- avertissement et erreur ;
- infobulle ;
- fenêtre inactive.

Si gtk-dark.css est utilisé, vérifiez comment le thème et l'application sélectionnent cette feuille. Ne supposez pas qu'un fichier portant ce nom est automatiquement chargé dans toutes les configurations.

## 25. Vérifier les applications qui mélangent les générations GTK

Une même session peut contenir des applications GTK 3, GTK 4 et Libadwaita. Le nom de l'application ou son apparence ne permet pas d'identifier avec certitude sa pile graphique.

Identifiez la bibliothèque chargée par le processus ou consultez les informations de l'application. Inspectez ensuite le moteur et les ressources réellement utilisés.

Ne tentez pas de corriger une application GTK 4 en ajoutant ses sélecteurs à gtk.css de GTK 3. Une règle GTK 3 ne traverse pas les moteurs CSS.

Si une application GTK 3 ne suit pas la palette générale, vérifiez si elle charge son propre CSS ou utilise des ressources embarquées. Documentez cette exception au lieu d'élargir une règle globale qui affecterait les autres applications.

## 26. Fiche de validation GTK 3

~~~text
Application et version :
Version GTK observée :
Distribution et session :
Thème GTK chargé :
Variante claire ou sombre :
Fournisseurs CSS spécifiques à l'application :
Fenêtres et headerbars :
Boutons et actions :
Champs et validations :
TreeView et cellules :
Menus et sous-menus :
Popovers :
Onglets et dialogues :
Barres de défilement et contrôles :
Focus clavier :
Sélection inactive :
Textes longs et internationalisation :
Avertissements CSS :
Sélecteurs et propriétés modifiés :
Captures de référence :
Anomalies :
Conclusion : validé / partiel / à corriger
~~~

Une validation complète doit être faite sur plusieurs applications GTK 3. Un composant qui fonctionne dans une application ne prouve pas que le même sélecteur convient à toutes les implémentations.
