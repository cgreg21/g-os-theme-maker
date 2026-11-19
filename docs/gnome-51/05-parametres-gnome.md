# 5. Paramètres GNOME, GSettings et dconf

Les réglages ne sont pas du CSS. Ils contrôlent préférences, comportement, périphériques et session. Les schémas installés localement font autorité : les clés varient selon distribution, paquet et version.

## 5.1 Explorer avant d'écrire

```sh
gsettings list-schemas
gsettings list-keys org.gnome.desktop.interface
gsettings describe org.gnome.desktop.interface color-scheme
gsettings range org.gnome.desktop.interface color-scheme
gsettings get org.gnome.desktop.interface color-scheme
gsettings writable org.gnome.desktop.interface color-scheme
```

Ne jamais inventer une clé ni supposer que sa plage est identique partout.

## 5.2 Apparence générale

Le schéma `org.gnome.desktop.interface` expose souvent `color-scheme`, `gtk-theme`, `icon-theme`, `cursor-theme`, `cursor-size`, `font-name`, `document-font-name`, `monospace-font-name`, `text-scaling-factor`, `enable-animations`, `clock-show-date`, `clock-show-seconds`, `clock-show-weekday` et `show-battery-percentage`. Vérifier chaque clé.

## 5.3 Fonds

Explorer `org.gnome.desktop.background` pour `picture-uri`, `picture-uri-dark`, `picture-options`, `primary-color`, `secondary-color` et `color-shading-type`. Les réglages de verrouillage peuvent relever de `org.gnome.desktop.screensaver`. Valider URI et valeurs localement.

## 5.4 Souris, pavé tactile, clavier, son

Schémas usuels : `org.gnome.desktop.peripherals.mouse`, `touchpad`, `keyboard`, `org.gnome.desktop.sound`. Ils pilotent vitesse, accélération, clic, défilement, répétition et sons. Les clés dépendent du matériel et ne doivent pas être embarquées dans un thème sans consentement.

## 5.5 Fenêtres, Shell et raccourcis

Inspecter `org.gnome.desktop.wm.preferences`, `org.gnome.desktop.wm.keybindings`, `org.gnome.mutter`, `org.gnome.shell`, `org.gnome.shell.keybindings`, `org.gnome.shell.window-switcher`, `org.gnome.shell.app-switcher` et `org.gnome.settings-daemon.plugins.media-keys`.

GNOME Shell 51 déclare extensions activées/désactivées, favoris, disposition de grille et raccourcis overview, quick settings, capture, enregistrement et luminosité. Voir [le schéma 51.0](https://github.com/GNOME/gnome-shell/blob/51.0/data/org.gnome.shell.gschema.xml.in).

Les raccourcis sont souvent des tableaux de chaînes. Détecter les conflits avec Shell, Mutter, applications et extensions. Ne jamais écraser une combinaison inconnue sans confirmation.

## 5.6 Écrans et Mutter

Résolution, fréquence, rotation, disposition multi-écrans et échelle relèvent de Mutter et des paramètres GNOME, pas du CSS. Utiliser l'interface Paramètres ; tester plusieurs échelles et écrans.

## 5.7 Sauvegarde et restauration

```sh
dconf dump /org/gnome/ > gnome-backup.ini
dconf load /org/gnome/ < gnome-backup.ini
```

Le dump contient des préférences personnelles : ne pas l'inclure dans un thème partageable. Préférer une liste blanche de clés choisies. Ne pas utiliser `dconf reset -f /` ou `gsettings reset-recursively` comme dépannage générique. Les valeurs par défaut et verrous sous `/etc/dconf/db/` relèvent de l'administration système.
