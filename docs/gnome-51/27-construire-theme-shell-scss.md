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

## 2. Suivre un composant depuis son sélecteur

Prenons les réglages rapides. La recherche commence par le nom de la classe :

    grep -Rni --include='*.scss' '.quick-toggle' data/theme/gnome-shell-sass/widgets

Ouvrez ensuite le fichier trouvé et remontez les imports depuis _widgets.scss. Cherchez les couleurs et fonctions utilisées, puis vérifiez les variantes clair, sombre et contraste élevé.

La même méthode fonctionne pour .popup-menu-item, .notification-banner, #panel ou .switcher-popup.

Ne copiez pas un sélecteur d’une ancienne version sans comparaison : le nom, la structure du widget et les états peuvent avoir changé.

## 3. Comprendre le rôle des variantes

Les fichiers d’entrée définissent notamment $variant et $contrast, puis importent les couleurs, fonctions communes et widgets. Les conditions SCSS sont résolues pendant la compilation.

Conséquences :
- les variables SCSS ne sont pas des variables CSS dynamiques ;
- un changement de palette doit être vérifié dans les trois variantes ;
- une valeur codée en dur dans un widget peut contourner la palette ;
- une règle adaptée au mode sombre peut devenir illisible en mode clair.

Évitez de construire un thème qui ne fonctionne que dans une variante.

## 4. Compiler les sources officielles

La construction amont GNOME Shell 51 déclare les feuilles SCSS dans data/theme/meson.build. Le projet utilise sassc pour générer les CSS lorsque les fichiers compilés ne sont pas déjà présents.

Dans un checkout complet de GNOME Shell, après installation des dépendances de compilation :

    meson setup _build
    meson compile -C _build

Pour une expérimentation isolée sur une feuille, depuis le dossier data/theme du checkout :

    sassc -a gnome-shell-dark.scss /tmp/gnome-shell-dark.css

Cette commande compile une feuille source ; elle ne l’installe pas et ne remplace pas le thème de la session. Les options et dépendances exactes doivent être vérifiées dans le meson.build de la branche utilisée.

## 5. Créer un thème utilisateur sans modifier GNOME

Pour une personnalisation personnelle, ne modifiez pas les sources du système. Créez un thème distinct :

    ~/.local/share/themes/MonTheme/
    └── gnome-shell/
        └── gnome-shell.css

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

## 6. Tester sans rendre la session inutilisable

- Conservez un compte ou une session de secours.
- Commencez par une seule règle.
- Testez dans une machine virtuelle GNOME ou une session imbriquée.
- Ne remplacez jamais directement les fichiers du thème système.
- Sur Wayland, ne comptez pas sur le raccourci de redémarrage Shell propre aux sessions X11.
- En cas d’écran inutilisable, désactivez le thème utilisateur depuis une session de secours ou supprimez uniquement le répertoire de test.

## 7. Mettre à jour un thème après une version GNOME

Pour chaque nouvelle version :
1. comparez les fichiers SCSS amont ;
2. recherchez les sélecteurs utilisés par votre thème ;
3. vérifiez les états et les composants déplacés ;
4. testez clair, sombre et contraste élevé ;
5. testez le verrouillage, les dialogues et les indicateurs de confidentialité ;
6. documentez les composants retirés ou non testés.

Un thème Shell est une personnalisation d’implémentation, pas une API stable. Le fait qu’un sélecteur ait existé en GNOME 50 ne prouve pas qu’il existe encore en GNOME 51.

Sources amont vérifiées : [SCSS GNOME Shell 51](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass), [construction du thème](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/meson.build), [entrée sombre](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-dark.scss).
