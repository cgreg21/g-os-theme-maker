#!/usr/bin/env python3
"""Validate local documentation images and the exported chapter inventory."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "gnome-51"
BUILD_SCRIPT = ROOT / "scripts" / "build-docs.sh"
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$"
)
ALLOWED_IMAGES = {".png", ".jpg", ".jpeg"}


def markdown_lines(path: Path):
    """Yield lines outside fenced code blocks."""
    fence_char = None
    fence_length = 0
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        match = re.match(r"(`{3,}|~{3,})", stripped)
        if match:
            marker = match.group(1)
            if fence_char is None:
                fence_char, fence_length = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                fence_char, fence_length = None, 0
            continue
        if fence_char is None:
            yield number, line


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
        included = set(re.findall(r"docs/gnome-51/[A-Za-z0-9._/-]+\.md", source_block.group(1)))
        missing = sorted(expected_chapters - included)
        if missing:
            errors.append("Chapitres absents des exports PDF/EPUB : " + ", ".join(missing))

    image_directory = DOCS / "images"
    if image_directory.exists():
        vector_images = sorted(image_directory.rglob("*.svg"))
        if vector_images:
            errors.append("Illustrations SVG interdites : " + ", ".join(str(p.relative_to(ROOT)) for p in vector_images))

    for document in markdown_files:
        for number, line in markdown_lines(document):
            if TABLE_SEPARATOR_RE.match(line):
                errors.append(
                    f"{document.relative_to(ROOT)}:{number}: tableau Markdown interdit"
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

    if errors:
        print("\n".join(f"ERREUR: {error}" for error in errors), file=sys.stderr)
        return 1

    print(
        f"Documentation valide : {len(markdown_files)} fichiers Markdown, "
        "chapitres exportés et images PNG/JPG locales."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
