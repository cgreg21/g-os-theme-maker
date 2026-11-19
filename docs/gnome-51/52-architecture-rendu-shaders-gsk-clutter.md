# 52. Architecture de rendu avancée : GSK, Clutter, shaders et GPU

Ce chapitre approfondit les mécanismes qui se trouvent derrière les effets visuels. Il s'adresse aux personnes qui développent un composant GTK personnalisé, une extension GNOME Shell ou un moteur d'effets. Il complète le chapitre 51 : celui-ci présente les effets disponibles ; celui-ci explique comment les images sont construites, transformées, mises en cache et composées.

Les exemples visent GNOME 51, GTK 4.23 et Mutter 51. Une API documentée dans une version plus récente ne doit pas être considérée comme disponible dans GNOME 51 sans vérification dans les sources et les introspections de cette version.

## 1. Trois pipelines graphiques distincts

GNOME n'utilise pas un moteur de rendu unique pour toutes ses interfaces.

### GTK et GSK

GTK construit l'interface à partir d'un arbre de widgets. Lors du rendu, chaque widget contribue à un instantané (GtkSnapshot). Cet instantané produit un arbre de nœuds de rendu GSK (GskRenderNode). Le renderer GSK transforme ensuite cet arbre en opérations adaptées au backend choisi, par exemple OpenGL, Vulkan ou Cairo.

Ce modèle est conservé : GTK peut réutiliser des nœuds déjà construits au lieu de redessiner tout le contenu à chaque image. Lorsqu'un widget invalide son rendu, les nœuds concernés doivent être reconstruits.

### GNOME Shell, St, Clutter et Cogl

GNOME Shell construit ses composants avec St, qui fournit les widgets et le CSS du Shell, et Clutter, qui gère la scène, les acteurs, les transformations, les animations et les effets. Cogl fournit les abstractions de pipeline graphique utilisées par Clutter.

Une règle CSS St peut modifier l'apparence d'un acteur, mais elle ne remplace pas un effet Clutter ni un shader. Les effets personnalisés s'attachent à un acteur par le code de l'extension.

### Mutter et la composition des surfaces

Mutter est le compositeur et gestionnaire de fenêtres de GNOME. Il assemble les surfaces des applications, les éléments du Shell et les autres couches de la session pour produire l'image affichée. Il gère également les protocoles Wayland et les ressources de composition.

Une application Wayland ne peut pas lire librement les pixels des autres fenêtres. Un flou qui prélève l'arrière-plan doit donc être fourni par le compositeur ou par un protocole prévu à cet effet. Un widget GTK ne peut pas obtenir ce résultat en dessinant simplement une règle CSS.

## 2. Le modèle de rendu GTK 4 : snapshot et GSK

GTK 4 n'utilise plus l'ancien modèle GTK 3 fondé sur le signal draw comme point d'entrée du dessin des widgets. Le rendu personnalisé passe par la méthode virtuelle Gtk.Widget.snapshot.

Le flux simplifié est :

1. GTK calcule la disposition et la taille des widgets.
2. Le widget reçoit un GtkSnapshot.
3. Il ajoute son fond, ses bordures, son contenu et ses enfants.
4. Le snapshot produit un ou plusieurs GskRenderNode.
5. Le renderer GSK convertit les nœuds en opérations graphiques.
6. Le contenu est associé à la surface de la fenêtre, puis composé par le système graphique.

Un snapshot est une description de ce qu'il faut dessiner, pas une image bitmap immédiatement rendue. Il maintient une pile de nœuds et de transformations. Les appels push ouvrent un contexte de rendu ; pop le ferme.

### Familles de nœuds et opérations

Les nœuds GSK représentent des opérations graphiques explicites. Les familles importantes comprennent :

- couleur unie, texture, texte, chemin et dégradé ;
- transformation, perspective, découpage rectangulaire ou arrondi ;
- opacité, ombre portée, ombre interne et flou ;
- matrice de couleur et transfert de composantes ;
- masque, composition et modes de fusion ;
- isolation et copie temporaire du contenu.

La présence d'un type de nœud GSK ne signifie pas que chaque fonction est exposée sous forme de propriété CSS. Plusieurs opérations sont accessibles uniquement au code qui construit un snapshot.

### Exemple conceptuel en C

Le code suivant illustre l'encadrement d'un rendu par une opération de flou. Il s'agit d'un extrait de méthode snapshot, pas d'un widget complet :

~~~c
static void
my_widget_snapshot (GtkWidget *widget,
                    GtkSnapshot *snapshot)
{
  graphene_rect_t bounds;

  graphene_rect_init (&bounds, 0, 0,
                      gtk_widget_get_width (widget),
                      gtk_widget_get_height (widget));

  gtk_snapshot_push_blur (snapshot, 4.0);

  /* Ajouter ici le contenu que le flou doit affecter. */
  gtk_snapshot_append_color (snapshot, &some_color, &bounds);

  gtk_snapshot_pop (snapshot);
}
~~~

L'opération agit sur le contenu ajouté dans la portée du snapshot. Elle ne floute pas les autres fenêtres ni l'arrière-plan du bureau. Le widget réel doit également gérer ses enfants, ses dimensions, son accessibilité et l'invalidation du rendu.

### Pourquoi le snapshot est utile

Le modèle permet de décrire le rendu sous forme d'un graphe que GSK peut optimiser. Un widget peut déléguer le rendu de ses enfants avec gtk_widget_snapshot_child(). Il ne doit pas redessiner arbitrairement les enfants lui-même ni modifier le snapshot reçu en dehors de sa portée.

Lorsqu'un état visuel change, le widget demande un nouveau rendu avec gtk_widget_queue_draw(). Les changements de taille ou de disposition relèvent des mécanismes de mesure et de disposition, pas uniquement de l'invalidation du dessin.

## 3. Render nodes, cache et invalidation

Un arbre de rendu peut être conservé et réutilisé. Cette conservation évite de reconstruire le contenu d'un widget si son rendu n'a pas changé.

Il faut distinguer trois choses :

- **cache des nœuds** : conserve la description du rendu ;
- **cache de textures ou surfaces** : conserve des pixels déjà produits ;
- **cache du compositeur** : conserve des ressources utilisées lors de la composition des surfaces.

Ces caches n'ont ni la même durée de vie ni les mêmes règles d'invalidation.

Un widget qui change une propriété visuelle doit demander un nouveau rendu. Un widget qui change sa géométrie doit également provoquer les mises à jour de disposition nécessaires. Un cache personnalisé doit être invalidé lorsque changent les données, les dimensions, le facteur d'échelle, le profil colorimétrique ou les paramètres du shader dont il dépend.

Ne créez pas un cache de texture pour chaque image sans mesurer son intérêt. Les textures consomment de la mémoire GPU et leur multiplication peut réduire les performances au lieu de les améliorer.

## 4. Effets de composition et portée des opérations

Les opérations de rendu ont une portée. Un flou appliqué à un groupe affecte le résultat du groupe, alors qu'un flou appliqué à un enfant affecte uniquement cet enfant. Une opération d'opacité placée au niveau parent peut composer les enfants ensemble avant d'appliquer l'opacité ; appliquée séparément à chaque enfant, elle peut produire un résultat différent aux zones de chevauchement.

Quelques principes :

- **clip** : limite la zone visible, sans nécessairement modifier la géométrie de l'objet ;
- **opacity** : mélange le contenu avec ce qui se trouve derrière ;
- **mask** : utilise une image ou une forme comme masque de visibilité ;
- **blend/composite** : combine plusieurs contenus selon une règle ;
- **color matrix** : transforme les composantes colorées ;
- **isolation** : sépare une portion de la scène pour contrôler les interactions de composition ;
- **shadow** : produit une ombre à partir d'une forme ou du contenu rendu.

L'ordre de ces opérations change le résultat. Flouter puis découper n'est pas équivalent à découper puis flouter : dans le second cas, les bords du contenu disponible peuvent produire un halo ou une coupure.

Lorsqu'un effet déborde de sa géométrie initiale, vérifiez les limites de rendu, les clips des parents et les zones invalidées. Un effet peut être correctement calculé mais coupé par un conteneur.

## 5. Shaders : du fragment au pixel

Un shader est un programme exécuté par le pipeline graphique. Dans les effets d'interface décrits ici, le shader de fragment calcule la couleur produite pour chaque fragment de la surface rendue.

Il peut notamment :
- appliquer une teinte ou une correction colorimétrique ;
- produire un dégradé procédural ;
- déformer des coordonnées de texture ;
- simuler des lignes de balayage, du bruit ou une aberration chromatique ;
- mélanger plusieurs textures ;
- calculer un masque ou une transition visuelle.

Un shader ne donne pas automatiquement accès à tout le bureau. Il travaille sur les entrées qui lui sont fournies : texture de l'acteur, coordonnées, uniformes et éventuellement textures supplémentaires.

### Concepts GLSL essentiels

- **uniform** : valeur transmise par le programme hôte, par exemple intensité, temps ou couleur ;
- **varying / entrée interpolée** : donnée interpolée entre les sommets, selon l'interface shader utilisée ;
- **coordonnées UV** : coordonnées normalisées servant à échantillonner une texture ;
- **sampler** : entrée permettant de lire une texture ;
- **fragment** : échantillon de la surface traité par le shader ;
- **alpha** : composante de transparence, dont la convention de prémultiplication doit être respectée ;
- **pipeline** : ensemble des étapes et états nécessaires à la production du rendu.

Les exemples GLSL ne sont pas universellement interchangeables : les noms des variables d'entrée et de sortie dépendent de l'API qui injecte le shader. Un fragment destiné à Cogl n'est pas nécessairement un shader GSK ni un shader GTK.

### Exemple de transformation colorimétrique

Voici une formule GLSL générique pour mélanger une couleur avec une teinte. Elle décrit le calcul, mais ne constitue pas à elle seule un shader GNOME prêt à compiler :

~~~glsl
vec3 tinted = mix(
    original.rgb,
    original.rgb * tint.rgb,
    clamp(amount, 0.0, 1.0)
);
~~~

Le programme hôte doit fournir original, tint et amount avec des types et des noms cohérents avec le shader complet. Il doit également préserver correctement l'alpha.

## 6. Shaders dans GNOME Shell 51 : Clutter.ShaderEffect

Dans GNOME Shell 51, l'ancienne classe Shell.GLSLEffect a été supprimée. Les extensions qui implémentaient cet ancien mécanisme doivent migrer vers Clutter.ShaderEffect.

Clutter.ShaderEffect dérive de Clutter.OffscreenEffect. L'acteur est d'abord rendu dans une cible hors écran, puis le shader GLSL traite cette texture avant son affichage. Cette étape intermédiaire est utile pour les effets de post-traitement, mais elle a un coût en mémoire et en bande passante.

L'API documente notamment :
- new_with_snippet pour créer un effet à partir d'un snippet Cogl ;
- get_static_snippet pour fournir le snippet utilisé par la classe ;
- set_uniform, set_uniform_float et set_uniform_value pour transmettre les paramètres ;
- paint_target dans le cycle de l'effet hors écran ;
- clutter_actor_add_effect() pour attacher un effet à un acteur.

### Organisation conceptuelle

Un effet personnalisé suit généralement cette organisation :

1. Définir le code GLSL et les uniformes nécessaires.
2. Construire un Cogl.Snippet pour le point d'insertion approprié.
3. Créer une classe d'effet basée sur Clutter.ShaderEffect.
4. Fournir le snippet statique.
5. Mettre à jour les uniformes avant le rendu.
6. Attacher l'effet à un acteur dont l'extension contrôle le cycle de vie.
7. Retirer l'effet et libérer les références lorsque l'extension est désactivée.

Le point d'insertion du snippet détermine à quel endroit du pipeline Cogl le code est exécuté. Le hook fragment est adapté à un traitement de couleur final ; il n'est pas équivalent à un shader de sommet ou à un traitement de géométrie.

### Exemple d'assemblage du snippet

Extrait illustratif de l'API Cogl/Clutter, à intégrer dans une sous-classe d'effet et non à exécuter isolément :

~~~js
const snippet = new Cogl.Snippet(
    Cogl.SnippetHook.FRAGMENT,
    'uniform vec3 component;',
    null
);

snippet.set_replace(
    'cogl_color_out = vec4(component, 1.0);'
);
~~~

L'exemple remplace la couleur de sortie par une couleur uniforme. Il sert à illustrer le point d'insertion et la transmission d'une valeur, pas à fournir un effet complet : la sous-classe doit retourner ce snippet via son mécanisme de classe, gérer les uniformes au bon moment et respecter le cycle de vie de l'acteur.

Pour un effet de teinte qui conserve l'image d'origine, le code GLSL doit utiliser la couleur d'entrée fournie par le pipeline et préserver l'alpha au lieu de remplacer toute la sortie par une couleur opaque. Consultez l'exemple officiel de Clutter.ShaderEffect pour les variables de pipeline exactes.

### Règles de migration GNOME 51

- Ne partez pas d'un ancien exemple utilisant Shell.GLSLEffect.
- Utilisez Clutter.ShaderEffect et Cogl.Snippet.
- Ne supposez pas que vfunc_build_pipeline() existe encore : le modèle documenté utilise vfunc_get_static_snippet().
- Testez la compilation du shader et le cas d'échec.
- N'attachez pas un effet à un acteur appartenant à un autre composant sans maîtriser son cycle de vie.
- Supprimez l'effet à la désactivation de l'extension et évitez les références persistantes vers des acteurs détruits.

## 7. GTK et GSK : ne pas réutiliser les anciens exemples de shaders OpenGL

GTK fournit des nœuds GSK et des opérations de snapshot pour construire les effets de widgets. Il est tentant de créer un shader personnalisé avec Gtk.Snapshot.push_gl_shader(). Cette voie est dépréciée depuis GTK 4.16 et n'est pas adaptée au renderer Vulkan de GTK.

Pour GTK 4.23, privilégiez les opérations de snapshot prises en charge : flou, masque, opacité, ombre, composition, matrice de couleur, isolation et transformations. Si un shader personnalisé est réellement nécessaire, étudiez les API de rendu prévues par la version exacte de GTK et les contraintes du renderer ciblé. Ne bâtissez pas une fonctionnalité de production sur l'ancien chemin GL déprécié.

Pour une interface GTK, un widget personnalisé peut construire son rendu dans snapshot() et produire des nœuds GSK. Ce mécanisme reste distinct de Clutter.ShaderEffect : il ne faut pas copier un snippet Cogl dans une API GSK.

## 8. Rendu hors écran, mémoire et coût des effets

Les effets de post-traitement demandent souvent une texture temporaire. Une surface RGBA non compressée consomme approximativement :

**largeur × hauteur × 4 octets**

Le facteur d'échelle multiplie les deux dimensions. À titre d'ordre de grandeur, une surface logique de 1440 × 900 à l'échelle 2 produit une cible de 2880 × 1800 pixels, soit environ 20,7 Mo pour une seule image RGBA de 8 bits par canal, avant alignement, allocations internes et copies éventuelles.

Si l'effet demande plusieurs cibles intermédiaires, la mémoire augmente en conséquence. Les formats 10 bits, les buffers supplémentaires et les textures de travail modifient ce calcul.

### Flou et passes de rendu

Un flou gaussien naïf peut nécessiter beaucoup d'échantillonnages. Une optimisation courante consiste à séparer le calcul horizontal et vertical en deux passes, parfois à réduire la résolution de la texture avant le flou puis à la réagrandir.

Cette technique diminue le coût, mais peut introduire :
- perte de détail ;
- halos sur les contours ;
- scintillement lors du déplacement ;
- différences de rendu selon l'échelle ;
- imprécision des petits textes et icônes.

Le rayon exprimé en pixels physiques ne correspond pas nécessairement au même rayon visuel sur tous les écrans. Tenez compte du facteur d'échelle et de la résolution réelle de la cible hors écran.

## 9. Alpha, prémultiplication et composition

Les pipelines graphiques utilisent souvent des couleurs avec alpha prémultiplié : les composantes RGB ont déjà été multipliées par alpha. Cette convention permet une composition efficace, mais elle doit être cohérente sur tout le trajet de l'image.

Une erreur de convention peut provoquer :
- des franges sombres ou claires autour des éléments transparents ;
- des halos sur les textures ;
- des bordures incorrectes après un flou ;
- des résultats différents selon le chemin de composition.

Ne multipliez pas deux fois les composantes RGB par alpha. Ne supposez pas non plus qu'une texture PNG, un buffer de shader et une sortie de pipeline utilisent la même convention sans vérifier leur contrat.

Le mélange alpha classique combine la couleur du premier plan et celle de l'arrière-plan pondérées par leur opacité. Les modes de fusion et les espaces colorimétriques peuvent modifier le résultat.

## 10. Espaces colorimétriques, profondeur et HDR

Un effet qui modifie les couleurs doit tenir compte de l'espace dans lequel les calculs sont effectués. Les valeurs RGB affichées ne sont pas toujours des intensités lumineuses linéaires. Une opération de flou, de mélange ou de luminosité peut donc donner un résultat différent selon que le calcul est fait dans un espace linéaire ou encodé.

GNOME 51 apporte notamment la prise en charge de formats d'image 10 bits dans le renderer GSK. Cela ne signifie pas que chaque écran, pilote, surface et application travaille automatiquement en HDR. La chaîne complète doit prendre en charge le format, le profil, le compositeur et le périphérique.

Pour un thème, évitez de coder des couleurs en supposant qu'elles seront identiques sur tous les écrans. Vérifiez les profils, les écrans à large gamut, les modes HDR éventuels et le rendu des transparences.

## 11. Fractional scaling et géométrie des pixels

Les coordonnées de GTK sont généralement exprimées en unités logiques. Le renderer doit les convertir en pixels physiques. Avec un facteur entier, l'alignement est relativement simple ; avec une échelle fractionnaire, une coordonnée logique peut tomber entre deux pixels physiques.

GNOME 51 améliore l'alignement sur les frontières de pixels physiques pour le rendu à échelle fractionnaire. Cela ne dispense pas les widgets et les effets personnalisés de vérifier :
- les lignes fines et bordures d'un pixel logique ;
- les textures et leurs filtres d'échantillonnage ;
- les ombres et leur rayon ;
- les limites de clipping ;
- les arrondis des rectangles et transformations.

Évitez les calculs qui supposent que multiplier une coordonnée par un facteur d'échelle donne toujours un entier. Testez au minimum 100 %, 125 %, 150 % et 200 % si ces facteurs sont proposés par l'environnement.

## 12. Synchronisation, frame clock et animations

Une animation fluide doit suivre l'horloge d'image de l'interface, et non une boucle arbitraire qui dessine aussi vite que possible. Une boucle trop fréquente gaspille du temps CPU/GPU ; une boucle trop lente produit des saccades.

Principes de conception :

- calculer la progression à partir du temps écoulé, pas du nombre d'itérations ;
- éviter de reconstruire des textures immuables à chaque image ;
- ne demander un nouveau rendu que lorsque l'état visuel change ;
- séparer la logique d'animation de la construction des nœuds ;
- arrêter les animations quand l'acteur n'est plus visible ;
- respecter la préférence de réduction des mouvements ;
- tester les transitions sous charge GPU et pendant le déplacement de fenêtres.

Une animation qui semble fluide sur une capture ou une machine rapide peut devenir coûteuse sur un GPU intégré ou un écran haute fréquence.

## 13. Diagnostic et mesure

Une analyse sérieuse doit distinguer le coût CPU, le coût GPU, les transferts mémoire et la synchronisation avec le compositeur.

Procédure :

1. Établir une mesure de référence sans effet.
2. Activer un seul effet et mesurer à nouveau.
3. Comparer une surface petite et une surface grande.
4. Comparer une scène statique et une scène avec arrière-plan animé.
5. Tester différents facteurs d'échelle.
6. Observer les images perdues et les temps d'image, pas uniquement la moyenne FPS.
7. Vérifier la consommation mémoire lorsque plusieurs fenêtres ou acteurs sont visibles.
8. Refaire les mesures après désactivation de l'effet pour détecter une fuite.

Pour GTK, le renderer GSK peut être choisi ou diagnostiqué selon les options prises en charge par la version installée. Les variables de diagnostic doivent être consultées dans la documentation GTK de la version ciblée ; ne recopiez pas aveuglément une variable d'environnement issue d'une version récente.

Pour GNOME Shell, utilisez les journaux de session et les outils de développement d'extensions. Un shader qui échoue à la compilation ou un acteur détruit mais toujours référencé peut provoquer un défaut visuel ou une erreur pendant le rendu.

## 14. Choisir le bon niveau d'implémentation

- **CSS GTK ou St** : couleurs, bordures, dégradés, ombres et transitions lorsqu'elles sont prises en charge par le moteur.
- **Widget GTK personnalisé** : rendu propre à un composant, snapshot, nœuds GSK, masques et opérations de composition.
- **Extension GNOME Shell** : acteur supplémentaire, comportement d'interface, animation et effets Clutter.
- **Shader Clutter** : traitement GPU personnalisé du contenu d'un acteur.
- **Mutter ou protocole Wayland** : effet qui dépend de la composition des surfaces ou de l'accès à l'arrière-plan.
- **Ressource pré-calculée** : effet fixe qui doit rester prévisible et peu coûteux.

Ne modifiez pas Mutter pour obtenir un simple effet de carte qui peut être réalisé dans GTK. Inversement, ne tentez pas de faire un flou du bureau en CSS lorsque l'accès aux pixels appartient au compositeur.

## 15. Checklist de revue technique

Avant d'intégrer un effet avancé :

- [ ] Le moteur responsable de l'élément est identifié.
- [ ] L'API existe dans la version GNOME 51 ciblée.
- [ ] Le chemin de rendu est compatible avec le renderer utilisé.
- [ ] La portée du flou, du masque ou de l'opacité est maîtrisée.
- [ ] Les textures temporaires et leur taille sont estimées.
- [ ] L'alpha et la convention de prémultiplication sont respectés.
- [ ] Les coordonnées logiques et physiques sont testées.
- [ ] Les profils colorimétriques et la profondeur de couleur sont considérés.
- [ ] Le shader gère les erreurs de compilation et les paramètres invalides.
- [ ] L'effet est retiré proprement à la désactivation de l'extension.
- [ ] Les performances sont mesurées sur une machine modeste.
- [ ] La réduction des mouvements et le contraste restent corrects.

## 16. Références techniques

- [GTK 4 — Drawing model](https://docs.gtk.org/gtk4/drawing-model.html)
- [GTK 4 — GtkSnapshot](https://docs.gtk.org/gtk4/class.Snapshot.html)
- [GTK 4 — Gtk.Widget.snapshot](https://docs.gtk.org/gtk4/vfunc.Widget.snapshot.html)
- [GTK 4 — Migration depuis GTK 3](https://docs.gtk.org/gtk4/migrating-3to4.html)
- [GSK — Node format](https://gnome.pages.gitlab.gnome.org/gtk/gsk4/node-format.html)
- [Mutter 51 — Clutter.ShaderEffect](https://mutter.gnome.org/clutter/class.ShaderEffect.html)
- [Mutter — API Clutter, Cogl et Meta](https://mutter.gnome.org/)
- [Migration des extensions vers GNOME Shell 51](https://gjs.guide/extensions/upgrading/gnome-shell-51.html)
- [Nouveautés développeur GNOME 51](https://release.gnome.org/51/developers/)

Les documentations en ligne peuvent afficher une version postérieure à GNOME 51. Pour les API internes et les signatures GJS, contrôlez toujours les sources et les introspections du tag correspondant à la version ciblée.
