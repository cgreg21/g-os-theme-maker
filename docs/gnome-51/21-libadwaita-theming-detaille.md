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


## 15. Préparer un laboratoire Libadwaita

Libadwaita est une bibliothèque de composants et de conventions visuelles, pas seulement une feuille CSS supplémentaire. Avant de personnaliser une application, identifiez les versions de GTK et de Libadwaita réellement chargées.

~~~bash
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
~~~

Ces commandes indiquent les versions de développement installées sur le système. Elles ne prouvent pas à elles seules la version utilisée par une application Flatpak ou par un processus qui embarque ses propres bibliothèques.

Pour une application empaquetée, inspectez l'environnement d'exécution et les bibliothèques réellement chargées. Consignez la version dans votre fiche de test. Les variables CSS, classes et composants peuvent évoluer entre versions.

Travaillez sur une application de test et conservez un thème de référence. Ne modifiez pas directement les feuilles fournies par le système ou par l'application.

## 16. Comprendre la hiérarchie des surfaces

Une interface Libadwaita n'utilise pas une seule couleur de fond. Les surfaces ont des rôles différents et doivent conserver une hiérarchie visuelle.

Repérez séparément :
- fond de fenêtre ;
- surface de contenu ;
- barre d'en-tête ;
- carte ;
- popover ;
- panneau latéral ;
- ligne de préférence ;
- zone de saisie ;
- bannière et message temporaire.

Une carte ne doit pas se confondre avec le fond de fenêtre. Un popover doit apparaître comme une surface au premier plan. Une barre d'en-tête ne doit pas devenir visuellement indistincte du contenu si elle marque une séparation fonctionnelle.

Modifiez d'abord les variables sémantiques disponibles dans la version ciblée. N'ajoutez une règle de classe que lorsque le composant expose réellement cette classe et qu'une variable sémantique ne suffit pas.

## 17. Atelier : fenêtre de préférences et lignes de réglage

AdwPreferencesWindow organise les préférences en pages et groupes. Une ligne peut associer un titre, une description, un contrôle, une icône et une action secondaire.

Testez plusieurs types de lignes :
- ligne d'action ;
- ligne avec interrupteur ;
- ligne avec liste de choix ;
- ligne avec champ de texte ;
- ligne avec mot de passe ;
- ligne numérique ;
- ligne extensible ;
- ligne avec description longue.

Pour chacune, contrôlez :
1. Alignement du titre et de la description.
2. Taille et contraste du texte secondaire.
3. Alignement du contrôle.
4. Focus clavier.
5. État actif et désactivé.
6. Survol et activation.
7. Débordement des libellés longs.
8. Présentation à fenêtre étroite.

Ne forcez pas une hauteur fixe pour toutes les lignes. Les descriptions peuvent s'étendre et les contrôles peuvent avoir des dimensions différentes.

Une règle appliquée à toutes les lignes de préférences peut aussi toucher des composants imbriqués. Inspectez les nœuds CSS avant d'utiliser un sélecteur descendant large.

## 18. Atelier : navigation adaptative

Les composants de navigation Libadwaita peuvent changer de forme selon la largeur disponible. La structure est décidée par l'application et par ses breakpoints.

Testez une navigation large, puis réduisez progressivement la fenêtre. Observez :
- panneau latéral permanent ;
- panneau latéral superposé ;
- bouton de retour ;
- titre de page ;
- contenu principal ;
- menus de navigation ;
- focus après changement de page.

Vérifiez également le retour à une fenêtre large. Une interface ne doit pas conserver un état visuel incohérent après plusieurs changements de largeur.

Le CSS peut modifier les surfaces et séparateurs, mais ne doit pas simuler une navigation qui n'existe pas. Ne masquez pas un bouton retour ou un panneau sans vérifier que l'application propose une autre manière d'accéder aux pages.

## 19. Atelier : onglets et sélecteurs de vue

AdwTabView et AdwTabBar présentent des pages pouvant être ouvertes, fermées ou déplacées. AdwViewSwitcher et AdwViewSwitcherBar changent de vue au sein d'une même fenêtre.

Scénarios :
- un seul onglet ;
- plusieurs onglets ;
- onglet actif ;
- onglet inactif ;
- onglet avec titre long ;
- fermeture d'un onglet ;
- indicateur de chargement ;
- débordement ;
- navigation clavier ;
- fenêtre étroite.

Le marqueur de sélection doit rester visible sans dépendre uniquement de la couleur. Le bouton de fermeture doit être suffisamment distinct et rester accessible au clavier.

Pour un sélecteur de vue, vérifiez le libellé, l'icône, l'état actif et la présentation lorsque la barre est déplacée vers une position compacte.

## 20. Atelier : boutons fractionnés et groupes de bascules

AdwSplitButton associe une action principale et un menu secondaire. AdwToggleGroup présente plusieurs choix liés.

Pour un bouton fractionné, testez séparément :
- activation de l'action principale ;
- ouverture du menu ;
- navigation dans les choix ;
- fermeture du menu ;
- focus clavier ;
- libellé long.

Pour un groupe de bascules, vérifiez :
- choix actif ;
- choix inactif ;
- focus ;
- désactivation ;
- groupe étroit ;
- libellés longs ;
- navigation clavier.

Ne donnez pas à l'action principale et au menu secondaire le même indicateur visuel si leurs fonctions diffèrent. La décoration ne doit pas rendre l'action ambiguë.

## 21. Atelier : cartes, bannières, états vides et toasts

Les cartes structurent les contenus, tandis que les bannières et toasts signalent un état ou un résultat.

Préparez les cas suivants :
- carte simple ;
- carte avec titre et description ;
- carte contenant un contrôle ;
- bannière d'information ;
- bannière d'avertissement ;
- état vide ;
- toast court ;
- toast avec action ;
- plusieurs messages successifs.

Vérifiez que le message temporaire ne masque pas une action essentielle. Une information importante doit rester accessible après la disparition d'un toast.

Pour les états vides, contrôlez l'illustration ou l'icône, le titre, le texte explicatif et l'action proposée. Le contenu doit rester compréhensible si l'image ne peut pas être affichée.

## 22. Atelier : champs et contrôles spécialisés

Testez les champs de texte, champs de recherche, champs de mot de passe, contrôles numériques et interrupteurs.

Pour chaque champ, vérifiez :
- libellé ;
- texte indicatif ;
- texte saisi ;
- curseur ;
- sélection ;
- focus ;
- erreur ;
- état désactivé ;
- texte long ;
- caractères accentués.

Le texte indicatif ne doit pas être le seul libellé. Un champ de mot de passe doit conserver un contrôle de visibilité compréhensible. Les messages d'erreur doivent être visibles et associés au champ.

Pour les interrupteurs, vérifiez l'état actif et inactif, le focus, la navigation clavier et le contraste. Ne confondez pas un interrupteur désactivé avec un interrupteur simplement inactif.

## 23. Tester les préférences de thème et les variantes

Les applications Libadwaita peuvent suivre la préférence d'apparence du système, proposer un choix clair/sombre ou appliquer une préférence propre à l'application.

Testez les transitions réelles :
1. Démarrez l'application dans la variante claire.
2. Ouvrez plusieurs pages et dialogues.
3. Changez la préférence d'apparence selon le mécanisme prévu.
4. Vérifiez les mêmes pages dans la variante sombre.
5. Contrôlez les menus, popovers, cartes et notifications.
6. Redémarrez l'application si nécessaire et comparez.

Ne supposez pas que toutes les applications suivent instantanément le même réglage. Une application peut proposer son propre choix ou ne pas exposer de changement dynamique.

Contrôlez les couleurs sémantiques dans les deux variantes. Une couleur d'accent lisible sur fond clair peut manquer de contraste sur fond sombre.

## 24. Diagnostic : une application ne suit pas le thème

Quand une application ne reflète pas une variable ou une règle, vérifiez successivement :
- la version de Libadwaita ;
- la version GTK ;
- le mode de distribution ;
- la préférence d'apparence de l'application ;
- les feuilles CSS ajoutées par le développeur ;
- les classes réellement présentes ;
- les ressources embarquées ;
- les widgets personnalisés.

Certaines applications chargent leur propre CSS ou utilisent des composants dessinés. Le thème global ne peut pas nécessairement les remplacer.

Ne compensez pas une feuille privée par des règles globales de plus en plus spécifiques. Isolez l'application concernée et documentez la limite.

## 25. Accessibilité, clavier et internationalisation

Testez l'interface sans souris et avec un texte agrandi. Vérifiez que le focus reste visible dans les pages de préférences, les menus, les onglets et les boutons fractionnés.

Contrôlez également :
- contraste des textes secondaires ;
- état actif et désactivé ;
- taille des cibles ;
- libellés longs ;
- caractères non latins ;
- langue RTL ;
- ordre des actions ;
- icônes directionnelles ;
- messages d'erreur et d'avertissement.

Une règle de style ne corrige pas un rôle accessible, un nom manquant ou un ordre de focus incorrect. Utilisez un lecteur d'écran pour valider les informations sémantiques.

## 26. Fiche de validation Libadwaita

~~~text
Application et version :
Version GTK :
Version Libadwaita :
Mode de distribution :
Préférence d'apparence :
Fenêtre et headerbar :
Pages et groupes de préférences :
Lignes de réglage :
Navigation adaptative :
Onglets et sélecteurs de vue :
Boutons fractionnés :
Groupes de bascules :
Cartes et états vides :
Bannières et toasts :
Champs et contrôles :
Menus et popovers :
Variante claire :
Variante sombre :
Focus et navigation clavier :
Lecteur d'écran :
Texte agrandi :
Langue et RTL :
Styles propres à l'application :
Sélecteurs et variables testés :
Captures de référence :
Anomalies :
Conclusion : validé / partiel / à corriger
~~~

Validez les mêmes parcours sur plusieurs applications Libadwaita. Le fait qu'une variable s'applique dans une application ne garantit pas qu'un composant personnalisé d'une autre application l'utilise.
