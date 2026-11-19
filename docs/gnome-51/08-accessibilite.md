# 8. Accessibilité, mouvement, langue et densité

## 6. États communs à chaque composant

Un catalogue complet ne s’arrête pas à l’apparence normale. Pour chaque composant interactif, prévoir et tester :

| État | Description | Règle de conception |
|---|---|---|
| Normal | repos | lisible et équilibré |
| Hover | pointeur au-dessus | différence visible mais discrète |
| Focus | navigation clavier | contour visible, jamais supprimé sans remplacement |
| Active / pressed | action en cours | retour visuel immédiat |
| Checked / selected | sélection persistante | contraste et indicateur explicite |
| Disabled / insensitive | indisponible | contraste réduit mais texte encore compréhensible |
| Backdrop / inactive | fenêtre inactive | hiérarchie visuelle conservée |
| Expanded / collapsed | panneau ouvert/fermé | état identifiable |
| Error | saisie invalide | couleur + indication non chromatique |
| Warning | avertissement | distinction du message d’erreur |
| Loading | chargement | spinner ou progression |
| Empty | aucune donnée | état vide lisible |
| Drag source / drop target | glisser-déposer | source, cible et emplacement visibles |
| High contrast | contraste renforcé | contours, icônes et textes robustes |

Prévoir aussi les directions LTR/RTL, les échelles HiDPI, les tailles de texte, la navigation clavier et les préférences de réduction des animations.

## 7. Variantes d’apparence

Les variantes ne doivent pas être un simple filtre inversant les couleurs.

- **Clair** : surfaces lumineuses, textes sombres, bordures lisibles.
- **Sombre** : surfaces sombres, textes clairs, niveaux de surface distincts.
- **Contraste élevé** : bordures renforcées, états explicites, dépendance réduite aux ombres et à la couleur.
- **Accent** : couleur sélectionnée, focus, contrôles actifs et indicateurs.
- **Densité** : espacements compacts ou confortables sans réduire les zones interactives.
- **Échelle** : tailles cohérentes à différentes densités d’écran et tailles de police.

GNOME Shell 51 fournit des variantes SCSS clair, sombre et contraste élevé. Le thème doit vérifier chacune des trois.


## 8.1 Contraste

Mesurer contraste textes, icônes informatives, contours, contrôles et focus. Une couleur ne doit jamais être le seul signal d'erreur, succès ou sélection : ajouter texte, forme ou icône.

## 8.2 Réduction des animations

GNOME 51 étend la prise en compte de la préférence de réduction des animations, y compris dans davantage de widgets et le Shell. Prévoir une alternative sans mouvement. Ne pas supposer que `prefers-reduced-motion` du Web existe dans GTK ou St.

## 8.3 Focus et clavier

Tester sans souris : tabulation, focus visible, activation Entrée/Espace, menus, popovers, listes, dialogues, échappement et retour. Ne jamais supprimer le focus sans remplacement. Détecter les conflits de raccourcis.

## 8.4 Lecteurs d'écran

Rôles, noms accessibles, descriptions et ordre de lecture viennent des widgets et applications. CSS ne corrige pas un arbre d'accessibilité défectueux ; identifier ces aspects comme non thémables.

## 8.5 RTL et internationalisation

Tester langues LTR/RTL, marges logiques, icônes directionnelles miroir, textes longs, troncature, formats date/heure, chiffres et glyphes. Ne pas inverser les icônes non directionnelles.

## 8.6 HiDPI et densité

Tester 100, 125, 150, 175 et 200 %, multi-écrans, icônes raster/vectorielles, curseurs et hotspots, bordures fines, ombres et textes. Les tailles GTK sont logiques. Une variante compacte ne doit pas rendre les contrôles inaccessibles ; prévoir densité confortable et tactile.
