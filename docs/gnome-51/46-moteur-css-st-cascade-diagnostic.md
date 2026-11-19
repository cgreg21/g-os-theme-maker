# Moteur CSS St de GNOME Shell 51 : cascade, sélecteurs et diagnostic

Ce chapitre décrit le moteur de styles utilisé par GNOME Shell, appelé **St** (*Shell Toolkit*). Il complète le catalogue des sélecteurs du thème Shell et les chapitres consacrés aux moteurs CSS GTK et Libadwaita.

L'objectif est de comprendre pourquoi une règle est appliquée, ignorée ou remplacée. St utilise une syntaxe inspirée de CSS, mais ce n'est pas un navigateur : les acteurs, les propriétés et les pseudo-classes disponibles dépendent des types St et des classes réellement ajoutées par GNOME Shell.

Les détails d'implémentation décrits ici sont vérifiés dans le tag officiel **GNOME Shell 51.0**.

## 1. Où se situe St dans GNOME

GNOME Shell construit son interface avec Clutter et St :

- **Clutter** fournit les acteurs graphiques, la scène, les événements et les mécanismes de rendu.
- **St** ajoute des widgets adaptés au Shell, comme les boutons, conteneurs, entrées et barres de niveau.
- **StTheme** gère les feuilles de style et leur cascade.
- **StThemeContext** fournit le contexte de thème partagé, notamment les informations de police, de couleur et d'échelle.
- **StThemeNode** représente le style calculé d'un acteur à partir de son type, de son identifiant, de ses classes et de ses pseudo-classes.
- **StWidget** relie les propriétés de style de l'acteur au calcul et au rendu du thème.

Les acteurs Clutter qui ne sont pas des widgets St ne disposent pas nécessairement des mêmes possibilités CSS. Une classe CSS ne crée pas un widget et ne transforme pas un acteur quelconque en composant stylable.

Sources :

- [Architecture des extensions GNOME Shell](https://gjs.guide/extensions/overview/architecture.html)
- [St.Theme — API 51](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/class.Theme.html)
- [St.ThemeNode — API 51](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/class.ThemeNode.html)

## 2. Les trois feuilles principales de la cascade

Le constructeur `St.Theme` reçoit trois feuilles principales :

- `application-stylesheet` : feuille de l'application, associée à l'origine CSS auteur ;
- `theme-stylesheet` : feuille du thème, associée à l'origine CSS utilisateur ;
- `default-stylesheet` : feuille par défaut, associée à l'origine CSS agent utilisateur.

L'ordre des origines est important. Dans le modèle CSS employé par St, les règles de l'origine agent utilisateur sont moins prioritaires que celles du thème, elles-mêmes moins prioritaires que les règles de l'application, avant prise en compte des déclarations importantes et des feuilles d'extension.

Il ne faut donc pas appliquer mécaniquement la règle « le dernier fichier chargé gagne ». Le moteur compare d'abord l'origine, puis la spécificité. L'ordre du code source intervient lorsque les autres critères ne départagent pas les déclarations.

Le code qui construit cette cascade se trouve dans `src/st/st-theme.c`, dans la fonction `st_theme_constructed()`.

## 3. Feuilles de style chargées par les extensions

Les extensions peuvent charger des feuilles de style supplémentaires dans le thème St. Le moteur les conserve dans une liste de feuilles personnalisées et les prend en compte lors du calcul des propriétés.

Dans le code 51.0, ces feuilles sont marquées comme feuilles d'extension. Le calcul de priorité leur applique un décalage d'origine spécifique, qui les place au-dessus des origines ordinaires. Les déclarations `!important` reçoivent elles aussi un décalage distinct.

Conséquence pratique : une extension peut modifier le rendu d'un composant du Shell même si le thème global fournit une règle très spécifique. Une règle de thème ne peut pas supposer qu'elle sera toujours la dernière autorité si des extensions sont actives.

Cela explique également pourquoi deux sessions ayant le même thème peuvent présenter des différences : elles ne chargent pas nécessairement les mêmes extensions ni les mêmes feuilles additionnelles.

Pour diagnostiquer un écart :

1. Désactivez temporairement les extensions non indispensables.
2. Reproduisez le problème avec le thème standard.
3. Réactivez les extensions une par une.
4. Identifiez celles qui chargent une feuille de style ou modifient les classes des acteurs.
5. Testez de nouveau avec le thème cible.

Ne désactivez pas durablement une extension sans vérifier les fonctions qu'elle apporte.

## 4. Comment St identifie un élément

Un nœud de thème St peut contenir plusieurs informations :

- le type GObject de l'acteur ;
- un identifiant d'élément ;
- une liste de classes séparées par des espaces ;
- une liste de pseudo-classes séparées par des espaces ;
- un style en ligne éventuel ;
- un nœud parent qui représente la hiérarchie de style.

Les sélecteurs CSS usuels peuvent alors s'appuyer sur les types, les identifiants, les classes, les pseudo-classes et les relations entre éléments lorsque celles-ci correspondent à l'arbre de thème.

Exemples :

```css
/* Classe */
.panel-button {
  padding: 6px;
}

/* Identifiant */
#panel {
  height: 32px;
}

/* Type et classe */
StButton.panel-button {
  border-radius: 10px;
}

/* Pseudo-classe */
.panel-button:hover {
  background-color: rgba(255, 255, 255, 0.12);
}

/* Combinaison de classes */
.quick-settings .icon-button {
  border-radius: 50%;
}
```

Un sélecteur n'est utile que si l'acteur ciblé expose réellement le type, l'identifiant ou les classes attendus. Un nom qui semble logique n'est pas automatiquement une classe présente dans l'arbre.

## 5. Classes de style : remplacer, ajouter et retirer

St distingue trois opérations importantes dans son API :

- définir la liste complète de classes ;
- ajouter une classe sans supprimer les autres ;
- retirer une classe précise.

Cette distinction explique certains comportements des extensions. Une extension qui remplace toute la liste peut supprimer des classes posées par GNOME Shell ou par une autre extension. Une extension qui ajoute une classe conserve les classes existantes.

Pour le créateur de thème, cela signifie qu'une classe peut être présente dans une session standard et disparaître lorsque le comportement d'un acteur est modifié par une extension.

Dans le code source, ces opérations sont exposées par `St.Widget`, notamment :

- `set_style_class_name()` ;
- `add_style_class_name()` ;
- `remove_style_class_name()` ;
- `get_style_class_name()`.

Référence : [St.Widget — API 51](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/class.Widget.html).

## 6. Pseudo-classes et états dynamiques

Une pseudo-classe représente un état, pas une classe permanente. Un bouton peut ainsi avoir une apparence différente lorsqu'il est survolé, activé, sélectionné ou désactivé.

Exemples de règles courantes :

```css
.button {
  background-color: transparent;
}

.button:hover {
  background-color: rgba(255, 255, 255, 0.08);
}

.button:active {
  background-color: rgba(255, 255, 255, 0.16);
}

.button:focus {
  outline: 2px solid #78aeed;
}

.button:insensitive {
  opacity: 0.5;
}
```

Les pseudo-classes présentes dans le thème GNOME Shell 51.0 comprennent notamment :

- `:hover` ;
- `:focus` ;
- `:active` ;
- `:checked` ;
- `:insensitive` ;
- `:ltr` et `:rtl`.

Le fait qu'une pseudo-classe soit reconnue par St ne signifie pas que chaque acteur l'utilise. Le code de l'acteur ou de GNOME Shell doit réellement activer l'état correspondant.

Pour vérifier un état, testez l'interaction qui le déclenche : survol avec la souris, navigation clavier, activation, désactivation ou sélection.

## 7. Spécificité et ordre des déclarations

St calcule une spécificité pour les règles correspondantes, puis compare les déclarations selon leur origine et leur spécificité. À spécificité égale, l'ordre stable des déclarations permet aux règles rencontrées plus tard de prendre le dessus.

Exemple :

```css
.button {
  border-radius: 6px;
}

.panel .button {
  border-radius: 10px;
}

#panel .button {
  border-radius: 14px;
}
```

La troisième règle est plus spécifique que les deux autres si le nœud possède bien l'identifiant `panel` et la classe `button`.

Évitez de répondre à un conflit en ajoutant systématiquement des identifiants et des sélecteurs très longs. Une règle trop spécifique devient difficile à remplacer et peut casser lors d'une évolution de l'arbre d'acteurs.

Une démarche plus robuste :

1. Vérifier que le sélecteur initial correspond.
2. Identifier la règle concurrente.
3. Vérifier son origine et sa spécificité.
4. Limiter la nouvelle règle au composant visé.
5. Éviter `!important` tant qu'une correction de sélecteur suffit.

## 8. Déclarations importantes

Le moteur St prend en compte les déclarations `!important` dans son calcul de priorité. Le code source applique un décalage d'origine spécifique à ces déclarations.

Exemple :

```css
.panel-button {
  color: white !important;
}
```

Cette syntaxe doit rester exceptionnelle. Si une extension utilise des déclarations importantes, elle peut rendre le thème plus difficile à personnaliser et provoquer des conflits.

Ne copiez pas `!important` dans toutes les règles d'un thème. Cela masque le problème de priorité au lieu de le résoudre.

## 9. Styles en ligne

St.Widget possède une propriété de style en ligne. Son contenu est une liste de déclarations CSS séparées par des points-virgules :

```css
background-color: #20242b;
border-radius: 12px;
padding: 8px;
```

Le style en ligne est ajouté au calcul du nœud et peut remplacer les déclarations venant des feuilles de style.

Il est généralement défini par le code JavaScript de GNOME Shell ou d'une extension. Le thème ne doit pas supposer qu'une propriété sera contrôlable uniquement par une règle de feuille de style si le code affecte ensuite une valeur en ligne.

Lorsque le style semble résister à toutes les règles CSS, inspectez l'implémentation GJS de l'acteur et recherchez les appels à `set_style()`.

## 10. Propriétés St et propriétés CSS web

St prend en charge une partie des propriétés CSS, mais ajoute aussi des propriétés propres à ses widgets. Les propriétés St ne sont pas des propriétés CSS web et ne sont pas automatiquement comprises par GTK.

Exemples rencontrés dans le Shell :

```css
.quick-settings {
  spacing: 12px;
}

.level {
  -barlevel-height: 4px;
  -barlevel-background-color: rgba(255, 255, 255, 0.15);
  -barlevel-active-background-color: #78aeed;
}
```

Les propriétés `-barlevel-*` sont liées au widget de niveau St. Elles ne doivent pas être copiées dans un thème GTK en supposant qu'elles auront le même effet.

Autres propriétés ou extensions rencontrées dans les sources Shell :

- `icon-size` ;
- `spacing` ;
- `spacing-rows` ;
- `spacing-columns` ;
- `-natural-hpadding` ;
- `-minimum-hpadding` ;
- `-st-icon-style`.

Cette liste est indicative, pas une grammaire exhaustive. La propriété doit être prise en charge par le type de widget qui la consomme.

## 11. Héritage et limites du style

Le thème St représente une hiérarchie de nœuds. Un nœud connaît son parent, son type, ses classes et ses états. Certaines propriétés peuvent être héritées par les descendants, alors que d'autres sont calculées ou dessinées localement.

Ne supposez pas que toutes les propriétés se propagent comme dans une page web. Le comportement dépend de la propriété et de son traitement dans St.

Par exemple, une couleur de texte peut être héritée alors qu'une bordure ou une image d'arrière-plan appartient uniquement au widget ciblé.

Si une propriété ne se propage pas :

1. Inspectez le widget parent.
2. Inspectez le widget enfant.
3. Vérifiez si l'enfant définit lui-même la propriété.
4. Vérifiez si la propriété est héritée par St.
5. Appliquez la règle sur l'acteur réellement dessiné si nécessaire.

## 12. Diagnostic avec Looking Glass

Looking Glass permet d'inspecter GNOME Shell en cours d'exécution. Il est utile pour examiner les acteurs, les classes, les propriétés et les erreurs JavaScript, mais il ne remplace pas un débogueur pas à pas.

Ouvrez Looking Glass avec :

```text
Alt+F2
lg
Entrée
```

Selon la configuration, la console peut également être ouverte par le raccourci ou le mécanisme d'accès disponible dans la session.

Procédure :

1. Ouvrez l'onglet d'inspection.
2. Sélectionnez l'acteur dans l'interface.
3. Relevez son type et sa hiérarchie.
4. Relevez ses classes de style.
5. Déclenchez l'état à examiner.
6. Vérifiez que la pseudo-classe apparaît.
7. Comparez l'acteur parent et l'acteur enfant.
8. Reproduisez après désactivation des extensions tierces.

Les libellés exacts de l'interface Looking Glass peuvent évoluer. Si l'inspecteur ne permet pas d'obtenir une information, examinez le code GJS du composant correspondant.

## 13. Comprendre les erreurs de feuille de style

Une feuille CSS peut échouer de plusieurs façons différentes :

- le fichier n'est pas chargé ;
- le fichier est chargé, mais contient une erreur de syntaxe ;
- la règle est analysée, mais son sélecteur ne correspond à aucun acteur ;
- le sélecteur correspond, mais une autre déclaration gagne la cascade ;
- la propriété est inconnue ou non prise en charge par le widget ;
- la propriété est appliquée, mais le rendu final est dessiné par un autre acteur ;
- une extension modifie l'acteur ou ajoute une feuille plus prioritaire.

Ces cas ne se corrigent pas de la même manière.

Une vérification efficace sépare donc quatre questions :

1. **Chargement** : la feuille est-elle présente ?
2. **Correspondance** : le sélecteur cible-t-il un acteur existant ?
3. **Cascade** : quelle déclaration gagne ?
4. **Rendu** : le widget dessine-t-il réellement la propriété ?

Ne concluez pas « CSS invalide » à partir d'un résultat visuel inchangé.

## 14. Exemple de diagnostic complet

Objectif : modifier le fond d'un bouton du panneau sans toucher aux autres boutons.

Première étape : identifier le composant dans le code source Shell 51.0 et dans Looking Glass. Supposons que l'acteur observé porte réellement la classe `panel-button`.

Créer une règle de test minimale :

```css
.panel-button {
  background-color: rgba(255, 0, 0, 0.25);
}
```

Si aucun bouton ne change :

- vérifier que la feuille est chargée ;
- vérifier que l'acteur possède cette classe ;
- vérifier si le bouton est un St.Widget ;
- vérifier si une règle d'extension ou un style en ligne gagne ;
- vérifier si le fond est dessiné par un enfant.

Si tous les boutons changent, le sélecteur est trop général. Relevez une classe ou un parent distinctif sur l'acteur visé et limitez la règle.

Après validation, remplacez la couleur de test par la couleur finale et testez le panneau en état normal, survolé, focus clavier, menu ouvert et en contraste élevé.

## 15. Règles de qualité pour un thème Shell

- Préférez les classes officielles réellement présentes aux sélecteurs construits par intuition.
- Limitez les règles à un composant et à un contexte.
- Ne surchargez pas tout le Shell avec des sélecteurs d'élément génériques.
- Conservez des états de focus visibles.
- Testez les états désactivés et sélectionnés.
- Vérifiez LTR et RTL.
- Contrôlez les menus, notifications, OSD et dialogues temporaires.
- Testez sans extensions tierces puis avec les extensions cibles.
- Évitez les déclarations `!important` systématiques.
- Revalidez les sélecteurs à chaque nouvelle version majeure de GNOME Shell.

## 16. Sources officielles GNOME Shell 51.0

Sources de code utilisées :

- [St.Theme — implémentation](https://github.com/GNOME/gnome-shell/blob/51.0/src/st/st-theme.c)
- [St.ThemeContext — implémentation](https://github.com/GNOME/gnome-shell/blob/51.0/src/st/st-theme-context.c)
- [St.ThemeNode — implémentation](https://github.com/GNOME/gnome-shell/blob/51.0/src/st/st-theme-node.c)
- [St.Widget — implémentation](https://github.com/GNOME/gnome-shell/blob/51.0/src/st/st-widget.c)
- [St.Theme — documentation API 51](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/class.Theme.html)
- [St.ThemeNode — documentation API 51](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/class.ThemeNode.html)
- [St.Widget — documentation API 51](https://gnome.pages.gitlab.gnome.org/gnome-shell/st/class.Widget.html)
- [GNOME Shell 51.0 — thème SCSS](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass)

Les sources sont épinglées sur 51.0. Un changement de code dans une version ultérieure peut modifier la cascade, les classes ou les propriétés disponibles.
