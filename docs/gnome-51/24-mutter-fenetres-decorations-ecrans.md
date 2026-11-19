# Mutter, fenêtres, décorations et écrans

![Application GNOME 51 affichée dans le thème standard Adwaita](https://release.gnome.org/51/calendar-event-editor-screenshot.webp)

Mutter est le compositeur et gestionnaire de fenêtres utilisé par GNOME Shell. Il gère les fenêtres, leur placement, les espaces de travail, les écrans et la composition graphique. Le thème GNOME Shell ne contrôle pas tout ce qui apparaît autour d'une fenêtre.

## 1. Les couches à distinguer

### Décoration côté client (CSD)

Avec une décoration côté client (*Client-Side Decorations*), l'application dessine elle-même sa barre de titre et ses contrôles. Une application GTK 4 ou Libadwaita utilise souvent une barre d'en-tête intégrée. Son apparence dépend principalement du CSS de l'application et de son toolkit.

### Décoration côté serveur (SSD)

Avec une décoration côté serveur (*Server-Side Decorations*), le gestionnaire de fenêtres fournit une partie de la décoration. Le rendu dépend du protocole, du compositeur et de l'application. Un thème GTK ne modifie pas nécessairement une décoration SSD.

### GNOME Shell

Le Shell dessine le panneau, la vue Activités, les menus, les OSD, les dialogues du Shell et certaines interfaces de gestion des fenêtres. Ces éléments utilisent le thème Shell.

### Mutter

Mutter gère le placement, les tailles, les contraintes, les espaces de travail, les moniteurs et la composition. Une grande partie de ce comportement n'est pas une propriété CSS.

## 2. Identifier le propriétaire d'un élément

Avant d'écrire une règle, observez l'élément :

- barre de titre et boutons intégrés à l'application : probablement CSD ;
- bordure et barre de titre autour de la surface applicative : possiblement SSD ;
- panneau, vue Activités ou Alt-Tab : GNOME Shell ;
- position, taille, espace de travail ou sortie écran : Mutter ou réglages d'affichage.

Identifiez le processus et le moteur qui dessinent l'élément. Un sélecteur CSS n'est utile que si la feuille de style correspondante est chargée par ce moteur.

## 3. Personnaliser une barre d'en-tête GTK

Pour une application GTK 4, inspectez la barre d'en-tête avec GTK Inspector. Exemple de règles pour une application qui utilise les classes GTK standard :

```css
headerbar {
  min-height: 42px;
  padding: 4px 8px;
}

headerbar button {
  border-radius: 999px;
}

headerbar .title {
  font-weight: 700;
}
```

Cet exemple concerne GTK, pas Mutter. Certaines applications ajoutent leurs propres classes ou dessinent une barre personnalisée. Pour Libadwaita, respectez ses variables sémantiques et vérifiez séparément les variantes claire et sombre.

## 4. Aperçus de fenêtres dans le Shell

Les aperçus de la vue Activités et du sélecteur Alt-Tab sont des acteurs du Shell, pas les fenêtres originales. Les modifier ne change pas la taille réelle de la fenêtre.

Consultez [Vue Activités](14-vue-activites-overview.md), [OSD, dialogues et Alt-Tab](17-osd-dialogues-alt-tab-capture.md) et [Inspection CSS](12-inspection-et-diagnostic-css.md).

## 5. Espaces de travail et réglages Mutter

Listez les schémas disponibles :

```bash
gsettings list-schemas | grep -E 'mutter|wm|desktop.wm'
gsettings list-recursively org.gnome.mutter
```

Toutes les clés ne sont pas présentes sur toutes les distributions. Certaines options peuvent être expérimentales ou réservées à une version particulière. Avant de modifier une clé, lisez sa description :

```bash
gsettings describe org.gnome.mutter nom-de-cle
```

Remplacez le nom fictif par une clé réellement listée sur votre système. Ne modifiez pas une préférence dont vous ne connaissez pas l'effet.

## 6. Écrans, HiDPI et mise à l'échelle

La taille visuelle dépend de la résolution physique, du facteur d'échelle logique, de la mise à l'échelle fractionnaire, des métriques du toolkit, de la taille de police et des dimensions minimales du composant.

Un bouton trop petit sur un écran HiDPI n'a pas nécessairement besoin d'une règle CSS plus grande. Vérifiez d'abord l'échelle du bureau et la taille logique du composant.

Testez au minimum un écran standard, un écran HiDPI, une mise à l'échelle fractionnaire si disponible, un écran externe et le déplacement d'une fenêtre entre deux écrans.

## 7. Wayland et X11

Wayland et X11 n'exposent pas les mêmes mécanismes de gestion des fenêtres. Sous Wayland, le compositeur contrôle les surfaces et la session. Sous X11, certains outils historiques peuvent interroger ou modifier plus largement les fenêtres.

Un thème CSS peut rester identique, mais le comportement des fenêtres et de certaines extensions peut différer. Testez les deux sessions si votre distribution les propose. Ne transposez pas automatiquement un résultat observé sous X11 à Wayland.

## 8. Bordures et ombres

Les ombres peuvent provenir du toolkit, des décorations CSD, de Mutter, des aperçus Shell ou d'un effet propre à l'application. Modifier une ombre GTK n'agit pas sur une ombre dessinée par Mutter. Modifier le thème Shell n'altère pas nécessairement les ombres des applications.

Supprimer toutes les ombres peut rendre les fenêtres difficiles à distinguer sur un fond uniforme. Identifiez leur propriétaire et conservez une séparation visuelle suffisante.

## 9. Dépannage

### Les boutons de titre ne changent pas

Vérifiez si la fenêtre utilise une CSD et inspectez son CSS. Les boutons peuvent avoir des classes propres à l'application.

### Les fenêtres ne se redimensionnent plus

Retirez les règles qui imposent des dimensions minimales ou fixes excessives. Le CSS ne doit pas empêcher le toolkit de respecter les contraintes de fenêtre.

### Les tailles varient entre deux écrans

Vérifiez l'échelle et les métriques logiques. Ne corrigez pas un problème d'échelle globale en ajoutant une taille fixe à chaque composant.

### Le résultat diffère sous Wayland

Identifiez les fonctions dépendantes du gestionnaire de fenêtres et des protocoles. Testez dans la session réellement ciblée.

## 10. Exercices

1. Ouvrez une application GTK 4 et inspectez sa barre d'en-tête.
2. Ouvrez la vue Activités et Alt-Tab pour distinguer les aperçus Shell des fenêtres réelles.
3. Comparez le rendu sur deux facteurs d'échelle.
4. Si Wayland et X11 sont disponibles, comparez la gestion des fenêtres sans modifier les réglages système.

## 11. Sources officielles

- [Mutter — code source](https://gitlab.gnome.org/GNOME/mutter)
- [Mutter — documentation](https://mutter.gnome.org/)
- [GNOME Shell 51.0](https://gitlab.gnome.org/GNOME/gnome-shell/-/tree/51.0)
- [GTK 4 — CSS overview](https://docs.gtk.org/gtk4/css-overview.html)
- [GTK 3 — CSS overview](https://docs.gtk.org/gtk3/css-overview.html)
- [Libadwaita — styles et apparence](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)
- [Wayland — documentation](https://wayland.freedesktop.org/)

Mutter n'est pas un moteur CSS. Ne cherchez pas un sélecteur pour une fonction de placement, de composition ou de protocole qui n'est pas dessinée par GTK ou GNOME Shell.
