# 9. Construction, installation et validation

## Périmètre réel d’un thème utilisateur

- L’écran GDM dépend du thème système de GDM et de sa configuration ; un thème utilisateur ne le remplace pas automatiquement.
- Les décorations de fenêtres dépendent du compositeur, de Mutter et des décorations côté client.
- Les applications Qt, Electron, web et toolkit propriétaires ont leurs propres moteurs.
- Les extensions GNOME Shell peuvent ajouter des widgets, menus et panneaux avec leurs propres classes.
- Les applications GTK peuvent ajouter des CSS providers et widgets personnalisés.
- Certains composants natifs utilisent des ressources, icônes ou rendus qui ne sont pas pilotés par CSS.

Ces cas doivent être indiqués comme « hors périmètre », « extension » ou « dépend de l’application », pas présentés comme une prise en charge garantie.

## 2. Structure d’un thème exporté

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

## 3. Matrice de tests obligatoire

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

## 4. Délimiter la portée d’un thème

Avant de commencer un thème, établissez une fiche de périmètre :

1. **Moteur** : GNOME Shell 51, GTK 3, GTK 4 ou Libadwaita.
2. **Zone** : panneau, menu, dialogue, fenêtre, liste, champ ou ressource visuelle.
3. **Élément réel** : nœud, classe, widget ou fichier de ressource observé.
4. **États** : normal, survol, focus, actif, sélectionné, désactivé et erreur lorsqu’ils existent.
5. **Mécanisme** : CSS, préférence GSettings, extension, ressource ou configuration système.
6. **Limites** : version testée, composants privés, styles applicatifs et éléments non modifiables.

Ne promettez jamais un rendu si le moteur ne fournit pas le mécanisme nécessaire. Les composants ajoutés par les extensions doivent être distingués des composants natifs.

## 5. Installation utilisateur

Installer dans les répertoires XDG utilisateur : thèmes, icônes, curseurs, polices et fonds. Ne pas écrire dans `/usr/share` sans demande explicite et privilèges. Le paquet doit contenir nom, version, auteur, cibles, versions testées, variantes, ressources absentes, licences, installation, désinstallation et limites.

## 6. Validation

1. syntaxe CSS ;
2. correspondance sélecteurs/nœuds ;
3. rendu GTK 3, GTK 4 et Libadwaita ;
4. Shell 51 en session imbriquée puis réelle ;
5. régression clair/sombre/contraste, états, extensions, HiDPI, RTL ;
6. vérifier qu'aucune préférence ni fichier système non demandé n'a été modifié.

Un CSS qui se parse peut ne correspondre à aucun nœud. Un aperçu statique n'est pas un test moteur.

## 7. Diagnostic

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

## 8. Retour arrière

Sauvegarder le thème précédent, fournir désactivation/restauration, désinstaller uniquement les fichiers créés, préserver une session alternative. Ne pas réinitialiser toutes les préférences dconf. Toute cible système doit avoir une procédure de récupération.

## 9. Critères de prise en charge

Une cible n'est prise en charge que si moteur/version identifiés, propriétés et sélecteurs documentés, états et variantes testés, parseur sans erreur inexpliquée, installation/retour arrière vérifiés et limites visibles.


## 10. Préparer un environnement de validation isolé

Ne validez pas un thème expérimental directement dans votre session de travail principale. Une erreur dans le CSS de GNOME Shell peut rendre l'interface difficile à utiliser, et une modification des préférences peut contaminer les essais suivants.

Préparez au minimum :

- un compte utilisateur de test ou une machine virtuelle avec un instantané restaurable ;
- une session GNOME correspondant exactement à la version annoncée ;
- les versions de GTK et Libadwaita relevées avant les essais ;
- une copie du thème installé, identifiée par son empreinte ;
- une procédure de désactivation accessible sans dépendre du thème testé.

Consignez l'environnement avant chaque campagne :

```sh
{
  date --iso-8601=seconds
  gnome-shell --version
  printf 'Session : %s\n' "$XDG_SESSION_TYPE"
  printf 'Desktop : %s\n' "$XDG_CURRENT_DESKTOP"
  pkg-config --modversion gtk+-3.0 2>/dev/null || true
  pkg-config --modversion gtk4 2>/dev/null || true
  pkg-config --modversion libadwaita-1 2>/dev/null || true
  printf '\nExtensions :\n'
  gnome-extensions list --enabled
} | tee environnement-test.txt
```

Une version de bibliothèque absente doit être notée comme telle ; ne remplacez pas cette information par une version supposée.

## 11. Contrôler les feuilles CSS GTK

GTK 3 et GTK 4 ne sont pas interchangeables. Exécutez les outils avec le moteur correspondant et sur les fichiers réellement distribués.

Pour GTK 3, `gtk3-widget-factory` permet de parcourir de nombreux widgets standards. Pour GTK 4, utilisez `gtk4-widget-factory`. Selon la distribution, ces exécutables sont fournis dans des paquets de démonstration distincts.

```sh
command -v gtk3-widget-factory
command -v gtk4-widget-factory
```

Lancez les deux applications séparément et vérifiez les familles de contrôles prévues par votre thème. Ne concluez pas qu'un thème GTK 4 fonctionne parce qu'il est chargé par une application GTK 3, ou inversement.

Activez l'inspecteur GTK lorsque la version installée le permet :

```sh
GTK_DEBUG=interactive gtk3-widget-factory
GTK_DEBUG=interactive gtk4-widget-factory
```

Dans l'inspecteur, sélectionnez le widget, examinez sa hiérarchie, ses classes et les règles CSS appliquées. Relevez le nom du widget et ses classes avant d'écrire un sélecteur. Les noms internes peuvent changer entre versions : vérifiez-les dans le moteur réellement ciblé.

Pour une application précise, distinguez les règles du thème global de celles injectées par l'application. Si une application ajoute son propre fournisseur CSS, un thème global ne peut pas garantir le résultat sur toutes ses vues.

## 12. Vérifier Libadwaita séparément

Libadwaita possède ses propres conventions visuelles et composants. Testez une application Libadwaita réelle, ainsi que les widgets de démonstration disponibles dans la version installée.

```sh
pkg-config --modversion libadwaita-1
pkg-config --variable=libdir libadwaita-1
```

Vérifiez au minimum les pages de préférences, lignes de liste, barres de navigation, dialogues, bannières, toasts, boutons et champs. Observez les variantes claire et sombre, les états désactivés et le redimensionnement.

Ne supposez pas qu'une feuille GTK 4 générique remplace les styles internes de Libadwaita. Identifiez précisément le point d'extension supporté par la version ciblée et documentez les limites des applications qui imposent leur propre apparence.

## 13. Tester GNOME Shell sans risquer la session principale

Pour développer du CSS Shell, privilégiez une session imbriquée lorsque l'environnement le permet :

```sh
dbus-run-session -- gnome-shell --nested --wayland
```

Cette commande dépend de la prise en charge de la session imbriquée par la construction de GNOME Shell et le compositeur. Si elle échoue, relevez le message exact ; ne basculez pas aveuglément vers une commande qui remplace la session en cours.

Dans la session de test, vérifiez les zones de la matrice une par une. Ouvrez les menus, changez d'espace, lancez et fermez des applications, affichez les notifications, ouvrez le calendrier et testez les dialogues. Une zone masquée ou non ouverte pendant le test n'est pas validée.

Pour examiner les erreurs, consultez les journaux de la session de test :

```sh
journalctl --user -b --since "10 minutes ago"   | grep -Ei 'gnome-shell|stylesheet|css|st-theme|warning|error'
```

Le filtre peut masquer des messages utiles ou retourner des avertissements sans rapport. Relisez le contexte autour de chaque ligne et comparez avec une session sans le thème.

## 14. Construire une campagne de tests reproductible

Une campagne doit décrire une combinaison précise : version de GNOME, version des toolkits, session Wayland ou X11, thème actif, extensions activées, échelle d'affichage et variante de contraste.

Procédez dans cet ordre :

1. démarrez avec le thème par défaut et vérifiez que l'environnement est sain ;
2. activez uniquement le thème à tester ;
3. vérifiez les composants natifs avant les extensions ;
4. activez ensuite les extensions prises en charge, une par une ;
5. répétez les parcours en clair et sombre ;
6. testez le contraste renforcé, le focus clavier, le RTL et les facteurs d'échelle ;
7. désactivez le thème et vérifiez que le rendu par défaut revient ;
8. recommencez après une nouvelle connexion pour repérer les effets persistants.

Ne changez qu'une variable à la fois lorsqu'un défaut apparaît. Cette méthode permet de distinguer une régression du thème d'une incompatibilité d'extension, d'une différence de version ou d'une préférence utilisateur.

## 15. Consigner un défaut et le rendre reproductible

Chaque anomalie doit être accompagnée des informations nécessaires à sa reproduction :

- version exacte de GNOME Shell et des bibliothèques ;
- session Wayland ou X11 ;
- nom et version du thème ;
- extension concernée, si applicable ;
- chemin du composant et sélecteur CSS impliqué ;
- état de l'interface au moment du défaut ;
- étapes précises pour reproduire ;
- résultat attendu et résultat observé ;
- capture d'écran locale si elle apporte une information utile ;
- extrait de journal pertinent, expurgé de toute donnée personnelle.

Évitez les rapports vagues comme « le menu est cassé ». Préférez : « Dans GNOME Shell 51.x sous Wayland, ouvrir le menu système puis activer le sous-menu réseau : le texte de l'état connecté se superpose à l'icône ; le défaut disparaît lorsque la règle ... est désactivée. »

Classez les défauts par gravité : blocage de session ou perte de lisibilité, fonction inutilisable, défaut visuel gênant, puis différence cosmétique mineure. Corrigez d'abord les problèmes qui empêchent l'utilisation ou l'accès aux commandes.

## 16. Exemple de contrôle automatisé des fichiers livrés

Les contrôles statiques détectent les oublis évidents, mais ne valident ni le rendu ni la compatibilité des sélecteurs.

```sh
#!/usr/bin/env bash
set -euo pipefail

theme_dir="${1:?Usage: $0 repertoire-du-theme}"
test -d "$theme_dir"

for file in README.md LICENSE; do
  if [[ ! -s "$theme_dir/$file" ]]; then
    printf 'Fichier requis absent ou vide : %s\n' "$file" >&2
    exit 1
  fi
done

if find "$theme_dir" -type l -print -quit | grep -q .; then
  printf 'Liens symboliques présents : vérifier leur cible et leur portabilité.\n'
  find "$theme_dir" -type l -printf '%p -> %l\n'
fi

if find "$theme_dir" -type f \( -name '*.bak' -o -name '*.tmp' -o -name '*~' \) -print -quit | grep -q .; then
  printf 'Fichiers temporaires détectés.\n' >&2
  find "$theme_dir" -type f \( -name '*.bak' -o -name '*.tmp' -o -name '*~' \) -print
  exit 1
fi

printf 'Contrôles statiques terminés. Les tests visuels restent obligatoires.\n'
```

Adaptez les fichiers obligatoires aux composants réellement fournis. Ce script ne doit pas exiger un répertoire GTK, Shell ou d'icônes que le paquet ne prétend pas distribuer.

## 17. Décider si une version peut être publiée

Une version est publiable lorsque les composants annoncés ont été testés sur les versions indiquées, que les défauts bloquants sont corrigés ou explicitement signalés, que l'installation et le retour arrière fonctionnent, et que les ressources redistribuées sont accompagnées de leurs licences.

Un résultat « non testé » n'est pas un résultat positif. Conservez une liste des combinaisons non couvertes et évitez d'étendre la déclaration de compatibilité au-delà des essais réalisés.
