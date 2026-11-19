# 41. Cible de versions et compatibilité GNOME 51

Ce chapitre fixe la référence de version du manuel. Il explique comment identifier les bibliothèques réellement utilisées, comment interpréter les numéros de version et comment annoncer une compatibilité sans confondre une version de GNOME avec les versions de GTK et Libadwaita.

## 1. Référence amont GNOME 51

Les notes officielles de GNOME 51 indiquent les versions suivantes pour la plateforme de développement :

- GNOME Shell : branche amont 51.0 pour les sources du thème Shell décrites dans ce manuel ;
- GTK 4 : génération 4.23 ;
- Libadwaita : génération 1.10 ;
- GTK 3 : branche 3.24 pour la compatibilité avec les applications historiques.

Libadwaita 1.10 requiert GTK 4.23.1. Il faut donc distinguer la mention générale GTK 4.23 dans les notes GNOME et la version minimale précise exigée par Libadwaita 1.10.

Cette référence décrit la plateforme amont GNOME 51. Une distribution peut fournir des correctifs, des versions de maintenance ou des options de compilation différentes. La version installée sur la machine reste celle à tester.

## 2. Identifier les versions présentes

Commencez par la session :

~~~sh
gnome-shell --version
~~~

Puis interrogez chaque bibliothèque séparément :

~~~sh
pkg-config --modversion gtk+-3.0
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
~~~

Une commande peut échouer si le paquet de développement n'est pas installé. Cela ne prouve pas que la bibliothèque d'exécution est absente : les fichiers pkg-config sont généralement fournis par les paquets de développement.

Pour examiner les applications Flatpak :

~~~sh
flatpak list --app
flatpak info ID_DE_L_APPLICATION
~~~

Une application Flatpak peut utiliser un runtime différent des bibliothèques installées sur l'hôte. Ne déduisez pas sa version GTK de la seule version du système.

## 3. Version GNOME, version de bibliothèque et version de thème

Ces numéros ne sont pas interchangeables.

**Version GNOME** désigne la publication coordonnée du bureau et de ses composants.

**Version GNOME Shell** identifie le code du Shell. Les sélecteurs privés du thème sont liés à cette version précise.

**Version GTK** détermine les widgets disponibles, les propriétés CSS, les sélecteurs et les fonctionnalités du moteur.

**Version Libadwaita** détermine les composants Adwaita, leurs classes, les variables CSS et les mécanismes de style de l'application.

**Version d'une application** peut être indépendante de la version GNOME installée. Une application mise à jour ou distribuée en Flatpak peut embarquer ou utiliser une autre génération de bibliothèque.

Une compatibilité sérieuse doit nommer chaque cible. Écrire simplement « compatible GNOME 51 » est insuffisant si le thème annonce aussi GTK et Libadwaita.

## 4. Évolutions CSS à prendre en compte

Les moteurs n'ajoutent pas leurs fonctionnalités au même rythme.

### GTK 3.24

GTK 3.24 possède son propre moteur CSS. Il documente notamment les nœuds CSS, les classes, les pseudo-classes, les propriétés prises en charge, les couleurs symboliques GTK et les transitions. Il ne faut pas lui appliquer automatiquement les fonctionnalités modernes de GTK 4.

Les variables personnalisées CSS utilisant --nom et var() ne font pas partie de la base GTK 3.24. Les feuilles GTK 3 historiques utilisent notamment @define-color pour les couleurs symboliques.

### GTK 4

GTK 4 possède un moteur CSS distinct. Les variables personnalisées CSS et les règles :root sont prises en charge depuis GTK 4.16. Les versions antérieures, par exemple GTK 4.14, ne les prennent pas en charge.

GTK 4.20 a ajouté la prise en charge de requêtes de média pour détecter notamment les préférences de schéma de couleurs et de contraste. Cette capacité est présente dans la génération GTK 4.23 de GNOME 51.

GTK 4.23 ajoute également la propriété font-width. La propriété font-stretch reste un raccourci ; la prise en charge de ces réglages de largeur de police dépend aussi de Pango 1.58 ou plus récent.

Ne confondez pas ces fonctionnalités CSS avec les propriétés de mise en page d'un navigateur. GTK conserve son propre modèle de widgets et de mesure.

### Libadwaita 1.10

Libadwaita 1.10 s'appuie sur GTK 4.23. Elle fournit les conventions de style Adwaita, des variables de couleur, des classes de style et des mécanismes pour les apparences claire, sombre et contraste élevé.

Les applications Libadwaita standard gèrent automatiquement une partie de ces variantes. Les styles personnalisés et le dessin applicatif doivent être vérifiés dans chaque apparence.

Les fichiers de style conditionnels chargés par AdwApplication sont des ressources propres à l'application. Ils ne constituent pas un mécanisme universel pour injecter un thème global dans toutes les applications Libadwaita.

## 5. Vérifier les propriétés plutôt que supposer

Pour chaque propriété CSS que vous documentez :

1. Identifiez le moteur : St, GTK 3, GTK 4 ou Libadwaita.
2. Identifiez la version minimale qui fournit la propriété.
3. Consultez la référence officielle correspondant à ce moteur.
4. Vérifiez la syntaxe et les valeurs admises.
5. Vérifiez si la propriété agit sur le type de nœud visé.
6. Testez dans une application ou session de la version cible.
7. Consignez la version exacte et le résultat.

Un parseur peut accepter une propriété sans produire de changement visible sur un widget donné. Inversement, une règle peut fonctionner dans une application parce qu'elle fournit une classe ou un provider privé.

## 6. Vérifier les sélecteurs GNOME Shell

Les sélecteurs du Shell doivent être comparés aux sources de la branche 51.0, et non à la documentation d'une branche de développement ultérieure.

~~~sh
git clone --branch 51.0 --depth 1 \
  https://github.com/GNOME/gnome-shell.git
cd gnome-shell
grep -R -nE 'panel-button|quick-settings|search-entry' \
  data/theme/gnome-shell-sass/widgets
~~~

Cette commande est un exemple de recherche. Adaptez les termes à l'élément inspecté. La présence d'un nom dans un fichier SCSS ne garantit pas qu'il soit présent dans toutes les situations de l'interface : vérifiez aussi le code qui crée l'acteur et ajoute ses classes.

Ne copiez pas un sélecteur de GNOME 52 ou d'une version plus récente dans un thème annoncé compatible GNOME 51 sans le vérifier.

## 7. Déclarer une compatibilité honnête

Un projet de thème devrait documenter séparément :

- la version de GNOME Shell testée ;
- les versions GTK 3 et GTK 4 testées ;
- la version Libadwaita testée ;
- les environnements de session utilisés ;
- les applications testées ;
- les composants couverts ;
- les composants non couverts ;
- les limitations connues.

Utilisez des formulations précises :

- **Testé** : le composant a été essayé sur la version indiquée.
- **Compatible selon la documentation** : la syntaxe est documentée, mais le rendu n'a pas été testé sur cette configuration.
- **Partiel** : certaines variantes ou certains états ne sont pas couverts.
- **Non pris en charge** : le moteur ou l'application ne fournit pas de mécanisme permettant le résultat annoncé.
- **Inconnu** : aucune validation suffisante n'a été effectuée.

Ne transformez pas « le CSS se charge » en « le thème est compatible ».

## 8. Matrice de validation pratique

Pour chaque version déclarée, exécutez au minimum :

- une session GNOME Shell réelle ;
- une application GTK 3 représentative ;
- une application GTK 4 représentative ;
- une application Libadwaita ;
- une application Flatpak si cette cible est annoncée ;
- une vérification du mode clair ;
- une vérification du mode sombre ;
- une vérification du contraste élevé ;
- une vérification du focus clavier ;
- une vérification avec un facteur d'échelle différent de 100 %.

Ajoutez une capture locale et les versions exactes dans le rapport de test. Si une version n'est pas disponible, marquez le résultat comme non testé au lieu de l'inférer.

## 9. Références officielles

- [GNOME 51 — notes de version](https://release.gnome.org/51/)
- [GNOME 51 — nouveautés développeurs](https://release.gnome.org/51/developers/)
- [GNOME Shell 51.0 — sources](https://github.com/GNOME/gnome-shell/tree/51.0)
- [GTK 3.24 — CSS Overview](https://docs.gtk.org/gtk3/css-overview.html)
- [GTK 3.24 — CSS Properties](https://docs.gtk.org/gtk3/css-properties.html)
- [GTK 4 — CSS Overview](https://docs.gtk.org/gtk4/css-overview.html)
- [GTK 4 — CSS Properties](https://docs.gtk.org/gtk4/css-properties.html)
- [Libadwaita 1.10 — Styles and Appearance](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)
- [Libadwaita — CSS Variables](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/css-variables.html)
