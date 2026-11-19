# 4. Référence CSS et compatibilité

## 5.2 Glossaire des propriétés CSS et compatibilité

Ce glossaire indique les propriétés utiles à la création de thèmes et leur disponibilité selon le moteur. « Oui » signifie que la propriété est généralement reconnue ; « Partiel » signifie que sa syntaxe, son effet ou les widgets concernés varient ; « Non » signifie qu’il ne faut pas compter dessus pour cette cible.

- **Shell 51** : feuille CSS interprétée par St (GNOME Shell), pas par un navigateur.
- **GTK 3** et **GTK 4** : sous-ensembles CSS propres à GTK, différents du CSS Web.
- **Libadwaita** : utilise le moteur GTK 4 et ajoute des variables et conventions sémantiques. La compatibilité Libadwaita dépend donc aussi de la version de GTK/Libadwaita.

### Propriétés de couleur et de surface

| Propriété | Rôle | Shell 51 | GTK 3 | GTK 4 | Libadwaita |
|---|---|:---:|:---:|:---:|:---:|
| `color` | Couleur du texte et des éléments de premier plan | Oui | Oui | Oui | Oui |
| `background-color` | Couleur de fond | Oui | Oui | Oui | Oui |
| `background` | Raccourci de fond | Partiel | Oui | Oui | Oui |
| `opacity` | Transparence de l’élément | Oui | Oui | Oui | Oui |
| `box-shadow` | Ombre portée | Partiel | Oui | Oui | Oui |
| `text-shadow` | Ombre du texte | Partiel | Oui | Oui | Oui |
| `background-image` | Image ou dégradé de fond | Partiel | Partiel | Partiel | Partiel |

Pour les dégradés, vérifier la syntaxe du moteur : les fonctions CSS disponibles et les formes de dégradé ne sont pas identiques partout. GNOME Shell expose aussi des mécanismes de dégradé propres à St. Préférer une couleur unie si le même rendu doit fonctionner sur toutes les cibles.

### Bordures et contours

| Propriété | Rôle | Shell 51 | GTK 3 | GTK 4 | Libadwaita |
|---|---|:---:|:---:|:---:|:---:|
| `border-color` | Couleur de bordure | Oui | Oui | Oui | Oui |
| `border-width` | Épaisseur de bordure | Oui | Oui | Oui | Oui |
| `border-style` | Style de bordure | Partiel | Oui | Oui | Oui |
| `border-radius` | Arrondi des angles | Oui | Oui | Oui | Oui |
| `border` | Raccourci de bordure | Partiel | Oui | Oui | Oui |
| `outline-color` | Couleur du contour de focus | Partiel | Oui | Oui | Oui |
| `outline-style` | Style du contour de focus | Partiel | Oui | Oui | Oui |
| `outline-width` | Épaisseur du contour de focus | Partiel | Oui | Oui | Oui |

Un contour de focus doit rester visible au clavier. Ne pas le supprimer sans fournir un indicateur de remplacement suffisamment contrasté.

### Dimensions, espacements et disposition

| Propriété | Rôle | Shell 51 | GTK 3 | GTK 4 | Libadwaita |
|---|---|:---:|:---:|:---:|:---:|
| `width`, `height` | Dimensions | Partiel | Partiel | Partiel | Partiel |
| `min-width`, `min-height` | Dimensions minimales | Oui | Oui | Oui | Oui |
| `max-width`, `max-height` | Dimensions maximales | Partiel | Oui | Oui | Oui |
| `margin` et variantes | Marge extérieure | Oui | Oui | Oui | Oui |
| `padding` et variantes | Espace intérieur | Oui | Oui | Oui | Oui |
| `spacing` | Écart entre enfants dans certains conteneurs | Partiel | Partiel | Partiel | Partiel |

Les dimensions CSS ne remplacent pas les propriétés de mise en page du widget. GTK et St déterminent souvent la taille finale à partir de la mesure du contenu, des contraintes du conteneur et de l’échelle d’affichage.

### Typographie

| Propriété | Rôle | Shell 51 | GTK 3 | GTK 4 | Libadwaita |
|---|---|:---:|:---:|:---:|:---:|
| `font-family` | Famille de police | Oui | Oui | Oui | Oui |
| `font-size` | Taille du texte | Oui | Oui | Oui | Oui |
| `font-weight` | Graisse | Oui | Oui | Oui | Oui |
| `font-style` | Normal ou italique | Oui | Oui | Oui | Oui |
| `line-height` | Hauteur de ligne | Partiel | Partiel | Partiel | Partiel |
| `text-decoration` | Soulignement et décoration | Partiel | Oui | Oui | Oui |
| `text-align` | Alignement du texte | Partiel | Partiel | Partiel | Partiel |

Les noms de polices doivent être disponibles sur le système. La taille effective dépend également du facteur d’échelle et des paramètres d’accessibilité.

### États et transitions

| Propriété / pseudo-classe | Rôle | Shell 51 | GTK 3 | GTK 4 | Libadwaita |
|---|---|:---:|:---:|:---:|:---:|
| `:hover` | Pointeur au-dessus | Oui | Oui | Oui | Oui |
| `:focus` | Élément ayant le focus | Oui | Oui | Oui | Oui |
| `:active` | Élément pressé / actif | Oui | Oui | Oui | Oui |
| `:checked` | Contrôle sélectionné | Partiel | Oui | Oui | Oui |
| `:disabled` / `:insensitive` | Élément indisponible | Partiel | Oui | Oui | Oui |
| `:selected` | Élément sélectionné | Partiel | Partiel | Partiel | Partiel |
| `:backdrop` | Fenêtre inactive | Partiel | Oui | Oui | Oui |
| `transition` | Transition animée de propriétés | Non garanti | Partiel | Partiel | Partiel |

Les pseudo-classes ne s’appliquent qu’aux nœuds qui exposent l’état correspondant. Dans GTK, l’état désactivé est fréquemment exprimé par `:disabled` ou `:insensitive` selon le moteur et le nœud ; vérifier l’arbre CSS réel du widget.

### Variables et directives CSS

| Fonction | Shell 51 | GTK 3 | GTK 4 | Libadwaita |
|---|:---:|:---:|:---:|:---:|
| Variables personnalisées `--nom` et `var()` | Non garanti | Non | GTK 4.16+ | Selon GTK 4.16+ |
| `@define-color` / `@color` | Non | Oui | Ancien mécanisme, déprécié dans les versions récentes | À éviter |
| `:root` | Non garanti | Non | GTK 4.16+ | Oui avec versions compatibles |
| `@media` | Non garanti | Non | Non garanti | Non garanti |
| `@import` | À éviter | Oui, selon contexte | Oui, selon contexte | Selon contexte |

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
