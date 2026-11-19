# Créer les ressources d'un thème : icônes, curseurs, polices, fonds et sons

Un thème GNOME ne se limite pas au CSS. Les icônes, les curseurs, les polices, les fonds d'écran et les sons sont des ressources séparées, chargées par des composants différents.

Ce chapitre montre comment les organiser, les installer et les vérifier sans modifier inutilement les fichiers système.


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
32 4 4 cursor-32.png
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

Directories=stereo

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


## 10. Comprendre la résolution et l'héritage des icônes

Quand une application demande une icône, le thème recherche le nom demandé dans les répertoires déclarés, puis dans la chaîne d'héritage. Le résultat dépend du nom, du contexte, de la taille et du format disponibles.

Si une icône manque :
1. Relevez le nom exact demandé par l'application.
2. Vérifiez l'orthographe et la casse du nom de fichier.
3. Vérifiez que le répertoire est déclaré dans index.theme.
4. Vérifiez le contexte et les tailles déclarées.
5. Vérifiez la chaîne Inherits.
6. Vérifiez que le thème parent est installé.
7. Comparez avec le thème hicolor.
8. Redémarrez l'application si elle conserve les icônes en cache.

Ne créez pas un fichier de remplacement sous un nom supposé. Identifiez d'abord le nom d'icône réellement utilisé par l'application ou le composant.

### Noms alternatifs et compatibilité

Certains noms d'icônes ont des alias historiques ou plusieurs variantes. Préservez les noms Freedesktop et évitez de remplacer un nom standard par un nom propre au thème.

Si vous fournissez plusieurs noms pour le même dessin, utilisez des liens ou copies maîtrisés et documentez leur rôle. Ne dupliquez pas des centaines de fichiers sans raison : l'héritage et les alias évitent les répétitions.

## 11. Valider les icônes symboliques

Une icône symbolique est conçue pour être affichée dans une couleur fournie par l'interface. Son dessin doit rester reconnaissable à petite taille.

Contrôlez :
- silhouette à 16 px ;
- lisibilité à 24 px ;
- alignement optique ;
- épaisseur des traits ;
- espace intérieur ;
- zones transparentes ;
- rendu sur fond clair ;
- rendu sur fond sombre ;
- recoloration par le composant ;
- direction des symboles en RTL.

N'utilisez pas une icône symbolique pour un logo ou une illustration dont les couleurs sont essentielles. Inversement, une icône multicolore détaillée peut devenir illisible lorsqu'elle est réduite dans une barre d'outils.

Les fichiers SVG symboliques doivent utiliser des couleurs compatibles avec le mécanisme de recoloration prévu par l'environnement. Vérifiez le résultat dans l'application réelle : un SVG affiché directement comme image peut ne pas être recoloré de la même façon qu'une icône symbolique chargée par le thème.

## 12. Contrôler les formats et les tailles d'icônes

Un thème peut fournir des images raster, des SVG ou les deux. Le format adapté dépend du contexte, du moteur et de la taille.

Préparez une série de tests à plusieurs tailles :
- petites icônes de barre d'outils ;
- icônes de liste ;
- icônes d'application ;
- icônes de dialogue ;
- icônes de bureau ;
- icônes de menu.

Un SVG ne garantit pas automatiquement un bon rendu. Vérifiez les traits très fins, les filtres, les masques, les dégradés et les effets qui peuvent être interprétés différemment selon le moteur.

Pour les ressources raster, fournissez des tailles adaptées plutôt que d'agrandir une petite image. Les images HiDPI doivent conserver une netteté suffisante à l'échelle prévue.

## 13. Installer et diagnostiquer un thème d'icônes

Installez le thème dans le dossier utilisateur :

~~~bash
mkdir -p ~/.local/share/icons
cp -a MonTheme ~/.local/share/icons/
gsettings get org.gnome.desktop.interface icon-theme
gsettings set org.gnome.desktop.interface icon-theme 'MonTheme'
~~~

La clé GSettings peut ne pas être disponible ou modifiable dans toutes les sessions. Préférez les paramètres GNOME lorsque la configuration est gérée par la distribution ou l'environnement.

Pour diagnostiquer :
- vérifiez le chemin du thème ;
- vérifiez index.theme ;
- contrôlez les permissions de lecture ;
- vérifiez la chaîne d'héritage ;
- recherchez le nom exact de l'icône ;
- testez dans une nouvelle application ;
- comparez avec Adwaita.

Ne supprimez pas les thèmes système pour forcer le repli. Un thème incomplet doit hériter proprement des ressources manquantes.

## 14. Concevoir un thème Xcursor cohérent

Un thème de curseurs doit couvrir les rôles courants et les situations d'interaction. Il ne suffit pas de fournir une flèche personnalisée.

Prévoyez notamment :
- pointeur normal ;
- pointeur d'aide ;
- curseur texte ;
- main sur lien ;
- attente ;
- chargement ;
- déplacement ;
- précision ;
- redimensionnement horizontal ;
- redimensionnement vertical ;
- redimensionnement diagonal ;
- indisponible.

Les noms exacts sont des identifiants attendus par les applications et les toolkits. Conservez les alias nécessaires pour les noms courants. Un thème incomplet peut afficher des curseurs différents selon l'application.

### Contrôler les hotspots

Le hotspot est le point actif du curseur. Il doit correspondre à l'endroit où l'utilisateur pense cliquer.

Pour une flèche, le hotspot se trouve généralement près de la pointe. Pour une croix de précision, il se trouve généralement au centre. Pour une main, vérifiez la position du doigt indicateur.

Testez chaque curseur sur une cible précise et observez si le clic correspond au point visuel attendu. Une image esthétique avec un hotspot incorrect est un défaut fonctionnel.

### Animation des curseurs

Un curseur animé doit avoir des images cohérentes, un hotspot stable et des durées adaptées. Vérifiez :
- ordre des images ;
- durée de chaque image ;
- taille identique ;
- absence de saut de position ;
- lisibilité à petite taille ;
- comportement dans les applications ;
- repli vers un curseur statique si nécessaire.

Une animation ne doit pas gêner la lecture ou détourner l'attention en permanence.

## 15. Installer et diagnostiquer les curseurs

Placez le thème dans le dossier utilisateur prévu pour les thèmes de curseurs, puis sélectionnez-le dans les paramètres ou par la configuration disponible.

Vérifiez que le thème possède un index valide et que le dossier cursors contient les ressources référencées. Un nom de thème correct sans les fichiers attendus ne suffit pas.

Si le curseur ne change pas :
1. Vérifiez le nom du thème sélectionné.
2. Vérifiez le chemin d'installation.
3. Vérifiez le fichier index.theme.
4. Vérifiez les noms de curseurs.
5. Vérifiez les formats Xcursor.
6. Testez dans une autre application.
7. Fermez et relancez la session si nécessaire.

Wayland et X11 peuvent exposer des chemins et comportements différents. Documentez le type de session et ne concluez pas qu'un thème est universellement compatible à partir d'un seul environnement.

## 16. Gérer les polices sans casser le système

Installez les polices utilisateur dans un répertoire personnel plutôt que dans les répertoires système.

~~~bash
mkdir -p ~/.local/share/fonts/MonTheme
cp *.ttf ~/.local/share/fonts/MonTheme/
fc-cache -f
fc-list | grep -i 'Nom de la police'
fc-match sans
~~~

Ces commandes actualisent le cache et aident à vérifier que Fontconfig connaît la police. Elles ne changent pas automatiquement la police utilisée par GNOME ou par chaque application.

Sélectionnez ensuite la famille souhaitée dans les paramètres ou dans la configuration appropriée. Évitez de remplacer globalement les familles génériques sans avoir vérifié les symboles, les caractères non latins et les métriques.

### Vérifier les variantes et les glyphes

Pour chaque famille, contrôlez :
- regular ;
- medium ;
- semibold ;
- bold ;
- italic ;
- chiffres ;
- ponctuation ;
- accents ;
- caractères non latins nécessaires ;
- symboles et pictogrammes.

Une police peut être installée correctement mais ne pas contenir les glyphes nécessaires. Fontconfig peut alors utiliser une police de repli pour certains caractères.

Vérifiez les métriques : hauteur de ligne, largeur des caractères, alignement vertical et débordement. Une police plus large peut casser des boutons ou des menus même si elle est lisible.

## 17. Comprendre le repli Fontconfig

Fontconfig sélectionne les polices en fonction des familles demandées, des propriétés et des polices disponibles. Une application peut demander une famille qui n'est pas installée ; le système choisit alors une alternative.

Commandes utiles :

~~~bash
fc-match sans
fc-match serif
fc-match monospace
fc-match 'Nom de famille'
fc-list : family style file
~~~

Si une application n'utilise pas la police attendue, vérifiez la famille réellement résolue avant de modifier le CSS. Le problème peut venir du nom de famille, du poids demandé, du cache ou de l'absence de glyphes.

Ne forcez pas une police de substitution pour tous les caractères. Les scripts non latins et les symboles nécessitent parfois des polices de repli spécifiques.

## 18. Fonds d'écran et écrans multiples

Les fonds GNOME peuvent être utilisés sur le bureau et sur l'écran de verrouillage. Les mécanismes de sélection et les formats de configuration peuvent dépendre de la version et de la distribution.

Préparez plusieurs images :
- paysage large ;
- portrait ;
- image claire ;
- image sombre ;
- image à fort contraste ;
- image avec détails proches des bords.

Vérifiez le cadrage sur plusieurs résolutions et facteurs d'échelle. Une image peut être recadrée différemment selon le rapport d'aspect de l'écran.

Avec plusieurs écrans, contrôlez le fond sur chaque écran et le comportement après déconnexion ou redémarrage. Ne supposez pas que le même fichier est toujours affiché partout.

Une image de verrouillage doit rester suffisamment sobre pour que les éléments d'authentification soient lisibles. Ne placez pas de détails importants sous les champs ou indicateurs.

## 19. Thèmes sonores et respect des préférences

Les sons d'événement sont des ressources optionnelles. Leur présence dans un thème ne signifie pas qu'ils seront joués : l'application, le système sonore et les préférences de l'utilisateur déterminent leur usage.

Testez les sons avec :
- volume faible ;
- volume normal ;
- sons désactivés ;
- événement répété ;
- environnement silencieux ;
- casque et haut-parleurs.

Évitez les sons longs, agressifs ou trop fréquents. Les événements sonores ne doivent pas être le seul moyen de transmettre une information importante.

Vérifiez la licence, le format, la durée et le niveau sonore. Normalisez les fichiers de manière cohérente sans écrêter le signal.

## 20. Inventorier et vérifier les ressources

Un thème distribué doit fournir un inventaire de ses ressources et de leurs licences. Conservez la provenance de chaque fichier et indiquez si une ressource a été modifiée.

Exemple de structure d'inventaire :

~~~text
resources/
├── icons/
│   ├── applications/
│   └── symbolic/
├── cursors/
├── fonts/
├── backgrounds/
└── sounds/
~~~

Pour chaque ressource, notez :
- chemin dans l'archive ;
- nom original ;
- auteur ;
- source ;
- licence ;
- modifications ;
- format ;
- dimensions ou durée ;
- rôle dans le thème.

Vérifiez les fichiers manquants, les chemins déclarés mais absents, les doublons involontaires et les ressources non utilisées. Une ressource inutilisée alourdit l'archive et complique la maintenance.

## 21. Fiche de validation des ressources

~~~text
Nom et version du thème :
Session Wayland ou X11 :
Thème d'icônes sélectionné :
Chaîne d'héritage :
Icônes standard :
Icônes symboliques :
Tailles et formats :
Thème Xcursor :
Rôles de curseur couverts :
Hotspots :
Curseurs animés :
Polices installées :
Résultats fc-match :
Glyphes et scripts :
Métriques et alignements :
Fonds de bureau :
Écran de verrouillage :
Configuration multi-écrans :
Thème sonore :
Préférences sonores respectées :
Inventaire et licences :
Ressources manquantes :
Anomalies :
Conclusion : validé / partiel / à corriger
~~~

La validation doit être réalisée sur une session réelle. Une ressource présente dans une archive n'est pas nécessairement sélectionnée, chargée ou utilisée par GNOME.
