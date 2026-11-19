# Concevoir un thème avec l'éditeur visuel G-OS Theme Maker

Ce chapitre explique comment passer d'une palette à un projet de thème exploitable avec l'application G-OS Theme Maker. Il décrit le fonctionnement réel de l'éditeur et distingue son aperçu GTK local de l'aperçu GNOME Shell imbriqué.

## 1. Comprendre les trois zones de l'application

L'interface actuelle est organisée en trois colonnes.

La colonne **Éléments** présente les familles de réglages et le bouton de lancement de Mutter imbriqué. Dans cette version, les entrées de bibliothèque affichées sont des repères d'interface : elles ne constituent pas encore un catalogue complet de widgets à glisser-déposer.

La zone **Aperçu des composants** est un aperçu GTK local. Elle contient une barre supérieure fictive, une carte, un bouton principal et un bouton secondaire. Ces éléments sont des widgets GTK construits par l'application. Ils servent à visualiser rapidement les tokens, mais ne sont pas une reproduction pixel-perfect de GNOME Shell.

La colonne **Inspecteur** permet de modifier les couleurs générales, le rayon, l'espacement et la taille de texte. Lorsqu'un composant sélectionnable est cliqué dans l'aperçu, l'inspecteur affiche aussi ses propriétés spécifiques.

## 2. Comprendre les tokens globaux

Le modèle de projet actuel expose les tokens suivants :

- `name` : nom du thème ;
- `background` : fond général ;
- `surface` : surface des composants ;
- `foreground` : texte principal ;
- `muted` : texte secondaire ;
- `accent` : couleur d'accent ;
- `border` : couleur de bordure ;
- `radius` : rayon commun ;
- `spacing` : espacement commun ;
- `font_size` : taille de texte ;
- `component_overrides` : réglages particuliers de certains composants.

Les valeurs initiales sont des valeurs de départ, pas une prescription esthétique. Le modèle vérifie le format des couleurs hexadécimales et borne les valeurs numériques : rayon entre 0 et 48, espacement entre 0 et 32 et taille de police entre 8 et 32.

Une valeur invalide empêche l'application du nouvel aperçu. Corrigez le champ avant de poursuivre l'édition.

## 3. Construire une palette cohérente

Commencez par le fond et la surface. Le fond doit séparer visuellement la fenêtre de travail ; la surface doit distinguer les cartes, menus et contrôles. Choisissez ensuite le texte principal et le texte secondaire.

La couleur secondaire doit rester lisible. Ne l'éclaircissez ou ne l'assombrissez pas uniquement pour obtenir un aspect discret : contrôlez-la sur chaque surface utilisée.

Enfin, choisissez l'accent. Il doit être suffisamment distinct du fond et de la surface pour signaler une action, une sélection ou un focus. Réservez-le aux éléments qui ont besoin d'attirer l'attention.

Méthode de travail :

1. régler le fond ;
2. régler la surface ;
3. régler le texte principal ;
4. régler le texte secondaire ;
5. régler l'accent ;
6. régler les bordures ;
7. vérifier les combinaisons dans l'aperçu ;
8. reprendre les contrastes avant de travailler les ombres ou les effets.

## 4. Régler les composants indépendamment

Cliquez directement sur un composant dans l'aperçu pour le sélectionner. Un contour indique l'élément sélectionné. Les réglages spécifiques sont enregistrés dans `component_overrides`.

Les composants actuellement reconnus par le modèle sont :

- `topbar` ;
- `card` ;
- `primary_button` ;
- `secondary_button`.

Les propriétés numériques spécifiques sont le rayon et l'espacement. Les couleurs spécifiques peuvent définir le fond, le texte, la bordure, le survol et l'état actif. Les propriétés affichées dépendent du composant sélectionné.

Un réglage de composant remplace le token global uniquement pour le composant concerné. Si une carte utilise un fond personnalisé, changer le token global `surface` ne doit pas être interprété comme une suppression de cette surcharge.

## 5. Comprendre les limites de l'aperçu GTK local

L'aperçu local utilise GTK 4 et un fournisseur CSS chargé dans le processus de l'éditeur. Il montre l'effet des principaux tokens sur les widgets de démonstration.

Il ne valide pas :

- les sélecteurs internes de GNOME Shell ;
- les composants de chaque application GTK ;
- les styles propres à Libadwaita ;
- le rendu sur toutes les distributions ;
- la compatibilité avec toutes les versions de GNOME.

Un bouton GTK local et un bouton dessiné par GNOME Shell ne sont pas le même widget. Le fait qu'ils aient un aspect similaire dans l'éditeur ne prouve pas que la feuille Shell les stylisera de la même manière.

## 6. Enregistrer un projet

Le projet est un document JSON versionné. Utilisez **Enregistrer** pour écrire le document sur disque. Si le projet n'a pas encore de chemin, l'application demande un emplacement.

Un projet contient la version du schéma et les tokens. Il ne contient pas une capture d'écran de l'aperçu ni une copie du thème GNOME installé.

Exemple simplifié de projet :

```json
{
  "schema_version": 1,
  "tokens": {
    "name": "Mon thème",
    "background": "#242424",
    "surface": "#303030",
    "foreground": "#f6f5f4",
    "muted": "#c0bfbc",
    "accent": "#3584e4",
    "border": "#454545",
    "radius": 12,
    "spacing": 8,
    "font_size": 14,
    "component_overrides": {}
  }
}
```

Conservez le fichier JSON comme source modifiable. Les feuilles CSS exportées sont des résultats générés : elles peuvent être recréées à partir du projet.

## 7. Enregistrer une méthode de travail reproductible

Pour éviter de perdre une direction visuelle :

1. enregistrez une première version du projet ;
2. faites une copie avant une modification importante ;
3. changez une famille de tokens à la fois ;
4. notez les valeurs qui donnent un résultat satisfaisant ;
5. vérifiez l'aperçu Shell imbriqué ;
6. exportez seulement après avoir contrôlé les deux aperçus ;
7. gardez le JSON avec les fichiers exportés.

Utilisez des noms explicites, par exemple `bleu-clair-v1.json` ou `sombre-contraste-eleve.json`. Évitez les noms génériques comme `final2.json`.

## 8. Exercice : créer une variante claire

1. Créez un nouveau projet.
2. Donnez-lui un nom distinctif.
3. Choisissez un fond gris très clair et une surface blanche.
4. Utilisez un texte principal sombre.
5. Choisissez un accent bleu.
6. Augmentez légèrement le rayon des cartes.
7. Sélectionnez la carte et modifiez son espacement sans changer les boutons.
8. Sélectionnez le bouton principal et donnez-lui un fond d'accent.
9. Enregistrez le projet.
10. Rouvrez le JSON et vérifiez que les surcharges sont bien conservées.

## 9. Exercice : créer une variante sombre

Dupliquez le projet précédent. Remplacez le fond, la surface, les textes, les bordures et l'accent par des valeurs conçues pour un environnement sombre. Ne vous contentez pas d'inverser chaque composante mathématiquement : le contraste perçu, les surfaces et les couleurs d'accent doivent être réévalués.

Vérifiez les textes secondaires et les bordures en priorité. Ce sont souvent les premiers éléments à devenir trop faibles dans une palette sombre.

## 10. Ce que l'éditeur ne génère pas encore

Le modèle et les exports actuels ne représentent pas un moteur de conception universel. Les surcharges sont limitées à quatre types de composants. Les ressources d'icônes, les curseurs et les fonds ne sont pas générés par le modèle de tokens actuel.

Le CSS exporté doit être relu et testé. Un fichier exporté n'est pas une garantie de compatibilité avec chaque version de GNOME, chaque application ou chaque extension.
