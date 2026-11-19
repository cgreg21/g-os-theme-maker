# 1. Architecture et périmètre


Ce guide est le catalogue de référence de G-OS Theme Maker. Il décrit les familles d’éléments visuels qu’un thème peut couvrir, les moteurs qui les dessinent, les états à prévoir et les limites de compatibilité.

La référence GNOME Shell est **GNOME Shell 51.0** (sources amont). Les applications sont séparées selon **GTK 3**, **GTK 4** et **Libadwaita**. Ce catalogue distingue les éléments réellement stylables des éléments dont l’apparence est contrôlée par le système, l’application ou une extension.

> « Couvrir tous les éléments » signifie couvrir toutes les familles de composants d’interface et leurs états, et fournir un inventaire vérifiable des composants GNOME Shell 51. Les applications peuvent créer leurs propres widgets : aucun thème global ne peut garantir le style de chaque interface tierce.

## 1. Périmètre : les moteurs de rendu

Un bureau GNOME n’a pas un moteur de thème unique. Il faut produire et tester plusieurs feuilles indépendantes.

| Cible | Technologie | Ressource principale | Éléments couverts |
|---|---|---|---|
| GNOME Shell 51 | St / Clutter | `gnome-shell.css` | panneau, vue Activités, dash, menus système, notifications, verrouillage, OSD |
| GTK 3.24 | GTK CSS | `gtk-3.0/gtk.css` | widgets GTK 3 et anciennes applications |
| GTK 4 | GTK CSS | `gtk-4.0/gtk.css` | widgets GTK 4 |
| Libadwaita | GTK 4 + styles Adwaita | CSS de l’application / CSS utilisateur | fenêtres et composants Adwaita |
| Icônes | Freedesktop Icon Theme | `index.theme` + ressources | applications, actions, appareils, fichiers |
| Curseurs | Xcursor | `index.theme` + fichiers curseurs | pointeurs et curseurs de saisie |
| Polices | Fontconfig / paramètres GNOME | fichiers de police et réglages | familles, graisse, taille et rendu |
| Fond d’écran | GNOME Background / URI | image + métadonnées | fond du bureau et écran de verrouillage |

Les thèmes Shell, GTK, icônes et curseurs sont des paquets distincts. Les paramètres de police et le fond d’écran ne sont pas des feuilles CSS.


## 1.1 Couches du bureau

| Couche | Composant | Contrôle | Mécanisme |
|---|---|---|---|
| Compositeur | Mutter | fenêtres, espaces, écrans, échelle, capture | paramètres / GSettings |
| Shell | GNOME Shell / St | panneau, Activités, menus, dash, OSD, verrouillage | thème, extensions, préférences |
| Widgets historiques | GTK 3 | widgets GTK 3 | thème GTK 3, CSS applicatif |
| Widgets modernes | GTK 4 | widgets GTK 4 | thème GTK 4, CSS applicatif |
| Design GNOME | Libadwaita | composants Adw et couleurs sémantiques | styles et API applicative |
| Préférences | Control Center / GSettings | comportement, apparence, périphériques | Paramètres, gsettings |
| Ressources | Freedesktop / Fontconfig | icônes, curseurs, fontes, sons | paquets de ressources |
| Connexion | GDM | écran de connexion | configuration système |

## 1.2 Niveaux de prise en charge

- **Directement thémable** : nœud CSS et propriétés exposés.
- **Configurable** : préférence GSettings ou option applicative.
- **Extensible** : code Shell ou extension.
- **Système** : dépend de GDM, Mutter, pilote, distribution ou droits administrateur.
- **Non garanti** : interface tierce, widget privé ou rendu propriétaire.

Ne jamais représenter une clé dconf comme une propriété CSS. L'éditeur doit afficher le niveau de prise en charge avant de proposer une modification.

## 1.3 Cascade et priorité

GTK utilise des providers CSS dont la priorité et la spécificité influencent le résultat. Une application peut ajouter son CSS ou dessiner ses composants. GNOME Shell peut être modifié par des extensions. Les sélecteurs privés ne sont pas une API stable. Utiliser des feuilles distinctes par moteur, des sélecteurs ciblés et tester les versions exactes.

## 1.4 Références
- [GNOME 51](https://release.gnome.org/51/)
- [GNOME Shell 51](https://github.com/GNOME/gnome-shell/tree/51.0)
- [Mutter](https://gitlab.gnome.org/GNOME/mutter)
- [GTK 3 CSS](https://docs.gtk.org/gtk3/css-overview.html)
- [GTK 4 CSS](https://docs.gtk.org/gtk4/css-overview.html)
