# Atelier pratique : personnaliser GNOME Shell 51

GNOME Shell dessine le panneau, la vue Activités, la grille d'applications, le dock, les menus système, les notifications, les dialogues, les OSD et l'écran verrouillé. Ce chapitre donne une méthode de travail par zone et des exemples de départ.

## Avant de commencer

Vérifiez la version avec `gnome-shell --version`. Les sélecteurs de ce chapitre sont des points de départ pour GNOME Shell 51. Ils peuvent changer entre versions et certaines parties ne sont pas exposées de manière stable. Consultez le CSS et le SCSS de la branche GNOME Shell 51.0 avant de publier un thème.

La feuille utilisateur s'appelle généralement `gnome-shell/gnome-shell.css` dans le paquet de thème. Pour le développement, gardez le fichier dans votre dossier de projet et testez dans une session imbriquée. L'activation d'un thème Shell peut dépendre de l'outil d'extensions et de la configuration de la distribution.

## 1. Panneau supérieur

Le panneau contient Activités, l'horloge et les indicateurs système. Il est principalement repéré par `#panel` et `.panel-button`.

```css
#panel {
  background-color: #20242b;
  color: #f6f5f4;
  border-bottom: 1px solid #414852;
}

#panel .panel-button {
  color: #f6f5f4;
  border-radius: 8px;
  padding: 0 10px;
  margin: 3px 2px;
}

#panel .panel-button:hover,
#panel .panel-button:focus {
  background-color: #394452;
}
```

Pour modifier la hauteur du panneau, il faut d'abord vérifier si la dimension est réellement contrôlée par le style dans la version visée. Une hauteur imposée trop petite peut couper l'horloge, les indicateurs ou les menus. Vérifiez aussi les facteurs d'échelle et les polices.

## 2. Vue Activités et recherche

La vue Activités comprend le fond, les espaces de travail, les aperçus de fenêtres, le champ de recherche et les résultats. Les sélecteurs repères incluent `.search-entry`, `.search-section`, `.grid-search-result`, `.list-search-result` et `.window-picker`.

```css
.search-entry {
  color: #f6f5f4;
  background-color: #303640;
  border: 1px solid #596575;
  border-radius: 12px;
  padding: 10px 14px;
}

.search-entry:focus {
  border-color: #78aeed;
}

.search-section {
  color: #f6f5f4;
}

.grid-search-result,
.list-search-result {
  border-radius: 10px;
}
```

Exercice : changez uniquement le champ de recherche. Vérifiez le texte saisi, l'icône, le focus clavier et le message « aucun résultat ». Ne rendez pas le texte secondaire illisible.

## 3. Grille d'applications et dossiers

Les repères de la grille incluent `.icon-grid`, `.overview-tile`, `.overview-icon`, `.app-folder`, `.app-folder-dialog` et `.page-indicator`.

```css
.overview-tile {
  border-radius: 12px;
}

.app-folder-dialog {
  background-color: #292e36;
  border: 1px solid #4a5360;
  border-radius: 16px;
}

.folder-name-entry {
  color: #f6f5f4;
  background-color: #343b45;
}
```

L'apparence des icônes dépend aussi du thème d'icônes et des ressources installées. CSS peut changer leur taille ou leur conteneur, mais ne remplace pas les fichiers d'icônes eux-mêmes.

## 4. Dock

Les repères courants sont `#dash`, `.dash-background`, `.dash-item-container`, `.dash-separator`, `.show-apps` et `.dash-label`.

```css
#dash .dash-background {
  background-color: rgba(32, 36, 43, 0.94);
  border: 1px solid #596575;
  border-radius: 18px;
}

#dash .dash-item-container {
  border-radius: 10px;
}

#dash .dash-item-container:hover {
  background-color: #394452;
}

#dash .dash-separator {
  background-color: #687383;
}
```

Le CSS dessine le dock, mais le déplacement, l'ordre, les animations, les zones de dépôt et le comportement du lanceur relèvent du code Shell. Un thème ne peut pas corriger un défaut de glisser-déposer.

## 5. Menus et popovers

Un popover est un panneau contextuel attaché à un bouton. Les menus système utilisent notamment `.popup-menu`, `.popup-menu-content`, `.popup-menu-item`, `.popup-sub-menu` et `.popup-separator-menu-item-separator`.

```css
.popup-menu-content {
  background-color: #292e36;
  color: #f6f5f4;
  border: 1px solid #596575;
  border-radius: 12px;
  padding: 6px;
}

.popup-menu-item {
  color: #f6f5f4;
  border-radius: 7px;
  padding: 8px 10px;
}

.popup-menu-item:hover {
  background-color: #394452;
}

.popup-separator-menu-item-separator {
  background-color: #596575;
}
```

Testez les sous-menus, les cases à cocher, les interrupteurs, les éléments désactivés et les menus qui contiennent des curseurs. Un menu système n'est pas un simple rectangle avec du texte.

## 6. Réglages rapides

Les repères incluent `.quick-settings`, `.quick-toggle`, `.quick-toggle-title`, `.quick-toggle-subtitle`, `.quick-slider` et `.quick-toggle-menu`.

```css
.quick-settings {
  color: #f6f5f4;
}

.quick-toggle {
  border-radius: 12px;
}

.quick-toggle:hover {
  background-color: #394452;
}

.quick-toggle-title {
  font-weight: 600;
}

.quick-toggle-subtitle {
  color: #c0c7d1;
}
```

Les éléments visibles dépendent du matériel, du réseau, des services et des extensions. Testez avec et sans Bluetooth, Wi-Fi, périphérique audio ou batterie si ces situations sont disponibles.

## 7. Calendrier, horloges et météo

Repères utiles : `.datemenu-popover`, `.calendar`, `.calendar-day`, `.calendar-today`, `.events-box`, `.world-clocks-grid`, `.weather-box`.

```css
.calendar {
  color: #f6f5f4;
}

.calendar-day {
  border-radius: 8px;
}

.calendar-day.calendar-today {
  background-color: #3584e4;
  color: #ffffff;
}

.events-box,
.weather-box {
  color: #f6f5f4;
}
```

Testez le jour courant, les autres mois, les jours avec événements, l'absence d'événement, les textes longs et les différentes langues.

## 8. Notifications et médias

Les classes de référence comprennent `.message-list`, `.message`, `.message-header`, `.message-content`, `.notification-banner`, `.notification-button` et `.media-message`.

```css
.message,
.notification-banner {
  background-color: #303640;
  color: #f6f5f4;
  border: 1px solid #596575;
  border-radius: 12px;
}

.message-title {
  font-weight: 700;
}

.notification-button {
  border-radius: 8px;
}
```

Vérifiez les notifications empilées, les groupes, les boutons d'action, les images, les contrôles multimédias et les messages très longs.

## 9. Dialogues, verrouillage et OSD

Les dialogues peuvent contenir des listes, des champs de mot de passe, des avertissements et des boutons de confirmation. Les OSD indiquent par exemple le volume ou la luminosité. Le verrouillage est un contexte distinct du bureau normal.

Repères Shell à explorer dans les sources 51.0 : `.modal-dialog`, `.modal-dialog-button`, `.prompt-dialog`, `.run-dialog`, `.osd-window`, `.login-dialog` et les classes de `_login-lock.scss`. Ne copiez pas un sélecteur avant de l'avoir confirmé dans le fichier SCSS correspondant.

Exercice : repérez un dialogue de confirmation dans la session de test, identifiez le conteneur, le texte, les boutons et les états de focus. Modifiez d'abord le rayon et la bordure du conteneur, puis le bouton principal. Vérifiez que l'avertissement reste visible.

## 10. Méthode pour couvrir les éléments restants

Pour chaque module listé dans le catalogue Shell :
1. ouvrez la zone dans GNOME ;
2. identifiez le module SCSS correspondant dans `data/theme/gnome-shell-sass/widgets/` ;
3. recherchez les noms de classes et identifiants dans le fichier ;
4. notez les éléments enfants et leurs états ;
5. ajoutez une règle ciblée dans votre feuille ;
6. testez les états normal, hover, focus, actif et désactivé ;
7. vérifiez clair, sombre, contraste élevé, HiDPI et RTL ;
8. notez les éléments qui nécessitent du code ou une extension plutôt que du CSS.

## Limites à connaître

Les sélecteurs Shell sont des détails d'implémentation. Une extension peut ajouter des composants qui ne figurent pas dans le thème natif. Une mise à jour GNOME peut modifier les noms et la structure. Les changements de comportement, animations, disposition ou glisser-déposer ne sont pas garantis par CSS.
