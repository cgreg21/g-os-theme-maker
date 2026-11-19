"""GTK4 application entry point."""
from __future__ import annotations

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk

from .model import ThemeDocument
from .window import ThemeMakerWindow


class ThemeMakerApplication(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(application_id="fr.cgreg21.GOSThemeMaker", flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

    def do_activate(self) -> None:
        window = self.props.active_window
        if window is None:
            window = ThemeMakerWindow(application=self)
        window.present()


def main() -> None:
    ThemeMakerApplication().run(None)
