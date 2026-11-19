# Maîtriser les thèmes d'icônes Freedesktop

Ce chapitre approfondit le thème d'icônes présenté au chapitre 22. Il suit le parcours complet : comprendre la résolution d'une icône, construire un thème minimal, gérer les variantes et diagnostiquer les icônes absentes. Le thème d'icônes est indépendant du CSS GNOME Shell et des thèmes GTK.

## 1. Comprendre comment une icône est trouvée

Une application demande généralement une icône par son nom, par exemple `folder`, `document-open` ou `org.gnome.Nautilus`. Le système recherche ce nom dans le thème actif, puis dans les thèmes parents déclarés par `Inherits`. Le thème `hicolor` sert de repli final conventionnel.

La résolution dépend aussi de la taille demandée et du contexte. Une icône présente dans le bon thème mais rangée dans un répertoire absent de `Directories` peut être ignorée. Un nom incorrect ne sera pas réparé par le CSS.

Pour diagnostiquer une icône, procédez dans cet ordre :

1. Relevez le nom réellement demandé par l'application.
2. Vérifiez le thème actif.
3. Cherchez le nom dans le thème actif et ses parents.
4. Vérifiez que le dossier est déclaré dans `Directories`.
5. Vérifiez les dimensions et le type de répertoire.
6. Vérifiez les caches éventuels et relancez l'application.

## 2. Construire un thème minimal complet

Créez cette arborescence dans le dossier utilisateur :

```text
~/.local/share/icons/Atelier/
├── index.theme
├── 48x48/
│   └── apps/
│       └── org.example.Editor.png
└── scalable/
    └── actions/
        └── document-save.svg
```

Le fichier `index.theme` :

```ini
[Icon Theme]
Name=Atelier
Comment=Thème d'icônes de démonstration
Inherits=Adwaita;hicolor;
Directories=48x48/apps;scalable/actions;

[48x48/apps]
Size=48
Type=Fixed
Context=Applications

[scalable/actions]
Size=16
Type=Scalable
MinSize=16
MaxSize=64
Context=Actions
```

Chaque entrée de `Directories` doit correspondre à une section portant exactement le même nom. Le chemin doit aussi correspondre au dossier réel, en respectant la casse.

`Type=Fixed` décrit une taille fixe. `Type=Scalable` décrit un fichier vectoriel pouvant être rendu dans une plage de tailles. `Type=Threshold` est destiné aux répertoires bitmap dont la taille nominale accepte une petite marge. Ne déclarez pas arbitrairement tous les dossiers comme scalables.

## 3. Comprendre les contextes

Le contexte décrit la fonction d'une icône, pas son apparence. Les contextes usuels comprennent :

- `Applications` pour les lanceurs ;
- `Actions` pour les opérations d'interface ;
- `Devices` pour les périphériques ;
- `Places` pour les emplacements ;
- `Status` pour les états ;
- `MimeTypes` pour les types de fichiers ;
- `Emblems` pour les petits symboles superposés ;
- `Categories` pour les catégories d'applications.

Respectez la sémantique : une icône de dossier appartient à `Places`, pas à `Applications`. Un mauvais contexte ne rend pas toujours l'icône introuvable, mais complique la maintenance et la cohérence du thème.

## 4. Noms standards, alias et héritage

Préférez les noms normalisés de la spécification Freedesktop. Les noms propres à une application doivent être conservés lorsqu'ils sont documentés par cette application. N'inventez pas un nom visuellement proche en espérant qu'une application le demande.

L'héritage permet de ne fournir que les icônes modifiées. Exemple :

```ini
Inherits=Adwaita;hicolor;
```

Évitez les cycles d'héritage : un thème A ne doit pas hériter de B si B hérite à son tour de A. Gardez un parent connu et disponible. L'ordre compte : les parents sont consultés selon la chaîne de repli.

Pour fournir plusieurs noms pointant vers le même dessin, utilisez des liens symboliques lorsque la plateforme et le système de fichiers le permettent, ou fournissez des fichiers identiques si le paquet doit fonctionner sur des systèmes qui ne préservent pas les liens.

## 5. Icônes symboliques

Les icônes symboliques sont généralement des SVG monochromes conçus pour être teintés par le composant qui les affiche. Leur suffixe usuel est `-symbolic`. Une icône symbolique doit rester reconnaissable à petite taille et sur plusieurs fonds.

Conseils de dessin :

- privilégiez une silhouette simple ;
- évitez les détails plus fins que le rendu à 16 pixels ;
- conservez une marge optique régulière ;
- utilisez les conventions de tracé attendues par l'écosystème GNOME ;
- vérifiez les états clair, sombre, désactivé et accentué ;
- prévoyez une version directionnelle inversée lorsque le symbole exprime une direction.

Ne remplacez pas toutes les icônes colorées d'une application par des variantes symboliques : les icônes d'application sont souvent volontairement multicolores.

## 6. Activer le thème sans toucher aux fichiers système

Vérifiez d'abord la valeur active :

```bash
gsettings get org.gnome.desktop.interface icon-theme
```

Activez le thème de test pour le compte courant :

```bash
gsettings set org.gnome.desktop.interface icon-theme 'Atelier'
```

Pour revenir au thème précédent, rétablissez la valeur que vous aviez notée avant le test. Le thème doit être installé dans `~/.local/share/icons/Atelier`, ou dans un emplacement système géré par la distribution.

Certaines applications conservent des icônes en mémoire. Fermez et relancez l'application avant de conclure que le changement n'a pas fonctionné.

## 7. Outils de vérification

```bash
# Thème actif
gsettings get org.gnome.desktop.interface icon-theme

# Fichiers présents
find ~/.local/share/icons/Atelier -type f -print

# Recherche d'un nom précis
find ~/.local/share/icons/Atelier -iname '*document-save*'

# Vérification du type de fichier
file ~/.local/share/icons/Atelier/scalable/actions/document-save.svg
```

Pour inspecter les noms et chemins réellement utilisés, observez les fichiers de l'application et utilisez GTK Inspector lorsqu'il s'agit d'une application GTK. Le nom visible dans le menu n'est pas nécessairement le nom d'icône demandé.

## 8. Erreurs fréquentes

**L'icône n'apparaît pas.** Vérifiez d'abord le nom exact, la casse, le dossier déclaré et l'héritage. Ne commencez pas par vider tous les caches.

**L'icône est floue.** Le répertoire peut être déclaré avec une mauvaise taille ou le fichier source peut être un bitmap trop petit. Utilisez un SVG approprié ou fournissez des tailles bitmap adaptées.

**Une application conserve l'ancienne icône.** Redémarrez cette application. Certaines applications et certains shells mettent les icônes en cache.

**Le thème semble incomplet.** C'est normal si vous ne fournissez que quelques icônes : l'héritage doit fonctionner et le thème parent doit être installé.

**Les icônes symboliques sont noires ou illisibles.** Vérifiez que le dessin respecte les conventions symboliques et que le composant qui l'affiche applique bien une couleur.

## 9. Exercice guidé

1. Créez le thème `Atelier` avec le fichier `index.theme` ci-dessus.
2. Ajoutez une icône d'application et une icône d'action.
3. Activez le thème avec GSettings.
4. Vérifiez que les icônes non fournies viennent du thème parent.
5. Renommez volontairement une icône et observez le résultat.
6. Corrigez le nom et documentez le comportement constaté.

## 10. Références

- [Spécification Freedesktop des thèmes d'icônes](https://specifications.freedesktop.org/icon-theme/)
- [Spécification des noms d'icônes](https://specifications.freedesktop.org/icon-naming-spec/)
- [GNOME Human Interface Guidelines — Icons](https://developer.gnome.org/hig/)


## 11. Syntaxe exacte de `index.theme`

Les listes de valeurs de `index.theme` utilisent le point-virgule comme séparateur. Une virgule ne remplace pas ce séparateur. La dernière valeur est habituellement suivie d'un point-virgule :

```ini
Inherits=Adwaita;hicolor;
Directories=16x16/actions;24x24/actions;48x48/apps;scalable/actions;
```

Chaque répertoire listé doit avoir sa propre section. Par exemple, si `24x24/actions` est déclaré, le fichier doit contenir une section `[24x24/actions]` avec les attributs adaptés à cette taille. Une entrée absente ou mal orthographiée peut rendre une partie du thème invisible.

Pour un répertoire bitmap à taille fixe :

```ini
[24x24/actions]
Size=24
Type=Fixed
Context=Actions
```

Pour un répertoire bitmap avec tolérance de taille :

```ini
[24x24/actions]
Size=24
Type=Threshold
Threshold=2
Context=Actions
```

Pour un répertoire vectoriel :

```ini
[scalable/actions]
Size=16
Type=Scalable
MinSize=16
MaxSize=64
Context=Actions
```

N'utilisez pas `Threshold` avec un répertoire `Fixed` ou `Scalable`. Les champs propres au type doivent rester cohérents avec le contenu réel du dossier.

## 12. Vérifier la structure et les métadonnées

Depuis la racine du thème :

```bash
# Afficher le fichier de configuration avec ses numéros de ligne
nl -ba index.theme

# Vérifier que les dossiers déclarés existent
find . -mindepth 1 -maxdepth 1 -type d -print

# Lister les fichiers dont le nom contient des espaces ou caractères inhabituels
find . -type f -print0 | while IFS= read -r -d '' f; do
    printf '%q\n' "$f"
done
```

Le contrôle automatique le plus utile consiste à comparer les chemins de `Directories` aux sections et aux dossiers réels. Vérifiez aussi que les noms d'icônes ne contiennent pas l'extension dans les appels applicatifs : une application demande généralement `document-save`, pas `document-save.svg`.

Un fichier présent sur disque n'est pas nécessairement sélectionné. Le thème doit être actif, le nom doit correspondre, le répertoire doit être déclaré et la taille demandée doit pouvoir être satisfaite.

## 13. Alias et liens symboliques

Un alias peut éviter de dupliquer un dessin lorsque deux noms standards doivent afficher exactement la même icône. Depuis le répertoire contenant l'icône cible, un lien relatif peut être créé ainsi :

```bash
ln -s document-save.svg document-save-as.svg
```

Le lien doit rester dans le paquet et sa cible doit exister. Contrôlez-le avec :

```bash
readlink -f actions/document-save-as.svg
```

Adaptez le chemin à votre arborescence réelle. Pour un paquet destiné à être extrait sur des systèmes qui ne préservent pas les liens symboliques, fournissez des fichiers ordinaires ou vérifiez explicitement le comportement de l'outil de packaging.

Ne créez pas d'alias en masse sans vérifier les noms demandés par les applications. Un alias incorrect peut masquer une icône manquante sans respecter la sémantique attendue.

## 14. Cache d'icônes : quand l'utiliser

Le cache n'est pas un substitut à un `index.theme` valide. Pour les thèmes GTK qui contiennent des répertoires bitmap, `gtk-update-icon-cache` peut générer ou actualiser un cache :

```bash
gtk-update-icon-cache --force --ignore-theme-index Atelier
```

Cette commande avec `--ignore-theme-index` n'est pas adaptée à la validation d'un thème Freedesktop complet : elle permet de traiter certains répertoires sans index et ne doit pas servir à contourner un `index.theme` manquant. Pour un thème correctement structuré, utilisez plutôt :

```bash
gtk-update-icon-cache --force Atelier
```

Exécutez-la depuis le dossier parent qui contient le répertoire `Atelier`, ou passez le chemin correct du thème. La disponibilité et le comportement exacts de l'outil dépendent de la version GTK installée. Les applications peuvent également conserver leurs propres caches en mémoire ; redémarrer l'application reste un test utile.

Ne supprimez pas les caches globaux de l'utilisateur ou du système pour corriger une seule icône. Commencez par vérifier le thème et le nom demandé.

## 15. Installer et mettre à jour proprement

Pour installer une version de test dans le compte courant :

```bash
install -d "$HOME/.local/share/icons/Atelier"
cp -a ./Atelier/. "$HOME/.local/share/icons/Atelier/"
```

Cette méthode copie le contenu dans la destination existante. Pour une mise à jour qui supprime aussi les anciens fichiers devenus inutiles, préparez une nouvelle arborescence complète, validez-la, puis remplacez l'ancienne avec une sauvegarde. Ne supprimez pas le dossier actif avant d'avoir vérifié la nouvelle copie.

Avant de remplacer un thème déjà utilisé, conservez la valeur précédente de `icon-theme`. Pour revenir en arrière, rétablissez cette valeur avec GSettings. N'utilisez pas `sudo` pour installer un thème dans le répertoire personnel.

## 16. Références complémentaires

- [Freedesktop — spécification des thèmes d'icônes, format index.theme](https://specifications.freedesktop.org/icon-theme/latest/)
- [GTK — gtk-update-icon-cache](https://docs.gtk.org/gtk4/)
