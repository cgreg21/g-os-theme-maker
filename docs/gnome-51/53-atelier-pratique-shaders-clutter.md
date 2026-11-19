# 53. Atelier pratique : créer des effets GPU pour GNOME Shell 51

Ce chapitre transforme les notions du chapitre 52 en un petit projet d'extension. L'objectif est de construire un acteur indépendant, de lui appliquer un shader Cogl via Clutter.ShaderEffect, de tester son rendu et de nettoyer correctement les ressources.

Le projet est volontairement limité à un acteur créé par l'extension. Il ne modifie pas les fenêtres des autres applications et ne capture pas l'arrière-plan du bureau. Il constitue un terrain d'expérimentation sûr pour comprendre le pipeline.

## 1. Résultat et périmètre

L'extension ajoute une carte de démonstration dans le groupe d'interface du Shell. Un shader transforme ses couleurs en niveaux de gris mélangés à la couleur d'origine.

Ce choix permet de vérifier plusieurs étapes sans dépendre d'une capture d'écran externe :

- création d'un acteur St ;
- construction d'un Cogl.Snippet ;
- insertion du code GLSL dans le hook fragment ;
- création de Clutter.ShaderEffect ;
- attachement de l'effet à l'acteur ;
- suppression de l'acteur et de ses ressources à la désactivation.

Le shader est statique : il ne possède ni timer ni uniforme animé. C'est volontaire. Commencez par valider un pipeline simple avant d'ajouter une animation ou des paramètres dynamiques.

## 2. Arborescence du projet

Créez le dossier suivant :

~~~text
shader-lab@example.org/
├── metadata.json
├── extension.js
└── stylesheet.css
~~~

Le nom du dossier doit être identique à l'UUID déclaré dans les métadonnées.

### metadata.json

~~~json
{
  "uuid": "shader-lab@example.org",
  "name": "Shader Lab",
  "description": "Démonstration d'un effet Cogl et Clutter.ShaderEffect.",
  "shell-version": ["51"],
  "version": 1
}
~~~

La déclaration de version ne garantit pas la compatibilité : elle indique uniquement la version visée. Ne déclarez GNOME 50 ou 52 qu'après avoir vérifié et testé les API correspondantes.

## 3. Feuille de style de l'acteur

Le CSS définit la géométrie visuelle de la carte. Le shader ne remplace pas le style : il traite les pixels produits par l'acteur.

### stylesheet.css

~~~css
.shader-lab-card {
  min-width: 260px;
  min-height: 140px;
  padding: 24px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.28);
  background-color: #4779b8;
  color: white;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.28);
}

.shader-lab-title {
  font-size: 18px;
  font-weight: 700;
}

.shader-lab-description {
  margin-top: 8px;
  font-size: 12px;
}
~~~

Les dimensions minimales CSS donnent une taille naturelle au widget. Le code JavaScript positionne ensuite l'acteur dans la scène.

## 4. Construire le shader de niveaux de gris

Le hook fragment intervient lors du calcul de la couleur de chaque fragment. Cogl expose des variables prédéfinies, notamment :

- `cogl_color_in` : couleur reçue par le fragment ;
- `cogl_color_out` : couleur finale à écrire.

Le shader calcule une luminance pondérée à partir des composantes RGB, puis mélange cette valeur avec la couleur initiale.

~~~glsl
vec3 luminanceWeights = vec3(0.2126, 0.7152, 0.0722);
float luminance = dot(cogl_color_in.rgb, luminanceWeights);
vec3 gray = vec3(luminance);
vec3 result = mix(cogl_color_in.rgb, gray, 0.75);

cogl_color_out = vec4(result, cogl_color_in.a);
~~~

Les coefficients donnent plus de poids au vert, conformément à une approximation courante de la luminance perceptuelle dans l'espace RGB sRGB. Ce calcul est un effet visuel simple, pas une conversion colorimétrique complète vers un espace linéaire.

L'alpha d'entrée est conservé. Remplacer systématiquement l'alpha par 1.0 rendrait opaques les pixels qui devaient rester transparents.

## 5. Extension complète : extension.js

Le code suivant utilise les API de GNOME Shell 51. Il crée un acteur St, construit le snippet, instancie l'effet et attache celui-ci à l'acteur.

~~~javascript
import { Extension } from
    'resource:///org/gnome/shell/extensions/extension.js';
import * as Main from
    'resource:///org/gnome/shell/ui/main.js';
import St from 'gi://St';
import Clutter from 'gi://Clutter';
import Cogl from 'gi://Cogl';

export default class ShaderLabExtension extends Extension {
    enable() {
        this._actor = new St.BoxLayout({
            orientation: Clutter.Orientation.VERTICAL,
            style_class: 'shader-lab-card',
        });

        const title = new St.Label({
            text: 'Shader Lab',
            style_class: 'shader-lab-title',
        });

        const description = new St.Label({
            text: 'Effet fragment : niveaux de gris',
            style_class: 'shader-lab-description',
        });

        this._actor.add_child(title);
        this._actor.add_child(description);

        this._actor.set_position(80, 140);

        this._snippet = new Cogl.Snippet(
            Cogl.SnippetHook.FRAGMENT,
            null,
            null
        );

        this._snippet.set_replace(`
            vec3 weights = vec3(0.2126, 0.7152, 0.0722);
            float luminance = dot(cogl_color_in.rgb, weights);
            vec3 gray = vec3(luminance);
            vec3 result = mix(cogl_color_in.rgb, gray, 0.75);
            cogl_color_out = vec4(result, cogl_color_in.a);
        `);

        this._effect =
            Clutter.ShaderEffect.new_with_snippet(this._snippet);

        this._actor.add_effect(this._effect);
        Main.uiGroup.add_child(this._actor);
    }

    disable() {
        if (this._actor) {
            this._actor.destroy();
            this._actor = null;
        }

        this._effect = null;
        this._snippet = null;
    }
}
~~~

Le snippet est conservé dans une propriété de l'extension afin que son cycle de vie soit explicite. L'acteur est détruit à la désactivation ; l'effet qui lui est attaché n'est alors plus utilisé. Les références JavaScript sont ensuite remises à null.

Le code est un exemple de départ destiné à une session GNOME Shell 51 de test. Il ne gère pas encore le repositionnement multi-écran, les préférences, les interactions, ni les changements de résolution.

## 6. Installer et tester dans une session de développement

Depuis le dossier qui contient le répertoire `shader-lab@example.org` :

~~~sh
UUID='shader-lab@example.org'
DEST="$HOME/.local/share/gnome-shell/extensions/$UUID"

install -d "$DEST"
cp -a "$UUID/." "$DEST/"
~~~

Vérifiez les métadonnées et la détection de l'extension :

~~~sh
gnome-extensions info shader-lab@example.org
~~~

Activez l'extension :

~~~sh
gnome-extensions enable shader-lab@example.org
~~~

Observez les journaux dans un terminal :

~~~sh
journalctl --user -b -f
~~~

Désactivez l'extension avant de modifier le code :

~~~sh
gnome-extensions disable shader-lab@example.org
~~~

Copiez ensuite les fichiers mis à jour et réactivez-la. Sous Wayland, ne comptez pas sur un redémarrage interactif du Shell comme méthode normale de développement. Utilisez une machine virtuelle ou un compte de test dont la session peut être relancée.

## 7. Variantes de shaders à expérimenter

Conservez le même squelette d'extension et ne changez que le corps du snippet. Testez une variante à la fois.

### Teinte colorée

Ce traitement mélange la couleur originale avec une teinte uniforme. Il ne nécessite pas de texture supplémentaire :

~~~glsl
vec3 tint = vec3(0.35, 0.75, 1.0);
vec3 result = mix(cogl_color_in.rgb, cogl_color_in.rgb * tint, 0.45);
cogl_color_out = vec4(result, cogl_color_in.a);
~~~

### Contraste

Ce calcul augmente ou réduit le contraste autour d'un niveau médian. Les valeurs extrêmes peuvent être écrêtées :

~~~glsl
float contrast = 1.25;
vec3 result = (cogl_color_in.rgb - 0.5) * contrast + 0.5;
result = clamp(result, 0.0, 1.0);
cogl_color_out = vec4(result, cogl_color_in.a);
~~~

### Inversion

L'inversion est utile pour vérifier rapidement le traitement des couleurs et l'alpha :

~~~glsl
vec3 result = vec3(1.0) - cogl_color_in.rgb;
cogl_color_out = vec4(result, cogl_color_in.a);
~~~

Ces fragments sont des remplacements alternatifs : ne les collez pas tous les uns à la suite des autres dans le même snippet, car chacun écrit la couleur finale.

## 8. Ajouter un uniforme dynamique

Un uniforme permet de changer une valeur sans reconstruire le code GLSL. Par exemple, une intensité de mélange peut être déclarée ainsi :

~~~glsl
uniform float intensity;

vec3 gray = vec3(dot(cogl_color_in.rgb,
                     vec3(0.2126, 0.7152, 0.0722)));
vec3 result = mix(cogl_color_in.rgb, gray, intensity);
cogl_color_out = vec4(result, cogl_color_in.a);
~~~

Le programme hôte doit fournir une valeur à l'uniforme nommé exactement `intensity`. GNOME Shell 51 expose des méthodes telles que `set_uniform_float()` et `set_uniform_value()` sur Clutter.ShaderEffect.

La méthode `set_uniform_float()` accepte un tableau de valeurs flottantes. Pour un uniforme scalaire, le tableau contient un seul élément. Vérifiez la signature introspectée par GJS dans la version ciblée avant d'intégrer cet appel à un composant complet.

Lorsqu'une valeur change, demandez un nouveau rendu de l'effet. Évitez de modifier l'uniforme en boucle à haute fréquence ; reliez son évolution à l'horloge d'image et arrêtez l'animation lorsque l'acteur n'est plus utilisé.

## 9. Comprendre le coût d'un shader

Même un shader court peut avoir un coût important si l'acteur occupe une grande surface ou si l'effet nécessite un rendu hors écran.

Le coût dépend notamment :

- du nombre de fragments traités ;
- du nombre d'échantillonnages de texture ;
- de la taille de la cible hors écran ;
- du nombre de passes ;
- de la fréquence de réaffichage ;
- du facteur d'échelle de l'écran ;
- du nombre d'acteurs utilisant simultanément l'effet.

Un shader qui ne lit qu'une couleur et effectue quelques opérations arithmétiques est généralement plus simple qu'un flou qui échantillonne de nombreux pixels voisins. Cependant, la taille de la surface et le nombre de réaffichages restent déterminants.

Ne concluez pas qu'un effet est performant à partir de sa seule longueur en lignes. Mesurez le temps d'image sur une machine représentative.

## 10. Diagnostic des erreurs courantes

### L'extension ne se charge pas

Vérifiez d'abord l'UUID, le nom du dossier, la syntaxe JavaScript et les imports :

~~~sh
gnome-extensions info shader-lab@example.org
journalctl --user -b --no-pager | grep -i -E 'shader|extension|gnome-shell'
~~~

### L'acteur apparaît sans effet

Vérifiez que le snippet est attaché au hook fragment, que le code écrit bien dans `cogl_color_out` et que le shader respecte les noms de variables Cogl. Le langage GLSL de Cogl n'est pas un shader GTK/GSK générique.

### L'acteur disparaît ou devient noir

Un shader invalide peut échouer à la compilation ou au linkage. Réduisez le fragment à une écriture de couleur simple, puis réintroduisez les calculs progressivement. Consultez les journaux de la session.

### L'extension fonctionne une fois puis échoue après réactivation

Vérifiez que `disable()` détruit l'acteur, que les connexions et les timers éventuels sont supprimés et qu'aucune référence à un acteur détruit n'est conservée.

### Le rendu est trop lent

Réduisez temporairement la taille de l'acteur. Désactivez les animations, supprimez les échantillonnages inutiles et comparez avec une version sans effet. Testez également à facteur d'échelle différent.

## 11. Aller plus loin : architecture d'un effet réutilisable

Lorsque plusieurs acteurs doivent partager le même traitement, ne dupliquez pas la construction du shader dans plusieurs fonctions. Créez un module qui centralise :

- la création du snippet ;
- les noms et types des uniformes ;
- les valeurs par défaut ;
- l'attachement et le retrait de l'effet ;
- la gestion des erreurs ;
- les paramètres propres à chaque instance.

Un effet statique peut partager le même snippet, tandis que les uniformes peuvent varier selon les instances. Si le shader dépend de textures ou de paramètres externes, documentez leur durée de vie et leur synchronisation avec le rendu.

Pour un effet animé, séparez le calcul de progression de l'écriture des uniformes. Pour un effet interactif, séparez les événements d'entrée de la logique graphique. Cette séparation rend le code testable et évite de faire du shader le lieu où toute la logique de l'extension est concentrée.

## 12. Limites à respecter

- Un shader attaché à un acteur ne floute pas les fenêtres situées derrière cet acteur.
- Un effet Clutter ne remplace pas une fonctionnalité de composition de Mutter.
- Le shader ne doit pas supposer un format colorimétrique ou une résolution fixe.
- Les variables Cogl ne sont pas interchangeables avec les variables GLSL d'un autre moteur.
- Les API internes du Shell peuvent évoluer ; testez les versions déclarées.
- Une extension qui modifie la scène du Shell doit toujours fournir un nettoyage complet.

## 13. Références GNOME 51

- [Migration des extensions vers GNOME Shell 51](https://gjs.guide/extensions/upgrading/gnome-shell-51.html)
- [Clutter.ShaderEffect — API 51](https://mutter.gnome.org/clutter/class.ShaderEffect.html)
- [Clutter.ShaderEffect.new_with_snippet — API 51](https://mutter.gnome.org/clutter/ctor.ShaderEffect.new_with_snippet.html)
- [Cogl.Snippet — API 51](https://mutter.gnome.org/cogl/class.Snippet.html)
- [Cogl.Snippet.new — API 51](https://mutter.gnome.org/cogl/ctor.Snippet.new.html)
- [Clutter.Effect — API 51](https://mutter.gnome.org/clutter/class.Effect.html)

Les pages de référence sont versionnées. Vérifiez toujours que la page consultée indique l'API 51 et confrontez les signatures GJS aux introspections livrées avec GNOME 51.
