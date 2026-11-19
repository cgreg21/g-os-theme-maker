# Comprendre et écrire du CSS pour GNOME

Ce chapitre explique le CSS nécessaire pour personnaliser GTK et GNOME Shell. GTK CSS ressemble au CSS du Web, mais ce n'est pas le navigateur : toutes les propriétés, unités, sélecteurs et pseudo-classes ne sont pas identiques.

## 1. Anatomie d'une règle

```css
.button {
  color: white;
  background-color: #3584e4;
  border-radius: 8px;
}
```

- `.button` est le sélecteur ;
- `color` règle la couleur du texte ;
- `background-color` règle le fond ;
- `border-radius` arrondit les coins ;
- les accolades délimitent la règle ;
- le point-virgule termine chaque déclaration.

Un commentaire aide à documenter une décision :

```css
/* Accent réservé aux actions importantes */
.suggested-action {
  background-color: #3584e4;
}
```

## 2. Sélecteurs courants

- `button` : tous les widgets de type bouton correspondant au moteur.
- `.button` : les widgets qui portent la classe `button`.
- `#panel` : l'élément qui porte l'identifiant `panel` dans le Shell.
- `button:hover` : un bouton survolé.
- `entry:focus` : un champ qui reçoit le focus, lorsque cette pseudo-classe est prise en charge.
- `button:disabled` : un bouton indisponible, selon le moteur.
- `A B` : un élément B descendant de A.
- `A, B` : A ou B, avec les mêmes déclarations.

Un sélecteur trop général peut modifier beaucoup plus d'éléments que prévu. Commencez par un seul composant, observez le résultat, puis élargissez si nécessaire.

## 3. Couleurs

Formats courants : `#RGB`, `#RRGGBB`, `rgb(...)` et `rgba(...)` lorsque le moteur les accepte.

```css
.example {
  color: #f6f5f4;
  background-color: rgba(30, 30, 30, 0.92);
  border-color: #777777;
}
```

Une couleur avec transparence laisse apparaître la surface située derrière. Elle peut donc sembler différente selon le fond réel. Testez les menus translucides sur plusieurs arrière-plans.

## 4. Dimensions et espacements

- `width`, `height` : dimensions ;
- `min-width`, `min-height` : dimensions minimales ;
- `padding` : espace à l'intérieur du composant ;
- `margin` : espace autour du composant ;
- `border-width` : épaisseur de bordure ;
- `border-radius` : arrondi ;
- `spacing` : propriété de certains conteneurs GTK, pas une propriété CSS universelle.

Exemple :

```css
.card {
  padding: 12px;
  margin: 6px;
  border: 1px solid #555555;
  border-radius: 12px;
}
```

Le padding augmente la distance entre le contenu et le bord. La marge éloigne le composant de ses voisins. Si un bouton paraît trop large, vérifiez son padding horizontal, mais aussi la taille de son icône, la largeur du texte et le conteneur parent.

## 5. Texte et typographie

```css
.label {
  font-family: "Cantarell";
  font-size: 1em;
  font-weight: 600;
  font-style: normal;
}
```

Une famille installée n'est pas forcément disponible sur tous les systèmes. Prévoir un fallback est important. Une taille relative suit mieux les réglages de police que des valeurs absolues arbitraires. Ne réduisez pas les textes pour faire tenir une interface trop dense.

## 6. Bordures et ombres

```css
.surface {
  border: 1px solid #555555;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.28);
}
```

Les moteurs GTK et St ne prennent pas nécessairement en charge les mêmes variantes de propriétés. Vérifiez la documentation officielle du moteur. Une ombre ne remplace pas une bordure : en contraste élevé, elle peut disparaître.

## 7. États interactifs

```css
button { background-color: #3b3b3b; }
button:hover { background-color: #484848; }
button:active { background-color: #202020; }
button:disabled { opacity: 0.55; }
```

Cet exemple est illustratif : les pseudo-classes exactes et l'état disabled dépendent du moteur et du widget. GTK peut exposer des états via ses nœuds CSS et ses classes. GNOME Shell utilise St. Confirmez toujours les sélecteurs dans la cible.

## 8. Cascade et spécificité

Quand plusieurs règles correspondent au même élément, le moteur résout les conflits selon la priorité du provider, la spécificité et l'ordre des règles. Un sélecteur plus précis peut l'emporter sur un sélecteur générique.

Exemple :

```css
button { background-color: #333333; }
.dialog button { background-color: #454545; }
```

Si le bouton se trouve dans un dialogue et que la classe `dialog` correspond réellement à son parent, la seconde règle est plus ciblée. Évitez d'empiler des exceptions contradictoires : regroupez les règles par composant et supprimez les anciennes déclarations devenues inutiles.

## 9. Variables : GTK 3, GTK 4 et Shell

GTK 3 possède notamment `@define-color`. GTK 4 et Libadwaita exposent des variables et conventions différentes selon versions. GNOME Shell possède ses propres feuilles et variables SCSS en amont, mais un thème CSS installé ne peut pas nécessairement réutiliser toutes les variables de compilation.

Exemple GTK 3 :

```css
@define-color accent_color #3584e4;
@define-color window_bg_color #242424;
@define-color window_fg_color #f6f5f4;

button.suggested-action {
  background-color: @accent_color;
}
```

Ne copiez pas cette syntaxe telle quelle dans Shell. Pour une palette multi-moteur, maintenez des valeurs cohérentes dans chaque fichier et documentez la source de vérité utilisée par votre outil.

## 10. Déboguer un sélecteur qui ne fonctionne pas

1. Vérifiez le moteur : GTK 3, GTK 4, Libadwaita ou Shell.
2. Vérifiez que la feuille chargée est bien celle que vous éditez.
3. Vérifiez que le composant existe dans l'écran affiché.
4. Inspectez le nom de classe ou le nom de nœud CSS avec l'outil adapté.
5. Testez une seule propriété très visible, par exemple un fond temporairement contrasté.
6. Regardez les avertissements du moteur.
7. Vérifiez si l'application ajoute son propre CSS.
8. Supprimez le test temporaire après diagnostic.

Un sélecteur sans erreur de syntaxe peut ne correspondre à aucun élément. Un CSS valide ne garantit donc pas un changement visible.

## 11. Ressources officielles

- [GTK 3 CSS](https://docs.gtk.org/gtk3/css-overview.html)
- [GTK 4 CSS](https://docs.gtk.org/gtk4/css-overview.html)
- [Propriétés CSS GTK 3](https://docs.gtk.org/gtk3/css-properties.html)
- [Propriétés CSS GTK 4](https://docs.gtk.org/gtk4/css-properties.html)
- [Styles Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)
