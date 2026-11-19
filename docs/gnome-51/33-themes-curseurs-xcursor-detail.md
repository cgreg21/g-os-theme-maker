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

`xcursorgen` construit un fichier Xcursor à partir d'images PNG et d'un fichier de description. Une ligne décrit la durée, le hotspot horizontal et vertical, puis le chemin de l'image.

Exemple pour un curseur statique :

```text
# délai_ms hotspot_x hotspot_y image.png
0 4 4 pointer-32.png
```

Générez le fichier :

```bash
xcursorgen pointer.conf left_ptr
file left_ptr
```

Le délai nul est adapté à une image statique. Pour une animation, fournissez plusieurs lignes avec des durées cohérentes et des images dont les dimensions et hotspots sont compatibles. Vérifiez la syntaxe exacte avec `man xcursorgen` sur votre distribution.

Une image de 32 × 32 pixels avec un hotspot à (4, 4) n'est qu'un exemple : la valeur doit correspondre au dessin réel. Les coordonnées commencent à zéro.

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
