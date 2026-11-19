# 10. Sources officielles et inventaire GNOME 51

## GNOME 51
- [Notes de version](https://release.gnome.org/51/)
- [GNOME Shell 51.0](https://github.com/GNOME/gnome-shell/tree/51.0)
- [Schéma GSettings Shell 51](https://github.com/GNOME/gnome-shell/blob/51.0/data/org.gnome.shell.gschema.xml.in)
- [Thème SCSS](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass)
- [Widgets SCSS](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass/widgets)
- [Mutter](https://gitlab.gnome.org/GNOME/mutter)
- [GNOME Control Center](https://gitlab.gnome.org/GNOME/gnome-control-center)
- [GNOME Settings Daemon](https://gitlab.gnome.org/GNOME/gnome-settings-daemon)

## GTK / Libadwaita
- [GTK 3 CSS overview](https://docs.gtk.org/gtk3/css-overview.html)
- [GTK 3 CSS properties](https://docs.gtk.org/gtk3/css-properties.html)
- [GTK 4 CSS overview](https://docs.gtk.org/gtk4/css-overview.html)
- [GTK 4 CSS properties](https://docs.gtk.org/gtk4/css-properties.html)
- [Libadwaita styles](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)
- [Libadwaita CSS variables](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/css-variables.html)

## Standards
- [Freedesktop Icon Theme](https://specifications.freedesktop.org/icon-theme/)
- [Icon Naming Specification](https://specifications.freedesktop.org/icon-naming-spec/)
- [Xcursor](https://www.x.org/releases/current/doc/libXcursor/)
- [Fontconfig](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)
- [XDG Base Directory](https://specifications.freedesktop.org/basedir-spec/latest/)
- [GNOME HIG](https://developer.gnome.org/hig/)

## Inventaire des modules de thème Shell 51

`_a11y.scss` accessibilité ; `_app-grid.scss` grille ; `_base.scss` base ; `_buttons.scss` boutons ; `_calendar.scss` calendrier ; `_check-box.scss` cases ; `_corner-ripple.scss` retour clic ; `_dash.scss` dock ; `_dialogs.scss` dialogues ; `_entries.scss` champs ; `_ibus-popup.scss` saisie ; `_keyboard.scss` clavier ; `_login-lock.scss` connexion/verrouillage ; `_looking-glass.scss` inspecteur ; `_message-list.scss` notifications ; `_misc.scss` divers ; `_notifications.scss` notifications ; `_osd.scss` OSD ; `_overview.scss` Activités ; `_panel.scss` panneau ; `_popovers.scss` menus ; `_qr-code.scss` QR ; `_quick-settings.scss` réglages ; `_screenshot.scss` capture ; `_scrollbars.scss` défilement ; `_search-entry.scss` recherche ; `_search-results.scss` résultats ; `_slider.scss` curseurs ; `_switcher-popup.scss` sélecteur fenêtres ; `_switches.scss` interrupteurs ; `_window-picker.scss` fenêtres ; `_workspace-switcher.scss` espaces ; `_workspace-thumbnails.scss` miniatures.

## Maintenir la couverture

À chaque version majeure : comparer les fichiers SCSS, schémas GSettings, notes de version, propriétés GTK, variables Libadwaita et résultats de tests. Les sélecteurs Shell ne sont pas stables ; ce catalogue 51 n'est pas une garantie pour les versions futures.



## Vérifier la version réellement installée

Le numéro « GNOME 51 » désigne une version de l'environnement, mais une distribution peut livrer des révisions différentes de Shell, Mutter, GTK et Libadwaita. Ne déduisez pas les versions des bibliothèques du seul numéro de GNOME.

Commencez par relever l'environnement :

```sh
gnome-shell --version
mutter --version 2>/dev/null || true
echo "Session : $XDG_SESSION_TYPE"
```

Pour les bibliothèques, si les fichiers de développement sont installés :

```sh
pkg-config --modversion gtk+-3.0
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
```

Une commande `pkg-config` qui échoue peut simplement indiquer l'absence du paquet de développement. Elle ne prouve pas que la bibliothèque d'exécution est absente. Pour connaître les paquets installés, utilisez le gestionnaire de paquets de votre distribution.

Notez ces versions dans votre carnet de test. Une règle CSS validée avec GTK 4.23 ne doit pas être présentée comme vérifiée avec toutes les versions GTK 4.

## Récupérer et examiner les sources GNOME 51

Pour étudier le code correspondant à cette documentation, clonez les dépôts officiels dans un répertoire de travail. Ces commandes ne modifient pas votre installation :

```sh
mkdir -p ~/Sources/gnome-51
cd ~/Sources/gnome-51
git clone https://github.com/GNOME/gnome-shell.git
cd gnome-shell
git checkout 51.0
git describe --tags --always
```

Le dernier résultat permet de vérifier la révision examinée. Pour retrouver les règles de style, cherchez dans les sources SCSS :

```sh
grep -RIn --include='*.scss' \
  -E '(^|[[:space:]])\.panel|\.quick-settings|\.notification' \
  data/theme/gnome-shell-sass
```

Pour retrouver l'origine d'un sélecteur ou d'une variable, utilisez aussi :

```sh
git grep -n 'quick-settings'
git grep -n 'panel-corner'
```

Les résultats doivent être lus dans leur contexte : une occurrence peut être un commentaire, un nom de variable SCSS ou un sélecteur compilé. Ne copiez pas automatiquement un nom trouvé dans le code sans vérifier qu'il existe dans le thème chargé.

## Relier une source à un élément visible

Lorsqu'un élément doit être documenté ou personnalisé, suivez cette chaîne :

1. Décrire précisément l'élément visible et son état : par exemple, le bouton d'ouverture des réglages rapides au repos et au survol.
2. Identifier le programme responsable : GNOME Shell, une application GTK, Mutter ou un service.
3. Ouvrir le dépôt et la version de ce programme, pas un dépôt portant seulement un nom voisin.
4. Chercher le composant dans les fichiers de thème, les fichiers UI et le code qui le construit.
5. Vérifier si le style est écrit directement en CSS/SCSS, construit par une classe, ou dépend d'une préférence.
6. Tester le résultat dans la version ciblée et consigner les écarts.

Un nom de fichier SCSS ne constitue pas à lui seul une API stable. GNOME Shell peut réorganiser ses modules, renommer des classes ou modifier la structure des widgets entre deux versions.

## Distinguer les sources de référence

- Les notes de version indiquent les changements annoncés, mais ne décrivent pas chaque détail de rendu.
- Le code source de la version ciblée permet d'étudier l'implémentation réellement livrée.
- La documentation GTK décrit le moteur et ses propriétés, mais ne garantit pas qu'un composant particulier expose chaque propriété.
- La documentation Libadwaita décrit ses conventions et API publiques ; elle ne transforme pas les détails internes d'une application en API stable.
- Les spécifications freedesktop décrivent les formats et conventions partagés pour les icônes, les polices ou les chemins.
- Les captures d'écran illustrent un état visuel précis ; elles ne remplacent pas l'inspection du code et des versions.

En cas de contradiction, vérifiez d'abord la version exacte et privilégiez le code source correspondant au composant étudié. Signalez explicitement toute incertitude au lieu de présenter une supposition comme une compatibilité garantie.

## Fiche de traçabilité d'une règle

Pour chaque règle importante du thème, conservez une note de ce type dans vos commentaires ou votre documentation de projet :

```text
Élément : bouton des réglages rapides
Programme : GNOME Shell
Version testée : 51.0
Source consultée : data/theme/gnome-shell-sass/widgets/
Sélecteur observé : à relever dans la source et l'inspecteur
États vérifiés : normal, survolé, pressé, désactivé
Résultat : conforme / partiel / non pris en charge
```

Remplacez les valeurs d'exemple par les informations réellement vérifiées. Cette fiche facilite les mises à jour et évite de conserver des sélecteurs obsolètes sans savoir pourquoi ils avaient été ajoutés.

## Contrôle avant de déclarer une compatibilité GNOME 51

- La version de GNOME Shell a été relevée sur l'environnement de test.
- La version GTK de l'application ciblée a été identifiée.
- La version Libadwaita a été identifiée lorsque l'application l'utilise.
- Le sélecteur ou la propriété a été retrouvé dans une source correspondant à la version annoncée.
- Les états interactifs pertinents ont été testés.
- Le résultat a été vérifié dans le moteur concerné, pas seulement dans un aperçu statique.
- Les limites connues et les composants non testés sont indiqués.

Une compatibilité doit toujours préciser son périmètre : par exemple « testé avec GNOME Shell 51.0 et GTK 4.23 », plutôt que « compatible GNOME » sans autre précision.
