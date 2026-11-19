# Paramètres GNOME, installation et dépannage

Un thème visuel et une préférence système sont deux choses différentes. Cette distinction évite de modifier un réglage de comportement avec du CSS ou d'écraser des paramètres personnels lors de l'installation.

## 1. Comprendre GSettings et dconf

GSettings expose des paramètres nommés par schéma et clé. dconf est un backend de stockage utilisé par de nombreux paramètres. L'outil `gsettings` permet de lire et modifier une valeur. `dconf` permet notamment d'exporter et restaurer des chemins de configuration.

Exemples de lecture :

```sh
gsettings list-schemas
gsettings list-keys org.gnome.desktop.interface
gsettings get org.gnome.desktop.interface color-scheme
gsettings get org.gnome.desktop.interface font-name
```

Les schémas et clés disponibles dépendent des paquets et de la version installés. Vérifiez toujours leur présence avant d'utiliser une commande.

Pour connaître les valeurs possibles d'une clé :

```sh
gsettings range org.gnome.desktop.interface color-scheme
```

Pour modifier une préférence, identifiez d'abord la clé, sauvegardez sa valeur exacte et expliquez à l'utilisateur comment restaurer cette valeur. Revenir à la valeur par défaut et revenir à la valeur précédente sont deux opérations différentes.

## 2. Exemple : lire, sauvegarder, modifier et restaurer une préférence

L'exemple suivant sauvegarde la valeur GVariant exacte dans un fichier privé avant de modifier la clé. Il suppose que la clé existe et que la plage de valeurs autorise `prefer-dark`.

```sh
umask 077
SCHEMA=org.gnome.desktop.interface
KEY=color-scheme
BACKUP="$HOME/color-scheme.before.txt"

# Vérifier la clé et les valeurs possibles
gsettings range "$SCHEMA" "$KEY"
gsettings writable "$SCHEMA" "$KEY"

# Enregistrer la valeur exacte avant modification
gsettings get "$SCHEMA" "$KEY" > "$BACKUP"

# Appliquer une valeur uniquement si elle est autorisée
gsettings set "$SCHEMA" "$KEY" 'prefer-dark'

# Restaurer exactement la valeur sauvegardée
gsettings set "$SCHEMA" "$KEY" "$(cat "$BACKUP")"
```

Le fichier de sauvegarde contient la représentation GVariant renvoyée par `gsettings get`. Gardez-le privé et supprimez-le seulement après avoir vérifié le retour à l'état initial. Si votre objectif est au contraire d'effacer la surcharge utilisateur et de reprendre la valeur par défaut du schéma, utilisez `gsettings reset "$SCHEMA" "$KEY"`. Cette dernière commande ne restaure pas nécessairement la valeur précédente.

## 3. Sauvegarder dconf

Avant une série de modifications, exportez le chemin que vous allez toucher :

```sh
dconf dump /org/gnome/desktop/interface/ > interface-backup.ini
```

Restauration :

```sh
dconf load /org/gnome/desktop/interface/ < interface-backup.ini
```

Ne restaurez pas un dump global sans comprendre son contenu. Il peut écraser des préférences personnelles sans rapport avec le thème.

## 4. Installer un thème utilisateur

Les chemins reconnus dépendent du type de ressource, des répertoires XDG, du moteur et de la distribution. Commencez par identifier le répertoire de données utilisateur :

```sh
printf 'XDG_DATA_HOME=%s\\n' "${XDG_DATA_HOME:-$HOME/.local/share}"
printf 'XDG_DATA_DIRS=%s\\n' "${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"
```

Emplacements courants :
- `~/.local/share/themes/MonTheme` pour les thèmes GTK utilisateur ; `~/.themes/MonTheme` reste utilisé par certains composants et outils comme chemin historique ;
- `~/.local/share/icons/MonTheme` pour les thèmes d'icônes ;
- `~/.local/share/icons/MonCurseur` pour les thèmes de curseurs, qui utilisent le format Xcursor ;
- `~/.local/share/fonts/` pour les polices utilisateur ;
- `~/.local/share/backgrounds/` pour organiser des fonds d'écran personnels, sans que ce dossier soit à lui seul un mécanisme d'activation universel.

Le thème GNOME Shell est un cas distinct : il est généralement fourni sous `gnome-shell/` dans un thème et son activation dépend de la prise en charge des thèmes utilisateur, notamment de l'extension User Themes et de la session. La présence du fichier `gnome-shell.css` ne signifie pas que le Shell le charge. Les icônes, curseurs et polices ont également leurs propres préférences d'activation.

Créez les dossiers nécessaires, copiez uniquement les fichiers du paquet et vérifiez les permissions. Ne copiez pas un dossier complet dans un emplacement système par habitude. Le support des thèmes GTK externes par Libadwaita est limité et dépend de l'application ; il ne faut pas promettre qu'un thème GTK personnalisé modifiera toutes les applications Libadwaita.

## 5. Désinstaller sans casser la configuration

Une désinstallation sûre supprime uniquement les fichiers installés par le paquet. Elle ne doit pas effacer le dossier entier des thèmes utilisateur ni réinitialiser tous les paramètres GNOME. Si le thème a modifié GSettings, restaurez uniquement les clés sauvegardées par l'installation.

## 6. Diagnostic pas à pas

### Le CSS ne change rien
- vérifiez le moteur utilisé ;
- vérifiez le chemin et le nom du fichier ;
- vérifiez que le thème est activé ;
- vérifiez le sélecteur ;
- vérifiez que le composant est présent ;
- testez une propriété évidente ;
- inspectez les avertissements du moteur.

### Une application est partiellement stylée
L'application peut utiliser plusieurs bibliothèques, charger un provider CSS local, utiliser des widgets personnalisés ou être isolée par Flatpak. Identifiez le widget réel au lieu de supposer que toute l'application utilise le même thème.

### Le texte est coupé
Vérifiez le padding, la hauteur, la taille de police, la graisse, l'échelle HiDPI et la longueur du texte traduit. Ne résolvez pas un problème de hauteur en diminuant systématiquement la police.

### Le menu est illisible
Testez séparément le fond, le texte, les séparateurs, les éléments désactivés, les icônes et le focus. Une règle de couleur sur le conteneur ne garantit pas que les widgets enfants héritent de cette couleur.

### Le thème casse après une mise à jour
Comparez la version GNOME/GTK, inspectez les changements de classes CSS, testez les nouvelles feuilles amont et identifiez le sélecteur devenu obsolète. Ne masquez pas le problème par une règle globale plus agressive.

## 7. Outils de diagnostic

```sh
gnome-shell --version
echo "$XDG_SESSION_TYPE"
echo "$XDG_CURRENT_DESKTOP"
pkg-config --modversion gtk+-3.0
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
gnome-extensions list
fc-match Cantarell
```

Pour examiner les journaux de la session :

```sh
journalctl --user -b
```

La commande peut retourner beaucoup de lignes. Filtrez avec `grep` et recherchez les avertissements CSS, GTK ou Shell pertinents.

## 8. Limites système

Mutter contrôle les fenêtres, les écrans et la composition. GDM est le gestionnaire de connexion système. Le verrouillage, la veille, les portails, les extensions et les applications tierces peuvent avoir des chemins de configuration différents. Toute modification GDM ou système doit être un module distinct, sauvegardé et réversible, avec des privilèges explicites.

## 9. Règle de sécurité

G-OS Theme Maker doit montrer les modifications avant de les appliquer, sauvegarder les valeurs initiales, limiter l'écriture aux fichiers qu'il gère et proposer un retour arrière. Il ne doit pas modifier silencieusement les préférences sans rapport avec le thème.
