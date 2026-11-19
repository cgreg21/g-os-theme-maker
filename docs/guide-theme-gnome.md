# Catalogue complet des éléments d’interface GNOME

Ce guide est le catalogue de référence de G-OS Theme Maker. Il décrit les familles d’éléments visuels qu’un thème peut couvrir, les moteurs qui les dessinent, les états à prévoir et les limites de compatibilité.

La référence GNOME Shell est **GNOME Shell 51.0** (sources amont). Les applications sont séparées selon **GTK 3**, **GTK 4** et **Libadwaita**. Ce catalogue distingue les éléments réellement stylables des éléments dont l’apparence est contrôlée par le système, l’application ou une extension.

> « Couvrir tous les éléments » signifie couvrir toutes les familles de composants d’interface et leurs états, et fournir un inventaire vérifiable des composants GNOME Shell 51. Les applications peuvent créer leurs propres widgets : aucun thème global ne peut garantir le style de chaque interface tierce.

## 1. Périmètre : les moteurs de rendu

Un bureau GNOME n’a pas un moteur de thème unique. Il faut produire et tester plusieurs feuilles indépendantes.

| Cible | Technologie | Ressource principale | Éléments couverts |
|---|---|---|---|
| GNOME Shell 51 | St / Clutter | `gnome-shell.css` | panneau, vue Activités, dash, menus système, notifications, verrouillage, OSD |
| GTK 3.24 | GTK CSS | `gtk-3.0/gtk.css` | widgets GTK 3 et anciennes applications |
| GTK 4 | GTK CSS | `gtk-4.0/gtk.css` | widgets GTK 4 |
| Libadwaita | GTK 4 + styles Adwaita | CSS de l’application / CSS utilisateur | fenêtres et composants Adwaita |
| Icônes | Freedesktop Icon Theme | `index.theme` + ressources | applications, actions, appareils, fichiers |
| Curseurs | Xcursor | `index.theme` + fichiers curseurs | pointeurs et curseurs de saisie |
| Polices | Fontconfig / paramètres GNOME | fichiers de police et réglages | familles, graisse, taille et rendu |
| Fond d’écran | GNOME Background / URI | image + métadonnées | fond du bureau et écran de verrouillage |

Les thèmes Shell, GTK, icônes et curseurs sont des paquets distincts. Les paramètres de police et le fond d’écran ne sont pas des feuilles CSS.

## 2. GNOME Shell 51 : inventaire complet des familles

Les noms ci-dessous proviennent de l’organisation des sources SCSS de GNOME Shell 51.0, dans `data/theme/gnome-shell-sass/widgets/`. Les sélecteurs sont des détails d’implémentation, pas une API stable. Toujours vérifier le code de la version ciblée.

### 2.1 Panneau supérieur et indicateurs

| Élément | Sélecteurs / classes repères | Ce qui doit être personnalisable |
|---|---|---|
| Panneau supérieur | `#panel` | fond, hauteur, bordure, typographie, ombre |
| Boutons du panneau | `.panel-button` | fond, texte, marges, padding, rayon |
| Activités | `#panelActivities` | libellé, points d’espaces de travail |
| Horloge | `.clock-display`, `.clock-display-box`, `.clock` | texte, espacement, survol |
| Indicateurs système | `.system-status-icon`, `.panel-status-indicators-box` | taille et couleur des icônes |
| Notifications du panneau | `.messages-indicator` | icône et état actif |
| Enregistrement écran | `.screen-recording-indicator` | indicateur de confidentialité |
| Partage écran | `.screen-sharing-indicator` | indicateur de confidentialité |
| Confidentialité | `.privacy-indicator` | couleur d’avertissement |

Exemple :

```css
#panel { background-color: #20242b; color: #ffffff; }
#panel .panel-button { border-radius: 8px; padding: 0 8px; }
#panel .panel-button:hover,
#panel .panel-button:focus { background-color: #3584e4; }
```

### 2.2 Vue Activités, recherche et navigation

| Élément | Sélecteurs / classes repères | Couverture visuelle |
|---|---|---|
| Fond de la vue Activités | `#overviewGroup`, `#overview` selon version | fond, voile, contraste |
| Conteneur des résultats | `#searchResults`, `#searchResultsContent` | largeur, marges |
| Section de recherche | `.search-section`, `.search-section-content`, `.search-section-separator` | panneaux et séparateurs |
| Champ de recherche | `.search-entry`, `.search-entry-icon` | saisie, icône, focus |
| État de recherche | `.search-statusbox`, `.search-statustext` | chargement, aucun résultat |
| Résultats en grille | `.grid-search-results`, `.grid-search-result` | tuiles et espacement |
| Résultats en liste | `.list-search-results`, `.list-search-result` | lignes, titres, descriptions |
| Fournisseurs de recherche | `.search-provider-icon`, `.list-search-provider-content` | icône et métadonnées |
| Aperçu des fenêtres | `.window-picker`, `.window-icon`, `.window-caption` | espacement, icône, légende |
| Bouton fermer une fenêtre | `.window-close` | taille, forme, états |
| Fond d’espace de travail | `.workspace-background` | fond et ombre |
| Prévisualisation de mosaïque | `.tile-preview` | contour et couleur d’accent |
| Écrans secondaires | `.secondary-monitor-workspaces` | espacement |

### 2.3 Grille d’applications et dock

| Élément | Sélecteurs / classes repères | Couverture visuelle |
|---|---|---|
| Grille | `.icon-grid`, `.apps-scroll-view` | espacements et marges |
| Tuile d’application | `.overview-tile`, `.overview-icon` | fond, rayon, padding |
| Icône et libellé | `.overview-icon-with-label` | taille, typographie, écart |
| Indicateur application active | `.app-grid-running-dot` | taille et couleur |
| Dossier d’applications | `.app-folder`, `.app-folder-dialog` | panneau, grille, bordure |
| Nom du dossier | `.folder-name-container`, `.folder-name-entry` | titre et champ de saisie |
| Boutons du dossier | `.icon-button` | icônes et états |
| Pagination | `.page-indicator`, `.page-indicator-icon` | points et sélection |
| Navigation entre pages | `.page-navigation-arrow`, `.page-navigation-hint` | flèches et zones de transition |
| Actions système de la grille | `.system-action-icon` | arrêt et autres actions |
| Dock | `#dash`, `.dash-background` | panneau, fond, rayon |
| Éléments du dock | `.dash-item-container`, `.show-apps`, `.overview-tile` | icônes, focus, survol |
| Séparateur du dock | `.dash-separator` | épaisseur et couleur |
| Emplacement de glisser-déposer | `.placeholder`, `.empty-dash-drop-target` | taille et état cible |
| Infobulle du dock | `.dash-label` | fond, texte, ombre |

### 2.4 Espaces de travail et changement de fenêtre

- Miniatures des espaces : `.workspace-thumbnails`, `.workspace-thumbnail`.
- Indicateur de l’espace sélectionné : `.workspace-thumbnail-indicator`.
- Emplacement de déplacement : `.placeholder`.
- Animation de changement : `.workspace-animation`.
- Sélecteur Alt-Tab : `.switcher-popup`, `.switcher-list`, `.switcher-list-item-container`, `.item-box`.
- Miniatures Alt-Tab : `.thumbnail-box`, `.thumbnail`.
- Flèche d’application multi-fenêtres : `.switcher-arrow`.
- Sélecteur de source de saisie : `.input-source-switcher-symbol`.
- Mise en évidence de fenêtre : `.cycler-highlight`.
- Indicateurs du sélecteur d’espace : `.workspace-switcher`, `.ws-switcher-indicator`.

### 2.5 Menus, popovers et menus contextuels

| Élément | Sélecteurs / classes repères |
|---|---|
| Conteneur du menu | `.popup-menu`, `.popup-menu-content` |
| Flèche du popover | `.popup-menu-boxpointer` |
| Élément de menu | `.popup-menu-item` |
| Élément inactif | `.popup-inactive-menu-item` |
| Élément ornementé | `.popup-ornamented-menu-item`, `.popup-menu-ornament` |
| Icône et flèche | `.popup-menu-icon`, `.popup-menu-arrow` |
| Sous-menu | `.popup-sub-menu` |
| Séparateur | `.popup-separator-menu-item`, `.popup-separator-menu-item-separator` |
| Menu d’application | `.app-menu` |
| Menu contextuel du fond | `.background-menu` |
| Cases et interrupteurs | `.check-box`, `.toggle-switch` |

Ne pas supposer que le style d’un élément parent suffit : les sous-menus, ornements, cases, séparateurs et éléments désactivés possèdent leurs propres états.

### 2.6 Réglages rapides et état du système

- Conteneur des réglages : `.quick-settings`.
- Grille des commandes : `.quick-settings-grid`.
- Bouton bascule simple : `.quick-toggle`.
- Bouton bascule avec menu : `.quick-toggle-has-menu`.
- Bouton du menu secondaire : `.quick-toggle-menu-button`.
- Séparateur : `.quick-toggle-separator`.
- Titre et sous-titre : `.quick-toggle-title`, `.quick-toggle-subtitle`.
- Icône : `.quick-toggle-icon`.
- Curseur de réglage : `.quick-slider`, `.slider-bin`.
- Menu détaillé : `.quick-toggle-menu`, `.quick-toggle-menu-container`.
- En-tête du menu : `.header`, `.title`, `.subtitle`, `.icon`.
- Réseau : `.nm-network-item`, `.wireless-secure-icon`.
- Bluetooth : `.bt-device-item`, `.bt-menu-placeholder`.
- État d’un appareil : `.device-subtitle`.
- Alimentation : `.quick-settings-system-item`, `.power-item`.
- Applications en arrière-plan : `.background-apps-quick-toggle`, `.background-app-item`.
- Luminosité clavier : `.keyboard-brightness-level`.

Les commandes visibles dépendent du matériel, des services et des extensions installés. Le thème doit couvrir les commandes génériques, pas figer la liste des appareils disponibles.

### 2.7 Date, calendrier, événements, horloges et météo

- Zone date/heure : `#calendarArea`, `.datemenu-popover`.
- Colonne du calendrier : `.datemenu-calendar-column`.
- Bouton du jour : `.datemenu-today-button`, `.day-label`, `.date-label`.
- Calendrier : `.calendar`.
- En-tête du mois : `.calendar-month-header`, `.calendar-month-label`.
- Navigation mois : `.calendar-change-month-back`, `.calendar-change-month-forward`, `.pager-button`.
- Jour : `.calendar-day`, avec états `.calendar-weekday`, `.calendar-weekend`, `.calendar-other-month`, `.calendar-today`, `.calendar-day-with-events`.
- En-tête des jours : `.calendar-day-heading`.
- Numéro de semaine : `.calendar-week-number`.
- Événements : `.events-button`, `.events-box`, `.events-title`, `.events-list`, `.event-box`, `.event-summary`, `.event-time`, `.event-placeholder`.
- Horloges mondiales : `.world-clocks-button`, `.world-clocks-header`, `.world-clocks-grid`, `.world-clocks-city`, `.world-clocks-time`, `.world-clocks-timezone`.
- Météo : `.weather-button`, `.weather-box`, `.weather-header-box`, `.weather-header`, `.weather-grid`, `.weather-forecast-time`, `.weather-forecast-icon`, `.weather-forecast-temp`.

### 2.8 Notifications et contrôles multimédias

- Liste : `.message-list`, `.message-view`, `.message-list-placeholder`.
- Contrôles de la liste : `.message-list-controls`, `.message-list-clear-button`.
- Groupe : `.message-notification-group`, `.message-group-header`, `.message-group-title`, `.message-collapse-button`.
- Carte : `.message`, états `:second-in-stack` et `:lower-in-stack`.
- En-tête : `.message-header`, `.message-source-icon`, `.message-header-content`, `.message-source-title`, `.event-time`.
- Actions de carte : `.message-expand-button`, `.message-close-button`, `.message-action-bin`.
- Contenu : `.message-box`, `.message-icon`, `.message-themed-icon`, `.message-content`, `.message-title`.
- Liens : `.url-highlighter`.
- Média : `.media-message`, `.message-media-control`.
- Bannière : `.notification-banner`, `.notification-buttons-bin`, `.notification-button`.

### 2.9 Dialogues, authentification et session

- Dialogue générique : `.modal-dialog`, `.modal-dialog-content-box`, `.modal-dialog-button-box`, `.modal-dialog-button`.
- Listes dans les dialogues : `.dialog-list`, `.dialog-list-title`, `.dialog-list-scrollview`, `.dialog-list-box`, `.dialog-list-item`.
- Fin de session : `.end-session-dialog`, `.end-session-dialog-battery-warning`.
- Message : `.message-dialog-content`, `.message-dialog-title`, `.message-dialog-description`.
- Exécuter une commande : `.run-dialog`, `.run-dialog-entry`, `.run-dialog-description`.
- Authentification : `.prompt-dialog`, `.prompt-dialog-password-grid`, `.prompt-dialog-password-entry`, `.prompt-dialog-error-label`, `.prompt-dialog-info-label`.
- Polkit : `.polkit-dialog-user-layout`, `.polkit-dialog-user-label`, `.polkit-dialog-user-root-label`.
- Sélection audio : `.audio-device-selection-dialog`, `.audio-selection-box`, `.audio-selection-device`, `.audio-selection-device-box`, `.audio-selection-device-icon`.
- Bienvenue : `.welcome-dialog-image`.
- Portail d’accès : `.access-dialog`.
- Message de redémarrage : `.restart-message`.

### 2.10 Écran de connexion et verrouillage

Ces composants sont présents dans les sources de thème Shell, mais l’écran de connexion GDM est lancé par un composant système distinct. Un thème utilisateur ordinaire ne garantit pas la personnalisation de GDM.

- Racines : `.login-dialog`, `.unlock-dialog`, `#lockDialogGroup`, `.screen-shield-background`.
- Formulaire : `.login-dialog-prompt-layout`, `.login-dialog-input-well`, `.login-dialog-prompt-entry-area`, `.login-dialog-prompt-entry`.
- Boutons : `.login-dialog-button`, `.login-button`, `.web-login-prompt-button`, `.login-dialog-not-listed-button`.
- Utilisateurs : `.login-dialog-user-selection-box`, `.login-dialog-user-list-view`, `.login-dialog-user-list`, `.login-dialog-user-list-item`, `.user-widget`, `.user-icon`.
- Authentification : `.login-dialog-auth-list-view`, `.login-dialog-auth-list`, `.login-dialog-auth-list-item`, `.login-dialog-auth-list-title`, `.login-dialog-auth-menu-button`.
- Session : `.login-dialog-session-list-button`, `.login-dialog-auth-menu-button-popup`.
- Messages : `.login-dialog-message`, `.login-dialog-message-hint`, `.login-dialog-banner-view`, `.login-dialog-banner`.
- Horloge de verrouillage : `.unlock-dialog-clock`, `.unlock-dialog-clock-time`, `.unlock-dialog-clock-date`, `.unlock-dialog-clock-hint`.
- Notifications verrouillées : `#unlockDialogNotifications`, `.unlock-dialog-notifications-container`, `.unlock-dialog-notification-icon`, `.unlock-dialog-notification-label`, `.unlock-dialog-notification-count-text`.
- Contrôle parental : `.parental-controls-shield`, `.parental-controls-shield-title`, `.parental-controls-shield-description`, `.parental-controls-shield-button`.
- Connexion web : `.web-login-title-label`, `.web-login-url-label`, `.web-login-code-label`, `.web-login-prompt`.
- Session conflictuelle : `.conflicting-session-dialog-content`, `.conflicting-session-dialog-title`, `.conflicting-session-dialog-desc`.

### 2.11 Clavier virtuel et saisie

- Clavier : `#keyboard`, `.key-container`, `.keyboard-key`, `.default-key`.
- Popup des touches longues : `.keyboard-subkeys-boxpointer`.
- Emoji : `.emoji-page`, `.emoji-panel`.
- Suggestions : `.word-suggestions`.
- Champ Shell : `StEntry`, `.capslock-warning`, `.peek-password`, `.hint-text`.
- Méthodes de saisie IBus : `.candidate-popup-boxpointer`, `.candidate-popup-content`, `.candidate-index`, `.candidate-box`, `.candidate-page-button`, `.candidate-page-button-previous`, `.candidate-page-button-next`.

### 2.12 Capture d’écran, OSD et retours système

- Panneau de capture : `.screenshot-ui-panel`.
- Fermeture : `.screenshot-ui-close-button`.
- Choix du type : `.screenshot-ui-type-button`.
- Capture : `.screenshot-ui-capture-button`, `.screenshot-ui-capture-button-circle`.
- Capture vidéo / diffusion : `.screenshot-ui-shot-cast-container`, `.screenshot-ui-shot-cast-button`.
- Afficher le pointeur : `.screenshot-ui-show-pointer-button`.
- Sélection de zone : `.screenshot-ui-area-selector`, `.screenshot-ui-area-indicator-shade`, `.screenshot-ui-area-indicator-selection`, `.screenshot-ui-area-selector-handle`.
- Sélection fenêtre : `.screenshot-ui-window-selector`, `.screenshot-ui-window-selector-window`, `.screenshot-ui-window-selector-window-border`, `.screenshot-ui-window-selector-check`.
- Sélection écran : `.screenshot-ui-screen-selector`.
- Infobulle : `.screenshot-ui-tooltip`.
- OSD générique : `.osd-window`, `.level`.
- Numéro d’écran et compte à rebours : `.osd-monitor-label`, `.osd-break-countdown-label`.
- Tablette : `.pad-osd-window`, `.pad-osd-title-box`, `.combo-box-label`.
- Popup de redimensionnement : `.resize-popup`.

### 2.13 Accessibilité, débogage et composants transversaux

- Localisation du pointeur : `.ripple-pointer-location`.
- Minuteur d’accessibilité : `.pie-timer`.
- Loupe : `.magnifier-zoom-region`.
- Sélection de zone : `.select-area-rubberband`.
- Icône utilisateur : `.user-icon`, `.user-avatar`.
- Liens Shell : `.shell-link`.
- Ombres d’icônes : `.lowres-icon`, `.icon-dropshadow`.
- Ascenseurs : `StScrollView`, `StScrollBar`, `.vhandle`, `.hhandle`.
- Inspecteur Looking Glass : `#LookingGlassDialog`, `#LookingGlassPropertyInspector`, `#LookingGlassEvaluator`, `#LookingGlassWindows`, `#LookingGlassExtensions`, `#LookingGlassActors`, `#LookingGlassDebugFlags`.
- Classes internes Looking Glass : `.lg-dialog`, `.lg-toolbar-button`, `.notebook-tab`, `.lg-obj-inspector-title`, `.lg-obj-inspector-button`, `.lg-window`, `.lg-extension`, `.lg-debug-flag-button`.

### 2.14 Composants communs Shell

Les fichiers `_buttons.scss`, `_check-box.scss`, `_entries.scss`, `_slider.scss`, `_switches.scss`, `_scrollbars.scss`, `_base.scss` définissent des composants réutilisés dans plusieurs écrans :

- bouton texte `.button`, variantes `.default` et `.flat` ;
- bouton icône `.icon-button` ;
- case à cocher `.check-box` ;
- champ `StEntry` ;
- curseur `.slider` ;
- interrupteur `.toggle-switch` ;
- lien `.shell-link` ;
- infobulle (style partagé `%tooltip`) ;
- barre de défilement `StScrollBar`.

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

## 6. États communs à chaque composant

Un catalogue complet ne s’arrête pas à l’apparence normale. Pour chaque composant interactif, prévoir et tester :

| État | Description | Règle de conception |
|---|---|---|
| Normal | repos | lisible et équilibré |
| Hover | pointeur au-dessus | différence visible mais discrète |
| Focus | navigation clavier | contour visible, jamais supprimé sans remplacement |
| Active / pressed | action en cours | retour visuel immédiat |
| Checked / selected | sélection persistante | contraste et indicateur explicite |
| Disabled / insensitive | indisponible | contraste réduit mais texte encore compréhensible |
| Backdrop / inactive | fenêtre inactive | hiérarchie visuelle conservée |
| Expanded / collapsed | panneau ouvert/fermé | état identifiable |
| Error | saisie invalide | couleur + indication non chromatique |
| Warning | avertissement | distinction du message d’erreur |
| Loading | chargement | spinner ou progression |
| Empty | aucune donnée | état vide lisible |
| Drag source / drop target | glisser-déposer | source, cible et emplacement visibles |
| High contrast | contraste renforcé | contours, icônes et textes robustes |

Prévoir aussi les directions LTR/RTL, les échelles HiDPI, les tailles de texte, la navigation clavier et les préférences de réduction des animations.

## 7. Variantes d’apparence

Les variantes ne doivent pas être un simple filtre inversant les couleurs.

- **Clair** : surfaces lumineuses, textes sombres, bordures lisibles.
- **Sombre** : surfaces sombres, textes clairs, niveaux de surface distincts.
- **Contraste élevé** : bordures renforcées, états explicites, dépendance réduite aux ombres et à la couleur.
- **Accent** : couleur sélectionnée, focus, contrôles actifs et indicateurs.
- **Densité** : espacements compacts ou confortables sans réduire les zones interactives.
- **Échelle** : tailles cohérentes à différentes densités d’écran et tailles de police.

GNOME Shell 51 fournit des variantes SCSS clair, sombre et contraste élevé. Le thème doit vérifier chacune des trois.

## 8. Icônes, curseurs, polices et arrière-plans

### 8.1 Icônes

Un thème d’icônes contient `index.theme` et des ressources classées par taille et contexte. Les contextes usuels comprennent Applications, Actions, Devices, Places, Status, MimeTypes, Emblems et Categories. Respecter les noms Freedesktop et les replis vers `hicolor`.

```ini
[Icon Theme]
Name=MonTheme
Comment=Thème d’icônes
Inherits=hicolor
Directories=scalable/apps,scalable/actions

[scalable/apps]
Size=48
Type=Scalable
MinSize=16
MaxSize=256
Context=Applications

[scalable/actions]
Size=16
Type=Scalable
MinSize=16
MaxSize=64
Context=Actions
```

### 8.2 Curseurs

Les curseurs sont des fichiers Xcursor, pas des SVG ordinaires. Prévoir au minimum les rôles pointeur, main, texte, attente, déplacement, redimensionnement dans chaque direction et précision. Hériter d’un thème existant si une ressource manque.

### 8.3 Polices

Documenter famille, graisse, taille, hauteur de ligne et rendu. Les polices sont installées séparément et sélectionnées par les paramètres GNOME / Fontconfig. Ne pas prétendre que le CSS Shell modifie toutes les polices système.

### 8.4 Fonds et images

Le fond du bureau et celui de l’écran verrouillé sont des ressources d’arrière-plan gérées par GNOME, non des widgets CSS. Le paquet doit documenter les images, leur format, leur résolution et leur licence.

## 9. Éléments qui ne sont pas contrôlés par le thème utilisateur

- L’écran GDM dépend du thème système de GDM et de sa configuration ; un thème utilisateur ne le remplace pas automatiquement.
- Les décorations de fenêtres dépendent du compositeur, de Mutter et des décorations côté client.
- Les applications Qt, Electron, web et toolkit propriétaires ont leurs propres moteurs.
- Les extensions GNOME Shell peuvent ajouter des widgets, menus et panneaux avec leurs propres classes.
- Les applications GTK peuvent ajouter des CSS providers et widgets personnalisés.
- Certains composants natifs utilisent des ressources, icônes ou rendus qui ne sont pas pilotés par CSS.

Ces cas doivent être indiqués comme « hors périmètre », « extension » ou « dépend de l’application », pas présentés comme une prise en charge garantie.

## 10. Structure d’un thème exporté

```text
MonTheme/
├── README.md
├── gnome-shell/
│   └── gnome-shell.css
├── gtk-3.0/
│   └── gtk.css
├── gtk-4.0/
│   └── gtk.css
├── libadwaita/
│   └── gtk-4.16.css
├── icons/MonTheme/
│   ├── index.theme
│   ├── scalable/apps/
│   ├── scalable/actions/
│   ├── scalable/devices/
│   ├── scalable/places/
│   └── scalable/status/
├── cursors/MonCurseur/
│   ├── index.theme
│   └── cursors/
├── backgrounds/
└── fonts/
```

Un répertoire vide n’est pas une ressource de thème terminée. L’export doit signaler clairement les ressources absentes.

## 11. Matrice de tests obligatoire

| Zone | Contrôles minimum |
|---|---|
| Panneau | horloge, activités, indicateurs, confidentialité |
| Activités | recherche, résultats, grille, dossiers, pages |
| Dock | lancement, application active, séparateur, glisser-déposer |
| Espaces | miniatures, sélection, aperçu de fenêtre |
| Menus | menu simple, sous-menu, case, interrupteur, séparateur |
| Réglages rapides | réseau, Bluetooth, son, luminosité, alimentation, périphériques |
| Calendrier | mois, jour courant, événements, horloges, météo |
| Notifications | carte, groupe, actions, média, ne pas déranger |
| Dialogues | confirmation, erreur, mot de passe, polkit, fin de session |
| Verrouillage | horloge, saisie, utilisateur, notifications |
| Saisie | clavier virtuel, emoji, IBus, suggestions |
| OSD | volume, luminosité, capture, sélection écran |
| GTK 3 | fenêtre, headerbar, bouton, champ, liste, menu, arbre, onglet |
| GTK 4 | fenêtre, headerbar, boutons, saisie, listes, popovers, défilement |
| Libadwaita | navigation, préférences, lignes, dialogues, bannières, toasts |
| Ressources | icônes manquantes, curseurs, polices, fonds |
| Accessibilité | clavier, focus, contraste élevé, RTL, HiDPI |

Tester chaque zone en clair, sombre et contraste élevé. Valider la syntaxe CSS avec les outils GTK correspondants et utiliser une session GNOME Shell imbriquée pour les tests Shell. Un aperçu statique ne remplace pas un test réel.

## 12. Organisation de l’éditeur G-OS Theme Maker

Le catalogue doit guider l’organisation de l’application :

1. **Cible** : Shell 51, GTK 3, GTK 4, Libadwaita, icônes, curseurs, polices, fonds.
2. **Écran** : choisir une zone d’interface dans la cible.
3. **Composant** : sélectionner le bouton, menu, carte, champ, ligne, etc.
4. **État** : normal, hover, focus, actif, sélectionné, désactivé, erreur.
5. **Propriétés** : couleurs, texte, bordure, rayon, taille, espacement, ombre.
6. **Aperçu** : montrer le composant et ses états, puis valider dans le moteur réel.
7. **Compatibilité** : afficher la version cible et les limites connues.

Ne pas présenter une propriété comme modifiable si le moteur ne l’expose pas. Les composants ajoutés par les extensions doivent être identifiés comme tels.

## 13. Sources et inventaires de référence

### GNOME Shell 51.0 — sources amont exactes

Le catalogue Shell ci-dessus est établi à partir des modules suivants :

- [Thème GNOME Shell 51.0 — répertoire des widgets SCSS](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass/widgets)
- [Panneau](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_panel.scss)
- [Vue Activités et grille](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_overview.scss)
- [Dash](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_dash.scss)
- [Grille d’applications](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_app-grid.scss)
- [Menus et popovers](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_popovers.scss)
- [Réglages rapides](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_quick-settings.scss)
- [Calendrier](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_calendar.scss)
- [Notifications](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_message-list.scss)
- [Dialogues](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_dialogs.scss)
- [Connexion et verrouillage](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_login-lock.scss)
- [Capture d’écran](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_screenshot.scss)
- [Clavier virtuel](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_keyboard.scss)
- [Sélecteur de fenêtres](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_switcher-popup.scss)
- [OSD](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_osd.scss)
- [Accessibilité](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_a11y.scss)

### GTK et Libadwaita

- [GTK 3 — CSS Overview](https://gnome.pages.gitlab.gnome.org/gtk/gtk3/css-overview.html)
- [GTK 3 — Widgets](https://docs.gtk.org/gtk3/)
- [GTK 4 — CSS Overview](https://gnome.pages.gitlab.gnome.org/gtk/gtk4/css-overview.html)
- [GTK 4 — CSS Properties](https://gnome.pages.gitlab.gnome.org/gtk/gtk4/css-properties.html)
- [GTK 4 — référence API](https://docs.gtk.org/gtk4/)
- [Libadwaita — Styles and Appearance](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)
- [Libadwaita — CSS Variables](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/css-variables.html)
- [Libadwaita — référence API](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/)
- [Freedesktop — Icon Theme Specification](https://specifications.freedesktop.org/icon-theme/)
- [GNOME HIG — UI Styling](https://developer.gnome.org/hig/guidelines/ui-styling.html)
