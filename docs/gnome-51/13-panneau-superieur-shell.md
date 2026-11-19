# Personnaliser le panneau supérieur de GNOME Shell 51

Ce chapitre est un tutoriel complet consacré au panneau supérieur : la barre qui traverse le haut de l'écran et contient Activités, l'horloge et les indicateurs système. Les sélecteurs et les comportements décrits ici ont été contrôlés dans les sources amont **GNOME Shell 51.0**.

Sources principales :
- [`_panel.scss` — style du panneau dans GNOME Shell 51.0](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_panel.scss)
- [`panel.js` — construction du panneau](https://github.com/GNOME/gnome-shell/blob/51.0/js/ui/panel.js)
- [`_buttons.scss` — styles communs des boutons](https://github.com/GNOME/gnome-shell/blob/51.0/data/theme/gnome-shell-sass/widgets/_buttons.scss)
- [Documentation du moteur St](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/)

Les noms de classes sont des détails d'implémentation. Ils peuvent changer lors d'une mise à jour de GNOME. Ce chapitre décrit la version 51.0 et ne garantit pas la compatibilité avec d'autres versions.

![Schéma annoté du panneau supérieur : Activités, horloge, indicateurs système et états des boutons](https://help.gnome.org/gnome-help/figures/shell-top-bar.png)

Le schéma est une représentation pédagogique simplifiée. Il sert à localiser les zones et classes ; il ne prétend pas reproduire à l'identique toutes les dispositions possibles.

## 1. Comprendre le panneau avant de le modifier

Le panneau est un ensemble d'acteurs St créés par le code JavaScript du Shell. Le CSS modifie leur apparence, mais ne crée pas les indicateurs et ne décide pas de leur position fonctionnelle.

Dans l'implémentation 51.0, le conteneur principal porte l'identifiant `panel`. Les zones gauche, centrale et droite sont construites par `panel.js`. Le contenu exact de ces zones dépend de la session, des services disponibles et des extensions actives.

Les éléments visuels principaux sont :

- **Activités** : bouton d'accès à la vue d'ensemble ; il peut aussi afficher des points représentant les espaces de travail.
- **Horloge** : bouton central qui ouvre le calendrier et les notifications.
- **Indicateurs système** : réseau, son, alimentation, Bluetooth, accessibilité et autres indicateurs regroupés dans le menu d'état.
- **Indicateurs de confidentialité** : signalement de l'enregistrement ou du partage d'écran.
- **Boutons ajoutés par des extensions** : ils peuvent employer leurs propres classes et ne sont pas nécessairement couverts par le thème natif.

Le panneau est donc à la fois un conteneur, une rangée de boutons et une zone d'état. Il faut inspecter séparément chaque niveau.

## 2. Préparer un environnement de test

Ne commencez pas par modifier le thème système dans `/usr/share`. Travaillez dans une copie de thème ou dans l'environnement de développement du projet.

Vérifiez la version réellement exécutée :

```sh
gnome-shell --version
```

Créez la structure minimale d'un thème :

```sh
mkdir -p ~/.local/share/themes/MonTheme/gnome-shell
touch ~/.local/share/themes/MonTheme/gnome-shell/gnome-shell.css
```

Le chargement d'un thème Shell utilisateur nécessite un mécanisme qui autorise les thèmes Shell, généralement l'extension User Themes. La disponibilité et le mode d'activation dépendent de la distribution et de la session. Ne supposez pas que le réglage du thème GTK active également le thème Shell.

Pour un travail sérieux, utilisez une session GNOME imbriquée ou une machine virtuelle. Un thème mal formé peut rendre l'interface difficile à utiliser. Conservez un moyen de revenir au thème par défaut.

## 3. Le conteneur principal `#panel`

Dans `_panel.scss`, le sélecteur principal est :

```css
#panel
```

La version 51.0 définit notamment :
- une couleur de fond issue de la palette du thème Shell ;
- une graisse de police en gras ;
- une hauteur basée sur `2.2em` dans la source SCSS ;
- une durée de transition de 250 ms ;
- une ombre inférieure dans la variante claire.

La hauteur est exprimée en em dans la source : elle suit donc la taille de police du panneau. Ce n'est pas un simple nombre de pixels indépendant de la typographie.

### Exemple : créer un panneau sombre avec une séparation discrète

Ajoutez dans `gnome-shell.css` :

```css
#panel {
  background-color: #242832;
  color: #f6f5f4;
  font-weight: 600;
  border-bottom: 1px solid #414957;
}
```

Explication :
- `background-color` définit la surface du panneau.
- `color` définit la couleur héritée par les éléments qui ne la remplacent pas.
- `font-weight` modifie la graisse lorsque la police possède cette variante.
- `border-bottom` ajoute une séparation entre le panneau et le contenu du bureau.

La valeur de hauteur n'est volontairement pas modifiée dans ce premier exercice. Commencez par la couleur, car changer la géométrie peut provoquer des décalages dans les menus et les zones cliquables.

### Exercice

1. Appliquez uniquement le fond et la bordure.
2. Ouvrez le menu réseau, le menu son et le calendrier.
3. Vérifiez que les popovers restent correctement attachés au panneau.
4. Ouvrez la vue Activités.
5. Revenez au bureau et vérifiez que le panneau retrouve son apparence normale.

Si la bordure n'est pas visible dans un état donné, vérifiez les règles spécifiques à cet état avant d'augmenter la spécificité.

## 4. Les boutons du panneau : `.panel-button`

Les indicateurs et les boutons principaux utilisent la classe :

```css
#panel .panel-button
```

Le SCSS source applique un mixin commun de bouton. Il gère des dimensions naturelles et minimales horizontales, ainsi que les états interactifs. Les propriétés St `-natural-hpadding` et `-minimum-hpadding` contrôlent le padding horizontal naturel et minimal du bouton.

Exemple de personnalisation :

```css
#panel .panel-button {
  color: #f6f5f4;
  border-radius: 8px;
  padding: 0 9px;
  margin: 3px 2px;
}

#panel .panel-button:hover {
  background-color: rgba(255, 255, 255, 0.10);
}

#panel .panel-button:active,
#panel .panel-button:checked {
  background-color: rgba(120, 174, 237, 0.28);
}

#panel .panel-button:focus {
  outline: 2px solid #78aeed;
  outline-offset: -2px;
}
```

Attention : le mixin natif peut déjà définir des effets de focus et d'activation. L'exemple remplace volontairement ces effets. Vérifiez que le focus reste évident au clavier et que les indicateurs actifs restent reconnaissables.

Ne mettez pas une hauteur arbitraire sur tous les boutons. Le contenu varie : certains indicateurs affichent une icône seule, d'autres plusieurs icônes ou un pourcentage.

## 5. Le bouton Activités : `#panelActivities`

Le bouton Activités est un bouton du panneau identifié par :

```css
#panel #panelActivities
```

Dans le SCSS 51.0, son conteneur StBoxLayout gère le padding et l'espacement. Les points d'espaces de travail utilisent la classe `.workspace-dot`.

Exemple :

```css
#panel #panelActivities StBoxLayout {
  padding-left: 4px;
  padding-right: 4px;
  spacing: 5px;
}

#panel #panelActivities .workspace-dot {
  min-width: 5px;
  min-height: 5px;
  border-radius: 999px;
  background-color: #f6f5f4;
}
```

Le point est un indicateur de navigation, pas une décoration. Ne le supprimez pas sans vérifier le comportement de navigation entre espaces de travail.

Pour tester :
- ouvrez plusieurs espaces de travail ;
- passez de l'un à l'autre ;
- ouvrez Activités ;
- vérifiez le contraste des points sur un fond clair et sombre ;
- vérifiez que leur taille reste visible à l'échelle 200 %.

Le CSS peut modifier les points existants, mais ne peut pas créer des espaces de travail supplémentaires.

## 6. L'horloge : `.clock-display` et `.clock`

Le bouton horloge utilise `.clock-display`. Son texte est placé dans un enfant `.clock`. La source 51.0 applique délibérément le fond d'état au sous-élément `.clock`, afin de ne pas inclure l'indicateur Ne pas déranger dans le même fond.

Les repères CSS sont :

```css
#panel .clock-display
#panel .clock-display .clock
#panel .clock-display .messages-indicator
.clock-display-box
```

Exemple :

```css
#panel .clock-display {
  padding-left: 4px;
  padding-right: 4px;
}

#panel .clock-display .clock {
  padding-left: 8px;
  padding-right: 8px;
  border-radius: 7px;
}

#panel .clock-display:hover .clock {
  background-color: rgba(255, 255, 255, 0.10);
}

#panel .clock-display .messages-indicator {
  icon-size: 16px;
}
```

Le sélecteur `.clock-display-box` règle l'espacement de la boîte d'affichage. Ne le confondez pas avec le bouton complet.

Testez les formats 12 h et 24 h, l'affichage de la date, les chaînes localisées longues et le mode Ne pas déranger. Le texte de l'horloge est calculé par le Shell : CSS ne change pas son format.

## 7. Indicateurs système et icônes

Les icônes des indicateurs du panneau utilisent notamment :

```css
#panel .system-status-icon
#panel .panel-status-indicators-box
#panel .panel-status-indicators-box > .system-status-icon
```

Dans la source 51.0 :
- la taille des icônes est liée à la variable d'échelle des icônes ;
- les icônes ont un padding horizontal ;
- les groupes d'indicateurs définissent leur espacement ;
- certains groupes combinés réduisent le padding individuel.

Exemple prudent :

```css
#panel .system-status-icon {
  icon-size: 16px;
}

#panel .panel-status-indicators-box {
  spacing: 4px;
}

#panel .panel-status-indicators-box > .system-status-icon {
  padding-left: 2px;
  padding-right: 2px;
}
```

Évitez d'augmenter simultanément la taille des icônes, leur padding et l'espacement du groupe. Le panneau peut manquer de place, particulièrement avec plusieurs indicateurs ou une langue dont les libellés sont plus longs.

Les icônes système ne sont pas toutes des images indépendantes. Leur dessin peut dépendre du thème d'icônes, de leur nom symbolique et de la propriété St `-st-icon-style`.

## 8. Indicateurs d'enregistrement et de partage d'écran

GNOME Shell 51.0 distingue les classes :

```css
#panel .screen-recording-indicator
#panel .screen-sharing-indicator
#panel .privacy-indicator
```

La source donne une couleur spécifique à l'enregistrement et une couleur de confidentialité au partage d'écran. Les deux indicateurs ont leurs propres styles de bouton rempli.

Exemple :

```css
#panel .panel-button.screen-recording-indicator {
  background-color: #c01c28;
  color: #ffffff;
}

#panel .panel-button.screen-sharing-indicator {
  background-color: #e5a50a;
  color: #241f31;
}

#panel .privacy-indicator {
  color: #e5a50a;
}
```

Ne rendez pas ces indicateurs invisibles ou indistinguables. Ils informent l'utilisateur qu'une capture ou un partage est en cours. Vérifiez leur contraste, y compris sur le panneau transparent de la vue Activités et sur l'écran verrouillé.

Les indicateurs sont liés à l'activité réelle du système. Un thème ne doit jamais simuler leur état ni masquer leur présence.

## 9. Les états spéciaux du panneau

Le SCSS GNOME Shell 51.0 prévoit des styles particuliers lorsque le panneau est dans certains contextes :

- `#panel:overview` : panneau dans la vue Activités ;
- `#panel.unlock-screen` : écran de verrouillage ;
- `#panel.login-screen` : écran de connexion.

Dans ces contextes, le panneau peut être transparent et la couleur du texte change. La source contient des règles spécifiques pour les boutons et les indicateurs de confidentialité.

Exemple de surcharge ciblée :

```css
#panel:overview {
  background-color: rgba(24, 27, 34, 0.35);
}

#panel.unlock-screen,
#panel.login-screen {
  background-color: transparent;
}

#panel.unlock-screen .panel-button,
#panel.login-screen .panel-button {
  color: #ffffff;
}
```

Cette surcharge est illustrative : les règles internes du thème peuvent être plus spécifiques ou réappliquer le style des boutons. Vérifiez le résultat réel dans chaque contexte. Ne supposez pas que le thème Shell utilisateur contrôle l'écran de connexion GDM : GDM utilise un contexte système distinct et ses propres contraintes de privilèges.

## 10. Clair, sombre et contraste élevé

Un thème Shell peut être chargé dans différents schémas de couleurs. Le fichier source 51.0 contient des branches Sass pour la variante claire et le contraste élevé.

Si vous écrivez un CSS statique, vous devez choisir explicitement vos couleurs. Une feuille statique ne récupère pas automatiquement toutes les variables Sass de GNOME.

Bonnes pratiques :
- conservez un contraste de texte suffisant ;
- ne dépendez pas uniquement de la couleur pour signaler un état ;
- gardez le focus clavier visible ;
- préservez les indicateurs de confidentialité ;
- testez la lisibilité sur le fond du bureau ;
- vérifiez les icônes symboliques et les indicateurs de faible taille.

Exemple de variante claire manuelle :

```css
/* À tester comme thème distinct, pas comme pseudo-variable CSS. */
#panel.light-theme {
  background-color: #f6f5f4;
  color: #241f31;
  border-bottom: 1px solid #c0bfbc;
}

#panel.light-theme .panel-button {
  color: #241f31;
}
```

La classe `.light-theme` ci-dessus est un exemple inventé pour un thème qui ajouterait explicitement cette classe. GNOME Shell ne l'ajoute pas automatiquement : ne copiez pas cette règle sans fournir le mécanisme qui pose la classe.

## 11. Propriétés CSS et propriétés St rencontrées

Les propriétés suivantes sont utiles dans ce composant :

- `background-color` : couleur de surface.
- `color` : couleur du texte et, selon le widget, de l'icône.
- `border` et `border-bottom` : bordures.
- `border-radius` : arrondi.
- `box-shadow` : ombre, selon le support du moteur St.
- `padding`, `margin` : espacements internes et externes.
- `font-weight` : graisse.
- `height`, `min-width`, `min-height` : dimensions.
- `spacing` : espacement des enfants des conteneurs St.
- `icon-size` : taille d'icône St.
- `-natural-hpadding` et `-minimum-hpadding` : propriétés spécifiques St utilisées par le thème natif.
- `transition-duration` : durée de transition prise en charge par St.

Ne transposez pas ces propriétés vers GTK 3 ou GTK 4 sans vérifier leur compatibilité. `icon-size` et les propriétés préfixées `-natural-` ne sont pas des propriétés CSS web universelles.

## 12. Diagnostic : le panneau ne change pas

Suivez cette séquence :

1. Vérifiez que le thème Shell est réellement activé.
2. Vérifiez que le fichier modifié est bien celui qui est chargé.
3. Vérifiez que la syntaxe CSS est valide.
4. Testez un changement évident sur `#panel`.
5. Vérifiez que le sélecteur cible le bon contexte : bureau, vue Activités ou verrouillage.
6. Inspectez les règles gagnantes et leur priorité.
7. Vérifiez qu'une extension ne remplace pas le style de l'indicateur.
8. Rechargez le thème selon la méthode autorisée par votre environnement de test.

Ne tentez pas de redémarrer le Shell sur une session de travail simplement pour forcer le rechargement. Utilisez la session imbriquée ou la machine virtuelle prévue pour les tests.

## 13. Exercices progressifs

### Exercice A — panneau minimal

- Modifier uniquement le fond.
- Ajouter une bordure inférieure.
- Vérifier les trois zones du panneau.
- Vérifier la vue Activités.

### Exercice B — boutons cohérents

- Définir un rayon commun.
- Définir un état de survol.
- Définir un état actif.
- Vérifier le focus clavier.
- Vérifier les menus et les boutons d'extension.

### Exercice C — horloge et indicateurs

- Modifier l'espacement de l'horloge.
- Modifier la taille des icônes système.
- Vérifier Ne pas déranger.
- Vérifier réseau, son et alimentation.
- Vérifier l'enregistrement et le partage d'écran sans masquer leur signalement.

### Exercice D — validation

- Tester une session claire et une session sombre.
- Tester une échelle d'affichage supérieure.
- Tester une langue avec des libellés longs.
- Tester le clavier uniquement.
- Consigner la version de GNOME Shell et les sélecteurs utilisés.

Le chapitre est terminé lorsque vous pouvez expliquer quelle règle modifie chaque élément et démontrer que les états interactifs et les indicateurs de sécurité restent visibles.
