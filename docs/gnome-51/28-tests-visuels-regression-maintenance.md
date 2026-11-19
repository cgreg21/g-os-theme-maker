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
