"""Versioned theme document and design-token model."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass
class ThemeTokens:
    name: str = "Nouveau thème"
    background: str = "#242424"
    surface: str = "#303030"
    foreground: str = "#f6f5f4"
    muted: str = "#c0bfbc"
    accent: str = "#3584e4"
    border: str = "#454545"
    radius: int = 12
    spacing: int = 8
    font_size: int = 14
    component_overrides: dict[str, dict[str, int]] = field(default_factory=dict)

    def validate(self) -> None:
        for key in ("background", "surface", "foreground", "muted", "accent", "border"):
            value = getattr(self, key)
            if not isinstance(value, str) or len(value) not in (4, 7) or not value.startswith("#"):
                raise ValueError(f"Couleur invalide pour {key}: {value!r}")
            try:
                int(value[1:], 16)
            except ValueError as exc:
                raise ValueError(f"Couleur invalide pour {key}: {value!r}") from exc
        if not 0 <= self.radius <= 48:
            raise ValueError("Le rayon doit être compris entre 0 et 48.")
        if not 0 <= self.spacing <= 32:
            raise ValueError("L'espacement doit être compris entre 0 et 32.")
        if not 8 <= self.font_size <= 32:
            raise ValueError("La taille de police doit être comprise entre 8 et 32.")
        allowed = {"topbar", "card", "primary_button", "secondary_button"}
        limits = {"radius": (0, 48), "spacing": (0, 32)}
        for component, values in self.component_overrides.items():
            if component not in allowed or not isinstance(values, dict):
                raise ValueError(f"Composant invalide : {component}")
            for key, value in values.items():
                if key not in limits or not isinstance(value, int) or not limits[key][0] <= value <= limits[key][1]:
                    raise ValueError(f"Valeur invalide pour {component}.{key}")


@dataclass
class ThemeDocument:
    schema_version: int = 1
    tokens: ThemeTokens = field(default_factory=ThemeTokens)

    def to_json(self) -> str:
        self.tokens.validate()
        return json.dumps({"schema_version": self.schema_version, "tokens": asdict(self.tokens)}, indent=2, ensure_ascii=False) + "\n"

    @classmethod
    def from_json(cls, source: str) -> "ThemeDocument":
        raw: dict[str, Any] = json.loads(source)
        if raw.get("schema_version") != 1:
            raise ValueError("Version de projet non prise en charge.")
        tokens = ThemeTokens(**raw["tokens"])
        tokens.validate()
        return cls(schema_version=1, tokens=tokens)

    def save(self, path: str | Path) -> None:
        Path(path).write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "ThemeDocument":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))
