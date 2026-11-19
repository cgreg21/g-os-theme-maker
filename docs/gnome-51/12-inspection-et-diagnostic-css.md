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


## 11. Préparer un diagnostic reproductible

Avant d'ouvrir un inspecteur, décrivez précisément le défaut : écran, composant, état (repos, survol, focus, actif, désactivé ou erreur), propriété concernée et résultat attendu. Relevez les versions et la session :

```sh
printf 'Session : %s\n' "$XDG_SESSION_TYPE"
printf 'Bureau : %s\n' "$XDG_CURRENT_DESKTOP"
gnome-shell --version
pkg-config --modversion gtk+-3.0 2>/dev/null || true
pkg-config --modversion gtk4 2>/dev/null || true
pkg-config --modversion libadwaita-1 2>/dev/null || true
```

Les paquets de développement nécessaires à `pkg-config` peuvent être absents même si les bibliothèques d'exécution sont installées. Les versions retournées ne prouvent pas à elles seules qu'une application donnée utilise ces bibliothèques. Conservez une capture avant modification.

## 12. Inspecter un widget GTK de bout en bout

L'inspecteur doit être ouvert dans le processus qui affiche réellement la fenêtre. Une application déjà active peut réutiliser son processus et ignorer la variable d'environnement de la nouvelle commande.

1. Enregistrez le travail et fermez toutes les fenêtres de l'application.
2. Vérifiez que son processus est terminé.
3. Lancez une nouvelle instance avec `GTK_DEBUG=interactive`.
4. Sélectionnez le widget dans l'inspecteur.
5. Relevez le type GTK, le nom, les classes, les pseudo-classes et les parents.
6. Dans l'onglet CSS, identifiez la déclaration gagnante et les déclarations barrées.
7. Modifiez temporairement une seule propriété.
8. Vérifiez le résultat dans les états voisins.

Si l'application est lancée par D-Bus ou réutilise un service existant, utilisez une application de test isolée. Ne tuez pas arbitrairement un processus de bureau ou un service partagé.

Les fabriques de widgets permettent d'isoler des composants sans dépendre d'un écran applicatif complet :

```sh
gtk3-widget-factory
gtk4-widget-factory
```

Elles ne sont pas forcément installées. Utilisez-les pour explorer les boutons, champs, listes et menus, puis confirmez le rendu dans l'application réelle : une fabrique ne reproduit pas nécessairement les classes et fournisseurs CSS de cette application.

## 13. Lire correctement les résultats de l'inspecteur

Distinguez quatre notions :

- **Règle correspondante** : le sélecteur correspond au nœud.
- **Déclaration gagnante** : la déclaration retenue par la cascade.
- **Valeur calculée** : la valeur finale après cascade et héritage.
- **Rendu observé** : le résultat effectivement dessiné à l'écran.

Une valeur calculée correcte ne garantit pas que l'effet soit visible : un enfant peut recouvrir le fond, le widget peut dessiner son contenu lui-même ou l'ombre peut appartenir à une autre couche.

Lorsqu'une propriété semble ignorée, vérifiez dans cet ordre : prise en charge par la version du moteur, nœud qui dessine l'effet, enfants et pseudo-classes, déclaration gagnante, puis avertissements du moteur. Réduisez le test à une seule propriété au lieu d'ajouter plusieurs déclarations à la fois.

## 14. Distinguer GTK 3, GTK 4 et Libadwaita

Un thème GTK 3 et un thème GTK 4 ne partagent pas automatiquement leurs sélecteurs, propriétés ni composants. Libadwaita ajoute ses propres conventions et fournisseurs CSS.

Pour relever les bibliothèques mappées par un processus :

```sh
pid=1234
grep -E '/(libgtk-3|libgtk-4|libadwaita-1)[.]so' "/proc/$pid/maps" | awk '{print $NF}' | sort -u
```

Remplacez `1234` par le PID réel. L'accès à `/proc/$pid/maps` peut être limité. Cette inspection identifie des bibliothèques mappées, mais ne prouve pas à elle seule quels widgets ou fournisseurs CSS sont utilisés.

Reproduisez le problème dans le moteur réellement chargé par l'application. Ne concluez pas qu'une règle est compatible GTK 4 parce qu'elle fonctionne dans une application GTK 3 d'apparence similaire.

## 15. Identifier la feuille CSS réellement chargée

Une application peut charger du CSS depuis son paquet, une ressource GResource, son code ou un emplacement utilisateur. Modifier un fichier dont le nom paraît pertinent ne prouve pas que le processus l'utilise.

Pour lister les ressources d'un fichier GResource autonome :

```sh
gresource list application.gresource
```

Le chemin dépend de l'application ; les ressources peuvent aussi être compilées dans un binaire. Dans GTK Inspector, relevez le fournisseur CSS et la règle qui gagne. Distinguez le CSS livré par l'application, celui du toolkit, le thème sélectionné et les surcharges utilisateur. Préférez une copie de travail ou un profil isolé aux modifications directes des fichiers système.

## 16. Inspecter GNOME Shell sans le confondre avec GTK

Les acteurs St ne sont pas des widgets GTK. Leurs sélecteurs, propriétés et pseudo-classes ne sont pas interchangeables. Dans Looking Glass :

1. Reproduisez l'état exact du composant.
2. Inspectez l'acteur, ses classes, son parent et ses enfants.
3. Notez si la classe apparaît uniquement dans un état dynamique.
4. Recherchez-la dans les sources JavaScript et SCSS de la version GNOME testée.
5. Vérifiez que le code ajoute effectivement cette classe dans le scénario observé.
6. Testez dans une session de développement et consultez les journaux.

Pour suivre les messages du Shell :

```sh
journalctl -b -f /usr/bin/gnome-shell
```

Selon la distribution et la journalisation, ce filtre peut ne rien retourner. Utilisez alors le journal de session. L'absence de message ne prouve pas que le CSS a été chargé correctement.

## 17. Isoler les erreurs de chargement

Pour observer les messages récents pendant une reproduction :

```sh
journalctl --user -b --since "5 minutes ago" --no-pager
```

Conservez aussi la sortie du terminal si l'application y a été lancée. Relevez le premier avertissement pertinent : les suivants peuvent être des conséquences.

Une propriété inconnue peut venir d'un moteur différent, d'une version trop ancienne, d'une faute de frappe ou d'un nœud qui ne la prend pas en charge. Vérifiez le moteur et sa version avant de remplacer la propriété. Consultez les références GTK, St et Libadwaita séparément.

## 18. Transformer le diagnostic en correction minimale

1. Créez une branche ou une copie de travail.
2. Ajoutez une règle limitée au composant et à l'état observés.
3. Ne modifiez pas simultanément les règles globales et spécifiques.
4. Rechargez ou redémarrez uniquement le processus concerné selon le mécanisme du moteur.
5. Reproduisez le scénario initial.
6. Testez les états voisins et les composants partageant le sélecteur.
7. Retirez les règles temporaires.
8. Comparez avec la capture initiale.
9. Conservez les versions, le journal et le résultat.

Le rechargement à chaud n'est pas universel. Une application peut charger son CSS uniquement au démarrage. Ne redémarrez pas brutalement le Shell ou la session de travail pour tester une règle.

## 19. Vérifier l'accessibilité pendant l'inspection

Après une correction, vérifiez le focus clavier, l'ordre de navigation, les états désactivés et sélectionnés, les grandes tailles de texte, les modes clair et sombre, les libellés longs et les messages d'erreur. Ne retirez pas un contour de focus parce qu'il semble décoratif et ne communiquez pas une sélection uniquement par la couleur. Testez clavier et souris séparément.

## 20. Modèle de preuve technique

Complétez une fiche distincte pour chaque moteur et application :

```text
Application et version :
Origine du paquet :
PID du processus :
Bibliothèques GTK/Libadwaita chargées :
GNOME et session :
Moteur CSS :
Composant et état :
Type, classes et parent du nœud :
Propriété étudiée :
Règle correspondante :
Déclaration gagnante :
Valeur calculée :
Rendu constaté :
Fichier ou ressource CSS :
Messages du journal :
Correction :
États voisins testés :
Accessibilité vérifiée :
Statut : confirmé / partiel / non testé
```

Une fiche « confirmé » doit permettre à une autre personne de retrouver le composant et de reproduire le test. Si le processus, le moteur ou la ressource CSS restent inconnus, indiquez explicitement cette limite.
