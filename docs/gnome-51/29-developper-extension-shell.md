# Développer une extension GNOME Shell 51

Une extension ajoute un comportement au bureau. Elle peut créer un indicateur, un menu, un raccourci, une page de préférences ou des composants visuels. Contrairement à un thème CSS, elle exécute du JavaScript dans le processus GNOME Shell : une erreur peut donc affecter toute la session.

Ce chapitre construit une extension minimale, explique son cycle de vie et montre comment éviter les fuites de ressources.

## 1. Choisir entre CSS, réglage et extension

Utilisez le mécanisme le moins puissant qui répond au besoin :

- Couleur, rayon, bordure, typographie d'un acteur existant : thème CSS.
- Option déjà exposée par GNOME : Paramètres ou GSettings.
- Nouvel indicateur, menu, action ou comportement : extension.
- Modification profonde du fonctionnement du Shell : évitez les patches internes si une API d'extension suffit.

Une extension ne doit pas servir à contourner une propriété CSS simplement parce que le sélecteur est difficile à trouver.

## 2. Préparer l'environnement

Vérifiez la version et les outils :

```sh
gnome-shell --version
gnome-extensions --version
gnome-extensions --help
```

Développez dans un compte ou une machine virtuelle de test. Une extension défectueuse peut rendre la session instable. Conservez un moyen de désactivation depuis une session de secours.

Le répertoire utilisateur habituel est :

```text
~/.local/share/gnome-shell/extensions/<uuid>/
```

Le nom du dossier doit correspondre exactement à l'UUID déclaré dans `metadata.json`.

## 3. Structure minimale et fichiers requis

Une extension GNOME Shell moderne doit au minimum fournir `metadata.json` et son module principal `extension.js`. Les autres fichiers dépendent des fonctionnalités :

```text
mon-extension@example.org/
├── metadata.json
├── extension.js
├── stylesheet.css       # facultatif
├── prefs.js              # facultatif
├── schemas/              # facultatif
│   └── org.example.mon-extension.gschema.xml
└── README.md             # documentation du projet
```

Le dossier installé doit porter le même UUID que les métadonnées. Le fichier `prefs.js` n'est chargé que si l'extension fournit une interface de préférences. Le schéma GSettings est nécessaire uniquement si l'extension stocke des options de cette manière. Une feuille CSS n'est utile que si l'extension crée ou stylise des acteurs.

Exemple de métadonnées GNOME Shell 51 :

```json
{
  "uuid": "mon-extension@example.org",
  "name": "Mon extension",
  "description": "Exemple pédagogique d'extension GNOME Shell.",
  "shell-version": ["51"],
  "version": 1
}
```

L'UUID doit être unique, stable et identique au nom du dossier. La clé `shell-version` déclare les versions prises en charge ; elle ne rend pas automatiquement le code compatible. Testez chaque version annoncée. N'ajoutez pas une version à cette liste uniquement pour faire disparaître un avertissement : cette déclaration est une promesse de compatibilité.

## 4. Comprendre le cycle de vie et l'état

GNOME Shell charge le module, crée l'objet extension, puis appelle `enable()` lorsque l'extension est activée. Lorsqu'elle est désactivée, `disable()` doit retirer tout ce que `enable()` a ajouté. Une même instance peut être activée, désactivée puis réactivée : le code ne doit donc pas supposer que `enable()` ne sera appelé qu'une seule fois.

Règle essentielle : chaque connexion, timer, raccourci, acteur, menu ou provider créé doit avoir une opération de nettoyage correspondante.

Organisez les ressources comme des propriétés de l'instance :

- initialisez les propriétés à `null` ou à une valeur neutre ;
- créez les objets dans `enable()` ;
- déconnectez et détruisez les objets dans `disable()` ;
- remettez les propriétés dans leur état neutre après nettoyage ;
- rendez le nettoyage sûr même si une initialisation partielle a échoué.

Ne masquez pas une erreur d'initialisation en laissant une extension à moitié active. Si une étape obligatoire échoue, nettoyez les ressources déjà créées et signalez l'erreur dans les journaux.

- `enable()` : créer les éléments et connecter les signaux.
- `disable()` : déconnecter les signaux, annuler les timers, retirer les raccourcis et détruire les acteurs.
- Ne conservez pas de référence globale à un acteur détruit.
- Ne lancez pas d'opération asynchrone qui pourrait modifier l'interface après désactivation sans vérifier son cycle de vie.

## 5. Exemple : ajouter un indicateur au panneau

Cet exemple ajoute un bouton simple au panneau. Il illustre le cycle de vie ; il ne constitue pas un modèle de menu complet.

```javascript
import { Extension } from
  'resource:///org/gnome/shell/extensions/extension.js';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from
  'resource:///org/gnome/shell/ui/panelMenu.js';
import St from 'gi://St';

export default class ExampleExtension extends Extension {
  enable() {
    this._indicator = new PanelMenu.Button(0.0, 'Mon extension');
    const label = new St.Label({
      text: 'Exemple',
      y_align: St.Align.MIDDLE,
    });

    this._indicator.add_child(label);
    Main.panel.addToStatusArea(this.uuid, this._indicator);
  }

  disable() {
    this._indicator?.destroy();
    this._indicator = null;
  }
}
```

Le bouton est détruit à la désactivation. Le code d'exemple est volontairement réduit : un véritable indicateur doit aussi gérer ses états, son accessibilité, ses actions et ses erreurs. Si vous connectez un signal sur un objet qui survit à l'extension, conservez l'identifiant renvoyé par `connect()` et déconnectez-le dans `disable()`.

Ne connectez pas un signal sur un objet persistant en supposant que la destruction de votre bouton supprimera automatiquement cette connexion. La durée de vie de la source du signal et celle de l'acteur sont deux choses différentes.

## 6. Connexions de signaux et temporisateurs

Une fuite fréquente consiste à connecter un signal à un objet persistant sans déconnecter le signal. Une autre consiste à laisser un timeout se déclencher après désactivation.

Conservez explicitement les identifiants :

```javascript
this._signalId = object.connect('notify::property', () => {
  this._refresh();
});

// Dans disable()
if (this._signalId) {
  object.disconnect(this._signalId);
  this._signalId = 0;
}
```

Pour un timer GLib, conservez l'identifiant retourné par la fonction d'ajout puis retirez la source à la désactivation. Ne supposez pas que détruire un widget annule un timer indépendant. Faites de même pour les raccourcis globaux et les gestionnaires d'événements.

Exemple de principe pour une source GLib :

```javascript
import GLib from 'gi://GLib';

// Dans enable()
this._timeoutId = GLib.timeout_add(
  GLib.PRIORITY_DEFAULT,
  1000,
  () => {
    this._refresh();
    return GLib.SOURCE_CONTINUE;
  }
);

// Dans disable()
if (this._timeoutId !== null) {
  GLib.Source.remove(this._timeoutId);
  this._timeoutId = null;
}
```

L'exemple montre la gestion de l'identifiant et doit être adapté au besoin réel. Une source qui doit s'arrêter d'elle-même peut retourner `GLib.SOURCE_REMOVE`. Vérifiez toujours que le callback ne peut plus être appelé après la destruction des objets qu'il utilise.

## 7. Ajouter une feuille de style

La classe `Extension` expose `loadStylesheet()` et `unloadStylesheet()`. Chargez la feuille lors de l'activation et retirez-la à la désactivation :

```javascript
enable() {
  this.loadStylesheet();
  // Créer les acteurs de l'extension.
}

disable() {
  // Détruire les acteurs de l'extension.
  this.unloadStylesheet();
}
```

Exemple CSS :

```css
.mon-extension-indicator {
  padding: 0 8px;
  border-radius: 8px;
}
```

Ajoutez votre propre classe aux acteurs. Évitez les sélecteurs génériques tels que `label` ou `button`, qui pourraient modifier les composants du Shell sans rapport avec l'extension.

## 8. Préférences et GSettings

Les préférences sont une interface GTK séparée du processus Shell. Utilisez `ExtensionPreferences` pour construire la fenêtre de préférences et un schéma GSettings pour stocker les options.

Exemple de schéma :

```xml
<schemalist>
  <schema id="org.example.mon-extension"
          path="/org/example/mon-extension/">
    <key name="show-label" type="b">
      <default>true</default>
      <summary>Afficher le libellé</summary>
      <description>Affiche le texte dans le panneau.</description>
    </key>
  </schema>
</schemalist>
```

Compilez les schémas avec `glib-compile-schemas` et validez-les avant installation :

```sh
glib-compile-schemas --strict schemas/
```

Ne modifiez pas directement les fichiers de schéma du système. Le schéma livré par l'extension doit avoir un identifiant propre et un chemin cohérent.

## 9. Installer, mettre à jour et diagnostiquer

Depuis le dossier parent de l'extension, installez le contenu dans le répertoire qui porte exactement l'UUID :

```sh
install -d "$HOME/.local/share/gnome-shell/extensions/mon-extension@example.org"
cp -a org.example.mon-extension/. \
  "$HOME/.local/share/gnome-shell/extensions/mon-extension@example.org/"
```

Cette copie met à jour les fichiers présents mais ne retire pas les fichiers obsolètes. Pour une mise à jour de développement propre, sauvegardez vos éventuelles données locales, supprimez uniquement le répertoire exact de cette extension, recréez-le et recopiez les sources. Ne faites pas de suppression par motif ou avec une variable non vérifiée.

Vérifiez ensuite que GNOME détecte les métadonnées :

```sh
gnome-extensions list
gnome-extensions info mon-extension@example.org
```

Si vous avez modifié les métadonnées, le schéma ou les fichiers, désactivez l'extension avant de copier les nouvelles versions, puis réactivez-la. Selon la version et la session, un rechargement peut être nécessaire ; ne supposez pas que le processus Shell recharge automatiquement chaque module.

```sh
gnome-extensions disable mon-extension@example.org
gnome-extensions enable mon-extension@example.org
```

Cette séquence ne doit être exécutée qu'après avoir vérifié que l'extension est installée et que l'environnement permet sa réactivation.

Pour désactiver :

```sh
gnome-extensions disable mon-extension@example.org
```

Pour supprimer l'extension après l'avoir désactivée, vérifiez l'UUID et le chemin avant de supprimer le seul répertoire concerné :

```sh
rm -rf -- "$HOME/.local/share/gnome-shell/extensions/mon-extension@example.org"
```

Ne supprimez pas le répertoire parent `extensions`, qui peut contenir d'autres extensions.

Consultez les erreurs de session :

```sh
journalctl --user -b --no-pager | grep -i gnome-shell
```

La commande de redémarrage du Shell dépend du type de session. Ne supposez pas qu'un redémarrage interactif est disponible sous Wayland. Préférez une session de test redémarrable.

## 10. Compatibilité et API privées

Les modules internes de GNOME Shell ne constituent pas une API stable. Un import depuis `resource:///org/gnome/shell/ui/` peut changer entre versions, même si l'extension est toujours syntaxiquement valide.

Pour maintenir une extension :
1. fixez les versions explicitement déclarées ;
2. comparez les API utilisées avec les sources de chaque version ;
3. testez activation, désactivation et réactivation ;
4. testez une session après déconnexion/reconnexion ;
5. vérifiez qu'aucun signal ou timer ne subsiste ;
6. documentez les limitations.

## 11. Publication et sécurité

Une extension s'exécute avec les droits du processus Shell de l'utilisateur. N'exécutez pas de commandes système arbitraires, ne téléchargez pas de code au runtime et ne demandez pas de privilèges administrateur pour une simple personnalisation visuelle.

Fournissez un UUID stable, une description précise, une licence, les versions testées, des instructions de désactivation et un historique de changements.

## 12. Références

- [Guide officiel des extensions GNOME](https://gjs.guide/extensions/)
- [Extensions GNOME — administration](https://help.gnome.org/system-admin-guide/extensions.html)
- [Sources GNOME Shell 51](https://github.com/GNOME/gnome-shell/tree/51.0)
- [Référence GJS](https://gjs-docs.gnome.org/)
