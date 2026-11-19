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

Le nom de l'application ou son apparence ne suffit pas pour identifier son moteur. Une application peut également mélanger plusieurs technologies : interface GTK et rendu OpenGL, fenêtre Qt et contenu web, ou décoration native et barre de titre dessinée par l'application.

Sur un système Linux, les informations du paquet et les dépendances donnent des indices :

```sh
file /usr/bin/nom-application
ldd /usr/bin/nom-application | grep -Ei 'gtk|adwaita|Qt'
```

Ces commandes ne sont pas des preuves absolues : une application peut charger des bibliothèques dynamiquement, utiliser un lanceur ou être empaquetée différemment. Pour un paquet Flatpak, examinez également son manifeste et son runtime. Pour une application AppImage, inspectez son contenu et ses bibliothèques embarquées sans supposer qu'elle utilise celles du système.

## 2. Pourquoi le CSS GTK ne modifie pas Qt

GTK et Qt possèdent leurs propres systèmes de widgets et de styles. Une règle comme :

```css
button {
  background-color: #3584e4;
  color: white;
}
```

est une règle GTK ou une règle d'un moteur CSS compatible, pas une règle Qt universelle.

Qt utilise notamment des styles natifs, des palettes et Qt Style Sheets. La syntaxe des feuilles Qt ressemble au CSS, mais les propriétés, les sélecteurs et les composants pris en charge sont spécifiques à Qt. Une propriété CSS valide pour GTK peut être ignorée ou interprétée différemment dans Qt.

Pour personnaliser une application Qt, consultez la documentation de la version Qt utilisée et les options exposées par l'application. Ne copiez pas directement un fichier `gtk.css` dans le répertoire de configuration Qt.

## 3. Qt Widgets : styles, palettes et feuilles Qt

Qt Widgets utilise des widgets classiques. Le style peut provenir du style de plateforme, d'une palette ou d'une feuille Qt Style Sheets.

Une feuille Qt Style Sheets doit cibler les classes et propriétés réellement prises en charge. Exemple conceptuel pour une application dont on contrôle le code :

```css
QPushButton {
    padding: 6px 12px;
    border: 1px solid palette(mid);
    border-radius: 6px;
}

QPushButton:hover {
    background-color: palette(midlight);
}
```

Cet exemple appartient à Qt Style Sheets, pas au CSS GTK. Il ne faut pas le déposer dans le dossier d'un thème GTK.

La palette Qt fournit des rôles de couleurs comme le fond, le texte, les couleurs de base et les états désactivés. Un style peut interpréter ces rôles différemment. Une feuille de style qui fixe toutes les couleurs en valeurs absolues peut neutraliser la palette et rendre les états clair/sombre incohérents.

Les styles de plateforme et les plugins QPA influencent également l'intégration. Les variables d'environnement et paramètres de style Qt dépendent de la version et de la distribution. Vérifiez les options disponibles avec les outils Qt installés plutôt que d'appliquer une variable au hasard. Ne définissez pas globalement une variable Qt pour toutes les applications sans avoir vérifié ses effets sur les programmes qui utilisent des versions différentes de Qt.

## 4. Qt Quick et QML

Qt Quick construit l'interface à partir d'éléments QML. Les composants peuvent être dessinés par le moteur Qt Quick Controls et utiliser un thème intégré à l'application.

Une feuille Qt Style Sheets destinée à Qt Widgets ne redessine pas automatiquement les composants QML. Il faut identifier le style Qt Quick Controls et les ressources de l'application.

Les styles Qt Quick Controls sont sélectionnés selon les mécanismes de Qt Quick et peuvent être fournis par Qt, par la distribution ou par l'application. Les versions de Qt et les modules installés déterminent les styles disponibles. Ne supposez pas que le style d'une application Qt Widgets est aussi utilisé par son équivalent Qt Quick.

Si vous développez l'application, centralisez les couleurs, espacements et dimensions dans des composants ou fichiers de thème QML. Si vous ne contrôlez pas son code, utilisez uniquement les options officiellement exposées par l'application.

## 5. Applications Electron et Chromium

Electron utilise Chromium pour afficher une interface généralement construite avec HTML, CSS et JavaScript. Le CSS GTK ne s'applique pas à la page web embarquée.

Certaines applications Electron utilisent des décorations de fenêtre natives, d'autres dessinent leur propre barre de titre. Cette différence détermine quelle partie de la fenêtre relève de Mutter et quelle partie relève du CSS de l'application.

Pour personnaliser une application Electron :

1. vérifiez si elle expose un thème clair/sombre ;
2. vérifiez si elle propose une couleur d'accent ou des paramètres d'apparence ;
3. identifiez si la barre de titre est native ou dessinée par l'application ;
4. utilisez les mécanismes officiellement pris en charge par l'application ;
5. évitez de modifier les fichiers compilés ou les bundles JavaScript : une mise à jour peut écraser les changements.

Les applications web peuvent utiliser des variables CSS, des feuilles de style propres et des composants qui ignorent les préférences du système. Certaines interprètent la préférence du navigateur via `prefers-color-scheme`, mais cela dépend du code de l'application et de sa configuration Electron.

Les feuilles de style personnalisées injectées par des extensions ou des outils tiers ne sont pas une fonction universelle d'Electron et peuvent présenter des risques de sécurité. Ne désactivez pas les protections Chromium et ne lancez pas une application avec des options de débogage non maîtrisées simplement pour forcer un thème.

## 6. Décoration de fenêtre et contenu de l'application

Une fenêtre peut mélanger plusieurs propriétaires visuels :

- Mutter gère la fenêtre, sa position, sa taille et la composition ;
- une décoration côté serveur peut être fournie par le gestionnaire de fenêtres ;
- une décoration côté client est dessinée par l'application ;
- le contenu interne appartient au toolkit ou au moteur graphique de l'application.

Un thème GTK ne peut pas nécessairement changer une décoration côté serveur. Un thème Shell ne peut pas redessiner le contenu d'une application Electron. Une application peut également dessiner une barre de titre personnalisée qui ne suit pas le style GTK.

Sur Wayland, la décoration et les demandes de décoration dépendent des protocoles et des choix de l'application et du compositeur. Sous X11 ou Xwayland, les mécanismes de décoration peuvent être différents. Pour comprendre ce qui est modifiable, consultez aussi le chapitre sur CSD, SSD, Wayland et X11.

Pour chaque élément, identifiez son propriétaire avant de chercher une règle. Un bouton situé dans une barre de titre dessinée par l'application ne relève pas nécessairement du même moteur que le contenu de la fenêtre.

## 7. Cohérence visuelle entre moteurs

La cohérence ne signifie pas que tous les moteurs partagent le même CSS. Elle se construit à partir de décisions de design communes :

- palette de couleurs et niveaux de contraste ;
- rayon et densité visuelle ;
- hiérarchie typographique ;
- icônes et symboles ;
- espacements ;
- comportement clair/sombre ;
- conventions d'interaction.

Reproduisez ces choix dans chaque moteur avec ses propres outils. Pour Qt, utilisez les palettes et styles Qt appropriés. Pour Electron, utilisez les options de thème ou les feuilles CSS prévues par l'application. Pour GTK et Libadwaita, utilisez les mécanismes documentés dans les chapitres correspondants.

Conservez une spécification visuelle indépendante des technologies : noms des couleurs, échelle d'espacement, tailles typographiques, rayons et états interactifs. Déclinez ensuite cette spécification en CSS GTK, paramètres Qt et variables CSS web. Cela évite de considérer un fichier de style unique comme une solution multi-moteur.

N'essayez pas de forcer une propriété inexistante dans un moteur : une règle ignorée ne crée pas de compatibilité.

## 8. Icônes, polices et curseurs entre moteurs

Les ressources partagées peuvent donner une cohérence partielle, mais leur découverte dépend de chaque application.

Les applications GTK utilisent les mécanismes d'icônes et de polices du toolkit. Les applications Qt peuvent utiliser leur propre thème d'icônes, les chemins de ressources Qt et les polices résolues par le système. Les applications Electron peuvent embarquer des icônes et polices dans leurs ressources web.

Vérifiez chaque catégorie indépendamment :

- **Icônes** : nom Freedesktop demandé, thème actif, chemins accessibles et solution de repli.
- **Polices** : famille réellement résolue, fichier accessible, glyphes présents et graisse disponible.
- **Curseurs** : thème sélectionné, prise en charge par la pile graphique et contexte d'exécution.
- **Images et logos** : ressources parfois embarquées et non remplaçables par le thème du bureau.

Le fait qu'une application reprenne les icônes système ne signifie pas que ses boutons, panneaux ou dialogues sont thémables par GTK.

## 9. Applications en conteneur et variables d'environnement

Une application peut utiliser Qt ou Electron tout en étant distribuée dans Flatpak. Il faut alors traiter deux questions séparément : le moteur graphique et l'accès aux ressources du bac à sable.

Un thème Qt ne devient pas accessible parce que l'application est Flatpak ; une police hôte ne devient pas automatiquement visible non plus. Utilisez les mécanismes d'extension et les permissions minimales décrits dans le chapitre Flatpak.

Les variables d'environnement peuvent influencer le choix du moteur, du plugin de plateforme ou du style, mais elles sont propres à chaque technologie et parfois à chaque version. Avant d'en définir une :

1. consultez la documentation officielle de la version installée ;
2. testez-la sur une seule application ;
3. relevez la valeur précédente ;
4. vérifiez les effets sur Wayland et X11 si les deux sont utilisés ;
5. retirez la surcharge après le test.

Évitez les exports permanents dans `~/.profile` ou `/etc/environment` pour corriger une seule application. Une variable globale peut affecter des logiciels qui ne partagent ni la même version ni le même moteur.

## 10. Méthode de diagnostic par application

Pour chaque application qui ne suit pas le thème :

1. identifiez son moteur graphique ;
2. identifiez sa version et son mode d'installation ;
3. déterminez si la décoration est native, côté client ou côté serveur ;
4. vérifiez les paramètres d'apparence propres à l'application ;
5. cherchez une documentation officielle sur la personnalisation ;
6. vérifiez si l'application embarque ses ressources ;
7. testez les icônes et polices indépendamment du CSS ;
8. identifiez les variables d'environnement et surcharges spécifiques ;
9. consignez les résultats et les limites.

Ne modifiez pas les fichiers d'une application installée dans un répertoire géré par le système ou par Flatpak. Les mises à jour peuvent remplacer ces fichiers et les modifications peuvent rendre l'application non prise en charge.

## 11. Construire une matrice de compatibilité honnête

Un thème peut annoncer plusieurs niveaux de prise en charge :

- **Natif GTK 3** : widgets GTK 3 testés avec le thème installé.
- **Natif GTK 4** : widgets GTK 4 testés.
- **Libadwaita** : applications et composants testés avec les versions indiquées.
- **Qt Widgets** : prise en charge par un style Qt distinct, si fourni.
- **Qt Quick** : prise en charge par un style Qt Quick Controls distinct, si fourni.
- **Electron** : prise en charge limitée aux options exposées par les applications testées.
- **Flatpak** : prise en charge vérifiée pour les runtimes et extensions indiqués.

Une application qui utilise une icône du thème ne doit pas être annoncée comme entièrement thémable. Décrivez précisément les éléments vérifiés : icônes, curseurs, polices, décorations ou contenu de fenêtre.

Pour chaque application testée, consignez au minimum son nom, sa version, son moteur, son mode d'installation, la session graphique et les éléments réellement modifiés. Une compatibilité annoncée doit correspondre à des essais reproductibles.

## 12. Exercice pratique

Choisissez trois applications : une GTK, une Qt et une Electron.

Pour chacune :

1. identifiez le moteur et la version ;
2. prenez une capture en mode clair ;
3. appliquez le thème GNOME ;
4. prenez une seconde capture ;
5. notez les changements réels ;
6. identifiez les éléments qui restent contrôlés par l'application ;
7. classez les résultats par ressource : CSS, icône, police, décoration et préférence sombre ;
8. relevez les éventuelles variables d'environnement et options de thème.

Vous obtenez ainsi une matrice de compatibilité fondée sur des observations, plutôt que sur des suppositions.

## 13. Références

- [Qt Documentation](https://doc.qt.io/)
- [Qt Style Sheets](https://doc.qt.io/qt-6/stylesheet.html)
- [Qt Quick Controls](https://doc.qt.io/qt-6/qtquickcontrols-index.html)
- [Electron Documentation](https://www.electronjs.org/docs/latest/)
- [Electron Native Theme](https://www.electronjs.org/docs/latest/api/native-theme)
- [GTK CSS overview](https://docs.gtk.org/gtk4/css-overview.html)
- [Mutter](https://gitlab.gnome.org/GNOME/mutter)
