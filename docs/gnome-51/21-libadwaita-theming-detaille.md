# Personnaliser Libadwaita : surfaces, préférences, navigation et composants adaptatifs

Libadwaita fournit les composants visuels de nombreuses applications GNOME modernes. Elle repose sur GTK 4, mais apporte ses propres conventions, composants et couleurs sémantiques.

Ce chapitre approfondit les composants les plus courants et explique ce qu'un thème global peut réellement modifier.

## 1. Le principe des couleurs sémantiques

Une couleur sémantique décrit un rôle dans l'interface : fond de fenêtre, surface de contenu, carte, popover, texte principal, texte secondaire, accent ou action destructive.

Les noms usuels comprennent :

- --window-bg-color et --window-fg-color ;
- --view-bg-color et --view-fg-color ;
- --headerbar-bg-color et --headerbar-fg-color ;
- --card-bg-color et --card-fg-color ;
- --popover-bg-color et --popover-fg-color ;
- --accent-bg-color, --accent-fg-color et --accent-color ;
- --destructive-color et les couleurs d'avertissement selon la version.

Exemple :

~~~css
:root {
  --window-bg-color: #f6f5f4;
  --window-fg-color: #241f31;
  --view-bg-color: #ffffff;
  --view-fg-color: #241f31;
  --headerbar-bg-color: #f6f5f4;
  --headerbar-fg-color: #241f31;
  --card-bg-color: #ffffff;
  --card-fg-color: #241f31;
  --popover-bg-color: #ffffff;
  --popover-fg-color: #241f31;
  --accent-bg-color: #3584e4;
  --accent-fg-color: #ffffff;
  --accent-color: #3584e4;
}
~~~

Les variables disponibles évoluent avec Libadwaita. Vérifiez la référence correspondant à la version installée. Ne copiez pas une variable récente dans une version ancienne sans contrôle.

## 2. Fenêtres et barres d'en-tête

Les composants principaux sont AdwWindow, AdwApplicationWindow, AdwHeaderBar, AdwToolbarView et AdwWindowTitle.

La barre d'en-tête peut accueillir le titre, le sous-titre, les boutons d'action, les menus et les contrôles de fenêtre. Les applications peuvent personnaliser son contenu.

Exemple de personnalisation de base :

~~~css
headerbar {
  background-color: var(--headerbar-bg-color);
  color: var(--headerbar-fg-color);
}

headerbar .title {
  font-weight: 700;
}
~~~

Vérifiez les fenêtres maximisées, les contrôles de fenêtre, les menus de la barre et les dispositions droite-à-gauche.

## 3. Cartes et groupes

Les cartes sont courantes dans les pages de préférences, les vues de contenu et les tableaux de bord.

~~~css
.card {
  background-color: var(--card-bg-color);
  color: var(--card-fg-color);
  border-radius: 12px;
}
~~~

Ne forcez pas toutes les surfaces à devenir des cartes. Une page de préférences, une liste de résultats et une zone de contenu n'ont pas la même hiérarchie visuelle.

## 4. Pages de préférences

AdwPreferencesWindow, AdwPreferencesPage et AdwPreferencesGroup structurent les réglages. Les lignes peuvent être :

- AdwActionRow ;
- AdwComboRow ;
- AdwEntryRow ;
- AdwPasswordEntryRow ;
- AdwSpinRow ;
- AdwSwitchRow ;
- AdwExpanderRow.

Les lignes présentent souvent un titre, une description, une icône, un contrôle et parfois une action secondaire. Il faut vérifier séparément le texte principal, la description, le contrôle, l'état actif et l'état indisponible.

Exercice : repérez une AdwSwitchRow dans les préférences d'une application, inspectez ses nœuds CSS, puis modifiez uniquement le style de son contrôle. Vérifiez que le titre et la description restent alignés.

## 5. Navigation et panneaux latéraux

AdwNavigationView, AdwNavigationPage, AdwNavigationSplitView, AdwOverlaySplitView et AdwFlap organisent la navigation.

Ces composants peuvent changer de présentation selon la largeur disponible. Un panneau latéral peut devenir un panneau superposé ou être remplacé par une navigation arrière.

Le CSS peut modifier les surfaces et les séparateurs, mais ne remplace pas les règles de disposition et les breakpoints de l'application.

Testez :
- fenêtre large ;
- fenêtre étroite ;
- panneau ouvert ;
- panneau fermé ;
- navigation arrière ;
- changement de page ;
- orientation RTL.

## 6. Onglets et sélecteurs de vue

AdwTabView et AdwTabBar gèrent les onglets. AdwViewSwitcher et AdwViewSwitcherBar permettent de changer de vue dans une fenêtre.

Les états visuels importants sont l'onglet actif, le focus, le survol, le débordement, les onglets fermables et les libellés longs. Ne réduisez pas l'indicateur de sélection au point qu'il disparaisse.

Inspectez les classes de style réellement présentes. Les noms de classes API ne sont pas automatiquement des sélecteurs CSS.

## 7. Boutons et contrôles spécialisés

AdwButtonContent, AdwSplitButton et AdwToggleGroup enrichissent les boutons GTK.

Un bouton fractionné combine une action principale et une action secondaire. Un groupe de bascules présente plusieurs choix. Il faut conserver une distinction visible entre l'action directe et le menu secondaire.

Testez les états normal, hover, focus, active, selected et disabled. Contrôlez également la navigation au clavier.

## 8. Pages d'état, bannières et toasts

AdwStatusPage présente un état vide ou une information importante. AdwBanner affiche un message dans la page. AdwToastOverlay et AdwToast présentent un retour temporaire.

Les messages doivent rester lisibles et ne pas masquer les contrôles importants. Une notification temporaire ne doit pas être le seul endroit où une information essentielle est disponible.

Exemple de surface de bannière :

~~~css
.banner {
  border-radius: 10px;
}
~~~

La classe exacte doit être vérifiée dans l'application. Ne supposez pas que chaque AdwBanner expose une classe CSS identique.

## 9. Largeur de contenu et adaptation

AdwClamp et AdwClampScrollable limitent la largeur du contenu pour préserver le confort de lecture. AdwBreakpoint permet de faire évoluer la structure selon la taille disponible.

Une règle CSS ne remplace pas un breakpoint. Elle peut modifier l'espacement et les couleurs, mais la logique qui masque une barre latérale ou change la navigation appartient à l'application.

Testez plusieurs largeurs et évitez de fixer des tailles qui empêchent les applications de s'adapter.

## 10. Avatars, chargements et carrousels

AdwAvatar affiche une identité visuelle. AdwSpinner indique un chargement. AdwCarousel présente plusieurs pages ou éléments.

Vérifiez les tailles d'avatar, le contraste du contenu de remplacement, la visibilité du spinner et les indicateurs de pagination. Les animations doivent respecter les préférences de réduction du mouvement.

## 11. Limites du thème utilisateur

Libadwaita n'offre pas un mécanisme universel de re-skinning de toutes les applications. Une application peut :

- charger son propre CSS ;
- ajouter des classes privées ;
- dessiner un composant avec un widget personnalisé ;
- utiliser une version différente de Libadwaita ;
- désactiver ou remplacer certaines règles de thème.

Un thème global ne doit pas promettre de modifier chaque application. Dans un éditeur de thèmes, distinguez les variables sémantiques, les classes documentées, les styles propres à une application et les éléments non exposés.

## 12. Vérifier les versions

~~~bash
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
~~~

Comparez les versions aux références API et CSS correspondantes. La documentation en ligne 1-latest peut décrire une version plus récente que celle installée.

## 13. Exercices

1. Modifiez les couleurs sémantiques d'une application de test.
2. Personnalisez une barre d'en-tête.
3. Repérez une carte et une ligne de préférences.
4. Testez un panneau de navigation à plusieurs largeurs.
5. Vérifiez les états d'un bouton fractionné ou d'un groupe de bascules.
6. Testez la variante sombre et le contraste élevé.

## 14. Références

- [Styles et apparence Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)
- [Variables CSS Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/css-variables.html)
- [Référence API Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/)
- [Vue d'ensemble CSS GTK 4](https://docs.gtk.org/gtk4/css-overview.html)
