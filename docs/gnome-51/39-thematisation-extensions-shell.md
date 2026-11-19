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
