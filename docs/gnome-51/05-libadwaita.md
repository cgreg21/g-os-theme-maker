# Atelier pratique : personnaliser les applications Libadwaita

Libadwaita fournit des composants et des conventions visuelles aux applications GNOME modernes. Il s'appuie sur GTK 4, mais ne doit pas être confondu avec un simple thème GTK générique.

## 1. Comprendre la relation GTK 4 / Libadwaita

GTK 4 fournit les widgets de base, le moteur CSS, les fenêtres et les mécanismes d'accessibilité. Libadwaita ajoute des composants de haut niveau : barres d'outils, navigation, lignes de préférences, bannières, pages d'état et couleurs sémantiques.

Une application GTK 4 n'est pas nécessairement une application Libadwaita. Une application Libadwaita est une application GTK 4 qui utilise cette bibliothèque. Cette distinction est importante pour comprendre pourquoi un sélecteur fonctionne dans une application mais pas dans une autre.

## 2. Les couleurs sémantiques

Une couleur sémantique décrit un rôle plutôt qu'une teinte arbitraire. Par exemple, une couleur de texte principal, de texte secondaire, d'accent, d'avertissement ou de surface.

Cela permet aux composants de suivre les variantes clair et sombre. Évitez de remplacer toutes les couleurs par des valeurs fixes si vous souhaitez conserver le changement de mode.

La documentation Libadwaita publie les styles et variables disponibles. Leur nom et leur disponibilité peuvent changer avec la version. Référez-vous à la version installée et à la documentation officielle.

## 3. Composants à connaître

### Fenêtres et barres d'outils
- `AdwWindow` et `AdwApplicationWindow` structurent les fenêtres.
- `AdwHeaderBar` présente le titre et les contrôles de fenêtre.
- `AdwToolbarView` organise les barres d'outils autour du contenu.
- `AdwWindowTitle` affiche un titre et un sous-titre.

### Navigation
- `AdwNavigationView` et `AdwNavigationPage` organisent les pages.
- `AdwTabView` et `AdwTabBar` gèrent les onglets.
- `AdwViewSwitcher` et `AdwViewSwitcherBar` permettent de changer de vue.
- `AdwPreferencesPage`, `AdwPreferencesGroup` et `AdwPreferencesDialog` organisent les réglages.

### Lignes de préférences
- `AdwActionRow` présente un libellé, une description et une action.
- `AdwComboRow` choisit une valeur dans une liste.
- `AdwEntryRow` contient un champ de texte.
- `AdwPasswordEntryRow` contient un mot de passe.
- `AdwSpinRow` modifie une valeur numérique.
- `AdwSwitchRow` active ou désactive une option.
- `AdwExpanderRow` révèle des réglages supplémentaires.

### Composants complémentaires
- `AdwStatusPage` affiche un état vide ou une page d'information.
- `AdwBanner` affiche un message important.
- `AdwToastOverlay` et les toasts présentent des retours temporaires.
- `AdwCarousel` fait défiler des pages.
- `AdwClamp` limite la largeur du contenu.
- `AdwFlap` présente un panneau latéral.
- `AdwAvatar` affiche une identité visuelle.
- `AdwSpinner` indique un chargement.
- Les breakpoints adaptent la disposition aux dimensions disponibles.

## 4. Exemple de lecture d'une ligne de préférence

Une ligne de préférence peut afficher un titre, une description, un contrôle et un état. Ne la traitez pas comme un bouton ordinaire : le texte, le contrôle secondaire, la sélection et l'espacement doivent rester lisibles.

Exercice :
1. ouvrez une application qui utilise des préférences Adwaita ;
2. repérez une ligne simple et une ligne avec interrupteur ;
3. inspectez les nœuds et classes CSS ;
4. repérez la surface de la ligne, le titre, la description et le contrôle ;
5. testez une modification de couleur sur une copie de la feuille ;
6. vérifiez le mode clair, sombre et la largeur réduite.

Les noms de classes internes ne sont pas garantis. Le code de l'application peut aussi ajouter un style local.

## 5. Pourquoi le CSS utilisateur peut être limité

Libadwaita est conçue pour fournir une identité cohérente aux applications. L'application peut charger des feuilles prioritaires, utiliser des widgets personnalisés ou ne pas prendre en charge un thème externe. La présence d'un fichier CSS dans `gtk-4.0` ne prouve donc pas que chaque composant Adwaita sera modifié.

G-OS Theme Maker doit afficher la portée réelle de chaque propriété : style GTK global, variable Adwaita, style de l'application ou propriété non exposée. Ne présentez pas un sélecteur privé comme une option universelle.

## 6. Vérifier la version et la compatibilité

```sh
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
```

Comparez ensuite avec les API et la documentation correspondant à cette version. Les composants et variables de Libadwaita évoluent. Ne supposez pas que la documentation `1-latest` correspond exactement à une version ancienne installée.

Ressources : [Styles et apparence Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html), [variables CSS](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/css-variables.html).
