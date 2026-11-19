# Maîtriser Fontconfig et la typographie du bureau

La typographie d'un bureau repose sur plusieurs couches. Fontconfig découvre les polices et choisit des correspondances ; FreeType rasterise les glyphes ; Pango assure la mise en forme du texte pour de nombreuses applications GTK ; GTK et GNOME définissent les polices et tailles utilisées par l'interface. Changer une seule couche ne contrôle donc pas tout le rendu.

## 1. Séparer les responsabilités

**Fontconfig** recherche les fichiers de polices et applique des règles de correspondance. Il gère les familles, styles, graisses, langues et replis.

**FreeType** lit les contours des polices et produit les glyphes rasterisés.

**Pango** compose le texte, gère les scripts, les langues, les formes contextuelles et la direction d'écriture.

**GTK et GNOME** choisissent les polices et tailles de l'interface. Le CSS peut définir la typographie d'un widget, mais ne remplace pas les règles globales de sélection de polices.

Cette séparation aide à diagnostiquer le bon niveau. Si une police n'est pas trouvée, commencez par Fontconfig. Si un caractère manque, vérifiez le repli. Si l'alignement du texte est incorrect, inspectez aussi Pango et les propriétés du widget.

## 2. Installer des polices pour l'utilisateur

Créez un dossier personnel et copiez uniquement des fichiers dont la licence autorise l'utilisation prévue :

```bash
mkdir -p ~/.local/share/fonts
cp ./MaPolice-Regular.ttf ~/.local/share/fonts/
fc-cache -f ~/.local/share/fonts
```

Vérifiez la détection :

```bash
fc-list | grep -i 'MaPolice'
fc-match 'MaPolice'
fc-match sans-serif
fc-match monospace
```

Le nom de famille enregistré dans la police peut différer du nom du fichier. Utilisez le nom retourné par les outils plutôt que de déduire la famille à partir du nom du fichier.

Pour supprimer une police, retirez le fichier installé par vos soins puis reconstruisez le cache du dossier. Ne supprimez jamais des fichiers de polices système pour corriger un thème.

## 3. Comprendre les familles génériques

Les familles génériques courantes sont :

- `sans-serif` pour le texte d'interface ;
- `serif` pour les textes à empattements ;
- `monospace` pour le code et les colonnes alignées ;
- `cursive` et `fantasy` lorsque l'application les utilise.

Une famille générique est une demande, pas un nom de fichier précis. Fontconfig la résout selon la configuration locale, les polices installées et la couverture linguistique.

Une famille peut exister sans contenir tous les glyphes nécessaires. Le système sélectionne alors des polices de repli pour les caractères absents. Testez des textes réels : accents français, apostrophes typographiques, symboles, grec, cyrillique, arabe et scripts asiatiques selon les langues ciblées.

## 4. Paramètres GNOME

Inspectez les clés réellement disponibles sur la machine :

```bash
gsettings list-keys org.gnome.desktop.interface
gsettings get org.gnome.desktop.interface font-name
gsettings get org.gnome.desktop.interface document-font-name
gsettings get org.gnome.desktop.interface monospace-font-name
gsettings get org.gnome.desktop.interface text-scaling-factor
```

Les noms de clés et valeurs par défaut peuvent évoluer avec la distribution. Ne copiez pas une commande trouvée pour une autre version sans vérifier le schéma installé.

Pour tester temporairement une police d'interface :

```bash
gsettings set org.gnome.desktop.interface font-name 'Cantarell 11'
```

Avant de modifier une valeur, notez-la afin de pouvoir la restaurer. Un thème redistribuable doit expliquer comment activer une police, mais ne doit pas remplacer silencieusement les préférences personnelles.

## 5. Configuration Fontconfig utilisateur

Fontconfig permet d'ajouter des règles dans `~/.config/fontconfig/conf.d/`. Les règles système se trouvent généralement dans des dossiers comme `/etc/fonts/conf.d` et `/usr/share/fontconfig/conf.avail`, selon la distribution.

Exemple de fichier utilisateur qui ajoute un alias de famille :

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <alias>
    <family>MonInterface</family>
    <prefer>
      <family>Cantarell</family>
      <family>Noto Sans</family>
    </prefer>
  </alias>
</fontconfig>
```

Enregistrez-le sous `~/.config/fontconfig/conf.d/50-mon-interface.conf`, puis vérifiez la configuration :

```bash
fc-match MonInterface
fc-conflist
fc-cache -f
```

Une règle d'alias ne crée pas une police et ne modifie pas les fichiers originaux. Elle indique à Fontconfig quelles familles préférer pour une demande donnée.

Évitez les règles globales complexes qui remplacent toutes les familles ou toutes les graisses : elles peuvent casser les applications, les symboles et les langues qui ont besoin d'un repli particulier.

## 6. Graisses, styles et variables

Les familles peuvent proposer des styles Regular, Medium, Semibold, Bold, Italic et leurs combinaisons. Les polices variables peuvent exposer des axes tels que poids, largeur ou inclinaison.

Ne demandez pas une graisse qui n'existe pas sans vérifier le résultat. Le moteur peut choisir une autre face ou simuler une graisse, avec un résultat moins précis. Utilisez `fc-match -v` pour examiner les propriétés de la police retenue.

Pour un thème, définissez une hiérarchie simple : une famille d'interface, une famille de documents si nécessaire et une famille monospace. Limitez le nombre de familles afin de conserver une identité visuelle cohérente et de réduire les risques de repli inattendu.

## 7. Lisibilité et accessibilité

La typographie ne doit pas être évaluée uniquement sur une capture à taille fixe. Vérifiez :

- les petites tailles et les facteurs d'échelle ;
- les contrastes entre texte et fond ;
- les différences entre Regular, Medium et Bold ;
- les formes ambiguës comme I, l et 1 ;
- la lisibilité des chiffres ;
- les accents et signes diacritiques ;
- les langues écrites de droite à gauche ;
- les polices de remplacement ;
- les textes longs et les libellés qui se replient.

Ne réduisez pas la taille des textes pour faire tenir une interface trop dense. Corrigez d'abord les espacements et la disposition des composants.

## 8. Diagnostic pas à pas

**La police demandée n'est pas utilisée.** Lancez `fc-match 'Nom de famille'` et vérifiez l'orthographe du nom de famille.

**Les caractères accentués s'affichent avec une autre police.** La face sélectionnée ne contient peut-être pas tous les glyphes. Vérifiez les fontes de repli et la couverture du fichier.

**Le changement ne touche pas toutes les applications.** Certaines applications utilisent une police propre, une configuration embarquée ou un moteur différent. Inspectez leur toolkit avant de modifier Fontconfig.

**Le rendu paraît trop fin.** Vérifiez la graisse réellement sélectionnée avec `fc-match -v`, puis testez une face Medium ou Semibold réellement fournie par la famille.

**Une règle XML n'est pas chargée.** Vérifiez le nom et l'emplacement du fichier, sa syntaxe XML et la sortie de `fc-conflist`.

## 9. Exercice guidé

1. Installez une famille de polices sous licence compatible dans le dossier utilisateur.
2. Vérifiez sa présence avec `fc-list` et sa résolution avec `fc-match`.
3. Activez-la explicitement comme police d'interface avec GSettings.
4. Testez un texte contenant accents, chiffres, symboles et caractères d'une autre langue.
5. Créez un alias Fontconfig dans le dossier utilisateur.
6. Vérifiez le résultat et restaurez les paramètres GNOME initiaux.

## 10. Références

- [Guide utilisateur Fontconfig](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)
- [Documentation Fontconfig](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-devel/)
- [Pango — documentation](https://docs.gtk.org/Pango/)
- [FreeType — documentation](https://freetype.org/freetype2/docs/)
