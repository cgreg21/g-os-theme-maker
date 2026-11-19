# Applications Qt, Electron et environnements hybrides

GNOME est un environnement de bureau, pas un moteur graphique universel. Un thème GNOME Shell, GTK ou Libadwaita ne contrôle pas automatiquement les applications Qt, Electron, les applications qui dessinent leur interface elles-mêmes ou les programmes exécutés dans un conteneur.

Ce chapitre définit les frontières entre les moteurs et donne une méthode pour obtenir une apparence cohérente sans appliquer des règles qui ne peuvent pas fonctionner.

## 1. Identifier le moteur d'une application

Avant de chercher un sélecteur CSS, identifiez la technologie de l'interface.

Quelques indices :

- une application GTK expose généralement des widgets et des nœuds CSS à GTK Inspector ;
- une application Libadwaita utilise GTK 4 et des composants Adwaita ;
- une application Qt utilise les mécanismes de style Qt, les palettes et éventuellement Qt Quick ;
- une application Electron affiche souvent une interface web dans Chromium ;
- une application qui dessine directement avec OpenGL, Vulkan ou un moteur propriétaire peut ne pas exposer de widgets GTK ou Qt.

Le nom de l'application ou son apparence ne suffit pas pour identifier son moteur.

Sur un système Linux, les informations du paquet et les dépendances donnent des indices :

```sh
file /usr/bin/nom-application
ldd /usr/bin/nom-application | grep -Ei 'gtk|adwaita|Qt'
```

Ces commandes ne sont pas des preuves absolues : une application peut charger des bibliothèques dynamiquement, utiliser un lanceur ou être empaquetée différemment. Pour un paquet Flatpak, examinez également son manifeste et son runtime.

## 2. Pourquoi le CSS GTK ne modifie pas Qt

GTK et Qt possèdent leurs propres systèmes de widgets et de styles. Une règle comme :

```css
button {
  background-color: #3584e4;
  color: white;
}
```

est une règle GTK ou une règle d'un moteur CSS compatible, pas une règle Qt universelle.

Qt utilise notamment des styles natifs, des palettes et Qt Style Sheets. La syntaxe des feuilles Qt ressemble au CSS, mais les propriétés, les sélecteurs et les composants pris en charge sont spécifiques à Qt.

Pour personnaliser une application Qt, consultez la documentation de la version Qt utilisée et les options exposées par l'application. Ne copiez pas directement un fichier `gtk.css` dans le répertoire de configuration Qt.

## 3. Qt Widgets et Qt Quick

Deux familles doivent être distinguées.

### Qt Widgets

Qt Widgets utilise des widgets classiques. Le style peut provenir du style de plateforme, d'une palette ou d'une feuille Qt Style Sheets.

Les variables d'environnement et paramètres de style Qt dépendent de la version et de la distribution. Vérifiez les options disponibles avec les outils Qt installés plutôt que d'appliquer une variable au hasard.

### Qt Quick et QML

Qt Quick construit l'interface à partir d'éléments QML. Les composants peuvent être dessinés par le moteur Qt Quick Controls et utiliser un thème intégré à l'application.

Une feuille Qt Style Sheets destinée à Qt Widgets ne redessine pas automatiquement les composants QML. Il faut identifier le style Qt Quick Controls et les ressources de l'application.

## 4. Applications Electron

Electron utilise Chromium pour afficher une interface généralement construite avec HTML, CSS et JavaScript. Le CSS GTK ne s'applique pas à la page web embarquée.

Certaines applications Electron utilisent des décorations de fenêtre natives, d'autres dessinent leur propre barre de titre. Cette différence détermine quelle partie de la fenêtre relève de Mutter et quelle partie relève du CSS de l'application.

Pour personnaliser une application Electron :

1. vérifiez si elle expose un thème clair/sombre ;
2. vérifiez si elle propose une couleur d'accent ou des paramètres d'apparence ;
3. identifiez si la barre de titre est native ou dessinée par l'application ;
4. utilisez les mécanismes officiellement pris en charge par l'application ;
5. évitez de modifier les fichiers compilés ou les bundles JavaScript : une mise à jour peut écraser les changements.

Les feuilles de style personnalisées injectées par des extensions ou des outils tiers ne sont pas une fonction universelle d'Electron et peuvent présenter des risques de sécurité.

## 5. Décoration de fenêtre et contenu de l'application

Une fenêtre peut mélanger plusieurs propriétaires visuels :

- Mutter gère la fenêtre, sa position, sa taille et la composition ;
- une décoration côté serveur peut être fournie par le gestionnaire de fenêtres ;
- une décoration côté client est dessinée par l'application ;
- le contenu interne appartient au toolkit ou au moteur graphique de l'application.

Un thème GTK ne peut pas nécessairement changer une décoration côté serveur. Un thème Shell ne peut pas redessiner le contenu d'une application Electron. Une application peut également dessiner une barre de titre personnalisée qui ne suit pas le style GTK.

Pour chaque élément, identifiez son propriétaire avant de chercher une règle.

## 6. Cohérence visuelle entre moteurs

La cohérence ne signifie pas que tous les moteurs partagent le même CSS. Elle se construit à partir de décisions de design communes :

- palette de couleurs et niveaux de contraste ;
- rayon et densité visuelle ;
- hiérarchie typographique ;
- icônes et symboles ;
- espacements ;
- comportement clair/sombre ;
- conventions d'interaction.

Reproduisez ces choix dans chaque moteur avec ses propres outils. Pour Qt, utilisez les palettes et styles Qt appropriés. Pour Electron, utilisez les options de thème ou les feuilles CSS prévues par l'application. Pour GTK et Libadwaita, utilisez les mécanismes documentés dans les chapitres correspondants.

N'essayez pas de forcer une propriété inexistante dans un moteur : une règle ignorée ne crée pas de compatibilité.

## 7. Méthode de diagnostic par application

Pour chaque application qui ne suit pas le thème :

1. identifiez son moteur graphique ;
2. identifiez sa version et son mode d'installation ;
3. déterminez si la décoration est native, côté client ou côté serveur ;
4. vérifiez les paramètres d'apparence propres à l'application ;
5. cherchez une documentation officielle sur la personnalisation ;
6. vérifiez si l'application embarque ses ressources ;
7. testez les icônes et polices indépendamment du CSS ;
8. consignez les résultats et les limites.

Ne modifiez pas les fichiers d'une application installée dans un répertoire géré par le système ou par Flatpak. Les mises à jour peuvent remplacer ces fichiers et les modifications peuvent rendre l'application non prise en charge.

## 8. Construire une matrice de compatibilité honnête

Un thème peut annoncer plusieurs niveaux de prise en charge :

- **Natif GTK 3** : widgets GTK 3 testés avec le thème installé.
- **Natif GTK 4** : widgets GTK 4 testés.
- **Libadwaita** : applications et composants testés avec les versions indiquées.
- **Qt Widgets** : prise en charge par un style Qt distinct, si fourni.
- **Qt Quick** : prise en charge par un style Qt Quick Controls distinct, si fourni.
- **Electron** : prise en charge limitée aux options exposées par les applications testées.
- **Flatpak** : prise en charge vérifiée pour les runtimes et extensions indiqués.

Une application qui utilise une icône du thème ne doit pas être annoncée comme entièrement thémable. Décrivez précisément les éléments vérifiés : icônes, curseurs, polices, décorations ou contenu de fenêtre.

## 9. Exercice pratique

Choisissez trois applications : une GTK, une Qt et une Electron.

Pour chacune :

1. identifiez le moteur et la version ;
2. prenez une capture en mode clair ;
3. appliquez le thème GNOME ;
4. prenez une seconde capture ;
5. notez les changements réels ;
6. identifiez les éléments qui restent contrôlés par l'application ;
7. classez les résultats par ressource : CSS, icône, police, décoration et préférence sombre.

Vous obtenez ainsi une matrice de compatibilité fondée sur des observations, plutôt que sur des suppositions.

## 10. Références

- [Qt Documentation](https://doc.qt.io/)
- [Qt Style Sheets](https://doc.qt.io/qt-6/stylesheet.html)
- [Qt Quick Controls](https://doc.qt.io/qt-6/qtquickcontrols-index.html)
- [Electron Documentation](https://www.electronjs.org/docs/latest/)
- [GTK CSS overview](https://docs.gtk.org/gtk4/css-overview.html)
- [Mutter](https://gitlab.gnome.org/GNOME/mutter)
