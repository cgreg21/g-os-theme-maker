# Catalogue pratique : comment modifier chaque famille de composants

Ce chapitre transforme l'inventaire technique en méthode de travail. Les noms CSS précis restent à vérifier dans les sources de GNOME Shell 51, GTK et Libadwaita. Un composant peut être composé de plusieurs nœuds : son fond, son texte, son icône, son séparateur et ses états peuvent nécessiter des règles différentes.

## 1. Panneau supérieur

Éléments à vérifier : fond du panneau, boutons Activités, horloge, indicateurs réseau/son/alimentation, indicateurs de confidentialité, menu d'état et notifications.

Pour chaque élément, examinez :
- surface et transparence ;
- hauteur et alignement vertical ;
- marge extérieure et padding intérieur ;
- typographie et taille d'icône ;
- hover, focus et état actif ;
- séparateurs et indicateurs ;
- lisibilité en mode clair et sombre.

Exercice : modifiez le fond du panneau, puis le bouton de l'horloge, sans modifier les autres boutons. Comparez les sélecteurs et évitez une règle trop générale.

## 2. Vue Activités

Éléments : fond, recherche, résultats, sections, aperçus de fenêtres, miniatures des espaces, sélection et transitions.

Vérifiez le champ de recherche avec du texte long, sans résultat et avec plusieurs catégories de résultats. Les miniatures doivent rester visibles sur des fonds d'écran clairs comme sombres.

## 3. Grille d'applications

Éléments : tuile, icône, libellé, indicateur d'application en cours, dossier, titre du dossier, navigation et pagination.

Le style du conteneur ne remplace pas l'icône. Testez les libellés longs, les noms traduits, les icônes manquantes et les dossiers contenant peu ou beaucoup d'applications.

## 4. Dock

Éléments : arrière-plan, icônes, applications épinglées, application en cours, indicateur, bouton afficher les applications, séparateur, infobulle, emplacement de dépôt.

Le CSS gère l'apparence, pas la logique de lancement ni le déplacement. Testez le survol, le focus clavier, le lancement, l'application active, les éléments épinglés et les zones de glisser-déposer.

## 5. Espaces de travail et sélecteurs de fenêtres

Éléments : miniatures, espace courant, aperçu de fenêtre, Alt-Tab, sélection de source de saisie et mise en évidence.

Vérifiez les fenêtres de tailles différentes, les applications avec plusieurs fenêtres et les configurations multi-écrans. Les animations et la logique de changement relèvent du Shell/Mutter.

## 6. Menus, popovers et menus contextuels

Éléments : conteneur, flèche, élément, sous-menu, séparateur, icône, case à cocher, interrupteur et élément désactivé.

Un menu complet doit être lisible lorsque la ligne est normale, survolée, sélectionnée, désactivée ou ouverte en sous-menu. Testez également les menus contenant un curseur, une liste ou une description secondaire.

## 7. Réglages rapides

Éléments : grille, bascule, bascule avec sous-menu, titre, sous-titre, icône, curseur, périphérique et état de connexion.

Testez les états activé/désactivé, connecté/déconnecté, indisponible, chargement et absence de périphérique. N'associez pas une couleur unique à l'état : gardez une icône ou un libellé compréhensible.

## 8. Calendrier et date

Éléments : bouton de date, mois, navigation, jour courant, week-end, jours hors mois, numéro de semaine et événements.

Testez les dates longues, le changement de mois, le premier jour de semaine selon les paramètres régionaux, les événements multiples et l'absence d'événement.

## 9. Horloges mondiales et météo

Éléments : ville, fuseau, heure, prévisions, icône météo, température et état indisponible.

Le thème ne contrôle pas les données. Il doit simplement présenter correctement les valeurs disponibles, y compris les textes manquants ou les erreurs de service.

## 10. Notifications

Éléments : liste, groupe, en-tête, source, titre, corps, horodatage, action, fermeture, expansion, média et bannière.

Testez une notification courte, longue, empilée, avec action, avec média et sans icône. Gardez les boutons d'action identifiables.

## 11. Dialogues et authentification

Éléments : dialogue modal, titre, description, boutons, listes, champ de mot de passe, erreur, information, polkit et sélection de périphérique.

Les dialogues sensibles doivent conserver un contraste élevé et des avertissements visibles. Ne rendez pas les messages d'erreur dépendants uniquement du rouge.

## 12. Verrouillage, connexion et saisie

Éléments : horloge, identité utilisateur, champ de mot de passe, retour d'erreur, notifications privées, clavier virtuel, emoji, IBus et suggestions.

Le thème Shell utilisateur ne contrôle pas nécessairement GDM. Distinguez écran de verrouillage et écran de connexion. Testez la saisie clavier et les langues avec caractères complexes.

## 13. OSD et capture d'écran

Éléments : volume, luminosité, périphérique, capture, sélection de zone, indicateur d'enregistrement et partage d'écran.

Les OSD sont souvent affichés brièvement. Vérifiez le contraste sur les fonds les plus clairs et les plus sombres, la taille du texte et la visibilité des indicateurs de confidentialité.

## 14. Widgets GTK 3

Couvrir au minimum :
- fenêtres, dialogues et barres d'en-tête ;
- boutons, boutons bascules, cases et radios ;
- interrupteurs, champs, recherche et texte multiligne ;
- menus, popovers, infobulles et barres d'outils ;
- listes, TreeView, colonnes, onglets et conteneurs ;
- barres de progression, niveaux, curseurs et défilement ;
- calendrier, sélecteurs de fichiers, couleurs et polices.

Pour chaque famille, inspectez les sous-nœuds et états. GTK 3 peut exposer des classes CSS différentes d'un widget à l'autre.

## 15. Widgets GTK 4

Couvrir au minimum :
- fenêtres et dialogues ;
- HeaderBar et contrôles de fenêtre ;
- boutons, cases, interrupteurs et spinners ;
- Entry, PasswordEntry, SearchEntry et TextView ;
- Label, listes, grilles, ListView et ColumnView ;
- Popover, Stack, Assistant et navigation ;
- Scale, ProgressBar et Scrollbar ;
- Calendar, ColorDialog et FileDialog ;
- Picture, Image, séparateurs et conteneurs.

Les composants GTK 4 peuvent avoir des nœuds internes différents des widgets GTK 3 portant un nom similaire.

## 16. Composants Libadwaita

Couvrir au minimum :
- fenêtres, HeaderBar, ToolbarView et WindowTitle ;
- NavigationView, pages, onglets et ViewSwitcher ;
- pages et groupes de préférences ;
- ActionRow, ComboRow, EntryRow, PasswordEntryRow, SpinRow, SwitchRow et ExpanderRow ;
- StatusPage, Banner, ToastOverlay, Carousel, Clamp, Flap, Avatar, Spinner et Breakpoint.

Pour chaque composant, identifiez les styles exposés par Libadwaita et les éventuels styles propres à l'application. Ne promettez pas la personnalisation universelle de tous les composants.

## 17. États obligatoires pour chaque composant interactif

Pour chaque famille, contrôlez normal, hover, focus clavier, actif/pressed, sélectionné/checked, désactivé, erreur, avertissement, chargement, vide et glisser-déposer si applicable. Vérifiez aussi fenêtre inactive, contraste élevé, clair/sombre, RTL et HiDPI.

## 18. Fiche de couverture à remplir

Pour chaque élément pris en charge par l'éditeur, consignez en texte :
- cible et version exacte ;
- zone et nom du composant ;
- nom du nœud ou sélecteur vérifié ;
- propriétés réellement prises en charge ;
- états disponibles ;
- méthode d'aperçu ;
- test effectué ;
- limites connues ;
- source amont et date de vérification.

Un élément ne doit être déclaré pris en charge qu'après vérification dans le moteur réel. Un nom dans un inventaire n'est pas une preuve de fonctionnement.
