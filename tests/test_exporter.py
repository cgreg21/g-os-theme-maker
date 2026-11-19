import tempfile
import unittest

from g_os_theme_maker.exporter import export_complete_theme, export_gtk3_css, export_gtk4_css, export_libadwaita_css
from g_os_theme_maker.model import ThemeTokens


class CompleteThemeExportTests(unittest.TestCase):
    def setUp(self):
        self.tokens = ThemeTokens(name="Mon thème", accent="#ff0000")

    def test_exports_separate_gtk_targets(self):
        self.assertIn("@define-color", export_gtk3_css(self.tokens))
        self.assertIn("GTK 4.0+", export_gtk4_css(self.tokens))
        self.assertNotIn("--theme-bg", export_gtk4_css(self.tokens))
        self.assertIn("--accent-bg-color: #ff0000", export_libadwaita_css(self.tokens))

    def test_exports_complete_theme_layout(self):
        with tempfile.TemporaryDirectory() as temporary:
            theme = export_complete_theme(self.tokens, temporary)
            self.assertTrue((theme / "gnome-shell/gnome-shell.css").is_file())
            self.assertTrue((theme / "gtk-3.0/gtk.css").is_file())
            self.assertTrue((theme / "gtk-4.0/gtk.css").is_file())
            self.assertTrue((theme / "libadwaita/gtk-4.16.css").is_file())
            self.assertIn("Libadwaita", (theme / "README.md").read_text())
            self.assertIn("icônes et de curseurs ne sont pas générées", (theme / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
