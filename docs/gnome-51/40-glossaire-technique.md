# 40. Glossaire technique de la personnalisation GNOME

Ce glossaire définit les termes employés dans le manuel. Il sert de référence pendant les ateliers : lorsqu'un terme apparaît dans une procédure, revenez ici pour distinguer les concepts qui se ressemblent.

Les définitions décrivent le contexte GNOME 51, GTK 3, GTK 4 et Libadwaita. Elles ne remplacent pas les spécifications des bibliothèques.

## A

**Acteur (St Actor)** — Élément graphique de GNOME Shell. Les acteurs St sont construits au-dessus de Clutter et composent des éléments comme les boutons, panneaux et menus du Shell. Ils ne sont pas des widgets GTK.

**Adwaita** — Système visuel et bibliothèque de composants de GNOME. Adwaita définit des conventions d'apparence, des couleurs sémantiques et des composants cohérents. Libadwaita étend ces conventions pour les applications GTK 4.

**API** — Interface de programmation exposée par une bibliothèque ou un composant. Une API documentée est destinée à être utilisée par les développeurs ; une classe CSS interne de GNOME Shell n'est pas nécessairement une API stable.

**Arbre CSS** — Structure des nœuds sur laquelle le moteur CSS applique les sélecteurs. Dans GTK, cet arbre peut différer de l'arbre logique des widgets. Dans Shell, il correspond aux acteurs et à leurs relations.

## B

**Backdrop** — État indiquant généralement qu'une fenêtre n'est pas active. GTK expose notamment la pseudo-classe :backdrop sur les nœuds concernés.

**Backend** — Implémentation qui fournit un service à une API. GSettings peut utiliser dconf comme backend de stockage. Le choix du backend ne change pas la signification du schéma GSettings.

**Bordure (border)** — Trait entourant une boîte. Les propriétés de bordure définissent son épaisseur, son style et sa couleur. Une bordure CSS ne remplace pas nécessairement les séparateurs dessinés par un widget.

**CSS provider** — Fournisseur de règles CSS chargé par GTK ou un autre moteur compatible. Une application peut charger un provider propre à son interface, qui s'ajoute au thème et aux autres providers.

## C

**Cascade CSS** — Processus qui détermine quelle déclaration s'applique lorsqu'une propriété est définie plusieurs fois. Elle dépend notamment de l'origine de la règle, de sa priorité, de sa spécificité et de l'ordre des déclarations.

**Clutter** — Bibliothèque de scène graphique utilisée par GNOME Shell via St. Elle gère notamment les acteurs, transformations, animations et compositions visuelles.

**Composant** — Partie identifiable d'une interface : bouton, panneau, menu, champ, dialogue, carte ou indicateur. Un composant peut contenir plusieurs nœuds CSS.

**Contraste élevé** — Variante d'affichage qui renforce la distinction entre textes, surfaces, bordures et contrôles. Elle ne doit pas être traitée comme une simple inversion du mode sombre.

**CSD (Client-Side Decorations)** — Décorations de fenêtre dessinées par l'application elle-même. Les barres d'en-tête GTK et Libadwaita sont des exemples courants.

## D

**dconf** — Système de configuration utilisé couramment comme backend de GSettings dans GNOME. Il stocke des valeurs et fournit des outils pour les lire, les écrire, les exporter et les importer.

**Déclaration CSS** — Association d'une propriété et d'une valeur, par exemple color: white. Une déclaration peut être ignorée si la propriété ou la valeur n'est pas prise en charge par le moteur ciblé.

**Densité** — Quantité d'espace et de contenu présentée dans une interface. Elle dépend des espacements, tailles minimales, polices, facteurs d'échelle et choix de conception.

**DPI** — Mesure de densité physique d'un écran. Les environnements de bureau utilisent également des pixels logiques et des facteurs d'échelle ; ne confondez pas DPI physique et taille CSS.

**dnd (Drag and Drop)** — Interaction de glisser-déposer. Le CSS peut styliser la source, la cible et l'indicateur de dépôt, mais ne crée pas le comportement fonctionnel du glisser-déposer.

## E

**État CSS** — Condition temporaire ou persistante d'un nœud : survol, focus, pression, sélection, désactivation, fenêtre inactive ou dépôt. Les états sont exposés par des pseudo-classes ou des classes.

**Échelle (scale factor)** — Rapport entre pixels logiques et pixels physiques. Une interface peut avoir une taille logique identique tout en utilisant davantage de pixels physiques sur un écran HiDPI.

**Extension GNOME Shell** — Module JavaScript qui ajoute ou modifie des fonctions du Shell. Une extension peut créer des acteurs St, ajouter une feuille CSS et enregistrer des raccourcis. Elle doit nettoyer ses ressources lors de sa désactivation.

## F

**Fallback** — Ressource ou valeur de repli utilisée lorsqu'un élément demandé n'est pas disponible. Exemples : police de remplacement, icône héritée, thème parent ou valeur par défaut.

**Flatpak** — Système de distribution et d'exécution d'applications dans un environnement isolé. Une application Flatpak peut ne pas voir les thèmes, polices ou ressources installés sur l'hôte sans extension ou accès adapté.

**Focus** — Élément qui reçoit les interactions clavier. Un thème doit rendre le focus visible, y compris dans les menus, dialogues et contrôles composites.

**Freedesktop** — Ensemble de spécifications et conventions partagées par les environnements de bureau Linux, notamment pour les icônes, les chemins et les thèmes de ressources.

## G

**GDM** — Gestionnaire de connexion GNOME. Il fonctionne dans un contexte système distinct de la session utilisateur ; un thème installé dans le dossier personnel ne modifie pas automatiquement son écran de connexion.

**GJS** — Environnement JavaScript qui permet d'utiliser les bibliothèques GNOME depuis JavaScript. GNOME Shell et ses extensions utilisent GJS.

**GLib** — Bibliothèque fondamentale de GNOME. Elle fournit notamment les types de base, les systèmes de fichiers, les boucles d'événements et GSettings.

**GResource** — Système de ressources compilées de GLib. Il permet d'intégrer des fichiers tels que CSS, images et interfaces dans un programme.

**GSettings** — API de préférences basée sur des schémas. Elle expose des clés typées, leurs valeurs par défaut et leurs contraintes. Les outils gsettings permettent de les explorer et de les modifier.

**GTK** — Toolkit d'interface graphique utilisé par de nombreuses applications GNOME. GTK 3 et GTK 4 possèdent des moteurs CSS distincts et ne partagent pas exactement les mêmes widgets ni les mêmes propriétés.

**GTK Inspector** — Outil de développement permettant d'inspecter les widgets GTK, leur arbre CSS, leurs classes, leurs états et leurs propriétés calculées. Il n'inspecte pas les acteurs internes de GNOME Shell.

## H

**HiDPI** — Écran à forte densité de pixels. L'interface doit conserver des tailles physiques lisibles grâce à l'échelle, aux ressources adaptées et à des dimensions cohérentes.

**HIG (Human Interface Guidelines)** — Recommandations de conception d'interface de GNOME. Elles décrivent les conventions d'interaction, la disposition et l'accessibilité ; elles ne constituent pas une spécification CSS.

**Hotspot** — Coordonnée du point actif d'un curseur. Le hotspot détermine l'endroit exact où le clic est appliqué dans l'image du pointeur.

## I

**Icône symbolique** — Icône monochrome conçue pour être recolorée selon le contexte. Elle est souvent utilisée dans les barres d'outils, indicateurs et interfaces adaptatives.

**ID CSS** — Identifiant unique associé à un nœud dans un contexte donné. Dans GTK, le sélecteur #nom cible le nom CSS du widget ; il ne faut pas l'interpréter comme un identifiant HTML.

**Inherit / héritage** — Mécanisme par lequel certaines propriétés sont transmises d'un parent à ses descendants. Toutes les propriétés CSS ne sont pas héritées.

## L

**Libadwaita** — Bibliothèque GNOME construite sur GTK 4. Elle fournit des widgets et conventions visuelles Adwaita. Son apparence dépend de sa version et de l'application qui la charge.

**Looking Glass** — Outil de diagnostic intégré à GNOME Shell. Il permet d'examiner les erreurs, extensions et acteurs du Shell. Il est distinct de GTK Inspector.

**LTR / RTL** — Sens d'écriture de gauche à droite ou de droite à gauche. Un thème doit tenir compte des langues RTL et éviter de coder en dur les directions lorsque des propriétés logiques existent.

## M

**Mutter** — Compositeur et gestionnaire de fenêtres de GNOME. Il gère notamment les fenêtres, écrans, espaces de travail, composition et interactions avec Wayland ou X11.

**Mode sombre** — Variante de présentation utilisant des surfaces généralement plus sombres. Les applications peuvent réagir à une préférence système, mais chaque moteur et application peut gérer cette préférence différemment.

## N

**Nœud CSS** — Élément de l'arbre de style ciblé par un sélecteur. Il peut représenter un widget, un sous-élément ou un acteur, et n'est pas nécessairement visible ou interactif seul.

**Nom de widget** — Nom donné à un widget GTK pour permettre notamment son ciblage CSS. Il ne correspond pas nécessairement au nom de sa classe de style.

## O

**OSD (On-Screen Display)** — Affichage temporaire superposé, par exemple un indicateur de volume, de luminosité ou de changement d'espace de travail.

**Origine d'une règle** — Source qui fournit une déclaration CSS : feuille du thème, CSS applicatif, provider utilisateur ou style interne. L'origine et la priorité contribuent à la cascade.

## P

**Pango** — Bibliothèque de mise en forme du texte utilisée notamment par GTK. Elle gère les scripts, langues, directions et choix de polices.

**Pseudo-classe** — Sélecteur qui représente un état ou une condition d'un nœud, par exemple :hover ou :focus. Sa prise en charge dépend du moteur et du composant.

**Pseudo-élément** — Sélecteur visant une partie particulière d'un élément dans les moteurs qui le prennent en charge. Ne supposez pas que les pseudo-éléments du Web existent dans GTK ou St.

**Provider** — Fournisseur de règles ou de valeurs. Dans GTK, un CSS provider apporte des règles à la cascade. Dans GSettings, le backend est parfois décrit comme le fournisseur du stockage.

## R

**Ressource Xcursor** — Image de curseur encodée dans le format Xcursor. Elle peut contenir plusieurs tailles et images animées, avec un hotspot associé.

**Ressource GResource** — Fichier intégré à un bundle de ressources GLib et adressé par un chemin de ressource. Elle peut être embarquée dans un exécutable.

**RGBA** — Modèle de couleur comprenant rouge, vert, bleu et alpha. Le canal alpha représente la transparence de la couleur, pas nécessairement l'opacité finale de tout le composant.

## S

**SCSS** — Extension de CSS qui ajoute notamment variables, fonctions, mixins et imbrication. Les sources SCSS du thème GNOME Shell sont compilées en feuilles CSS ; les variables SCSS ne deviennent pas automatiquement des variables CSS.

**Sélecteur** — Expression qui identifie les nœuds auxquels une règle CSS s'applique. Un sélecteur valide syntaxiquement peut ne correspondre à aucun élément de l'interface.

**Serveur-side decorations (SSD)** — Décorations de fenêtre dessinées par le compositeur ou le gestionnaire de fenêtres, par opposition aux décorations côté client.

**Shell (GNOME Shell)** — Interface principale du bureau GNOME : panneau, vue Activités, menus système, notifications, espaces de travail et autres composants. Le Shell n'est pas une application GTK ordinaire.

**Spécificité** — Règle de comparaison entre sélecteurs CSS lorsque plusieurs déclarations de même origine et priorité ciblent une propriété. Les détails diffèrent selon le moteur.

**St** — Toolkit utilisé par GNOME Shell pour créer ses acteurs et appliquer des styles. Il repose sur Clutter et expose un sous-ensemble de mécanismes de style distinct de GTK.

## T

**Thème GTK** — Ensemble de ressources et feuilles CSS destinées à GTK. GTK 3 et GTK 4 sont des cibles distinctes ; une feuille n'est pas garantie compatible avec les deux.

**Thème Shell** — Feuille de style et ressources utilisées par GNOME Shell. Ses classes et identifiants sont des détails internes susceptibles de changer d'une version à l'autre.

**Toolkit** — Bibliothèque qui fournit les composants et mécanismes d'interface d'une application. GTK, Qt et les composants web d'Electron sont des toolkits ou environnements d'interface différents.

**Transition** — Animation interpolant une propriété entre deux valeurs lorsqu'un état change. Les propriétés animables et la syntaxe disponible varient selon le moteur CSS.

## V

**Valeur calculée** — Valeur finale d'une propriété après cascade, héritage, valeurs par défaut et traitement du moteur. Elle peut différer de la valeur écrite dans une règle CSS.

**Variable CSS personnalisée** — Valeur définie avec une syntaxe --nom et réutilisée avec var(). La prise en charge dépend de la version du moteur ; ne la supposez pas identique dans GTK 3, GTK 4 et Shell.

**Variable SCSS** — Valeur utilisée à la compilation SCSS. Elle est résolue lors de la génération du CSS et n'est pas modifiable dynamiquement à l'exécution comme une variable CSS.

## W

**Wayland** — Protocole et architecture de serveur d'affichage utilisés par GNOME. Mutter joue le rôle de compositeur Wayland dans une session GNOME.

**Widget** — Composant d'interface fourni par GTK ou une bibliothèque construite sur GTK. Un widget peut exposer plusieurs nœuds CSS et classes de style.

## X

**X11 / Xorg** — Système d'affichage historique pour les environnements Linux. GNOME peut fonctionner avec une session X11 selon la distribution et la version, mais les mécanismes d'affichage et de décoration diffèrent de Wayland.

**XDG Base Directory** — Spécification définissant des emplacements standards pour les données, configurations et caches utilisateur. Les thèmes et ressources doivent respecter ces chemins plutôt que s'installer arbitrairement.

## Règle de lecture

Lorsqu'un terme décrit un mécanisme interne, identifiez toujours sa couche :
- CSS du Shell et acteurs St ;
- widgets et moteur CSS GTK ;
- composants et styles Libadwaita ;
- préférences GSettings et stockage dconf ;
- composition et fenêtres Mutter ;
- ressources Freedesktop ;
- comportement propre à une application ou à une extension.

Cette distinction évite de chercher une solution CSS à un problème de configuration, de toolkit ou de comportement.
