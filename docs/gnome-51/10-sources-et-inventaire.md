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


## Figer une source pour qu'une vérification soit reproductible

Un lien vers une branche comme `main`, `master` ou `51.x` peut changer après la rédaction. Pour une affirmation technique importante, notez le tag ou le commit réellement examiné.

Dans un clone du dépôt GNOME Shell :

```sh
git fetch --tags
git checkout 51.0
git rev-parse HEAD
git status --short
```

Conservez le résultat de `git rev-parse HEAD` dans la fiche de traçabilité. Le tag identifie une version publiée ; le hash identifie précisément le contenu examiné. Si vous travaillez sur une révision corrigée par une distribution, notez également le paquet et sa révision : son contenu peut différer du tag amont.

Pour consulter l'historique d'un fichier précis :

```sh
git log --oneline --follow -- data/theme/gnome-shell-sass/widgets/_panel.scss
git blame -L 1,100 -- data/theme/gnome-shell-sass/widgets/_panel.scss
```

Adaptez le chemin au fichier réellement présent dans la révision clonée. `git blame` aide à retrouver l'origine d'une ligne, mais ne remplace pas la lecture du commit et de ses changements associés.

## Comparer deux versions de GNOME Shell

Avant de réutiliser une règle d'une ancienne version, comparez les sources des deux versions :

```sh
git diff 50.0..51.0 -- data/theme/gnome-shell-sass
git diff --stat 50.0..51.0 -- data/theme/gnome-shell-sass
```

Cette comparaison met en évidence les fichiers ajoutés, supprimés ou modifiés. Elle ne prouve pas à elle seule qu'un sélecteur est utilisé à l'exécution : remontez jusqu'au widget qui lui correspond et vérifiez le rendu dans une session de test.

Pour rechercher les changements d'un symbole :

```sh
git log --all -S'quick-settings' --oneline -- data/theme/gnome-shell-sass
git log --all -G'\.panel|\.quick-settings' --oneline -- data/theme/gnome-shell-sass
```

La recherche textuelle peut retourner des commentaires, des variables SCSS ou des sélecteurs qui ne sont plus chargés. Inspectez le diff et le contexte d'utilisation.

## Examiner les schémas GSettings sans confondre préférence et style

Les schémas GSettings décrivent des préférences configurables. Ils ne constituent pas un catalogue de propriétés CSS. Une préférence peut modifier un comportement sans exposer de mécanisme de personnalisation visuelle.

Dans le dépôt GNOME Shell :

```sh
find data -type f -name '*.gschema.xml*' -print
grep -RIn --include='*.gschema.xml*' \
  -E '<schema|<key name=|<default>' data
```

Sur le système installé, interrogez les schémas disponibles plutôt que de supposer leur présence :

```sh
gsettings list-schemas | grep -E 'org\.gnome\.shell|org\.gnome\.desktop'
gsettings list-recursively org.gnome.shell
```

Une clé ne doit être modifiée que si son schéma existe et si sa description confirme son rôle. Pour comprendre une préférence, relevez son type, sa valeur par défaut, sa description et le composant qui la lit. Ne présentez pas une clé interne ou expérimentale comme une interface stable.

## Retrouver l'origine d'une propriété GTK

La documentation des propriétés indique ce que le moteur sait interpréter, pas nécessairement ce qu'un widget utilise. Pour investiguer une propriété :

1. identifiez le moteur GTK réellement chargé par l'application ;
2. vérifiez que la propriété figure dans la documentation de cette version ;
3. identifiez le widget et son nœud CSS ;
4. observez les classes et états du widget avec l'inspecteur ;
5. appliquez une règle minimale dans un environnement de test ;
6. vérifiez le rendu et les avertissements du moteur.

Pour GTK 3 et GTK 4, gardez des références séparées. Une propriété ou un sélecteur valide dans une version ne doit pas être transposé à l'autre sans vérification.

Les pages de documentation « latest » sont utiles pour comprendre l'état actuel d'une API, mais elles peuvent décrire une version plus récente que celle installée. Pour un manuel ciblant GNOME 51, associez chaque affirmation à la version effectivement testée et, lorsque possible, à la documentation versionnée.

## Construire un dossier de preuves par composant

Pour éviter les références vagues, créez une fiche pour chaque composant important. Elle peut être conservée dans le dépôt du thème, à côté des tests, ou dans les commentaires des règles concernées.

Exemple de fiche à compléter :

```text
Composant :
Application ou service responsable :
Version du programme :
Paquet de la distribution et révision :
Dépôt amont :
Tag ou commit consulté :
Fichier source :
Widget ou classe observée :
Sélecteur CSS vérifié :
Propriétés utilisées :
États vérifiés :
Environnement de test :
Résultat :
Limites et écarts connus :
Date de vérification :
```

N'inscrivez pas « vérifié » si seule la documentation a été lue. Distinguez clairement une propriété documentée, un sélecteur retrouvé dans les sources, un nœud observé à l'exécution et un rendu réellement testé : ce sont quatre niveaux de preuve différents.

## Qualifier le niveau de confiance d'une information

Dans vos notes, utilisez des formulations précises :

- **Documenté** : l'information figure dans la documentation officielle de la version ciblée.
- **Présent dans les sources** : l'implémentation existe dans le tag ou commit examiné.
- **Observé à l'exécution** : le widget, la classe ou la préférence a été constaté dans le programme lancé.
- **Testé visuellement** : le changement a été appliqué et contrôlé dans le moteur concerné.
- **Non vérifié** : la preuve manque ou l'environnement requis n'est pas disponible.

Ces niveaux ne sont pas interchangeables. Un sélecteur présent dans les sources peut ne jamais être utilisé dans le contexte testé ; un rendu correct sur une machine ne garantit pas le même résultat avec une autre révision de bibliothèque.

## Mettre à jour l'inventaire lors d'une nouvelle version

À chaque nouvelle version majeure ou mise à jour importante :

1. récupérez les tags et commits officiels ;
2. identifiez les versions réellement livrées par la distribution cible ;
3. comparez les fichiers SCSS, UI et schémas GSettings ;
4. comparez les propriétés CSS et variables GTK/Libadwaita ;
5. recherchez les sélecteurs supprimés, renommés ou déplacés ;
6. refaites les observations à l'exécution ;
7. rejouez les tests visuels des composants concernés ;
8. actualisez les fiches de preuve et les limites de compatibilité.

Ne supprimez pas une règle uniquement parce qu'elle n'apparaît plus dans un fichier portant le même nom : le code peut avoir été déplacé. Recherchez le symbole dans l'ensemble du dépôt et suivez son usage avant de conclure.

L'inventaire de ce manuel est un point de départ pour l'investigation, pas une API contractuelle. Les sources versionnées, l'environnement observé et les essais reproductibles restent les éléments qui permettent de justifier une compatibilité.
