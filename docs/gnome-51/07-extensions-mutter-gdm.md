# 7. Extensions, Mutter, GDM et session

## 7.1 Extensions Shell

Une extension est du JavaScript exécuté dans GNOME Shell. Elle peut ajouter panneaux, menus, indicateurs, raccourcis et CSS. Structure courante : `metadata.json`, `extension.js`, `stylesheet.css`, éventuellement `prefs.js`, ressources et traductions. Tout signal, timer, raccourci ou nœud ajouté doit être nettoyé à la désactivation. Éviter les patches de prototypes.

## 7.2 Schéma d'extensions Shell 51

Clés : `enabled-extensions`, `disabled-extensions`, `disable-user-extensions`, `allow-extension-installation`, `disable-extension-version-validation`, `favorite-apps`, `app-picker-layout`. Une extension est identifiée par UUID ; une extension désactivée explicitement peut prévaloir sur une extension activée.

```sh
gnome-extensions list
gnome-extensions info UUID
gnome-extensions enable UUID
gnome-extensions disable UUID
```

Confirmer les sous-commandes avec `gnome-extensions --help`. Ne pas désactiver le contrôle de version comme solution normale.

## 7.3 Thème ou extension ?

| Besoin | Mécanisme |
|---|---|
| couleur, bordure, rayon, typographie | CSS |
| icône ou curseur | thème de ressources |
| ajouter indicateur ou menu | extension |
| nouveau comportement | extension |
| raccourci standard | GSettings |
| résolution / écran | Paramètres et Mutter |
| widget privé d'une application | API / préférences applicatives |
| écran GDM | configuration système distincte |

## 7.4 Mutter

Mutter gère placement des fenêtres, espaces, écrans, échelle, capture et composition. Les décorations côté client sont dessinées par GTK/Libadwaita ; les décorations côté serveur dépendent du compositeur. Résolution, fréquence, rotation, disposition et échelle ne sont pas des propriétés CSS. Les options expérimentales peuvent changer.

## 7.5 GDM

GDM est une session système distincte. Un thème dans le home utilisateur ne modifie pas automatiquement l'écran de connexion. Toute personnalisation GDM doit être une cible séparée avec sauvegarde, privilèges, test de récupération et avertissement. Ne pas remplacer les fichiers système depuis l'export utilisateur.

## 7.6 Verrouillage et autres toolkits

Le verrouillage Shell, les notifications privées, veille et écran vide relèvent de plusieurs composants et préférences. Qt, Electron, Web, SDL et applications propriétaires ont leurs moteurs. Flatpak peut isoler l'accès aux thèmes. Les extensions ajoutent leurs propres styles.
