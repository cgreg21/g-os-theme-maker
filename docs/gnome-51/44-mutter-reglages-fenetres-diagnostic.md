# Mutter 51 : réglages, fenêtres et diagnostic avancé

Ce chapitre complète [Mutter, fenêtres, décorations et écrans](24-mutter-fenetres-decorations-ecrans.md). Il s'adresse à la personne qui sait déjà distinguer GNOME Shell, GTK et Mutter et veut comprendre précisément quels comportements de la session peuvent être configurés.

La référence utilisée est le code source **Mutter 51.0**. Les noms de clés et les valeurs par défaut cités ci-dessous proviennent des schémas GSettings de cette version. Une distribution peut appliquer des valeurs différentes, omettre une fonctionnalité ou livrer un correctif propre.

## 1. Le rôle exact de Mutter

Mutter est à la fois le gestionnaire de fenêtres et le compositeur de GNOME. Dans une session Wayland, il assure également le rôle de compositeur Wayland et coordonne les surfaces des applications. Dans une session X11, il gère les fenêtres X11 et leur composition.

Le code source sépare plusieurs responsabilités :

- **MetaWindow** représente une fenêtre et expose son état logique : titre, type, maximisation, plein écran, espace de travail, état de décoration et contraintes.
- **MetaWindowX11** et **MetaWindowWayland** adaptent cette représentation aux protocoles clients.
- **MetaWindowActor** relie la fenêtre à la scène graphique.
- **Clutter** fournit le graphe de scène, les acteurs, les événements et les mécanismes d'animation.
- **Cogl** et les couches de rendu associées participent à la composition graphique.
- **GNOME Shell** construit l'interface utilisateur du bureau et ses composants visuels au-dessus de ces mécanismes.

Cette architecture explique pourquoi une propriété de fenêtre, une animation du Shell et une règle CSS GTK sont trois choses différentes. Une fenêtre peut être déplacée par Mutter, représentée par un acteur dans la scène et entourée d'une interface dessinée par l'application. Une seule règle CSS ne contrôle pas ces trois couches.

Pour explorer le code de la version ciblée, partez de :

- [Vue d'ensemble de l'architecture Mutter 51.0](https://github.com/GNOME/mutter/blob/51.0/doc/code-overview.md)
- [Implémentation des fenêtres](https://github.com/GNOME/mutter/blob/51.0/src/core/window.c)
- [Composant compositeur](https://github.com/GNOME/mutter/tree/51.0/src/compositor)
- [Schéma GSettings Mutter](https://github.com/GNOME/mutter/blob/51.0/data/org.gnome.mutter.gschema.xml.in)

## 2. Inspecter les réglages réellement disponibles

Ne partez pas d'une liste trouvée pour une autre version de GNOME. Interrogez la session qui exécute réellement le bureau :

```bash
gsettings list-schemas | grep -E 'mutter|wm.preferences'
gsettings list-recursively org.gnome.mutter
gsettings list-recursively org.gnome.mutter.keybindings
```

Pour connaître le type, la valeur par défaut et la description d'une clé, utilisez :

```bash
gsettings describe org.gnome.mutter edge-tiling
gsettings range org.gnome.mutter edge-tiling
gsettings get org.gnome.mutter edge-tiling
```

Ces commandes sont plus fiables qu'une commande de modification copiée depuis un tutoriel. Si le schéma ou la clé n'existe pas, n'essayez pas de la créer : vérifiez la version de Mutter, les schémas installés et les éventuelles différences de distribution.

Pour retrouver la version des composants :

```bash
gnome-shell --version
mutter --version
```

Selon la distribution, la commande du binaire Mutter peut ne pas être installée dans le PATH. Les informations de paquet du gestionnaire de paquets sont alors une autre source de vérification.

## 3. Réglages de placement et de comportement des fenêtres

Les clés suivantes sont déclarées dans le schéma `org.gnome.mutter` de Mutter 51.0. Leur présence sur le système doit toujours être confirmée avant usage.

### Centrer les nouvelles fenêtres

La clé `center-new-windows` contrôle le placement initial des nouvelles fenêtres au centre de l'écran actif du moniteur.

Inspecter :

```bash
gsettings get org.gnome.mutter center-new-windows
gsettings describe org.gnome.mutter center-new-windows
```

Activer le centrage :

```bash
gsettings set org.gnome.mutter center-new-windows true
```

Revenir à la valeur par défaut du schéma :

```bash
gsettings reset org.gnome.mutter center-new-windows
```

Le centrage initial ne signifie pas que toutes les fenêtres resteront centrées. Le déplacement manuel, les contraintes de taille, les règles propres à l'application et la configuration multi-écrans continuent d'intervenir.

### Maximisation automatique

La clé `auto-maximize` concerne les nouvelles fenêtres dont la taille initiale est proche de celle du moniteur. Elle ne remplace pas la commande de maximisation et ne transforme pas une règle CSS de taille en règle de gestion de fenêtres.

```bash
gsettings get org.gnome.mutter auto-maximize
gsettings describe org.gnome.mutter auto-maximize
```

Avant de modifier cette option, testez plusieurs applications : certaines fenêtres de dialogue ou certains outils ont des dimensions initiales particulières.

### Tuilage sur les bords

La clé `edge-tiling` active le comportement de tuilage lorsque l'utilisateur dépose une fenêtre sur un bord de l'écran. Dans le schéma 51.0, sa valeur par défaut est `false`.

```bash
gsettings get org.gnome.mutter edge-tiling
gsettings set org.gnome.mutter edge-tiling true
```

Lorsque cette fonction est active, les bords verticaux permettent de placer la fenêtre sur une moitié de l'espace disponible et le bord supérieur permet la maximisation. Ce comportement est une fonction de gestion des fenêtres. Il ne peut pas être obtenu en donnant une largeur de 50 % à un sélecteur CSS.

### Dialogues modaux attachés

La clé `attach-modal-dialogs` détermine si les dialogues modaux sont attachés à la barre de titre de leur fenêtre parente et déplacés avec elle.

```bash
gsettings get org.gnome.mutter attach-modal-dialogs
gsettings describe org.gnome.mutter attach-modal-dialogs
```

Cette option modifie la relation de placement entre les fenêtres. Elle ne redessine pas le contenu du dialogue et ne remplace pas le CSS de l'application.

### Largeur de la bordure interactive

La clé entière `draggable-border-width` définit la largeur totale de la zone de bordure utilisable pour déplacer ou redimensionner une fenêtre. Le schéma 51.0 déclare une plage de 0 à 64 et une valeur par défaut de 10.

```bash
gsettings range org.gnome.mutter draggable-border-width
gsettings get org.gnome.mutter draggable-border-width
gsettings describe org.gnome.mutter draggable-border-width
```

La zone interactive peut être plus large que la bordure visible. Cela permet de conserver une cible de redimensionnement accessible sans dessiner une bordure épaisse. Modifier la valeur ne change donc pas nécessairement l'épaisseur visuelle du cadre.

### Espaces de travail dynamiques

La clé `dynamic-workspaces` détermine si Mutter gère dynamiquement les espaces de travail. Lorsqu'elle est désactivée, le nombre d'espaces de travail est déterminé par la préférence `num-workspaces` du schéma `org.gnome.desktop.wm.preferences`.

Inspecter les deux côtés :

```bash
gsettings get org.gnome.mutter dynamic-workspaces
gsettings describe org.gnome.mutter dynamic-workspaces
gsettings get org.gnome.desktop.wm.preferences num-workspaces
```

Ne modifiez pas simultanément plusieurs préférences d'espaces de travail sans noter les valeurs d'origine. Le comportement attendu dépend de la combinaison des réglages et de la version de GNOME Shell.

### Espaces de travail sur l'écran principal

La clé `workspaces-only-on-primary` détermine si le changement d'espace de travail concerne les fenêtres de tous les moniteurs ou seulement celles du moniteur principal.

```bash
gsettings get org.gnome.mutter workspaces-only-on-primary
gsettings describe org.gnome.mutter workspaces-only-on-primary
```

Testez ce réglage avec au moins deux écrans connectés. Sur un ordinateur à un seul écran, le changement peut sembler sans effet.

## 4. Focus clavier et pointeur

Le focus est l'état qui détermine quelle fenêtre reçoit les événements clavier. Il ne faut pas le confondre avec la décoration visuelle d'une fenêtre active.

Mutter expose notamment la clé `focus-change-on-pointer-rest`. Elle retarde le changement de focus jusqu'à l'arrêt du pointeur lorsque le mode de focus est `sloppy` ou `mouse`.

```bash
gsettings get org.gnome.mutter focus-change-on-pointer-rest
gsettings describe org.gnome.mutter focus-change-on-pointer-rest
```

Le mode de focus général est une préférence de gestionnaire de fenêtres distincte. Inspectez le schéma avant de l'utiliser :

```bash
gsettings list-recursively org.gnome.desktop.wm.preferences
gsettings describe org.gnome.desktop.wm.preferences focus-mode
```

Le document de conception de Mutter explique les compromis entre focus au clic, focus au survol et navigation clavier : [How to get focus right](https://github.com/GNOME/mutter/blob/51.0/doc/mutter-focus.txt).

Pour un thème, la conséquence est importante : une fenêtre peut recevoir le focus sans que son apparence soit contrôlée par le Shell. L'application, son toolkit ou son décorateur peut dessiner l'indication de focus.

## 5. Raccourcis gérés par Mutter

Les raccourcis de Mutter se trouvent dans le schéma enfant `org.gnome.mutter.keybindings`. Pour les inspecter :

```bash
gsettings list-recursively org.gnome.mutter.keybindings
```

Mutter 51.0 déclare notamment les clés suivantes :

- `toggle-tiled-left` : raccourci de placement en mosaïque à gauche.
- `toggle-tiled-right` : raccourci de placement en mosaïque à droite.
- `switch-monitor` : raccourci de changement de configuration des moniteurs.
- `rotate-monitor` : raccourci de rotation de la configuration du moniteur intégré.
- `cancel-input-capture` : raccourci d'annulation d'une session de capture d'entrée.

Pour examiner une clé précise :

```bash
gsettings get org.gnome.mutter.keybindings toggle-tiled-left
gsettings describe org.gnome.mutter.keybindings toggle-tiled-left
```

Une liste de raccourcis peut contenir plusieurs combinaisons. Ne remplacez pas toute la liste si votre objectif est seulement d'ajouter une combinaison. Conservez la valeur d'origine et vérifiez les conflits avec les raccourcis de GNOME Shell et des applications.

## 6. Configuration des moniteurs

Mutter conserve les configurations d'écrans dans un fichier XML appelé `monitors.xml`. Pour la configuration utilisateur, l'emplacement usuel est :

```text
~/.config/monitors.xml
```

La configuration système peut se trouver dans un emplacement défini par les répertoires XDG, par défaut sous `/etc/xdg/monitors.xml`.

Le fichier contient des configurations correspondant à des ensembles de moniteurs et à leur état matériel. Mutter gère normalement ce fichier à travers le panneau **Affichage** des Paramètres GNOME. Lorsqu'une configuration est acceptée, le contenu utilisateur est mis à jour.

La méthode recommandée est donc :

1. Ouvrir Paramètres GNOME puis Affichage.
2. Modifier la résolution, l'orientation, la disposition et l'échelle proposées.
3. Appliquer la configuration et vérifier l'affichage.
4. Confirmer la configuration avant la fin du délai de retour arrière.
5. Revenir dans le panneau Affichage pour vérifier le résultat après reconnexion.

Ne fabriquez pas un fichier `monitors.xml` à partir d'un exemple générique. Les connecteurs, identifiants d'écran, modes supportés et capacités varient selon le matériel. Une configuration incorrecte peut rendre l'affichage inutilisable jusqu'à sa restauration.

Pour comprendre le format, la politique de priorité et le rôle de D-Bus, consultez [la documentation de configuration des moniteurs de Mutter 51.0](https://github.com/GNOME/mutter/blob/51.0/doc/monitor-configuration.md).

## 7. Distinguer les décorations, les bordures et les ombres

Le mot « bordure » désigne plusieurs éléments différents :

- La bordure dessinée dans une barre d'en-tête GTK appartient à l'interface de l'application.
- Les contrôles de titre d'une décoration côté client appartiennent généralement à l'application et à son toolkit.
- Une décoration côté serveur dépend du gestionnaire de fenêtres et du protocole utilisé.
- La zone de redimensionnement interactive dépend du gestionnaire de fenêtres et peut dépasser la bordure visible.
- Une ombre peut être dessinée par l'application, par une décoration ou par le compositeur.

Il faut donc identifier le propriétaire avant de modifier quoi que ce soit. Le CSS GTK ne règle pas la zone de redimensionnement Mutter. Le réglage `draggable-border-width` ne redessine pas la barre d'en-tête GTK. Une règle CSS du Shell ne remplace pas le rendu d'une application.

Sous Wayland, le compositeur est l'autorité qui organise les surfaces de la session. Une application peut dessiner sa propre décoration, mais elle ne peut pas imposer au compositeur une décoration globale au moyen d'une feuille CSS utilisateur.

## 8. Paramètres expérimentaux : prudence

Mutter possède un schéma distinct `org.gnome.mutter.experimental`. Dans le code source 51.0, certaines options expérimentales touchent par exemple à l'allocation des buffers KMS ou à la durée de vie de Xwayland.

Ces paramètres ne sont pas des options de personnalisation visuelle. Ils peuvent dépendre du pilote graphique, du matériel et du protocole. Certains exigent un redémarrage de Mutter ou de la session.

Pour les examiner sans les modifier :

```bash
gsettings list-recursively org.gnome.mutter.experimental
```

N'activez pas une option expérimentale dans un thème destiné à être distribué. Elle ne garantit ni une apparence identique ni un comportement stable sur les autres machines.

## 9. Procédure de diagnostic

Lorsqu'un comportement de fenêtre ne correspond pas au résultat attendu, procédez dans cet ordre :

1. Déterminer si le problème concerne une seule application ou toutes les fenêtres.
2. Identifier la session active : Wayland ou X11.
3. Vérifier le propriétaire du rendu : application, GTK, Shell ou Mutter.
4. Lire les valeurs GSettings réellement installées.
5. Modifier une seule préférence à la fois.
6. Tester avec une fenêtre simple et une application GTK.
7. Revenir à la valeur précédente si le résultat est mauvais.
8. Refaire le test après reconnexion si le paramètre concerne la session ou le backend graphique.

Pour mémoriser une valeur avant modification :

```bash
gsettings get org.gnome.mutter edge-tiling
```

Pour restaurer la valeur par défaut du schéma :

```bash
gsettings reset org.gnome.mutter edge-tiling
```

La réinitialisation restaure la valeur par défaut du schéma installé ; elle ne restaure pas forcément une valeur personnalisée que vous aviez définie auparavant. Notez donc toujours la valeur initiale.

## 10. Ce qu'un thème ne doit pas prétendre contrôler

Un thème GNOME ne peut pas, par du CSS seul :

- changer l'algorithme de placement des fenêtres ;
- définir les contraintes de taille d'une application ;
- changer le protocole Wayland ou X11 ;
- imposer la configuration physique des moniteurs ;
- modifier le focus clavier ou le comportement de tuilage ;
- remplacer les raccourcis internes de Mutter ;
- garantir que toutes les applications utilisent les mêmes décorations ;
- changer le rendu des surfaces d'une application qui dessine elle-même son interface.

Ces comportements doivent être configurés par les interfaces prévues, les clés GSettings documentées, les API d'extension prises en charge ou le code de l'application concernée.

## 11. Exercices

### Exercice A — comprendre le tuilage

1. Lire la valeur de `edge-tiling`.
2. Activer le réglage si la session le propose.
3. Déposer une fenêtre sur le bord gauche puis sur le bord supérieur.
4. Observer la géométrie obtenue.
5. Restaurer la valeur d'origine.

### Exercice B — comprendre le placement initial

1. Lire `center-new-windows` et `auto-maximize`.
2. Lancer plusieurs applications de types différents.
3. Modifier une seule clé.
4. Comparer les nouvelles fenêtres avec celles déjà ouvertes.
5. Restaurer la valeur précédente.

### Exercice C — comprendre le multi-écran

1. Connecter un second moniteur.
2. Ouvrir le panneau Affichage.
3. Configurer la disposition et l'échelle.
4. Déplacer une fenêtre entre les écrans.
5. Vérifier le comportement des espaces de travail.
6. Déconnecter puis reconnecter le moniteur et contrôler la configuration restaurée.

### Exercice D — identifier le propriétaire d'une décoration

1. Comparer une application GTK avec une application utilisant un autre toolkit.
2. Inspecter la barre d'en-tête de l'application GTK.
3. Comparer la bordure visible et la zone interactive de redimensionnement.
4. Déterminer quelles parties relèvent de l'application et lesquelles relèvent du gestionnaire de fenêtres.
5. Ne modifier le CSS qu'après avoir identifié la couche concernée.

## 12. Sources de référence GNOME 51.0

- [Mutter — schéma principal GSettings](https://github.com/GNOME/mutter/blob/51.0/data/org.gnome.mutter.gschema.xml.in)
- [Mutter — schéma des options expérimentales](https://github.com/GNOME/mutter/blob/51.0/data/org.gnome.mutter.experimental.gschema.xml.in)
- [Mutter — configuration des moniteurs](https://github.com/GNOME/mutter/blob/51.0/doc/monitor-configuration.md)
- [Mutter — architecture du code](https://github.com/GNOME/mutter/blob/51.0/doc/code-overview.md)
- [Mutter — règles de focus](https://github.com/GNOME/mutter/blob/51.0/doc/mutter-focus.txt)
- [Mutter — abstraction des fenêtres](https://github.com/GNOME/mutter/blob/51.0/src/core/window.c)
- [Mutter — compositeur](https://github.com/GNOME/mutter/tree/51.0/src/compositor)
- [GNOME Shell 51.0 — sources du thème](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass)

Les liens pointent vers la version 51.0 afin de limiter les confusions avec les changements ultérieurs. Pour une distribution réelle, confrontez toujours ces sources aux schémas installés localement.
