# Composants Shell spécialisés : espaces, avatars, défilement et dialogues avancés

![Capture officielle GNOME des espaces de travail](images/official/shell-workspaces.png)

Les chapitres précédents couvrent les grandes zones de GNOME Shell. Il reste des composants plus spécialisés, visibles seulement dans certaines situations : sélecteur d'espace de travail, fenêtre de redimensionnement, dialogues de permission, sélection audio, avatars, liens et aides visuelles.

Ce chapitre complète l'inventaire GNOME Shell 51.0. Il s'appuie sur les sélecteurs présents dans le catalogue et évite d'inventer des classes pour les modules dont les noms internes doivent être inspectés dans la source.

## 1. Sélecteur d'espace de travail

Le sélecteur d'espace de travail peut apparaître lors de raccourcis ou de gestes de navigation. Les repères CSS recensés sont :

- .workspace-switcher : conteneur ;
- .ws-switcher-indicator : indicateur de l'espace sélectionné.

Exemple :

~~~css
.workspace-switcher {
  border-radius: 14px;
  padding: 8px;
}

.ws-switcher-indicator {
  border: 2px solid #78aeed;
  border-radius: 8px;
}
~~~

Testez avec un, deux puis plusieurs espaces de travail. Vérifiez la sélection clavier, les animations et la visibilité de l'indicateur sur les fonds clair et sombre.

Ne confondez pas ce sélecteur temporaire avec la colonne des miniatures de la vue Activités.

## 2. Popup de redimensionnement

Le Shell peut afficher une fenêtre temporaire lors de certaines opérations de redimensionnement. Le sélecteur recensé est .resize-popup.

~~~css
.resize-popup {
  border-radius: 10px;
  padding: 8px 12px;
  background-color: rgba(32, 32, 32, 0.94);
  color: #ffffff;
}
~~~

La présence de ce popup dépend de la méthode de redimensionnement et du gestionnaire de fenêtres. Testez les opérations avec le clavier et la souris. Ne masquez pas les dimensions ou indications utiles à l'utilisateur.

## 3. Avatars et icônes utilisateur

Le Shell utilise plusieurs éléments visuels pour représenter un compte ou un utilisateur :

- .user-icon ;
- .user-avatar ;
- .user-widget ;
- .framed-user-icon dans les interfaces qui utilisent un avatar encadré.

Exemple de règle prudente :

~~~css
.user-avatar,
.user-icon {
  border-radius: 999px;
}
~~~

Le style ne doit pas déformer les images. Vérifiez les avatars carrés, les images manquantes, les comptes sans photo et les variantes de taille.

Les interfaces de connexion et de déverrouillage peuvent utiliser d'autres classes spécifiques : ne supposez pas qu'une règle sur .user-avatar couvre toutes les vues.

## 4. Liens Shell

La classe .shell-link identifie des liens dans certaines interfaces du Shell.

~~~css
.shell-link {
  color: #78aeed;
  text-decoration: underline;
}

.shell-link:focus {
  outline: 2px solid #78aeed;
  outline-offset: 2px;
}
~~~

Un lien doit être reconnaissable sans survol. Vérifiez sa lisibilité sur les fonds de dialogue, dans les messages et en navigation clavier.

## 5. Icônes basse résolution et ombres

Le thème Shell contient des classes transversales pour certains traitements d'icônes :

- .lowres-icon ;
- .icon-dropshadow.

Elles peuvent servir à distinguer ou améliorer la lisibilité d'icônes selon le contexte. Ne supprimez pas systématiquement les ombres : elles peuvent assurer le contraste sur un fond variable.

Exemple :

~~~css
.icon-dropshadow {
  icon-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
}
~~~

La propriété icon-shadow est spécifique à St. Elle n'est pas une propriété CSS standard du navigateur.

## 6. Défilement St

Les interfaces Shell utilisent StScrollView et StScrollBar. Les repères de style incluent StScrollBar, .vhandle et .hhandle.

~~~css
StScrollBar {
  -bar-width: 8px;
}

StScrollBar .vhandle,
StScrollBar .hhandle {
  background-color: rgba(255, 255, 255, 0.45);
  border-radius: 999px;
}
~~~

Les propriétés St et les nœuds disponibles doivent être vérifiés dans la version installée. Les barres de défilement peuvent être verticales ou horizontales et leur poignée peut apparaître seulement au survol.

Ne réduisez pas la zone interactive au point de rendre le défilement difficile. Testez au clavier, à la souris et avec un écran tactile.

## 7. Dialogues de permission et d'accès

Les dialogues de permission ne sont pas de simples messages. Ils peuvent demander une authentification ou l'autorisation d'accéder à une ressource.

Les classes recensées dans GNOME Shell 51.0 comprennent :

- .prompt-dialog ;
- .prompt-dialog-password-grid ;
- .prompt-dialog-password-entry ;
- .prompt-dialog-error-label ;
- .prompt-dialog-info-label ;
- .polkit-dialog-user-layout ;
- .polkit-dialog-user-label ;
- .polkit-dialog-user-root-label ;
- .access-dialog.

Exemple :

~~~css
.prompt-dialog-password-entry {
  border-radius: 8px;
  padding: 8px 10px;
}

.prompt-dialog-error-label {
  color: #c01c28;
  font-weight: 700;
}

.prompt-dialog-info-label {
  opacity: 0.85;
}
~~~

Ne masquez jamais une erreur d'authentification, un nom d'utilisateur ou une indication de permission. Vérifiez le contraste et la navigation clavier.

## 8. Sélection d'un périphérique audio

Le dialogue de sélection audio peut apparaître lorsque le système propose plusieurs périphériques de sortie ou d'entrée.

Les classes recensées sont :

- .audio-device-selection-dialog ;
- .audio-selection-box ;
- .audio-selection-device ;
- .audio-selection-device-box ;
- .audio-selection-device-icon.

Exemple :

~~~css
.audio-device-selection-dialog {
  border-radius: 16px;
}

.audio-selection-device {
  border-radius: 10px;
  padding: 8px;
}

.audio-selection-device:focus {
  outline: 2px solid #78aeed;
}
~~~

Testez avec plusieurs périphériques, un périphérique débranché et un nom long. L'utilisateur doit comprendre quel périphérique est sélectionné.

## 9. Contrôle parental, sessions et redémarrage

D'autres interfaces spécialisées peuvent apparaître selon les services installés et la configuration de la session :

- .parental-controls-shield, .parental-controls-shield-title, .parental-controls-shield-description et .parental-controls-shield-button ;
- .conflicting-session-dialog-content, .conflicting-session-dialog-title et .conflicting-session-dialog-desc ;
- .restart-message ;
- .welcome-dialog-image.

Ces interfaces ne sont pas présentes dans toutes les sessions. Un sélecteur sans effet peut simplement correspondre à une fonction non activée.

Ne supprimez pas les messages de contrôle parental, de conflit de session ou de redémarrage. Ils expliquent un état système ou une action requise.

## 10. QR codes et retours visuels

Le thème GNOME Shell 51 contient des modules dédiés aux QR codes et aux retours visuels de clic, notamment _qr-code.scss et _corner-ripple.scss.

Le nom du fichier SCSS ne suffit pas à déduire le nom des nœuds CSS. Pour personnaliser ces composants :

1. ouvrez le fichier SCSS de la version 51.0 ;
2. relevez les sélecteurs réellement définis ;
3. recherchez dans le code JavaScript où ils sont ajoutés ;
4. vérifiez dans Looking Glass qu'ils existent dans le contexte testé ;
5. écrivez une règle ciblée et testez-la.

Ne créez pas un sélecteur supposé comme .qr-code si le fichier amont ne le déclare pas. Cette règle évite de documenter un nom qui ne correspond à aucun acteur.

## 11. Exercices

### Exercice A — workspace switcher

Modifiez le contour de l'indicateur et vérifiez plusieurs espaces de travail.

### Exercice B — avatar

Ajustez le rayon d'un avatar et testez une image manquante et une image non carrée.

### Exercice C — dialogue de permission

Améliorez le champ et l'état d'erreur sans masquer les messages de sécurité.

### Exercice D — défilement

Modifiez la largeur de la poignée et vérifiez la navigation tactile et clavier.

### Exercice E — inspection d'un composant rare

Choisissez un composant qui n'apparaît pas au démarrage, activez le contexte qui le fait apparaître, puis inspectez ses classes dans Looking Glass.

## 12. Sources GNOME Shell 51.0

- [Thème Shell — widgets SCSS](https://gitlab.gnome.org/GNOME/gnome-shell/-/tree/51.0/data/theme/gnome-shell-sass/widgets)
- [Code JavaScript du Shell](https://gitlab.gnome.org/GNOME/gnome-shell/-/tree/51.0/js/ui)
- [Documentation St](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/)
- [GNOME Shell — notes de version](https://release.gnome.org/51/)
