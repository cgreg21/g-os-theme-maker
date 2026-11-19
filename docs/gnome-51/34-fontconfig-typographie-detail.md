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

Les formats courants sont TTF et OTF. Une famille peut être répartie dans plusieurs fichiers (Regular, Bold, Italic, etc.) ou être variable. Installez les faces nécessaires de la même famille : une seule face Regular ne garantit pas que les graisses et styles demandés seront disponibles.

## 3. Comprendre les familles génériques

Les familles génériques courantes sont :

- `sans-serif` pour le texte d'interface ;
- `serif` pour les textes à empattements ;
- `monospace` pour le code et les colonnes alignées ;
- `cursive` et `fantasy` lorsque l'application les utilise.

Une famille générique est une demande, pas un nom de fichier précis. Fontconfig la résout selon la configuration locale, les polices installées et la couverture linguistique.

Une famille peut exister sans contenir tous les glyphes nécessaires. Le système sélectionne alors des polices de repli pour les caractères absents. Testez des textes réels : accents français, apostrophes typographiques, symboles, grec, cyrillique, arabe et scripts asiatiques selon les langues ciblées.

Le repli peut se produire caractère par caractère. Un même paragraphe peut donc combiner plusieurs fichiers de polices, même si son style semble uniforme. C'est normal lorsque la famille principale ne couvre pas tous les caractères.

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

Avant de modifier une valeur, notez-la afin de pouvoir la restaurer. Par exemple :

```bash
gsettings get org.gnome.desktop.interface font-name
gsettings get org.gnome.desktop.interface document-font-name
gsettings get org.gnome.desktop.interface monospace-font-name
```

Conservez les sorties avant le test. Pour restaurer une valeur, réutilisez exactement la chaîne relevée avec `gsettings set`. Si la clé n'avait pas de valeur personnalisée, consultez le schéma et les valeurs par défaut de la distribution avant de la réinitialiser.

Un thème redistribuable doit expliquer comment activer une police, mais ne doit pas remplacer silencieusement les préférences personnelles. Le facteur `text-scaling-factor` agrandit le texte dans les applications qui respectent ce réglage ; il ne remplace pas un contrôle de mise en page ni les réglages d'accessibilité propres à chaque application.

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

Une règle d'alias ne crée pas une police et ne modifie pas les fichiers originaux. Elle indique à Fontconfig quelles familles préférer pour une demande donnée. La liste `prefer` exprime un ordre de préférence ; elle ne garantit pas que chaque famille dispose des glyphes nécessaires.

Les fichiers de configuration sont lus selon les règles d'inclusion et l'ordre définis par l'installation Fontconfig. Le préfixe numérique des fichiers `.conf` facilite l'organisation, mais ne doit pas être interprété comme une priorité universelle indépendante des inclusions du système. Évitez de recopier ou remplacer les fichiers de configuration fournis par la distribution.

Pour tester une règle, commencez par un alias ciblé dans le dossier utilisateur. Vérifiez le résultat avec `fc-match`, puis retirez uniquement ce fichier si le résultat est incorrect. Une erreur XML peut empêcher le chargement de la règle : contrôlez les journaux et la configuration effectivement chargée avant de multiplier les modifications.

## 6. Graisses, styles et polices variables

Les familles peuvent proposer des styles Regular, Medium, Semibold, Bold, Italic et leurs combinaisons. Les polices variables peuvent exposer des axes tels que poids, largeur ou inclinaison.

Ne demandez pas une graisse qui n'existe pas sans vérifier le résultat. Le moteur peut choisir une autre face ou simuler une graisse, avec un résultat moins précis. Utilisez :

```bash
fc-match -v 'MaPolice:style=Semibold'
fc-match -v 'MaPolice:weight=bold'
```

Les valeurs de poids utilisées dans les motifs Fontconfig ne sont pas des nombres CSS directement interchangeables. Pour un diagnostic, formulez une demande lisible puis examinez les propriétés de la face retournée.

Une police variable peut contenir plusieurs valeurs d'un axe dans un seul fichier. La disponibilité et l'utilisation effective des axes dépendent de la police, de Fontconfig, de FreeType et du toolkit. Ne supposez pas qu'une déclaration CSS `font-weight: 650` sera rendue de façon identique dans toutes les applications.

Pour un thème, définissez une hiérarchie simple : une famille d'interface, une famille de documents si nécessaire et une famille monospace. Limitez le nombre de familles afin de conserver une identité visuelle cohérente et de réduire les risques de repli inattendu.

## 7. Diagnostiquer la sélection d'une police

Les outils Fontconfig permettent de distinguer la demande de la police réellement retenue.

Afficher la meilleure correspondance :

```bash
fc-match 'Noto Sans'
```

Afficher plusieurs correspondances classées :

```bash
fc-match -s 'sans-serif:lang=fr'
```

Cette liste aide à comprendre les solutions de repli possibles. Elle ne constitue pas une garantie que chaque application utilisera exactement toutes les entrées dans cet ordre : le toolkit et la demande réelle peuvent ajouter leurs propres critères.

Inspecter les propriétés d'un fichier de police connu :

```bash
fc-query ~/.local/share/fonts/MaPolice-Regular.ttf
```

Examiner le motif de demande :

```bash
fc-pattern 'sans-serif:lang=fr:style=Regular'
```

- `fc-match` répond à la question « quelle police correspond à cette demande ? ».
- `fc-match -s` affiche une liste de correspondances ordonnées.
- `fc-query` interroge les propriétés d'un fichier de police.
- `fc-pattern` analyse une expression de motif Fontconfig.
- `fc-list` inventorie les polices connues de Fontconfig.
- `fc-conflist` affiche les fichiers de configuration chargés.

Ces commandes sont des outils de diagnostic. Leur disponibilité exacte dépend des paquets installés par la distribution. Si une commande manque, installez le paquet Fontconfig correspondant plutôt que de télécharger un binaire isolé.

## 8. CSS GTK et sélection Fontconfig

Le CSS GTK peut définir des propriétés typographiques sur un widget, par exemple :

```css
.label-emphasis {
  font-family: "Cantarell";
  font-size: 1rem;
  font-weight: 600;
}
```

Cette règle ne remplace pas Fontconfig. Elle exprime une demande au toolkit ; la résolution de la famille, la disponibilité des graisses et les glyphes de repli restent dépendants des polices installées et du moteur de texte.

Ne confondez pas les unités CSS avec les tailles affichées dans les préférences GNOME. Les unités, facteurs d'échelle et métriques peuvent varier selon le toolkit et l'environnement. Évitez de figer une taille en pixels pour tous les écrans : vérifiez la lisibilité à plusieurs facteurs d'échelle et densités.

GTK 3, GTK 4, libadwaita et GNOME Shell n'utilisent pas nécessairement le même moteur CSS ni les mêmes conventions de style. Une règle typographique validée dans une application GTK ne prouve pas qu'elle fonctionnera dans le thème de GNOME Shell.

## 9. Lisibilité et accessibilité

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

Ne réduisez pas la taille des textes pour faire tenir une interface trop dense. Corrigez d'abord les espacements et la disposition des composants. Vérifiez également les états désactivés, les infobulles, les menus, les notifications et les champs de saisie : ces zones utilisent parfois des styles différents.

## 10. Diagnostic pas à pas

**La police demandée n'est pas utilisée.** Lancez `fc-match 'Nom de famille'` et vérifiez l'orthographe du nom de famille, puis inspectez la liste avec `fc-list`.

**Les caractères accentués s'affichent avec une autre police.** La face sélectionnée ne contient peut-être pas tous les glyphes. Vérifiez les fontes de repli avec `fc-match -s 'Nom:lang=fr'` et inspectez la couverture du fichier avec `fc-query`.

**Le changement ne touche pas toutes les applications.** Certaines applications utilisent une police propre, une configuration embarquée ou un moteur différent. Inspectez leur toolkit avant de modifier Fontconfig.

**Le rendu paraît trop fin.** Vérifiez la graisse réellement sélectionnée avec `fc-match -v`, puis testez une face Medium ou Semibold réellement fournie par la famille.

**Une règle XML n'est pas chargée.** Vérifiez le nom et l'emplacement du fichier, sa syntaxe XML et la sortie de `fc-conflist`. Revenez temporairement à la configuration précédente en retirant uniquement le fichier utilisateur ajouté.

**La police installée n'apparaît pas.** Confirmez que le fichier est lisible, que son format est pris en charge, puis reconstruisez le cache du dossier. Fermez et relancez l'application de test si elle conserve les polices déjà découvertes en mémoire.

**Le texte change après une mise à jour.** Vérifiez les versions de la police, les règles Fontconfig de la distribution et les paramètres GNOME. Un changement de paquet peut modifier les correspondances sans que le thème CSS ait changé.

## 11. Exercice guidé

1. Installez une famille de polices sous licence compatible dans le dossier utilisateur.
2. Vérifiez sa présence avec `fc-list` et sa résolution avec `fc-match`.
3. Inspectez le fichier avec `fc-query` et comparez plusieurs correspondances avec `fc-match -s`.
4. Activez-la explicitement comme police d'interface avec GSettings, après avoir sauvegardé la valeur initiale.
5. Testez un texte contenant accents, chiffres, symboles et caractères d'une autre langue.
6. Créez un alias Fontconfig dans le dossier utilisateur.
7. Vérifiez le résultat et restaurez les paramètres GNOME initiaux.
8. Supprimez l'alias de test et vérifiez que la résolution revient à son état précédent.

## 12. Références

- [Guide utilisateur Fontconfig](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)
- [Documentation Fontconfig](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-devel/)
- [Pango — documentation](https://docs.gtk.org/Pango/)
- [FreeType — documentation](https://freetype.org/freetype2/docs/)
- [GTK 4 — CSS overview](https://docs.gtk.org/gtk4/css-overview.html)
