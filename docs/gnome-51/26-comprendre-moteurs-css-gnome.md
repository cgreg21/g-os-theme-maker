# Comprendre les moteurs CSS et leurs cascades

Ce chapitre explique pourquoi une règle qui fonctionne dans GNOME Shell ne fonctionne pas nécessairement dans une application GTK, et pourquoi deux applications GTK 4 peuvent afficher des styles différents. C’est la compétence centrale qui permet de diagnostiquer un thème au lieu d’empiler des sélecteurs au hasard.

## 1. Trois moteurs à ne pas confondre

GNOME ne possède pas une feuille CSS globale qui contrôle tout le bureau.

- **GNOME Shell** utilise St, une boîte à outils basée sur Clutter et GObject. Son CSS est appliqué à des acteurs St. Les propriétés disponibles comprennent des extensions propres à St, notamment certaines propriétés d’icône et d’espacement.
- **GTK 3 et GTK 4** utilisent chacun leur moteur CSS et leur arbre de nœuds. Le CSS cible les nœuds exposés par le widget, pas directement le nom de la classe du code.
- **Libadwaita** est une bibliothèque construite sur GTK 4. Elle ajoute des widgets, des conventions de style et des couleurs sémantiques. Elle ne constitue pas un quatrième moteur CSS indépendant.

Une règle CSS identique peut donc être reconnue par un moteur, ignorée par un autre, ou ne correspondre à aucun nœud.

## 2. Le chemin d’une règle

Pour qu’une règle modifie réellement un composant, toutes les étapes suivantes doivent être vraies :

1. Le processus concerné charge une feuille de style.
2. Le moteur sait interpréter la propriété et sa valeur.
3. Le sélecteur correspond à un nœud présent dans l’arbre courant.
4. La pseudo-classe correspond à l’état actuel du nœud.
5. La priorité de la règle lui permet de gagner la cascade.
6. Le widget autorise la propriété à influencer son rendu ou sa mesure.

Si une seule étape échoue, la règle peut rester sans effet sans provoquer d’erreur visible.

## 3. GTK : le nœud CSS n’est pas la classe du widget

Un widget GTK expose un arbre CSS. Un bouton peut contenir plusieurs nœuds internes ; un curseur possède une piste et une poignée ; une ligne Libadwaita peut contenir un titre, une description et un contrôle.

Pour examiner cet arbre :

1. Lancez l’application avec GTK Inspector.
2. Sélectionnez le widget dans l’arbre.
3. Relevez le nom du nœud, ses classes et son état.
4. Vérifiez les règles appliquées et les providers actifs.
5. Écrivez un sélecteur limité au composant visé.
6. Testez aussi le focus, l’état désactivé et la sélection.

Le nom de l’objet GtkButton ne garantit pas que le sélecteur GtkButton existe. Le nœud CSS est généralement button ; une classe de style peut préciser le rôle, par exemple suggested-action.

## 4. GTK : comprendre la cascade des providers

GTK peut recevoir des providers CSS à plusieurs niveaux : moteur, thème, écran ou display selon la version, application et widget. La priorité du provider compte autant que la spécificité du sélecteur.

Une application peut charger une feuille privée, ajouter une classe à l’exécution, définir un provider à priorité supérieure, dessiner un composant personnalisé ou embarquer ses ressources dans un GResource.

Un thème installé dans le répertoire utilisateur ne peut pas garantir qu’il remplacera ces choix. Si une application ignore une règle, inspectez ses providers avant d’augmenter la spécificité.

## 5. GNOME Shell : St et les acteurs

Le Shell n’expose pas un DOM. Les acteurs sont construits par le code JavaScript et les widgets St. Le thème CSS ne peut modifier que les aspects exposés par les acteurs et leurs styles.

Les propriétés spécifiques à St, comme -natural-hpadding, -minimum-hpadding, icon-size ou spacing, ne doivent pas être copiées dans une feuille GTK. À l’inverse, une propriété GTK ne doit pas être présumée disponible dans St.

Le sélecteur #panel cible un acteur portant cet identifiant dans le Shell ; il ne s’agit pas d’un identifiant HTML. Les noms internes restent des détails d’implémentation qui peuvent changer à chaque version.

## 6. Libadwaita : couleurs sémantiques et composants

Une couleur sémantique exprime une fonction, pas une teinte arbitraire. Une couleur de fond de vue doit rester adaptée à la vue, que le thème soit clair ou sombre.

Les variables comme --window-bg-color, --view-bg-color, --headerbar-bg-color, --card-bg-color et --accent-bg-color dépendent des versions de GTK et Libadwaita. Vérifiez leur présence dans la documentation de la version ciblée.

Les widgets Adw sont des classes API. Leur nom n’est pas automatiquement le nom de leur nœud CSS. Utilisez l’inspecteur et la documentation du composant.

## 7. Diagnostic guidé

Quand une règle ne fonctionne pas, procédez dans cet ordre :

1. Confirmez l’application et son moteur : Shell, GTK 3, GTK 4 ou Libadwaita.
2. Confirmez la version du moteur.
3. Confirmez que la feuille est réellement chargée.
4. Inspectez le nœud CSS ou l’acteur.
5. Vérifiez que le sélecteur correspond.
6. Vérifiez la propriété et la valeur acceptées.
7. Vérifiez les providers et la cascade.
8. Retirez temporairement les règles voisines pour isoler le problème.
9. Relancez le test dans un environnement propre.

Commandes de repérage :

    gnome-shell --version
    pkg-config --modversion gtk+-3.0
    pkg-config --modversion gtk4
    pkg-config --modversion libadwaita-1

Ne concluez jamais « propriété non supportée » avant d’avoir vérifié le moteur et le nœud. Ne concluez jamais « thème ignoré » avant d’avoir vérifié le chargement de la feuille.

## 8. À retenir

- Un sélecteur valide ne garantit pas qu’un nœud existe.
- Une propriété reconnue ne garantit pas qu’un widget l’utilise.
- La cascade peut être dominée par une feuille privée d’application.
- Les moteurs St, GTK 3 et GTK 4 ont des syntaxes et propriétés différentes.
- Libadwaita s’appuie sur GTK 4 et ajoute des conventions propres.
- L’inspection doit précéder l’écriture du CSS.

Références : [CSS GTK 3](https://docs.gtk.org/gtk3/css-overview.html), [CSS GTK 4](https://docs.gtk.org/gtk4/css-overview.html), [styles Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html), [sources Shell 51](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass).


## 9. Identifier le moteur à partir du processus réel

Ne choisissez pas une feuille CSS à partir du seul nom de l'application. Une application peut utiliser plusieurs bibliothèques, charger des composants différents ou être distribuée dans un environnement isolé.

Commencez par repérer le processus :

~~~bash
pgrep -a -f 'nom-de-application'
~~~

Remplacez le motif par une partie suffisamment distinctive du nom du processus. Si plusieurs processus correspondent, identifiez celui qui possède la fenêtre observée.

Pour un processus connu :

~~~bash
PID=1234
grep -E 'libgtk-3|libgtk-4|libadwaita|libst-' "/proc/$PID/maps" 2>/dev/null
~~~

Remplacez 1234 par le PID réel. La présence d'une bibliothèque dans maps constitue un indice de chargement, mais ne décrit pas à elle seule tous les composants qui dessinent la fenêtre.

Pour une application Flatpak, examinez également l'identifiant et le runtime :

~~~bash
flatpak ps
flatpak info IDENTIFIANT
~~~

Un outil de développement installé sur l'hôte peut annoncer une version différente de celle utilisée dans le runtime. Consignez les deux informations si elles sont pertinentes.

## 10. Reconnaître les responsabilités de chaque couche

Une fenêtre GNOME peut combiner plusieurs couches indépendantes :

- Mutter place les fenêtres, compose les surfaces et gère les sorties.
- GNOME Shell construit le panneau, les menus système, la vue Activités et d'autres interfaces du shell.
- St fournit des acteurs et un moteur de style utilisés par GNOME Shell.
- GTK 3 ou GTK 4 construit les widgets d'une application.
- Libadwaita ajoute des composants et conventions visuelles à GTK 4.
- L'application peut dessiner elle-même certaines surfaces ou charger des ressources privées.

Un défaut apparent de couleur peut donc être causé par une couche qui n'est pas celle que vous modifiez. Une ombre de fenêtre, par exemple, peut relever du compositeur, tandis que l'ombre d'une carte peut être dessinée par le widget.

Avant d'écrire une règle, décrivez l'élément visible et son propriétaire probable. Confirmez ce propriétaire par inspection ou par le code source.

## 11. Atelier : créer un cas minimal pour chaque moteur

Un cas minimal permet de distinguer un problème du moteur d'un problème propre à l'application.

Préparez quatre cas séparés :
- une application GTK 3 ;
- une application GTK 4 sans Libadwaita ;
- une application Libadwaita ;
- un composant GNOME Shell/St.

Pour chaque cas, consignez la version, le mode de distribution, le chemin de la feuille et la méthode de rechargement. Utilisez des composants réels et visibles, pas seulement un fichier CSS vide.

Commencez par une propriété visuelle simple et facilement observable. Vérifiez ensuite que la même règle ne produit pas un résultat inattendu dans un autre moteur.

Ne réunissez pas les règles des quatre moteurs dans un fichier commun. La séparation des fichiers évite qu'une syntaxe spécifique soit interprétée par un moteur qui ne la connaît pas.

## 12. Comprendre les niveaux de la cascade

Une règle peut être valide et chargée sans gagner la cascade. Les fournisseurs ont des priorités, et les applications peuvent installer des feuilles supplémentaires.

Pour diagnostiquer une propriété, suivez ce chemin :

1. Le fichier est-il accessible et chargé ?
2. Le parseur accepte-t-il la règle ?
3. Le sélecteur correspond-il au nœud ?
4. La propriété existe-t-elle dans ce moteur ?
5. La valeur est-elle valide pour cette propriété ?
6. Une autre déclaration gagne-t-elle la cascade ?
7. Le widget utilise-t-il réellement la propriété pour dessiner ?
8. Le rendu est-il masqué par un autre acteur ou une autre surface ?

Ne changez pas simultanément le sélecteur, la propriété et la couleur. Une seule variable modifiée à la fois permet de comprendre le résultat.

## 13. Distinguer erreur de syntaxe et absence d'effet

Une feuille peut être partiellement interprétée. Une erreur sur une déclaration ne signifie pas toujours que tout le fichier est rejeté.

Consultez les messages du moteur au moment du chargement. Recherchez les erreurs de syntaxe, les propriétés inconnues, les valeurs incorrectes et les ressources absentes.

Pour isoler une règle :
- copiez-la dans une feuille de test ;
- réduisez le sélecteur à un nœud connu ;
- utilisez une valeur simple et valide ;
- vérifiez le résultat ;
- réintroduisez progressivement les conditions et descendants.

Ne corrigez pas un avertissement en supprimant aveuglément la déclaration. Vérifiez si la propriété est nécessaire et si son remplacement conserve le comportement attendu.

## 14. Les sélecteurs ne sont pas interchangeables

Les syntaxes peuvent se ressembler sans avoir la même sémantique. Un sélecteur GTK n'est pas un sélecteur de navigateur, et un sélecteur St n'est pas nécessairement un sélecteur GTK.

Vérifiez en particulier :
- classes et identifiants réellement exposés ;
- relations entre parents et descendants ;
- pseudo-classes disponibles ;
- propriétés de priorité et d'état ;
- gestion des états actifs et désactivés ;
- prise en charge des sélecteurs d'attributs ;
- règles propres aux widgets personnalisés.

Un nom de classe trouvé dans le code source peut être appliqué à un acteur parent, tandis que le dessin visible est effectué par un enfant. Inspectez l'arbre complet avant de choisir le niveau ciblé.

## 15. Comprendre les unités et les métriques

Les unités et les métriques ne doivent pas être copiées sans vérification d'un moteur à l'autre.

Une valeur exprimée en pixels logiques peut être affectée par le facteur d'échelle et par les conventions de la bibliothèque. Les tailles minimales, marges internes et espacements peuvent également être calculés par le widget plutôt que par le CSS.

Quand une dimension paraît incorrecte :
1. Relevez la taille logique de la fenêtre.
2. Relevez le facteur d'échelle.
3. Identifiez le widget ou l'acteur qui impose la taille.
4. Inspectez les propriétés de taille et les contraintes du code.
5. Modifiez une seule dimension.
6. Vérifiez les textes longs et les traductions.

Évitez les hauteurs fixes pour les composants qui peuvent contenir plusieurs lignes. Une règle visuellement correcte dans une langue peut tronquer le texte dans une autre.

## 16. Les ressources et couleurs ne sont pas toujours globales

Les couleurs sémantiques de Libadwaita, les variables Sass du thème Shell et les couleurs définies par une application ne partagent pas nécessairement le même espace de noms.

De même, une image référencée par une feuille CSS doit être résolue selon les mécanismes du moteur et l'emplacement de la feuille. Une URL de ressource GTK, un chemin de fichier et une ressource GResource ne sont pas équivalents.

Avant de remplacer une couleur ou une image :
- identifiez sa définition ;
- identifiez son mécanisme de chargement ;
- vérifiez la variante claire ou sombre ;
- vérifiez le contraste ;
- vérifiez le comportement à plusieurs échelles ;
- vérifiez le repli si la ressource est absente.

Ne supposez pas qu'une variable CSS de navigateur comme var(--accent) existe dans GTK ou St. Les variables CSS personnalisées et les variables de thème ont des règles propres à chaque moteur.

## 17. Diagnostic des différences entre applications

Deux applications utilisant GTK 4 peuvent avoir des rendus différents parce qu'elles n'utilisent pas les mêmes widgets, fournisseurs, versions ou conventions.

Pour comparer :
- choisissez le même type de composant ;
- utilisez le même contenu ;
- vérifiez les versions GTK et Libadwaita ;
- inspectez les classes des deux widgets ;
- relevez les fournisseurs propres aux applications ;
- comparez les états et la variante d'apparence.

Si le composant d'une application est personnalisé, ne généralisez pas son sélecteur à toutes les applications GTK 4. Documentez l'exception et le périmètre testé.

## 18. Décider où corriger un défaut

Utilisez le propriétaire du rendu pour choisir le lieu de correction :

- règle partagée entre widgets GTK standards : feuille GTK correspondante ;
- composant Libadwaita : variable ou style documenté pour la version utilisée ;
- panneau ou menu GNOME Shell : thème Shell/St ;
- placement, ombre de fenêtre ou sortie : réglages et comportement de Mutter ;
- composant dessiné par l'application : préférence ou code de l'application ;
- ressource embarquée : ressource de l'application ou mécanisme de surcharge pris en charge.

Si aucun point d'extension officiel n'existe, indiquez la limite. Ne créez pas une règle globale agressive qui risque de modifier des éléments sans rapport.

## 19. Contrôler les régressions lors d'une mise à jour

Après une mise à jour de GNOME, GTK ou Libadwaita, ne supposez pas que les mêmes classes et variables sont encore disponibles.

Rejouez une sélection de cas de référence :
- fenêtre principale ;
- barre d'en-tête ;
- bouton normal et désactivé ;
- champ de saisie ;
- menu et popover ;
- liste avec sélection ;
- dialogue ;
- variante sombre ;
- navigation clavier.

Comparez les avertissements et les captures. Si une règle ne s'applique plus, vérifiez d'abord si le widget ou sa classe a changé avant d'augmenter la spécificité du sélecteur.

Conservez les versions testées et les différences dans le journal de maintenance.

## 20. Fiche d'identification du moteur CSS

~~~text
Application ou composant :
Processus et PID :
Mode de distribution :
Runtime éventuel :
Bibliothèques chargées :
Moteur confirmé :
Version du moteur :
Version GNOME Shell :
Version Mutter :
Version Libadwaita :
Session :
Fichier CSS chargé :
Fournisseurs additionnels :
Nœud ou acteur observé :
Classe et identifiant :
Propriété testée :
Valeur testée :
Avertissements :
Déclaration gagnante :
Propriétaire du rendu :
Résultat dans un cas minimal :
Limites :
Conclusion :
~~~

Cette fiche évite de traiter comme un problème CSS une différence due à la version, au runtime, au toolkit ou au propriétaire réel du rendu.
