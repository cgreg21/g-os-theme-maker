# 1. Architecture et périmètre

Ce guide est le catalogue de référence de G-OS Theme Maker. Il décrit les familles d’éléments visuels qu’un thème peut couvrir, les moteurs qui les dessinent, les états à prévoir et les limites de compatibilité.

La référence GNOME Shell est **GNOME Shell 51.0** (sources amont). Les applications sont séparées selon **GTK 3**, **GTK 4** et **Libadwaita**. Ce catalogue distingue les éléments réellement stylables des éléments dont l’apparence est contrôlée par le système, l’application ou une extension.

> « Couvrir tous les éléments » signifie couvrir toutes les familles de composants d’interface et leurs états, et fournir un inventaire vérifiable des composants GNOME Shell 51. Les applications peuvent créer leurs propres widgets : aucun thème global ne peut garantir le style de chaque interface tierce.

## 1. Périmètre : les moteurs de rendu

Un bureau GNOME n’a pas un moteur de thème unique. Il faut produire et tester plusieurs feuilles indépendantes.

- **Cible** : GNOME Shell 51 ; **Technologie** : St / Clutter ; **Ressource principale** : `gnome-shell.css` ; **Éléments couverts** : panneau, vue Activités, dash, menus système, notifications, verrouillage, OSD
- **Cible** : GTK 3.24 ; **Technologie** : GTK CSS ; **Ressource principale** : `gtk-3.0/gtk.css` ; **Éléments couverts** : widgets GTK 3 et anciennes applications
- **Cible** : GTK 4 ; **Technologie** : GTK CSS ; **Ressource principale** : `gtk-4.0/gtk.css` ; **Éléments couverts** : widgets GTK 4
- **Cible** : Libadwaita ; **Technologie** : GTK 4 + styles Adwaita ; **Ressource principale** : CSS de l’application / CSS utilisateur ; **Éléments couverts** : fenêtres et composants Adwaita
- **Cible** : Icônes ; **Technologie** : Freedesktop Icon Theme ; **Ressource principale** : `index.theme` + ressources ; **Éléments couverts** : applications, actions, appareils, fichiers
- **Cible** : Curseurs ; **Technologie** : Xcursor ; **Ressource principale** : `index.theme` + fichiers curseurs ; **Éléments couverts** : pointeurs et curseurs de saisie
- **Cible** : Polices ; **Technologie** : Fontconfig / paramètres GNOME ; **Ressource principale** : fichiers de police et réglages ; **Éléments couverts** : familles, graisse, taille et rendu
- **Cible** : Fond d’écran ; **Technologie** : GNOME Background / URI ; **Ressource principale** : image + métadonnées ; **Éléments couverts** : fond du bureau et écran de verrouillage

Les thèmes Shell, GTK, icônes et curseurs sont des paquets distincts. Les paramètres de police et le fond d’écran ne sont pas des feuilles CSS.

## 1.1 Couches du bureau

- **Couche** : Compositeur ; **Composant** : Mutter ; **Contrôle** : fenêtres, espaces, écrans, échelle, capture ; **Mécanisme** : paramètres / GSettings
- **Couche** : Shell ; **Composant** : GNOME Shell / St ; **Contrôle** : panneau, Activités, menus, dash, OSD, verrouillage ; **Mécanisme** : thème, extensions, préférences
- **Couche** : Widgets historiques ; **Composant** : GTK 3 ; **Contrôle** : widgets GTK 3 ; **Mécanisme** : thème GTK 3, CSS applicatif
- **Couche** : Widgets modernes ; **Composant** : GTK 4 ; **Contrôle** : widgets GTK 4 ; **Mécanisme** : thème GTK 4, CSS applicatif
- **Couche** : Design GNOME ; **Composant** : Libadwaita ; **Contrôle** : composants Adw et couleurs sémantiques ; **Mécanisme** : styles et API applicative
- **Couche** : Préférences ; **Composant** : Control Center / GSettings ; **Contrôle** : comportement, apparence, périphériques ; **Mécanisme** : Paramètres, gsettings
- **Couche** : Ressources ; **Composant** : Freedesktop / Fontconfig ; **Contrôle** : icônes, curseurs, fontes, sons ; **Mécanisme** : paquets de ressources
- **Couche** : Connexion ; **Composant** : GDM ; **Contrôle** : écran de connexion ; **Mécanisme** : configuration système

## 1.2 Niveaux de prise en charge

- **Directement thémable** : nœud CSS et propriétés exposés.
- **Configurable** : préférence GSettings ou option applicative.
- **Extensible** : code Shell ou extension.
- **Système** : dépend de GDM, Mutter, pilote, distribution ou droits administrateur.
- **Non garanti** : interface tierce, widget privé ou rendu propriétaire.

Ne jamais représenter une clé dconf comme une propriété CSS. Le niveau de prise en charge doit être explicite avant toute modification.

## 1.3 Cascade et priorité

GTK utilise des providers CSS dont la priorité et la spécificité influencent le résultat. Une application peut ajouter son CSS ou dessiner ses composants. GNOME Shell peut être modifié par des extensions. Les sélecteurs privés ne sont pas une API stable. Utiliser des feuilles distinctes par moteur, des sélecteurs ciblés et tester les versions exactes.

## 1.4 Choisir le bon fichier avant de modifier l'apparence

Suivez toujours cette séquence. Elle évite d'écrire une règle dans une feuille qui n'est jamais chargée par le composant visé.

1. **Identifier l'application ou la zone** : panneau supérieur, menu système, fenêtre d'application, bouton, icône ou curseur.
2. **Identifier le moteur** : le panneau et les menus du bureau relèvent de GNOME Shell/St ; un bouton dans une application GTK relève de GTK 3 ou GTK 4 ; un composant Adw utilise Libadwaita.
3. **Identifier la version réelle** : ne déduisez pas la version GTK de la seule version GNOME. Une application peut encore utiliser GTK 3.
4. **Observer le composant** : inspectez le widget ou l'acteur, son nom, ses classes et les règles déjà appliquées. Les chapitres d'inspection expliquent les outils adaptés à chaque moteur.
5. **Choisir le mécanisme** : CSS pour un style exposé, préférence pour un réglage documenté, ressource pour une icône ou une police, extension lorsque le Shell doit être modifié fonctionnellement.
6. **Tester dans une portée limitée** : créez une règle minimale, vérifiez qu'elle correspond, puis ajoutez les propriétés une par une.

### Exemple : changer la couleur du panneau supérieur

Le panneau supérieur appartient à GNOME Shell, pas à GTK. Une règle placée dans `gtk-4.0/gtk.css` ne le modifiera pas. La feuille concernée est celle du thème Shell, généralement `gnome-shell/gnome-shell.css` dans un thème installé. Il faut ensuite confirmer le sélecteur dans le code et le thème de GNOME Shell 51.0 ; ne pas supposer qu'un nom de classe vu dans une ancienne version existe encore.

### Exemple : changer l'apparence d'un bouton d'application

Identifiez d'abord le toolkit de l'application. Si elle utilise GTK 3, ses règles GTK 4 ne seront pas chargées. Si elle utilise GTK 4 avec Libadwaita, le style peut dépendre de classes sémantiques et de variables Adwaita ; un sélecteur générique GTK peut être insuffisant ou volontairement neutralisé par l'application. Vérifiez le résultat dans l'application réelle.

### Vérifier les versions installées

Sur une distribution disposant de `pkg-config`, ces commandes donnent les versions des bibliothèques installées :

```sh
gnome-shell --version
pkg-config --modversion gtk+-3.0
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
```

Une commande peut échouer si le paquet de développement correspondant n'est pas installé. Cela ne signifie pas que la bibliothèque d'exécution est absente ; vérifiez alors les paquets de la distribution.

## 1.5 Références
- [GNOME 51](https://release.gnome.org/51/)
- [GNOME Shell 51](https://github.com/GNOME/gnome-shell/tree/51.0)
- [Mutter](https://gitlab.gnome.org/GNOME/mutter)
- [GTK 3 CSS](https://docs.gtk.org/gtk3/css-overview.html)
- [GTK 4 CSS](https://docs.gtk.org/gtk4/css-overview.html)
