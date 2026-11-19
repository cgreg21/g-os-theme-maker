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

Pour modifier une préférence, identifiez d'abord la clé, sauvegardez sa valeur et expliquez à l'utilisateur comment revenir en arrière.

## 2. Exemple : lire puis modifier une préférence

```sh
# Lire la valeur actuelle
gsettings get org.gnome.desktop.interface color-scheme

# Lire les valeurs autorisées
gsettings range org.gnome.desktop.interface color-scheme

# Exemple de modification, seulement si cette valeur est proposée
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'

# Restaurer la valeur précédente connue
gsettings set org.gnome.desktop.interface color-scheme 'default'
```

Ne copiez pas aveuglément la dernière commande : la valeur initiale de la machine peut être différente. Le bon retour arrière consiste à restaurer la valeur sauvegardée.

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

Les chemins reconnus peuvent varier selon la distribution et les spécifications XDG. Les emplacements usuels incluent :
- `~/.themes/MonTheme` pour certains thèmes GTK/Shell ;
- `~/.local/share/icons/MonTheme` pour les icônes ;
- `~/.icons/MonCurseur` pour certains thèmes de curseurs historiques ;
- `~/.local/share/fonts` pour les polices ;
- `~/.local/share/backgrounds` pour les fonds.

Créez les dossiers nécessaires, copiez uniquement les fichiers du paquet et vérifiez les permissions. L'activation du thème Shell peut demander une extension ou un réglage distinct. Le support des thèmes GTK externes par Libadwaita est limité et dépend de l'application.

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
