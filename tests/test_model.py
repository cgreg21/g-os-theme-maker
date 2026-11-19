import tempfile
import unittest

from g_os_theme_maker.exporter import export_css, export_gnome_shell_css, export_gnome_shell_theme
from g_os_theme_maker.model import ThemeDocument, ThemeTokens


class ThemeModelTests(unittest.TestCase):
    def test_json_round_trip(self):
        document = ThemeDocument(tokens=ThemeTokens(name="Test", accent="#ff0000"))
        restored = ThemeDocument.from_json(document.to_json())
        self.assertEqual(restored.tokens.name, "Test")
        self.assertEqual(restored.tokens.accent, "#ff0000")

    def test_component_overrides_round_trip(self):
        tokens = ThemeTokens(component_overrides={"card": {"radius": 20, "spacing": 12}})
        restored = ThemeDocument.from_json(ThemeDocument(tokens=tokens).to_json())
        self.assertEqual(restored.tokens.component_overrides["card"], {"radius": 20, "spacing": 12})

    def test_component_color_overrides_export(self):
        tokens = ThemeTokens(component_overrides={"primary_button": {"background": "#123456", "hover": "#abcdef"}})
        css = export_css(tokens)
        self.assertIn(".gom-primary-button", css)
        self.assertIn("background-color: #123456;", css)
        self.assertIn("background-color: #abcdef;", css)

    def test_rejects_invalid_component_color(self):
        with self.assertRaises(ValueError):
            ThemeTokens(component_overrides={"card": {"background": "invalid"}}).validate()

    def test_rejects_invalid_component_override(self):
        with self.assertRaises(ValueError):
            ThemeTokens(component_overrides={"card": {"radius": 99}}).validate()

    def test_rejects_unsupported_schema(self):
        with self.assertRaises(ValueError):
            ThemeDocument.from_json('{"schema_version": 99, "tokens": {}}')

    def test_rejects_invalid_color(self):
        with self.assertRaises(ValueError):
            ThemeTokens(background="not-a-color").validate()

    def test_css_export_contains_tokens(self):
        css = export_css(ThemeTokens(accent="#123456", radius=16))
        self.assertIn("@define-color gom_accent #123456;", css)
        self.assertIn("border-radius: 16px", css)

    def test_gnome_shell_css_uses_theme_tokens(self):
        css = export_gnome_shell_css(ThemeTokens(background="#111111", accent="#abcdef"))
        self.assertIn("#panel", css)
        self.assertIn("background-color: #111111;", css)
        self.assertIn("background-color: #abcdef;", css)
        self.assertIn(".popup-menu-content", css)

    def test_gnome_shell_theme_export_creates_installable_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            theme_dir = export_gnome_shell_theme(ThemeTokens(name="My Theme"), directory)
            self.assertEqual(theme_dir.name, "My-Theme")
            self.assertTrue((theme_dir / "gnome-shell" / "gnome-shell.css").is_file())
            self.assertTrue((theme_dir / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
