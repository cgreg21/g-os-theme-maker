# Créer et modifier les ressources visuelles

Les icônes, curseurs, polices et fonds ne sont pas des widgets CSS. Ils ont leurs propres formats, conventions de nommage, métadonnées et règles d'installation.

## 1. Thème d'icônes

Un thème d'icônes contient des images classées par contexte et taille. Le fichier `index.theme` décrit le thème, ses répertoires et ses thèmes parents.

Exemple minimal à adapter :

```ini
[Icon Theme]
Name=MonTheme
Comment=Thème d'icônes personnel
Inherits=Adwaita,hicolor
Directories=scalable/apps,scalable/actions,scalable/status

[scalable/apps]
Size= scalable
Type=Scalable
MinSize=16
MaxSize=256
Context=Applications

[scalable/actions]
Size=scalable
Type=Scalable
MinSize=16
MaxSize=256
Context=Actions

[scalable/status]
Size=scalable
Type=Scalable
MinSize=16
MaxSize=256
Context=Status
```

Vérifiez la syntaxe attendue par la spécification Freedesktop et les versions des outils. Le champ `Size` des répertoires scalables doit respecter le format prévu par la spécification ; utilisez les exemples officiels avant de distribuer votre thème.

Arborescence habituelle :

```text
icons/MonTheme/
├── index.theme
└── scalable/
    ├── apps/
    ├── actions/
    ├── devices/
    ├── places/
    ├── status/
    └── mimetypes/
```

Les noms de fichiers doivent suivre la convention Freedesktop lorsque vous remplacez une icône standard. Une icône `org.gnome.Nautilus.svg` n'est pas nécessairement équivalente à `org.gnome.Files.svg` : recherchez le nom réellement utilisé par l'application.

### Concevoir une icône SVG

Une icône doit être lisible à petite taille. Utilisez une grille cohérente, des marges optiques, une épaisseur de trait constante et un nombre limité de détails. Les icônes symboliques doivent généralement être monochromes et recolorables. Évitez d'inscrire une couleur fixe dans le SVG si l'usage attendu est une icône symbolique.

### Vérifier les icônes manquantes

- Comparez les noms fournis avec ceux utilisés par les applications.
- Vérifiez les contextes déclarés dans `index.theme`.
- Vérifiez les thèmes parents, notamment `hicolor`.
- Testez les tailles 16, 24, 32, 48 et les tailles HiDPI.
- Vérifiez les variantes symboliques et colorées.
- Respectez la licence des œuvres originales.

## 2. Curseurs

Les thèmes de curseurs suivent la convention Xcursor et possèdent un fichier `index.theme` et un répertoire `cursors/`.

Rôles à couvrir : pointeur normal, aide, sélection de texte, attente, travail en arrière-plan, main, déplacement, copie, interdiction, redimensionnement horizontal/vertical/diagonal et précision.

Un curseur comporte une image, une taille et un hotspot. Le hotspot est le pixel qui correspond réellement au point d'action. Un hotspot incorrect donne l'impression que le pointeur clique à côté.

GNOME 51 introduit des évolutions autour de ressources SVG scalables. Cela ne signifie pas que tous les thèmes Xcursor anciens deviennent automatiquement compatibles. Vérifiez le format pris en charge par le système cible et testez chaque rôle.

## 3. Polices

Une police se compose de familles, styles, graisses et axes éventuels. Pour un thème de bureau, vérifiez :
- la famille d'interface ;
- la famille monospace ;
- les graisses régulière, moyenne et grasse ;
- les caractères accentués et les glyphes non latins ;
- les symboles, flèches et pictogrammes ;
- les licences et droits de redistribution.

Installer un fichier de police ne l'active pas automatiquement. GNOME possède des préférences de famille et de taille. Fontconfig intervient dans la découverte et le rendu des polices.

Commandes utiles :

```sh
fc-list | head
fc-match Cantarell
fc-match monospace
```

Ne forcez pas une police inexistante : le système utilisera un fallback qui peut modifier les dimensions et l'alignement.

## 4. Fonds d'écran

Un fond d'écran est une image, pas une règle CSS. Préparez des versions adaptées aux écrans et aux modes clair/sombre si le mécanisme de fond le permet. Vérifiez le cadrage, le contraste des icônes et les résolutions élevées.

Documentez pour chaque image :
- son nom ;
- sa résolution ;
- son ratio ;
- son auteur ;
- sa licence ;
- le mode ou contexte prévu ;
- la source d'origine.

Le fond du bureau, le fond de verrouillage et le fond de GDM peuvent être configurés séparément. Un thème utilisateur ne contrôle pas automatiquement l'écran de connexion.

## 5. Sons

Les thèmes sonores utilisent les conventions Freedesktop. Les sons dépendent des événements, des préférences et des applications. Un dossier de sons vide ne constitue pas un thème sonore. Vérifiez le nom de l'événement, le format audio et la licence avant d'ajouter un son.

## 6. Installation utilisateur et retour arrière

Installez les ressources dans les chemins utilisateur reconnus par la spécification XDG. Évitez de copier dans `/usr/share` pendant le développement. Gardez la possibilité de revenir au thème précédent et n'écrasez pas les ressources d'un autre thème.

Références :
- [Freedesktop Icon Theme](https://specifications.freedesktop.org/icon-theme/)
- [Icon Naming Specification](https://specifications.freedesktop.org/icon-naming-spec/)
- [Xcursor](https://www.x.org/releases/current/doc/libXcursor/)
- [Fontconfig](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)
- [XDG Base Directory](https://specifications.freedesktop.org/basedir-spec/latest/)
