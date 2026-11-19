# Créer les ressources d'un thème : icônes, curseurs, polices, fonds et sons

Un thème GNOME ne se limite pas au CSS. Les icônes, les curseurs, les polices, les fonds d'écran et les sons sont des ressources séparées, chargées par des composants différents.

Ce chapitre montre comment les organiser, les installer et les vérifier sans modifier inutilement les fichiers système.

![Aperçu du fond d'écran Adwaita GNOME 51 avec variantes claire et sombre](https://release.gnome.org/51/adwaita-thumb.webp)

## 1. Organiser les ressources

Un thème complet peut contenir plusieurs dossiers indépendants :

~~~text
MonTheme/
├── gnome-shell/
│   └── gnome-shell.css
├── gtk-3.0/
│   └── gtk.css
├── gtk-4.0/
│   └── gtk.css
├── icons/
│   └── MonTheme/
│       └── index.theme
├── cursors/
│   └── MonCurseur/
│       ├── index.theme
│       └── cursors/
├── backgrounds/
├── sounds/
│   └── MonSon/
│       └── index.theme
├── fonts/
└── README.md
~~~

Tous ces dossiers ne sont pas chargés par le même moteur. Le thème Shell ne remplace pas le thème d'icônes, et un dossier de polices ne change pas automatiquement la police active du bureau.

## 2. Thème d'icônes

### Structure

Un thème d'icônes possède un fichier index.theme et des répertoires classés par taille et par contexte. Les contextes usuels sont :

- Applications ;
- Actions ;
- Devices ;
- Places ;
- Status ;
- MimeTypes ;
- Emblems ;
- Categories.

Exemple minimal :

~~~ini
[Icon Theme]
Name=MonTheme
Comment=Thème d'icônes personnel
Inherits=Adwaita,hicolor
Directories=48x48/apps,scalable/apps,scalable/actions

[48x48/apps]
Size=48
Type=Fixed
Context=Applications

[scalable/apps]
Size=48
Type=Scalable
MinSize=16
MaxSize=256
Context=Applications

[scalable/actions]
Size=16
Type=Scalable
MinSize=16
MaxSize=64
Context=Actions
~~~

Le chemin des répertoires déclaré dans Directories doit correspondre exactement à leur emplacement. Un dossier présent mais absent de index.theme peut ne pas être utilisé.

### Nommage

Les noms d'icônes suivent la spécification Freedesktop. Utilisez les noms standards lorsqu'ils existent. Évitez de renommer les icônes en fonction de leur apparence : leur nom doit décrire leur fonction.

Un thème peut hériter d'un autre thème. Déclarez hicolor comme repli afin que les icônes manquantes puissent être recherchées dans la hiérarchie.

### Icônes symboliques

Les icônes symboliques sont monochromes et conçues pour être recolorées par le moteur qui les affiche. Les fichiers utilisent couramment le suffixe -symbolic.svg.

Bonnes pratiques :

- tracés simples et lisibles à petite taille ;
- épaisseur de trait cohérente ;
- marges optiques régulières ;
- couleurs non codées lorsque l'icône doit être recolorée ;
- vérification sur fonds clairs et sombres ;
- vérification des variantes RTL pour les symboles directionnels.

Ne transformez pas une icône multicolore en icône symbolique en supprimant simplement ses couleurs : simplifiez d'abord sa forme.

### Vérifier le thème

~~~bash
find ~/.local/share/icons/MonTheme -maxdepth 3 -type f
gsettings get org.gnome.desktop.interface icon-theme
~~~

Installez le thème dans ~/.local/share/icons/MonTheme. Sélectionnez-le ensuite dans les paramètres ou avec GSettings si la clé est disponible.

## 3. Thème de curseurs

Les curseurs utilisent un format dédié. Un thème Xcursor classique contient un dossier cursors et un index.theme.

~~~ini
[Icon Theme]
Name=MonCurseur
Comment=Curseurs personnalisés
Inherits=Adwaita
~~~

Le dossier cursors contient les ressources nommées selon les rôles attendus par le système : pointeur, texte, main, attente, déplacement, précision et redimensionnement.

Les noms peuvent être des alias vers un même fichier de curseur. Préservez les noms standards utilisés par les applications et les toolkits.

### Hotspot et tailles

Un curseur possède un point chaud (*hotspot*) : le pixel qui correspond à la position réelle du pointeur. Une flèche dont le hotspot est mal placé donne l'impression que le clic se produit à côté de la pointe.

Vérifiez :
- la taille standard ;
- les tailles HiDPI ;
- le hotspot ;
- les variantes claire et sombre ;
- les curseurs animés ;
- les alias de noms ;
- les replis vers le thème parent.

### Générer un curseur Xcursor

xcursorgen peut créer un fichier Xcursor depuis des images et un fichier de configuration. La configuration indique l'image, le hotspot et la durée de chaque image.

~~~text
# Exemple de ligne de configuration xcursorgen
32 4 4 0 cursor-32.png
~~~

Cette ligne est un exemple de structure, pas une configuration universelle. Adaptez les dimensions et le hotspot à votre image. Consultez xcursorgen --help et la documentation installée.

### GNOME 51 et les curseurs SVG

GNOME 51 améliore le rendu des curseurs à partir de ressources SVG scalables. Cela ne signifie pas que chaque thème Xcursor ancien devient automatiquement un thème SVG. Conservez les formats et replis nécessaires aux applications, serveurs d'affichage et environnements ciblés.

## 4. Polices

Les polices sont gérées par Fontconfig et les paramètres GNOME, pas par le CSS Shell seul.

### Installer une police pour l'utilisateur

Placez les fichiers de police dans un dossier utilisateur :

~~~bash
mkdir -p ~/.local/share/fonts
cp MaPolice-Regular.ttf ~/.local/share/fonts/
fc-cache -f
~~~

Vérifiez que Fontconfig la détecte :

~~~bash
fc-list | grep -i "MaPolice"
fc-match "MaPolice"
~~~

Le nom de famille déclaré dans le fichier de police peut être différent du nom du fichier.

### Choisir les polices GNOME

Le schéma org.gnome.desktop.interface expose généralement des clés telles que :

- font-name : police d'interface ;
- document-font-name : police des documents ;
- monospace-font-name : police à chasse fixe ;
- text-scaling-factor : facteur d'échelle du texte.

Vérifiez les clés réellement disponibles :

~~~bash
gsettings list-keys org.gnome.desktop.interface
gsettings get org.gnome.desktop.interface font-name
~~~

Ne modifiez pas les préférences de l'utilisateur sans son accord. Un thème partageable peut fournir une police et expliquer comment l'activer, mais ne doit pas écraser silencieusement la configuration personnelle.

### Couverture des glyphes

Vérifiez les accents, symboles, caractères grecs, cyrilliques, arabes, asiatiques et emoji selon les langues ciblées. Fontconfig peut choisir une police de remplacement pour les caractères absents.

Respectez les licences des polices : certaines autorisent la redistribution, d'autres non.

## 5. Fonds d'écran

Les fonds d'écran sont des ressources gérées par GNOME et les paramètres de session. Ils ne sont pas des widgets CSS.

Prévoyez :
- une image principale ;
- une variante sombre si elle existe ;
- une résolution suffisante ;
- un recadrage adapté aux écrans larges et verticaux ;
- un rendu sur plusieurs écrans ;
- les crédits et la licence.

### Installer une image pour le compte courant

Placez les images dans un dossier utilisateur, par exemple ~/Pictures/Wallpapers ou ~/.local/share/backgrounds.

Pour définir le fond du bureau :

~~~bash
gsettings set org.gnome.desktop.background picture-uri \
  'file:///home/utilisateur/.local/share/backgrounds/mon-fond.jpg'
~~~

Pour une variante sombre, vérifiez la présence de la clé :

~~~bash
gsettings list-keys org.gnome.desktop.background
~~~

Le fond du verrouillage relève de org.gnome.desktop.screensaver. Le greeter GDM utilise une configuration distincte. Ne supposez pas qu'une image choisie pour le bureau sera automatiquement utilisée dans les trois contextes.

### Apparaître dans le sélecteur de fonds

Le fait de copier une image dans un dossier ne garantit pas qu'elle apparaisse dans le sélecteur de fonds GNOME. La liste des fonds fournis par la distribution peut dépendre de métadonnées et de fichiers installés au niveau système.

Pour un thème utilisateur simple, documentez le chemin de l'image et fournissez une méthode explicite pour la choisir. N'écrivez pas dans les répertoires système sans privilèges et sans procédure adaptée.

## 6. Sons

Les thèmes sonores suivent la convention Freedesktop. Ils sont séparés des thèmes GTK et Shell.

Un thème sonore contient un index.theme qui déclare son nom, son thème parent et ses répertoires. Les fichiers audio sont nommés selon les événements attendus par les applications et les services.

Exemple de structure :

~~~text
sounds/
└── MonSon/
    ├── index.theme
    └── stereo/
        ├── dialog-warning.oga
        ├── dialog-error.oga
        └── device-added.oga
~~~

Exemple de métadonnées :

~~~ini
[Sound Theme]
Name=MonSon
Comment=Thème sonore personnel
Inherits=freedesktop

[stereo]
OutputProfile=stereo
~~~

Les noms d'événements disponibles dépendent des applications et de la spécification sonore utilisée. Fournir un fichier audio ne signifie pas que chaque application l'utilisera.

Vérifiez les préférences sonores de GNOME :

~~~bash
gsettings list-recursively org.gnome.desktop.sound
~~~

Les sons doivent être optionnels. Respectez les préférences de l'utilisateur, les réglages de volume et les situations où les retours sonores doivent être désactivés.

## 7. Licences et attribution

Pour chaque ressource, conservez :

- nom et auteur ;
- URL de provenance ;
- licence exacte ;
- modifications apportées ;
- restrictions de redistribution ;
- version ou date de récupération.

N'incluez pas une police, une icône ou un fond trouvé sur Internet sans vérifier sa licence. Une ressource visible publiquement n'est pas nécessairement librement redistribuable.

## 8. Exercices

### Exercice A — icônes

Créez un index.theme minimal, ajoutez deux icônes d'application et vérifiez l'héritage vers Adwaita.

### Exercice B — curseurs

Créez un curseur pointeur et un curseur texte. Vérifiez le hotspot et les tailles HiDPI.

### Exercice C — polices

Installez une police dans le dossier utilisateur, vérifiez-la avec fc-match, puis activez-la volontairement dans les paramètres GNOME.

### Exercice D — fonds

Ajoutez une image claire et une image sombre, puis vérifiez le bureau, le verrouillage et le comportement multi-écrans.

### Exercice E — sons

Créez un thème sonore minimal et vérifiez qu'il n'altère pas les préférences de volume de l'utilisateur.

## 9. Sources et outils

- [Spécification Freedesktop des thèmes d'icônes](https://specifications.freedesktop.org/icon-theme/)
- [Spécification des noms d'icônes](https://specifications.freedesktop.org/icon-naming-spec/)
- [Spécification Xcursor](https://www.x.org/releases/current/doc/libXcursor/)
- [Fontconfig — guide utilisateur](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)
- [Spécification des thèmes sonores](https://www.freedesktop.org/wiki/Specifications/sound-theme-spec/)
- [Notes de version GNOME 51](https://release.gnome.org/51/)
