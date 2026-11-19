# 43. GNOME Shell 51.0 : inventaire pratique des sélecteurs du thème

Ce chapitre est un index de travail des sélecteurs CSS visibles dans les feuilles SCSS livrées avec GNOME Shell 51.0. Il complète les chapitres consacrés au panneau, à la vue Activités, aux menus, aux notifications et aux composants spécialisés.

La référence est le code source officiel, tagué `51.0`, dans `data/theme/gnome-shell-sass/widgets/`. Les sélecteurs ci-dessous sont relevés dans ces feuilles, pas déduits d'une capture d'écran.

**Important :** cet inventaire décrit le thème fourni par GNOME Shell 51.0. Il ne constitue pas une API stable. Un composant peut être construit dynamiquement par GJS, recevoir des classes selon son état, ou ne pas exister dans une configuration donnée. Avant de publier une règle, inspectez la session GNOME 51 réellement ciblée.

## 1. Retrouver la source correspondant à un composant

Le thème Shell est maintenu sous forme de SCSS et compilé en CSS. Le répertoire des widgets permet de retrouver les styles par famille :

```text
data/theme/gnome-shell-sass/
  widgets/
    _panel.scss
    _overview.scss
    _dash.scss
    _calendar.scss
    _quick-settings.scss
    _popovers.scss
    _notifications.scss
    _search-results.scss
    _workspace-thumbnails.scss
    _osd.scss
```

Pour vérifier une classe, consultez d'abord le fichier de style, puis le code GJS qui crée l'acteur. Le SCSS indique les règles attendues ; le code GJS explique à quel moment l'acteur reçoit une classe et quelle structure de nœuds est construite.

Un nom présent dans un fichier SCSS n'est pas forcément visible en permanence. Il peut être réservé à un état ou à une fonctionnalité facultative.

## 2. Panneau supérieur

Source : `widgets/_panel.scss`.

Le conteneur principal est `#panel`. Il change d'apparence suivant l'état de la session. Le code 51.0 cible notamment les états `:overview`, `.unlock-screen` et `.login-screen`.

Sélecteurs relevés :

- `#panel` : panneau supérieur ;
- `#panel .panel-button` : boutons et zones interactives du panneau ;
- `#panel #panelActivities` : zone Activités ;
- `#panel #panelActivities .workspace-dot` : indicateurs de bureaux ;
- `#panel .screen-recording-indicator` : indicateur d'enregistrement ;
- `#panel .screen-sharing-indicator` : indicateur de partage d'écran ;
- `#panel .clock-display` : zone de l'horloge ;
- `#panel .clock-display .clock` : texte de l'horloge ;
- `#panel .clock-display .messages-indicator` : indicateur de messages ;
- `#panel .panel-status-indicators-box` : groupe d'indicateurs ;
- `#panel .privacy-indicator` : indicateur de confidentialité ;
- `.clock-display-box` : conteneur de l'affichage de l'horloge.

Exemple limité au panneau de la session normale :

```css
#panel {
  background-color: #20242b;
}

#panel .panel-button {
  color: #f6f5f4;
}

#panel .panel-button:hover {
  background-color: rgba(255, 255, 255, 0.12);
}
```

Ne supposez pas que la règle s'applique de la même manière à l'overview ou à l'écran verrouillé. Le thème GNOME définit explicitement des styles différents pour ces contextes. Vérifiez aussi le comportement de l'horloge lorsque l'indicateur Ne pas déranger est présent.

## 3. Vue Activités et arrière-plan

Source : `widgets/_overview.scss`.

Le groupe principal est `#overviewGroup`. Les aperçus sur les écrans secondaires sont organisés dans `.secondary-monitor-workspaces`.

```css
#overviewGroup {
  background-color: #17191d;
}

.secondary-monitor-workspaces {
  spacing: 12px;
}
```

Cette feuille est volontairement courte : une grande partie des composants de la vue Activités est définie dans les feuilles spécialisées, notamment le dash, les résultats de recherche, le sélecteur de fenêtres et les miniatures d'espaces de travail. Ne cherchez pas tous les styles de l'overview dans un unique fichier.

## 4. Dash et lanceurs

Source : `widgets/_dash.scss`.

Sélecteurs relevés :

- `#dash` : conteneur du dash ;
- `#dash .dash-background` : fond derrière les éléments ;
- `#dash .dash-item-container` : zone des lanceurs ;
- `#dash .placeholder` : emplacement temporaire pendant un déplacement ;
- `#dash .empty-dash-drop-target` : cible de dépôt lorsque le dash est vide ;
- `#dash .show-apps` : bouton Afficher les applications ;
- `#dash .overview-tile` : tuile de lanceur ;
- `#dash .overview-icon` : icône et surface interactive de la tuile ;
- `#dash .app-grid-running-dot` : indicateur d'application en cours ;
- `#dash .dash-separator` : séparation favoris/applications actives ;
- `.dash-label` : infobulle d'un lanceur.

Exemple :

```css
#dash .dash-background {
  border-radius: 20px;
  background-color: rgba(32, 36, 43, 0.94);
}

#dash .overview-icon {
  border-radius: 14px;
}

#dash .overview-tile:hover .overview-icon {
  background-color: rgba(255, 255, 255, 0.14);
}
```

Le placeholder et la cible de dépôt ne sont pas les lanceurs eux-mêmes. Leur apparence doit être testée pendant un vrai glisser-déposer. Une feuille CSS ne peut pas réparer une logique de déplacement incorrecte.

## 5. Calendrier, horloge et météo

Source : `widgets/_calendar.scss`.

Conteneur et cartes :

- `#calendarArea` : zone du calendrier ;
- `.datemenu-popover` : popover de date et heure ;
- `.datemenu-calendar-column` : colonne calendrier ;
- `.datemenu-displays-box` : zone des horloges et affichages ;
- `.datemenu-today-button` : bouton de date du jour ;
- `.calendar` : calendrier mensuel ;
- `.calendar-month-header` : en-tête du mois ;
- `.calendar-change-month-back` et `.calendar-change-month-forward` : navigation du mois ;
- `.calendar-month-label` : libellé du mois ;
- `.calendar-day` : cellule d'un jour ;
- `.calendar-weekday` : jour de semaine ;
- `.calendar-weekend` : samedi/dimanche ;
- `.calendar-other-month` : jour appartenant au mois adjacent ;
- `.calendar-today` : jour courant ;
- `.calendar-day-with-events` : jour avec événement ;
- `.calendar-day-heading` : en-tête des jours ;
- `.calendar-week-number` : numéro de semaine.

Cartes et événements :

- `.events-button`, `.world-clocks-button`, `.weather-button` ;
- `.events-title`, `.events-list`, `.event-box`, `.event-summary`, `.event-time`, `.event-placeholder` ;
- `.world-clocks-header`, `.world-clocks-grid`, `.world-clocks-city`, `.world-clocks-time`, `.world-clocks-timezone` ;
- `.weather-box`, `.weather-header-box`, `.weather-header`, `.weather-grid`.

Exemple :

```css
.calendar .calendar-day {
  border-radius: 999px;
}

.calendar .calendar-day.calendar-today {
  font-weight: 700;
}

.calendar .calendar-day.calendar-other-month {
  opacity: 0.55;
}
```

Ne supprimez pas les distinctions visuelles entre le jour courant, le jour sélectionné, les jours du mois précédent/suivant et les jours avec événements. Le contraste élevé doit également rester compréhensible.

## 6. Réglages rapides

Source : `widgets/_quick-settings.scss`.

Les classes structurantes relevées comprennent :

- `.quick-settings` : panneau des réglages rapides ;
- `.quick-settings-grid` : grille des contrôles ;
- `.quick-toggle` : bascule autonome ;
- `.quick-toggle-has-menu` : contrôle avec menu associé ;
- `.quick-toggle-title` et `.quick-toggle-subtitle` : textes principal et secondaire ;
- `.quick-toggle-icon` : icône du contrôle ;
- `.quick-toggle-menu-button` : bouton ouvrant le menu associé ;
- `.quick-toggle-separator` : séparation entre les deux parties ;
- `.quick-slider` : contrôle de type curseur ;
- `.slider-bin` : zone interactive du curseur ;
- `.quick-toggle-menu` : menu détaillé d'un contrôle ;
- `.quick-settings-system-item` : élément système ;
- `.header`, `.title`, `.subtitle` dans l'en-tête du menu.

Le code distingue explicitement les états `:checked`, `:focus`, `:hover`, `:active`, `:insensitive`, ainsi que les directions `:ltr` et `:rtl`.

Exemple :

```css
.quick-toggle {
  border-radius: 18px;
}

.quick-toggle:checked {
  font-weight: 700;
}

.quick-toggle:focus,
.quick-toggle-menu-button:focus {
  outline: 2px solid -st-accent-color;
}
```

La propriété `outline` et la couleur système doivent être testées dans la version cible. Conservez toujours un indicateur de focus visible. Les contrôles avec menu ont une géométrie différente en LTR et RTL ; ne remplacez pas leurs rayons de bordure par une règle uniforme.

## 7. Menus et popovers

Source : `widgets/_popovers.scss`.

Sélecteurs principaux :

- `.popup-menu-boxpointer` : pointe du menu ;
- `.popup-menu` : conteneur du menu ;
- `.popup-menu.panel-menu` : menu associé au panneau ;
- `.popup-menu-content` : surface du menu ;
- `.popup-menu-item` : entrée interactive ;
- `.popup-ornamented-menu-item` : entrée avec ornement ;
- `.popup-inactive-menu-item` : texte ou entrée non interactive ;
- `.popup-menu-arrow` et `.popup-menu-icon` : flèche et icône ;
- `.popup-sub-menu` : sous-menu ;
- `.popup-separator-menu-item` : entrée séparatrice ;
- `.popup-separator-menu-item-separator` : trait du séparateur ;
- `.popup-menu-ornament` : emplacement de coche ou radio ;
- `.background-menu` : menu contextuel du bureau ;
- `.app-menu` : menu d'application.

Les états de menu sont importants : `:checked`, `:hover`, `:focus`, `:active` et `:insensitive`. Le thème distingue aussi les menus LTR/RTL et les derniers éléments d'un sous-menu pour conserver des coins cohérents.

Exemple :

```css
.popup-menu-content {
  border-radius: 16px;
  padding: 8px;
}

.popup-menu-item {
  border-radius: 10px;
}

.popup-menu-item:hover,
.popup-menu-item:focus {
  background-color: rgba(255, 255, 255, 0.12);
}
```

Une règle générale sur `.popup-menu-item` peut affecter les entrées de plusieurs menus. Inspectez le menu précis avant d'ajouter des sélecteurs globaux.

## 8. Recherche et résultats

Source : `widgets/_search-results.scss`.

Sélecteurs relevés :

- `#searchResults` et `#searchResultsContent` : conteneurs des résultats ;
- `.search-section` et `.search-section-separator` : groupes de résultats ;
- `.search-section-content` : surface d'une section ;
- `.search-statusbox` et `.search-statustext` : état de recherche vide ou message ;
- `.grid-search-results` et `.grid-search-result` : résultats sous forme de grille ;
- `.search-provider-icon` : icône d'un fournisseur ;
- `.list-search-provider-content` et `.list-search-provider-details` : informations du fournisseur ;
- `.list-search-results` et `.list-search-result` : résultats sous forme de liste ;
- `.list-search-result-content`, `.list-search-result-title`, `.list-search-result-description` : contenu du résultat.

Exemple :

```css
.search-section-content {
  border-radius: 18px;
}

.list-search-result {
  border-radius: 12px;
}

.search-statustext {
  font-weight: 600;
}
```

Testez la recherche vide, les résultats, l'absence de résultats, les fournisseurs différents, les libellés longs et la sélection clavier. Le thème ne doit pas rendre illisible une description secondaire.

## 9. Notifications

Source : `widgets/_notifications.scss`.

Sélecteurs présents :

- `.notification-banner` : bannière de notification ;
- `.notification-buttons-bin` : groupe des boutons d'action ;
- `.notification-button` : bouton de notification.

Exemple :

```css
.notification-banner {
  border-radius: 16px;
  margin: 8px;
}

.notification-button {
  border-radius: 10px;
}
```

Les notifications peuvent contenir du texte long, des images, plusieurs actions ou être regroupées. Une bannière visuellement jolie mais dont les actions sortent de la surface n'est pas un thème correct. Vérifiez les notifications privées sur écran verrouillé.

## 10. OSD et affichages temporaires

Source : `widgets/_osd.scss`.

Sélecteurs relevés :

- `.osd-window` : fenêtre d'affichage temporaire ;
- `.level` : niveau représenté, par exemple volume ou luminosité ;
- `.osd-monitor-label` : indication d'écran ;
- `.osd-break-countdown-label` : compte à rebours ;
- `.pad-osd-window` : affichage lié à la tablette ;
- `.pad-osd-title-box` et `.pad-osd-title-menu-box` : zones de titre ;
- `.combo-box-label` : libellé de sélection ;
- `.resize-popup` : indication de redimensionnement.

Exemple :

```css
.osd-window {
  border-radius: 18px;
  padding: 16px 22px;
}

.osd-monitor-label {
  border-radius: 12px;
}
```

Les niveaux utilisent des propriétés spécifiques au composant St BarLevel, par exemple `-barlevel-height`, `-barlevel-background-color` et `-barlevel-active-background-color`. Ce ne sont pas des propriétés CSS web standard. Consultez la documentation St et les sources Shell avant de les modifier.

## 11. Miniatures des espaces de travail

Source : `widgets/_workspace-thumbnails.scss`.

Sélecteurs :

- `.workspace-thumbnails` : ensemble des miniatures ;
- `.workspace-thumbnail` : miniature individuelle ;
- `.workspace-thumbnail-indicator` : indicateur de l'espace sélectionné ;
- `.placeholder` : emplacement temporaire pendant un déplacement.

Exemple :

```css
.workspace-thumbnail {
  border-radius: 8px;
}

.workspace-thumbnail-indicator {
  border-width: 3px;
}
```

Vérifiez l'espace courant, les espaces non sélectionnés, le déplacement d'une fenêtre et la navigation au clavier. Sur plusieurs écrans, les miniatures secondaires utilisent aussi des conteneurs spécifiques.

## 12. Pseudo-classes et propriétés propres à St

Les feuilles GNOME Shell emploient des pseudo-classes et propriétés qui ne doivent pas être confondues avec les fonctionnalités GTK ou celles d'un navigateur.

Exemples observés dans les sources 51.0 :

- états interactifs : `:hover`, `:focus`, `:active`, `:checked`, `:insensitive` ;
- direction : `:ltr`, `:rtl` ;
- état de l'overview : `#panel:overview` ;
- propriétés St : `icon-size`, `spacing`, `spacing-rows`, `spacing-columns`, `-natural-hpadding`, `-minimum-hpadding`, `-st-icon-style`, `-barlevel-height`, `-barlevel-background-color`, `-barlevel-active-background-color`.

La liste n'est pas une grammaire exhaustive. Pour chaque propriété, vérifiez qu'elle est prise en charge par le type d'acteur concerné. Une propriété St copiée dans une feuille GTK peut être ignorée ou signalée comme inconnue.

## 13. Procédure de vérification d'un sélecteur

Pour chaque règle ajoutée :

1. Identifiez le composant dans GNOME Shell 51.0.
2. Retrouvez son SCSS dans le tag source `51.0`.
3. Cherchez le nom de classe ou l'identifiant dans le code GJS.
4. Ouvrez Looking Glass et inspectez l'arbre d'acteurs si nécessaire.
5. Vérifiez la présence de l'acteur et de ses classes dans l'état visé.
6. Ajoutez une règle minimale et distinctive dans une copie de test.
7. Vérifiez les états normal, survol, focus, actif, sélectionné et désactivé.
8. Vérifiez LTR et RTL pour les composants directionnels.
9. Vérifiez clair, sombre et contraste élevé.
10. Retirez la règle de test et consignez le sélecteur validé.

Ne testez pas uniquement le bureau au repos. Les composants temporaires (menus, OSD, notifications, dialogues) doivent être provoqués pour apparaître.

## 14. Pourquoi ce catalogue n'est pas un contrat de compatibilité

GNOME Shell est développé avec GJS et St. Les acteurs et leurs classes évoluent avec l'implémentation. Une extension peut ajouter, retirer ou modifier des classes. Un composant peut aussi être construit seulement lorsque son service ou son matériel est disponible.

Par conséquent :

- un sélecteur de thème Shell n'est pas une API publique stable ;
- une classe privée peut changer entre deux versions mineures ou majeures ;
- une classe présente dans le SCSS peut être absente dans une session donnée ;
- une extension peut introduire une collision de noms ;
- un sélecteur trop général peut modifier plusieurs composants sans intention.

Conservez une copie du thème par version majeure et vérifiez les différences de sources lors d'une mise à niveau.

## 15. Sources GNOME 51.0

Sources primaires utilisées pour cet inventaire :

- [GNOME Shell 51.0 — thème SCSS](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass)
- [Panneau supérieur — _panel.scss](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_panel.scss)
- [Réglages rapides — _quick-settings.scss](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_quick-settings.scss)
- [Vue Activités — _overview.scss](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_overview.scss)
- [Dash — _dash.scss](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_dash.scss)
- [Calendrier — _calendar.scss](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_calendar.scss)
- [Menus — _popovers.scss](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_popovers.scss)
- [Recherche — _search-results.scss](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_search-results.scss)
- [Notifications — _notifications.scss](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_notifications.scss)
- [OSD — _osd.scss](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_osd.scss)
- [Espaces de travail — _workspace-thumbnails.scss](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_workspace-thumbnails.scss)
