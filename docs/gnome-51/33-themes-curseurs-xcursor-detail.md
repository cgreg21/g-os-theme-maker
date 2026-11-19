# Concevoir et diagnostiquer un thème de curseurs Xcursor

Un thème de curseurs est une ressource distincte du thème d'icônes. Il fournit des images adaptées aux rôles du pointeur, avec un point chaud et parfois plusieurs images animées. Ce chapitre détaille sa structure, sa fabrication et les tests à effectuer dans une session graphique.

## 1. Structure d'un thème

Un thème utilisateur est installé dans `~/.local/share/icons/NomCurseur` :

```text
NomCurseur/
├── index.theme
└── cursors/
    ├── left_ptr
    ├── hand
    ├── text
    ├── watch
    ├── crosshair
    ├── move
    └── ...
```

Le fichier `index.theme` minimal :

```ini
[Icon Theme]
Name=NomCurseur
Comment=Curseurs de démonstration
Inherits=Adwaita
```

Le format réutilise une partie de la convention des thèmes d'icônes, mais les fichiers du dossier `cursors` sont des ressources Xcursor, pas des PNG simplement renommés.

## 2. Rôles de curseur et compatibilité

Les applications peuvent demander différents rôles : pointeur normal, sélection de texte, lien, attente, déplacement, précision, redimensionnement horizontal ou vertical, redimensionnement diagonal et glisser-déposer.

Les noms courants incluent `left_ptr`, `text`, `hand`, `watch`, `crosshair`, `fleur`, `move`, `sb_h_double_arrow` et `sb_v_double_arrow`. Les noms exacts attendus peuvent varier selon les toolkits et les applications.

Ne créez pas uniquement le curseur flèche. Un thème incomplet peut afficher un mélange de curseurs provenant du thème parent, ou des curseurs de repli inattendus. Conservez une liste de compatibilité et testez les interactions réelles.

## 3. Le point chaud

Le point chaud (*hotspot*) est la coordonnée de l'image qui correspond à la position réelle du pointeur. Pour une flèche, il se trouve généralement près de la pointe. Pour une croix, il est généralement au centre.

Un hotspot erroné se remarque immédiatement : les clics semblent décalés par rapport au dessin. Le hotspot doit rester cohérent entre les différentes tailles et les images d'une animation.

Pour chaque ressource, vérifiez :

- la position du hotspot ;
- la taille logique et les tailles haute densité ;
- la netteté des contours ;
- le contraste sur fonds clairs et foncés ;
- l'alignement entre les images d'une animation.

## 4. Générer un fichier avec xcursorgen

`xcursorgen` construit un fichier Xcursor à partir d'images PNG et d'un fichier de description. Chaque ligne indique la taille nominale du curseur, le hotspot horizontal et vertical, le fichier PNG et, pour une animation, la durée d'affichage en millisecondes. Le délai est facultatif pour une image statique.

Exemple pour un curseur statique de taille nominale 32 :

```text
# taille xhot yhot image.png
32 4 4 pointer-32.png
```

Exemple pour une animation de trois images de même taille nominale :

```text
# taille xhot yhot image.png délai_ms
32 15 15 watch-1.png 100
32 15 15 watch-2.png 100
32 15 15 watch-3.png 100
```

Les lignes de même taille constituent les images successives du curseur animé. Le délai appartient à chaque image. Vérifiez que les hotspots restent cohérents et que les images sont conçues pour la même taille nominale.

Générez le fichier :

```bash
xcursorgen pointer.conf left_ptr
file left_ptr
```

Le délai nul est adapté à une image statique. Pour une animation, fournissez plusieurs lignes avec des durées cohérentes et des images dont les dimensions et hotspots sont compatibles. Vérifiez la syntaxe exacte avec `man xcursorgen` sur votre distribution.

Une image PNG de 32 × 32 pixels avec un hotspot à (4, 4) n'est qu'un exemple : la taille nominale et les coordonnées doivent correspondre au dessin réel. Les coordonnées commencent à zéro. Le paramètre `size` est la taille nominale Xcursor, pas un délai.

## 5. Tailles et HiDPI

Ne supposez pas que doubler les pixels de l'image suffit à produire un curseur HiDPI correct. Le rendu dépend de la taille demandée par le serveur d'affichage, du toolkit et de la session.

Fournissez des images de bonne qualité, évitez l'agrandissement d'un petit bitmap et testez au moins une échelle standard et une échelle élevée. La taille apparente doit rester cohérente avec les contrôles de l'interface.

Les curseurs vectoriels peuvent être utiles dans certains environnements, mais la compatibilité de bout en bout ne doit pas être présumée. Pour un thème Xcursor distribuable, testez le format réellement chargé par la session et gardez un repli compatible.

## 6. Installer et sélectionner le thème

Installez le dossier dans :

```text
~/.local/share/icons/NomCurseur/
```

Vérifiez les paramètres disponibles :

```bash
gsettings get org.gnome.desktop.interface cursor-theme
gsettings get org.gnome.desktop.interface cursor-size
```

Sélectionnez le thème :

```bash
gsettings set org.gnome.desktop.interface cursor-theme 'NomCurseur'
```

La taille se règle séparément. Ne changez pas la taille globale dans un paquet de thème sans expliquer ce choix : elle relève d'une préférence d'accessibilité et de confort.

Selon le serveur d'affichage et les applications, le changement peut ne pas être visible partout immédiatement. Déconnectez-vous puis reconnectez-vous si nécessaire, et comparez plusieurs applications.

## 7. Tester systématiquement

Testez au minimum :

1. bureau et panneau supérieur ;
2. fenêtre GTK 3 ;
3. fenêtre GTK 4/Libadwaita ;
4. champ de saisie ;
5. lien cliquable ;
6. poignée de redimensionnement ;
7. glisser-déposer ;
8. attente et animation ;
9. affichage HiDPI ;
10. écran clair et écran sombre.

Un curseur doit être visible sans être agressif. Vérifiez aussi que sa taille et son contraste restent utilisables par les personnes ayant une vision réduite.

## 8. Diagnostic

**Le thème ne se charge pas.** Vérifiez le chemin, la présence de `index.theme`, le nom du thème sélectionné et la validité du fichier Xcursor.

**Le pointeur fonctionne mais les autres rôles sont incohérents.** Complétez les noms attendus et utilisez l'héritage pour les rôles non fournis.

**Le clic est décalé.** Corrigez le hotspot dans la configuration de génération.

**Le curseur est flou.** Fournissez une ressource adaptée à la taille demandée au lieu d'étirer un petit bitmap.

**Une application ignore le thème.** Vérifiez son toolkit, son environnement d'exécution et le serveur d'affichage. Une application isolée peut avoir un comportement différent de celui des applications natives.

## 9. Exercice guidé

Créez un thème qui remplace uniquement le pointeur standard et le curseur de texte. Faites hériter les autres rôles d'Adwaita. Vérifiez les hotspots, puis complétez progressivement les rôles manquants. Gardez une capture de chaque étape pour repérer les régressions.

## 10. Références

- [Xcursor — documentation de libXcursor](https://www.x.org/releases/current/doc/libXcursor/)
- [xcursorgen — manuel](https://manpages.debian.org/xcursorgen)
- [Spécification Freedesktop des thèmes d'icônes](https://specifications.freedesktop.org/icon-theme/)


## 11. Noms de curseurs et liens de compatibilité

Le nom de fichier dans `cursors/` est un nom de rôle, pas un nom arbitraire choisi pour décrire le dessin. Les applications et toolkits peuvent demander des noms différents pour une même intention. Il est donc courant de fournir plusieurs noms compatibles qui pointent vers un même fichier Xcursor.

Exemple de lien dans le dossier `cursors` :

```bash
ln -s left_ptr default
ln -s hand pointer
ln -s text xterm
```

Ces exemples illustrent le mécanisme ; ils ne remplacent pas un inventaire vérifié des noms réellement demandés. Ne créez un alias que si les deux noms désignent bien le même comportement. Conservez les noms de base attendus par les environnements ciblés et testez les applications GTK, Qt et les applications XWayland.

Pour inspecter les liens et leurs cibles :

```bash
find cursors -maxdepth 1 -type l -printf '%f -> %l\n'
```

Un lien cassé équivaut à une ressource absente. Pour un paquet qui doit être extrait sur différents systèmes, vérifiez que l'archive préserve les liens symboliques ; sinon, fournissez des fichiers ordinaires.

## 12. Tailles nominales et images sources

La taille inscrite dans la configuration `xcursorgen` décrit la taille nominale de l'image Xcursor. Elle ne doit pas être confondue avec la taille du PNG en pixels ni avec le facteur d'échelle de GNOME.

Un thème peut fournir plusieurs tailles nominales pour un même rôle. Pour chaque taille :

- choisissez une source PNG adaptée, sans agrandissement excessif ;
- vérifiez les dimensions réelles du fichier ;
- placez le hotspot au même endroit fonctionnel ;
- comparez l'épaisseur des traits et la lisibilité ;
- testez l'affichage sur un écran standard et un écran HiDPI.

Exemple de génération de deux variantes du même rôle :

```text
24 3 3 pointer-24.png
32 4 4 pointer-32.png
48 6 6 pointer-48.png
```

Les trois lignes de tailles différentes sont des variantes de taille, pas les images d'une animation. Pour une animation, plusieurs lignes partagent la même taille nominale et possèdent un délai.

## 13. Vérifier le résultat généré

Après génération, vérifiez que le fichier est bien reconnu comme un curseur Xcursor :

```bash
file cursors/left_ptr
```

Inspectez également la configuration et les sources utilisées :

```bash
nl -ba pointer.conf
file pointer-*.png
```

Si le curseur est décalé, vérifiez d'abord le hotspot. S'il est flou, comparez les sources PNG à la taille nominale demandée. Si l'animation est trop rapide ou trop lente, ajustez les délais en millisecondes, pas les dimensions.

La validation finale doit se faire dans une session graphique réelle. Un fichier reconnu par `file` peut encore présenter un hotspot incorrect, un contraste insuffisant ou une animation incohérente.

## 14. Déployer et revenir en arrière

Installez le thème dans le répertoire utilisateur :

```bash
install -d "$HOME/.local/share/icons/NomCurseur"
cp -a ./NomCurseur/. "$HOME/.local/share/icons/NomCurseur/"
```

Avant de changer le thème, notez les valeurs actuelles :

```bash
gsettings get org.gnome.desktop.interface cursor-theme
gsettings get org.gnome.desktop.interface cursor-size
```

Après le test, restaurez le nom et la taille précédents avec `gsettings set`. Ne réinitialisez pas toutes les préférences GNOME pour annuler un essai de curseur.

Pour mettre à jour un thème, préparez et vérifiez une copie complète avant de remplacer l'ancienne. Une simple copie par-dessus peut laisser des curseurs obsolètes qui ne figurent plus dans la nouvelle version.

## 15. Références complémentaires

- [Manuel xcursorgen — format du fichier de configuration](https://manpages.debian.org/bookworm/x11-apps/xcursorgen.1.en.html)
- [Xcursor — documentation de libXcursor](https://www.x.org/releases/current/doc/libXcursor/)
