# 4. Référence CSS et compatibilité

## 5.2 Glossaire des propriétés CSS et compatibilité

Ce glossaire indique les propriétés utiles à la création de thèmes et leur disponibilité selon le moteur. « Oui » signifie que la propriété est généralement reconnue ; « Partiel » signifie que sa syntaxe, son effet ou les widgets concernés varient ; « Non » signifie qu’il ne faut pas compter dessus pour cette cible.

- **Shell 51** : feuille CSS interprétée par St (GNOME Shell), pas par un navigateur.
- **GTK 3** et **GTK 4** : sous-ensembles CSS propres à GTK, différents du CSS Web.
- **Libadwaita** : utilise le moteur GTK 4 et ajoute des variables et conventions sémantiques. La compatibilité Libadwaita dépend donc aussi de la version de GTK/Libadwaita.

### Propriétés de couleur et de surface

- **Propriété** : `color` ; **Rôle** : Couleur du texte et des éléments de premier plan ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `background-color` ; **Rôle** : Couleur de fond ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `background` ; **Rôle** : Raccourci de fond ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `opacity` ; **Rôle** : Transparence de l’élément ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `box-shadow` ; **Rôle** : Ombre portée ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `text-shadow` ; **Rôle** : Ombre du texte ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `background-image` ; **Rôle** : Image ou dégradé de fond ; **Shell 51** : Partiel ; **GTK 3** : Partiel ; **GTK 4** : Partiel ; **Libadwaita** : Partiel

Pour les dégradés, vérifier la syntaxe du moteur : les fonctions CSS disponibles et les formes de dégradé ne sont pas identiques partout. GNOME Shell expose aussi des mécanismes de dégradé propres à St. Préférer une couleur unie si le même rendu doit fonctionner sur toutes les cibles.

### Bordures et contours

- **Propriété** : `border-color` ; **Rôle** : Couleur de bordure ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `border-width` ; **Rôle** : Épaisseur de bordure ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `border-style` ; **Rôle** : Style de bordure ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `border-radius` ; **Rôle** : Arrondi des angles ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `border` ; **Rôle** : Raccourci de bordure ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `outline-color` ; **Rôle** : Couleur du contour de focus ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `outline-style` ; **Rôle** : Style du contour de focus ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `outline-width` ; **Rôle** : Épaisseur du contour de focus ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui

Un contour de focus doit rester visible au clavier. Ne pas le supprimer sans fournir un indicateur de remplacement suffisamment contrasté.

### Dimensions, espacements et disposition

- **Propriété** : `width`, `height` ; **Rôle** : Dimensions ; **Shell 51** : Partiel ; **GTK 3** : Partiel ; **GTK 4** : Partiel ; **Libadwaita** : Partiel
- **Propriété** : `min-width`, `min-height` ; **Rôle** : Dimensions minimales ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `max-width`, `max-height` ; **Rôle** : Dimensions maximales ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `margin` et variantes ; **Rôle** : Marge extérieure ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `padding` et variantes ; **Rôle** : Espace intérieur ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `spacing` ; **Rôle** : Écart entre enfants dans certains conteneurs ; **Shell 51** : Partiel ; **GTK 3** : Partiel ; **GTK 4** : Partiel ; **Libadwaita** : Partiel

Les dimensions CSS ne remplacent pas les propriétés de mise en page du widget. GTK et St déterminent souvent la taille finale à partir de la mesure du contenu, des contraintes du conteneur et de l’échelle d’affichage.

### Typographie

- **Propriété** : `font-family` ; **Rôle** : Famille de police ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `font-size` ; **Rôle** : Taille du texte ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `font-weight` ; **Rôle** : Graisse ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `font-style` ; **Rôle** : Normal ou italique ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `line-height` ; **Rôle** : Hauteur de ligne ; **Shell 51** : Partiel ; **GTK 3** : Partiel ; **GTK 4** : Partiel ; **Libadwaita** : Partiel
- **Propriété** : `text-decoration` ; **Rôle** : Soulignement et décoration ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété** : `text-align` ; **Rôle** : Alignement du texte ; **Shell 51** : Partiel ; **GTK 3** : Partiel ; **GTK 4** : Partiel ; **Libadwaita** : Partiel

Les noms de polices doivent être disponibles sur le système. La taille effective dépend également du facteur d’échelle et des paramètres d’accessibilité.

### États et transitions

- **Propriété / pseudo-classe** : `:hover` ; **Rôle** : Pointeur au-dessus ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété / pseudo-classe** : `:focus` ; **Rôle** : Élément ayant le focus ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété / pseudo-classe** : `:active` ; **Rôle** : Élément pressé / actif ; **Shell 51** : Oui ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété / pseudo-classe** : `:checked` ; **Rôle** : Contrôle sélectionné ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété / pseudo-classe** : `:disabled` / `:insensitive` ; **Rôle** : Élément indisponible ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété / pseudo-classe** : `:selected` ; **Rôle** : Élément sélectionné ; **Shell 51** : Partiel ; **GTK 3** : Partiel ; **GTK 4** : Partiel ; **Libadwaita** : Partiel
- **Propriété / pseudo-classe** : `:backdrop` ; **Rôle** : Fenêtre inactive ; **Shell 51** : Partiel ; **GTK 3** : Oui ; **GTK 4** : Oui ; **Libadwaita** : Oui
- **Propriété / pseudo-classe** : `transition` ; **Rôle** : Transition animée de propriétés ; **Shell 51** : Non garanti ; **GTK 3** : Partiel ; **GTK 4** : Partiel ; **Libadwaita** : Partiel

Les pseudo-classes ne s’appliquent qu’aux nœuds qui exposent l’état correspondant. Dans GTK, l’état désactivé est fréquemment exprimé par `:disabled` ou `:insensitive` selon le moteur et le nœud ; vérifier l’arbre CSS réel du widget.

### Variables et directives CSS

- **Fonction** : Variables personnalisées `--nom` et `var()` ; **Shell 51** : Non garanti ; **GTK 3** : Non ; **GTK 4** : GTK 4.16+ ; **Libadwaita** : Selon GTK 4.16+
- **Fonction** : `@define-color` / `@color` ; **Shell 51** : Non ; **GTK 3** : Oui ; **GTK 4** : Ancien mécanisme, déprécié dans les versions récentes ; **Libadwaita** : À éviter
- **Fonction** : `:root` ; **Shell 51** : Non garanti ; **GTK 3** : Non ; **GTK 4** : GTK 4.16+ ; **Libadwaita** : Oui avec versions compatibles
- **Fonction** : `@media` ; **Shell 51** : Non garanti ; **GTK 3** : Non ; **GTK 4** : Non garanti ; **Libadwaita** : Non garanti
- **Fonction** : `@import` ; **Shell 51** : À éviter ; **GTK 3** : Oui, selon contexte ; **GTK 4** : Oui, selon contexte ; **Libadwaita** : Selon contexte

Les variables Libadwaita telles que `--window-bg-color`, `--view-bg-color`, `--headerbar-bg-color`, `--card-bg-color`, `--popover-bg-color`, `--accent-bg-color` et `--accent-fg-color` sont des variables sémantiques. Leur présence et leur valeur par défaut dépendent de la version Libadwaita. Ne pas les confondre avec une garantie que toutes les applications acceptent un CSS utilisateur.

### Propriétés à ne pas traiter comme universelles

Les propriétés de navigateur telles que `display: flex`, `display: grid`, `position: absolute`, `z-index`, `transform`, `filter`, `backdrop-filter`, `animation` et les règles de mise en page Web ne constituent pas une base portable pour GNOME Shell, GTK 3 ou GTK 4. Ne pas les proposer dans l’inspecteur comme propriétés communes.

### Règle de compatibilité pour l’éditeur

Chaque propriété affichée dans G-OS Theme Maker doit porter une cible explicite :

- **Commun** : disponible et vérifiée sur toutes les cibles sélectionnées.
- **Spécifique** : disponible seulement sur un moteur ou une version donnée.
- **Partiel** : prise en charge limitée ou dépendante du widget.
- **Non pris en charge** : ne pas exporter cette propriété pour la cible.

L’exporteur doit générer des feuilles adaptées à chaque moteur au lieu de copier aveuglément le même CSS dans tous les répertoires. Les tableaux ci-dessus sont un guide de conception ; valider les propriétés et sélecteurs avec les versions réelles de GTK et GNOME Shell ciblées avant de les déclarer comme testés.

Références techniques :
- [GNOME Shell 51 — sources SCSS du thème](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass)
- [GTK 3 — CSS Overview](https://gnome.pages.gitlab.gnome.org/gtk/gtk3/css-overview.html)
- [GTK 4 — CSS Overview](https://gnome.pages.gitlab.gnome.org/gtk/gtk4/css-overview.html)
- [GTK 4 — CSS Properties](https://gnome.pages.gitlab.gnome.org/gtk/gtk4/css-properties.html)
- [Libadwaita — CSS Variables](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/css-variables.html)

## 4.1 Sélecteurs GTK

Formes courantes : nœud (`button`), classe (`.suggested-action`), nom de widget (`#my-widget`), descendants (`headerbar button`), enfant direct (`notebook > header`), pseudo-classes et combinateurs. GTK ne prend pas en charge tous les sélecteurs Web ; ne pas supposer les sélecteurs d'attributs. Dans GTK, #nom désigne le nom du widget, pas un identifiant HTML.

## 4.2 États et pseudo-classes

`:hover`, `:focus`, `:active`, `:checked`, `:disabled`, `:insensitive`, `:indeterminate`, `:inconsistent`, `:selected`, `:backdrop`, `:dir(ltr)`, `:dir(rtl)`, `:drop(active)` doivent être vérifiés selon moteur et nœud. Une pseudo-classe valide syntaxiquement peut ne correspondre à aucun nœud.

## 4.3 Valeurs, unités et images

Les longueurs peuvent utiliser px, pt, em, ex, rem et unités physiques selon moteur. Les unités sont logiques et influencées par l'échelle. GTK supporte images et dégradés avec extensions propres ; les formats dépendent des chargeurs. Les propriétés `-gtk-*` sont spécifiques à GTK.

## 4.4 Exclusions du socle commun

Ne pas proposer comme universels : `display:flex`, `display:grid`, `position:absolute`, `z-index`, `transform`, `filter`, `backdrop-filter`, `@media`, sélecteurs d'attributs et animations Web. Une propriété reconnue par un moteur ne garantit pas son effet sur chaque nœud.

## 4.5 Métadonnées de compatibilité

Chaque propriété de l'inspecteur doit déclarer moteur, version minimale, type, widgets admissibles, états admissibles, exporteur, statut de validation et référence. Statuts : commun vérifié, spécifique, partiel, non pris en charge. Un parseur sans erreur ne prouve pas le rendu.
