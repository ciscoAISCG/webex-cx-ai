"""Generate the Playbooks index and filterable MkDocs catalog from manifests."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PLAYBOOKS_DIR = REPO_ROOT / "Playbooks"
TAXONOMY_PATH = PLAYBOOKS_DIR / "taxonomy.yaml"
INDEX_PATH = PLAYBOOKS_DIR / "README.md"
OUTPUT_PATH = REPO_ROOT / "Cookbooks" / "docs" / "playbooks.md"
GITHUB_PLAYBOOK_ROOT = "https://github.com/ciscoAISCG/webex-cx-ai/tree/main/Playbooks"
FILTER_FACETS = (
    "verticals",
    "channels",
    "features",
    "customer_journeys",
    "integrations",
    "complexity",
)
FACET_TITLES = {
    "verticals": "Vertical",
    "channels": "Channel",
    "features": "Feature",
    "customer_journeys": "Customer journey",
    "integrations": "Integration",
    "complexity": "Complexity",
}


def load_catalog() -> tuple[dict[str, object], list[dict[str, object]]]:
    taxonomy = yaml.safe_load(TAXONOMY_PATH.read_text(encoding="utf-8"))
    entries: list[dict[str, object]] = []
    for folder in sorted(PLAYBOOKS_DIR.iterdir(), key=lambda path: path.name.lower()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        manifest_path = folder / "manifest.yaml"
        readme_path = folder / "README.md"
        if not manifest_path.is_file() or not readme_path.is_file():
            continue
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("schema_version") != 2 or manifest.get("id") != folder.name:
            raise ValueError(f"{manifest_path} must use schema v2 and match its folder slug")
        entries.append(manifest)
    return taxonomy, entries


def label_for(taxonomy: dict[str, object], facet: str, value: str) -> str:
    labels = taxonomy.get("display_labels", {}).get(facet, {})
    return labels.get(value, value.replace("-", " ").title())


def labels_for(taxonomy: dict[str, object], manifest: dict[str, object], facet: str) -> list[str]:
    values = manifest.get("classification", {}).get(facet, []) or []
    return [label_for(taxonomy, facet, value) for value in values]


def render_index(taxonomy: dict[str, object], manifests: list[dict[str, object]]) -> str:
    rows: list[str] = []
    for manifest in sorted(manifests, key=lambda item: str(item["title"]).casefold()):
        slug = str(manifest["id"])
        title = str(manifest["title"])
        summary = str(manifest["summary"])
        journeys = labels_for(taxonomy, manifest, "customer_journeys")
        journey_text = ", ".join(journeys) or "—"
        rows.append(f"| [{title}]({slug}/README.md) | {summary} | {journey_text} |")
    table = "\n".join(rows)
    return f"""# Playbooks

Reusable, implementation-oriented Webex CX AI patterns. Each package includes its use-case guide and supporting assets; `manifest.yaml` supplies its searchable metadata.

Browse by searching or filtering the [website catalog](../Cookbooks/docs/playbooks.md), or open a playbook below.

| Playbook | Summary | Customer journey |
|---|---|---|
{table}

## Folder name updates

Playbook folders use lowercase kebab-case. The original underscore-based paths are visible in the repository's rename history.
"""


def render_filters(taxonomy: dict[str, object], manifests: list[dict[str, object]]) -> str:
    facet_data = taxonomy["facets"]
    rows: list[str] = []
    for facet in FILTER_FACETS:
        if facet == "complexity":
            values = facet_data[facet]
        else:
            used = {
                value
                for manifest in manifests
                for value in (manifest.get("classification", {}).get(facet, []) or [])
            }
            values = [value for value in facet_data.get(facet, []) if value in used]
        if not values:
            continue
        options = "\n".join(
            f'      <option value="{html.escape(value, quote=True)}">'
            f"{html.escape(label_for(taxonomy, facet, value))}</option>"
            for value in values
        )
        label = FACET_TITLES[facet]
        rows.append(
            f'''    <label class="playbook-filter" for="filter-{facet}">
      <span>{html.escape(label)}</span>
      <select id="filter-{facet}" data-filter="{facet}">
        <option value="">Any</option>
{options}
      </select>
    </label>'''
        )
    return "\n".join(rows)


def render_card(taxonomy: dict[str, object], manifest: dict[str, object]) -> str:
    slug = str(manifest["id"])
    classification = manifest.get("classification", {})
    fields = {
        facet: (classification.get(facet, []) or []) if facet != "complexity" else [manifest["complexity"]]
        for facet in FILTER_FACETS
    }
    search_terms = [str(manifest["title"]), str(manifest["summary"])]
    search_terms.extend(manifest.get("keywords", []) or [])
    for facet, values in fields.items():
        search_terms.extend(label_for(taxonomy, facet, value) for value in values)
    attributes = " ".join(
        f'data-{facet}="{html.escape(",".join(values), quote=True)}"'
        for facet, values in fields.items()
    )
    return f'''  <a class="playbook-card" href="{GITHUB_PLAYBOOK_ROOT}/{quote(slug)}" target="_blank" rel="noopener" {attributes} data-search="{html.escape(" ".join(search_terms).casefold(), quote=True)}">
    <span class="playbook-card__eyebrow">Playbook</span>
    <h2>{html.escape(str(manifest["title"]))}</h2>
    <p>{html.escape(str(manifest["summary"]))}</p>
    <span class="playbook-card__tags">{html.escape(" · ".join(labels_for(taxonomy, manifest, "customer_journeys")))}</span>
    <span class="playbook-card__link">Open playbook on GitHub →</span>
  </a>'''


def render_catalog(taxonomy: dict[str, object], manifests: list[dict[str, object]]) -> str:
    filters = render_filters(taxonomy, manifests)
    cards = "\n\n".join(
        render_card(taxonomy, manifest)
        for manifest in sorted(manifests, key=lambda item: str(item["title"]).casefold())
    )
    return f'''<!-- Generated by scripts/generate_playbook_catalog.py. Edit Playbooks/*/manifest.yaml. -->
# Playbooks

Search across the collection or combine filters for vertical, channel, feature, journey, integration, and complexity. Each card opens the complete playbook in the AI SCG GitHub repository.

<div class="playbook-filters" role="search" aria-label="Filter playbooks">
  <label class="playbook-filter playbook-filter--search" for="playbook-search">
    <span>Search</span>
    <input id="playbook-search" type="search" placeholder="Title, summary, or keyword" autocomplete="off">
  </label>
{filters}
  <button class="playbook-filter__clear" id="clear-playbook-filters" type="button">Clear filters</button>
</div>

<p class="playbook-results" id="playbook-results" role="status" aria-live="polite"></p>
<p id="playbook-empty" hidden>No playbooks match these filters.</p>

<div class="playbook-grid" id="playbook-grid">
{cards}
</div>
'''


def generate() -> None:
    taxonomy, manifests = load_catalog()
    INDEX_PATH.write_text(render_index(taxonomy, manifests), encoding="utf-8", newline="\n")
    OUTPUT_PATH.write_text(render_catalog(taxonomy, manifests), encoding="utf-8", newline="\n")
    print(f"Generated Playbooks/README.md and the website catalog with {len(manifests)} playbooks.")


if __name__ == "__main__":
    generate()
