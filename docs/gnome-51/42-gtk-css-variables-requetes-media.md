# 42. GTK 4.23 : variables CSS, requêtes de média et variantes d'interface

Ce chapitre décrit les mécanismes CSS modernes disponibles dans GTK 4.23, la version minimale requise par Libadwaita 1.10. Il complète les chapitres sur GTK 4 et Libadwaita en expliquant comment écrire des règles adaptatives sans supposer que GTK est un navigateur.

Les exemples ciblent GTK 4.23. Ils ne doivent pas être copiés tels quels dans GTK 3.24 ni dans une ancienne version de GTK 4 sans vérifier chaque fonctionnalité.

## 1. Identifier le moteur avant d'écrire une règle

GTK 4 possède son propre moteur CSS. Il reprend une partie des concepts CSS courants, mais son modèle est construit autour des widgets et de leurs nœuds CSS.

Une règle peut être syntaxiquement valide et ne rien modifier parce que :

- le sélecteur ne correspond à aucun nœud ;
- le widget ne possède pas la propriété visée ;
- la propriété est acceptée, mais sans effet sur ce type de nœud ;
- une règle de priorité supérieure la remplace ;
- l'application charge un provider CSS supplémentaire ;
- la bibliothèque ou l'application dessine elle-même une partie du composant.

Ne commencez donc pas par inventer un sélecteur. Inspectez d'abord le widget avec GTK Inspector, repérez son nom CSS, ses classes, ses états et les nœuds enfants.

## 2. Variables personnalisées CSS

GTK prend en charge les propriétés personnalisées CSS depuis GTK 4.16. GTK 4.23 les prend donc en charge.

Une propriété personnalisée commence par deux tirets et se lit avec `var()` :

```css
:root {
  --demo-surface: #20242b;
  --demo-text: #f6f5f4;
  --demo-accent: #78aeed;
  --demo-radius: 12px;
}

window {
  background-color: var(--demo-surface);
  color: var(--demo-text);
}

button.suggested-action {
  background-color: var(--demo-accent);
  border-radius: var(--demo-radius);
}
```

Dans cet exemple, les valeurs sont définies sur `:root`, puis réutilisées par plusieurs règles. Cela évite de recopier une même couleur ou un même rayon dans toute la feuille.

Une propriété personnalisée n'est pas automatiquement une propriété de thème Libadwaita. Le préfixe `--demo-` indique ici une convention privée au projet. Les variables fournies par Libadwaita ont leur propre contrat et leur propre sémantique.

### Valeur de repli

La fonction `var()` peut recevoir une valeur de secours :

```css
button {
  color: var(--demo-text, #ffffff);
}
```

Si la propriété personnalisée n'est pas définie dans le contexte applicable, la valeur de secours est utilisée. Cette forme est utile lorsqu'une feuille est partagée entre plusieurs composants ou chargée dans plusieurs contextes.

### Portée et héritage

Les propriétés personnalisées participent à la cascade et sont héritées. Une valeur définie sur `:root` peut donc être utilisée par les descendants, sauf si une valeur plus proche la remplace.

Pour créer une variante locale :

```css
.warning-panel {
  --demo-accent: #e01b24;
}

.warning-panel button.suggested-action {
  background-color: var(--demo-accent);
}
```

La variable est redéfinie sur le conteneur de l'avertissement. Elle n'altère pas la valeur globale utilisée ailleurs.

Ne nommez pas vos variables avec des noms génériques susceptibles d'entrer en collision avec celles de la bibliothèque. Utilisez un préfixe propre au projet, par exemple `--gostm-`.

## 3. Sélecteur :root

GTK 4.16 a ajouté la prise en charge de `:root`. Il représente la racine de l'arbre CSS concerné par le provider.

Exemple :

```css
:root {
  --gostm-panel-radius: 14px;
  --gostm-panel-gap: 8px;
}
```

Ne confondez pas `:root` avec un sélecteur HTML. GTK ne possède pas de document HTML : la racine correspond au contexte de style GTK.

Dans une application, un provider CSS peut être appliqué à une portée différente. La portée effective du provider et l'arbre CSS inspecté déterminent donc les nœuds concernés.

## 4. Détecter le mode clair ou sombre

GTK 4.20 prend en charge les requêtes de média `prefers-color-scheme`. Elles permettent d'adapter une feuille CSS à la préférence de couleur effective du provider.

```css
.preview-card {
  background-color: #f6f5f4;
  color: #241f31;
}

@media (prefers-color-scheme: dark) {
  .preview-card {
    background-color: #2e2e32;
    color: #ffffff;
  }
}
```

La règle de base définit l'apparence claire. La règle conditionnelle ne s'applique que lorsque le provider utilise le schéma sombre.

La requête CSS ne remplace pas la logique de préférence de l'application. Dans Libadwaita, le choix final dépend notamment de `AdwStyleManager:color-scheme` et de la préférence système. Une application peut préférer le clair, préférer le sombre ou forcer un mode.

Libadwaita 1.10 prend également en charge les ressources conditionnelles `style-dark.css`, `style-hc.css` et `style-hc-dark.css` via `AdwApplication`. Pour une nouvelle application, la documentation recommande toutefois une feuille `style.css` unique et des requêtes `prefers-color-scheme` et `prefers-contrast`, qui rendent les variantes plus faciles à maintenir. Ces ressources séparées restent utiles pour comprendre et maintenir les applications qui les utilisent.

Pour un thème d'application, privilégiez les variables sémantiques Libadwaita lorsqu'elles sont disponibles. Les valeurs codées en dur dans l'exemple servent uniquement à montrer la structure d'une requête.

## 5. Détecter le contraste élevé

GTK 4.20 prend en charge `prefers-contrast`. La valeur `more` permet de cibler un contexte de contraste renforcé.

```css
.status-label {
  border: 1px solid alpha(currentColor, 0.25);
}

@media (prefers-contrast: more) {
  .status-label {
    border: 2px solid currentColor;
    font-weight: 700;
  }
}
```

Le contraste élevé n'est pas un synonyme du mode sombre. Il s'agit d'une préférence distincte, qui peut être combinée avec le mode clair ou sombre.

Évitez de construire une variante contraste élevé en augmentant simplement l'opacité de tous les éléments. Les textes, les bordures, les états de focus et les contrôles doivent rester distinguables. Les composants standard Libadwaita gèrent déjà une grande partie de cette adaptation ; les composants personnalisés doivent être vérifiés séparément.

## 6. Détecter la réduction des animations

GTK 4.22 a ajouté la prise en charge de `prefers-reduced-motion`. GTK 4.23 peut donc l'utiliser.

```css
.progress-decoration {
  transition: opacity 180ms ease;
}

@media (prefers-reduced-motion: reduce) {
  .progress-decoration {
    transition: none;
  }
}
```

La requête permet de réduire ou supprimer les transitions CSS concernées. Elle ne peut pas désactiver une animation déclenchée directement par du code applicatif ou par une bibliothèque qui ne consulte pas cette préférence.

Dans Libadwaita, les widgets standards adaptent leur comportement. Pour un composant personnalisé, il faut aussi adapter les animations programmatiques, les déplacements et les effets visuels. Ne supposez pas qu'une règle CSS suffit à rendre toute l'application compatible avec la réduction des mouvements.

## 7. Combiner les variantes sans dupliquer toute la feuille

Les requêtes peuvent être combinées pour exprimer une condition précise :

```css
.preview-surface {
  background-color: #f6f5f4;
  color: #241f31;
  border: 1px solid alpha(currentColor, 0.2);
  transition: background-color 160ms ease;
}

@media (prefers-color-scheme: dark) {
  .preview-surface {
    background-color: #242428;
    color: #ffffff;
  }
}

@media (prefers-contrast: more) {
  .preview-surface {
    border-width: 2px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .preview-surface {
    transition: none;
  }
}
```

Chaque requête modifie uniquement les propriétés qui doivent changer. Cette approche évite de maintenir quatre feuilles complètes qui divergent au fil des corrections.

Il reste nécessaire de tester les combinaisons réelles : clair standard, sombre standard, clair avec contraste élevé et sombre avec contraste élevé. La réduction des mouvements constitue une dimension supplémentaire.

## 8. Couleurs sémantiques Libadwaita

Libadwaita fournit des variables de couleur destinées à exprimer le rôle d'une surface ou d'un texte plutôt qu'une valeur arbitraire.

Exemples courants :

- `--window-bg-color` et `--window-fg-color` pour la fenêtre ;
- `--view-bg-color` et `--view-fg-color` pour les surfaces de contenu ;
- `--headerbar-bg-color` et `--headerbar-fg-color` pour les barres d'en-tête ;
- `--card-bg-color` pour les cartes ;
- `--popover-bg-color` pour les popovers ;
- `--accent-bg-color` et `--accent-fg-color` pour les surfaces d'accent.

Exemple d'utilisation dans une feuille applicative :

```css
.preview-card {
  background-color: var(--card-bg-color);
  color: var(--window-fg-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}
```

Ces variables sont fournies par la feuille Libadwaita et doivent être utilisées dans un contexte où cette feuille est effectivement chargée. Elles ne sont pas disponibles dans GNOME Shell ni dans une application GTK 3.

Ne remplacez pas systématiquement toutes les variables. Certaines valeurs auxiliaires, notamment `--border-opacity`, `--dim-opacity` et `--disabled-opacity`, servent à adapter automatiquement les bordures, les textes atténués et les éléments désactivés au contraste. Les détourner peut casser l'accessibilité.

Lorsque vous surchargez une couleur d'accent, conservez un contraste suffisant entre la couleur de fond et la couleur de premier plan. Si vous surchargez une couleur d'accent locale à un widget, vérifiez aussi la couleur autonome associée lorsque le composant l'utilise.

## 9. Charger les styles conditionnels d'une application Libadwaita

Libadwaita permet à une application de fournir des ressources de style conditionnelles. Le mécanisme appartient à l'application et à ses ressources GResource ; il ne s'agit pas d'un dossier universel que l'utilisateur peut déposer dans son thème global.

Les noms de ressources documentés sont :

- `style.css` pour les règles générales ;
- `style-dark.css` pour les règles du mode sombre ;
- `style-hc.css` pour le contraste élevé ;
- `style-hc-dark.css` pour le contraste élevé avec le mode sombre.

Ces fichiers sont chargés par `AdwApplication` depuis la base de ressources de l'application. Leur présence dépend donc de la manière dont le programme est construit et empaqueté.

Pour personnaliser une application tierce, il faut d'abord déterminer si elle expose un mécanisme de CSS utilisateur. La présence de Libadwaita ne garantit pas qu'un fichier placé dans `~/.themes` sera chargé.

## 10. Vérifier les fonctionnalités dans l'environnement réel

Vérifiez la version du moteur :

```sh
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
```

Une erreur de `pkg-config` peut indiquer l'absence du paquet de développement. Elle ne prouve pas que la bibliothèque d'exécution n'est pas installée.

Pour vérifier une feuille CSS :

1. Lancez l'application dans un environnement de test.
2. Ouvrez GTK Inspector.
3. Sélectionnez le widget concerné.
4. Vérifiez son nom CSS, ses classes et ses états.
5. Examinez les règles appliquées et les avertissements du provider.
6. Changez le mode clair/sombre depuis les préférences de l'application ou de la session.
7. Activez le contraste élevé.
8. Activez la réduction des mouvements.
9. Vérifiez les quatre combinaisons de couleurs et les états interactifs.
10. Conservez une capture locale de chaque résultat important.

Un chargement sans avertissement ne garantit pas que les sélecteurs correspondent. Une règle sans erreur peut simplement ne cibler aucun nœud.

## 11. Erreurs fréquentes

**Utiliser les variables Libadwaita dans GTK 3.** GTK 3.24 ne fournit pas le système de variables personnalisées CSS de GTK 4.16+. Les variables Libadwaita ne sont donc pas une solution de compatibilité GTK 3.

**Utiliser `:root` dans une ancienne version de GTK 4.** Les variables personnalisées et `:root` nécessitent GTK 4.16 ou plus récent.

**Confondre contraste élevé et mode sombre.** Les deux préférences sont indépendantes. Testez leur combinaison.

**Supprimer les transitions sans traiter les animations programmatiques.** La requête de réduction des mouvements doit aussi être prise en compte dans le code des composants personnalisés.

**Copier un CSS d'application dans le thème global.** Un provider applicatif et un thème global n'ont pas nécessairement la même portée ni la même priorité.

**Surcharger toutes les couleurs sémantiques.** Les couleurs et variables auxiliaires sont conçues pour fonctionner ensemble. Modifier une seule valeur peut dégrader le contraste dans une variante.

## 12. Références officielles

- [GTK 4 — CSS Overview](https://docs.gtk.org/gtk4/css-overview.html)
- [GTK 4 — CSS Properties](https://docs.gtk.org/gtk4/css-properties.html)
- [GTK 4 — GtkCssProvider: prefers-contrast](https://docs.gtk.org/gtk4/property.CssProvider.prefers-contrast.html)
- [GTK 4 — GtkCssProvider: prefers-reduced-motion](https://docs.gtk.org/gtk4/property.CssProvider.prefers-reduced-motion.html)
- [Libadwaita 1.10 — Styles and Appearance](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)
- [Libadwaita 1.10 — CSS Variables](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/css-variables.html)
- [GNOME 51 — nouveautés développeurs](https://release.gnome.org/51/developers/)
