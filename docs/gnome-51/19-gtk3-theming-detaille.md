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
