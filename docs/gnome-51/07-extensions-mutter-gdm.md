# 7. Extensions, Mutter, GDM et session

## 7.1 Extensions Shell

Une extension est du JavaScript exécuté dans GNOME Shell. Elle peut ajouter panneaux, menus, indicateurs, raccourcis et CSS. Structure courante : `metadata.json`, `extension.js`, `stylesheet.css`, éventuellement `prefs.js`, ressources et traductions. Tout signal, timer, raccourci ou nœud ajouté doit être nettoyé à la désactivation. Éviter les patches de prototypes.

## 7.2 Schéma d'extensions Shell 51

Clés : `enabled-extensions`, `disabled-extensions`, `disable-user-extensions`, `allow-extension-installation`, `disable-extension-version-validation`, `favorite-apps`, `app-picker-layout`. Une extension est identifiée par UUID ; une extension désactivée explicitement peut prévaloir sur une extension activée.

```sh
gnome-extensions list
gnome-extensions info UUID
gnome-extensions enable UUID
gnome-extensions disable UUID
```

Confirmer les sous-commandes avec `gnome-extensions --help`. Ne pas désactiver le contrôle de version comme solution normale.

## 7.3 Thème ou extension ?

- **Besoin** : couleur, bordure, rayon, typographie ; **Mécanisme** : CSS
- **Besoin** : icône ou curseur ; **Mécanisme** : thème de ressources
- **Besoin** : ajouter indicateur ou menu ; **Mécanisme** : extension
- **Besoin** : nouveau comportement ; **Mécanisme** : extension
- **Besoin** : raccourci standard ; **Mécanisme** : GSettings
- **Besoin** : résolution / écran ; **Mécanisme** : Paramètres et Mutter
- **Besoin** : widget privé d'une application ; **Mécanisme** : API / préférences applicatives
- **Besoin** : écran GDM ; **Mécanisme** : configuration système distincte

## 7.4 Mutter

Mutter gère placement des fenêtres, espaces, écrans, échelle, capture et composition. Les décorations côté client sont dessinées par GTK/Libadwaita ; les décorations côté serveur dépendent du compositeur. Résolution, fréquence, rotation, disposition et échelle ne sont pas des propriétés CSS. Les options expérimentales peuvent changer.

## 7.5 GDM

GDM est une session système distincte. Un thème dans le home utilisateur ne modifie pas automatiquement l'écran de connexion. Toute personnalisation GDM doit être une cible séparée avec sauvegarde, privilèges, test de récupération et avertissement. Ne pas remplacer les fichiers système depuis l'export utilisateur.

## 7.6 Verrouillage et autres toolkits

Le verrouillage Shell, les notifications privées, veille et écran vide relèvent de plusieurs composants et préférences. Qt, Electron, Web, SDL et applications propriétaires ont leurs moteurs. Flatpak peut isoler l'accès aux thèmes. Les extensions ajoutent leurs propres styles.

## 7.7 Cycle de vie d'une extension

Une extension doit être conçue comme un composant temporaire de la session. Son code peut être chargé, activé, désactivé puis réactivé sans redémarrer l'ordinateur. La désactivation doit donc remettre le Shell dans l'état qui précédait l'activation.

Dans une extension moderne, le cycle de vie est généralement organisé autour de méthodes comme `enable()` et `disable()`. Les API exactes dépendent du modèle d'extension de la version GNOME ciblée ; consultez les exemples livrés avec GNOME Shell 51 avant de copier un ancien tutoriel.

Pendant l'activation, l'extension peut :

- créer un acteur St ou Clutter et l'ajouter à un conteneur du Shell ;
- connecter un signal à un objet GNOME ;
- enregistrer une action ou un raccourci ;
- installer un fournisseur CSS ou charger une feuille propre à l'extension ;
- démarrer une surveillance ou une tâche asynchrone ;
- modifier temporairement une propriété d'un composant existant.

Pour chaque opération, notez immédiatement comment l'annuler. Pendant la désactivation :

1. arrêtez les tâches et sources de temporisation créées par l'extension ;
2. déconnectez les signaux dont elle est propriétaire ;
3. retirez les raccourcis et actions enregistrés ;
4. retirez les acteurs ajoutés à l'interface ;
5. enlevez les fournisseurs CSS installés par l'extension ;
6. restaurez les propriétés qu'elle avait modifiées ;
7. libérez les références et ressources détenues.

Ne supprimez pas un signal ou un acteur appartenant au Shell ou à une autre extension. L'extension doit annuler uniquement ses propres effets. Une désactivation incomplète peut laisser des boutons en double, des raccourcis actifs, des références obsolètes ou des callbacks exécutés après la disparition de l'interface.

### Exemple de registre de ressources

Le principe suivant est un pseudocode pédagogique, pas un module prêt à installer. Il illustre le fait de conserver les identifiants nécessaires au nettoyage.

```js
enable() {
    this._signalIds = [];
    this._timeoutIds = [];
    this._actors = [];

    // Après chaque connexion, conserver l'identifiant retourné.
    // Après chaque temporisation, conserver son identifiant.
    // Après chaque création, conserver la référence de l'acteur.
}

disable() {
    for (const id of this._timeoutIds ?? []) {
        GLib.Source.remove(id);
    }

    for (const id of this._signalIds ?? []) {
        // Déconnecter sur l'objet exact auquel le signal appartient.
    }

    for (const actor of this._actors ?? []) {
        // Retirer uniquement les acteurs créés par cette extension.
    }

    this._timeoutIds = [];
    this._signalIds = [];
    this._actors = [];
}
```

Adaptez le nettoyage aux API réelles utilisées. Certains objets ont une méthode de destruction ou un mécanisme de cancellation dédié ; une simple suppression d'identifiant n'est pas universelle.

## 7.8 Ajouter une feuille CSS sans polluer le Shell

Une extension qui fournit du CSS doit isoler ses sélecteurs. Préfixez les classes que vous créez avec un nom stable propre à l'extension, par exemple `.mon-extension-status`, plutôt que de redéfinir globalement `.button`, `.label` ou `.popup-menu`.

Un sélecteur générique peut modifier des composants natifs ou ceux d'autres extensions. Préférez une classe dédiée sur le conteneur créé par votre extension, puis ciblez ses descendants.

Avant d'ajouter un fournisseur CSS :

1. confirmez le moteur de style utilisé par le composant ;
2. inspectez les sélecteurs disponibles dans GNOME Shell 51 ;
3. chargez uniquement la feuille nécessaire ;
4. gardez une référence au fournisseur pour pouvoir le retirer ;
5. testez l'activation, la désactivation et la réactivation ;
6. contrôlez le journal pour repérer les erreurs de parsing ou les propriétés inconnues.

Ne supposez pas que toutes les propriétés CSS de GTK ou d'un navigateur sont prises en charge par St. Les chapitres de référence St décrivent le moteur du Shell.

## 7.9 Déclarer et contrôler la compatibilité

Le fichier `metadata.json` identifie notamment l'extension par son UUID, son nom, sa description et les versions de Shell déclarées compatibles. Respectez le format attendu par GNOME Shell 51 et validez le JSON avant installation.

Exemple minimal illustratif :

```json
{
  "uuid": "exemple@local",
  "name": "Exemple local",
  "description": "Extension de test",
  "shell-version": ["51"]
}
```

Cet exemple ne contient pas nécessairement tous les champs recommandés par le modèle d'extension courant. Vérifiez la documentation GNOME 51 et les métadonnées d'une extension maintenue pour la même version. Ne déclarez pas une version compatible uniquement pour contourner le contrôle : testez réellement l'activation et les interactions.

Contrôles de base :

```sh
python3 -m json.tool metadata.json >/dev/null
gnome-shell --version
gnome-extensions info exemple@local
journalctl --user -b | grep -iE 'extension|gnome-shell'
```

La commande `gnome-extensions info` ne remplace pas un test d'activation. Relevez séparément l'état déclaré, l'état activé et les erreurs éventuelles.

## 7.10 Installer et tester une extension locale

Pour un essai utilisateur, l'emplacement courant des extensions locales est :

```text
~/.local/share/gnome-shell/extensions/UUID/
```

Le répertoire doit porter exactement l'UUID déclaré dans `metadata.json`. Vérifiez la structure avant de copier :

```sh
find . -maxdepth 2 -type f -print
python3 -m json.tool metadata.json
```

Copiez l'extension dans un compte de test ou une machine virtuelle. Activez-la avec son UUID exact, observez les journaux, puis désactivez-la et vérifiez que tous ses éléments ont disparu. Répétez le cycle plusieurs fois : une extension qui fonctionne au premier chargement mais échoue à la réactivation possède souvent un nettoyage incomplet.

Ne développez pas en remplaçant des fichiers d'extension dans une session contenant des données importantes. Une exception JavaScript peut perturber le Shell et rendre nécessaire une reconnexion.

## 7.11 Diagnostiquer une extension défaillante

Procédez du plus simple au plus spécifique :

1. vérifiez l'UUID et le chemin réellement installés ;
2. validez la syntaxe JSON de `metadata.json` ;
3. vérifiez la version de GNOME Shell et la déclaration de compatibilité ;
4. consultez les journaux immédiatement après l'activation ;
5. désactivez les autres extensions pour rechercher un conflit ;
6. testez sans votre feuille CSS ;
7. réintroduisez les fonctionnalités une par une ;
8. testez désactivation et réactivation.

Commandes utiles :

```sh
gnome-extensions list --enabled
gnome-extensions info UUID
journalctl --user -b -f
```

Pour isoler un conflit, ne désactivez qu'une extension à la fois et notez le résultat. Ne supprimez pas le dossier d'une extension pendant que la session l'utilise. Désactivez-la d'abord, puis conservez une copie avant toute modification.

### L'extension n'apparaît pas dans la liste

Vérifiez que le répertoire porte l'UUID exact, que `metadata.json` est lisible et que le fichier n'est pas placé dans un sous-répertoire supplémentaire. Contrôlez aussi les permissions de lecture.

### L'extension s'active puis disparaît

Cherchez une exception JavaScript dans le journal, vérifiez les API utilisées et les ressources chargées. Une version de Shell non prise en charge ou un import obsolète peut provoquer un échec pendant l'activation.

### L'interface reste modifiée après désactivation

Le nettoyage ne retire probablement pas tous les effets créés. Vérifiez les signaux, temporisations, acteurs, fournisseurs CSS, raccourcis et propriétés modifiées. Ajoutez une étape de nettoyage pour chaque ressource créée.

### Deux extensions modifient le même composant

Désactivez-les séparément pour identifier le conflit. Une extension ne doit pas supposer qu'elle est la seule à modifier un acteur partagé. Préférez l'ajout d'un acteur indépendant à la modification profonde d'un composant interne.

## 7.12 GDM : distinguer personnalisation utilisateur et système

GDM démarre avant la session personnelle et utilise un compte et une configuration système distincts. Les thèmes installés dans `~/.themes` ou `~/.local/share/themes` ne sont pas automatiquement disponibles pour l'écran de connexion.

Avant toute intervention GDM, identifiez la distribution, la version du paquet GDM, le mécanisme de thème réellement pris en charge et le chemin de configuration actif. Les méthodes historiques qui remplacent des fichiers du thème système peuvent devenir incompatibles après une mise à jour.

Une procédure de personnalisation système doit impérativement prévoir :

- une sauvegarde datée des fichiers et réglages modifiés ;
- la liste exacte des fichiers remplacés ;
- les permissions et propriétaires d'origine ;
- un moyen de restaurer depuis une console ou une session de secours ;
- un test après redémarrage, pas seulement après déconnexion ;
- une procédure de retour arrière vérifiée.

Ne copiez pas un thème utilisateur complet dans le répertoire de GDM sans vérifier les besoins et les permissions. N'appliquez pas de commande récursive de changement de propriétaire sur un répertoire système entier. N'ajoutez pas de privilèges administrateur à un installateur de thème utilisateur.

## 7.13 Flatpak, thèmes et portails

Une application Flatpak peut ne pas voir les mêmes chemins de thèmes que les applications installées nativement. Son environnement est isolé et l'accès aux ressources de l'hôte dépend des permissions, des runtimes et des mécanismes d'intégration de la distribution.

Si une application Flatpak n'adopte pas le thème :

1. vérifiez si l'application est réellement un Flatpak ;
2. relevez son identifiant et son runtime ;
3. comparez le rendu avec une application native du même toolkit ;
4. contrôlez les permissions et les chemins accessibles ;
5. vérifiez les thèmes et extensions disponibles dans le runtime ;
6. testez après redémarrage complet de l'application.

Ne concluez pas à un défaut CSS global sur la base d'une seule application isolée. Ne modifiez pas les permissions Flatpak de manière large pour forcer l'accès à tout le répertoire personnel. Toute permission ajoutée doit être minimale, justifiée et réversible.

## 7.14 Fiche de validation d'une extension

Pour chaque extension incluse dans la cible du thème, conservez une fiche dans le dossier de test :

- nom et UUID exacts ;
- version de l'extension et provenance ;
- version de GNOME Shell testée ;
- dépendances et extensions concurrentes ;
- composants visuels ajoutés ou modifiés ;
- classes CSS réellement observées ;
- état d'activation après démarrage ;
- résultat du cycle activation/désactivation/réactivation ;
- erreurs ou avertissements du journal ;
- limites connues et date du dernier essai.

Une extension non testée doit être indiquée comme non vérifiée. Ne la présentez pas comme compatible parce que son nom apparaît dans une liste d'extensions disponibles.

## 7.15 Exercice guidé : analyser un conflit de thème

L'objectif est de déterminer si un changement de rendu provient du thème Shell, d'une extension ou d'une application.

1. Capturez le composant dans son état initial.
2. Notez les extensions activées.
3. Désactivez temporairement une extension non essentielle depuis un compte de test.
4. Capturez exactement le même état.
5. Réactivez l'extension et vérifiez le retour au rendu initial.
6. Répétez avec la feuille CSS de l'extension si elle est séparable.
7. Inspectez le journal et identifiez les erreurs.
8. Concluez en indiquant le composant propriétaire et la règle ou l'extension responsable.

Ne désactivez pas une extension de sécurité, d'accessibilité ou nécessaire à la session sur votre compte principal pour réaliser cet exercice.

## 7.16 Sources et vérification de version

Pour toute extension qui cible GNOME Shell 51, vérifiez le modèle d'extension, les API et les exemples directement dans les sources et la documentation de cette version. Les tutoriels anciens peuvent utiliser un modèle de cycle de vie ou des imports qui ne sont plus valides.

- [GNOME Shell 51.0 — code source](https://gitlab.gnome.org/GNOME/gnome-shell/-/tree/51.0)
- [GNOME Shell — extensions et documentation](https://gjs.guide/extensions/)
- [GNOME Shell — documentation API](https://gnome.pages.gitlab.gnome.org/gnome-shell/)
- [Flatpak — documentation des permissions](https://docs.flatpak.org/en/latest/sandbox-permissions.html)

Les liens génériques peuvent afficher la documentation de la version la plus récente. Pour une affirmation de compatibilité GNOME 51, recoupez toujours avec la branche 51.0 du code source et testez dans une session GNOME 51 réelle.
