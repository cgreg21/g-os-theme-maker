# CSS des applications, GResource et thèmes embarqués

Un thème global n'est pas toujours prioritaire. Les applications peuvent embarquer leurs propres feuilles CSS dans un bundle GResource, charger un provider à l'exécution ou ajouter des classes privées à leurs widgets. Comprendre ce mécanisme explique pourquoi certaines applications ne suivent pas le thème du bureau.

## 1. Les trois sources de style d'une application

Une application GTK peut recevoir du style de plusieurs endroits :

- thème GTK installé dans les répertoires XDG ;
- feuille CSS propre à l'application ;
- provider CSS ajouté par un composant ou un widget.

L'application peut aussi dessiner elle-même une partie du rendu. Dans ce cas, aucun sélecteur global ne peut nécessairement modifier le résultat.

Le thème du bureau et le CSS applicatif sont deux responsabilités différentes. Un développeur d'application doit utiliser ses propres classes CSS plutôt que dépendre de sélecteurs privés d'un thème tiers.

## 2. Qu'est-ce que GResource ?

GResource est le système de ressources compilées de GLib. Il permet d'intégrer des fichiers dans l'application : CSS, UI GTK Builder, icônes, traductions et autres données.

Le fichier XML décrit les ressources et leur chemin logique :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gresources>
  <gresource prefix="/org/example/MonApplication">
    <file>style.css</file>
  </gresource>
</gresources>
```

Avec ce fichier placé dans le répertoire `data/`, le fichier CSS sera accessible sous le chemin de ressource :

```text
/org/example/MonApplication/style.css
```

Ce chemin n'est pas un chemin du système de fichiers. Il désigne une ressource intégrée au programme.

Le préfixe est un espace de noms choisi par le projet. Il doit être suffisamment spécifique pour éviter les collisions avec les ressources d'autres bibliothèques. Le nom du fichier peut être remplacé dans le bundle par un alias explicite :

```xml
<gresource prefix="/org/example/MonApplication">
  <file alias="css/application.css">style.css</file>
</gresource>
```

Dans ce cas, le chemin logique devient `/org/example/MonApplication/css/application.css`. Le chemin source reste relatif au répertoire source indiqué à la compilation. Distinguez toujours le chemin du fichier sur disque du chemin logique exposé par GResource.

## 3. Compiler les ressources

Avec l'outil GLib :

```sh
glib-compile-resources resources.gresource.xml \
  --sourcedir=data \
  --target=app-resources.c \
  --generate-source
```

Pour générer un fichier binaire autonome :

```sh
glib-compile-resources resources.gresource.xml \
  --sourcedir=data \
  --target=app.gresource
```

Le premier mode produit du code source à compiler avec l'application. Le second produit un bundle à distribuer ou enregistrer selon la stratégie du projet.

Dans Meson, le module GNOME fournit `compile_resources()` :

```meson
gnome = import('gnome')

resources = gnome.compile_resources(
  'app-resources',
  'resources.gresource.xml',
  source_dir: 'data',
  c_name: 'app'
)
```

Ajoutez la ressource générée aux sources de la cible de l'application. Vérifiez la syntaxe Meson avec la version installée et les exemples du projet.

## 4. Charger une feuille CSS dans GTK 4

Exemple Python GTK 4 :

```python
from gi.repository import Gtk, Gdk

provider = Gtk.CssProvider()
provider.load_from_resource(
    "/org/example/MonApplication/style.css"
)

display = Gdk.Display.get_default()
Gtk.StyleContext.add_provider_for_display(
    display,
    provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
)
```

Le provider doit rester référencé aussi longtemps que nécessaire. Chargez-le après l'initialisation GTK et vérifiez le résultat dans l'application concernée. Pour une application réelle, conservez le provider dans un attribut de l'application ou de l'objet qui gère son cycle de vie. Ne le créez pas dans une fonction locale qui se termine immédiatement.

Exemple de gestion explicite du provider dans une application GTK 4 :

```python
from gi.repository import Gtk, Gdk

class Application(Gtk.Application):
    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.css_provider = Gtk.CssProvider()
        self.css_provider.connect(
            "parsing-error",
            self.on_css_error,
        )
        self.css_provider.load_from_resource(
            "/org/example/MonApplication/style.css"
        )

        display = Gdk.Display.get_default()
        if display is None:
            raise RuntimeError("Aucun écran GTK disponible")

        self.css_display = display
        Gtk.StyleContext.add_provider_for_display(
            display,
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def on_css_error(self, provider, section, error):
        print(f"Erreur CSS : {error}")

    def do_shutdown(self):
        if getattr(self, "css_display", None) is not None:
            Gtk.StyleContext.remove_provider_for_display(
                self.css_display,
                self.css_provider,
            )
            self.css_display = None
            self.css_provider = None

        Gtk.Application.do_shutdown(self)
```

Ce patron illustre la durée de vie du provider et son retrait. Adaptez la classe à la structure réelle de votre application. Dans une application multi-écrans ou multi-fenêtres, définissez clairement si le provider doit être global au display ou limité à un contexte plus restreint.

La priorité `APPLICATION` est adaptée à une feuille applicative ordinaire. N'utilisez pas systématiquement une priorité supérieure pour écraser les styles du thème : cela peut dégrader la cohérence des composants.

## 5. Charger une feuille CSS dans GTK 3

GTK 3 utilise un provider associé à l'écran :

```python
from gi.repository import Gtk, Gdk

provider = Gtk.CssProvider()
provider.load_from_resource(
    "/org/example/MonApplication/style.css"
)

screen = Gdk.Screen.get_default()
Gtk.StyleContext.add_provider_for_screen(
    screen,
    provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
)
```

Cette API GTK 3 n'est pas interchangeable avec celle de GTK 4. Gardez des implémentations séparées si votre application prend en charge les deux générations de GTK.

Le provider doit lui aussi rester vivant tant que la feuille est active. Si l'application le retire explicitement, utilisez `Gtk.StyleContext.remove_provider_for_screen()` avec le même écran et le même provider. Évitez de multiplier les providers à chaque ouverture de fenêtre : un provider global peut être installé une fois au démarrage et retiré à l'arrêt de l'application.

Exemple de retrait :

```python
Gtk.StyleContext.remove_provider_for_screen(
    screen,
    provider,
)
```

Dans GTK 3, connectez également le signal `parsing-error` du provider pendant le développement afin de repérer les propriétés ou sélecteurs invalides. Les propriétés CSS disponibles ne sont pas identiques entre GTK 3, GTK 4 et St.

## 6. Préférer des classes applicatives explicites

Dans le code de l'application, ajoutez une classe à l'élément à personnaliser :

```python
widget.add_css_class("account-summary")
```

Puis utilisez un sélecteur limité :

```css
.account-summary {
  padding: 12px;
  border-radius: 12px;
}

.account-summary:focus-within {
  outline: 2px solid var(--accent-color);
}
```

Les classes applicatives doivent être documentées et stables à l'échelle du projet. Ne réutilisez pas une classe interne d'un thème tiers comme contrat d'API.

GTK 3 utilise notamment `get_style_context().add_class()` pour ajouter une classe ; GTK 4 expose `add_css_class()`. Vérifiez les API selon la version et le langage.

## 7. Déboguer le chargement et les erreurs CSS

Un provider chargé ne garantit pas que chaque règle soit valide ni qu'elle corresponde à un widget. Séparez les diagnostics :

- ressource introuvable : vérifiez le préfixe, l'alias et le bundle compilé ;
- erreur de syntaxe : écoutez `parsing-error` et consultez les journaux ;
- règle sans effet : vérifiez le nœud CSS, les classes et la spécificité ;
- style écrasé : examinez la priorité des providers et les règles applicatives ;
- propriété ignorée : vérifiez la prise en charge par la version GTK utilisée.

Le signal `parsing-error` fournit un emplacement et une erreur de parsing. Il ne signale pas nécessairement une règle syntaxiquement valide mais sans effet sur le widget ciblé. Pour ce dernier cas, l'inspecteur reste nécessaire.

GTK Inspector expose des informations sur l'application et ses ressources. Il peut notamment aider à repérer le chemin de ressources utilisé et à charger des règles CSS temporaires.

Pour ouvrir l'inspecteur, lancez une application compatible avec :

```sh
GTK_DEBUG=interactive nom-de-l-application
```

Dans l'inspecteur :
1. sélectionnez le widget ;
2. relevez ses nœuds CSS et classes ;
3. consultez les providers actifs ;
4. testez une règle temporaire très ciblée ;
5. vérifiez si une règle plus prioritaire la remplace ;
6. comparez le rendu avec et sans la feuille de l'application.

Procédez avec une seule modification à la fois. Une règle temporaire qui fonctionne dans l'inspecteur prouve que le widget peut être stylé, mais pas que le chemin GResource ou le provider de production est correctement configuré.

L'inspecteur est un outil de diagnostic, pas une garantie que l'application accepte un thème utilisateur particulier.

## 8. Flatpak et chemins de ressources

Une application Flatpak fonctionne dans un environnement isolé. Les chemins du système hôte ne sont pas nécessairement visibles dans le sandbox. Les thèmes disponibles dépendent des extensions de runtime, des permissions et de la manière dont l'application charge ses ressources.

Un CSS embarqué dans GResource est accessible à l'application parce qu'il fait partie de son paquet. Une feuille placée arbitrairement dans le home de l'utilisateur peut être invisible ou ignorée.

Pour diagnostiquer une application Flatpak :
- identifiez son identifiant ;
- relevez le runtime et les extensions installées ;
- vérifiez les permissions et chemins réellement accessibles ;
- inspectez la version GTK/Libadwaita dans le sandbox ;
- ne concluez pas que le thème hôte est cassé avant d'avoir vérifié l'isolation.

## 9. Comment personnaliser une application qui embarque son CSS

Ordre recommandé :

1. recherchez une préférence officielle de thème ou d'apparence ;
2. vérifiez si l'application expose un CSS utilisateur documenté ;
3. inspectez les providers et les ressources ;
4. vérifiez si le composant est dessiné par l'application ;
5. si aucune extension n'est prévue, considérez le style comme non personnalisable depuis un thème global.

Ne modifiez pas directement le bundle installé : une mise à jour écrasera les changements et la signature ou l'intégrité du paquet peut être affectée.

## 10. Exercices

### Exercice A — repérer un CSS embarqué

Dans une application de test, ouvrez GTK Inspector et cherchez les ressources CSS chargées.

### Exercice B — créer un provider

Ajoutez une feuille CSS dans GResource et appliquez-la à un widget portant une classe dédiée.

### Exercice C — comparer GTK 3 et GTK 4

Reproduisez le même composant dans deux petites applications. Comparez les APIs de provider et les nœuds CSS.

### Exercice D — Flatpak

Comparez une application native et sa version Flatpak. Relevez le runtime, les versions de bibliothèque et les ressources accessibles.

## 11. Références

- [GResource — GLib](https://docs.gtk.org/gio/struct.Resource.html)
- [Construire une application GTK 4 et compiler ses ressources](https://docs.gtk.org/gtk4/getting_started.html)
- [Construire une application GTK 3 et compiler ses ressources](https://docs.gtk.org/gtk3/getting_started.html)
- [GTK 3 — CSS providers](https://docs.gtk.org/gtk3/class.CssProvider.html)
- [GTK 4 — CSS providers](https://docs.gtk.org/gtk4/class.CssProvider.html)
- [GTK Inspector](https://developer.gnome.org/documentation/tools/inspector.html)
- [Flatpak — documentation](https://docs.flatpak.org/)
