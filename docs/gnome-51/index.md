# Manuel de création et de personnalisation GNOME 51

Ce manuel accompagne un débutant depuis ses premières notions jusqu'à la création d'un thème GNOME structuré. Il comprend des tutoriels pratiques, des exemples, des exercices, des captures d'écran légendées, des méthodes de diagnostic et un catalogue technique.

La documentation cible GNOME Shell 51.0, GTK 3.24, GTK 4 et Libadwaita. Les sélecteurs Shell et les détails internes des widgets peuvent changer : vérifiez toujours la version installée.

## Parcours débutant — à lire dans l'ordre

1. [Bien démarrer](00-bien-demarrer.md)
2. [Créer son premier thème complet](01-creer-premier-theme.md)
3. [Comprendre et écrire du CSS pour GNOME](02-css-debutant.md)
4. [Atelier pratique : GNOME Shell 51](03-atelier-gnome-shell.md)
5. [Atelier pratique : GTK 3 et GTK 4](04-atelier-gtk.md)
6. [Atelier pratique : Libadwaita](05-libadwaita.md)
7. [Créer et modifier les ressources visuelles](06-icones-curseurs-polices-fonds.md)
8. [Paramètres GNOME, installation et dépannage](07-parametres-installation-diagnostic.md)
9. [Catalogue pratique des composants](08-catalogue-pratique-composants.md)
10. [Personnaliser les applications GNOME](11-applications-gnome.md)
11. [Personnaliser le panneau supérieur](13-panneau-superieur-shell.md)
12. [Personnaliser la vue Activités](14-vue-activites-overview.md)
13. [Menus, réglages rapides, calendrier et notifications](15-menus-reglages-notifications.md)
14. [Écran de verrouillage, déverrouillage et GDM](16-ecran-verrouillage-gdm.md)
15. [OSD, dialogues, Alt-Tab et capture d'écran](17-osd-dialogues-alt-tab-capture.md)

## Captures de l'interface GNOME standard

- [Anatomie du panneau supérieur](https://help.gnome.org/gnome-help/figures/shell-top-bar.png)
- [Anatomie de la vue Activités](https://help.gnome.org/gnome-help/figures/shell-activities-dash.png)
- [Anatomie d'une application GNOME](https://release.gnome.org/49/assets/img/gnome49.png)
- [Menus et réglages rapides](https://help.gnome.org/gnome-help/figures/shell-exit.png)
- [Calendrier et notifications](https://help.gnome.org/gnome-help/figures/shell-appts.png)

Les visuels renvoient désormais aux captures officielles de GNOME Help et aux images de présentation GNOME. Ils montrent l'apparence standard ; certaines captures documentaires sont antérieures à GNOME 51 et servent à identifier les composants, pas à figer leurs dimensions.

## Compléments pédagogiques

- [Personnaliser les applications GNOME](11-applications-gnome.md)
- [Inspection et diagnostic CSS](12-inspection-et-diagnostic-css.md)
- [Panneau supérieur](13-panneau-superieur-shell.md)
- [Vue Activités](14-vue-activites-overview.md)
- [Menus, réglages rapides, calendrier et notifications](15-menus-reglages-notifications.md)

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

Lisez d'abord le parcours débutant. Réalisez les exercices dans un dossier de test et ne modifiez pas les fichiers système. Pour un composant précis, consultez son tutoriel, observez la capture, puis vérifiez le sélecteur dans les sources correspondant à la version utilisée.

Chaque exemple est un point de départ. Un sélecteur CSS peut être valide sans correspondre à un composant présent. Une application peut charger son propre style. Les extensions peuvent ajouter des widgets et le thème utilisateur ne contrôle pas tous les moteurs.

## Couverture et limites

Le manuel vise les familles de composants natifs documentées pour GNOME Shell 51, GTK 3, GTK 4 et Libadwaita, ainsi que les ressources visuelles et paramètres GNOME. Il ne peut pas garantir la modification de chaque widget personnalisé de chaque application tierce, ni des écrans système protégés. Ces limites sont identifiées plutôt que masquées.

## Formats exportés

Le PDF et l'EPUB sont générés à partir des chapitres Markdown et des captures officielles liées dans les chapitres. Après chaque modification, reconstruisez les deux formats et vérifiez que les schémas et exemples sont présents.
