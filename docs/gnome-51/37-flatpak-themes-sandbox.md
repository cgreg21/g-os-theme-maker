# Thèmes GNOME et applications Flatpak

Flatpak modifie la manière dont une application accède aux thèmes, aux icônes, aux polices et aux fichiers de l'hôte. Un thème installé dans le compte utilisateur peut fonctionner dans les applications natives et rester invisible dans une application Flatpak. Ce n'est pas nécessairement une erreur CSS : le bac à sable possède ses propres chemins et dépendances.

Ce chapitre explique comment diagnostiquer cette différence sans désactiver la sécurité du bac à sable.

## 1. Comprendre les deux systèmes de fichiers

Une application native consulte généralement les répertoires XDG de l'utilisateur et les ressources installées par la distribution. Une application Flatpak s'exécute dans un environnement isolé. Elle voit une partie des fichiers de l'hôte, les runtimes et les extensions de thème explicitement accessibles.

Les chemins importants sont :

- `~/.themes` : thèmes GTK historiques installés pour l'utilisateur ;
- `~/.local/share/themes` : autre emplacement utilisateur couramment utilisé pour les thèmes ;
- `~/.icons` et `~/.local/share/icons` : thèmes d'icônes utilisateur ;
- `~/.local/share/fonts` : polices installées pour l'utilisateur ;
- `/usr/share/themes`, `/usr/share/icons` et `/usr/share/fonts` : ressources système.

Le fait qu'un chemin existe sur l'hôte ne signifie pas qu'il est visible dans le bac à sable.

## 2. Identifier l'application et son environnement

Listez les applications Flatpak installées :

```sh
flatpak list --app
```

Affichez les informations d'une application :

```sh
flatpak info org.gnome.TextEditor
```

Remplacez l'identifiant par celui de l'application testée. Pour examiner les permissions :

```sh
flatpak info --show-permissions org.gnome.TextEditor
```

N'ajoutez pas de permission générale d'accès au système de fichiers uniquement pour faire fonctionner un thème. Une permission trop large affaiblit l'isolation et ne garantit pas que GTK chargera le thème.

## 3. Distinguer thème GTK, thème d'icônes et préférence sombre

Ces ressources sont indépendantes. Une application peut utiliser :

- un thème GTK fourni par son runtime ;
- un thème GTK transmis depuis l'hôte ;
- un thème d'icônes différent de celui du bureau ;
- une préférence d'apparence sombre communiquée par les portails ;
- des feuilles CSS privées embarquées dans l'application.

Changer le nom du thème GTK ne change pas automatiquement le thème d'icônes. Inversement, une icône absente ne prouve pas que le CSS est ignoré.

Pour isoler le problème, comparez une application GTK native et sa version Flatpak, si les deux existent. Utilisez la même action, la même taille de fenêtre et le même mode clair ou sombre.

## 4. Vérifier les extensions de thèmes Flatpak

Flatpak peut fournir des extensions de thèmes correspondant aux runtimes. Recherchez les extensions disponibles :

```sh
flatpak remote-ls flathub --runtime | grep -i theme
```

La disponibilité et le nom des extensions dépendent du dépôt et de la version du runtime. N'inventez pas un identifiant d'extension : vérifiez-le dans le résultat de la commande ou dans la documentation du dépôt utilisé.

Une extension de thème doit correspondre à la famille de runtime attendue. Une extension GTK 3 ne fournit pas nécessairement un thème GTK 4, et une extension de thème d'icônes ne fournit pas de feuille GTK.

Après installation ou mise à jour d'une extension, fermez complètement l'application puis relancez-la. Certaines ressources sont découvertes uniquement au démarrage du processus.

## 5. Examiner le thème réellement chargé

Pour une application GTK, activez GTK Inspector dans un environnement de test :

```sh
GTK_DEBUG=interactive flatpak run org.gnome.TextEditor
```

Le support de cette variable dépend du runtime et de la façon dont l'application a été construite. Si l'inspecteur n'est pas disponible, ne concluez pas que le thème est absent : vérifiez d'abord les extensions et les ressources exposées au bac à sable.

Dans l'inspecteur, identifiez le widget, son arbre de nœuds CSS, les classes et les providers. Comparez ces informations à celles de l'application native. Les sélecteurs privés d'une application peuvent être différents même si les deux programmes utilisent GTK.

## 6. Diagnostiquer les polices et les icônes

Une police présente sur l'hôte peut ne pas être visible par le runtime. Comparez le rendu avec une famille générique, puis vérifiez que la police est réellement accessible depuis l'environnement Flatpak.

Pour examiner les polices visibles dans le bac à sable :

```sh
flatpak run --command=sh org.gnome.TextEditor
fc-list | head
```

Si la commande n'existe pas dans le runtime, utilisez un autre outil disponible ou vérifiez les chemins montés. Ne modifiez pas les fichiers du runtime en place : les runtimes sont gérés par Flatpak et peuvent être remplacés lors d'une mise à jour.

Pour les icônes, vérifiez le nom d'icône demandé, la présence du thème correspondant et les solutions de repli. Les noms d'icônes Freedesktop sont des identifiants, pas des noms de fichiers garantis dans chaque thème.

## 7. Comprendre les portails d'apparence

Les portails XDG permettent à une application sandboxée de recevoir certaines préférences de l'environnement, notamment des préférences d'apparence prises en charge par la version du portail et du runtime.

Une préférence sombre communiquée par un portail n'est pas un transfert complet du thème CSS de l'hôte. Elle indique une préférence ou un schéma d'apparence ; l'application et son toolkit décident ensuite comment l'interpréter.

Si le mode sombre fonctionne mais que les couleurs personnalisées ne sont pas reprises, vérifiez les deux mécanismes séparément. Ne confondez pas le choix clair/sombre et le chargement d'un thème GTK arbitraire.

## 8. Procédure de diagnostic reproductible

1. Notez l'identifiant Flatpak et le runtime de l'application.
2. Notez les versions de GTK et Libadwaita disponibles.
3. Vérifiez les permissions sans les élargir.
4. Vérifiez les extensions de thème correspondant au runtime.
5. Redémarrez l'application après chaque changement de ressource.
6. Comparez une application native et une application sandboxée.
7. Inspectez les nœuds CSS si GTK Inspector est disponible.
8. Testez séparément CSS, icônes, polices et préférence sombre.
9. Consignez la distribution, le runtime et les versions testées.

Cette procédure permet de distinguer une absence de ressource, un problème de visibilité dans le bac à sable et une feuille CSS applicative prioritaire.

## 9. Limites et bonnes pratiques

Ne désactivez pas le bac à sable et n'accordez pas un accès global au système de fichiers pour obtenir une apparence uniforme. Préférez les extensions de thème officielles compatibles avec le runtime, les portails et les mécanismes documentés par Flatpak.

Certaines applications Flatpak embarquent leurs propres styles ou utilisent des composants personnalisés. Le thème de l'hôte ne peut pas imposer une apparence identique à chaque application.

Un thème publié doit indiquer les applications natives et Flatpak réellement testées. Évitez les promesses générales comme « compatible avec toutes les applications Flatpak ».

## 10. Références

- [Documentation Flatpak](https://docs.flatpak.org/)
- [Portals : documentation XDG](https://flatpak.github.io/xdg-desktop-portal/)
- [GTK 4 : CSS overview](https://docs.gtk.org/gtk4/css-overview.html)
- [GTK 3 : CSS overview](https://docs.gtk.org/gtk3/css-overview.html)
