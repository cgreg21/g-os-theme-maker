# Inspecter et diagnostiquer le CSS GNOME

Ce chapitre donne une méthode reproductible pour retrouver un élément, comprendre pourquoi une règle ne fonctionne pas et vérifier qu'une correction n'introduit pas de régression. Les noms de menus et la disponibilité des outils varient selon les versions et distributions.

## 1. Comprendre ce que l'on inspecte

Un widget GTK est composé d'un objet, parfois de plusieurs nœuds CSS et d'enfants. L'arbre CSS n'est pas nécessairement identique à l'arbre logique de l'interface. Un bouton peut contenir un label et une image ; une ligne de préférences peut contenir un titre, une description et un contrôle.

Dans GNOME Shell, les éléments sont des acteurs St. Les classes et identifiants sont définis par le code Shell et son thème. GTK Inspector ne sert pas à inspecter le Shell : utilisez Looking Glass et les outils de développement du Shell.

## 2. Activer GTK Inspector

Sur une session de développement, activez l'inspecteur avec le raccourci fourni par GTK ou via les paramètres de débogage disponibles dans la version utilisée. La méthode usuelle pour une application GTK est :

```sh
# Lancer une application avec l'inspecteur GTK activé
GTK_DEBUG=interactive nautilus
```

Cette variable ne fonctionne que si l'application utilise une version GTK qui prend en charge l'inspecteur et si le paquet n'a pas désactivé cette possibilité. Certaines applications refusent une seconde instance ou réutilisent un processus existant. Fermez l'application avant de relancer la commande, si nécessaire.

Dans l'inspecteur :
1. Choisissez l'outil de sélection.
2. Cliquez sur l'élément dans la fenêtre.
3. Examinez le type de widget et le chemin de nœuds.
4. Relevez les classes CSS et les états.
5. Consultez les propriétés calculées et les règles qui les définissent.
6. Ajoutez une règle temporaire dans l'éditeur CSS de l'inspecteur.
7. Confirmez visuellement que seul l'élément attendu est touché.

Ne copiez pas uniquement le nom de la classe : conservez aussi le contexte parent et l'état observé.

## 3. Confirmer un sélecteur sans casser le thème

Commencez par une propriété temporaire évidente :

```css
/* Diagnostic temporaire uniquement */
.nom-de-classe-observee {
  outline: 3px solid magenta;
}
```

Si aucun contour n'apparaît :
- le sélecteur ne correspond peut-être à aucun nœud ;
- la feuille CSS n'est peut-être pas chargée ;
- une règle plus prioritaire peut recouvrir la propriété ;
- le composant peut être dessiné hors du moteur CSS ;
- l'application peut utiliser un autre toolkit ;
- le CSS peut contenir une erreur qui empêche son chargement.

Retirez ensuite le contour de diagnostic. Ne publiez jamais une règle de test comme style final.

## 4. Comprendre la cascade et les priorités

Plusieurs fournisseurs CSS peuvent être actifs : thème, CSS de l'application, CSS utilisateur et règles internes. La priorité et l'ordre de chargement varient selon le moteur et l'application.

Procédure :
1. Repérez la propriété dans les règles affichées par l'inspecteur.
2. Vérifiez quelle déclaration est gagnante.
3. Vérifiez la spécificité du sélecteur.
4. Vérifiez si la propriété est héritée.
5. Vérifiez si le widget dessine lui-même le fond ou l'icône.
6. Modifiez le sélecteur de manière ciblée plutôt que d'ajouter immédiatement `!important`.

`!important` peut masquer le vrai problème et rendre les variantes d'état difficiles à gérer. Utilisez-le uniquement lorsqu'une contrainte documentée le justifie.

## 5. GTK 3 et GTK 4 : outils et validations

Vérifiez les versions présentes :

```sh
pkg-config --modversion gtk+-3.0
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
```

Les commandes peuvent échouer si le paquet de développement correspondant n'est pas installé. Cela ne signifie pas nécessairement que la bibliothèque d'exécution est absente.

Pour valider un thème, testez-le dans une application représentative de chaque moteur. Les applications de démonstration GTK et les fabriques de widgets sont utiles pour isoler un composant, mais elles ne remplacent pas le test dans l'application réelle.

## 6. GNOME Shell : Looking Glass

Looking Glass est l'outil de diagnostic intégré au Shell. Il permet notamment d'examiner les acteurs et les erreurs. Son accès et ses possibilités dépendent de la session et de la version.

Méthode :
1. Ouvrez Looking Glass dans une session de test.
2. Consultez les erreurs après le rechargement du thème.
3. Utilisez l'inspection des acteurs si elle est disponible.
4. Relevez les classes et identifiants du composant.
5. Comparez avec les fichiers SCSS de la version exacte de GNOME Shell.
6. Testez le CSS dans une session imbriquée plutôt que sur la session de travail.

Les sélecteurs Shell internes ne sont pas une API stable. Le fait qu'un sélecteur fonctionne dans GNOME 51 ne garantit pas son fonctionnement dans GNOME 52.

## 7. Lire les journaux

Pour observer les messages d'une application lancée depuis un terminal, démarrez-la depuis ce terminal et reproduisez le problème. Pour les messages de session :

```sh
journalctl --user -b --no-pager
```

Filtrer par processus ou unité peut être plus utile que lire tout le journal. Ne publiez pas un journal brut sans vérifier qu'il ne contient pas de chemins personnels, noms d'utilisateur ou informations privées.

## 8. Diagnostic : le CSS ne produit aucun changement

Suivez cet ordre, sans sauter directement à `!important` :

1. Confirmez que vous modifiez le bon fichier.
2. Confirmez que l'application utilise le moteur ciblé.
3. Confirmez que le thème ou la feuille est effectivement chargé.
4. Vérifiez les erreurs de syntaxe.
5. Confirmez que le sélecteur correspond à un nœud existant.
6. Vérifiez la propriété dans la liste des propriétés calculées.
7. Vérifiez la priorité des autres fournisseurs.
8. Vérifiez si le composant est dessiné par un moteur non-CSS.

## 9. Diagnostic : le style touche trop d'éléments

Un sélecteur tel que `button` ou `.view` peut toucher de nombreux composants. Pour limiter la portée :
- ajoutez un parent stable observé ;
- ciblez une classe spécifique ;
- séparez les règles de l'application des règles globales ;
- testez les dialogues et menus, pas seulement la fenêtre principale ;
- vérifiez les boutons suggérés, destructifs et désactivés.

Évitez de cibler une longue chaîne de descendants fondée sur des détails internes fragiles si un sélecteur plus simple suffit.

## 10. Fiche de diagnostic à remplir

Pour chaque problème, consignez :
- application et version ;
- moteur et version ;
- chemin du fichier CSS ;
- composant observé ;
- sélecteur essayé ;
- état du composant ;
- propriété attendue et valeur calculée ;
- résultat constaté ;
- message d'erreur éventuel ;
- correction retenue ;
- version dans laquelle le test a été effectué.

Une règle n'est considérée comme vérifiée que lorsque le test est reproductible sur la version déclarée.
