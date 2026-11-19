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
