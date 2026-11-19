# Construire un thème GNOME Shell à partir des sources SCSS

Ce chapitre s’adresse à ceux qui veulent comprendre comment le thème officiel est construit, retrouver l’origine d’un sélecteur et maintenir une personnalisation lorsque GNOME évolue. Il distingue clairement le thème utilisateur du travail sur les sources de GNOME Shell.

## 1. Source SCSS et CSS installé

Dans GNOME Shell 51, les sources du thème sont organisées sous data/theme :

- gnome-shell-light.scss : variante claire ;
- gnome-shell-dark.scss : variante sombre ;
- gnome-shell-high-contrast.scss : contraste élevé ;
- gnome-shell-sass/_colors.scss et les fichiers de couleurs : palette et valeurs sémantiques ;
- gnome-shell-sass/_common.scss et _drawing.scss : fonctions et styles partagés ;
- gnome-shell-sass/_widgets.scss : assemblage des familles de composants ;
- gnome-shell-sass/widgets/ : feuilles par composant.

Le fichier CSS utilisé à l’exécution est le résultat compilé. Modifier le SCSS d’une copie du dépôt GNOME ne modifie pas le thème installé sur une session existante.

## 2. Obtenir les sources exactes de GNOME Shell 51

Pour comprendre un sélecteur, partez de la version amont qui correspond à la session testée. Un checkout limité à la branche 51.0 permet de chercher sans mélanger les versions :

```bash
git clone --depth 1 --branch 51.0 \
  https://github.com/GNOME/gnome-shell.git gnome-shell-51
cd gnome-shell-51
```

Vérifiez le commit récupéré :

```bash
git describe --tags --always
git rev-parse HEAD
```

Conservez ce commit dans vos notes de compatibilité. Une distribution peut appliquer des correctifs en plus de la version amont ; lorsque le résultat diffère, comparez aussi les sources du paquet de la distribution.

## 3. Suivre un composant depuis son sélecteur

Prenons les réglages rapides. La recherche commence par le nom de la classe :

```bash
grep -Rni --include='*.scss' '.quick-toggle' \
  data/theme/gnome-shell-sass/widgets
```

Ouvrez ensuite le fichier trouvé et remontez les imports depuis `_widgets.scss`. Cherchez les couleurs, mixins et fonctions utilisées, puis vérifiez les variantes clair, sombre et contraste élevé.

La même méthode fonctionne pour `.popup-menu-item`, `.notification-banner`, `#panel` ou `.switcher-popup`.

Pour retrouver toutes les occurrences, y compris dans le code qui construit l'acteur :

```bash
grep -Rni --include='*.js' --include='*.ui' \
  --include='*.scss' 'quick-toggle' .
```

Le SCSS décrit l'apparence ; le code JavaScript ou les fichiers UI peuvent expliquer quand le nœud est créé, quelles classes lui sont ajoutées et dans quels états il apparaît. Vérifiez ces deux côtés avant de conclure qu'un sélecteur est utilisable.

Ne copiez pas un sélecteur d'une ancienne version sans comparaison : le nom, la structure du widget et les états peuvent avoir changé.

## 4. Comprendre le rôle des variantes

Les fichiers d’entrée définissent notamment $variant et $contrast, puis importent les couleurs, fonctions communes et widgets. Les conditions SCSS sont résolues pendant la compilation.

Conséquences :
- les variables SCSS ne sont pas des variables CSS dynamiques ;
- un changement de palette doit être vérifié dans les trois variantes ;
- une valeur codée en dur dans un widget peut contourner la palette ;
- une règle adaptée au mode sombre peut devenir illisible en mode clair.

Évitez de construire un thème qui ne fonctionne que dans une variante.

## 5. Compiler les sources officielles

La construction amont GNOME Shell 51 déclare les feuilles SCSS dans data/theme/meson.build. Le projet utilise sassc pour générer les CSS lorsque les fichiers compilés ne sont pas déjà présents.

Dans un checkout complet de GNOME Shell, après installation des dépendances de compilation indiquées par le projet :

```bash
meson setup _build
meson compile -C _build
```

Cette construction concerne le projet GNOME Shell complet et peut nécessiter de nombreuses dépendances de développement. Consultez le `meson.build` et les instructions de construction de la branche 51.0 avant de lancer la configuration. Si Meson indique une dépendance absente, installez le paquet de développement correspondant à votre distribution ; ne désactivez pas au hasard les fonctionnalités pour faire aboutir la compilation.

Pour une expérimentation isolée, utilisez le compilateur et les options réellement déclarés par le projet. Vérifiez la commande exacte dans `data/theme/meson.build` et la version de Sass attendue. Une compilation manuelle peut omettre des options ou des dépendances que Meson applique automatiquement.

La sortie compilée est un artefact de test. Elle ne doit pas être copiée dans les répertoires système ni considérée comme installée dans la session. Cette compilation ne remplace pas les tests visuels du Shell.

## 6. Créer un thème utilisateur sans modifier GNOME

Pour une personnalisation personnelle, ne modifiez pas les sources du système. Créez un thème distinct dans un emplacement utilisateur reconnu :

```text
~/.local/share/themes/MonTheme/
└── gnome-shell/
    └── gnome-shell.css
```

Le nom `MonTheme` est le nom du thème à sélectionner. Le sous-répertoire `gnome-shell` et le fichier `gnome-shell.css` doivent respecter exactement cette orthographe. Un fichier nommé `gtk.css` ou un dossier `gnome-shell-theme` ne sera pas chargé à leur place.

Exemple minimal :

    #panel {
      background-color: #20242b;
      color: #ffffff;
    }

    #panel .panel-button:hover,
    #panel .panel-button:focus {
      background-color: #3584e4;
    }

L’utilisation d’un thème Shell utilisateur nécessite l’extension User Themes et dépend des possibilités de la session/distribution. Installez et activez cette extension depuis une source de confiance, puis sélectionnez le thème avec un outil compatible. Si cette extension n’est pas disponible ou autorisée, n’essayez pas de contourner les protections du système.

## 7. Tester sans rendre la session inutilisable

- Conservez un compte ou une session de secours.
- Commencez par une seule règle.
- Testez dans une machine virtuelle GNOME ou une session imbriquée.
- Ne remplacez jamais directement les fichiers du thème système.
- Sur Wayland, ne comptez pas sur le raccourci de redémarrage Shell propre aux sessions X11.
- En cas d’écran inutilisable, désactivez le thème utilisateur depuis une session de secours ou supprimez uniquement le répertoire de test.

## 8. Mettre à jour un thème après une version GNOME

Pour chaque nouvelle version :
1. récupérez les sources exactes et notez le commit ;
2. comparez les fichiers SCSS amont ;
3. recherchez les sélecteurs utilisés par votre thème dans SCSS et dans le code des acteurs ;
4. vérifiez les classes ajoutées et retirées à l'exécution ;
5. vérifiez les propriétés St et les états interactifs ;
6. testez clair, sombre et contraste élevé ;
7. testez le verrouillage, les dialogues et les indicateurs de confidentialité ;
8. documentez les composants retirés, modifiés ou non testés.

Pour un thème qui contient peu de règles, une recherche manuelle ciblée est souvent plus fiable qu'une migration automatique. Pour un thème volumineux, établissez une liste de sélecteurs utilisés et vérifiez chacun dans les sources de la nouvelle version. Supprimez les règles qui ne correspondent plus à un acteur réel au lieu de conserver des correctifs spéculatifs.

Un thème Shell est une personnalisation d’implémentation, pas une API stable. Le fait qu’un sélecteur ait existé en GNOME 50 ne prouve pas qu’il existe encore en GNOME 51.

Sources amont vérifiées : [SCSS GNOME Shell 51](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass), [construction du thème](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/meson.build), [entrée sombre](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-dark.scss).
