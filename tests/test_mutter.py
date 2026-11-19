import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from g_os_theme_maker.mutter import NestedShellController


class NestedShellControllerTests(unittest.TestCase):
    @patch("g_os_theme_maker.mutter.subprocess.Popen")
    @patch("g_os_theme_maker.mutter.shutil.which", return_value="/usr/bin/fake")
    @patch("g_os_theme_maker.mutter.subprocess.run")
    def test_starts_nested_shell_with_isolated_theme_extension(self, run, _which, popen):
        run.return_value.stdout = "GNOME Shell 50.0"
        process = popen.return_value
        process.poll.return_value = None
        controller = NestedShellController()
        controller.start("#panel { background-color: #123456; }")
        try:
            command = popen.call_args.args[0]
            env = popen.call_args.kwargs["env"]
            self.assertEqual(command[:3], ["dbus-run-session", "--", "sh"])
            extension = (
                Path(env["XDG_DATA_HOME"])
                / "gnome-shell"
                / "extensions"
                / "g-os-theme-preview@local"
            )
            self.assertIn("#123456", (extension / "gnome-shell.css").read_text())
            self.assertTrue((extension / "metadata.json").is_file())
            self.assertTrue((extension / "extension.js").is_file())
            self.assertIn("enabled-extensions", command[3])
            self.assertIn("--devkit", command[3])
            self.assertTrue(Path(env["DCONF_PROFILE"]).is_file())
        finally:
            controller.stop()
        process.terminate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
