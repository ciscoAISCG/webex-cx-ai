"""Generate MkDocs card catalogs for plugins, skills, and MCP servers."""

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote


REPO_ROOT = Path(__file__).resolve().parents[1]
GITHUB_ROOT = "https://github.com/ciscoAISCG/webex-cx-ai/tree/main"

CATALOGS = (
    {
        "key": "plugins",
        "title": "Plugins",
        "intro": "Reusable Codex plugins from the AI SCG repository. Each card opens the plugin package and its included skills.",
        "kind": "Plugin",
        "source": REPO_ROOT / "Plugins",
        "marker": "README.md",
        "github_root": "Plugins",
        "output": REPO_ROOT / "Cookbooks" / "docs" / "plugins.md",
    },
    {
        "key": "skills",
        "title": "Skills",
        "intro": "Task-focused skills for building, configuring, and operating Webex CX AI solutions. Each card opens the skill package in GitHub.",
        "kind": "Skill",
        "source": REPO_ROOT / "Skills",
        "marker": "SKILL.md",
        "github_root": "Skills",
        "output": REPO_ROOT / "Cookbooks" / "docs" / "skills.md",
    },
    {
        "key": "mcp-factory",
        "title": "MCP Factory",
        "intro": "MCP server assets and implementation notes maintained by the AI SCG team. Each card opens the server package in GitHub.",
        "kind": "MCP Server",
        "source": REPO_ROOT / "MCP Factory" / "servers",
        "marker": "README.md",
        "github_root": "MCP Factory/servers",
        "output": REPO_ROOT / "Cookbooks" / "docs" / "mcp-factory.md",
    },
)


def clean_markdown(text: str) -> str:
    """Convert a short README sentence into safe plain text."""
    text = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def title_from_folder(folder_name: str) -> str:
    return folder_name.replace("_", " ").replace("-", " ").title()


def shorten(text: str, limit: int = 280) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(" .,;") + "..."


def read_title_and_description(readme_path: Path, folder_name: str, kind: str) -> tuple[str, str]:
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    title = title_from_folder(folder_name)
    description = ""
    title_found = False

    if kind == "Skill":
        for line in lines:
            match = re.match(r"^description:\s*(.+?)\s*$", line)
            if match:
                description = clean_markdown(match.group(1))
                break

    for line in lines:
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match and not title_found:
            title = clean_markdown(match.group(1))
            title = re.sub(r"\s+(?:-|—)\s+Webex Contact Center.*$", "", title, flags=re.I)
            title = re.sub(r"^Skill:\s*", "", title, flags=re.I)
            title_found = True
            continue

        if not title_found or description:
            continue

        stripped = line.strip()
        if not stripped:
            if description:
                break
            continue
        if stripped.startswith(("#", "!", "---", "```", "|", "- ", "* ")):
            if description:
                break
            continue

        description = clean_markdown(stripped)
        break

    if not description:
        description = f"Reusable {kind.lower()} package and supporting assets."
    description = shorten(description)
    return title, description.rstrip(" .,;") + "."


def card(folder: Path, catalog: dict[str, object]) -> str:
    kind = str(catalog["kind"])
    title, description = read_title_and_description(folder / str(catalog["marker"]), folder.name, kind)
    safe_title = html.escape(title)
    safe_description = html.escape(description)
    github_root = str(catalog["github_root"])
    link = f"{GITHUB_ROOT}/{quote(github_root, safe="/")}/{quote(folder.name)}"
    link_kind = "MCP server" if kind == "MCP Server" else kind.lower()
    return f'''  <a class="catalog-card" href="{link}" target="_blank" rel="noopener">
    <span class="catalog-card__eyebrow">{html.escape(kind)}</span>
    <h2>{safe_title}</h2>
    <p>{safe_description}</p>
    <span class="catalog-card__link">Open {html.escape(link_kind)} on GitHub -&gt;</span>
  </a>'''


def generate_catalog(catalog: dict[str, object]) -> None:
    source = Path(str(catalog["source"]))
    marker = str(catalog["marker"])
    folders = sorted(
        (
            folder
            for folder in source.iterdir()
            if folder.is_dir() and not folder.name.startswith(".") and (folder / marker).exists()
        ),
        key=lambda path: path.name.lower(),
    )
    cards = "\n\n".join(card(folder, catalog) for folder in folders)
    title = str(catalog["title"])
    intro = str(catalog["intro"])
    output = Path(str(catalog["output"]))
    body = f'''<!-- Generated by scripts/generate_resource_catalogs.py. Edit the source package READMEs instead. -->
# {title}

{intro}

<div class="catalog-grid">
{cards}
</div>
'''
    output.write_text(body, encoding="utf-8", newline="\n")
    print(f"Generated {output} with {len(folders)} {str(catalog['kind']).lower()} cards.")


def main() -> None:
    for catalog in CATALOGS:
        generate_catalog(catalog)


if __name__ == "__main__":
    main()
