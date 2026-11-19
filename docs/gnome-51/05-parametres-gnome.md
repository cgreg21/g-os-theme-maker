# 5. Paramètres GNOME, GSettings et dconf

Les paramètres GNOME ne sont pas du CSS. Ils déterminent des préférences, des comportements, des périphériques et une partie de la configuration de session. Un thème peut proposer une apparence claire ou sombre, mais il ne doit pas modifier silencieusement les préférences personnelles de l'utilisateur.

Ce chapitre apprend à découvrir les réglages réellement disponibles sur une machine, à comprendre leur origine, à les modifier proprement et à restaurer l'état initial. Les schémas installés localement font autorité : les clés et leurs valeurs peuvent varier selon la distribution, les paquets et leur version.

## 1. Comprendre les différentes couches

**GSettings** est l'API de préférences utilisée par les applications et composants GNOME. Un schéma déclare des clés, leur type, leur valeur par défaut et parfois des contraintes.

**dconf** est le système de stockage fréquemment utilisé par le backend GSettings sur les postes GNOME. Il stocke les valeurs utilisateur dans une base de données. gsettings est l'outil de consultation et de modification d'une clé ; dconf permet notamment d'inspecter des chemins et d'importer ou exporter des sous-arbres.

**Les profils dconf** et les bases système permettent aux administrateurs de définir des valeurs par défaut ou de verrouiller des réglages. Une valeur verrouillée ne peut pas être remplacée par une modification utilisateur ordinaire.

**Les fichiers de schémas** sont généralement installés sous /usr/share/glib-2.0/schemas/. Les schémas compilés sont regroupés dans gschemas.compiled. Ne modifiez pas directement les fichiers système pour personnaliser un poste.

Il faut distinguer trois opérations :
- changer une préférence utilisateur ;
- définir une valeur par défaut pour une machine administrée ;
- verrouiller une préférence afin que l'utilisateur ne puisse pas la modifier.

Un thème partageable devrait normalement se limiter aux ressources visuelles. Les préférences GSettings doivent rester facultatives et clairement présentées.

## 2. Découvrir les schémas disponibles

Commencez par demander au système ce qu'il connaît :

~~~sh
# Lister les schémas installés
gsettings list-schemas

# Rechercher les schémas liés à GNOME
gsettings list-schemas | grep -E '^(org\.gnome|org\.gtk)'

# Afficher les clés d'un schéma précis
gsettings list-keys org.gnome.desktop.interface
~~~

Une clé présente dans une documentation trouvée en ligne peut être absente de votre poste. Le paquet qui fournit le schéma peut ne pas être installé, ou sa version peut différer.

Pour retrouver le fichier source d'un schéma installé :

~~~sh
grep -R -n 'schema id="org.gnome.desktop.interface"' \
  /usr/share/glib-2.0/schemas
~~~

La recherche peut aussi se faire dans les fichiers XML des paquets de développement ou dans les sources correspondant exactement à la version installée. Ne modifiez pas le XML système pour changer une préférence.

## 3. Examiner une clé avant de la modifier

Pour une clé, suivez toujours la même séquence :

~~~sh
SCHEMA=org.gnome.desktop.interface
KEY=color-scheme

# Description lisible
gsettings describe "$SCHEMA" "$KEY"

# Type et plage de valeurs
gsettings range "$SCHEMA" "$KEY"

# Valeur actuellement enregistrée
gsettings get "$SCHEMA" "$KEY"

# Valeur par défaut déclarée dans le schéma
gsettings get-default "$SCHEMA" "$KEY"

# La clé est-elle modifiable par l'utilisateur ?
gsettings writable "$SCHEMA" "$KEY"
~~~

La sortie de range indique la forme attendue : booléen, entier, chaîne, énumération, tableau ou autre type GVariant. Respectez exactement cette forme.

Pour une énumération, la plage peut afficher les chaînes admises. N'inventez pas une valeur parce qu'elle semble logique. Pour un tableau, la syntaxe GVariant doit être respectée ; une chaîne de raccourcis n'est pas un texte libre.

Si writable renvoie false, recherchez une stratégie système ou un verrou dconf. Ne tentez pas de contourner ce verrou dans un thème.

## 4. Modifier une préférence sans risque

Exemple de modification du mode de couleurs, uniquement si la clé existe et si sa plage confirme les valeurs utilisées :

~~~sh
gsettings get org.gnome.desktop.interface color-scheme
gsettings range org.gnome.desktop.interface color-scheme
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
~~~

Pour revenir à la valeur par défaut du schéma :

~~~sh
gsettings reset org.gnome.desktop.interface color-scheme
~~~

Pour restaurer une clé, préférez gsettings reset SCHEMA KEY à une valeur devinée. Cette commande supprime la surcharge utilisateur et laisse le système appliquer la valeur par défaut ou la politique administrateur.

Ne lancez jamais une commande de réinitialisation globale pour résoudre un problème de thème. Elle peut supprimer des préférences sans rapport avec l'apparence.

## 5. Familles de réglages utiles à la personnalisation

Les schémas ci-dessous sont des points de départ pour l'exploration, pas une promesse que chaque clé citée existe sur toutes les distributions.

### Apparence générale

org.gnome.desktop.interface contient couramment les préférences de thème GTK, icônes, curseur, police, facteur d'échelle du texte, animations et présentation de l'horloge. Pour chaque clé, vérifiez son existence, son type, sa plage et son caractère modifiable.

### Fonds d'écran et verrouillage

Explorez org.gnome.desktop.background pour les préférences du fond d'écran. Selon la version, les clés peuvent distinguer les images du mode clair et du mode sombre, le cadrage et les couleurs de fond.

Les préférences de verrouillage sont généralement associées à org.gnome.desktop.screensaver. Elles ne garantissent pas que l'écran GDM utilisera le même fond : GDM fonctionne dans un contexte système séparé.

### Fenêtres, raccourcis et espaces de travail

Explorez notamment :
- org.gnome.desktop.wm.preferences pour certaines préférences du gestionnaire de fenêtres ;
- org.gnome.desktop.wm.keybindings pour les raccourcis du gestionnaire de fenêtres ;
- org.gnome.mutter pour des préférences du compositeur ;
- org.gnome.shell et ses sous-schémas pour les préférences du Shell ;
- org.gnome.settings-daemon.plugins.media-keys pour des raccourcis gérés par le démon de paramètres.

Les raccourcis sont fréquemment des tableaux de chaînes. Avant de les modifier, recherchez les conflits avec GNOME Shell, Mutter, les applications et les extensions. N'écrasez pas une combinaison existante sans avoir enregistré sa valeur initiale.

### Souris, pavé tactile, clavier et son

Les schémas des périphériques et du son peuvent contrôler la vitesse, l'accélération, le clic, le défilement, la répétition des touches et les sons d'interface. Ces paramètres dépendent parfois du matériel et des services actifs.

Ils ne doivent pas être imposés par un thème graphique. Une application de création de thèmes peut les afficher à titre informatif, mais ne devrait jamais les modifier sans action explicite.

## 6. Comprendre dconf et ses chemins

Les commandes suivantes permettent d'explorer les valeurs stockées :

~~~sh
# Lister les valeurs sous un chemin
dconf list /org/gnome/desktop/interface/

# Lire une valeur précise
dconf read /org/gnome/desktop/interface/color-scheme

# Écrire une valeur (syntaxe GVariant)
dconf write /org/gnome/desktop/interface/color-scheme "'prefer-dark'"

# Supprimer une surcharge utilisateur
dconf reset /org/gnome/desktop/interface/color-scheme
~~~

Les chemins dconf se terminent généralement par une barre oblique lorsqu'ils désignent un répertoire. Les valeurs sont écrites en syntaxe GVariant. Pour une utilisation quotidienne, gsettings est souvent plus simple, car il vérifie le schéma et la clé.

Ne modifiez pas directement le fichier binaire de la base dconf. Utilisez les commandes prévues pour lire et écrire les valeurs.

## 7. Sauvegarder avant une expérimentation

Pour sauvegarder une partie des préférences GNOME de l'utilisateur :

~~~sh
dconf dump /org/gnome/ > gnome-backup.ini
~~~

Pour restaurer cette sauvegarde :

~~~sh
dconf load /org/gnome/ < gnome-backup.ini
~~~

Cette sauvegarde peut contenir des informations personnelles : raccourcis, périphériques, préférences et noms d'applications. Ne l'intégrez jamais à un thème publié et ne la partagez pas sans l'avoir inspectée.

Pour une modification isolée, notez plutôt la valeur initiale :

~~~sh
gsettings get org.gnome.desktop.interface color-scheme \
  > color-scheme.before.txt
~~~

Puis restaurez-la explicitement ou utilisez gsettings reset si l'objectif est de revenir à la valeur par défaut.

## 8. Comprendre les valeurs par défaut et les verrous administrateur

Les administrateurs peuvent déployer des profils dconf et des fichiers de verrouillage sous /etc/dconf/. Les valeurs système ne sont pas nécessairement des préférences utilisateur modifiables.

Sur une machine administrée, une clé peut :
- avoir une valeur système par défaut ;
- être remplacée par l'utilisateur si elle n'est pas verrouillée ;
- être verrouillée pour empêcher les modifications utilisateur.

Une clé non modifiable ne signifie pas que GSettings est cassé. Il peut s'agir d'une politique volontaire. La bonne démarche consiste à identifier le schéma, le profil actif et le verrou, puis à demander à l'administrateur si une modification est nécessaire.

La création de profils et de verrous est une tâche d'administration système. Elle doit être documentée séparément de l'installation d'un thème utilisateur.

## 9. Relier les réglages au thème sans confondre les responsabilités

Un thème peut fournir :
- des feuilles CSS pour Shell, GTK 3 et GTK 4 ;
- des icônes, curseurs, polices et fonds ;
- des métadonnées et des instructions d'installation.

Il peut proposer des valeurs conseillées, mais ne doit pas supposer que l'utilisateur souhaite changer :
- son mode clair ou sombre ;
- ses polices et leur taille ;
- ses raccourcis ;
- ses périphériques ;
- ses paramètres d'accessibilité ;
- ses extensions activées ;
- ses préférences de confidentialité.

Si un outil propose de modifier ces réglages, il doit afficher la clé exacte, la valeur actuelle, la valeur proposée, la portée et une possibilité de retour arrière. Il doit également vérifier que la clé est disponible et modifiable.

## 10. Atelier : découvrir, modifier et restaurer une préférence

Effectuez cet exercice sur une session de test.

1. Vérifiez que org.gnome.desktop.interface est installé.
2. Listez ses clés.
3. Choisissez une clé liée à l'apparence dont la plage est comprise.
4. Notez sa valeur actuelle.
5. Vérifiez sa valeur par défaut et son caractère modifiable.
6. Changez une seule valeur avec gsettings set.
7. Observez les composants affectés.
8. Restaurez la valeur initiale.
9. Vérifiez que le comportement initial est revenu.

Ne choisissez pas une clé dont la portée ou les conséquences ne sont pas comprises.

## 11. Diagnostic

**La clé n'existe pas.** Vérifiez le nom du schéma, le paquet installé et la version. Ne remplacez pas une clé absente par une clé supposée.

**La valeur est refusée.** Consultez gsettings range et respectez le type GVariant exact.

**La clé n'est pas modifiable.** Vérifiez les politiques dconf et les droits administrateur. Ne contournez pas le verrou.

**Le changement n'est pas visible.** Vérifiez que le composant lit cette préférence, que l'application a rechargé son état et que le paramètre n'est pas contrôlé par une autre couche.

**Le réglage change après reconnexion.** Une session, un service, une stratégie système ou un outil de synchronisation peut réappliquer une valeur.

## 12. Références

- [GSettings — documentation GLib](https://docs.gtk.org/gio/class.Settings.html)
- [GVariant — types et syntaxe](https://docs.gtk.org/glib/struct.Variant.html)
- [dconf — projet et documentation](https://github.com/dconf/dconf)
- [Schéma GNOME Shell 51.0](https://github.com/GNOME/gnome-shell/blob/51.0/data/org.gnome.shell.gschema.xml.in)
- [GNOME Shell 51.0 — sources](https://github.com/GNOME/gnome-shell/tree/51.0)
