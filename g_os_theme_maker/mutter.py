"""Lifecycle helper for an isolated nested GNOME Shell (Mutter) session.

The nested compositor runs in its own window. It is intentionally not confused
with the in-process GTK mock preview and never changes the user's live theme.
"""
from __future__ import annotations

import shutil
import subprocess
from typing import Sequence


class NestedShellController:
    def __init__(self, command: Sequence[str] | None = None) -> None:
        self.command = list(command or ("gnome-shell", "--nested", "--wayland"))
        self.process: subprocess.Popen[bytes] | None = None

    @property
    def available(self) -> bool:
        return shutil.which(self.command[0]) is not None

    @property
    def running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def start(self) -> None:
        if self.running:
            return
        if not self.available:
            raise RuntimeError("gnome-shell est introuvable. Installe GNOME Shell pour lancer la session imbriquée.")
        self.process = subprocess.Popen(self.command, stdin=subprocess.DEVNULL)

    def stop(self) -> None:
        if self.running and self.process is not None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=2)
        self.process = None
