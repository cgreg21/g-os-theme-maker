# OSD, dialogues système, sélecteurs de fenêtres et capture d'écran

![Outil de capture d’écran officiel de GNOME 51](images/official/screenshot-tool.png)

Cette capture issue de GNOME User Documentation 51 sert de référence visuelle pour l’interface de capture ; les OSD et dialogues décrits plus loin sont d’autres composants.

Ce chapitre couvre les petites interfaces qui apparaissent au-dessus du bureau : indicateurs de volume et de luminosité, boîtes de dialogue, fenêtre d'exécution, sélecteur Alt-Tab et outil de capture. Elles sont parfois visibles quelques secondes seulement, mais elles font partie du thème GNOME Shell.

Les sélecteurs cités sont issus de l'inventaire GNOME Shell 51.0. Ils ne sont pas une API stable. Vérifiez toujours les sources de la version installée.

## 1. Comprendre les interfaces superposées

Une interface superposée n'est pas forcément une fenêtre GTK. Dans GNOME Shell, beaucoup de ces éléments sont des acteurs St/Clutter dessinés directement par le Shell. Leur style se trouve dans le thème Shell, pas dans le thème GTK de vos applications.

Les principaux groupes sont :

- les OSD qui confirment une action matérielle ou système ;
- les dialogues modaux qui demandent une décision ;
- les dialogues d'authentification et de permission ;
- le sélecteur de fenêtres Alt-Tab ;
- la fenêtre de commande Alt-F2 ;
- l'interface de capture d'écran et d'enregistrement.

Ne confondez pas ces interfaces avec les fenêtres natives des applications. Une règle GTK sur button ne modifie pas nécessairement un bouton St du Shell.

## 2. OSD : volume, luminosité et retours système

OSD signifie *On-Screen Display*. Le Shell affiche ces indicateurs lorsqu'une action système est déclenchée : changement de volume, luminosité, périphérique audio ou autre retour visuel.

Les sélecteurs principaux sont :

- .osd-window : conteneur de l'indicateur ;
- .level : niveau visuel, par exemple la progression du volume ;
- .osd-monitor-label : indication de l'écran concerné ;
- .osd-break-countdown-label : compte à rebours associé à certains rappels.

Exemple de style :

~~~css
.osd-window {
  border-radius: 18px;
  padding: 14px 20px;
  background-color: rgba(32, 32, 32, 0.94);
  color: #ffffff;
}

.osd-window .level {
  border-radius: 999px;
  min-height: 8px;
}

.osd-monitor-label {
  border-radius: 10px;
  padding: 6px 10px;
}
~~~

Ce code donne une direction visuelle. Il ne faut pas supposer que tous les OSD contiennent un curseur .level ou le même nombre d'enfants.

### Comment tester un OSD

- Utilisez les touches matérielles de volume.
- Modifiez la luminosité si l'écran et le pilote exposent ce réglage.
- Branchez ou débranchez un périphérique audio.
- Si vous avez plusieurs écrans, vérifiez l'indication du moniteur.
- Répétez le test avec un facteur d'échelle différent.

Ne masquez pas les OSD pour obtenir un bureau plus épuré : ils confirment à l'utilisateur qu'une action a été prise en compte.

## 3. Dialogues modaux

Un dialogue modal bloque temporairement les interactions avec le reste du Shell. Il peut demander une confirmation, signaler une erreur ou proposer une action système.

Les classes générales recensées dans le thème 51.0 sont :

- .modal-dialog : conteneur du dialogue ;
- .modal-dialog-content-box : zone de contenu ;
- .modal-dialog-button-box : groupe des actions ;
- .modal-dialog-button : bouton ;
- .dialog-list : liste d'éléments ;
- .dialog-list-title : titre de la liste ;
- .dialog-list-scrollview : zone défilante ;
- .dialog-list-box : conteneur des lignes ;
- .dialog-list-item : ligne individuelle ;
- .message-dialog-content : contenu d'un message ;
- .message-dialog-title : titre ;
- .message-dialog-description : description.

Exemple :

~~~css
.modal-dialog {
  border-radius: 18px;
  padding: 18px;
}

.modal-dialog-content-box {
  spacing: 12px;
}

.modal-dialog-button-box {
  spacing: 8px;
}

.modal-dialog-button {
  border-radius: 999px;
  padding: 8px 16px;
}

.modal-dialog-button:default {
  background-color: #3584e4;
  color: #ffffff;
}
~~~

Les dialogues ne sont pas tous identiques. Certains héritent de ces classes puis ajoutent leurs propres sélecteurs. Le style général doit rester compatible avec les variantes de confirmation, d'erreur, de batterie faible et de fin de session.

### États à contrôler

- bouton normal ;
- survol ;
- focus clavier ;
- activation ;
- bouton par défaut ;
- bouton désactivé ;
- texte long ;
- contenu défilant ;
- disposition droite-à-gauche.

Ne supprimez pas le focus visible. Ne donnez pas le même aspect à une action destructive et à une action de validation ordinaire.

## 4. Fin de session et avertissement batterie

Les dialogues de fermeture et de fin de session utilisent notamment :

- .end-session-dialog ;
- .end-session-dialog-battery-warning ;
- .message-dialog-content ;
- .message-dialog-title ;
- .message-dialog-description.

Ils peuvent proposer la fermeture de session, le redémarrage ou l'arrêt. Leur apparence doit clairement distinguer l'action principale, l'annulation et les avertissements.

Exemple prudent :

~~~css
.end-session-dialog {
  border-radius: 18px;
}

.end-session-dialog-battery-warning {
  color: #f9a825;
  font-weight: 700;
}
~~~

Un avertissement ne doit pas dépendre uniquement de sa couleur : le texte et l'icône doivent conserver leur sens.

## 5. Dialogue d'exécution Alt-F2

La fenêtre d'exécution permet de saisir une commande dans le Shell. Elle est associée à :

- .run-dialog : conteneur ;
- .run-dialog-entry : champ de saisie ;
- .run-dialog-description : aide ou description.

Exemple :

~~~css
.run-dialog {
  border-radius: 14px;
  padding: 12px;
}

.run-dialog-entry {
  border-radius: 10px;
  padding: 8px 12px;
}

.run-dialog-description {
  opacity: 0.8;
}
~~~

Pour tester l'apparence, ouvrez la fenêtre avec Alt-F2 puis fermez-la sans exécuter de commande. N'utilisez pas un thème en développement pour tester des commandes système inconnues.

## 6. Sélecteur de fenêtres Alt-Tab

Alt-Tab affiche un sélecteur de fenêtres ou d'applications selon les préférences et le contexte. Les éléments visuels repérés dans le thème Shell comprennent :

- .switcher-popup : surface générale ;
- .switcher-list : liste des choix ;
- .switcher-list-item-container : conteneur d'un choix ;
- .item-box : élément sélectionnable ;
- .thumbnail-box et .thumbnail : aperçu de fenêtre ;
- .switcher-arrow : indicateur de navigation ;
- .cycler-highlight : mise en évidence de la fenêtre ciblée.

Exemple :

~~~css
.switcher-popup {
  border-radius: 18px;
  padding: 12px;
}

.switcher-list {
  spacing: 8px;
}

.switcher-list .item-box {
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 12px;
  padding: 8px;
}

.switcher-arrow {
  color: #ffffff;
}
~~~

La pseudo-classe exacte utilisée par le thème pour l'élément sélectionné doit être vérifiée dans le SCSS 51.0. L'exemple ci-dessus ne doit pas remplacer les états natifs sans inspection.

### Vérifications

- Plusieurs fenêtres d'une même application.
- Plusieurs applications.
- Navigation avec Tab et les flèches.
- Fenêtres avec des titres longs.
- Plusieurs écrans.
- Aperçus de fenêtres de tailles différentes.

Un aperçu ne doit pas être rogné de manière à masquer le contenu qui permet d'identifier la fenêtre.

## 7. Interface de capture d'écran

GNOME Shell possède une interface de capture intégrée. Elle permet de sélectionner une zone, une fenêtre ou un écran, de choisir certains paramètres et de lancer une capture ou un enregistrement.

Les sélecteurs recensés pour GNOME Shell 51.0 comprennent :

- .screenshot-ui-panel : panneau principal ;
- .screenshot-ui-close-button : fermeture ;
- .screenshot-ui-type-button : choix du type de capture ;
- .screenshot-ui-capture-button : action de capture ;
- .screenshot-ui-capture-button-circle : indicateur circulaire ;
- .screenshot-ui-shot-cast-container et .screenshot-ui-shot-cast-button : capture vidéo et diffusion ;
- .screenshot-ui-show-pointer-button : affichage du pointeur ;
- .screenshot-ui-area-selector : sélection de zone ;
- .screenshot-ui-area-indicator-shade : voile autour de la sélection ;
- .screenshot-ui-area-indicator-selection : rectangle sélectionné ;
- .screenshot-ui-area-selector-handle : poignées de sélection ;
- .screenshot-ui-window-selector et .screenshot-ui-window-selector-window : sélection de fenêtre ;
- .screenshot-ui-window-selector-window-border : contour de la fenêtre ;
- .screenshot-ui-window-selector-check : indication de sélection ;
- .screenshot-ui-screen-selector : sélection d'écran ;
- .screenshot-ui-tooltip : infobulle.

Exemple de personnalisation de la surface :

~~~css
.screenshot-ui-panel {
  border-radius: 18px;
  padding: 12px;
}

.screenshot-ui-type-button,
.screenshot-ui-close-button,
.screenshot-ui-show-pointer-button {
  border-radius: 999px;
}

.screenshot-ui-area-indicator-selection {
  border: 2px solid #78aeed;
}
~~~

L'interface de capture est un outil de travail. Préservez les indications de sélection, les poignées et le contraste entre la zone choisie et le voile extérieur. Les poignées doivent rester faciles à saisir.

### Test complet

1. Ouvrez l'outil avec le raccourci de capture d'écran de GNOME.
2. Sélectionnez une zone.
3. Déplacez et redimensionnez la sélection.
4. Basculez entre zone, fenêtre et écran.
5. Vérifiez le bouton de capture et le bouton de fermeture.
6. Testez l'option d'affichage du pointeur.
7. Vérifiez le comportement sur un écran HiDPI et avec plusieurs moniteurs.

## 8. OSD des tablettes graphiques

Certains environnements affichent un OSD de configuration de tablette graphique. Les classes repères sont :

- .pad-osd-window ;
- .pad-osd-title-box ;
- .combo-box-label.

Ces éléments ne sont visibles que si le matériel, le pilote et la configuration exposent cette interface. Il est inutile de conclure qu'un sélecteur est incorrect parce que l'élément n'apparaît pas sur un ordinateur sans tablette.

## 9. Méthode de diagnostic

Quand une règle ne semble pas agir :

1. Vérifiez que le composant appartient au Shell et non à une application GTK.
2. Vérifiez que le sélecteur est présent dans la version installée.
3. Ouvrez Looking Glass pour examiner l'acteur lorsqu'il est visible.
4. Inspectez les règles CSS chargées et les erreurs du Shell.
5. Désactivez temporairement les extensions qui remplacent l'interface concernée.
6. Retestez sans autre modification.

Les OSD sont éphémères : préparez le changement CSS avant de déclencher l'action. Pour les interfaces de capture et Alt-Tab, gardez un moyen de fermer l'interface même si le style est mauvais.

## 10. Exercices

### Exercice A — OSD

Modifiez le rayon du panneau et contrôlez les retours de volume et de luminosité.

### Exercice B — dialogue

Personnalisez les boutons d'un dialogue modal et vérifiez le focus, l'action par défaut et les états désactivés.

### Exercice C — Alt-Tab

Augmentez l'espacement entre les éléments sans masquer les aperçus. Testez avec plusieurs fenêtres.

### Exercice D — capture

Modifiez le contour de sélection et vérifiez que la zone choisie reste évidente sur des fonds clairs et sombres.


## 11. Préparer les tests des interfaces éphémères

Les OSD et certains dialogues disparaissent rapidement. Préparez donc le scénario avant de recharger le thème :

1. Gardez le terminal ou Looking Glass accessible sur un autre espace de travail.
2. Préparez la règle CSS dans le fichier de développement, sans déclencher l'action système.
3. Rechargez le thème selon la méthode de test de votre session.
4. Déclenchez une seule action : volume, luminosité, branchement audio ou dialogue.
5. Prenez une capture immédiatement, puis répétez avec un autre état.
6. Retirez la règle si elle rend le contrôle difficile à fermer.

Pour comparer deux versions, gardez le même écran, la même résolution, le même facteur d'échelle, le même niveau de volume et le même nombre de fenêtres. Une capture prise à un instant différent peut montrer un OSD à un niveau différent et fausser la comparaison.

## 12. Contrôler les interfaces au clavier et en situation réelle

La validation ne doit pas se limiter à l'apparence statique. Pour chaque dialogue et sélecteur, effectuez les contrôles suivants :

- ouvrir et fermer l'interface sans souris ;
- parcourir tous les choix au clavier ;
- repérer visuellement le focus courant ;
- vérifier qu'une action destructive est identifiable ;
- tester les libellés longs et les traductions ;
- vérifier le contraste sur les surfaces translucides ;
- confirmer que l'interface reste utilisable à l'échelle d'affichage habituelle ;
- vérifier que le pointeur et les poignées de sélection restent visibles.

Pour Alt-Tab, vérifiez également la distinction entre fenêtre sélectionnée et fenêtres simplement visibles. Pour la capture, vérifiez que le contour, le voile et les poignées ne se confondent pas avec le contenu capturé.

Une règle qui améliore une capture mais masque le focus, le bouton de fermeture ou l'état sélectionné doit être considérée comme une régression.

## 13. Sources amont GNOME Shell 51.0

- [OSD — osdWindow.js](https://gitlab.gnome.org/GNOME/gnome-shell/-/blob/51.0/js/ui/osdWindow.js)
- [Capture — screenshot.js](https://gitlab.gnome.org/GNOME/gnome-shell/-/blob/51.0/js/ui/screenshot.js)
- [Fenêtres — altTab.js](https://gitlab.gnome.org/GNOME/gnome-shell/-/blob/51.0/js/ui/altTab.js)
- [Dialogue d'exécution — runDialog.js](https://gitlab.gnome.org/GNOME/gnome-shell/-/blob/51.0/js/ui/runDialog.js)
- [Thème Shell — widgets SCSS](https://gitlab.gnome.org/GNOME/gnome-shell/-/tree/51.0/data/theme/gnome-shell-sass/widgets)
- [Documentation St](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/)
