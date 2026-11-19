# 3. GTK 3, GTK 4 et Libadwaita

## Catalogue des widgets GTK 3.24

GTK 3 utilise les nœuds CSS, classes de style et états. Le nom du widget et le nom de son nœud CSS peuvent différer. Les widgets ci-dessous couvrent les familles standard courantes. Les applications peuvent ajouter des widgets personnalisés.

- **Famille** : Fenêtres ; **Widgets / nœuds à couvrir** : `window`, `.background`, `dialog` ; **Détails visuels** : fond, bordure, ombre, rayon
- **Famille** : Barres de titre ; **Widgets / nœuds à couvrir** : `headerbar`, `.titlebar`, `headerbar.titlebar` ; **Détails visuels** : fond, titre, sous-titre, boutons
- **Famille** : Boutons ; **Widgets / nœuds à couvrir** : `button`, `.flat`, `.suggested-action`, `.destructive-action` ; **Détails visuels** : normal, hover, focus, active, disabled
- **Famille** : Boutons à bascule ; **Widgets / nœuds à couvrir** : `togglebutton`, `:checked` ; **Détails visuels** : sélection et état actif
- **Famille** : Cases / radios ; **Widgets / nœuds à couvrir** : `checkbutton`, `radiobutton` ; **Détails visuels** : indicateur, coché, indéterminé
- **Famille** : Interrupteurs ; **Widgets / nœuds à couvrir** : `switch`, `.slider` ; **Détails visuels** : piste, poignée, checked
- **Famille** : Champs ; **Widgets / nœuds à couvrir** : `entry`, `textview`, `spinbutton` ; **Détails visuels** : saisie, placeholder, sélection, erreur
- **Famille** : Menus ; **Widgets / nœuds à couvrir** : `menu`, `menuitem`, `menubar`, `popover` ; **Détails visuels** : ligne, icône, raccourci, séparateur
- **Famille** : Listes ; **Widgets / nœuds à couvrir** : `list`, `row`, `listbox` ; **Détails visuels** : sélection, survol, alternance
- **Famille** : Arbres GTK 3 ; **Widgets / nœuds à couvrir** : `treeview`, `treeview.view`, `header` ; **Détails visuels** : ligne, colonne, en-tête
- **Famille** : Onglets ; **Widgets / nœuds à couvrir** : `notebook`, `.tab` ; **Détails visuels** : onglet actif, barre et contenu
- **Famille** : Barres ; **Widgets / nœuds à couvrir** : `toolbar`, `statusbar`, `infobar` ; **Détails visuels** : fond, bordure, message
- **Famille** : Progression ; **Widgets / nœuds à couvrir** : `progressbar`, `levelbar`, `spinner` ; **Détails visuels** : remplissage, activité
- **Famille** : Curseurs ; **Widgets / nœuds à couvrir** : `scale`, `trough`, `slider` ; **Détails visuels** : piste, poignée, valeurs
- **Famille** : Défilement ; **Widgets / nœuds à couvrir** : `scrollbar`, `trough`, `slider` ; **Détails visuels** : poignée et états
- **Famille** : Conteneurs ; **Widgets / nœuds à couvrir** : `frame`, `box`, `grid`, `stack`, `paned`, `overlay` ; **Détails visuels** : fond, séparateur, bordure
- **Famille** : Dépliants ; **Widgets / nœuds à couvrir** : `expander`, `.title` ; **Détails visuels** : flèche et contenu
- **Famille** : Séparateurs ; **Widgets / nœuds à couvrir** : `separator` ; **Détails visuels** : orientation et couleur
- **Famille** : Calendrier ; **Widgets / nœuds à couvrir** : `calendar` ; **Détails visuels** : jour courant, sélection, navigation
- **Famille** : Infobulles ; **Widgets / nœuds à couvrir** : `tooltip` ; **Détails visuels** : fond, texte, bordure
- **Famille** : Sélection de fichiers ; **Widgets / nœuds à couvrir** : widgets FileChooser ; **Détails visuels** : emplacement, liste, aperçu, boutons
- **Famille** : Choix couleur/police ; **Widgets / nœuds à couvrir** : ColorChooser, FontChooser ; **Détails visuels** : champs, listes, aperçu
- **Famille** : Accessibilité ; **Widgets / nœuds à couvrir** : focus, indicateurs, descriptions ; **Détails visuels** : focus visible et contraste

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

## Catalogue des widgets GTK 4

GTK 4 conserve le CSS par nœuds mais a fait évoluer les widgets et les conteneurs. Les familles de composants à représenter dans un éditeur sont :

- **Famille** : Fenêtres ; **Widgets GTK 4** : `GtkWindow`, `GtkDialog`, `GtkApplicationWindow` ; **États / parties à régler** : fond, surface, contour
- **Famille** : En-tête ; **Widgets GTK 4** : `GtkHeaderBar`, `GtkWindowControls` ; **États / parties à régler** : titre, boutons, ordre RTL
- **Famille** : Boutons ; **Widgets GTK 4** : `GtkButton`, `GtkToggleButton`, `GtkLinkButton` ; **États / parties à régler** : normal, hover, focus, active, checked, disabled
- **Famille** : Boutons spécialisés ; **Widgets GTK 4** : `GtkMenuButton`, `GtkScaleButton`, `GtkVolumeButton`, `GtkLockButton` ; **États / parties à régler** : icône, menu, valeur
- **Famille** : Indicateurs ; **Widgets GTK 4** : `GtkCheckButton`, `GtkSwitch`, `GtkSpinner` ; **États / parties à régler** : coché, bascule, animation
- **Famille** : Texte ; **Widgets GTK 4** : `GtkEntry`, `GtkPasswordEntry`, `GtkSearchEntry`, `GtkText`, `GtkTextView`, `GtkLabel`, `GtkInscription` ; **États / parties à régler** : saisie, sélection, placeholder, liens
- **Famille** : Sélection ; **Widgets GTK 4** : `GtkDropDown`, `GtkComboBoxText` (selon API), `GtkListBox`, `GtkGridView`, `GtkListView`, `GtkColumnView` ; **États / parties à régler** : ligne, cellule, sélection, focus
- **Famille** : Menus ; **Widgets GTK 4** : `GtkPopover`, `GtkPopoverMenu`, `GtkPopoverMenuBar` ; **États / parties à régler** : panneau, items, séparateurs
- **Famille** : Onglets ; **Widgets GTK 4** : `GtkNotebook` (compatibilité), `GtkStack`, `GtkStackSwitcher` ; **États / parties à régler** : page active, transition
- **Famille** : Navigation ; **Widgets GTK 4** : `GtkShortcutsWindow`, `GtkAssistant` ; **États / parties à régler** : pages, groupes, raccourcis
- **Famille** : Valeurs ; **Widgets GTK 4** : `GtkScale`, `GtkLevelBar`, `GtkProgressBar`, `GtkSpinButton` ; **États / parties à régler** : piste, remplissage, poignée
- **Famille** : Défilement ; **Widgets GTK 4** : `GtkScrollbar`, `GtkScrolledWindow` ; **États / parties à régler** : poignée, bord, overshoot
- **Famille** : Conteneurs ; **Widgets GTK 4** : `GtkBox`, `GtkGrid`, `GtkCenterBox`, `GtkOverlay`, `GtkPaned`, `GtkFrame`, `GtkAspectFrame`, `GtkFixed` ; **États / parties à régler** : fonds, bordures, séparateurs
- **Famille** : Révélation ; **Widgets GTK 4** : `GtkRevealer`, `GtkExpander` ; **États / parties à régler** : flèche, transition
- **Famille** : Date et couleur ; **Widgets GTK 4** : `GtkCalendar`, `GtkColorButton`, `GtkColorChooser` ; **États / parties à régler** : sélection, navigation
- **Famille** : Média ; **Widgets GTK 4** : `GtkPicture`, `GtkImage`, `GtkVideo` ; **États / parties à régler** : fond, cadre, contrôles
- **Famille** : Aide ; **Widgets GTK 4** : `GtkTooltip`, `GtkPopover` ; **États / parties à régler** : fond, texte, contour
- **Famille** : Fichiers ; **Widgets GTK 4** : `GtkFileChooser`, `GtkFileChooserWidget`, `GtkFileChooserDialog` ; **États / parties à régler** : sidebar, fichiers, sélection
- **Famille** : Divers ; **Widgets GTK 4** : `GtkSeparator`, `GtkDrawingArea`, `GtkGLArea`, `GtkNativeDialog` ; **États / parties à régler** : cas spécifiques

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

## Catalogue des composants Libadwaita

Libadwaita repose sur GTK 4 et ajoute des composants, des conventions visuelles et des variables de style. Les classes API `Adw*` ne sont pas nécessairement des sélecteurs CSS. Vérifier les nœuds et classes de style indiqués par la documentation de chaque composant.

- **Famille** : Fenêtres ; **Composants Libadwaita** : `AdwWindow`, `AdwApplicationWindow`, `AdwAboutWindow` ; **Éléments à couvrir** : surface, bordure, ombre, titre
- **Famille** : Dialogues ; **Composants Libadwaita** : `AdwDialog`, `AdwAlertDialog`, `AdwMessageDialog`, `AdwPreferencesDialog` ; **Éléments à couvrir** : contenu, actions, avertissements
- **Famille** : Barre d’outils ; **Composants Libadwaita** : `AdwHeaderBar`, `AdwToolbarView`, `AdwWindowTitle` ; **Éléments à couvrir** : titre, sous-titre, zones de contrôle
- **Famille** : Navigation ; **Composants Libadwaita** : `AdwNavigationView`, `AdwNavigationPage`, `AdwNavigationSplitView`, `AdwOverlaySplitView`, `AdwFlap` ; **Éléments à couvrir** : panneau, séparation, transition
- **Famille** : Onglets ; **Composants Libadwaita** : `AdwTabView`, `AdwTabBar`, `AdwViewSwitcher`, `AdwViewSwitcherBar` ; **Éléments à couvrir** : onglet actif, indicateur, débordement
- **Famille** : Préférences ; **Composants Libadwaita** : `AdwPreferencesWindow`, `AdwPreferencesPage`, `AdwPreferencesGroup`, `AdwPreferencesRow` ; **Éléments à couvrir** : titres, groupes, lignes
- **Famille** : Lignes ; **Composants Libadwaita** : `AdwActionRow`, `AdwComboRow`, `AdwEntryRow`, `AdwPasswordEntryRow`, `AdwSpinRow`, `AdwSwitchRow`, `AdwExpanderRow` ; **Éléments à couvrir** : icônes, valeurs, descriptions, bascule
- **Famille** : Boutons ; **Composants Libadwaita** : `AdwButtonContent`, `AdwSplitButton`, `AdwToggleGroup` ; **Éléments à couvrir** : contenu, icône, sélection
- **Famille** : Contenu ; **Composants Libadwaita** : `AdwStatusPage`, `AdwBanner`, `AdwToastOverlay`, `AdwToast`, `AdwClamp`, `AdwClampScrollable`, `AdwCarousel` ; **Éléments à couvrir** : état vide, bannière, notification, largeur
- **Famille** : Utilitaires ; **Composants Libadwaita** : `AdwAvatar`, `AdwSpinner`, `AdwViewStack`, `AdwViewStackPage`, `AdwBreakpoint` ; **Éléments à couvrir** : avatar, chargement, navigation adaptative

### Couleurs et surfaces

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

## Comprendre et inspecter les nœuds CSS

GTK ne stylise pas un DOM Web. Chaque widget expose un arbre de nœuds CSS : noms, classes, états et enfants. GtkScale possède par exemple trough, slider, marks et fill. La classe API du widget n'est pas nécessairement le sélecteur CSS.

Méthode : inspecter l'arbre avec les outils de développement disponibles ; consulter la documentation du widget ; relever nœud/classes/états ; écrire une règle ciblée ; vérifier les avertissements ; refaire le test après changement de version.

## Cascade et priorité des providers

Les providers internes, thème, paramètres et application ont des priorités différentes. Une application peut ajouter son CSS, avoir des classes privées ou dessiner ses composants. Ne pas promettre qu'un thème global peut forcer tous les styles Libadwaita.

## Différences entre GTK 3 et GTK 4

GTK 3 conserve des widgets historiques comme GtkTreeView. GTK 4 privilégie ListView/GridView/ColumnView et expose des nœuds différents. Vérifier les sélecteurs de headerbars, menus, popovers, champs, listes, scrollbars, notebooks, dialogues, infobulles et sélecteurs de fichiers sur chaque version.

## Règles propres à Libadwaita

Les classes Adw* sont des classes API, pas nécessairement des sélecteurs CSS. Préférer les classes de style et couleurs sémantiques documentées. Les applications peuvent charger leur propre CSS ; le CSS utilisateur n'est pas une API universelle de re-skinning.

## Couleurs sémantiques

Selon version : window-bg/fg, view-bg/fg, headerbar-bg/fg, card-bg/fg, popover-bg/fg, accent-bg/fg, accent-color et destructive-color. Vérifier la référence de la version Libadwaita ciblée.

Références : [GTK 3 CSS](https://docs.gtk.org/gtk3/css-overview.html), [GTK 4 CSS](https://docs.gtk.org/gtk4/css-overview.html), [Libadwaita styles](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html).
