# Bien démarrer : comprendre GNOME avant de le personnaliser

Ce parcours s'adresse à une personne qui n'a jamais écrit de CSS et ne connaît pas GTK. Il explique les mots utilisés dans le reste du manuel. Lisez les chapitres dans l'ordre et réalisez les exercices dans une session de test. Vous n'avez pas besoin de modifier les fichiers système.

## Ce que vous allez apprendre

À la fin du parcours, vous saurez distinguer le bureau GNOME des applications, reconnaître les différents moteurs graphiques, créer une feuille CSS, modifier un bouton, donner un style à un menu, installer un thème utilisateur, diagnostiquer une erreur et comprendre les limites d'un thème.

Un thème n'est pas une image qui recouvre l'écran. C'est un ensemble de règles et de ressources que différents programmes interprètent. Une règle peut demander à un moteur de dessiner un fond bleu, une bordure, une marge ou une police. Elle ne peut pas inventer un bouton qui n'existe pas et ne peut pas forcément changer le comportement d'un programme.

## Les mots essentiels

- **Bureau** : ensemble de l'expérience visible après la connexion : panneau supérieur, vue Activités, fenêtres, notifications et réglages.
- **GNOME Shell** : programme qui dessine et gère le panneau, la vue Activités, le dock, les menus système, les notifications et l'écran de verrouillage.
- **Mutter** : compositeur et gestionnaire de fenêtres. Il place les fenêtres, gère les écrans et compose l'image finale.
- **Application** : programme lancé dans une fenêtre, par exemple Fichiers ou Paramètres.
- **GTK** : bibliothèque de composants d'interface. Elle fournit les boutons, champs, listes, menus et fenêtres utilisés par beaucoup d'applications.
- **Libadwaita** : bibliothèque de composants et de conventions visuelles utilisée par les applications GNOME modernes. Elle repose sur GTK 4.
- **CSS** : langage de règles visuelles. Il décrit notamment les couleurs, dimensions, bordures, marges et polices.
- **Sélecteur** : motif qui désigne le ou les éléments auxquels une règle CSS s'applique. Exemple : `.button` vise les éléments qui portent la classe `button`.
- **Propriété** : aspect modifié par une règle. Exemple : `background-color` définit la couleur de fond.
- **Valeur** : réglage donné à une propriété. Exemple : `#3584e4` est une couleur hexadécimale.
- **État** : situation momentanée d'un composant : normal, survolé, sélectionné, désactivé ou en focus.
- **Ressource** : fichier non-CSS, comme une icône SVG, une police, un curseur ou une image de fond.
- **Préférence** : réglage de comportement stocké par GNOME ou une application. Une préférence n'est pas une règle CSS.
- **Extension** : code qui ajoute ou change un comportement du Shell. Une extension peut aussi fournir sa propre feuille CSS.

## Pourquoi plusieurs thèmes sont nécessaires

GNOME n'utilise pas un moteur unique. Le panneau et les menus système sont dessinés par GNOME Shell. Les applications historiques peuvent utiliser GTK 3. Les applications modernes utilisent généralement GTK 4 et parfois Libadwaita. Les icônes et curseurs suivent des formats distincts.

Il faut donc traiter séparément :
- le thème Shell dans `gnome-shell/gnome-shell.css` ;
- le thème GTK 3 dans `gtk-3.0/gtk.css` ;
- le thème GTK 4 dans `gtk-4.0/gtk.css` ;
- les styles Libadwaita, dont l'application de CSS externe est limitée et dépend de la version ;
- les thèmes d'icônes et de curseurs ;
- les polices et les arrière-plans ;
- les préférences GNOME qui contrôlent le comportement.

Changer `gtk.css` ne change donc pas automatiquement le panneau supérieur. Changer `gnome-shell.css` ne change pas automatiquement les boutons d'une application.

## Préparer un environnement sans risque

1. Identifiez votre version : exécutez `gnome-shell --version`.
2. Identifiez votre session : `echo "$XDG_SESSION_TYPE"`.
3. Créez un dossier de travail dans votre répertoire personnel.
4. Conservez une copie du thème avant chaque modification importante.
5. Commencez par une session imbriquée ou une machine virtuelle lorsque vous testez du CSS Shell.
6. Ne remplacez jamais des fichiers dans `/usr/share` pour un premier essai.

Commandes utiles :

```sh
mkdir -p ~/Themes/MonPremierTheme/gnome-shell
mkdir -p ~/Themes/MonPremierTheme/gtk-3.0
mkdir -p ~/Themes/MonPremierTheme/gtk-4.0
gnome-shell --version
```

Le dossier `~/Themes` est ici un espace de travail. Pour une installation utilisateur conventionnelle, les thèmes sont généralement placés dans `~/.themes` ou dans le chemin XDG correspondant. Voir le chapitre installation avant de copier un thème.

## Comment lire un exemple CSS

```css
/* Cette règle vise les boutons GTK. */
.button {
  /* Couleur du texte */
  color: #202124;

  /* Couleur de la surface */
  background-color: #f6f5f4;

  /* Arrondit les quatre coins */
  border-radius: 8px;

  /* Espace entre le contenu et le bord */
  padding: 8px 12px;
}
```

Le point devant `.button` signifie « classe CSS ». Les accolades encadrent les déclarations. Chaque déclaration contient une propriété, deux-points, une valeur et un point-virgule. Les commentaires entre `/*` et `*/` ne changent pas le rendu.

Dans `padding: 8px 12px`, la première valeur correspond au haut et au bas, la seconde à la gauche et à la droite. Il s'agit de l'espace intérieur. `margin` désigne l'espace extérieur.

## Votre premier exercice

Créez `gtk-3.0/gtk.css` et collez le CSS de l'exemple. Ouvrez une application GTK 3 de test avec votre thème activé. Si rien ne change, ne modifiez pas dix propriétés au hasard : vérifiez d'abord que l'application utilise GTK 3, que le thème est bien installé et que le sélecteur existe dans son arbre de widgets.

Résultat attendu : les boutons qui correspondent au sélecteur prennent un fond clair, un texte sombre, des coins arrondis et un espacement intérieur. Tous les boutons de toutes les applications ne sont pas garantis : une application peut utiliser un composant personnalisé.

## Une règle d'or

Avant d'éditer un élément, répondez à quatre questions : quel programme le dessine ? quel moteur utilise-t-il ? quel sélecteur ou quelle ressource le représente ? comment vérifier le résultat dans le moteur réel ? Les chapitres suivants vous apprennent à répondre à ces questions.


## Distinguer le dossier de travail du thème installé

Le dossier créé dans l'exercice précédent est un espace où vous écrivez vos fichiers. GNOME ne le surveille pas automatiquement et sa présence ne signifie pas que le thème est actif.

Il faut distinguer trois étapes :

1. **Écrire** : modifier les fichiers dans votre dossier de travail.
2. **Installer** : copier une version contrôlée dans le répertoire utilisateur adapté au type de ressource.
3. **Activer et tester** : sélectionner la ressource avec le mécanisme pris en charge par le moteur, puis ouvrir un composant qui l'utilise.

Ces étapes ne sont pas identiques pour GTK 3, GTK 4, Libadwaita, GNOME Shell, les icônes et les curseurs. Certains moteurs ne proposent pas de sélection globale de thème utilisateur. Ne supposez donc pas qu'un seul réglage active toutes les parties du thème. Suivez le chapitre [installation, paramètres et dépannage](07-parametres-installation-diagnostic.md) avant de copier ou d'activer votre thème.

Conservez le dossier de travail intact. Il doit rester votre source modifiable ; le dossier installé est une copie de test que vous pouvez remplacer ou supprimer.

## Vérifier le moteur avant de chercher une solution

Quand un changement n'apparaît pas, répondez dans cet ordre :

1. **Quel élément est concerné ?** Par exemple, un bouton dans une application ou l'indicateur réseau du panneau.
2. **Quel programme le dessine ?** Une application ou GNOME Shell ?
3. **Quel moteur utilise-t-il ?** GTK 3, GTK 4, Libadwaita ou St ?
4. **Quel fichier est chargé ?** Le fichier GTK d'une application n'est pas la feuille du Shell.
5. **Le composant correspond-il au sélecteur ?** Un sélecteur peut être syntaxiquement valide sans désigner un élément existant.

Pour les applications GTK, le chapitre [inspection et diagnostic CSS](12-inspection-et-diagnostic-css.md) explique comment ouvrir GTK Inspector. Pour GNOME Shell, il présente Looking Glass et les précautions d'une session de test.

## Exercice de diagnostic guidé

Reprenez le bouton de l'exercice précédent et imaginez que son fond ne change pas.

- Si le bouton appartient à une application GTK 3, vérifiez le fichier `gtk-3.0/gtk.css` et le thème GTK effectivement sélectionné.
- Si l'application utilise GTK 4, le fichier GTK 3 ne peut pas agir sur elle.
- Si le bouton est dans le panneau GNOME, il appartient au Shell : une règle GTK ne le modifiera pas.
- Si le bon fichier est chargé mais que rien ne change, inspectez le nœud CSS et ses classes au lieu d'ajouter immédiatement `!important`.
- Si le changement fonctionne dans une fenêtre mais pas dans un dialogue, vérifiez si le dialogue utilise un composant ou un fournisseur CSS différent.

Le but de cet exercice n'est pas de deviner le bon sélecteur. Il est d'apprendre à éliminer les causes possibles une par une et à prouver où se situe le problème.

## Sauvegarder et revenir en arrière

Avant une modification importante, créez une copie du fichier :

```sh
cp gtk-3.0/gtk.css gtk-3.0/gtk.css.bak
```

Après un essai raté, restaurez-la :

```sh
cp gtk-3.0/gtk.css.bak gtk-3.0/gtk.css
```

Adaptez le chemin au fichier réellement modifié. Cette sauvegarde concerne uniquement votre fichier de travail ; elle ne restaure pas une préférence GNOME, une extension ou un fichier système. Pour désinstaller un thème déjà installé, utilisez la procédure du chapitre d'installation et ne supprimez que le dossier que vous avez créé.

Ne lancez pas de commande de suppression avec `sudo` pour corriger un problème de thème utilisateur. Si vous ne savez plus quelle ressource a été modifiée, arrêtez les changements et identifiez d'abord le fichier et son emplacement.

## Suite conseillée

Après ce chapitre, suivez le parcours débutant du [sommaire](index.md) dans l'ordre. Ne passez aux références avancées qu'après avoir réalisé le premier thème, inspecté au moins un composant et vérifié le mécanisme d'installation correspondant à votre moteur.
