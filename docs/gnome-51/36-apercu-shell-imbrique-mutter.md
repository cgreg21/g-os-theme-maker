# Aperçu GNOME Shell isolé : Mutter imbriqué et diagnostic

L'éditeur peut lancer une session GNOME Shell dans une fenêtre séparée afin de visualiser le CSS Shell généré. Cette session est distincte du bureau actif. Elle est utile pour tester les sélecteurs et les composants Shell sans remplacer le thème de la session de travail.

## 1. Aperçu local et aperçu Shell : deux environnements différents

L'aperçu GTK local est rendu par le processus de G-OS Theme Maker. Il utilise GTK 4 et montre les widgets de démonstration de l'application.

L'aperçu Shell imbriqué lance un autre processus GNOME Shell avec un serveur de session D-Bus et des répertoires XDG temporaires. Il affiche le véritable environnement Shell dans une fenêtre séparée, sous réserve que la machine et la version de Mutter autorisent ce mode.

Il faut donc utiliser les deux aperçus pour deux questions différentes :

- l'aperçu local permet-il de comprendre et régler les tokens ?
- le Shell imbriqué applique-t-il réellement les styles aux composants GNOME Shell ?

## 2. Préparer les dépendances

Le contrôleur vérifie la présence de `dbus-run-session` et de la commande `gnome-shell`.

Sur une distribution Debian ou Ubuntu, ces commandes sont généralement fournies par les paquets D-Bus et GNOME Shell. Le nom des paquets peut varier selon la distribution.

Vérifiez les exécutables :

```sh
command -v dbus-run-session
command -v gnome-shell
gnome-shell --version
```

Si l'une des commandes est absente, installez le composant correspondant depuis les dépôts de votre distribution, puis relancez l'éditeur.

L'application ne télécharge pas GNOME Shell et ne remplace pas les composants système.

## 3. Lancer et arrêter la session imbriquée

Dans la colonne Éléments, cliquez sur **Lancer Mutter imbriqué**. Si le lancement réussit, une fenêtre distincte affiche GNOME Shell. Le bouton devient une action d'arrêt.

Pour terminer proprement l'essai, cliquez sur **Arrêter Mutter imbriqué**. Le contrôleur termine le processus, attend sa fermeture, puis nettoie le répertoire temporaire.

Si le processus ne se termine pas dans le délai prévu, le contrôleur demande son arrêt forcé. Évitez de tuer manuellement des processus GNOME Shell de votre session principale : identifiez toujours le processus de la session de test avant toute action manuelle.

## 4. Pourquoi le bureau actif n'est-il pas modifié ?

Le contrôleur crée un répertoire temporaire contenant des données GNOME, une configuration et un profil dconf isolés. Il y installe une extension temporaire dont le rôle est de charger la feuille CSS générée.

Les variables d'environnement `XDG_DATA_HOME`, `XDG_CONFIG_HOME` et `DCONF_PROFILE` sont définies pour le processus lancé. L'extension d'aperçu n'est donc pas installée dans le répertoire personnel habituel de l'utilisateur.

Cette isolation réduit les risques de modifier les paramètres de la session principale. Elle ne remplace pas les précautions normales : ne modifiez pas les fichiers système et vérifiez toujours que la fenêtre observée est bien celle de la session imbriquée.

## 5. Rechargement du CSS

Lorsque l'éditeur modifie les tokens, il régénère le CSS Shell. Si la session imbriquée est active, le fichier temporaire est remplacé. L'extension surveille le répertoire et recharge la feuille lorsqu'elle détecte le changement du fichier CSS.

Le rechargement permet de comparer rapidement les valeurs sans relancer toute la session. Il ne garantit pas que chaque changement de structure ou chaque extension soit réinitialisé. Si un composant reste dans un état incohérent, fermez puis relancez la session imbriquée.

## 6. Choix du mode de lancement

Le contrôleur inspecte la version de GNOME Shell. Pour les versions récentes à partir de 49, il utilise la commande de développement imbriquée avec Wayland. Pour les versions plus anciennes, il utilise le mode imbriqué Wayland classique.

Ce choix est un mécanisme de compatibilité du lanceur, pas une promesse que tous les environnements disposent des dépendances nécessaires. Les options disponibles dépendent de la compilation GNOME Shell installée et de la session graphique.

Si votre distribution fournit une commande GNOME Shell modifiée, le lancement peut différer du comportement attendu. Conservez le message d'erreur exact et la sortie de `gnome-shell --version` pour diagnostiquer le problème.

## 7. Dépannage

### Le bouton ne lance pas la session

Vérifiez les deux exécutables :

```sh
command -v dbus-run-session
command -v gnome-shell
```

L'application affiche un message explicite lorsque les dépendances minimales manquent. Installez les paquets de la distribution, puis relancez G-OS Theme Maker.

### La fenêtre apparaît puis se ferme

Lisez les journaux de la session de test si la distribution les expose. Vérifiez la disponibilité de Wayland, les pilotes graphiques et les options imbriquées prises en charge par la version installée.

L'éditeur ne peut pas corriger un problème de pilote ou une fonctionnalité désactivée dans le paquet GNOME Shell.

### Le CSS semble ignoré

Procédez dans cet ordre :

1. vérifiez que la session imbriquée est toujours active ;
2. changez une propriété très visible, comme la couleur du fond du panneau ;
3. vérifiez que le composant existe dans cette version du Shell ;
4. vérifiez le sélecteur dans les sources GNOME correspondantes ;
5. contrôlez les journaux de la session ;
6. redémarrez la session imbriquée si le rechargement n'a pas pris effet.

Un sélecteur qui ne correspond à aucun élément ne produit pas nécessairement une erreur CSS. Il peut simplement ne rien modifier.

### La session principale semble inchangée

C'est le comportement attendu. L'aperçu utilise des données et une configuration temporaires. Pour installer un thème, utilisez l'export complet ou Shell, puis suivez les instructions d'installation et d'activation du chapitre consacré à la publication.

### Le lancement échoue dans une machine virtuelle

Certaines configurations virtuelles n'exposent pas les capacités graphiques ou Wayland requises. Vérifiez les options du pilote virtuel, l'accélération graphique et les restrictions de la session hôte. Le lancement imbriqué n'est pas un substitut à une machine de test GNOME correctement configurée.

## 8. Tester les composants pertinents

Une fois la session ouverte, ne vous contentez pas de regarder le bureau au repos. Ouvrez les éléments qui correspondent aux règles CSS générées :

- panneau supérieur et boutons du panneau ;
- menus système ;
- réglages rapides ;
- notifications ;
- dialogues ;
- vue Activités et espaces de travail.

Certains composants n'apparaissent qu'après une interaction ou une notification. Testez-les manuellement et comparez les états repos, survol, appui, sélection et focus.

## 9. Vérifier les différences entre versions

Le CSS Shell dépend des classes et de la structure interne de GNOME Shell. L'exporteur fournit une base de styles, mais un sélecteur peut changer d'une version à l'autre.

Pour une validation fiable :

1. notez la version affichée par `gnome-shell --version` ;
2. consultez les sources correspondant à cette version ;
3. vérifiez le composant dans l'aperçu imbriqué ;
4. ne généralisez pas un résultat observé sur une version unique ;
5. consignez les sélecteurs spécifiques à une version dans la documentation du thème.

## 10. Limites de sécurité et de portée

La session temporaire est conçue pour isoler le test de l'environnement utilisateur. Elle ne constitue pas un bac à sable de sécurité contre du code malveillant. Le processus GNOME Shell conserve les permissions de l'utilisateur qui lance l'application.

L'aperçu ne simule pas tous les matériels, toutes les extensions ni toutes les configurations graphiques. Il est un outil de validation rapide, à compléter par des essais sur une session de test et, si nécessaire, sur une machine distincte.
