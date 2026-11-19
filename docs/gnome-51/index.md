# Manuel de création et de personnalisation GNOME 51

Ce manuel est conçu pour accompagner un débutant depuis ses premières notions jusqu'à la création d'un thème GNOME structuré. Il comprend des tutoriels pratiques, des exemples de fichiers, des exercices, des méthodes de diagnostic et un catalogue technique des composants.

La documentation cible GNOME Shell 51.0, GTK 3.24, GTK 4 et Libadwaita. Les sélecteurs Shell et les détails internes des widgets peuvent changer : vérifiez toujours la version réellement installée.

## Parcours débutant — à lire dans l'ordre

1. [Bien démarrer : comprendre GNOME avant de le personnaliser](00-bien-demarrer.md)
2. [Créer son premier thème complet](01-creer-premier-theme.md)
3. [Comprendre et écrire du CSS pour GNOME](02-css-debutant.md)
4. [Atelier pratique : personnaliser GNOME Shell 51](03-atelier-gnome-shell.md)
5. [Atelier pratique : GTK 3 et GTK 4](04-atelier-gtk.md)
6. [Atelier pratique : Libadwaita](05-libadwaita.md)
7. [Créer et modifier les ressources visuelles](06-icones-curseurs-polices-fonds.md)
8. [Paramètres GNOME, installation et dépannage](07-parametres-installation-diagnostic.md)
9. [Catalogue pratique de toutes les familles de composants](08-catalogue-pratique-composants.md)
10. [Personnaliser les applications GNOME](11-applications-gnome.md)

## Compléments pédagogiques

- [Personnaliser les applications GNOME](11-applications-gnome.md)
- [Méthode d'inspection et de diagnostic CSS](12-inspection-et-diagnostic-css.md)

## Référence technique

- [Architecture et périmètre](01-architecture.md)
- [Inventaire GNOME Shell 51](02-gnome-shell.md)
- [GTK 3, GTK 4 et Libadwaita](03-gtk-libadwaita.md)
- [Référence CSS](04-reference-css.md)
- [GSettings et dconf](05-parametres-gnome.md)
- [Icônes, curseurs, polices, fonds et sons](06-ressources-visuelles.md)
- [Extensions, Mutter, GDM et session](07-extensions-mutter-gdm.md)
- [Accessibilité, mouvement, langue et densité](08-accessibilite.md)
- [Construction, installation et validation](09-construction-validation.md)
- [Sources officielles et inventaire](10-sources-et-inventaire.md)

## Comment utiliser ce manuel

Lisez d'abord le parcours débutant. Réalisez les exercices dans un dossier de test et ne modifiez pas les fichiers système. Lorsque vous souhaitez personnaliser un composant précis, utilisez le catalogue pour retrouver sa famille, puis consultez le tutoriel du moteur correspondant.

Chaque exemple est un point de départ et doit être vérifié avec la version ciblée. Un sélecteur CSS peut être valide sans correspondre à un composant présent. Une application peut charger son propre style. Les extensions peuvent ajouter des widgets et le thème utilisateur ne contrôle pas tous les moteurs.

## Ce que signifie « tous les éléments »

Le manuel vise la couverture de toutes les familles de composants natifs documentées pour GNOME Shell 51, GTK 3, GTK 4 et Libadwaita, ainsi que des ressources visuelles et paramètres GNOME. Il ne peut pas garantir la modification de chaque widget personnalisé de chaque application tierce, ni des écrans système protégés. Ces limites sont identifiées plutôt que masquées.

## Formats exportés

Le PDF et l'EPUB sont générés à partir des chapitres Markdown. Après chaque modification de la documentation, reconstruisez les deux formats et vérifiez qu'ils contiennent bien le parcours débutant et les exemples.
