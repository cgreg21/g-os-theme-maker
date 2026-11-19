#!/usr/bin/env python3
"""Validate local documentation images, links and exported chapter inventory."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "gnome-51"
BUILD_SCRIPT = ROOT / "scripts" / "build-docs.sh"
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$"
)
HTML_TABLE_RE = re.compile(r"<\s*/?\s*table\b", re.IGNORECASE)
ALLOWED_IMAGES = {".png", ".jpg", ".jpeg"}


def markdown_lines(path: Path):
    """Yield lines outside fenced code blocks and reject unclosed fences."""
    fence_char = None
    fence_length = 0
    opening_line = None

    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence_char is None:
            if opening:
                marker, info = opening.groups()
                if marker[0] == "`" and "`" in info:
                    raise ValueError(
                        f"{path}:{number}: métadonnées de bloc à backticks invalides"
                    )
                fence_char = marker[0]
                fence_length = len(marker)
                opening_line = number
                continue
            yield number, line
            continue

        closing = re.match(
            r"^ {0,3}" + re.escape(fence_char) +
            r"{" + str(fence_length) + r",}[ \t]*$",
            line,
        )
        if closing:
            fence_char = None
            fence_length = 0
            opening_line = None

    if fence_char is not None:
        raise ValueError(
            f"{path}:{opening_line}: bloc de code non refermé avant la fin du fichier"
        )


def code_blocks(path: Path):
    """Yield fenced code block contents for API-specific example checks."""
    fence_char = None
    fence_length = 0
    block_lines = []

    for line in path.read_text(encoding="utf-8").splitlines():
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence_char is None:
            if opening:
                marker, _ = opening.groups()
                fence_char = marker[0]
                fence_length = len(marker)
                block_lines = []
            continue

        closing = re.match(
            r"^ {0,3}" + re.escape(fence_char) +
            r"{" + str(fence_length) + r",}[ \t]*$",
            line,
        )
        if closing:
            yield "\n".join(block_lines)
            fence_char = None
            fence_length = 0
            block_lines = []
        else:
            block_lines.append(line)

def main() -> int:
    errors = []
    markdown_files = sorted(DOCS.glob("*.md"))
    expected_chapters = {
        path.relative_to(ROOT).as_posix()
        for path in markdown_files
        if path.name != "README.md"
    }

    build_text = BUILD_SCRIPT.read_text(encoding="utf-8")
    source_block = re.search(r"SOURCE_FILES=\((.*?)\)", build_text, re.S)
    if not source_block:
        errors.append("SOURCE_FILES introuvable dans scripts/build-docs.sh")
    else:
        source_entries = re.findall(
            r"docs/gnome-51/[A-Za-z0-9._/-]+\.md", source_block.group(1)
        )
        included = set(source_entries)
        missing = sorted(expected_chapters - included)
        duplicates = sorted(
            path for path in included if source_entries.count(path) > 1
        )
        if missing:
            errors.append(
                "Chapitres absents des exports PDF/EPUB : " + ", ".join(missing)
            )
        if duplicates:
            errors.append(
                "Chapitres inclus plusieurs fois dans les exports : "
                + ", ".join(duplicates)
            )

    image_directory = DOCS / "images"
    if image_directory.exists():
        vector_images = sorted(image_directory.rglob("*.svg"))
        if vector_images:
            errors.append(
                "Illustrations SVG interdites : "
                + ", ".join(str(p.relative_to(ROOT)) for p in vector_images)
            )

    for document in markdown_files:
        for block in code_blocks(document):
            if re.search(
                r"St\.BoxLayout\s*\(\s*\{[^}]*\bvertical\s*:",
                block,
                re.S,
            ):
                errors.append(
                    f"{document.relative_to(ROOT)}: propriété St.BoxLayout.vertical "
                    "supprimée dans GNOME Shell 51 ; utiliser orientation"
                )

        try:
            visible_lines = list(markdown_lines(document))
        except ValueError as error:
            errors.append(str(error))
            continue
        for number, line in visible_lines:
            if TABLE_SEPARATOR_RE.match(line):
                errors.append(
                    f"{document.relative_to(ROOT)}:{number}: tableau Markdown interdit"
                )

            without_inline_code = re.sub(r"`+.*?`+", "", line)
            if HTML_TABLE_RE.search(without_inline_code):
                errors.append(
                    f"{document.relative_to(ROOT)}:{number}: tableau HTML interdit"
                )

            for match in IMAGE_RE.finditer(line):
                target = match.group(1).split()[0].strip("<>")
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("//"):
                    errors.append(
                        f"{document.relative_to(ROOT)}:{number}: image externe interdite ({target})"
                    )
                    continue
                image_path = (document.parent / target).resolve()
                if not image_path.is_relative_to(DOCS.resolve()):
                    errors.append(
                        f"{document.relative_to(ROOT)}:{number}: image hors du dossier documentaire ({target})"
                    )
                    continue
                if image_path.suffix.lower() not in ALLOWED_IMAGES:
                    errors.append(
                        f"{document.relative_to(ROOT)}:{number}: image non PNG/JPG ({target})"
                    )
                elif not image_path.is_file():
                    errors.append(
                        f"{document.relative_to(ROOT)}:{number}: image locale introuvable ({target})"
                    )

            for match in LINK_RE.finditer(line):
                raw_target = match.group(1).strip()
                if raw_target.startswith("<") and ">" in raw_target:
                    target = raw_target[1:raw_target.find(">")]
                else:
                    target = raw_target.split()[0] if raw_target else ""
                if not target or target.startswith("#"):
                    continue
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("//"):
                    continue
                local_target = target.split("#", 1)[0].split("?", 1)[0]
                if not local_target:
                    continue
                linked_path = (document.parent / local_target).resolve()
                if not linked_path.is_relative_to(ROOT.resolve()):
                    errors.append(
                        f"{document.relative_to(ROOT)}:{number}: lien local hors du dépôt ({target})"
                    )
                elif not linked_path.is_file():
                    errors.append(
                        f"{document.relative_to(ROOT)}:{number}: lien local introuvable ({target})"
                    )

    if errors:
        print("\n".join(f"ERREUR: {error}" for error in errors), file=sys.stderr)
        return 1

    print(
        f"Documentation valide : {len(markdown_files)} fichiers Markdown, "
        "chapitres exportés, liens locaux et images PNG/JPG locales."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
