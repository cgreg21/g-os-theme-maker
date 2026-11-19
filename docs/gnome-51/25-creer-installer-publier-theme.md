# Construire, installer, tester et publier un thème GNOME complet


Ce dernier atelier relie les chapitres spécialisés pour produire un thème utilisateur cohérent, testable et réversible. Il ne remplace pas les références techniques : il fournit une procédure reproductible.

## 1. Définir le périmètre

Un thème peut contenir une feuille GNOME Shell, un thème GTK 3, des adaptations GTK 4, des icônes, des curseurs, des polices, des fonds d'écran et des sons. Ces ressources sont indépendantes. Il est préférable de livrer un thème Shell et GTK fiables plutôt qu'un paquet qui prétend modifier des composants qu'il ne contrôle pas.

Documentez les limites : applications Libadwaita, GDM, extensions tierces, composants privés et versions non testées.

## 2. Organiser le paquet

```text
MonTheme/
├── gnome-shell/
│   └── gnome-shell.css
├── gtk-3.0/
│   └── gtk.css
├── gtk-4.0/
│   └── gtk.css
├── icons/
│   └── MonTheme/
│       └── index.theme
├── cursors/
│   └── MonCurseur/
│       ├── index.theme
│       └── cursors/
├── backgrounds/
├── README.md
└── LICENSE
```

N'ajoutez pas de dossier vide pour donner l'impression qu'une famille est prise en charge. Chaque dossier doit contenir des ressources valides et des instructions d'installation.

## 3. Créer le thème Shell minimal

Le dossier doit contenir `gnome-shell/gnome-shell.css`.

```css
#panel {
  background-color: #242424;
  color: #ffffff;
}

#panel .panel-button {
  border-radius: 999px;
  padding: 0 10px;
}

.popup-menu {
  border-radius: 12px;
}

.popup-menu-item {
  padding: 8px 12px;
}
```

Ces sélecteurs sont des détails internes du Shell et peuvent changer entre versions. Vérifiez-les dans les sources de la version ciblée et testez-les dans une session isolée. Le thème Shell utilisateur peut nécessiter l'extension User Themes.

## 4. Préparer GTK 3, GTK 4 et Libadwaita

Pour GTK 3, créez `gtk-3.0/gtk.css`. Pour GTK 4, créez `gtk-4.0/gtk.css`. N'annoncez pas une prise en charge Libadwaita complète sans tests sur les applications concernées.

Testez boutons, champs, listes, barres d'en-tête, menus, dialogues, vues vides, barres de défilement et états désactivés.

## 5. Installer les ressources dans le compte utilisateur

Le nom du dossier installé doit correspondre au nom choisi dans les préférences. Depuis le répertoire qui contient `MonTheme/` :

```bash
mkdir -p "$HOME/.themes" "$HOME/.local/share/icons"
cp -a MonTheme "$HOME/.themes/MonTheme"
```

Cette copie installe les sous-répertoires `gnome-shell/`, `gtk-3.0/` et `gtk-4.0/` éventuels. N'ajoutez pas ces répertoires si le paquet ne contient pas réellement les ressources correspondantes.

Les thèmes d'icônes et les thèmes de curseurs sont généralement installés comme thèmes d'icônes XDG, chacun dans son propre répertoire :

```bash
cp -a MonTheme/icons/MonTheme "$HOME/.local/share/icons/MonTheme"
cp -a MonTheme/cursors/MonCurseur "$HOME/.local/share/icons/MonCurseur"
```

N'exécutez chaque copie que si le dossier source existe et contient un `index.theme` valide. Le dossier `cursors/` du paquet est ici une convention d'organisation : après installation, le thème Xcursor est bien recherché parmi les thèmes d'icônes. Vérifiez aussi les chemins des ressources référencées dans `index.theme`.

Les polices, fonds d'écran et sons ont leurs propres mécanismes et ne deviennent pas actifs parce qu'ils sont placés dans `~/.themes`. Documentez séparément leur installation. Pour un usage personnel, évitez `/usr/share` et les commandes avec `sudo`.

## 6. Sauvegarder, sélectionner et vérifier les préférences

Avant de modifier les préférences, sauvegardez la branche dconf concernée. Elle contient plusieurs réglages d'interface, pas uniquement les noms de thèmes :

```bash
mkdir -p "$HOME/.local/state/mon-theme"
dconf dump /org/gnome/desktop/interface/ \
  > "$HOME/.local/state/mon-theme/interface.dconf"
```

Vérifiez que le fichier existe et n'est pas vide avant de poursuivre. Relevez ensuite les valeurs actuellement actives :

```bash
gsettings get org.gnome.desktop.interface gtk-theme
gsettings get org.gnome.desktop.interface icon-theme
gsettings get org.gnome.desktop.interface cursor-theme
gsettings get org.gnome.desktop.interface color-scheme
```

Sélectionnez uniquement les familles réellement installées :

```bash
gsettings set org.gnome.desktop.interface gtk-theme 'MonTheme'
gsettings set org.gnome.desktop.interface icon-theme 'MonTheme'
gsettings set org.gnome.desktop.interface cursor-theme 'MonCurseur'
```

La dernière commande ne s'applique que si le thème de curseurs a été installé. Le schéma et la clé doivent exister sur la version ciblée ; consultez `gsettings list-schemas` et `gsettings list-keys` en cas de doute.

Le thème GNOME Shell est distinct du thème GTK. Son activation peut nécessiter l'extension User Themes, installée et compatible avec la version courante :

```bash
gnome-extensions list
gnome-extensions info user-theme@gnome-shell-extensions.gcampax.github.com
```

Si l'extension est disponible, son schéma expose généralement la clé `name`. Vérifiez avant de la modifier :

```bash
gsettings list-schemas | grep -F org.gnome.shell.extensions.user-theme
gsettings list-keys org.gnome.shell.extensions.user-theme
```

N'activez pas une extension inconnue ou incompatible sur votre session principale. Une modification de thème GTK ne garantit pas un changement équivalent dans les applications GTK 4 ou Libadwaita : vérifiez chaque famille séparément.

## 7. Construire un test reproductible

Testez dans un compte secondaire, une machine virtuelle ou une session GNOME isolée. Consignez la version de GNOME Shell, GTK 3, GTK 4 et Libadwaita, la distribution, le type de session, les extensions actives, la résolution, le facteur d'échelle et la variante clair/sombre.

```bash
gnome-shell --version
pkg-config --modversion gtk+-3.0
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
```

Une commande peut manquer si le paquet de développement correspondant n'est pas installé. Cela ne signifie pas que le toolkit est absent du système.

## 8. Vérifier les composants Shell

Testez panneau, menus, réglages rapides, calendrier, notifications, vue Activités, Dash, grille d'applications, Alt-Tab, OSD, dialogues, écran verrouillé, capture d'écran et interfaces de saisie.

Pour chaque composant, vérifiez l'état normal, survol, focus, activation, désactivation, contenu long, thème clair, thème sombre et contraste élevé.

## 9. Vérifier les applications et ressources

Testez Nautilus, Paramètres, Calendar, Console, Software, au moins une application GTK 3, plusieurs applications GTK 4 et plusieurs applications Libadwaita.

Vérifiez les icônes symboliques et d'applications, curseurs, polices, glyphes, fonds clairs et sombres et sons optionnels.

## 10. Accessibilité et langues

Vérifiez contraste, focus clavier, navigation sans souris, taille du texte, contraste élevé, réduction des animations et dispositions droite-à-gauche. La couleur ne doit jamais être le seul moyen de transmettre une information.

## 11. Journaux et diagnostic

```bash
journalctl --user -f
journalctl --user -b | grep -iE 'gnome-shell|stylesheet|css|extension'
GTK_DEBUG=interactive nom-de-l-application
```

Le nom d'exécutable dépend de l'application. Fermez-la proprement après l'inspection.

## 12. Retour arrière et désinstallation

La sauvegarde créée à l'étape 6 permet de restaurer les réglages de la branche dconf de l'interface :

```bash
dconf load /org/gnome/desktop/interface/ \
  < "$HOME/.local/state/mon-theme/interface.dconf"
```

Cette opération restaure les valeurs enregistrées dans cette branche, y compris les préférences d'interface sans rapport direct avec le thème. Utilisez-la si vous souhaitez revenir à l'état complet sauvegardé. Si vous ne voulez restaurer que les thèmes, remettez uniquement les valeurs précédemment relevées avec `gsettings set`. Ne confondez pas cette restauration avec `gsettings reset`, qui rétablit la valeur par défaut du schéma et non votre ancienne valeur personnelle.

Si User Themes a été activée uniquement pour cet essai, désactivez-la après avoir vérifié que cela ne perturbe pas d'autres personnalisations :

```bash
gnome-extensions disable user-theme@gnome-shell-extensions.gcampax.github.com
```

Ne lancez cette commande que si l'extension est installée et si vous l'aviez activée pour ce test. Rétablissez également le nom du thème Shell précédent si vous n'avez pas restauré la sauvegarde dconf.

Supprimez ensuite uniquement les répertoires de ce paquet que vous avez effectivement installés. Vérifiez chaque chemin avant suppression :

```bash
rm -rf -- "$HOME/.themes/MonTheme"
rm -rf -- "$HOME/.local/share/icons/MonTheme"
rm -rf -- "$HOME/.local/share/icons/MonCurseur"
```

Retirez une ligne si le répertoire correspondant n'appartient pas à ce test. N'utilisez jamais une variable vide ou non vérifiée dans une commande de suppression. Les polices, fonds d'écran et sons installés séparément doivent être désinstallés selon les chemins indiqués dans le README du paquet.

## 13. Documenter et publier

Le README du paquet doit préciser l'objectif, la version GNOME ciblée, les toolkits pris en charge, les limites, les dépendances, l'installation, la désinstallation, le retour arrière, les captures, les licences et la procédure de signalement d'un problème.

Les captures doivent montrer le thème réellement testé. N'utilisez pas une capture d'un autre thème ou d'une autre version pour prétendre démontrer la compatibilité.

```bash
tar -czf MonTheme.tar.gz MonTheme/
tar -tzf MonTheme.tar.gz
```

Ne publiez pas de fichiers temporaires, de caches, de sauvegardes personnelles ou de chemins absolus.

## 14. Maintenir la compatibilité

Pour chaque version majeure de GNOME : lisez les notes de version, comparez les fichiers SCSS du Shell, vérifiez les sélecteurs et propriétés, vérifiez les schémas GSettings, testez GTK 3, GTK 4 et Libadwaita séparément, inspectez les applications importantes et mettez à jour la matrice de compatibilité.

Un CSS accepté par le parseur ne prouve pas que les sélecteurs correspondent à des éléments réellement présents.

## 15. Licences et attribution

Vérifiez les licences des images, icônes, curseurs, polices, sons et fonds d'écran. Conservez les fichiers de licence lorsque la redistribution l'exige. Un thème inspiré d'Adwaita ne doit pas laisser croire qu'il est un thème officiel GNOME.

## 16. Projet final

Réalisez le projet dans cet ordre : palette claire et sombre, couleurs sémantiques, typographie, thème Shell, adaptations GTK 3 et GTK 4, vérification Libadwaita, icônes, curseurs, ressources optionnelles, tests d'états, tests d'applications, validation d'accessibilité, documentation des limites, archive et procédure de retour arrière.

Le thème est prêt à être partagé lorsque son installation est reproductible, ses limites explicites et chaque composant annoncé testé dans la version GNOME ciblée.

## 17. Références finales

- [Manuel GNOME](https://help.gnome.org/gnome-help/)
- [GNOME Shell 51.0](https://gitlab.gnome.org/GNOME/gnome-shell/-/tree/51.0)
- [GTK 3](https://docs.gtk.org/gtk3/)
- [GTK 4](https://docs.gtk.org/gtk4/)
- [Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/)
- [Mutter](https://gitlab.gnome.org/GNOME/mutter)
- [Freedesktop specifications](https://specifications.freedesktop.org/)
- [GNOME Human Interface Guidelines](https://developer.gnome.org/hig/)

Ce chapitre clôt le parcours pratique. Les chapitres précédents restent la référence détaillée de chaque moteur et composant.
