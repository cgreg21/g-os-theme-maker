# Clavier virtuel, saisie, IBus et accessibilité du Shell

Ce chapitre couvre les éléments du Shell liés à la saisie et à l'accessibilité : clavier à l'écran, suggestions, panneaux de caractères, méthodes de saisie et aides visuelles. Ces interfaces ne sont pas toujours visibles. Leur présence dépend de la langue, du matériel, des méthodes de saisie configurées et des options d'accessibilité activées.

Les sélecteurs sont ceux de l'inventaire GNOME Shell 51.0. Ils peuvent changer : vérifiez la version installée avant de les réutiliser.

## 1. Clavier virtuel

Le clavier à l'écran est une interface du Shell, pas un clavier GTK ordinaire. Les principaux sélecteurs recensés sont :

- #keyboard : conteneur du clavier ;
- .key-container : conteneur d'une touche ;
- .keyboard-key : touche ;
- .default-key : touche ayant un rôle particulier ;
- .keyboard-subkeys-boxpointer : panneau des variantes affichées lors d'un appui prolongé ;
- .emoji-page et .emoji-panel : zone de sélection des emoji ;
- .word-suggestions : suggestions de mots.

Exemple :

~~~css
#keyboard {
  spacing: 6px;
}

#keyboard .keyboard-key {
  border-radius: 8px;
  padding: 8px;
  min-height: 42px;
}

#keyboard .keyboard-key:active {
  background-color: #3584e4;
  color: #ffffff;
}

.keyboard-subkeys-boxpointer {
  border-radius: 12px;
  padding: 8px;
}

.word-suggestions {
  spacing: 10px;
}
~~~

Les dimensions sont des valeurs de départ. Le clavier doit rester utilisable sur un écran tactile : ne réduisez pas les touches pour gagner de la place. Vérifiez les variantes d'une touche, les touches spéciales, les caractères accentués et les dispositions linguistiques.

### Vérifications

- Activez le clavier à l'écran dans les paramètres d'accessibilité.
- Essayez une disposition française et une autre disposition.
- Testez les touches avec variantes et les appuis prolongés.
- Vérifiez le panneau emoji et les suggestions.
- Testez avec un facteur d'échelle différent.

## 2. Champs Shell et états de saisie

Les champs du Shell peuvent être construits avec StEntry. Les classes et repères transversaux comprennent :

- StEntry : champ de saisie St ;
- .capslock-warning : avertissement de verrouillage majuscule ;
- .peek-password : contrôle d'affichage du mot de passe ;
- .hint-text : texte d'aide ou d'indication.

Exemple :

~~~css
StEntry {
  border-radius: 9px;
  padding: 8px 10px;
}

StEntry:focus {
  border-color: #78aeed;
}

.capslock-warning {
  color: #f9a825;
  font-weight: 700;
}

.hint-text {
  opacity: 0.8;
}
~~~

Les noms de pseudo-classes et les propriétés prises en charge dépendent du widget St et de son thème. N'appliquez pas automatiquement la syntaxe CSS d'un navigateur. Le champ doit conserver un focus visible et un contraste suffisant.

Ne masquez jamais un avertissement de verrouillage majuscule ou un contrôle d'affichage de mot de passe pour des raisons purement esthétiques.

## 3. Méthodes de saisie IBus

IBus permet d'utiliser des méthodes de saisie qui ne correspondent pas directement à une touche physique : composition de caractères, saisie de langues asiatiques, choix de candidats et navigation entre pages.

Les sélecteurs repérés dans GNOME Shell 51.0 comprennent :

- .candidate-popup-boxpointer : conteneur du popup de candidats ;
- .candidate-popup-content : contenu du popup ;
- .candidate-index : index d'un candidat ;
- .candidate-box : candidat ;
- .candidate-page-button : bouton de pagination ;
- .candidate-page-button-previous et .candidate-page-button-next : navigation précédente et suivante.

Exemple :

~~~css
.candidate-popup-boxpointer {
  border-radius: 12px;
  padding: 8px;
}

.candidate-popup-content {
  spacing: 6px;
}

.candidate-box {
  border-radius: 8px;
  padding: 6px 10px;
}

.candidate-box:selected,
.candidate-box:focus {
  background-color: #3584e4;
  color: #ffffff;
}

.candidate-index {
  opacity: 0.75;
}

.candidate-page-button {
  border-radius: 8px;
  padding: 6px;
}
~~~

Vérifiez les états réellement employés par la version installée avant de conserver les pseudo-classes de l'exemple. Un candidat sélectionné doit rester identifiable sans dépendre uniquement de la couleur.

### Test IBus

1. Configurez une méthode de saisie supplémentaire dans les paramètres.
2. Activez cette méthode depuis le sélecteur de langue du panneau.
3. Ouvrez un champ de texte dans une application.
4. Saisissez une séquence qui ouvre le panneau de candidats.
5. Parcourez les candidats et les pages avec le clavier.
6. Vérifiez que le popup ne sort pas de l'écran et reste lisible.

Une session sans méthode de saisie supplémentaire ne permet pas de valider cette partie du thème.

## 4. Aides visuelles d'accessibilité

Le Shell fournit plusieurs éléments d'aide visuelle :

- .ripple-pointer-location : indication visuelle de l'emplacement du pointeur ;
- .pie-timer : minuteur visuel ;
- .magnifier-zoom-region : région de zoom de la loupe ;
- .select-area-rubberband : rectangle de sélection d'une zone.

Exemple :

~~~css
.ripple-pointer-location {
  border: 2px solid #ffffff;
  background-color: rgba(53, 132, 228, 0.35);
}

.pie-timer {
  color: #ffffff;
}

.select-area-rubberband {
  border: 2px solid #3584e4;
  background-color: rgba(53, 132, 228, 0.12);
}
~~~

La loupe peut afficher une zone agrandie et modifier la perception des couleurs et des contours. Testez son rendu sur plusieurs arrière-plans et ne réduisez pas sa visibilité.

## 5. Ce que le CSS ne peut pas corriger

Le thème ne remplace pas l'arbre d'accessibilité d'une application. Les rôles, noms accessibles, descriptions, ordre de lecture et annonces vocales sont fournis par les widgets, les applications et AT-SPI.

Le CSS ne peut pas :

- donner un nom accessible à un bouton qui n'en possède pas ;
- corriger l'ordre de lecture d'un lecteur d'écran ;
- rendre accessible au clavier une action qui ne reçoit aucun événement clavier ;
- transformer un texte intégré dans une image en texte sélectionnable ;
- corriger une annonce vocale manquante.

Quand un problème relève de ces comportements, il faut corriger le composant ou l'application, pas ajouter une règle CSS.

## 6. Contraste, focus et réduction des animations

Pour chaque composant de saisie, prévoyez les états suivants :

- repos ;
- survol ;
- focus clavier ;
- activation ;
- sélection ;
- indisponibilité ;
- erreur ;
- avertissement ;
- chargement.

Le focus doit rester visible. Les messages d'erreur et d'avertissement doivent associer une couleur à un libellé ou un symbole. Ne réduisez pas l'opacité au point de rendre un texte secondaire illisible.

Respectez les préférences GNOME de contraste élevé et de réduction des animations. Ne supposez pas que la propriété CSS du navigateur prefers-reduced-motion est prise en charge par St. Les mécanismes de préférence sont différents selon le moteur.

## 7. Langues, direction et caractères

Testez le thème dans au moins deux contextes linguistiques :

- français ou anglais, de gauche à droite ;
- une langue de droite à gauche, si elle fait partie des usages ciblés.

Vérifiez les marges logiques, l'ordre des boutons, les flèches directionnelles, les textes longs, les chiffres, les accents et les glyphes. Ne retournez pas les icônes non directionnelles.

Le clavier virtuel et IBus doivent être testés avec les méthodes de saisie réellement configurées. Un thème qui fonctionne uniquement avec une disposition française n'est pas un thème internationalisé.

## 8. Exercices

### Exercice A — clavier virtuel

Augmentez le rayon des touches et vérifiez leur taille tactile, les touches spéciales et les variantes.

### Exercice B — IBus

Modifiez le style d'un candidat et vérifiez la sélection, la pagination et la navigation clavier.

### Exercice C — focus

Vérifiez que le focus est visible dans les champs Shell, les candidats et les touches du clavier virtuel.

### Exercice D — contraste élevé

Activez le contraste élevé et vérifiez que les textes, icônes et contours restent identifiables.

## 9. Sources amont GNOME Shell 51.0

- [Clavier virtuel — keyboard.js](https://gitlab.gnome.org/GNOME/gnome-shell/-/blob/51.0/js/ui/keyboard.js)
- [Méthodes de saisie — ibusCandidatePopup.js](https://gitlab.gnome.org/GNOME/gnome-shell/-/blob/51.0/js/ui/ibusCandidatePopup.js)
- [Thème Shell — widgets SCSS](https://gitlab.gnome.org/GNOME/gnome-shell/-/tree/51.0/data/theme/gnome-shell-sass/widgets)
- [Accessibilité GNOME](https://help.gnome.org/users/gnome-help/stable/a11y.html)
- [Documentation St](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/)
