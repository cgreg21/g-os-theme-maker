# Créer son premier thème complet

Ce tutoriel construit un petit thème cohérent. Il ne cherche pas à recolorer tout GNOME d'un seul coup : il établit une base propre que vous pourrez enrichir.

## 1. Choisir une identité visuelle

Commencez par cinq décisions simples :
- une couleur de surface principale ;
- une couleur de surface secondaire ;
- une couleur de texte principale ;
- une couleur de texte secondaire ;
- une couleur d'accent pour les actions et la sélection.

Exemple de palette :
- fond : `#242424` ;
- surface : `#303030` ;
- surface élevée : `#3b3b3b` ;
- texte : `#f6f5f4` ;
- texte secondaire : `#c0bfbc` ;
- accent : `#3584e4` ;
- bordure : `#555555` ;
- erreur : `#e01b24`.

Une palette n'est pas encore un thème. Elle sert à garder les mêmes couleurs dans les différents moteurs.

## 2. Créer l'arborescence

```text
MonTheme/
├── README.md
├── gnome-shell/
│   └── gnome-shell.css
├── gtk-3.0/
│   └── gtk.css
└── gtk-4.0/
    └── gtk.css
```

Ne créez pas de dossier d'icônes ou de curseurs vide en prétendant qu'il s'agit d'un thème complet. Ajoutez ces ressources uniquement lorsque vous avez réellement les fichiers et leur métadonnée.

## 3. Créer les feuilles de style

Dans `gtk-3.0/gtk.css`, commencez par :

```css
/* Palette du thème */
@define-color theme_bg_color #242424;
@define-color theme_fg_color #f6f5f4;
@define-color theme_base_color #303030;
@define-color theme_text_color #f6f5f4;
@define-color theme_selected_bg_color #3584e4;
@define-color theme_selected_fg_color #ffffff;

/* Fenêtres et surfaces */
window,
.background {
  background-color: @theme_bg_color;
  color: @theme_fg_color;
}

/* Boutons */
button {
  color: @theme_fg_color;
  background-color: #3b3b3b;
  border: 1px solid #555555;
  border-radius: 8px;
  padding: 7px 12px;
}

/* Survol */
button:hover {
  background-color: #484848;
}

/* Appui */
button:active {
  background-color: #202020;
}

/* Clavier : garder un focus visible */
button:focus {
  outline: 2px solid #78aeed;
  outline-offset: 2px;
}
```

Les couleurs nommées avec `@define-color` sont des variables GTK 3. Cette syntaxe n'est pas identique aux variables CSS web. Ne copiez pas automatiquement ces déclarations dans une feuille GTK 4 ou Shell.

Dans `gtk-4.0/gtk.css`, utilisez une feuille indépendante :

```css
window,
.background {
  background-color: #242424;
  color: #f6f5f4;
}

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

button:focus-visible {
  outline: 2px solid #78aeed;
  outline-offset: 2px;
}
```

Les sélecteurs et pseudo-classes disponibles varient selon GTK et les widgets. Validez la feuille avec la version GTK réellement installée.

## 4. Donner un style au Shell

Dans `gnome-shell/gnome-shell.css` :

```css
/* Panneau supérieur */
#panel {
  background-color: #242424;
  color: #f6f5f4;
  border-bottom: 1px solid #555555;
}

/* Boutons du panneau */
#panel .panel-button {
  border-radius: 8px;
  padding: 0 10px;
  color: #f6f5f4;
}

/* Retour visuel au survol */
#panel .panel-button:hover {
  background-color: #484848;
}

/* Menus */
.popup-menu-content {
  background-color: #303030;
  color: #f6f5f4;
  border: 1px solid #555555;
  border-radius: 12px;
}

/* Lignes de menu */
.popup-menu-item {
  padding: 8px 12px;
  border-radius: 7px;
}

/* Ligne sélectionnée au survol */
.popup-menu-item:hover {
  background-color: #484848;
}
```

Ces sélecteurs sont des repères d'implémentation de GNOME Shell 51, pas une API garantie pour les versions futures. Vérifiez-les dans les sources de la version exacte. Un sélecteur valide peut aussi ne rien changer si l'élément n'est pas présent dans l'état affiché.

## 5. Comprendre les états

Un bouton n'a pas une seule apparence :
- normal : il attend une action ;
- hover : le pointeur se trouve dessus ;
- focus : le clavier l'a sélectionné ;
- active : l'utilisateur appuie dessus ;
- checked : il est activé ou sélectionné ;
- disabled : l'action n'est pas disponible.

Ne confondez pas hover et focus. Une personne qui navigue au clavier doit pouvoir identifier le contrôle courant sans souris. N'utilisez pas uniquement une couleur pour indiquer une sélection.

## 6. Tester sans casser la session

Testez d'abord les applications GTK avec un thème utilisateur. Pour Shell, utilisez une session GNOME imbriquée si votre environnement le permet. Ne redémarrez pas brutalement le Shell sur une session de travail importante.

Après chaque changement :
1. sauvegardez le fichier ;
2. rechargez le thème avec la méthode adaptée au moteur ;
3. affichez l'élément et son état ;
4. vérifiez le texte, le focus, les icônes et les contrastes ;
5. consultez les journaux en cas d'erreur ;
6. revenez au dernier changement si le rendu se dégrade.

## 7. Écrire un README pour son thème

Le README doit donner le nom et la version du thème, les cibles couvertes, les versions GNOME/GTK testées, les ressources incluses, les licences, l'installation, la désinstallation et les limites connues. Indiquez clairement si les icônes, curseurs, polices ou fonds sont absents.

## 8. Pour aller plus loin

Une fois le premier rendu validé, poursuivez dans cet ordre : champs de saisie, menus et popovers, listes, barres de défilement, dialogues, états d'erreur, variantes clair/sombre, puis icônes et curseurs. Cette progression évite de multiplier les variables avant de comprendre leur effet.
