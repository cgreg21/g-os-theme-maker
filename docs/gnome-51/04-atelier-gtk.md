# Atelier pratique : GTK 3 et GTK 4

GTK fournit les composants utilisés par de nombreuses applications : boutons, champs, listes, menus, barres de défilement, dialogues et fenêtres. GTK 3 et GTK 4 ont des moteurs CSS différents. Un thème doit fournir une feuille adaptée à chaque version.

## 1. Identifier GTK

Pour connaître les bibliothèques installées :

```sh
pkg-config --modversion gtk+-3.0
pkg-config --modversion gtk4
```

Ces commandes donnent les versions disponibles sur le système, pas nécessairement la bibliothèque utilisée par une application précise. Une application peut également embarquer ou isoler des ressources.

## 2. Fenêtres et surfaces

GTK 3 :

```css
window,
.background {
  background-color: #242424;
  color: #f6f5f4;
}

headerbar {
  background-color: #303030;
  color: #f6f5f4;
  border-bottom: 1px solid #555555;
}
```

GTK 4 :

```css
window,
.background {
  background-color: #242424;
  color: #f6f5f4;
}

headerbar {
  background-color: #303030;
  color: #f6f5f4;
  border-bottom: 1px solid #555555;
}
```

Ces exemples sont volontairement simples. Une application peut utiliser une décoration côté client, une barre d'en-tête personnalisée ou Libadwaita. Inspectez l'arbre réel avant de conclure que le sélecteur est ignoré.

## 3. Boutons et boutons d'action

```css
button {
  color: #f6f5f4;
  background-color: #3b3b3b;
  border: 1px solid #555555;
  border-radius: 8px;
  padding: 7px 12px;
}

button:hover {
  background-color: #484848;
}

button:active {
  background-color: #202020;
}

button:disabled {
  opacity: 0.55;
}

button.suggested-action {
  color: #ffffff;
  background-color: #3584e4;
}

button.destructive-action {
  color: #ffffff;
  background-color: #c01c28;
}
```

Les classes d'action peuvent être ajoutées par le widget ou l'application. Testez un bouton ordinaire, un bouton principal, une action destructive, un bouton avec icône et un bouton uniquement textuel.

## 4. Champs de saisie

```css
entry {
  color: #f6f5f4;
  background-color: #202020;
  border: 1px solid #666666;
  border-radius: 7px;
  padding: 7px 9px;
}

entry:focus {
  border-color: #78aeed;
}

entry:disabled {
  opacity: 0.55;
}
```

Testez texte normal, sélection, curseur, placeholder, champ vide, champ invalide, mot de passe et recherche. Le placeholder doit rester distinct du texte saisi sans devenir illisible.

## 5. Cases à cocher, boutons radio et interrupteurs

```css
checkbutton,
radiobutton {
  color: #f6f5f4;
}

switch {
  background-color: #555555;
}

switch:checked {
  background-color: #3584e4;
}
```

Les nœuds internes et les classes exactes peuvent différer selon GTK et la version. Certains contrôles sont dessinés par le moteur plutôt que par un simple fond CSS. Utilisez l'inspecteur GTK et la documentation des widgets.

## 6. Listes, lignes et tableaux d'applications

Les applications utilisent ListBox, TreeView, ListView, GridView ou des composants propriétaires. Les noms CSS et la structure diffèrent.

Exemple générique pour une ligne GTK :

```css
row {
  color: #f6f5f4;
  background-color: #303030;
  border-bottom: 1px solid #454545;
  padding: 6px;
}

row:selected {
  background-color: #245b91;
  color: #ffffff;
}
```

Ne supposez pas que `row` s'applique à toutes les listes GTK 4. Vérifiez le nom de nœud CSS de la liste utilisée.

## 7. Menus et popovers

```css
popover,
menu {
  color: #f6f5f4;
  background-color: #303030;
  border: 1px solid #555555;
  border-radius: 10px;
}

menuitem:hover {
  background-color: #484848;
}
```

Les menus historiques GTK 3 et les popovers GTK 4 ne sont pas toujours construits de la même façon. Testez séparément menus contextuels, menus de barre, sous-menus et popovers attachés aux boutons.

## 8. Curseurs, barres de défilement et progression

Les widgets de défilement et de progression peuvent être dessinés par plusieurs nœuds internes. Ne copiez pas un sélecteur trouvé sur Internet sans vérifier la version.

Exercice : utilisez l'inspecteur pour repérer le nœud du curseur, le rail, le contenu et le bouton de défilement. Modifiez une propriété à la fois. Gardez une zone interactive suffisamment grande et vérifiez le contraste.

## 9. GTK 4 et Libadwaita ne sont pas interchangeables

Une application GTK 4 peut ne pas utiliser Libadwaita. Une application Libadwaita utilise GTK 4, mais ajoute ses propres widgets, styles, couleurs sémantiques et conventions. Une feuille GTK générique ne permet pas de garantir le contrôle de toutes les surfaces Adwaita.

## 10. Inspecter et diagnostiquer

L'inspecteur GTK est l'outil essentiel pour découvrir les nœuds CSS, classes, propriétés et hiérarchies. Selon l'application et la distribution, il peut être activé avec une variable d'environnement ou une option de débogage. Consultez la documentation de la version GTK utilisée et ne laissez pas l'inspection activée dans un environnement de production.

Pour chaque composant, notez :
- le nom du widget ;
- le nom du nœud CSS ;
- ses classes ;
- les pseudo-classes observées ;
- le provider qui fournit le style ;
- le résultat de votre règle ;
- les différences entre GTK 3 et GTK 4.

## 11. Exercices à réaliser

- Bouton : normal, survol, appui, focus, désactivé et action principale.
- Champ : vide, saisi, sélectionné, focus, invalide et désactivé.
- Liste : ligne normale, survolée, sélectionnée et désactivée.
- Menu : ouvert, sous-menu, séparateur et action indisponible.
- Fenêtre : active, inactive, avec et sans barre d'en-tête.
- Défilement : contenu court, contenu long et curseur au minimum/maximum.

Ressources : [GTK 3 CSS](https://docs.gtk.org/gtk3/css-overview.html), [GTK 4 CSS](https://docs.gtk.org/gtk4/css-overview.html), [GTK 3 widgets](https://docs.gtk.org/gtk3/), [GTK 4 widgets](https://docs.gtk.org/gtk4/).
