"""Three-pane visual editor: library, live preview, property inspector."""
from __future__ import annotations

from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, Gio, Gtk

from .exporter import export_complete_theme, export_css, export_gnome_shell_css, export_gnome_shell_theme
from .model import ThemeDocument, ThemeTokens
from .mutter import NestedShellController


class ThemeMakerWindow(Gtk.ApplicationWindow):
    def __init__(self, application: Gtk.Application) -> None:
        super().__init__(application=application, title="G-OS Theme Maker")
        self.set_default_size(1440, 900)
        self.document = ThemeDocument()
        self.tokens = self.document.tokens
        self.project_path: Path | None = None
        self.selected_widget: Gtk.Widget | None = None
        self.selected_component: str | None = None
        self.shell = NestedShellController()
        self._provider = Gtk.CssProvider()
        self._build_ui()
        self._apply_preview()

    def _build_ui(self) -> None:
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_child(root)
        header = Gtk.HeaderBar()
        title = Gtk.Label(label="G-OS Theme Maker")
        title.add_css_class("title")
        header.set_title_widget(title)
        for label, callback in (("Ouvrir", self._open_project), ("Enregistrer", self._save_project), ("Exporter CSS", self._export_css), ("Exporter thème Shell", self._export_gnome_shell_theme), ("Exporter thème complet", self._export_complete_theme)):
            button = Gtk.Button(label=label)
            button.connect("clicked", callback)
            header.pack_start(button)
        self.set_titlebar(header)

        body = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        root.append(body)
        body.append(self._build_library())
        body.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
        body.append(self._build_preview_area())
        body.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
        body.append(self._build_inspector())

        self.status = Gtk.Label(label="Aperçu local GTK · aucun changement appliqué au bureau")
        self.status.set_xalign(0)
        self.status.set_margin_start(12)
        self.status.set_margin_top(6)
        self.status.set_margin_bottom(6)
        root.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))
        root.append(self.status)

    def _panel(self, title: str, width: int) -> Gtk.Box:
        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        panel.set_size_request(width, -1)
        panel.set_margin_top(16)
        panel.set_margin_bottom(16)
        panel.set_margin_start(14)
        panel.set_margin_end(14)
        heading = Gtk.Label(label=title)
        heading.add_css_class("heading")
        heading.set_xalign(0)
        panel.append(heading)
        return panel

    def _build_library(self) -> Gtk.Widget:
        panel = self._panel("Éléments", 190)
        for name in ("Couleurs", "Typographie", "Boutons", "Menus", "Fenêtres", "Panneaux", "Espacements"):
            item = Gtk.Button(label=name)
            item.add_css_class("flat")
            item.set_halign(Gtk.Align.FILL)
            panel.append(item)
        panel.append(Gtk.Separator())
        nested = Gtk.Button(label="▶ Lancer Mutter imbriqué")
        nested.connect("clicked", self._toggle_nested_shell)
        panel.append(nested)
        self.nested_button = nested
        panel.append(Gtk.Label(label="La session imbriquée s'ouvre dans sa propre fenêtre.", wrap=True, xalign=0))
        return panel

    def _build_preview_area(self) -> Gtk.Widget:
        area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        area.set_hexpand(True)
        area.set_margin_top(16)
        area.set_margin_bottom(16)
        area.set_margin_start(20)
        area.set_margin_end(20)
        bar = Gtk.Box(spacing=8)
        heading = Gtk.Label(label="Aperçu des composants")
        heading.add_css_class("heading")
        heading.set_hexpand(True)
        heading.set_xalign(0)
        bar.append(heading)
        bar.append(Gtk.Label(label="GTK local"))
        area.append(bar)

        canvas = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        canvas.set_hexpand(True)
        canvas.set_vexpand(True)
        canvas.set_halign(Gtk.Align.FILL)
        canvas.set_valign(Gtk.Align.FILL)
        canvas.set_margin_top(20)
        canvas.set_margin_bottom(20)
        canvas.set_margin_start(20)
        canvas.set_margin_end(20)
        canvas.add_css_class("preview-canvas")
        self.preview_canvas = canvas

        top = Gtk.Box(spacing=8)
        top.append(Gtk.Label(label="Activités"))
        top.append(Gtk.Label(label="Applications"))
        top.append(Gtk.Box(hexpand=True))
        top.append(Gtk.Label(label="19:42"))
        top.add_css_class("preview-topbar")
        self._make_selectable(top, "Barre supérieure", "topbar")
        canvas.append(top)

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        card.set_margin_top(36)
        card.set_margin_start(36)
        card.set_margin_end(36)
        card.set_halign(Gtk.Align.CENTER)
        card.set_size_request(420, -1)
        card.add_css_class("preview-card")
        self._make_selectable(card, "Carte", "card")
        card.append(Gtk.Label(label="Paramètres", css_classes=["title-2"]))
        card.append(Gtk.Label(label="Personnalisez l'apparence de votre environnement.", wrap=True))
        action = Gtk.Button(label="Bouton principal")
        action.add_css_class("suggested-action")
        action.set_halign(Gtk.Align.START)
        self._make_selectable(action, "Bouton principal", "primary_button")
        card.append(action)
        secondary = Gtk.Button(label="Action secondaire")
        secondary.set_halign(Gtk.Align.START)
        self._make_selectable(secondary, "Bouton secondaire", "secondary_button")
        card.append(secondary)
        canvas.append(card)
        area.append(canvas)
        return area

    def _build_inspector(self) -> Gtk.Widget:
        panel = self._panel("Inspecteur", 300)
        self.fields: dict[str, Gtk.Widget] = {}
        self._color_field(panel, "Arrière-plan", "background")
        self._color_field(panel, "Surface", "surface")
        self._color_field(panel, "Texte", "foreground")
        self._color_field(panel, "Texte secondaire", "muted")
        self._color_field(panel, "Accent", "accent")
        self._color_field(panel, "Bordure", "border")
        panel.append(Gtk.Separator())
        self._number_field(panel, "Arrondi", "radius", 0, 48)
        self._number_field(panel, "Espacement", "spacing", 0, 32)
        self._number_field(panel, "Taille du texte", "font_size", 8, 32)
        panel.append(Gtk.Separator())
        self.selection_label = Gtk.Label(label="Sélection : aucune", xalign=0)
        self.selection_label.set_wrap(True)
        panel.append(self.selection_label)
        self.component_properties = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.component_properties.set_visible(False)
        panel.append(self.component_properties)
        self.component_fields: dict[str, Gtk.SpinButton] = {}
        self._component_number_field("Arrondi du composant", "radius", 0, 48)
        self._component_number_field("Espacement du composant", "spacing", 0, 32)
        self.component_color_fields: dict[str, Gtk.Entry] = {}
        self._component_color_field("Fond", "background")
        self._component_color_field("Texte", "foreground")
        self._component_color_field("Bordure", "border")
        self._component_color_field("Survol", "hover")
        self._component_color_field("Actif", "active")
        return panel

    def _make_selectable(self, widget: Gtk.Widget, name: str, component: str) -> None:
        widget.add_css_class("preview-selectable")
        gesture = Gtk.GestureClick()
        gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        gesture.connect("pressed", self._on_preview_component_pressed, widget, name, component)
        widget.add_controller(gesture)

    def _on_preview_component_pressed(
        self,
        _gesture: Gtk.GestureClick,
        _press_count: int,
        _x: float,
        _y: float,
        widget: Gtk.Widget,
        name: str,
        component: str,
    ) -> None:
        if self.selected_widget is not None:
            self.selected_widget.remove_css_class("preview-selected")
        self.selected_widget = widget
        widget.add_css_class("preview-selected")
        self.selected_component = None
        self.selection_label.set_text(f"Sélection : {name}")
        self.component_properties.set_visible(True)
        values = self.tokens.component_overrides.get(component, {})
        for key, spin in self.component_fields.items():
            spin.set_value(values.get(key, getattr(self.tokens, key)))
        defaults = {
            "background": self.tokens.accent if component == "primary_button" else self.tokens.surface,
            "foreground": "#ffffff" if component == "primary_button" else self.tokens.foreground,
            "border": self.tokens.border,
            "hover": self.tokens.accent,
            "active": self.tokens.accent,
        }
        for key, entry in self.component_color_fields.items():
            entry.set_text(values.get(key, defaults[key]))
            entry.get_parent().set_visible(key not in ("hover", "active") or component.endswith("button"))
        self.selected_component = component

    def _component_number_field(self, label: str, key: str, low: int, high: int) -> None:
        row = Gtk.Box(spacing=8)
        row.append(Gtk.Label(label=label, xalign=0, hexpand=True))
        spin = Gtk.SpinButton.new_with_range(low, high, 1)
        spin.set_value(getattr(self.tokens, key))
        spin.connect("value-changed", self._on_component_number_changed, key)
        row.append(spin)
        self.component_properties.append(row)
        self.component_fields[key] = spin

    def _component_color_field(self, label: str, key: str) -> None:
        row = Gtk.Box(spacing=8)
        row.append(Gtk.Label(label=label, xalign=0, hexpand=True))
        entry = Gtk.Entry()
        entry.set_width_chars(9)
        entry.connect("changed", self._on_component_color_changed, key)
        row.append(entry)
        self.component_properties.append(row)
        self.component_color_fields[key] = entry

    def _on_component_color_changed(self, entry: Gtk.Entry, key: str) -> None:
        if self.selected_component is None:
            return
        values = self.tokens.component_overrides.setdefault(self.selected_component, {})
        values[key] = entry.get_text()
        self._apply_preview()

    def _on_component_number_changed(self, spin: Gtk.SpinButton, key: str) -> None:
        if self.selected_component is None:
            return
        values = self.tokens.component_overrides.setdefault(self.selected_component, {})
        values[key] = spin.get_value_as_int()
        self._apply_preview()

    def _color_field(self, panel: Gtk.Box, label: str, key: str) -> None:
        row = Gtk.Box(spacing=8)
        row.append(Gtk.Label(label=label, xalign=0, hexpand=True))
        entry = Gtk.Entry()
        entry.set_width_chars(9)
        entry.set_text(getattr(self.tokens, key))
        entry.connect("changed", self._on_token_changed, key)
        row.append(entry)
        panel.append(row)
        self.fields[key] = entry

    def _number_field(self, panel: Gtk.Box, label: str, key: str, low: int, high: int) -> None:
        row = Gtk.Box(spacing=8)
        row.append(Gtk.Label(label=label, xalign=0, hexpand=True))
        spin = Gtk.SpinButton.new_with_range(low, high, 1)
        spin.set_value(getattr(self.tokens, key))
        spin.connect("value-changed", self._on_number_changed, key)
        row.append(spin)
        panel.append(row)
        self.fields[key] = spin

    def _on_token_changed(self, entry: Gtk.Entry, key: str) -> None:
        setattr(self.tokens, key, entry.get_text())
        self._apply_preview()

    def _on_number_changed(self, spin: Gtk.SpinButton, key: str) -> None:
        setattr(self.tokens, key, spin.get_value_as_int())
        self._apply_preview()

    def _apply_preview(self) -> None:
        try:
            self.tokens.validate()
        except ValueError:
            return
        overrides = self.tokens.component_overrides
        topbar = overrides.get("topbar", {})
        card = overrides.get("card", {})
        primary = overrides.get("primary_button", {})
        secondary = overrides.get("secondary_button", {})
        topbar_bg = topbar.get("background", self.tokens.surface)
        topbar_fg = topbar.get("foreground", self.tokens.foreground)
        card_bg = card.get("background", self.tokens.surface)
        card_fg = card.get("foreground", self.tokens.foreground)
        card_border = card.get("border", self.tokens.border)
        primary_bg = primary.get("background", self.tokens.accent)
        primary_fg = primary.get("foreground", "#ffffff")
        secondary_bg = secondary.get("background", self.tokens.surface)
        secondary_fg = secondary.get("foreground", self.tokens.foreground)
        css = f"""
        .preview-canvas {{ background: {self.tokens.background}; color: {self.tokens.foreground}; }}
        .preview-topbar {{ background: {topbar_bg}; color: {topbar_fg}; border: 1px solid {topbar.get("border", self.tokens.border)}; padding: {topbar.get("spacing", self.tokens.spacing)}px; border-radius: {topbar.get("radius", self.tokens.radius)}px; }}
        .preview-card {{ background: {card_bg}; color: {card_fg}; border: 1px solid {card_border}; border-radius: {card.get("radius", self.tokens.radius)}px; padding: {card.get("spacing", self.tokens.spacing) * 2}px; font-size: {self.tokens.font_size}px; }}
        .preview-card button {{ background: {secondary_bg}; color: {secondary_fg}; border: 1px solid {secondary.get("border", self.tokens.border)}; border-radius: {secondary.get("radius", self.tokens.radius)}px; padding: {secondary.get("spacing", self.tokens.spacing)}px; }}\n        .preview-card button.suggested-action {{ border-radius: {primary.get("radius", self.tokens.radius)}px; padding: {primary.get("spacing", self.tokens.spacing)}px; }}
        .preview-card button.suggested-action {{ background: {primary_bg}; color: {primary_fg}; border-color: {primary.get("border", self.tokens.border)}; }}\n        .preview-card button:hover {{ background: {secondary.get("hover", self.tokens.accent)}; }}\n        .preview-card button:active {{ background: {secondary.get("active", self.tokens.accent)}; }}\n        .preview-card button.suggested-action:hover {{ background: {primary.get("hover", self.tokens.accent)}; }}\n        .preview-card button.suggested-action:active {{ background: {primary.get("active", self.tokens.accent)}; }}
        """
        css += f"""
        .preview-selectable {{ transition: outline-color 120ms ease; }}
        .preview-selected {{ outline: 2px solid {self.tokens.accent}; outline-offset: 3px; }}
        """
        self._provider.load_from_data(css.encode())
        display = Gdk.Display.get_default()
        if display:
            Gtk.StyleContext.add_provider_for_display(display, self._provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        if self.shell.running:
            self.shell.update_theme(export_gnome_shell_css(self.tokens))

    def _toggle_nested_shell(self, _button: Gtk.Button) -> None:
        try:
            if self.shell.running:
                self.shell.stop()
                self.nested_button.set_label("▶ Lancer Mutter imbriqué")
                self.status.set_text("Session Mutter imbriquée arrêtée.")
            else:
                self.shell.start(export_gnome_shell_css(self.tokens))
                self.nested_button.set_label("■ Arrêter Mutter imbriqué")
                self.status.set_text("Aperçu GNOME Shell lancé en session isolée. Les modifications du thème sont rechargées automatiquement.")
        except (RuntimeError, OSError) as exc:
            self.status.set_text(str(exc))

    def _choose_file(self, title: str, save: bool, callback) -> None:
        dialog = Gtk.FileDialog(title=title)
        action = dialog.save if save else dialog.open
        action(self, None, callback)

    def _open_project(self, _button: Gtk.Button) -> None:
        self._choose_file("Ouvrir un thème", False, self._on_project_opened)

    def _on_project_opened(self, dialog: Gtk.FileDialog, result: Gio.AsyncResult) -> None:
        try:
            file = dialog.open_finish(result)
            path = Path(file.get_path())
            self.document = ThemeDocument.load(path)
            self.tokens = self.document.tokens
            if self.selected_widget is not None:
                self.selected_widget.remove_css_class("preview-selected")
            self.selected_widget = None
            self.selected_component = None
            self.selection_label.set_text("Sélection : aucune")
            self.component_properties.set_visible(False)
            self.project_path = path
            self._sync_fields()
            self._apply_preview()
            self.status.set_text(f"Projet ouvert : {path.name}")
        except Exception as exc:
            self.status.set_text(f"Ouverture impossible : {exc}")

    def _save_project(self, _button: Gtk.Button) -> None:
        if self.project_path:
            try:
                self.document.save(self.project_path)
                self.status.set_text(f"Projet enregistré : {self.project_path.name}")
            except Exception as exc:
                self.status.set_text(str(exc))
        else:
            self._choose_file("Enregistrer le thème", True, self._on_project_saved)

    def _on_project_saved(self, dialog: Gtk.FileDialog, result: Gio.AsyncResult) -> None:
        try:
            file = dialog.save_finish(result)
            self.project_path = Path(file.get_path())
            self.document.save(self.project_path)
            self.status.set_text(f"Projet enregistré : {self.project_path.name}")
        except Exception as exc:
            self.status.set_text(f"Enregistrement impossible : {exc}")

    def _export_complete_theme(self, _button: Gtk.Button) -> None:
        dialog = Gtk.FileDialog(title="Choisir le dossier de destination")
        dialog.select_folder(self, None, self._on_complete_theme_folder_selected)

    def _on_complete_theme_folder_selected(self, dialog: Gtk.FileDialog, result: Gio.AsyncResult) -> None:
        try:
            folder = dialog.select_folder_finish(result)
            theme_dir = export_complete_theme(self.tokens, Path(folder.get_path()))
            self.status.set_text(f"Thème complet exporté : {theme_dir}")
        except Exception as exc:
            self.status.set_text(f"Export du thème complet impossible : {exc}")

    def _export_gnome_shell_theme(self, _button: Gtk.Button) -> None:
        dialog = Gtk.FileDialog(title="Choisir le dossier de destination")
        dialog.select_folder(self, None, self._on_gnome_shell_folder_selected)

    def _on_gnome_shell_folder_selected(self, dialog: Gtk.FileDialog, result: Gio.AsyncResult) -> None:
        try:
            folder = dialog.select_folder_finish(result)
            destination = Path(folder.get_path())
            theme_dir = export_gnome_shell_theme(self.tokens, destination)
            self.status.set_text(f"Thème GNOME Shell exporté : {theme_dir}")
        except Exception as exc:
            self.status.set_text(f"Export GNOME Shell impossible : {exc}")

    def _export_css(self, _button: Gtk.Button) -> None:
        dialog = Gtk.FileDialog(title="Exporter le thème CSS")
        dialog.save(self, None, self._on_css_saved)

    def _on_css_saved(self, dialog: Gtk.FileDialog, result: Gio.AsyncResult) -> None:
        try:
            file = dialog.save_finish(result)
            Path(file.get_path()).write_text(export_css(self.tokens), encoding="utf-8")
            self.status.set_text(f"CSS exporté : {file.get_path()}")
        except Exception as exc:
            self.status.set_text(f"Export impossible : {exc}")

    def _sync_fields(self) -> None:
        for key, widget in self.fields.items():
            if isinstance(widget, Gtk.Entry):
                widget.set_text(str(getattr(self.tokens, key)))
            else:
                widget.set_value(getattr(self.tokens, key))

    def do_close_request(self) -> bool:
        self.shell.stop()
        return False
