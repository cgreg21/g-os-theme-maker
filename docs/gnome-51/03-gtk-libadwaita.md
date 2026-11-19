# 3. GTK 3, GTK 4 et Libadwaita

## 3. GTK 3.24 : catalogue des widgets

GTK 3 utilise les nœuds CSS, classes de style et états. Le nom du widget et le nom de son nœud CSS peuvent différer. Les widgets ci-dessous couvrent les familles standard courantes. Les applications peuvent ajouter des widgets personnalisés.

| Famille | Widgets / nœuds à couvrir | Détails visuels |
|---|---|---|
| Fenêtres | `window`, `.background`, `dialog` | fond, bordure, ombre, rayon |
| Barres de titre | `headerbar`, `.titlebar`, `headerbar.titlebar` | fond, titre, sous-titre, boutons |
| Boutons | `button`, `.flat`, `.suggested-action`, `.destructive-action` | normal, hover, focus, active, disabled |
| Boutons à bascule | `togglebutton`, `:checked` | sélection et état actif |
| Cases / radios | `checkbutton`, `radiobutton` | indicateur, coché, indéterminé |
| Interrupteurs | `switch`, `.slider` | piste, poignée, checked |
| Champs | `entry`, `textview`, `spinbutton` | saisie, placeholder, sélection, erreur |
| Menus | `menu`, `menuitem`, `menubar`, `popover` | ligne, icône, raccourci, séparateur |
| Listes | `list`, `row`, `listbox` | sélection, survol, alternance |
| Arbres GTK 3 | `treeview`, `treeview.view`, `header` | ligne, colonne, en-tête |
| Onglets | `notebook`, `.tab` | onglet actif, barre et contenu |
| Barres | `toolbar`, `statusbar`, `infobar` | fond, bordure, message |
| Progression | `progressbar`, `levelbar`, `spinner` | remplissage, activité |
| Curseurs | `scale`, `trough`, `slider` | piste, poignée, valeurs |
| Défilement | `scrollbar`, `trough`, `slider` | poignée et états |
| Conteneurs | `frame`, `box`, `grid`, `stack`, `paned`, `overlay` | fond, séparateur, bordure |
| Dépliants | `expander`, `.title` | flèche et contenu |
| Séparateurs | `separator` | orientation et couleur |
| Calendrier | `calendar` | jour courant, sélection, navigation |
| Infobulles | `tooltip` | fond, texte, bordure |
| Sélection de fichiers | widgets FileChooser | emplacement, liste, aperçu, boutons |
| Choix couleur/police | ColorChooser, FontChooser | champs, listes, aperçu |
| Accessibilité | focus, indicateurs, descriptions | focus visible et contraste |

Exemple de style GTK 3 :

```css
@define-color theme_bg_color #242424;
@define-color theme_fg_color #ffffff;
@define-color theme_selected_bg_color #3584e4;
@define-color theme_selected_fg_color #ffffff;

window, .background { background: @theme_bg_color; color: @theme_fg_color; }
button { background: #303030; color: @theme_fg_color; border: 1px solid #555; border-radius: 8px; padding: 6px 10px; }
button:hover { background: #3b3b3b; }
button:checked, button:active { background: @theme_selected_bg_color; color: @theme_selected_fg_color; }
entry { background: #202020; color: @theme_fg_color; border: 1px solid #555; }
*:focus { outline-color: @theme_selected_bg_color; }
```

GTK 3 autorise des nœuds et classes spécifiques. Pour un composant précis, consulter la page API du widget et son arbre CSS réel. Ne pas utiliser les sélecteurs GTK 3 dans une feuille GTK 4 sans vérification.

## 4. GTK 4 : catalogue des widgets

GTK 4 conserve le CSS par nœuds mais a fait évoluer les widgets et les conteneurs. Les familles de composants à représenter dans un éditeur sont :

| Famille | Widgets GTK 4 | États / parties à régler |
|---|---|---|
| Fenêtres | `GtkWindow`, `GtkDialog`, `GtkApplicationWindow` | fond, surface, contour |
| En-tête | `GtkHeaderBar`, `GtkWindowControls` | titre, boutons, ordre RTL |
| Boutons | `GtkButton`, `GtkToggleButton`, `GtkLinkButton` | normal, hover, focus, active, checked, disabled |
| Boutons spécialisés | `GtkMenuButton`, `GtkScaleButton`, `GtkVolumeButton`, `GtkLockButton` | icône, menu, valeur |
| Indicateurs | `GtkCheckButton`, `GtkSwitch`, `GtkSpinner` | coché, bascule, animation |
| Texte | `GtkEntry`, `GtkPasswordEntry`, `GtkSearchEntry`, `GtkText`, `GtkTextView`, `GtkLabel`, `GtkInscription` | saisie, sélection, placeholder, liens |
| Sélection | `GtkDropDown`, `GtkComboBoxText` (selon API), `GtkListBox`, `GtkGridView`, `GtkListView`, `GtkColumnView` | ligne, cellule, sélection, focus |
| Menus | `GtkPopover`, `GtkPopoverMenu`, `GtkPopoverMenuBar` | panneau, items, séparateurs |
| Onglets | `GtkNotebook` (compatibilité), `GtkStack`, `GtkStackSwitcher` | page active, transition |
| Navigation | `GtkShortcutsWindow`, `GtkAssistant` | pages, groupes, raccourcis |
| Valeurs | `GtkScale`, `GtkLevelBar`, `GtkProgressBar`, `GtkSpinButton` | piste, remplissage, poignée |
| Défilement | `GtkScrollbar`, `GtkScrolledWindow` | poignée, bord, overshoot |
| Conteneurs | `GtkBox`, `GtkGrid`, `GtkCenterBox`, `GtkOverlay`, `GtkPaned`, `GtkFrame`, `GtkAspectFrame`, `GtkFixed` | fonds, bordures, séparateurs |
| Révélation | `GtkRevealer`, `GtkExpander` | flèche, transition |
| Date et couleur | `GtkCalendar`, `GtkColorButton`, `GtkColorChooser` | sélection, navigation |
| Média | `GtkPicture`, `GtkImage`, `GtkVideo` | fond, cadre, contrôles |
| Aide | `GtkTooltip`, `GtkPopover` | fond, texte, contour |
| Fichiers | `GtkFileChooser`, `GtkFileChooserWidget`, `GtkFileChooserDialog` | sidebar, fichiers, sélection |
| Divers | `GtkSeparator`, `GtkDrawingArea`, `GtkGLArea`, `GtkNativeDialog` | cas spécifiques |

Les noms de widgets ci-dessus sont des classes API ; pour les feuilles CSS, utiliser les nœuds et classes documentés par GTK. Certains widgets GTK 3 n’ont pas d’équivalent direct en GTK 4 (notamment `GtkTreeView`, remplacé par les vues de liste/colonnes).

Exemple GTK 4 conservateur :

```css
window, .background { background-color: #242424; color: #ffffff; }
headerbar { background-color: #303030; color: #ffffff; }
button { background-color: #303030; color: #ffffff; border-radius: 8px; padding: 6px 10px; }
button:hover { background-color: #3b3b3b; }
entry, textview { background-color: #202020; color: #ffffff; }
```

GTK 4.16+ prend en charge les propriétés CSS personnalisées et `var()`. Ne pas les utiliser pour une cible GTK 4.0–4.15.

## 5. Libadwaita : composants GNOME modernes

Libadwaita repose sur GTK 4 et ajoute des composants, des conventions visuelles et des variables de style. Les classes API `Adw*` ne sont pas nécessairement des sélecteurs CSS. Vérifier les nœuds et classes de style indiqués par la documentation de chaque composant.

| Famille | Composants Libadwaita | Éléments à couvrir |
|---|---|---|
| Fenêtres | `AdwWindow`, `AdwApplicationWindow`, `AdwAboutWindow` | surface, bordure, ombre, titre |
| Dialogues | `AdwDialog`, `AdwAlertDialog`, `AdwMessageDialog`, `AdwPreferencesDialog` | contenu, actions, avertissements |
| Barre d’outils | `AdwHeaderBar`, `AdwToolbarView`, `AdwWindowTitle` | titre, sous-titre, zones de contrôle |
| Navigation | `AdwNavigationView`, `AdwNavigationPage`, `AdwNavigationSplitView`, `AdwOverlaySplitView`, `AdwFlap` | panneau, séparation, transition |
| Onglets | `AdwTabView`, `AdwTabBar`, `AdwViewSwitcher`, `AdwViewSwitcherBar` | onglet actif, indicateur, débordement |
| Préférences | `AdwPreferencesWindow`, `AdwPreferencesPage`, `AdwPreferencesGroup`, `AdwPreferencesRow` | titres, groupes, lignes |
| Lignes | `AdwActionRow`, `AdwComboRow`, `AdwEntryRow`, `AdwPasswordEntryRow`, `AdwSpinRow`, `AdwSwitchRow`, `AdwExpanderRow` | icônes, valeurs, descriptions, bascule |
| Boutons | `AdwButtonContent`, `AdwSplitButton`, `AdwToggleGroup` | contenu, icône, sélection |
| Contenu | `AdwStatusPage`, `AdwBanner`, `AdwToastOverlay`, `AdwToast`, `AdwClamp`, `AdwClampScrollable`, `AdwCarousel` | état vide, bannière, notification, largeur |
| Utilitaires | `AdwAvatar`, `AdwSpinner`, `AdwViewStack`, `AdwViewStackPage`, `AdwBreakpoint` | avatar, chargement, navigation adaptative |

### 5.1 Couleurs et surfaces

Les couleurs Libadwaita doivent conserver la sémantique : fond de fenêtre, fond de vue, barre d’en-tête, carte, popover, accent, texte et bordure. Exemple de variables (la disponibilité exacte dépend de la version Libadwaita) :

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
  --popover-bg-color: #303030;
  --popover-fg-color: #ffffff;
  --accent-bg-color: #3584e4;
  --accent-fg-color: #ffffff;
  --accent-color: #3584e4;
  --border-color: #555555;
}
```

Un CSS utilisateur peut être ignoré ou supplanté par une application. Libadwaita ne fournit pas de mécanisme universel pour remplacer tous les styles de toutes les applications.


## 3.1 Inspecter les nœuds CSS

GTK ne stylise pas un DOM Web. Chaque widget expose un arbre de nœuds CSS : noms, classes, états et enfants. GtkScale possède par exemple trough, slider, marks et fill. La classe API du widget n'est pas nécessairement le sélecteur CSS.

Méthode : inspecter l'arbre avec les outils de développement disponibles ; consulter la documentation du widget ; relever nœud/classes/états ; écrire une règle ciblée ; vérifier les avertissements ; refaire le test après changement de version.

## 3.2 Providers et priorité

Les providers internes, thème, paramètres et application ont des priorités différentes. Une application peut ajouter son CSS, avoir des classes privées ou dessiner ses composants. Ne pas promettre qu'un thème global peut forcer tous les styles Libadwaita.

## 3.3 GTK 3 et GTK 4 ne sont pas interchangeables

GTK 3 conserve des widgets historiques comme GtkTreeView. GTK 4 privilégie ListView/GridView/ColumnView et expose des nœuds différents. Vérifier les sélecteurs de headerbars, menus, popovers, champs, listes, scrollbars, notebooks, dialogues, infobulles et sélecteurs de fichiers sur chaque version.

## 3.4 Libadwaita

Les classes Adw* sont des classes API, pas nécessairement des sélecteurs CSS. Préférer les classes de style et couleurs sémantiques documentées. Les applications peuvent charger leur propre CSS ; le CSS utilisateur n'est pas une API universelle de re-skinning.

## 3.5 Couleurs sémantiques

Selon version : window-bg/fg, view-bg/fg, headerbar-bg/fg, card-bg/fg, popover-bg/fg, accent-bg/fg, accent-color et destructive-color. Vérifier la référence de la version Libadwaita ciblée.

Références : [GTK 3 CSS](https://docs.gtk.org/gtk3/css-overview.html), [GTK 4 CSS](https://docs.gtk.org/gtk4/css-overview.html), [Libadwaita styles](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html).
