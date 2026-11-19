# 8. Accessibilité, mouvement, langue et densité

## États transversaux à tester

Un catalogue complet ne s’arrête pas à l’apparence normale. Pour chaque composant interactif, prévoir et tester :

- **État** : Normal ; **Description** : repos ; **Règle de conception** : lisible et équilibré
- **État** : Hover ; **Description** : pointeur au-dessus ; **Règle de conception** : différence visible mais discrète
- **État** : Focus ; **Description** : navigation clavier ; **Règle de conception** : contour visible, jamais supprimé sans remplacement
- **État** : Active / pressed ; **Description** : action en cours ; **Règle de conception** : retour visuel immédiat
- **État** : Checked / selected ; **Description** : sélection persistante ; **Règle de conception** : contraste et indicateur explicite
- **État** : Disabled / insensitive ; **Description** : indisponible ; **Règle de conception** : contraste réduit mais texte encore compréhensible
- **État** : Backdrop / inactive ; **Description** : fenêtre inactive ; **Règle de conception** : hiérarchie visuelle conservée
- **État** : Expanded / collapsed ; **Description** : panneau ouvert/fermé ; **Règle de conception** : état identifiable
- **État** : Error ; **Description** : saisie invalide ; **Règle de conception** : couleur + indication non chromatique
- **État** : Warning ; **Description** : avertissement ; **Règle de conception** : distinction du message d’erreur
- **État** : Loading ; **Description** : chargement ; **Règle de conception** : spinner ou progression
- **État** : Empty ; **Description** : aucune donnée ; **Règle de conception** : état vide lisible
- **État** : Drag source / drop target ; **Description** : glisser-déposer ; **Règle de conception** : source, cible et emplacement visibles
- **État** : High contrast ; **Description** : contraste renforcé ; **Règle de conception** : contours, icônes et textes robustes

Prévoir aussi les directions LTR/RTL, les échelles HiDPI, les tailles de texte, la navigation clavier et les préférences de réduction des animations.

## Variantes visuelles

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


## 8.7 Mesurer le contraste avec une méthode reproductible

Le contraste doit être mesuré entre les couleurs réellement affichées, pas seulement entre les deux couleurs principales de la palette. Vérifiez notamment :

- texte et surface derrière le texte ;
- texte secondaire et surface ;
- icône informative et surface ;
- bordure d'un champ et surface adjacente ;
- indicateur de sélection et éléments voisins ;
- contour de focus et surfaces qu'il traverse ;
- états survolé, désactivé, erreur et avertissement.

Pour une vérification de référence WCAG, les seuils AA usuels sont de 4,5:1 pour le texte courant et de 3:1 pour le grand texte. Les composants d'interface et les informations graphiques nécessaires à la compréhension ont également un seuil de 3:1 par rapport aux couleurs adjacentes. Les critères ont des exceptions et des définitions précises : ne réduisez pas l'audit à une seule valeur de contraste.

La formule utilise la luminance relative sRGB. Le calcul ci-dessous permet de contrôler deux couleurs hexadécimales sans installer de bibliothèque :

```python
def luminance(hex_color):
    value = hex_color.lstrip("#")
    if len(value) != 6:
        raise ValueError("Utiliser une couleur #RRGGBB")
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [
        channel / 12.92 if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return (
        0.2126 * linear[0]
        + 0.7152 * linear[1]
        + 0.0722 * linear[2]
    )

def contrast_ratio(color_a, color_b):
    first, second = sorted(
        (luminance(color_a), luminance(color_b)),
        reverse=True,
    )
    return (first + 0.05) / (second + 0.05)

print(f"{contrast_ratio('#FFFFFF', '#242424'):.2f}:1")
```

Enregistrez le résultat avec les deux couleurs, le rôle du composant, la variante testée et le seuil visé. Le calcul ne remplace pas l'inspection visuelle : transparence, opacité, images, dégradés et superpositions peuvent modifier les couleurs réellement perçues. Mesurez alors la couleur composée sur la surface effective.

Ne choisissez pas une couleur de focus uniquement parce qu'elle contraste avec le fond principal. Elle doit rester visible sur chaque surface traversée par le contour.

## 8.8 Contrôler les préférences d'accessibilité de la session

Les noms de schémas et les clés disponibles dépendent de la version installée et des composants présents. Commencez par inventorier les préférences réellement exposées :

```sh
gsettings list-schemas | grep -E 'a11y|interface|wm'
gsettings list-recursively org.gnome.desktop.a11y
gsettings list-recursively org.gnome.desktop.interface
```

Une commande peut afficher beaucoup de réglages ou signaler qu'un schéma précis n'existe pas. Ne copiez pas une clé trouvée sur une autre version sans vérifier sa présence avec `gsettings list-keys NOM_DU_SCHEMA`.

Dans les paramètres GNOME, activez les options d'accessibilité utiles à votre campagne : contraste renforcé, agrandissement, clavier visuel, navigation clavier et réduction des animations lorsqu'elles sont proposées. Les intitulés et la disponibilité peuvent varier avec la distribution.

Relevez l'état initial avant de modifier une préférence. Pour restaurer une valeur, réutilisez la valeur relevée et non une valeur par défaut supposée. Les préférences d'accessibilité appartiennent à l'environnement de test : un thème ne doit pas les modifier silencieusement.

## 8.9 Tester le focus sans souris

Effectuez une passe clavier complète sur chaque famille de composants :

1. ouvrez l'application ou le menu sans utiliser la souris ;
2. parcourez les éléments avec Tab et Maj+Tab ;
3. vérifiez que le focus est toujours visible et qu'il suit un ordre compréhensible ;
4. activez un bouton avec Entrée ou Espace selon son comportement ;
5. ouvrez et fermez un menu avec les commandes clavier prévues ;
6. vérifiez que Échap ferme le niveau courant sans perdre le contexte ;
7. parcourez les éléments d'une liste et les contrôles d'un dialogue ;
8. vérifiez que le focus ne disparaît pas derrière une fenêtre ou un popover ;
9. répétez dans les variantes claire, sombre et contraste élevé.

Ne remplacez pas le contour de focus par une simple différence de couleur trop faible. Le focus doit être distinguable du survol et de la sélection persistante. Si le composant ne reçoit pas le focus, recherchez d'abord un défaut de comportement ou d'accessibilité : une règle CSS ne peut pas rendre navigable un élément qui ne l'est pas.

## 8.10 Tester le lecteur d'écran et les informations non visuelles

Le thème agit sur la présentation, pas sur la plupart des informations sémantiques. Pour contrôler ce que reçoit un lecteur d'écran, testez les applications avec Orca lorsqu'il est disponible :

```sh
orca --version
```

Démarrez ensuite Orca depuis les outils d'accessibilité de GNOME ou selon la procédure de votre distribution. Parcourez les mêmes écrans que lors du test clavier et vérifiez que les contrôles possèdent un nom, un rôle, un état et une description compréhensibles.

Contrôlez particulièrement :

- boutons dont l'icône est le seul contenu visible ;
- champs avec indication d'erreur ;
- cases à cocher et interrupteurs ;
- éléments sélectionnés dans une liste ;
- notifications et dialogues ;
- changements d'état qui ne sont pas annoncés visuellement par du texte.

Si une information manque dans l'arbre d'accessibilité, signalez un défaut du widget, de l'application ou de l'extension. N'ajoutez pas une règle CSS pour tenter de corriger un problème sémantique.

## 8.11 Réduction des animations : vérifier le comportement réel

Une animation décorative peut provoquer une gêne ou masquer une information si elle est trop rapide, répétée ou indispensable à la compréhension. Pour chaque transition, identifiez :

- ce qui change et pourquoi ;
- sa durée et sa répétition ;
- si l'information reste compréhensible sans mouvement ;
- si le mouvement peut être réduit ou supprimé ;
- si l'état final reste visible après l'animation.

Testez la préférence de réduction des animations depuis les paramètres GNOME, puis répétez exactement la même séquence. Ne vous contentez pas de vérifier qu'une préférence existe : observez le Shell et les applications, car chaque composant doit la prendre en charge. N'importez pas automatiquement la syntaxe web `prefers-reduced-motion` dans les feuilles GTK ou St.

Une animation ne doit pas être le seul moyen de signaler une erreur, une progression ou une modification d'état. Fournissez également une différence visuelle stable et, lorsque nécessaire, une information textuelle accessible.

## 8.12 Direction du texte et contenu long

Pour vérifier une interface droite-à-gauche, utilisez une session ou une application configurée dans une langue RTL et contrôlez les composants réellement concernés. Ne vous contentez pas de retourner horizontalement une capture.

Vérifiez :

- alignement du texte et position des libellés ;
- marges et espacements logiques ;
- ordre des boutons d'action ;
- sens des icônes précédent/suivant et retour/avance ;
- placement des menus et popovers ;
- troncature et retour à la ligne ;
- chiffres, dates, ponctuation et texte mêlant plusieurs directions.

Une icône représentant un objet ou une action non directionnelle ne doit pas être retournée automatiquement. Les propriétés physiques gauche/droite peuvent créer des défauts en RTL ; privilégiez les propriétés logiques lorsque le moteur les prend en charge et vérifiez leur disponibilité dans la version ciblée.

## 8.13 Densité, agrandissement et zones interactives

La densité compacte concerne l'espacement visuel, pas la suppression des zones nécessaires à l'interaction. Testez le thème avec un texte agrandi et une échelle d'affichage différente. Contrôlez que :

- les libellés ne se chevauchent pas ;
- les boutons ne coupent pas leur texte ;
- les champs restent utilisables ;
- les menus ne sortent pas de l'écran ;
- les zones de clic et de focus restent suffisamment grandes ;
- les icônes ne deviennent pas floues ;
- les curseurs gardent un hotspot cohérent ;
- les fenêtres et dialogues restent accessibles sur un écran de faible hauteur.

Ne fixez pas des hauteurs rigides qui supposent une police et une langue uniques. Les libellés traduits peuvent être nettement plus longs que les libellés français ou anglais utilisés pendant le développement.

## 8.14 Distinguer ce que le thème peut corriger

Un thème peut améliorer les couleurs, les bordures, la lisibilité, la hiérarchie et la visibilité des états. Il ne peut pas, à lui seul :

- ajouter un nom accessible à un bouton sans libellé ;
- rendre un contrôle non focalisable accessible au clavier ;
- modifier l'ordre de navigation défini par l'application ;
- corriger un rôle ou un état absent de l'arbre d'accessibilité ;
- garantir qu'une notification soit annoncée par un lecteur d'écran ;
- modifier le comportement d'une application qui dessine ses propres composants ;
- remplacer une préférence d'accessibilité ou un service système.

Classez ces problèmes comme défauts de l'application, du widget, de l'extension ou de la session. Cette distinction évite de promettre une correction CSS impossible et permet de signaler le problème au bon projet.

## 8.15 Fiche de validation accessibilité

Pour chaque version publiée, conservez un compte rendu reproductible avec :

- versions GNOME Shell, GTK et Libadwaita ;
- session Wayland ou X11 et distribution ;
- variante claire, sombre ou contraste élevé ;
- échelle d'affichage et facteur de texte ;
- langue et direction du texte ;
- extensions et applications testées ;
- mesures de contraste avec couleurs et seuils ;
- composants testés au clavier ;
- résultat avec lecteur d'écran ;
- résultat avec réduction des animations ;
- défauts observés, contournements et limites.

Un test non effectué doit être marqué « non testé ». Ne le transformez pas en résultat positif parce que le composant semble visuellement correct.

## Références complémentaires

- [WCAG 2.2 — contraste minimum (1.4.3)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [WCAG 2.2 — contraste des composants non textuels (1.4.11)](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)
- [WCAG 2.2 — apparence du focus (2.4.13)](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html)
- [GNOME — Accessibilité](https://help.gnome.org/users/gnome-help/stable/a11y.html)
- [Orca — lecteur d'écran GNOME](https://help.gnome.org/users/orca/stable/)
