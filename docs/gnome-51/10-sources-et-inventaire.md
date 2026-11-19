# 10. Sources officielles et inventaire GNOME 51

## GNOME 51
- [Notes de version](https://release.gnome.org/51/)
- [GNOME Shell 51.0](https://github.com/GNOME/gnome-shell/tree/51.0)
- [Schéma GSettings Shell 51](https://github.com/GNOME/gnome-shell/blob/51.0/data/org.gnome.shell.gschema.xml.in)
- [Thème SCSS](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass)
- [Widgets SCSS](https://github.com/GNOME/gnome-shell/tree/51.0/data/theme/gnome-shell-sass/widgets)
- [Mutter](https://gitlab.gnome.org/GNOME/mutter)
- [GNOME Control Center](https://gitlab.gnome.org/GNOME/gnome-control-center)
- [GNOME Settings Daemon](https://gitlab.gnome.org/GNOME/gnome-settings-daemon)

## GTK / Libadwaita
- [GTK 3 CSS overview](https://docs.gtk.org/gtk3/css-overview.html)
- [GTK 3 CSS properties](https://docs.gtk.org/gtk3/css-properties.html)
- [GTK 4 CSS overview](https://docs.gtk.org/gtk4/css-overview.html)
- [GTK 4 CSS properties](https://docs.gtk.org/gtk4/css-properties.html)
- [Libadwaita styles](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/styles-and-appearance.html)
- [Libadwaita CSS variables](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/css-variables.html)

## Standards
- [Freedesktop Icon Theme](https://specifications.freedesktop.org/icon-theme/)
- [Icon Naming Specification](https://specifications.freedesktop.org/icon-naming-spec/)
- [Xcursor](https://www.x.org/releases/current/doc/libXcursor/)
- [Fontconfig](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)
- [XDG Base Directory](https://specifications.freedesktop.org/basedir-spec/latest/)
- [GNOME HIG](https://developer.gnome.org/hig/)

## Inventaire des modules de thème Shell 51

`_a11y.scss` accessibilité ; `_app-grid.scss` grille ; `_base.scss` base ; `_buttons.scss` boutons ; `_calendar.scss` calendrier ; `_check-box.scss` cases ; `_corner-ripple.scss` retour clic ; `_dash.scss` dock ; `_dialogs.scss` dialogues ; `_entries.scss` champs ; `_ibus-popup.scss` saisie ; `_keyboard.scss` clavier ; `_login-lock.scss` connexion/verrouillage ; `_looking-glass.scss` inspecteur ; `_message-list.scss` notifications ; `_misc.scss` divers ; `_notifications.scss` notifications ; `_osd.scss` OSD ; `_overview.scss` Activités ; `_panel.scss` panneau ; `_popovers.scss` menus ; `_qr-code.scss` QR ; `_quick-settings.scss` réglages ; `_screenshot.scss` capture ; `_scrollbars.scss` défilement ; `_search-entry.scss` recherche ; `_search-results.scss` résultats ; `_slider.scss` curseurs ; `_switcher-popup.scss` sélecteur fenêtres ; `_switches.scss` interrupteurs ; `_window-picker.scss` fenêtres ; `_workspace-switcher.scss` espaces ; `_workspace-thumbnails.scss` miniatures.

## Maintenir la couverture

À chaque version majeure : comparer les fichiers SCSS, schémas GSettings, notes de version, propriétés GTK, variables Libadwaita et résultats de tests. Les sélecteurs Shell ne sont pas stables ; ce catalogue 51 n'est pas une garantie pour les versions futures.
