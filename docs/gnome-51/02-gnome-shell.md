# 2. GNOME Shell 51

## 2. GNOME Shell 51 : inventaire complet des familles

Les noms ci-dessous proviennent de l’organisation des sources SCSS de GNOME Shell 51.0, dans `data/theme/gnome-shell-sass/widgets/`. Les sélecteurs sont des détails d’implémentation, pas une API stable. Toujours vérifier le code de la version ciblée.

#### 3. Panneau supérieur et indicateurs

- **Élément** : Panneau supérieur ; **Sélecteurs / classes repères** : `#panel` ; **Ce qui doit être personnalisable** : fond, hauteur, bordure, typographie, ombre
- **Élément** : Boutons du panneau ; **Sélecteurs / classes repères** : `.panel-button` ; **Ce qui doit être personnalisable** : fond, texte, marges, padding, rayon
- **Élément** : Activités ; **Sélecteurs / classes repères** : `#panelActivities` ; **Ce qui doit être personnalisable** : libellé, points d’espaces de travail
- **Élément** : Horloge ; **Sélecteurs / classes repères** : `.clock-display`, `.clock-display-box`, `.clock` ; **Ce qui doit être personnalisable** : texte, espacement, survol
- **Élément** : Indicateurs système ; **Sélecteurs / classes repères** : `.system-status-icon`, `.panel-status-indicators-box` ; **Ce qui doit être personnalisable** : taille et couleur des icônes
- **Élément** : Notifications du panneau ; **Sélecteurs / classes repères** : `.messages-indicator` ; **Ce qui doit être personnalisable** : icône et état actif
- **Élément** : Enregistrement écran ; **Sélecteurs / classes repères** : `.screen-recording-indicator` ; **Ce qui doit être personnalisable** : indicateur de confidentialité
- **Élément** : Partage écran ; **Sélecteurs / classes repères** : `.screen-sharing-indicator` ; **Ce qui doit être personnalisable** : indicateur de confidentialité
- **Élément** : Confidentialité ; **Sélecteurs / classes repères** : `.privacy-indicator` ; **Ce qui doit être personnalisable** : couleur d’avertissement

Exemple :

```css
#panel { background-color: #20242b; color: #ffffff; }
#panel .panel-button { border-radius: 8px; padding: 0 8px; }
#panel .panel-button:hover,
#panel .panel-button:focus { background-color: #3584e4; }
```

#### 4. Vue Activités, recherche et navigation

- **Élément** : Fond de la vue Activités ; **Sélecteurs / classes repères** : `#overviewGroup`, `#overview` selon version ; **Couverture visuelle** : fond, voile, contraste
- **Élément** : Conteneur des résultats ; **Sélecteurs / classes repères** : `#searchResults`, `#searchResultsContent` ; **Couverture visuelle** : largeur, marges
- **Élément** : Section de recherche ; **Sélecteurs / classes repères** : `.search-section`, `.search-section-content`, `.search-section-separator` ; **Couverture visuelle** : panneaux et séparateurs
- **Élément** : Champ de recherche ; **Sélecteurs / classes repères** : `.search-entry`, `.search-entry-icon` ; **Couverture visuelle** : saisie, icône, focus
- **Élément** : État de recherche ; **Sélecteurs / classes repères** : `.search-statusbox`, `.search-statustext` ; **Couverture visuelle** : chargement, aucun résultat
- **Élément** : Résultats en grille ; **Sélecteurs / classes repères** : `.grid-search-results`, `.grid-search-result` ; **Couverture visuelle** : tuiles et espacement
- **Élément** : Résultats en liste ; **Sélecteurs / classes repères** : `.list-search-results`, `.list-search-result` ; **Couverture visuelle** : lignes, titres, descriptions
- **Élément** : Fournisseurs de recherche ; **Sélecteurs / classes repères** : `.search-provider-icon`, `.list-search-provider-content` ; **Couverture visuelle** : icône et métadonnées
- **Élément** : Aperçu des fenêtres ; **Sélecteurs / classes repères** : `.window-picker`, `.window-icon`, `.window-caption` ; **Couverture visuelle** : espacement, icône, légende
- **Élément** : Bouton fermer une fenêtre ; **Sélecteurs / classes repères** : `.window-close` ; **Couverture visuelle** : taille, forme, états
- **Élément** : Fond d’espace de travail ; **Sélecteurs / classes repères** : `.workspace-background` ; **Couverture visuelle** : fond et ombre
- **Élément** : Prévisualisation de mosaïque ; **Sélecteurs / classes repères** : `.tile-preview` ; **Couverture visuelle** : contour et couleur d’accent
- **Élément** : Écrans secondaires ; **Sélecteurs / classes repères** : `.secondary-monitor-workspaces` ; **Couverture visuelle** : espacement

#### 5. Grille d’applications et dock

- **Élément** : Grille ; **Sélecteurs / classes repères** : `.icon-grid`, `.apps-scroll-view` ; **Couverture visuelle** : espacements et marges
- **Élément** : Tuile d’application ; **Sélecteurs / classes repères** : `.overview-tile`, `.overview-icon` ; **Couverture visuelle** : fond, rayon, padding
- **Élément** : Icône et libellé ; **Sélecteurs / classes repères** : `.overview-icon-with-label` ; **Couverture visuelle** : taille, typographie, écart
- **Élément** : Indicateur application active ; **Sélecteurs / classes repères** : `.app-grid-running-dot` ; **Couverture visuelle** : taille et couleur
- **Élément** : Dossier d’applications ; **Sélecteurs / classes repères** : `.app-folder`, `.app-folder-dialog` ; **Couverture visuelle** : panneau, grille, bordure
- **Élément** : Nom du dossier ; **Sélecteurs / classes repères** : `.folder-name-container`, `.folder-name-entry` ; **Couverture visuelle** : titre et champ de saisie
- **Élément** : Boutons du dossier ; **Sélecteurs / classes repères** : `.icon-button` ; **Couverture visuelle** : icônes et états
- **Élément** : Pagination ; **Sélecteurs / classes repères** : `.page-indicator`, `.page-indicator-icon` ; **Couverture visuelle** : points et sélection
- **Élément** : Navigation entre pages ; **Sélecteurs / classes repères** : `.page-navigation-arrow`, `.page-navigation-hint` ; **Couverture visuelle** : flèches et zones de transition
- **Élément** : Actions système de la grille ; **Sélecteurs / classes repères** : `.system-action-icon` ; **Couverture visuelle** : arrêt et autres actions
- **Élément** : Dock ; **Sélecteurs / classes repères** : `#dash`, `.dash-background` ; **Couverture visuelle** : panneau, fond, rayon
- **Élément** : Éléments du dock ; **Sélecteurs / classes repères** : `.dash-item-container`, `.show-apps`, `.overview-tile` ; **Couverture visuelle** : icônes, focus, survol
- **Élément** : Séparateur du dock ; **Sélecteurs / classes repères** : `.dash-separator` ; **Couverture visuelle** : épaisseur et couleur
- **Élément** : Emplacement de glisser-déposer ; **Sélecteurs / classes repères** : `.placeholder`, `.empty-dash-drop-target` ; **Couverture visuelle** : taille et état cible
- **Élément** : Infobulle du dock ; **Sélecteurs / classes repères** : `.dash-label` ; **Couverture visuelle** : fond, texte, ombre

#### 6. Espaces de travail et changement de fenêtre

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

#### 7. Menus, popovers et menus contextuels

- **Élément** : Conteneur du menu ; **Sélecteurs / classes repères** : `.popup-menu`, `.popup-menu-content`
- **Élément** : Flèche du popover ; **Sélecteurs / classes repères** : `.popup-menu-boxpointer`
- **Élément** : Élément de menu ; **Sélecteurs / classes repères** : `.popup-menu-item`
- **Élément** : Élément inactif ; **Sélecteurs / classes repères** : `.popup-inactive-menu-item`
- **Élément** : Élément ornementé ; **Sélecteurs / classes repères** : `.popup-ornamented-menu-item`, `.popup-menu-ornament`
- **Élément** : Icône et flèche ; **Sélecteurs / classes repères** : `.popup-menu-icon`, `.popup-menu-arrow`
- **Élément** : Sous-menu ; **Sélecteurs / classes repères** : `.popup-sub-menu`
- **Élément** : Séparateur ; **Sélecteurs / classes repères** : `.popup-separator-menu-item`, `.popup-separator-menu-item-separator`
- **Élément** : Menu d’application ; **Sélecteurs / classes repères** : `.app-menu`
- **Élément** : Menu contextuel du fond ; **Sélecteurs / classes repères** : `.background-menu`
- **Élément** : Cases et interrupteurs ; **Sélecteurs / classes repères** : `.check-box`, `.toggle-switch`

Ne pas supposer que le style d’un élément parent suffit : les sous-menus, ornements, cases, séparateurs et éléments désactivés possèdent leurs propres états.

#### 8. Réglages rapides et état du système

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

#### 9. Date, calendrier, événements, horloges et météo

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

#### 10. Notifications et contrôles multimédias

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

#### 11. Dialogues, authentification et session

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

## Méthode de personnalisation et variantes

Les inventaires précédents répondent à la question « où se trouve le composant ? ». Cette partie explique dans quel ordre le modifier et comment éviter les effets de bord.

### Sources et variantes

Le thème amont 51 est produit depuis `data/theme/gnome-shell-sass/`. Les variantes générées incluent clair, sombre et contraste élevé. Sources importantes : `_colors.scss`, `_default-colors.scss`, `_high-contrast-colors.scss`, `_common.scss` et `widgets/*.scss`. Les variables SCSS sont résolues à la compilation : elles ne sont pas des variables CSS dynamiques du thème final.

### 4. Palette sémantique

Définir fond, surface, surface élevée, popover, dialogue, texte principal/secondaire/désactivé, accent normal/hover/pressed, bordure, séparateur, focus, sélection, succès, avertissement, erreur et information. Construire trois palettes cohérentes, ne pas simplement inverser les couleurs.

### 5. Panneau et indicateurs

Tester repos, hover, focus, pressed, menu ouvert, application active et notification en attente. Vérifier horloge, date, activités, indicateurs de confidentialité, enregistrement et partage d'écran. Ces indicateurs dépendent des services actifs.

### 6. Activités, recherche et dock

Couvrir recherche vide/en saisie/aucun résultat, résultats liste/grille, fournisseur, libellés longs, icônes absentes, dossier ouvert/fermé/renommé, pagination, multi-écrans, miniatures, sélection de fenêtre, dock masqué/visible, favoris, applications actives, infobulles et glisser-déposer. Le placeholder et la cible DnD doivent être testés fonctionnellement : le CSS ne corrige pas un DnD cassé.

### 7. Menus et réglages rapides

Tester élément normal, survolé, sélectionné, désactivé, sous-menu, séparateur, case, toggle, icône, raccourci, texte secondaire et menu défilant. Les réglages rapides varient selon matériel : Wi-Fi, Bluetooth, audio, alimentation, luminosité, périphériques et applications d'arrière-plan.

### 8. Calendrier, événements et météo

Tester navigation mois, jours hors mois, aujourd'hui, sélection, événements, fuseaux horaires, plusieurs horloges, prévisions et absence de données. La météo et les événements dépendent de services externes.

### 9. Notifications et média

Couvrir carte seule/empilée, groupe replié/déplié, source, icône, image, texte long, actions, lien, média, fermeture, suppression et état vide.

### 10. Dialogues, authentification et verrouillage

Couvrir dialogues génériques, fin de session, exécution de commande, Polkit, mot de passe, montage chiffré, choix audio, verrouillage, sélection utilisateur, méthode d'authentification, erreurs et notifications privées. Ne jamais masquer les erreurs, le focus ou les indications de sécurité.

### 11. Capture, OSD, clavier et accessibilité

Tester capture écran/fenêtre/zone, poignées, pointeur, enregistrement, volume, luminosité, tablette, compte à rebours, clavier virtuel, emoji, IBus, suggestions, loupe et aides visuelles.

## 2.10 Activation et limites

Le thème utilisateur est généralement installé sous `~/.themes/NOM/gnome-shell/gnome-shell.css` et activé par un mécanisme compatible de gestion de thème Shell. Ne jamais écraser `/usr/share/gnome-shell`. GDM est une cible séparée. Les extensions peuvent ajouter leurs propres nœuds. Tester dans Shell 51 réel après la session imbriquée.
