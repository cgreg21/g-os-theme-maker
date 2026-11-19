# Thèmes GNOME et applications Flatpak

Flatpak modifie la manière dont une application accède aux thèmes, aux icônes, aux polices et aux fichiers de l'hôte. Un thème installé dans le compte utilisateur peut fonctionner dans les applications natives et rester invisible dans une application Flatpak. Ce n'est pas nécessairement une erreur CSS : le bac à sable possède ses propres chemins et dépendances.

Ce chapitre explique comment diagnostiquer cette différence sans désactiver la sécurité du bac à sable. Il distingue les ressources de l'hôte, les extensions Flatpak, les préférences d'apparence et les styles privés des applications.

## 1. Comprendre les deux systèmes de fichiers

Une application native consulte généralement les répertoires XDG de l'utilisateur et les ressources installées par la distribution. Une application Flatpak s'exécute dans un environnement isolé. Elle voit une partie des fichiers de l'hôte, les runtimes et les extensions de thème explicitement accessibles.

Les chemins importants sur l'hôte sont :

- `~/.themes` : thèmes GTK historiques installés pour l'utilisateur ;
- `~/.local/share/themes` : autre emplacement utilisateur couramment utilisé pour les thèmes ;
- `~/.icons` et `~/.local/share/icons` : thèmes d'icônes utilisateur ;
- `~/.local/share/fonts` : polices installées pour l'utilisateur ;
- `/usr/share/themes`, `/usr/share/icons` et `/usr/share/fonts` : ressources système.

Le fait qu'un chemin existe sur l'hôte ne signifie pas qu'il est visible dans le bac à sable. Même lorsqu'un chemin est visible, le runtime peut ne pas disposer du moteur ou des bibliothèques nécessaires pour exploiter la ressource.

Ne confondez pas le système de fichiers de l'hôte, le runtime de l'application et les extensions Flatpak. Le runtime fournit une base logicielle partagée ; une extension peut ajouter des ressources compatibles avec cette base. Une extension de thème n'est pas un accès général à tous les fichiers de l'hôte.

## 2. Identifier l'application, le runtime et la version

Listez les applications Flatpak installées :

```sh
flatpak list --app
```

Affichez les informations d'une application :

```sh
flatpak info org.gnome.TextEditor
flatpak info --show-runtime org.gnome.TextEditor
flatpak info --show-permissions org.gnome.TextEditor
```

Remplacez l'identifiant par celui de l'application testée. Relevez le runtime, sa branche et les permissions. Les identifiants et versions présents sur une machine peuvent être différents des exemples.

Pour comparer deux installations, notez aussi la source du paquet et sa portée : installation utilisateur ou système. Les commandes suivantes permettent de consulter les installations connues :

```sh
flatpak list --app --columns=application,version,branch,installation
flatpak remotes --show-details
```

Ne concluez pas qu'une application utilise GTK 4 ou Libadwaita uniquement à partir de son apparence. Consultez les métadonnées, le runtime et les dépendances lorsque cette information est disponible.

## 3. Distinguer thème GTK, thème d'icônes et préférence sombre

Ces ressources sont indépendantes. Une application peut utiliser :

- un thème GTK fourni par son runtime ;
- un thème GTK transmis depuis l'hôte ;
- un thème d'icônes différent de celui du bureau ;
- une préférence d'apparence sombre communiquée par les portails ;
- des feuilles CSS privées embarquées dans l'application.

Changer le nom du thème GTK ne change pas automatiquement le thème d'icônes. Inversement, une icône absente ne prouve pas que le CSS est ignoré.

Pour isoler le problème, comparez une application GTK native et sa version Flatpak, si les deux existent. Utilisez la même action, la même taille de fenêtre et le même mode clair ou sombre. Vérifiez séparément les polices, les icônes, les curseurs, les couleurs et les décorations.

Une application Libadwaita peut choisir une apparence claire ou sombre sans accepter un thème GTK arbitraire. La préférence sombre et le remplacement complet des composants sont deux mécanismes distincts.

## 4. Vérifier les extensions de thèmes Flatpak

Flatpak peut fournir des extensions de thèmes correspondant aux runtimes. Recherchez les extensions disponibles :

```sh
flatpak remote-ls flathub --runtime | grep -i theme
```

La disponibilité et le nom des extensions dépendent du dépôt et de la version du runtime. N'inventez pas un identifiant d'extension : vérifiez-le dans le résultat de la commande ou dans la documentation du dépôt utilisé.

Une extension de thème doit correspondre à la famille et à la branche de runtime attendues. Une extension GTK 3 ne fournit pas nécessairement un thème GTK 4, et une extension de thème d'icônes ne fournit pas de feuille GTK. Vérifiez également si l'extension est installée dans la même portée que l'application.

Après installation ou mise à jour d'une extension, fermez complètement l'application puis relancez-la. Certaines ressources sont découvertes uniquement au démarrage du processus. Si l'application reste lancée en arrière-plan, fermez aussi son processus avant de conclure que l'extension n'a aucun effet.

Ne copiez pas manuellement les fichiers dans les répertoires internes d'un runtime. Les runtimes et extensions sont gérés par Flatpak et leurs contenus peuvent être remplacés lors d'une mise à jour.

## 5. Examiner les permissions et les surcharges

Affichez les permissions effectives :

```sh
flatpak info --show-permissions org.gnome.TextEditor
flatpak override --user --show org.gnome.TextEditor
flatpak override --system --show org.gnome.TextEditor
```

Les surcharges utilisateur et système peuvent ajouter ou retirer des permissions et des variables d'environnement. Une configuration ancienne peut expliquer une différence entre deux machines.

N'ajoutez pas de permission générale d'accès au système de fichiers uniquement pour faire fonctionner un thème. Une permission trop large affaiblit l'isolation et ne garantit pas que GTK chargera le thème.

Si un test exige exceptionnellement de rendre un dossier visible, limitez l'accès au dossier strictement nécessaire et en lecture seule lorsque c'est possible. Notez la surcharge avant de la créer, vérifiez son effet, puis retirez-la après le test. Ne partagez jamais tout le répertoire personnel ou la racine de l'hôte pour résoudre un problème de couleur.

Une surcharge temporaire ne doit pas devenir une dépendance implicite du thème. Pour distribuer un thème, privilégiez les extensions prévues pour les runtimes et les mécanismes d'apparence documentés.

## 6. Examiner les ressources depuis le bac à sable

Ouvrez un shell dans l'environnement de l'application :

```sh
flatpak run --command=sh org.gnome.TextEditor
```

À l'intérieur du shell, examinez les chemins et les outils disponibles :

```sh
printf '%s\n' "$XDG_DATA_DIRS"
command -v fc-list
command -v gtk4-demo
```

La présence d'une commande dépend du runtime. L'absence de `fc-list` ou de `gtk4-demo` ne prouve pas que le moteur correspondant est absent ; le runtime peut simplement ne pas inclure ces outils de diagnostic.

Pour examiner les polices visibles dans le bac à sable, si Fontconfig est présent :

```sh
fc-list | head
fc-match sans-serif
```

Comparez ces résultats à ceux de l'hôte. Une police présente sur l'hôte mais absente du runtime est un indice de problème de visibilité ou d'intégration des polices.

Sortez du shell avec `exit`. Ne modifiez pas les fichiers du runtime en place : utilisez les extensions et les mécanismes Flatpak documentés.

## 7. Examiner le thème réellement chargé

Pour une application GTK, GTK Inspector peut aider à identifier le widget, son arbre de nœuds CSS, ses classes et ses providers.

Si l'inspecteur est inclus dans le runtime et autorisé par l'application, essayez :

```sh
flatpak run --env=GTK_DEBUG=interactive org.gnome.TextEditor
```

Le support dépend du runtime, de la version GTK et de la façon dont l'application a été construite. Si l'inspecteur n'est pas disponible, ne concluez pas que le thème est absent : vérifiez d'abord les extensions et les ressources exposées au bac à sable.

Dans l'inspecteur, identifiez le widget, son arbre de nœuds CSS, les classes et les providers. Comparez ces informations à celles de l'application native. Les sélecteurs privés d'une application peuvent être différents même si les deux programmes utilisent GTK.

L'inspecteur montre le CSS du toolkit, pas nécessairement les règles d'une page web interne ou les styles dessinés directement par une application. Pour Electron, utilisez les outils de développement propres à Chromium si l'application les expose.

## 8. Comprendre les portails d'apparence

Les portails XDG permettent à une application sandboxée de recevoir certaines préférences de l'environnement, notamment des préférences d'apparence prises en charge par la version du portail et du runtime.

Une préférence sombre communiquée par un portail n'est pas un transfert complet du thème CSS de l'hôte. Elle indique une préférence ou un schéma d'apparence ; l'application et son toolkit décident ensuite comment l'interpréter.

Sur GNOME, la préférence de schéma de couleurs peut être consultée avec :

```sh
gsettings get org.gnome.desktop.interface color-scheme
```

Cette clé peut ne pas exister sur des environnements ou versions différents. Vérifiez le schéma installé avant de l'utiliser dans un script portable.

Si le mode sombre fonctionne mais que les couleurs personnalisées ne sont pas reprises, vérifiez les deux mécanismes séparément. Ne confondez pas le choix clair/sombre et le chargement d'un thème GTK arbitraire.

## 9. Diagnostiquer les icônes, les curseurs et les polices

Pour les icônes, vérifiez le nom d'icône demandé, la présence du thème correspondant et les solutions de repli. Les noms d'icônes Freedesktop sont des identifiants, pas des noms de fichiers garantis dans chaque thème.

Les curseurs constituent un cas distinct : le thème de curseurs doit être disponible dans l'environnement concerné et reconnu par la pile graphique. Un thème GTK visible ne garantit pas que les curseurs personnalisés le soient aussi.

Pour les polices, comparez `fc-match` sur l'hôte et dans le bac à sable. Vérifiez que la famille est présente, que la face contient les glyphes requis et que le runtime peut accéder aux fichiers correspondants. Un repli typographique peut donner l'impression que le thème n'a pas chargé la police attendue.

Consignez les résultats ressource par ressource. Ne corrigez pas une icône manquante en ajoutant une permission de fichiers globale, et ne corrigez pas un repli de police en remplaçant le CSS de toute l'application.

## 10. Procédure de diagnostic reproductible

1. Notez l'identifiant Flatpak, sa portée d'installation et son runtime.
2. Relevez les versions de GTK et Libadwaita lorsqu'elles sont identifiables.
3. Vérifiez les permissions et les surcharges existantes sans les élargir.
4. Vérifiez les extensions de thème correspondant à la branche du runtime.
5. Comparez les ressources visibles sur l'hôte et dans le bac à sable.
6. Redémarrez complètement l'application après chaque changement.
7. Inspectez les nœuds CSS si GTK Inspector est disponible.
8. Testez séparément CSS, icônes, curseurs, polices et préférence sombre.
9. Comparez avec une version native lorsque c'est possible.
10. Consignez la distribution, le runtime, les versions et les limites observées.

Cette procédure permet de distinguer une absence de ressource, un problème de visibilité dans le bac à sable, une surcharge de permissions et une feuille CSS applicative prioritaire.

## 11. Limites et bonnes pratiques

Ne désactivez pas le bac à sable et n'accordez pas un accès global au système de fichiers pour obtenir une apparence uniforme. Préférez les extensions de thème officielles compatibles avec le runtime, les portails et les mécanismes documentés par Flatpak.

Certaines applications Flatpak embarquent leurs propres styles ou utilisent des composants personnalisés. Le thème de l'hôte ne peut pas imposer une apparence identique à chaque application.

Un thème publié doit indiquer les applications Flatpak réellement testées, la branche de runtime utilisée et les ressources effectivement prises en charge. Évitez les promesses générales comme « compatible avec toutes les applications Flatpak ».

## 12. Exercice pratique

1. Choisissez une application GTK native et une application Flatpak comparable.
2. Relevez l'identifiant, le runtime et les permissions de l'application Flatpak.
3. Comparez les polices et les chemins de données visibles sur l'hôte et dans le bac à sable.
4. Vérifiez les extensions de thème disponibles pour le runtime.
5. Comparez l'apparence claire et sombre sans modifier les permissions.
6. Si l'inspecteur GTK est disponible, comparez les arbres CSS.
7. Notez les différences entre thème GTK, icônes, polices, curseurs et décorations.
8. Supprimez toute surcharge temporaire et vérifiez que l'application fonctionne toujours.

L'exercice doit produire un constat reproductible, pas simplement une capture d'écran : indiquez les versions, les ressources visibles et les limites du test.

## 13. Références

- [Documentation Flatpak](https://docs.flatpak.org/)
- [Commandes Flatpak](https://docs.flatpak.org/en/latest/flatpak-command-reference.html)
- [Portals : documentation XDG](https://flatpak.github.io/xdg-desktop-portal/)
- [Portail Settings](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Settings.html)
- [GTK 4 : CSS overview](https://docs.gtk.org/gtk4/css-overview.html)
- [GTK 3 : CSS overview](https://docs.gtk.org/gtk3/css-overview.html)
