# 51. Effets visuels avancés : flou, transparence, ombres et animations

Ce chapitre présente les effets qui permettent de dépasser un thème composé uniquement de couleurs et de bordures : verre dépoli, flou, opacité, dégradés, ombres, filtres colorimétriques, transformations et animations.

**Règle essentielle : un effet dépend du moteur qui dessine l'élément.** GNOME Shell utilise St et Clutter ; les applications GTK utilisent GTK CSS ; Mutter compose les surfaces et les fenêtres. Une propriété CSS disponible dans GTK n'est pas automatiquement disponible dans St. Le flou de l'arrière-plan n'est pas non plus la même chose que le flou du contenu d'un widget.

Les exemples ciblent GNOME 51, GTK 4.23 et les API GNOME Shell 51. Les sélecteurs et les API internes doivent être vérifiés dans la version réellement installée.

## 1. Cartographier les effets et leur moteur

Avant de choisir une technique, identifiez le propriétaire visuel :

- **GNOME Shell / St** : panneau, dash, menus, réglages rapides, notifications et vue Activités. Le CSS St sait notamment gérer couleurs, transparence, dégradés St, ombres et durées de transition. Il ne fournit pas les filtres graphiques CSS du navigateur.
- **Clutter / GNOME Shell en GJS** : effets appliqués à un acteur, dont `Shell.BlurEffect`. Ils nécessitent du code et un accès à l'acteur, pas une simple règle CSS.
- **GTK 4** : widgets d'applications. GTK 4.23 expose notamment `filter`, `opacity`, `transform`, les ombres, les dégradés, les transitions et les animations CSS.
- **Mutter / Wayland** : composition des surfaces et effets demandés au compositeur. Le protocole `ext-background-effect-v1` permet aux clients compatibles de demander un effet sur l'arrière-plan d'une surface, si le compositeur annonce cette capacité.
- **Image préparée** : une texture, un fond ou une image prétraitée peut fournir un résultat visuel fixe, sans calcul d'effet en temps réel.

Pour un thème Shell, commencez par les effets St. Pour un effet de flou réellement dynamique, prévoyez une extension ou une fonctionnalité qui utilise une API de rendu dédiée.

## 2. Transparence et opacité

La transparence est le moyen le plus simple de créer une surface légère. Elle ne produit cependant aucun flou : les pixels situés derrière la surface restent visibles tels quels.

### Couleur alpha dans St et GTK

Exemple pour un menu GNOME Shell :

```css
.popup-menu-content {
  background-color: rgba(30, 34, 42, 0.88);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
}
```

La valeur alpha va de 0 (transparent) à 1 (opaque). Le fond à 0,88 laisse apparaître une partie du contenu derrière la surface, si le chemin de composition et l'acteur le permettent.

Dans GTK, `opacity` règle l'opacité de l'élément rendu et de son contenu :

```css
.preview-card {
  opacity: 0.92;
}
```

Ne confondez pas l'alpha de la couleur de fond et l'opacité de l'ensemble du widget. Une couleur de fond semi-transparente laisse le texte opaque ; une opacité appliquée au widget atténue également ses enfants.

### Conseils de conception

- Gardez les textes et les icônes suffisamment contrastés.
- Ne rendez pas translucides les surfaces qui portent des informations sensibles.
- Évitez les couches transparentes empilées : leurs couleurs se composent et peuvent devenir boueuses.
- Testez le rendu sur un fond clair, sombre, détaillé et animé.
- Prévoyez une surface opaque de repli si le fond sous-jacent n'est pas contrôlable.

## 3. Verre dépoli et flou d'arrière-plan

Un effet « glassmorphism » combine généralement quatre éléments : un arrière-plan flouté, une surface translucide, une bordure claire très fine et parfois une légère teinte ou un grain.

Le flou de l'arrière-plan exige que le moteur puisse échantillonner ce qui se trouve derrière la surface. Une feuille CSS de thème ne dispose pas automatiquement de cet accès.

### Ce que St ne fait pas

Cette règle ne crée pas un flou dans GNOME Shell :

```css
/* À ne pas utiliser dans St : filter n'est pas une propriété CSS St */
.panel {
  backdrop-filter: blur(18px);
}
```

St 51 ne fournit ni `filter: blur(...)` ni `backdrop-filter` comme propriétés de thème. Ajouter ces déclarations ne transforme pas le panneau en surface floutée.

### Shell.BlurEffect

GNOME Shell expose `Shell.BlurEffect`, un effet Clutter pouvant être attaché à un acteur par du code GJS. Il possède notamment un rayon, une luminosité et un mode :

- `ACTOR` : floute l'acteur et ses enfants ;
- `BACKGROUND` : floute les pixels situés derrière l'acteur, sans flouter l'acteur lui-même.

Le mode arrière-plan peut être coûteux : le contenu situé derrière l'acteur ne peut pas être mis en cache de la même façon. Il faut donc limiter la surface concernée, le rayon et les mises à jour inutiles.

Exemple conceptuel d'utilisation dans une extension GNOME Shell 51 :

```js
import Shell from 'gi://Shell';

const effect = new Shell.BlurEffect({
    radius: 18,
    brightness: 0.85,
    mode: Shell.BlurMode.BACKGROUND,
});

actor.add_effect(effect);
```

Cet extrait illustre l'API, mais n'est pas une extension complète : `actor` doit être un acteur Clutter existant, détenu et géré proprement par l'extension. L'extension doit retirer l'effet et déconnecter ses signaux dans `disable()`. Ne conservez pas une référence à un acteur du Shell après sa destruction. Vérifiez les noms d'énumération et les propriétés exposées par les introspections de GNOME Shell 51 de la distribution ciblée.

Le flou d'acteur et le flou d'arrière-plan ont des résultats différents. Pour un fond de panneau « verre dépoli », c'est le mode arrière-plan qui correspond à l'intention.

### Flou demandé au compositeur Wayland

GNOME 51 intègre la prise en charge Mutter du protocole expérimental `ext-background-effect-v1`. Un client Wayland compatible peut demander un effet d'arrière-plan sur sa surface. Le compositeur annonce ses capacités ; si la capacité n'est pas disponible, le client ne doit pas supposer que le flou sera appliqué.

Ce mécanisme vise les surfaces des clients Wayland, par exemple une fenêtre d'application. Il ne signifie pas qu'une règle CSS GTK ou Shell peut demander arbitrairement le flou de n'importe quelle zone du bureau. Le support dépend du compositeur, du protocole et du toolkit ou de l'application qui l'implémente.

Mutter expose aussi des paramètres globaux de rendu pour ces effets, notamment le rayon de flou, la saturation et le bruit. Ce sont des paramètres du compositeur, pas des propriétés CSS destinées aux thèmes utilisateur.

### Alternative statique

Si aucun moteur de flou n'est disponible, utilisez une image de fond déjà floutée, ou une couleur translucide avec une bordure discrète. Cette solution est prévisible et peu coûteuse, mais elle ne floute pas dynamiquement les fenêtres qui passent derrière.

## 4. Ombres portées et profondeur

Les ombres séparent les couches et aident à comprendre la hiérarchie visuelle. GNOME Shell St prend en charge `box-shadow` et `text-shadow` pour les acteurs qui utilisent ces chemins de rendu.

```css
.popup-menu-content {
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.34);
}

.dash-background {
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.24);
}
```

Une ombre comporte un décalage horizontal, un décalage vertical, un flou et éventuellement une couleur. Évitez les ombres très sombres et très étendues : elles donnent un aspect artificiel et peuvent coûter plus cher au rendu.

GTK 4 prend également en charge `box-shadow` et `text-shadow`. Dans GTK, la propriété est interprétée selon les règles GTK CSS et non selon un moteur de navigateur complet.

À distinguer :
- ombre dessinée par GTK : modifiable dans la feuille CSS du widget si celui-ci la dessine ;
- ombre d'une fenêtre dessinée par Mutter : ne se règle pas avec le CSS de l'application ;
- ombre d'un acteur Shell : dépend du thème Shell ou du code de l'acteur ;
- ombre intégrée à une image : doit être modifiée dans l'image source.

Ne multipliez pas les ombres entre la fenêtre, sa barre d'en-tête et ses cartes internes. Une hiérarchie simple est plus lisible.

## 5. Dégradés et surfaces colorées

St possède ses propres propriétés de dégradé. Elles ne sont pas les fonctions `linear-gradient()` et `radial-gradient()` d'un navigateur.

Exemple GNOME Shell :

```css
#panel {
  -st-gradient-direction: vertical;
  -st-gradient-start: rgba(40, 46, 58, 0.96);
  -st-gradient-end: rgba(20, 24, 32, 0.96);
}
```

Directions reconnues par St 51 :
- `vertical` ;
- `horizontal` ;
- `radial` ;
- `none`.

Pour GTK 4.23, les dégradés CSS standards peuvent être utilisés :

```css
.preview-card {
  background-image: linear-gradient(
    135deg,
    #303b50 0%,
    #242a38 55%,
    #171b25 100%
  );
}
```

N'utilisez pas la syntaxe GTK dans le thème Shell. Inversement, les propriétés `-st-gradient-*` ne sont pas des propriétés GTK.

Un dégradé doit conserver un contraste suffisant sur toute sa surface. Vérifiez le texte au point le plus clair et au point le plus sombre.

## 6. Filtres de couleur : luminosité, contraste, saturation et niveaux de gris

GTK 4.23 documente la propriété `filter`. Elle agit sur le rendu du widget ciblé, y compris son contenu ; elle ne prélève pas les pixels de la fenêtre située derrière.

Exemple GTK 4 :

```css
.preview-image {
  filter: saturate(1.2) contrast(1.05);
}

.preview-image:disabled {
  filter: grayscale(1) opacity(0.55);
}
```

Les fonctions courantes comprennent :
- `blur()` : flou du contenu rendu par le widget ;
- `brightness()` : luminosité ;
- `contrast()` : contraste ;
- `saturate()` : saturation ;
- `grayscale()` : niveaux de gris ;
- `sepia()` : teinte sépia ;
- `hue-rotate()` : rotation de teinte ;
- `invert()` : inversion ;
- `opacity()` : opacité du rendu ;
- `drop-shadow()` : ombre du contenu alpha.

Exemple de flou du contenu d'une image GTK :

```css
.preview-image.is-softened {
  filter: blur(3px);
}
```

Ce filtre floute l'image ou le contenu du widget, pas le bureau visible derrière. Ne confondez pas `filter` et `backdrop-filter`.

GTK propose aussi `-gtk-icon-filter` pour appliquer un filtre à certaines icônes. Cette propriété concerne les icônes chargées par les mécanismes GTK appropriés ; elle ne recolore pas arbitrairement toute image.

**Limite GNOME Shell :** ces fonctions CSS de filtre ne sont pas disponibles dans St 51. Pour un effet de couleur dans le Shell, il faut employer les propriétés St réellement documentées, une image prétraitée ou un effet Clutter géré par du code.

## 7. Transformations et effets de mouvement

GTK 4.23 prend en charge `transform` et `transform-origin`. Les transformations peuvent déplacer, faire pivoter ou mettre à l'échelle un widget sans modifier la disposition logique de ses voisins.

```css
.preview-icon {
  transform: scale(1);
  transition: transform 160ms ease;
}

.preview-icon:hover {
  transform: scale(1.06);
}
```

La transformation ne remplace pas le calcul de taille : un widget agrandi peut chevaucher ses voisins ou être rogné par un conteneur. Testez les limites, les zones cliquables et le focus clavier.

St ne doit pas être considéré comme un navigateur. Les propriétés de transformation CSS Web ne figurent pas parmi les propriétés de thème St 51 garanties par le chapitre 47. Pour déplacer ou mettre à l'échelle un acteur Shell, utilisez les API Clutter adaptées, ou une propriété St dont la prise en charge est explicitement vérifiée.

## 8. Transitions et animations

GTK 4.23 prend en charge les propriétés de transition et les animations CSS. Une transition anime le changement d'une propriété compatible ; une animation nommée peut appliquer plusieurs étapes.

Exemple de transition :

```css
.action-card {
  opacity: 0.88;
  transition: opacity 180ms ease, background-color 180ms ease;
}

.action-card:hover {
  opacity: 1;
  background-color: alpha(@accent_bg_color, 0.16);
}
```

Exemple d'animation GTK :

```css
@keyframes pulse-subtle {
  from { opacity: 0.72; }
  to   { opacity: 1; }
}

.status-indicator.attention {
  animation: pulse-subtle 900ms ease-in-out infinite alternate;
}
```

N'animez pas en permanence un grand nombre de widgets. Les animations infinies consomment des ressources et peuvent distraire. Réservez-les à une information utile et temporaire.

Dans GNOME Shell, les transitions et animations sont aussi pilotées par le code Clutter et le comportement des composants. Une règle CSS ne peut pas remplacer une animation programmée ni garantir qu'un changement d'état est animé.

## 9. Grain, texture et effets lumineux

Le grain, les reflets et les halos ne sont pas des propriétés magiques du thème. Ils sont généralement obtenus par :
- une texture PNG intégrée dans le thème ;
- une image superposée à faible opacité ;
- un effet Clutter personnalisé ;
- un shader ou un traitement graphique dans le code applicatif.

Pour un thème distribué, une petite texture répétable est souvent plus fiable qu'un effet temps réel. Vérifiez toutefois le poids des ressources, leur résolution HiDPI et leur contraste. Évitez d'ajouter un grain visible sur les textes ou les zones de lecture.

Un halo peut être simulé avec une ombre colorée si le moteur et le widget la prennent en charge :

```css
/* Exemple GTK 4 ; ne pas transposer tel quel dans St */
.glowing-card {
  box-shadow: 0 0 18px alpha(@accent_color, 0.32);
}
```

Un halo trop intense réduit la netteté et peut créer des problèmes de contraste. Ne l'utilisez pas comme seul indicateur d'un état important.

## 10. Construire une surface « verre dépoli » cohérente

Pour GTK 4.23, une carte translucide avec bordure, ombre et contenu légèrement filtré peut être écrite ainsi :

```css
.glass-card {
  background-color: alpha(@window_bg_color, 0.82);
  border: 1px solid alpha(currentColor, 0.14);
  border-radius: 18px;
  box-shadow: 0 12px 32px alpha(black, 0.22);
  padding: 18px;
}

/* Le filtre ne floute que le contenu de ce widget. */
.glass-card .preview-image {
  filter: saturate(0.85) brightness(0.92);
}
```

Cette carte est translucide et possède une profondeur visuelle, mais elle n'est pas encore un vrai verre dépoli : elle ne floute pas l'arrière-plan. Pour obtenir ce dernier effet, l'application doit utiliser un mécanisme de flou fourni par le compositeur ou un effet de rendu adapté.

Dans St, reproduisez uniquement les éléments compatibles : alpha, bordure, rayon et ombre. Le vrai flou demande une extension et `Shell.BlurEffect`, ou une solution explicitement prise en charge par la version du Shell.

## 11. Accessibilité et réduction des mouvements

Les effets ne doivent jamais être indispensables à la compréhension de l'interface.

- Maintenez le contraste des textes sur les surfaces translucides.
- Ne transmettez pas une information uniquement par une couleur, un halo ou une animation.
- Évitez les clignotements et les pulsations répétées.
- Réduisez les déplacements et les zooms lorsque l'utilisateur demande moins d'animations.
- Préservez les indicateurs de focus et les états désactivés.
- Fournissez une surface lisible lorsque les effets GPU sont indisponibles.

GTK 4.23 prend en charge la requête de média `prefers-reduced-motion`. Exemple :

```css
.animated-card {
  transition: transform 180ms ease, opacity 180ms ease;
}

@media (prefers-reduced-motion: reduce) {
  .animated-card {
    transition: none;
    animation: none;
    transform: none;
  }
}
```

Cette règle ne désactive que les animations CSS concernées. Une animation pilotée par GJS, Clutter ou le code de l'application doit consulter la préférence de réduction des mouvements dans son propre code.

## 12. Performances et stabilité

Les effets les plus coûteux sont souvent ceux qui doivent recalculer une grande zone à chaque image : flou d'arrière-plan, filtres animés, textures haute résolution et effets superposés.

Pour limiter les coûts :

1. Réduisez la surface floutée.
2. Utilisez un rayon raisonnable.
3. Évitez le flou sur des acteurs qui changent constamment.
4. Ne multipliez pas les effets sur le même acteur.
5. Préférez les images prétraitées pour les éléments statiques.
6. Testez sur GPU intégré et matériel moins puissant.
7. Vérifiez les fréquences d'images et la consommation en situation réelle.
8. Désactivez proprement les effets et restaurez l'état initial lorsque l'extension est désactivée.

Le mode `BACKGROUND` de `Shell.BlurEffect` mérite une attention particulière car le contenu sous l'acteur ne peut pas être mis en cache comme le contenu d'un acteur flouté. Un flou spectaculaire sur une capture statique peut devenir saccadé lorsqu'une fenêtre ou une vidéo bouge derrière le panneau.

## 13. Procédure de test

Pour chaque effet ajouté :

1. Identifiez le moteur qui dessine l'élément.
2. Vérifiez que la propriété ou l'API existe dans la version cible.
3. Testez d'abord un seul effet sur une petite surface.
4. Vérifiez clair, sombre et contraste élevé.
5. Vérifiez les états normal, survolé, actif, désactivé et focus.
6. Testez avec plusieurs facteurs d'échelle et plusieurs moniteurs.
7. Testez une session Wayland et X11 si elles sont prises en charge.
8. Testez la réduction des mouvements.
9. Mesurez les performances avec du contenu animé derrière la surface.
10. Désactivez l'extension ou retirez le thème pour confirmer le retour à l'état normal.

Conservez une capture avant/après et notez la version de GNOME Shell, GTK, Mutter, le type de session, le GPU et les extensions activées.

## 14. Dépannage

**Le flou CSS n'apparaît pas dans le panneau Shell.** C'est attendu : St ne prend pas en charge `filter` ni `backdrop-filter` comme les navigateurs. Utilisez un effet Clutter dans une extension, ou une alternative statique.

**Le widget GTK est flou mais le bureau derrière reste net.** La propriété GTK `filter: blur()` agit sur le widget lui-même. Le flou de l'arrière-plan exige une API du compositeur.

**Le verre dépoli est trop opaque.** Réduisez l'alpha de la couleur de fond, mais vérifiez le contraste sur plusieurs arrière-plans. Une surface très transparente n'est pas toujours lisible.

**Les menus sont lents après ajout du flou.** Réduisez le rayon et la zone affectée. Vérifiez que le mode arrière-plan n'est pas appliqué à un acteur trop grand ou fréquemment redessiné.

**L'animation ne respecte pas la préférence de réduction des mouvements.** Vérifiez si elle vient du CSS ou du code Clutter/GJS. La règle CSS ne contrôle pas une animation programmée.

**L'effet disparaît sur une autre distribution.** Vérifiez la version réelle de Mutter, GNOME Shell et GTK, les protocoles Wayland annoncés et les extensions activées. Ne supposez pas que la présence de GNOME 51 garantit toutes les options expérimentales de la même manière.

## 15. Références officielles

- [GTK 4 — CSS Properties](https://docs.gtk.org/gtk4/css-properties.html)
- [GTK 4 — CSS Overview](https://docs.gtk.org/gtk4/css-overview.html)
- [GNOME Shell — Shell.BlurEffect](https://gnome.pages.gitlab.gnome.org/gnome-shell/shell/class.BlurEffect.html)
- [Mutter — Meta.Compositor.set_background_blur_params](https://gnome.pages.gitlab.gnome.org/mutter/meta/method.Compositor.set_background_blur_params.html)
- [Mutter — documentation API](https://mutter.gnome.org/)
- [Protocole Wayland ext-background-effect-v1](https://wayland.app/protocols/ext-background-effect-v1)
- [GNOME Shell 51.0 — code source](https://gitlab.gnome.org/GNOME/gnome-shell/-/tree/51.0)
- [Mutter — code source](https://gitlab.gnome.org/GNOME/mutter)

Les références d'API évoluent. Lorsque la documentation en ligne affiche une version plus récente que 51, vérifiez les signatures dans les introspections et les sources du tag 51.0 avant de reprendre un exemple.
