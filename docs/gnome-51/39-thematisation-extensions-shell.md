# Thématisation des extensions GNOME Shell et coexistence des styles

Les extensions GNOME Shell ajoutent des composants au bureau : indicateurs, menus, boutons, panneaux, fenêtres contextuelles ou éléments de l'interface Activités. Elles peuvent également charger leur propre feuille CSS. Un thème Shell global peut donc être correct tout en laissant certains composants inchangés, ou en étant partiellement recouvert par le style d'une extension.

Ce chapitre explique comment repérer ces situations, organiser les responsabilités et tester un thème avec les extensions réellement utilisées.

## 1. Comprendre les trois sources de style

Un bureau GNOME peut afficher simultanément :

- les composants natifs de GNOME Shell, stylés par le thème Shell actif ;
- les composants ajoutés par une extension, stylés par le thème Shell et éventuellement par une feuille propre à l'extension ;
- les fenêtres et widgets d'une application, stylés par GTK, Libadwaita ou le moteur de cette application.

Une extension n'est pas une application GTK ordinaire. Ses composants sont généralement des acteurs du Shell. GTK Inspector ne permet donc pas d'inspecter leurs nœuds : utilisez Looking Glass et les outils de développement de GNOME Shell.

## 2. Inventorier les extensions activées

Commencez par relever les extensions présentes et leur état :

```sh
gnome-extensions list
gnome-extensions list --enabled
```

Pour obtenir les informations d'une extension :

```sh
gnome-extensions info UUID_DE_EXTENSION
```

Remplacez le texte d'exemple par l'identifiant UUID exact affiché par la commande. Ne devinez pas l'identifiant à partir du nom visible.

Conservez cet inventaire avec les captures de référence. Une extension activée peut ajouter des éléments visuels qui n'existent pas dans une session GNOME sans extension.

## 3. Identifier le propriétaire d'un composant

Avant d'écrire une règle, déterminez si l'élément appartient au Shell ou à une extension.

Procédure :

1. notez le nom visible de l'élément ;
2. désactivez temporairement l'extension concernée dans une session de test ;
3. vérifiez si l'élément disparaît ;
4. réactivez l'extension ;
5. inspectez les classes et acteurs avec Looking Glass ;
6. consultez les sources de l'extension pour confirmer le nom de ses classes.

Ne désactivez pas à l'aveugle les extensions de la session de travail. Faites ces essais dans un compte ou une session de test, en conservant un moyen de revenir à la configuration initiale.

## 4. Pourquoi une extension peut ignorer le thème

Plusieurs situations sont possibles :

- l'extension utilise des classes CSS différentes de celles du Shell natif ;
- elle charge une feuille CSS qui ajoute des règles plus spécifiques ;
- elle définit des styles directement dans son code ;
- elle utilise des images ou icônes embarquées ;
- elle crée des acteurs dont la structure change selon sa version ;
- elle n'a pas été conçue pour la version actuelle de GNOME Shell.

Une règle générale comme `.button` peut affecter plusieurs composants, mais elle ne garantit pas que tous les boutons d'une extension partagent cette classe. Une règle plus spécifique peut également l'emporter.

La bonne méthode consiste à inspecter le composant réel et à consulter le code de la version installée de l'extension.

## 5. Éviter les sélecteurs globaux dangereux

Une règle globale peut modifier involontairement les composants ajoutés par une extension :

```css
/* Trop large : peut affecter de nombreux boutons */
.button {
  border-radius: 12px;
}
```

Préférez un sélecteur contextualisé lorsque la structure réelle le permet :

```css
/* Exemple de principe : confirmer les classes dans le Shell réel */
.ma-zone-de-theme .mon-bouton {
  border-radius: 12px;
}
```

Les noms `.ma-zone-de-theme` et `.mon-bouton` sont des espaces réservés, pas des classes GNOME garanties. Remplacez-les par les classes réellement observées.

Ne créez pas une règle à partir d'un nom supposé. Un sélecteur inconnu peut être ignoré sans erreur visible.

## 6. Feuille de style propre à une extension

Une extension peut livrer sa propre feuille de style et la charger pendant son activation, puis la retirer lors de sa désactivation. Le cycle de vie doit être respecté : une feuille ajoutée sans être retirée peut laisser des styles actifs après le rechargement de l'extension.

Pour les développeurs d'extensions :

- chargez la feuille au moment approprié du cycle de vie ;
- retirez-la lors de la désactivation ;
- évitez les sélecteurs trop généraux ;
- utilisez des classes propres à l'extension ;
- ne dépendez pas de classes privées d'une autre extension ;
- testez l'activation, la désactivation et la réactivation ;
- vérifiez la compatibilité avec la version GNOME déclarée.

Le chapitre consacré au développement d'extensions détaille le cycle de vie JavaScript et les ressources. Ici, l'objectif est de comprendre l'impact de ces feuilles sur un thème global.

## 7. Diagnostiquer un conflit entre extensions

Lorsqu'un composant change d'apparence de façon inattendue :

1. reproduisez le problème avec le thème activé ;
2. relevez les extensions activées ;
3. désactivez uniquement l'extension suspecte dans la session de test ;
4. vérifiez si le rendu revient à la normale ;
5. réactivez-la et contrôlez son CSS ;
6. inspectez la spécificité et l'ordre des règles ;
7. testez une règle ciblée dans une copie de travail ;
8. vérifiez qu'aucun autre composant n'a changé.

Pour observer les messages du Shell pendant l'essai :

```sh
journalctl --user -f -o cat
```

Selon la distribution et la configuration du journal, tous les messages ne seront pas nécessairement disponibles. Conservez les erreurs exactes et la version de l'extension.

## 8. Activer et désactiver proprement une extension

Les commandes usuelles sont :

```sh
gnome-extensions disable UUID_DE_EXTENSION
gnome-extensions enable UUID_DE_EXTENSION
```

Une désactivation peut retirer immédiatement les acteurs et la feuille CSS de l'extension. Certaines modifications d'extension nécessitent toutefois une nouvelle session.

Sous Wayland, ne comptez pas sur le raccourci de redémarrage du Shell historiquement utilisé sous X11. Fermez la session et reconnectez-vous lorsque le Shell doit être redémarré.

Avant une désactivation, vérifiez que l'extension n'est pas indispensable à votre méthode de saisie, à l'accessibilité ou à une fonction de votre environnement.

## 9. Construire une compatibilité documentée

Un thème ne peut pas annoncer une compatibilité universelle avec toutes les extensions. Leurs versions, leurs classes CSS et leurs feuilles privées évoluent indépendamment de GNOME Shell.

Pour chaque extension prise en charge, consignez :

- son UUID ;
- sa version ;
- la version GNOME Shell testée ;
- les composants visuels vérifiés ;
- les éventuelles règles spécifiques ;
- les limites connues ;
- le résultat après activation et désactivation.

Si une mise à jour de l'extension modifie son interface, recommencez l'inspection avant de réutiliser les anciens sélecteurs.

## 10. Exercice : isoler un conflit de style

Choisissez une extension qui ajoute un indicateur au panneau.

1. Prenez une capture avec l'extension désactivée.
2. Activez l'extension et prenez une seconde capture.
3. Identifiez le composant ajouté.
4. Inspectez ses classes dans Looking Glass.
5. Consultez la feuille CSS de l'extension si elle existe.
6. Ajoutez une règle ciblée dans une copie du thème.
7. Vérifiez le panneau, le menu et les états survolé, actif et focus.
8. Désactivez puis réactivez l'extension.
9. Vérifiez que le rendu reste correct après une nouvelle connexion.

L'exercice est réussi lorsque le composant est personnalisé sans modifier les autres éléments du panneau.

## 11. Références

- [Documentation officielle des extensions GNOME](https://extensions.gnome.org/)
- [GNOME Shell 51.0 — sources](https://github.com/GNOME/gnome-shell/tree/51.0)
- [GNOME Shell — documentation de développement](https://gjs.guide/extensions/)


## 12. Ouvrir Looking Glass et inspecter un acteur

Looking Glass est l'outil de diagnostic intégré à GNOME Shell. Il permet d'observer l'état du Shell et d'inspecter des acteurs St. Il ne remplace pas l'inspection des sources : les classes et la hiérarchie observées doivent être rapprochées du code de la version installée.

Dans une session de test :

1. appuyez sur `Alt+F2` ;
2. saisissez `lg` puis validez ;
3. ouvrez l'onglet d'inspection ;
4. sélectionnez l'acteur concerné avec l'outil de sélection si celui-ci est disponible dans la version utilisée ;
5. relevez le type, les classes et la hiérarchie du composant ;
6. fermez Looking Glass et vérifiez que l'interface reste dans son état normal.

L'accès et la présentation de l'inspecteur peuvent évoluer selon GNOME Shell. Si l'outil de sélection ne permet pas de cibler un menu transitoire, ouvrez le menu avant de sélectionner l'acteur et recommencez. Certains acteurs disparaissent dès que le pointeur quitte leur zone.

Ne copiez pas un nom de classe à partir d'une capture ou d'un thème tiers. Relevez-le dans la session et confirmez-le dans le code de l'extension. Un nom de classe peut être créé dynamiquement ou n'exister que dans un état donné.

## 13. Localiser les fichiers d'une extension

Les extensions utilisateur sont généralement installées sous :

```text
~/.local/share/gnome-shell/extensions/UUID/
```

Les extensions installées pour tout le système peuvent se trouver dans un répertoire partagé de la distribution, notamment sous `/usr/share/gnome-shell/extensions/`. Le chemin exact dépend du paquet et de la distribution.

Pour identifier le répertoire de l'extension :

```sh
gnome-extensions info UUID_DE_EXTENSION
```

Examinez ensuite les fichiers de l'extension sans les modifier :

```sh
find ~/.local/share/gnome-shell/extensions/UUID_DE_EXTENSION \
  -maxdepth 3 -type f -print
```

Adaptez le chemin au répertoire indiqué par les informations de l'extension. Une extension système peut ne pas être présente dans le dossier utilisateur.

Recherchez les déclarations de classes et les feuilles de style :

```sh
grep -R -nE 'add_style_class_name|remove_style_class_name|add_style_pseudo_class|\.css' \
  ~/.local/share/gnome-shell/extensions/UUID_DE_EXTENSION
```

Cette recherche donne des pistes, pas une description complète du style calculé. Les classes peuvent être construites à partir de chaînes, les feuilles peuvent être chargées indirectement et les acteurs peuvent être créés par des dépendances. Confirmez toujours le résultat à l'exécution.

Ne modifiez pas directement une extension installée depuis extensions.gnome.org ou par le gestionnaire de paquets. Une mise à jour écraserait les changements et rendrait le diagnostic difficile à reproduire. Travaillez sur une copie ou sur un fork de l'extension, en respectant sa licence.

## 14. Comprendre les feuilles CSS chargées par une extension

Une feuille CSS peut être chargée à différents moments du cycle de vie. Une extension doit retirer ses ressources lors de sa désactivation. Si elle conserve un provider ou des acteurs après la désactivation, elle risque de laisser des effets visuels ou des références obsolètes.

Pour analyser une extension existante, recherchez dans ses sources :

- le point où la feuille CSS est chargée ;
- le point où elle est retirée ;
- les acteurs créés et détruits ;
- les classes ajoutées et retirées ;
- les signaux connectés et déconnectés ;
- les éventuelles modifications de prototypes ou de méthodes du Shell.

Ne supposez pas que toutes les extensions utilisent la même API de chargement CSS. La méthode dépend de la génération d'API et de l'architecture de l'extension. La référence exacte est le code GNOME Shell correspondant à la version déclarée, ainsi que les sources de l'extension.

Pour une extension que vous développez, regroupez les opérations dans des fonctions d'activation et de désactivation faciles à auditer. Conservez les références aux objets et connexions que vous créez afin de pouvoir les détruire proprement. Le chapitre 29 détaille le développement et les ressources d'extension.

## 15. Distinguer classe, pseudo-classe et état visuel

Une classe décrit généralement une catégorie ou une variante d'acteur. Une pseudo-classe représente un état, par exemple survolé, actif, focalisé ou désactivé. Un état visuel peut aussi être représenté par une classe ajoutée par le code de l'extension.

Pour comprendre pourquoi une règle ne s'applique pas :

1. observez le composant au repos ;
2. observez-le au survol ;
3. activez-le ou ouvrez son menu ;
4. placez le focus clavier dessus ;
5. comparez les classes et états entre chaque situation ;
6. vérifiez si l'extension change de classe ou si le moteur applique une pseudo-classe.

Un composant peut ne pas recevoir le focus clavier de la même façon qu'un widget GTK. N'inventez pas une pseudo-classe en vous fondant sur le CSS web : vérifiez les pseudo-classes prises en charge par St et celles effectivement émises par le composant.

Une règle correcte pour l'état normal peut masquer l'indication de focus ou rendre un état désactivé illisible. Le test doit donc couvrir les interactions, pas seulement le rendu statique.

## 16. Dépanner une extension qui ne se recharge pas

Lorsqu'un changement de CSS ne semble pas pris en compte :

1. vérifiez que vous modifiez bien le répertoire de l'extension active ;
2. vérifiez son UUID et sa version ;
3. recherchez les erreurs de syntaxe ou les ressources introuvables ;
4. désactivez puis réactivez l'extension ;
5. observez les journaux de session ;
6. si nécessaire, fermez la session puis reconnectez-vous ;
7. contrôlez que la feuille est chargée et retirée au bon moment.

Suivez les journaux utilisateur :

```sh
journalctl --user -f -o cat
```

Pour filtrer les messages contenant le nom d'une extension :

```sh
journalctl --user -b -o cat | grep -i 'nom de l extension'
```

Le texte des journaux varie selon l'extension. Un filtrage par nom peut manquer une erreur émise sous un autre identifiant ; en cas de doute, consultez les messages autour de l'heure du test sans filtre.

Sous Wayland, le redémarrage complet de la session est la méthode de référence lorsque le Shell lui-même doit être relancé. Ne conseillez pas `Alt+F2`, puis `r` comme procédure générale : cette méthode historique ne fonctionne pas dans une session Wayland.

## 17. Tester les interactions et la coexistence

Une extension peut sembler correcte au repos, mais provoquer des régressions lorsque plusieurs extensions sont activées ensemble. Construisez une séquence de test contrôlée :

1. testez le Shell sans extension tierce ;
2. activez une seule extension ;
3. vérifiez ses états et ses menus ;
4. activez une seconde extension qui touche une zone voisine ;
5. vérifiez les deux composants et le Shell natif ;
6. répétez avec les extensions réellement utilisées ;
7. désactivez-les une par une pour identifier un conflit.

Contrôlez au minimum les états normal, survolé, actif, désactivé et focus lorsqu'ils existent. Testez également les ouvertures et fermetures répétées, les changements d'espace de travail, le mode sombre et les facteurs d'échelle utilisés.

Documentez les conflits reproductibles avec les UUID et versions exacts. Une simple liste de noms d'extensions n'est pas suffisante pour retrouver le même environnement.

## 18. Exercice : produire un diagnostic vérifiable

Reprenez l'extension choisie dans l'exercice précédent et produisez un compte rendu :

- version GNOME Shell et session graphique ;
- UUID et version de l'extension ;
- emplacement de ses fichiers ;
- acteur ciblé et classes observées ;
- fichier CSS ou règles concernées ;
- états testés ;
- extensions coexistantes ;
- messages de journal pertinents ;
- résultat après désactivation et réactivation.

Le compte rendu doit permettre à une autre personne de reproduire le problème sans avoir à deviner les classes, versions ou chemins utilisés.
