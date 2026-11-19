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

## 3. Structure minimale

```text
org.example.mon-extension/
├── metadata.json
├── extension.js
├── stylesheet.css
├── prefs.js
└── README.md
```

Tous les fichiers ne sont pas obligatoires. `prefs.js` n'est utile que si l'extension possède des préférences. Une feuille CSS est facultative.

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

L'UUID doit être unique. La clé `shell-version` déclare les versions prises en charge ; elle ne rend pas automatiquement le code compatible. Testez chaque version annoncée.

## 4. Comprendre le cycle de vie

GNOME Shell charge le module, crée l'objet extension, puis appelle `enable()` lorsque l'extension est activée. Lorsqu'elle est désactivée, `disable()` doit retirer tout ce que `enable()` a ajouté.

Règle essentielle : chaque connexion, timer, raccourci, acteur, menu ou provider créé doit avoir une opération de nettoyage correspondante.

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

Le bouton est détruit à la désactivation. Si vous connectez un signal sur un objet qui survit à l'extension, conservez l'identifiant renvoyé par `connect()` et déconnectez-le dans `disable()`.

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

Pour un timer GLib, conservez l'identifiant retourné par la fonction d'ajout puis retirez la source à la désactivation. Ne supposez pas que détruire un widget annule un timer indépendant.

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

## 9. Installer et diagnostiquer

Depuis le dossier parent de l'extension :

```sh
mkdir -p ~/.local/share/gnome-shell/extensions
cp -a org.example.mon-extension \
  ~/.local/share/gnome-shell/extensions/mon-extension@example.org
gnome-extensions list
gnome-extensions info mon-extension@example.org
gnome-extensions enable mon-extension@example.org
```

Pour désactiver :

```sh
gnome-extensions disable mon-extension@example.org
```

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
