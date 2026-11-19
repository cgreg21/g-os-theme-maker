# 54. Atelier avancé : verre dépoli, distorsion et rendu CRT

Ce chapitre transforme les mécanismes des chapitres 52 et 53 en effets visuels concrets. Il distingue le flou de l'arrière-plan, le flou du contenu d'un acteur et les traitements GLSL appliqués à une texture. Les exemples ciblent GNOME Shell 51 et doivent être testés dans une session de développement isolée.

Un principe guide tout l'atelier : choisir l'API la plus simple qui produit réellement l'effet attendu. Un shader attaché à une carte ne peut pas prélever les pixels des fenêtres placées derrière elle. Pour un panneau en verre dépoli, il faut un effet de flou d'arrière-plan fourni par GNOME Shell ou une capacité du compositeur.

## 1. Choisir le bon type de flou

GNOME 51 expose plusieurs mécanismes qui portent le même nom mais n'ont pas la même portée.

### Shell.BlurEffect

`Shell.BlurEffect` est l'outil adapté aux extensions GNOME Shell qui veulent flouter une zone du bureau située derrière un acteur. Son mode `BACKGROUND` traite les pixels sous l'acteur sans flouter l'acteur lui-même. Le mode `ACTOR` floute l'acteur et ses enfants.

L'effet expose notamment les propriétés `mode`, `radius` et `brightness`. Il s'attache à un acteur Clutter avec `add_effect()` ou `add_effect_with_name()`.

Le mode d'arrière-plan est coûteux : le contenu situé dessous ne peut pas être mis en cache de la même manière que le contenu d'un acteur statique. Évitez de multiplier les zones floutées, de leur donner une surface excessive ou de les animer sans nécessité.

### Clutter.BlurEffect

`Clutter.BlurEffect` floute l'acteur auquel il est attaché ainsi que son contenu. Il ne prélève pas le bureau situé derrière cet acteur. Il est pertinent pour flouter une image, une vignette ou un composant déjà rendu.

### Clutter.ShaderEffect

`Clutter.ShaderEffect` traite le rendu hors écran d'un acteur avec un shader GLSL. Il convient aux déformations, corrections colorimétriques et motifs procéduraux. Il ne donne pas automatiquement accès aux fenêtres voisines.

### CSS et transparence

Une couleur de fond avec alpha peut laisser apparaître les éléments situés derrière un widget, mais elle ne les floute pas. Une transparence CSS seule ne constitue donc pas un effet de verre dépoli.

## 2. Construire une carte en verre dépoli

L'exemple suivant crée un acteur indépendant dans le Shell. Il applique un flou d'arrière-plan, puis laisse le CSS ajouter une teinte translucide, une bordure et des arrondis.

### Feuille de style

```css
.frosted-card {
  min-width: 320px;
  min-height: 150px;
  padding: 22px;
  border-radius: 22px;
  border: 1px solid rgba(255, 255, 255, 0.24);
  background-color: rgba(24, 31, 43, 0.42);
  color: rgba(255, 255, 255, 0.96);
}

.frosted-card-title {
  font-size: 18px;
  font-weight: 700;
}

.frosted-card-description {
  margin-top: 8px;
  color: rgba(255, 255, 255, 0.78);
  font-size: 12px;
}
```

Le fond doit rester translucide pour que le résultat du flou soit visible. Une couleur opaque masquerait complètement l'arrière-plan, même si l'effet continue à travailler.

### Extension GNOME Shell 51

Le fichier `extension.js` :

```javascript
import { Extension } from
    'resource:///org/gnome/shell/extensions/extension.js';
import * as Main from
    'resource:///org/gnome/shell/ui/main.js';
import St from 'gi://St';
import Clutter from 'gi://Clutter';
import Shell from 'gi://Shell';

export default class FrostedCardExtension extends Extension {
    enable() {
        this._card = new St.BoxLayout({
            orientation: Clutter.Orientation.VERTICAL,
            style_class: 'frosted-card',
        });

        this._card.add_child(new St.Label({
            text: 'Verre dépoli',
            style_class: 'frosted-card-title',
        }));

        this._card.add_child(new St.Label({
            text: 'Flou de l’arrière-plan et teinte translucide',
            style_class: 'frosted-card-description',
        }));

        this._card.set_position(80, 140);

        this._blur = new Shell.BlurEffect({
            mode: Shell.BlurMode.BACKGROUND,
            radius: 18,
            brightness: 0.82,
        });

        this._card.add_effect_with_name('frosted-background', this._blur);
        Main.uiGroup.add_child(this._card);
    }

    disable() {
        if (this._card) {
            this._card.destroy();
            this._card = null;
        }

        this._blur = null;
    }
}
```

Le nom du dossier d'extension doit correspondre à l'UUID de ses métadonnées. Ajoutez une feuille de style chargée par le mécanisme normal de l'extension et déclarez uniquement GNOME Shell 51 dans `shell-version` tant que les autres versions n'ont pas été testées.

Le code illustre le cycle de vie minimal. Une extension destinée à être distribuée doit aussi traiter le repositionnement selon les écrans, la géométrie disponible, les changements de session et les éventuelles erreurs de création de l'effet.

### Ajuster le rendu

Commencez avec un rayon modéré et une luminosité proche de 1. Modifiez ensuite une seule propriété à la fois.

- Augmenter `radius` élargit la zone de mélange et peut augmenter le coût.
- Diminuer `brightness` assombrit le résultat flouté ; la teinte CSS reste un réglage distinct.
- Le mode `BACKGROUND` convient au verre dépoli ; le mode `ACTOR` ne floute que l'acteur et ses enfants.
- Une bordure claire très fine aide à détacher le panneau du fond sans rendre son remplissage opaque.

Ne supposez pas qu'un rayon numérique correspond à la même perception sur tous les écrans. Vérifiez les facteurs d'échelle et la taille physique des zones concernées.

## 3. Flouter le contenu d'un acteur

Pour flouter un contenu qui appartient déjà à l'acteur, utilisez `Clutter.BlurEffect` plutôt que le mode d'arrière-plan de `Shell.BlurEffect`.

Exemple conceptuel d'attachement :

```javascript
import Clutter from 'gi://Clutter';

const effect = new Clutter.BlurEffect();
actor.add_effect_with_name('content-blur', effect);
```

L'effet natif de Clutter est un `Clutter.OffscreenEffect`. Le contenu de l'acteur est rendu dans une cible intermédiaire, puis flouté. Il ne s'agit pas d'un flou des fenêtres voisines.

La classe ne propose pas, dans son API 51 documentée, le même ensemble de paramètres publics que `Shell.BlurEffect`. N'inventez pas de propriété `radius` pour cet objet. Si le réglage du rayon est une exigence, vérifiez les possibilités de la version réellement installée ou implémentez un traitement contrôlé avec un shader.

## 4. Déformation de texture : principe du déplacement UV

Une déformation de type vague, ondulation ou lentille déplace les coordonnées de lecture d'une texture. Le shader ne déplace pas directement les fenêtres du bureau : il modifie la façon dont la texture de l'acteur est échantillonnée.

Cogl propose le hook `TEXTURE_LOOKUP`. À cet endroit, le snippet peut utiliser les coordonnées de texture et lire la texture à une position légèrement décalée. Les noms `cogl_sampler`, `cogl_tex_coord` et `cogl_texel` appartiennent à ce pipeline Cogl ; ils ne doivent pas être copiés dans un shader GTK/GSK.

### Exemple de vague statique

Ce fragment est le corps d'un snippet Cogl attaché au hook de recherche de texture :

```glsl
vec2 uv = cogl_tex_coord.st;
uv.x += sin(uv.y * 18.0) * 0.006;
cogl_texel = texture2D(cogl_sampler, uv);
```

La fréquence et l'amplitude contrôlent la forme de l'ondulation. Une amplitude trop forte peut faire apparaître des zones non couvertes sur les bords. Gardez la déformation modeste et vérifiez les limites de texture.

### Raccorder le hook au pipeline Cogl

Attention : un snippet `TEXTURE_LOOKUP` ne se raccorde pas comme un snippet `FRAGMENT`. Le premier est propre à une couche de texture et doit être ajouté avec `Cogl.Pipeline.add_layer_snippet()` (couche 0 dans cet exemple). `Clutter.ShaderEffect.new_with_snippet()` est illustré au chapitre 53 pour les traitements `FRAGMENT` ; ne lui passez pas ce snippet de recherche de texture en supposant qu'il sera automatiquement attaché à une couche.

L'assemblage bas niveau du pipeline suit ce principe :

```c
CoglSnippet *snippet =
    cogl_snippet_new (COGL_SNIPPET_HOOK_TEXTURE_LOOKUP, NULL, NULL);

cogl_snippet_set_replace (snippet,
    "vec2 uv = cogl_tex_coord.st; "
    "uv.x += sin(uv.y * 18.0) * 0.006; "
    "cogl_texel = texture2D(cogl_sampler, uv);");

cogl_pipeline_add_layer_snippet (pipeline, 0, snippet);
g_object_unref (snippet);
```

Ce fragment C montre uniquement la création et l'attachement du snippet à un pipeline Cogl déjà configuré avec une couche de texture. Il ne constitue pas à lui seul un effet d'acteur GNOME Shell. Pour l'utiliser sur le contenu d'un acteur, il faut intégrer ce pipeline dans un effet hors écran Clutter adapté (ou une implémentation native de `Clutter.OffscreenEffect`) et gérer la cible, la couche, le rendu et les uniformes. Cette intégration avancée n'est pas fournie ici sous la forme d'une extension GJS complète : mieux vaut ne pas présenter un `Clutter.ShaderEffect` générique comme un raccordement valide de ce hook spécialisé.

## 5. Vignettage, lignes de balayage et aberration chromatique

Les traitements suivants sont des variantes de post-traitement. Ils s'appliquent à une texture fournie au shader, pas au bureau complet. Les fragments utilisant `cogl_sampler`, `cogl_tex_coord` et `cogl_texel` ciblent le hook `TEXTURE_LOOKUP` d'une couche Cogl ; ils nécessitent donc le raccordement par `Cogl.Pipeline.add_layer_snippet()` décrit à la section précédente et un effet hors écran qui utilise ce pipeline. Ils ne peuvent pas être collés tels quels dans l'exemple `Clutter.ShaderEffect` du chapitre 53.

### Vignettage

Le vignettage assombrit progressivement les bords. Il utilise la distance entre les coordonnées UV et le centre de la texture.

```glsl
vec2 centered = cogl_tex_coord.st - vec2(0.5);
float distanceFromCenter = length(centered);
float edge = smoothstep(0.32, 0.72, distanceFromCenter);
vec4 sampleColor = texture2D(cogl_sampler, cogl_tex_coord.st);
sampleColor.rgb *= 1.0 - edge * 0.42;
cogl_texel = sampleColor;
```

La transition doit rester progressive. Un seuil trop brutal produit un cercle visible plutôt qu'un assombrissement naturel.

### Lignes de balayage CRT

Les lignes de balayage simulent la modulation périodique d'un écran cathodique. Un motif simple peut être calculé à partir de la coordonnée verticale en pixels ou de la coordonnée de texture.

```glsl
vec2 uv = cogl_tex_coord.st;
vec4 sampleColor = texture2D(cogl_sampler, uv);
float scanline = 0.94 + 0.06 * sin(uv.y * 900.0);
sampleColor.rgb *= scanline;
cogl_texel = sampleColor;
```

La fréquence `900.0` est illustrative. Elle dépend de la taille de la texture et de son échelle. Un motif trop fin peut scintiller, se moirer ou disparaître après redimensionnement.

### Aberration chromatique

Une aberration chromatique sépare légèrement les lectures des canaux rouge et bleu. Elle nécessite plusieurs échantillonnages :

```glsl
vec2 uv = cogl_tex_coord.st;
float shift = 0.002;
vec4 center = texture2D(cogl_sampler, uv);
float red = texture2D(cogl_sampler, uv + vec2(shift, 0.0)).r;
float blue = texture2D(cogl_sampler, uv - vec2(shift, 0.0)).b;
cogl_texel = vec4(red, center.g, blue, center.a);
```

Le décalage doit rester faible. Il augmente le nombre de lectures de texture et peut produire des franges excessives sur les textes et les icônes. Conservez l'alpha de l'échantillon central.

### Combiner les traitements

Il est possible de combiner plusieurs opérations dans un seul snippet afin d'éviter de multiplier les effets hors écran. Cette fusion complique toutefois le réglage et le diagnostic. Développez chaque opération séparément, validez-la, puis combinez-les seulement après avoir établi un résultat de référence.

Les snippets de cette section décrivent le calcul et les variables du pipeline Cogl. Ils doivent être intégrés à un effet complet, puis compilés et testés sur GNOME Shell 51. Ils ne sont pas des shaders autonomes universels.

## 6. Distorsion de type CRT et bruit

Un rendu CRT plus complet peut combiner plusieurs éléments :

- lignes de balayage ;
- séparation légère des canaux RVB ;
- vignettage ;
- courbure de l'image ;
- bruit fin et discret ;
- variation très faible de luminosité.

La courbure est une déformation radiale des coordonnées UV. Elle peut être ajoutée au déplacement de texture en calculant un vecteur depuis le centre, puis en augmentant légèrement sa longueur en fonction de son carré.

```glsl
vec2 centered = cogl_tex_coord.st - vec2(0.5);
float r2 = dot(centered, centered);
vec2 curvedUV = vec2(0.5) + centered * (1.0 + 0.12 * r2);
cogl_texel = texture2D(cogl_sampler, curvedUV);
```

Cette formule est une approximation géométrique. Elle ne crée pas les coins noirs ni le masque arrondi d'un tube cathodique. Il faut prévoir un masque ou un traitement des coordonnées hors limites si ces éléments font partie du résultat attendu.

Le bruit temporel animé demande une source de temps et une mise à jour contrôlée. Ne créez pas une boucle permanente qui réveille le Shell à chaque intervalle arbitraire. Utilisez un mécanisme d'animation adapté à l'horloge d'image, arrêtez-le lorsque l'effet n'est plus visible et nettoyez systématiquement sa source à la désactivation.

## 7. Qualité d'image et limites

### Échantillonnage et bords

Une déformation peut demander des coordonnées en dehors de la texture. Selon le pipeline et le mode de filtrage, cela peut produire des bords transparents, des répétitions ou des couleurs inattendues. Vérifiez le comportement réel et choisissez explicitement une stratégie : limiter les coordonnées, agrandir la zone de rendu ou masquer les bords.

### Alpha et couleurs

Préservez l'alpha de l'échantillon lorsque l'effet ne doit pas modifier la transparence. Respectez la convention de prémultiplication des couleurs utilisée par le pipeline. Une mauvaise convention provoque des halos autour des zones transparentes, surtout après un flou ou un mélange de canaux.

### Échelle et fréquence des motifs

Les lignes de balayage, le bruit et les petits décalages UV sont sensibles à la taille de la cible hors écran. Testez au minimum plusieurs facteurs d'échelle, des tailles de fenêtres différentes et des changements de résolution.

### Accessibilité

Un effet décoratif ne doit pas réduire la lisibilité. Évitez les scintillements rapides, les clignotements, les contrastes agressifs et les mouvements continus inutiles. Prévoyez un moyen de désactiver les effets animés et conservez une présentation lisible sans eux.

## 8. Mesurer le coût GPU

Mesurez chaque étape séparément :

1. Rendu de référence sans effet.
2. Ajout du flou d'arrière-plan sur une petite surface.
3. Augmentation progressive de la surface floutée.
4. Ajout d'un seul échantillonnage de texture.
5. Ajout des échantillonnages supplémentaires.
6. Activation du mouvement ou du bruit animé.
7. Répétition sur un GPU intégré et à plusieurs facteurs d'échelle.

Le coût d'un effet dépend de la surface réellement traitée, du nombre de passes, des lectures de texture et de la fréquence de réaffichage. Un shader court qui lit plusieurs textures à chaque fragment peut coûter davantage qu'un shader plus long qui effectue quelques opérations arithmétiques.

Pour le flou d'arrière-plan, gardez en tête la limite particulière de `Shell.BlurEffect` : le contenu derrière l'acteur ne peut pas être mis en cache comme un contenu statique. Limitez donc le nombre et la surface des zones en mode `BACKGROUND`.

## 9. Nettoyage et diagnostic

Retirez les effets avec leur acteur propriétaire. Ne laissez pas d'acteur de démonstration dans `Main.uiGroup` après la désactivation.

Pour un effet attaché à un acteur qui doit rester en place, retirez-le explicitement :

```javascript
const effect = actor.get_effect('wave-distortion');
if (effect)
    actor.remove_effect(effect);
```

En cas de rendu noir ou absent :

- vérifiez le hook Cogl utilisé ;
- réduisez le snippet à une lecture de texture sans déformation ;
- réintroduisez une seule opération à la fois ;
- vérifiez les noms des variables Cogl ;
- consultez les journaux de la session ;
- testez avec un acteur de petite taille et une texture simple.

Commandes de diagnostic :

```sh
gnome-extensions info shader-lab@example.org
journalctl --user -b --no-pager | grep -i -E 'gnome-shell|shader|cogl|clutter'
```

Une erreur GLSL n'est pas une erreur CSS. Le fait que la feuille de style soit chargée ne prouve pas que le shader compile ou que le hook est compatible.

## 10. Compatibilité et frontières d'API

- `Shell.BlurEffect` est une API du Shell et non une propriété CSS publique et stable.
- `Clutter.BlurEffect` traite l'acteur lui-même, pas son arrière-plan.
- `Clutter.ShaderEffect` utilise un rendu hors écran et un snippet Cogl.
- `Cogl.SnippetHook.TEXTURE_LOOKUP` et `FRAGMENT` ne sont pas interchangeables.
- Un shader Cogl n'est pas un shader GSK.
- Un acteur du Shell n'a pas le droit de lire arbitrairement les pixels des autres fenêtres par simple accès JavaScript.
- Les effets de fond fournis par le compositeur et les protocoles Wayland ont leurs propres conditions de prise en charge.

Les noms de classes et propriétés doivent être vérifiés dans l'API GNOME 51 ciblée. Une extension qui annonce plusieurs versions doit adapter ses imports et ses effets à chaque version, puis les tester séparément.

## 11. Références GNOME 51

- [Shell.BlurEffect — API GNOME Shell 51](https://gnome.pages.gitlab.gnome.org/gnome-shell/shell/class.BlurEffect.html)
- [Clutter.BlurEffect — API Mutter 51](https://mutter.gnome.org/clutter/class.BlurEffect.html)
- [Clutter.ShaderEffect — API Mutter 51](https://mutter.gnome.org/clutter/class.ShaderEffect.html)
- [Clutter.ShaderEffect.set_uniform_float — API Mutter 51](https://gnome.pages.gitlab.gnome.org/mutter/clutter/method.ShaderEffect.set_uniform_float.html)
- [Cogl.Snippet — API Mutter 51](https://mutter.gnome.org/cogl/class.Snippet.html)
- [Cogl.SnippetHook — API Mutter 51](https://mutter.gnome.org/cogl/enum.SnippetHook.html)
- [Migration des extensions vers GNOME Shell 51](https://gjs.guide/extensions/upgrading/gnome-shell-51.html)

La documentation Shell et Mutter est versionnée. Vérifiez la version affichée par les pages et les signatures réellement introspectées sur la session GNOME 51 cible.
