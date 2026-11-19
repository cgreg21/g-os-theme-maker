# 9. Construction, installation et validation

## Périmètre réel d’un thème utilisateur

- L’écran GDM dépend du thème système de GDM et de sa configuration ; un thème utilisateur ne le remplace pas automatiquement.
- Les décorations de fenêtres dépendent du compositeur, de Mutter et des décorations côté client.
- Les applications Qt, Electron, web et toolkit propriétaires ont leurs propres moteurs.
- Les extensions GNOME Shell peuvent ajouter des widgets, menus et panneaux avec leurs propres classes.
- Les applications GTK peuvent ajouter des CSS providers et widgets personnalisés.
- Certains composants natifs utilisent des ressources, icônes ou rendus qui ne sont pas pilotés par CSS.

Ces cas doivent être indiqués comme « hors périmètre », « extension » ou « dépend de l’application », pas présentés comme une prise en charge garantie.

## 10. Structure d’un thème exporté

```text
MonTheme/
├── README.md
├── gnome-shell/
│   └── gnome-shell.css
├── gtk-3.0/
│   └── gtk.css
├── gtk-4.0/
│   └── gtk.css
├── libadwaita/
│   └── gtk-4.16.css
├── icons/MonTheme/
│   ├── index.theme
│   ├── scalable/apps/
│   ├── scalable/actions/
│   ├── scalable/devices/
│   ├── scalable/places/
│   └── scalable/status/
├── cursors/MonCurseur/
│   ├── index.theme
│   └── cursors/
├── backgrounds/
└── fonts/
```

Un répertoire vide n’est pas une ressource de thème terminée. L’export doit signaler clairement les ressources absentes.

## 11. Matrice de tests obligatoire

- **Zone** : Panneau ; **Contrôles minimum** : horloge, activités, indicateurs, confidentialité
- **Zone** : Activités ; **Contrôles minimum** : recherche, résultats, grille, dossiers, pages
- **Zone** : Dock ; **Contrôles minimum** : lancement, application active, séparateur, glisser-déposer
- **Zone** : Espaces ; **Contrôles minimum** : miniatures, sélection, aperçu de fenêtre
- **Zone** : Menus ; **Contrôles minimum** : menu simple, sous-menu, case, interrupteur, séparateur
- **Zone** : Réglages rapides ; **Contrôles minimum** : réseau, Bluetooth, son, luminosité, alimentation, périphériques
- **Zone** : Calendrier ; **Contrôles minimum** : mois, jour courant, événements, horloges, météo
- **Zone** : Notifications ; **Contrôles minimum** : carte, groupe, actions, média, ne pas déranger
- **Zone** : Dialogues ; **Contrôles minimum** : confirmation, erreur, mot de passe, polkit, fin de session
- **Zone** : Verrouillage ; **Contrôles minimum** : horloge, saisie, utilisateur, notifications
- **Zone** : Saisie ; **Contrôles minimum** : clavier virtuel, emoji, IBus, suggestions
- **Zone** : OSD ; **Contrôles minimum** : volume, luminosité, capture, sélection écran
- **Zone** : GTK 3 ; **Contrôles minimum** : fenêtre, headerbar, bouton, champ, liste, menu, arbre, onglet
- **Zone** : GTK 4 ; **Contrôles minimum** : fenêtre, headerbar, boutons, saisie, listes, popovers, défilement
- **Zone** : Libadwaita ; **Contrôles minimum** : navigation, préférences, lignes, dialogues, bannières, toasts
- **Zone** : Ressources ; **Contrôles minimum** : icônes manquantes, curseurs, polices, fonds
- **Zone** : Accessibilité ; **Contrôles minimum** : clavier, focus, contraste élevé, RTL, HiDPI

Tester chaque zone en clair, sombre et contraste élevé. Valider la syntaxe CSS avec les outils GTK correspondants et utiliser une session GNOME Shell imbriquée pour les tests Shell. Un aperçu statique ne remplace pas un test réel.

## Organiser un éditeur de thèmes

Le catalogue doit guider l’organisation de l’application :

1. **Cible** : Shell 51, GTK 3, GTK 4, Libadwaita, icônes, curseurs, polices, fonds.
2. **Écran** : choisir une zone d’interface dans la cible.
3. **Composant** : sélectionner le bouton, menu, carte, champ, ligne, etc.
4. **État** : normal, hover, focus, actif, sélectionné, désactivé, erreur.
5. **Propriétés** : couleurs, texte, bordure, rayon, taille, espacement, ombre.
6. **Aperçu** : montrer le composant et ses états, puis valider dans le moteur réel.
7. **Compatibilité** : afficher la version cible et les limites connues.

Ne pas présenter une propriété comme modifiable si le moteur ne l’expose pas. Les composants ajoutés par les extensions doivent être identifiés comme tels.

## 9.1 Installation utilisateur

Installer dans les répertoires XDG utilisateur : thèmes, icônes, curseurs, polices et fonds. Ne pas écrire dans `/usr/share` sans demande explicite et privilèges. Le paquet doit contenir nom, version, auteur, cibles, versions testées, variantes, ressources absentes, licences, installation, désinstallation et limites.

## 9.2 Validation

1. syntaxe CSS ;
2. correspondance sélecteurs/nœuds ;
3. rendu GTK 3, GTK 4 et Libadwaita ;
4. Shell 51 en session imbriquée puis réelle ;
5. régression clair/sombre/contraste, états, extensions, HiDPI, RTL ;
6. vérifier qu'aucune préférence ni fichier système non demandé n'a été modifié.

Un CSS qui se parse peut ne correspondre à aucun nœud. Un aperçu statique n'est pas un test moteur.

## 9.3 Diagnostic

```sh
gnome-shell --version
pkg-config --modversion gtk+-3.0 gtk4 libadwaita-1
gsettings list-schemas
gsettings list-recursively org.gnome.desktop.interface
gnome-extensions list
echo "$XDG_SESSION_TYPE"
echo "$XDG_CURRENT_DESKTOP"
```

Les commandes dépendent de la distribution.

## 9.4 Matrice de test

La matrice détaillée figure dans la section « Matrice de tests obligatoire » ci-dessus. Ne maintenez pas deux listes de tests différentes : utilisez une seule matrice comme référence.

## 9.5 Retour arrière

Sauvegarder le thème précédent, fournir désactivation/restauration, désinstaller uniquement les fichiers créés, préserver une session alternative. Ne pas réinitialiser toutes les préférences dconf. Toute cible système doit avoir une procédure de récupération.

## 9.6 Critères de prise en charge

Une cible n'est prise en charge que si moteur/version identifiés, propriétés et sélecteurs documentés, états et variantes testés, parseur sans erreur inexpliquée, installation/retour arrière vérifiés et limites visibles.
