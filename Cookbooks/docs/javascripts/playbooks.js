(() => {
  const grid = document.getElementById("playbook-grid");
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll(".playbook-card"));
  const search = document.getElementById("playbook-search");
  const filters = Array.from(document.querySelectorAll("[data-filter]"));
  const clear = document.getElementById("clear-playbook-filters");
  const results = document.getElementById("playbook-results");
  const empty = document.getElementById("playbook-empty");
  const params = new URLSearchParams(window.location.search);

  search.value = params.get("search") || "";
  filters.forEach((filter) => {
    filter.value = params.get(filter.dataset.filter) || "";
  });

  const selectedValues = (card, facet) =>
    (card.dataset[facet] || "").split(",").filter(Boolean);

  const applyFilters = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let visibleCount = 0;

    cards.forEach((card) => {
      const textMatch = !query || card.dataset.search.includes(query);
      const facetMatch = filters.every((filter) => {
        if (!filter.value) return true;
        return selectedValues(card, filter.dataset.filter).includes(filter.value);
      });
      const visible = textMatch && facetMatch;
      card.hidden = !visible;
      if (visible) visibleCount += 1;
    });

    results.textContent = `${visibleCount} of ${cards.length} playbooks`;
    empty.hidden = visibleCount !== 0;

    const next = new URLSearchParams();
    if (search.value.trim()) next.set("search", search.value.trim());
    filters.forEach((filter) => {
      if (filter.value) next.set(filter.dataset.filter, filter.value);
    });
    const queryString = next.toString();
    const url = `${window.location.pathname}${queryString ? `?${queryString}` : ""}${window.location.hash}`;
    window.history.replaceState({}, "", url);
  };

  search.addEventListener("input", applyFilters);
  filters.forEach((filter) => filter.addEventListener("change", applyFilters));
  clear.addEventListener("click", () => {
    search.value = "";
    filters.forEach((filter) => {
      filter.value = "";
    });
    applyFilters();
    search.focus();
  });

  applyFilters();
})();
