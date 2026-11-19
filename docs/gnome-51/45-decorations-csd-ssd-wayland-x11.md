# Décorations de fenêtres : CSD, SSD, Wayland et X11 sous GNOME 51

Ce chapitre explique qui dessine les barres de titre, les boutons de fenêtre, les bordures et les ombres. Il complète le chapitre [Mutter, fenêtres, décorations et écrans](24-mutter-fenetres-decorations-ecrans.md) et le chapitre [Mutter 51 : réglages, fenêtres et diagnostic avancé](44-mutter-reglages-fenetres-diagnostic.md).

La règle essentielle est simple : **la décoration visible n'est pas nécessairement dessinée par le gestionnaire de fenêtres**. Avant de créer une règle CSS, il faut identifier le protocole utilisé, le toolkit de l'application et le propriétaire du rendu.

## 1. Les deux modèles de décoration

### CSD — Client-Side Decorations

Avec les décorations côté client (*Client-Side Decorations*), l'application dessine sa propre barre de titre, ses boutons et souvent une partie de ses ombres et de ses bordures.

Dans une application GTK, la barre de titre peut être un `GtkHeaderBar` placée dans la fenêtre. Une application Libadwaita utilise fréquemment une barre d'en-tête intégrée à son contenu. Le style dépend alors de GTK, de Libadwaita et éventuellement du CSS propre à l'application.

Conséquences pour un thème :

- le CSS GTK peut modifier les éléments qui sont réellement exposés par le toolkit ;
- les classes et les sous-arbres exacts dépendent de l'application ;
- les boutons peuvent être des widgets GTK ordinaires ou des composants personnalisés ;
- une application peut charger sa propre feuille de style ou encapsuler certains éléments ;
- Mutter ne transforme pas automatiquement la barre d'en-tête de l'application en composant du thème Shell.

### SSD — Server-Side Decorations

Avec les décorations côté serveur (*Server-Side Decorations*), le gestionnaire de fenêtres ou le compositeur fournit le cadre extérieur et gère son intégration avec la fenêtre cliente.

Il faut distinguer au moins trois parties :

- le cadre visible et ses éventuels boutons ;
- la zone invisible ou supplémentaire utilisée pour le déplacement et le redimensionnement ;
- la surface cliente qui contient l'interface de l'application.

Ces parties n'ont pas nécessairement le même propriétaire graphique. Les dimensions du cadre influencent la géométrie de la fenêtre, mais elles ne déterminent pas le CSS du contenu de l'application.

## 2. Le cas des applications GTK et Libadwaita

Une application GTK peut construire une barre d'en-tête à l'intérieur de sa propre fenêtre. Elle peut aussi demander une fenêtre sans décoration ou utiliser une composition personnalisée.

Pour inspecter une application GTK 4 :

1. Lancez l'application avec GTK Inspector disponible.
2. Ouvrez l'inspecteur avec le raccourci configuré ou la méthode d'activation de votre environnement.
3. Sélectionnez la barre d'en-tête et ses boutons.
4. Relevez les classes, les types de widgets et les propriétés CSS.
5. Vérifiez si les éléments sont dessinés par GTK ou par un composant personnalisé.

Exemple de CSS illustratif pour une application qui expose bien un widget GTK `headerbar` :

```css
headerbar {
  min-height: 42px;
  padding: 4px 8px;
}

headerbar button {
  border-radius: 10px;
}
```

Ce code ne modifie que le rendu GTK de l'application qui charge cette feuille de style. Il ne redessine pas une décoration gérée par Mutter et ne garantit pas de résultat identique dans toutes les applications.

Dans Libadwaita, les barres d'en-tête suivent les conventions visuelles de la bibliothèque. Les applications peuvent combiner une barre d'en-tête, des vues de contenu et des contrôles propres à leur interface. Consultez [Libadwaita en détail](21-libadwaita-theming-detaille.md) avant de remplacer les styles sémantiques par des valeurs fixes.

## 3. Fenêtres natives Wayland

Dans Mutter 51.0, les fenêtres natives Wayland sont représentées par `MetaWindowWayland`. Leur initialisation marque la fenêtre comme non décorée du point de vue du cadre géré par Mutter. Cela ne signifie pas que la fenêtre n'a pas de barre de titre : cela signifie que la décoration visible est généralement fournie par le client.

Le protocole `xdg-shell` permet au client et au compositeur de coordonner les états de fenêtre : maximisation, plein écran, minimisation, déplacement, redimensionnement, contraintes de taille et relations entre fenêtres. Il ne transforme pas le CSS GTK en CSS de Mutter.

Le chemin Wayland natif doit donc être traité ainsi :

- l'application dessine son contenu et sa décoration CSD ;
- Mutter configure la surface, sa position, son état et ses contraintes ;
- GNOME Shell dessine les interfaces du bureau, comme la vue Activités et les menus ;
- le CSS Shell ne remplace pas le CSS de l'application.

Un thème global ne peut pas imposer arbitrairement la barre de titre d'une application native Wayland en modifiant seulement `gnome-shell.css`.

Sources du code Mutter 51.0 :

- [MetaWindowWayland](https://github.com/GNOME/mutter/blob/51.0/src/wayland/meta-window-wayland.c)
- [Implémentation xdg-shell](https://github.com/GNOME/mutter/blob/51.0/src/wayland/meta-wayland-xdg-shell.c)
- [Surface Wayland](https://github.com/GNOME/mutter/blob/51.0/src/wayland/meta-wayland-surface.c)

## 4. Fenêtres X11 et cadres gérés par Mutter

Le chemin X11 est différent. Mutter représente ces fenêtres avec `MetaWindowX11`. Dans le code de Mutter 51.0, les fenêtres X11 sont initialisées comme décorées par défaut ; lorsqu'un cadre est requis, Mutter crée et gère une fenêtre de cadre séparée.

Le code correspondant se trouve dans :

- [MetaWindowX11](https://github.com/GNOME/mutter/blob/51.0/src/x11/window-x11.c)
- [Gestion des cadres X11](https://github.com/GNOME/mutter/blob/51.0/src/x11/meta-x11-frame.c)
- [Structure MetaFrame](https://github.com/GNOME/mutter/blob/51.0/src/x11/meta-x11-frame.h)

Le cadre possède une géométrie distincte de celle de la surface cliente. Mutter doit connaître les bordures visibles et les bordures supplémentaires pour calculer correctement la position, le redimensionnement et les dimensions globales.

Dans Mutter 51.0, le code de cadre interroge notamment les propriétés X11 suivantes :

- `_GTK_FRAME_EXTENTS` pour les extensions de cadre invisibles annoncées par le composant qui gère la décoration ;
- `_MUTTER_FRAME_EXTENTS` pour les extensions visibles du cadre.

Mutter utilise ces valeurs pour ses calculs de géométrie. Ce sont des propriétés de coordination internes au fonctionnement des cadres X11, pas des sélecteurs CSS ni une interface de personnalisation à modifier manuellement.

Ne créez pas ces propriétés avec `xprop -f` pour tenter de dessiner une bordure. Vous risqueriez de désynchroniser la géométrie de la fenêtre, la zone de saisie et la zone de redimensionnement.

## 5. Applications X11 exécutées dans une session Wayland

Une session Wayland peut également exécuter des applications X11 via Xwayland. Ces applications ne deviennent pas des clients Wayland natifs simplement parce que le bureau utilise Wayland.

Leur chemin de gestion conserve des caractéristiques X11. Mutter possède une implémentation spécifique `MetaWindowXwayland`, qui s'appuie sur le chemin des fenêtres X11 et l'associe à une surface Wayland.

Cela explique pourquoi deux applications ouvertes dans la même session peuvent avoir des comportements différents :

- une application GTK native Wayland peut dessiner sa propre CSD ;
- une ancienne application X11 peut utiliser des mécanismes de décoration X11 ;
- une application X11 lancée via Xwayland peut présenter des contraintes propres à cette compatibilité ;
- une application Electron peut dépendre de sa version, de son backend et de ses options de lancement.

Sources :

- [MetaWindowXwayland](https://github.com/GNOME/mutter/blob/51.0/src/wayland/meta-window-xwayland.c)
- [MetaXwaylandSurface](https://github.com/GNOME/mutter/blob/51.0/src/wayland/meta-xwayland-surface.c)

## 6. Identifier le protocole utilisé par une application

Commencez par identifier le type de session :

```bash
printf 'Session : %s\n' "$XDG_SESSION_TYPE"
```

Cette variable décrit la session du bureau, pas nécessairement le protocole de chaque application. Dans une session Wayland, une application peut toujours être exécutée via Xwayland.

Pour une application GTK, vérifiez ses informations de processus et son environnement :

```bash
ps -eo pid,comm,args | grep -E 'gnome|gtk|electron|firefox'
```

Les informations de lancement seules ne suffisent pas toujours à déterminer le backend. Consultez les journaux de l'application, ses options de lancement et sa documentation.

Pour les fenêtres X11 accessibles au serveur X :

```bash
xprop
```

Cliquez ensuite sur la fenêtre à inspecter. Les propriétés `_NET_WM_NAME`, `WM_CLASS`, `_NET_WM_STATE` et, si elles existent, `_NET_FRAME_EXTENTS` aident à comprendre la fenêtre.

Limites importantes :

- `xprop` ne voit que les fenêtres exposées au serveur X auquel il se connecte ;
- dans une session Wayland, il inspecte principalement les clients Xwayland ;
- il ne permet pas d'inspecter directement toutes les surfaces Wayland natives ;
- l'absence d'une propriété X11 ne prouve pas l'absence de décoration.

Pour une application GTK, utilisez également GTK Inspector. Pour le Shell, utilisez Looking Glass et l'inspection St. Les outils et les couches d'inspection sont différents.

## 7. Comprendre les bordures visibles et invisibles

Une fenêtre peut avoir une bordure visible très fine et une zone de redimensionnement plus large. C'est volontaire : les cibles interactives doivent rester utilisables sans imposer une bordure épaisse.

Sous X11, Mutter distingue les extensions visibles et invisibles du cadre. Le réglage `draggable-border-width` de `org.gnome.mutter` agit sur la zone de bordure interactive globale, pas sur l'épaisseur CSS d'une barre d'en-tête.

Inspectez le réglage :

```bash
gsettings describe org.gnome.mutter draggable-border-width
gsettings get org.gnome.mutter draggable-border-width
```

Ne cherchez pas à reproduire cette zone avec une marge CSS. Une marge agrandit ou déplace un widget ; elle ne modifie pas la région d'entrée du cadre de fenêtre.

## 8. Ombres et coins arrondis

Les ombres et les coins arrondis peuvent être produits à plusieurs niveaux :

- le widget GTK de l'application ;
- le rendu propre à Libadwaita ;
- le cadre d'une fenêtre X11 ;
- la surface ou la texture composée par Mutter ;
- un acteur d'aperçu créé par GNOME Shell ;
- un effet graphique propre à l'application.

Une capture d'écran peut montrer une ombre sans permettre d'en identifier le propriétaire. Comparez le rendu de l'application en fenêtre normale, maximisée, en plein écran et dans un aperçu du Shell.

Ne supprimez pas toutes les ombres sans vérifier le contraste entre les fenêtres. Sur un fond uniforme, une ombre légère ou une bordure discrète aide à identifier les limites de chaque surface.

## 9. Matrice de diagnostic sans tableau

### La barre de titre change avec le CSS de l'application

Le composant est probablement une CSD. Continuez l'inspection GTK ou le diagnostic du CSS propre à l'application.

### La barre de titre ne change pas avec le CSS GTK

Vérifiez si elle est dessinée par un autre toolkit, par l'application elle-même ou par le chemin X11 de décoration. Le CSS GTK ne s'applique pas à tous les clients.

### Le Shell change, mais pas la barre de titre

C'est normal lorsque la barre appartient à l'application. Le thème Shell et le thème GTK sont chargés par des moteurs distincts.

### La fenêtre X11 possède une bordure invisible

Vérifiez les réglages de redimensionnement et les extensions de cadre. La zone interactive peut dépasser la bordure visible.

### Le rendu diffère entre Wayland natif et Xwayland

Identifiez le backend de l'application et comparez les deux chemins. Ne déduisez pas le comportement d'une application native Wayland à partir d'une fenêtre X11.

### Les coins arrondis disparaissent en plein écran

Le plein écran modifie la géométrie et peut supprimer les marges ou les effets de cadre. Ce changement ne signifie pas nécessairement que le CSS a été ignoré.

## 10. Procédure de travail pour un créateur de thème

Pour chaque application de référence :

1. Notez son toolkit et son backend graphique.
2. Déterminez si la décoration est CSD ou SSD.
3. Inspectez la barre de titre avec l'outil adapté au toolkit.
4. Inspectez les propriétés X11 uniquement si la fenêtre est accessible via X11.
5. Relevez les classes CSS réellement présentes.
6. Créez une règle limitée au moteur concerné.
7. Testez en fenêtre normale, maximisée et en plein écran.
8. Répétez sous Wayland natif et Xwayland si ces deux chemins font partie des cibles.
9. Documentez les limites propres à l'application.

Un thème sérieux doit annoncer ses limites. Il vaut mieux indiquer qu'une décoration est contrôlée par une application que promettre un résultat uniforme que le moteur ne peut pas garantir.

## 11. Sources officielles GNOME 51.0

- [Mutter — fenêtres X11](https://github.com/GNOME/mutter/blob/51.0/src/x11/window-x11.c)
- [Mutter — cadres X11](https://github.com/GNOME/mutter/blob/51.0/src/x11/meta-x11-frame.c)
- [Mutter — structure des cadres](https://github.com/GNOME/mutter/blob/51.0/src/x11/meta-x11-frame.h)
- [Mutter — fenêtres Wayland](https://github.com/GNOME/mutter/blob/51.0/src/wayland/meta-window-wayland.c)
- [Mutter — protocole xdg-shell](https://github.com/GNOME/mutter/blob/51.0/src/wayland/meta-wayland-xdg-shell.c)
- [Mutter — fenêtres Xwayland](https://github.com/GNOME/mutter/blob/51.0/src/wayland/meta-window-xwayland.c)
- [GTK 4 — CSS overview](https://docs.gtk.org/gtk4/css-overview.html)
- [GTK 3 — CSS overview](https://docs.gtk.org/gtk3/css-overview.html)
- [Libadwaita — styles et apparence](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)

Les sources de Mutter sont épinglées sur 51.0. Les documentations GTK et Libadwaita suivent leurs versions documentées : vérifiez la version réellement installée avant de vous fier à une propriété récente.
