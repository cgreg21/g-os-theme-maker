# Tests visuels, régressions et maintenance d’un thème

Un thème ne peut pas être déclaré compatible parce que son CSS se compile ou parce qu’une capture d’écran paraît correcte. Il faut tester le moteur réel, les états interactifs et les variantes d’affichage. Ce chapitre fournit une méthode reproductible pour les projets personnels et les thèmes distribués.

## 1. Fixer un environnement de référence

Avant chaque série de tests, consignez :

- version exacte de GNOME Shell ;
- versions de GTK 3, GTK 4 et Libadwaita ;
- distribution et session (Wayland ou X11) ;
- résolution, facteur d’échelle et nombre d’écrans ;
- langue et direction d’écriture ;
- mode clair/sombre et contraste ;
- extensions activées ;
- version du thème testé.

Sans ces informations, deux captures ne sont pas comparables.

## 2. Préparer une session de test

Préférez une machine virtuelle ou un utilisateur de test. Gardez une session de secours qui n’utilise pas le thème en cours de modification.

Testez dans cet ordre :
1. Shell seul, sans extension tierce ;
2. Shell avec les extensions réellement prises en charge ;
3. applications GTK 3 ;
4. applications GTK 4 ;
5. applications Libadwaita ;
6. ressources : icônes, curseurs, polices et fonds.

Une extension peut ajouter ses propres acteurs et styles. Notez-la comme dépendance au lieu d’attribuer ses effets au thème de base.

## 3. Vérifier la syntaxe sans confondre compilation et rendu

Pour les sources SCSS du thème amont, compilez avec les outils déclarés par la version de GNOME ciblée. Pour GTK, lancez une application de test et observez les avertissements CSS. Pour Shell, chargez le thème dans une session de test et inspectez les erreurs du journal.

Commandes de diagnostic :

    journalctl --user -b | grep -Ei 'gnome-shell|gtk|css|sass'
    gnome-shell --version
    pkg-config --modversion gtk+-3.0 gtk4 libadwaita-1

Une feuille peut être syntaxiquement correcte tout en ne correspondant à aucun nœud. Le test visuel et l’inspection restent indispensables.

## 4. Construire un jeu de captures reproductible

Pour chaque zone importante, gardez une capture de référence et une capture du thème candidat. Utilisez toujours :
- la même résolution et le même facteur d’échelle ;
- la même langue et les mêmes données de démonstration ;
- le même état (menu ouvert, fenêtre inactive, recherche vide, etc.) ;
- le même fond et les mêmes applications ;
- la même variante de couleur.

N’incluez pas d’informations personnelles dans les captures publiées. Les captures de référence doivent être stockées dans un dossier de test distinct des ressources du thème distribué.

## 5. Comparer les images

Une comparaison pixel à pixel révèle les différences exactes, mais signale aussi les variations d’anticrénelage, d’horloge et de contenu dynamique. Pour une première comparaison locale avec ImageMagick :

    compare reference.png candidate.png diff.png

Examinez toujours le résultat. Ne masquez pas une différence importante en augmentant simplement la tolérance. Excluez ou stabilisez les zones dynamiques (heure, notifications, contenu réseau) avant la capture.

Pour les changements de rendu importants, conservez une comparaison avant/après et expliquez la différence attendue dans le journal de modifications.

## 6. Matrice de validation minimale

Vérifiez chaque famille de composants dans les situations suivantes :

- repos, survol, focus clavier, pressé, sélectionné et désactivé ;
- menu ouvert, sous-menu, élément avec icône, séparateur et infobulle ;
- contenu vide, long, tronqué, erreur et chargement ;
- fenêtre active et inactive ;
- clair, sombre et contraste élevé ;
- LTR et RTL ;
- échelle standard et HiDPI ;
- un écran et plusieurs écrans ;
- avec et sans extensions prises en charge.

Pour les composants sensibles, ajoutez les cas de verrouillage, authentification, capture, partage d’écran et enregistrement. Ne masquez jamais les indicateurs de confidentialité.

## 7. Automatiser ce qui est fiable

Une intégration continue peut vérifier :
- présence des fichiers attendus ;
- validité de la structure du thème ;
- compilation SCSS avec la version de compilateur prévue ;
- absence de chemins de ressources cassés ;
- présence et validité des fichiers `index.theme` annoncés ;
- absence de fichiers vides ou temporaires ;
- cohérence des métadonnées et licences ;
- génération du PDF et de l’EPUB.

Séparez les vérifications rapides des validations qui nécessitent une session graphique. Une vérification de structure ne doit pas être présentée comme un test de rendu. Si la compilation dépend d'un outil externe, épinglez ou documentez sa version : un résultat peut changer lorsque l'environnement de CI évolue.

Pour les tests visuels automatisés, construisez une image d'environnement contrôlée et consignez le serveur d'affichage, le pilote, la résolution, les polices et les versions des composants. Le test doit échouer si la capture attendue n'a pas été produite : une capture absente ne doit jamais être interprétée comme une comparaison réussie.

La CI ne prouve pas que le rendu est correct. Les tests graphiques dépendent d'un environnement GNOME contrôlé et doivent être identifiés comme tests d'intégration visuelle, pas comme simples tests unitaires. Gardez une validation humaine pour les différences de contraste, de hiérarchie, d'alignement et de lisibilité.

## 8. Gérer la compatibilité par version

Chaque publication doit indiquer clairement :
- versions GNOME Shell testées ;
- versions GTK 3, GTK 4 et Libadwaita testées ;
- extensions compatibles ;
- composants partiellement pris en charge ;
- composants non pris en charge ;
- défauts connus ;
- date et environnement des derniers tests.

Quand un thème cible plusieurs versions, conservez des branches ou des feuilles distinctes si les sélecteurs divergent. Ne multipliez pas les sélecteurs spéculatifs pour faire croire à une compatibilité universelle.

## 9. Procédure de livraison et critères d'acceptation

Avant publication :
1. nettoyer les règles mortes et commenter les exceptions nécessaires ;
2. vérifier les licences de chaque ressource ;
3. reconstruire les formats distribués depuis les sources versionnées ;
4. installer le paquet dans un compte vierge ou un instantané propre ;
5. tester l'installation, la mise à jour et la désinstallation ;
6. vérifier le retour arrière depuis les préférences réellement utilisées ;
7. archiver les captures de référence et les différences significatives ;
8. rédiger les limites, dépendances et le journal des changements ;
9. vérifier l'archive finale et son contenu avant de la publier.

La livraison doit répondre à des critères vérifiables : le paquet s'installe sans privilèges inattendus, chaque famille annoncée possède les fichiers nécessaires, les préférences peuvent être restaurées, les composants non pris en charge sont explicitement signalés et les captures correspondent à la version livrée.

Testez aussi une mise à jour depuis la version précédente. Une installation neuve ne révèle pas les anciens fichiers devenus obsolètes. Vérifiez que la procédure de mise à jour ne laisse pas de sélecteurs périmés, d'icônes supprimées ou de ressources non référencées.

Un thème prêt à publier doit être reproductible, réversible et documenté. La qualité visuelle ne compense pas une procédure de désinstallation dangereuse.

## 10. Références

- [GNOME Shell 51 — sources du thème](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass)
- [GTK 3 — CSS](https://docs.gtk.org/gtk3/css-overview.html)
- [GTK 4 — CSS](https://docs.gtk.org/gtk4/css-overview.html)
- [Libadwaita — apparence](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)
- [GNOME User Documentation 51 — captures](https://github.com/GNOME/gnome-user-docs/tree/gnome-51/gnome-help/C/figures)


## 11. Définir un protocole de capture stable

Une comparaison n'est utile que si les deux images représentent le même état. Avant de capturer, fixez un protocole écrit et réutilisable :

1. Démarrez la même version de GNOME et la même session.
2. Définissez la même résolution, la même échelle et la même disposition des écrans.
3. Choisissez la même langue, le même format horaire et les mêmes paramètres d'accessibilité.
4. Désactivez les notifications non nécessaires et attendez la fin des animations.
5. Ouvrez la même application et le même écran, avec les mêmes données de démonstration.
6. Placez le pointeur au même endroit ou hors de la zone comparée.
7. Déclenchez explicitement l'état à capturer : repos, survol, focus, menu ouvert, dialogue, etc.
8. Enregistrez la capture sans la redimensionner ni la recomprimer.

Le nom du fichier doit identifier au minimum le composant, l'état, la version GNOME et la variante du thème. Par exemple :

```text
panel-overview-dark-gnome51-reference.png
panel-overview-dark-gnome51-candidate.png
```

Conservez à côté de chaque jeu de captures un fichier texte décrivant l'environnement. N'utilisez pas la date et l'heure dans le nom comme seul identifiant : elles ne permettent pas de retrouver les paramètres de la session.

### Éliminer les sources de bruit

Les horloges, animations, curseurs clignotants, notifications, contenus réseau et indicateurs matériels peuvent varier entre deux captures. Ne les masquez pas automatiquement. Déterminez d'abord s'ils font partie du composant testé.

Si un élément dynamique ne fait pas partie du test, stabilisez-le dans l'environnement de démonstration ou excluez une zone précisément documentée de la comparaison. Gardez une capture complète pour vérifier que l'exclusion ne cache pas un défaut réel.

Une zone masquée pour le calcul ne doit jamais être considérée comme validée visuellement.

## 12. Organiser les références et les résultats

Séparez les images de référence approuvées des résultats générés par chaque campagne :

```text
tests/
  visuels/
    environnement.txt
    references/
      panel/
      overview/
      calendar/
      menus/
    campagnes/
      2026-11-19/
        captures/
        differences/
        rapport.md
```

Ce dossier est un exemple d'organisation de projet ; adaptez-le au dépôt du thème. Les captures contenant des noms, événements, notifications ou chemins personnels ne doivent pas être versionnées.

Une référence approuvée ne doit pas être remplacée automatiquement par la capture du candidat. Lorsqu'un changement visuel est volontaire :
- décrivez le changement attendu ;
- comparez les captures avant et après ;
- vérifiez les états voisins ;
- faites approuver la nouvelle référence ;
- conservez l'historique de la décision.

Cette règle empêche une régression de devenir la nouvelle référence simplement parce qu'un test a été relancé.

## 13. Produire une différence avec ImageMagick

Vérifiez d'abord que les images ont les mêmes dimensions et le même espace colorimétrique :

```sh
identify -format '%f : %wx%h %[colorspace]\\n' reference.png candidate.png
```

Si les dimensions diffèrent, ne redimensionnez pas silencieusement une capture pour faire disparaître le problème. Recommencez la capture dans le bon environnement ou documentez pourquoi les dimensions sont volontairement différentes.

Pour produire une image qui met en évidence les pixels différents :

```sh
magick compare reference.png candidate.png difference.png
```

Pour mesurer le nombre de pixels différents :

```sh
magick compare -metric AE reference.png candidate.png null:
```

ImageMagick peut retourner un code différent de zéro lorsque des différences sont détectées. Dans un script de test, distinguez donc explicitement « différence trouvée » de « outil en erreur ». Ne transformez pas toute sortie non nulle en échec de l'outil, ni toute sortie nulle en preuve de qualité visuelle.

Une différence pixel à pixel est très sensible à l'anticrénelage, aux polices, aux pilotes graphiques et aux variations de rendu. Elle sert à localiser une variation, pas à décider seule si cette variation est une régression.

### Examiner une région précise

Pour isoler une zone, utilisez une région de même position et de mêmes dimensions sur les deux images. Notez les coordonnées et la raison de l'exclusion dans le rapport. Gardez toujours les originaux complets.

Ne comparez pas une zone recadrée à une référence différente sans conserver la correspondance avec l'image complète. Un décalage de quelques pixels peut faire apparaître toute une bordure comme différente.

## 14. Distinguer régression, changement attendu et bruit de rendu

Pour chaque différence, classez le constat avant de modifier le CSS :

- **Régression fonctionnelle** : un contrôle disparaît, devient inaccessible ou ne répond plus.
- **Régression de lisibilité** : contraste, taille de texte, focus ou hiérarchie visuelle dégradés.
- **Régression géométrique** : chevauchement, décalage, découpe ou zone interactive déplacée.
- **Changement attendu** : différence décrite dans la demande et validée dans les états voisins.
- **Bruit de rendu** : variation d'anticrénelage ou de contenu dynamique sans changement perceptible du composant.
- **Résultat indéterminé** : environnement ou référence insuffisamment contrôlé.

Ne classez pas une différence comme bruit simplement parce qu'elle est petite. Une modification d'un pixel peut être importante sur un indicateur de focus ou une icône de confidentialité.

Pour les polices, vérifiez d'abord que les mêmes fichiers de police et les mêmes versions sont utilisés. Pour les icônes, vérifiez le thème d'icônes et les ressources réellement chargées. Pour les couleurs, vérifiez le profil d'écran et la chaîne de capture avant de modifier les valeurs CSS.

## 15. Tester les états interactifs séparément

Une capture du composant au repos ne valide pas son comportement. Pour chaque famille, créez des captures séparées :

- repos ;
- survol souris ;
- focus clavier ;
- activation ou pression ;
- sélection persistante ;
- état désactivé ;
- chargement ;
- erreur ;
- contenu long ou tronqué ;
- dialogue ou menu associé.

Pour un bouton, vérifiez que le focus clavier reste identifiable sans souris. Pour un menu, vérifiez les éléments actifs, séparateurs, sous-menus et éléments désactivés. Pour un champ, vérifiez le texte saisi, le curseur, la sélection, l'indication d'erreur et le texte d'aide.

Les états qui ne peuvent pas être déclenchés dans l'environnement de test doivent être marqués « non testés ». Ne remplacez pas cette mention par une supposition fondée sur le CSS.

## 16. Vérifier la géométrie et l'accessibilité

En complément de la comparaison d'images, vérifiez les dimensions et le comportement :

- le texte ne déborde pas de son conteneur ;
- les boutons ne se recouvrent pas ;
- les libellés longs restent compréhensibles ;
- le focus clavier est visible sur chaque fond ;
- les zones interactives restent utilisables ;
- les indicateurs ne reposent pas uniquement sur la couleur ;
- le zoom et les grandes tailles de texte ne coupent pas le contenu ;
- les langues RTL ne provoquent pas d'inversion incohérente ;
- les animations peuvent être réduites lorsque l'environnement le demande.

La capture ne permet pas de mesurer à elle seule la zone réellement interactive ni de confirmer l'ordre de navigation clavier. Complétez-la par un test manuel au clavier et, lorsque disponible, par les outils d'accessibilité du toolkit.

N'utilisez pas une valeur de contraste calculée sur une capture compressée comme unique preuve de conformité. Mesurez les couleurs sources et vérifiez le rendu réel.

## 17. Construire une campagne de régression après modification

Après chaque changement CSS, identifiez les composants directement ciblés et ceux qui partagent les mêmes règles. Une modification de `button`, `.view`, `label` ou d'une classe de base peut toucher beaucoup plus d'écrans que prévu.

Procédez ainsi :

1. Listez les sélecteurs modifiés.
2. Recherchez les autres composants qui utilisent ces sélecteurs ou leurs parents.
3. Associez à chaque sélecteur les états interactifs à retester.
4. Capturez les composants directement modifiés.
5. Capturez au moins un composant voisin qui partage la règle.
6. Testez les variantes clair/sombre et les tailles d'écran pertinentes.
7. Examinez les journaux pour détecter les erreurs de chargement.
8. Archivez les différences et leur classification.

Une correction ciblée doit réduire la portée de la modification, pas seulement rendre la capture principale plus jolie.

## 18. Exemple de script de comparaison prudent

Le script suivant compare deux fichiers déjà capturés. Il vérifie leur existence et leurs dimensions, puis produit une image de différence. Il ne décide pas si la différence est acceptable : cette décision reste documentée dans le rapport.

```sh
#!/usr/bin/env bash
set -eu

reference=${1:?Usage: compare.sh reference.png candidate.png output.png}
candidate=${2:?Usage: compare.sh reference.png candidate.png output.png}
output=${3:?Usage: compare.sh reference.png candidate.png output.png}

for file in "$reference" "$candidate"; do
  if [ ! -s "$file" ]; then
    printf 'Fichier absent ou vide : %s\\n' "$file" >&2
    exit 2
  fi
done

ref_size=$(identify -format '%wx%h' "$reference")
candidate_size=$(identify -format '%wx%h' "$candidate")

if [ "$ref_size" != "$candidate_size" ]; then
  printf 'Dimensions incompatibles : référence=%s candidat=%s\\n' \\
    "$ref_size" "$candidate_size" >&2
  exit 2
fi

magick compare "$reference" "$candidate" "$output"
printf 'Différence enregistrée dans %s\\n' "$output"
```

Le code de sortie de `magick compare` peut signaler qu'une différence existe. Si vous l'intégrez à une CI, traitez séparément les erreurs d'exécution et les différences visuelles, puis publiez l'image de différence comme artefact. Une différence détectée ne doit pas être acceptée ou rejetée sans règle explicite et revue humaine.

## 19. Modèle de rapport de régression visuelle

Copiez ce modèle dans le dossier de la campagne :

```text
Campagne :
Date :
Thème et commit :
GNOME Shell :
GTK 3 / GTK 4 / Libadwaita :
Distribution :
Session : Wayland / X11
Résolution et échelle :
Moniteurs :
Langue et direction :
Mode clair/sombre :
Polices et thème d'icônes :
Composant :
État testé :
Référence utilisée :
Capture candidate :
Image de différence :
Différence observée :
Classification :
Impact fonctionnel :
Impact accessibilité :
États voisins vérifiés :
Décision : accepté / corrigé / à investiguer / non testé
Justification :
Validateur :
```

Un rapport sans environnement, référence et état testé n'est pas suffisamment reproductible pour servir de preuve de compatibilité.

## 20. Maintenir les tests au fil des versions

Lorsqu'une version de GNOME, GTK, Libadwaita ou du thème d'icônes change, ne réutilisez pas automatiquement toutes les références précédentes.

Pour chaque mise à niveau :
- recréez l'environnement de test ;
- vérifiez les sélecteurs et les widgets inspectés ;
- identifiez les changements de polices et de rendu ;
- exécutez la campagne de captures ;
- comparez les résultats avec les références de la version précédente ;
- approuvez de nouvelles références uniquement après revue ;
- mettez à jour les versions réellement testées dans la documentation du thème.

Gardez les anciennes références lorsqu'elles servent à expliquer une évolution. Associez-les à leur version exacte plutôt que de les mélanger avec les captures actuelles.

La maintenance visuelle est une activité continue : un thème qui fonctionne aujourd'hui peut perdre des sélecteurs, des espacements ou des états lors d'une mise à niveau du bureau. Une campagne courte et reproductible à chaque changement vaut mieux qu'une vérification générale occasionnelle.
