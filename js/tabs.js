// Sub-tabs: show one .tab-panel at a time. The open tab is kept in the URL hash, and links to a
// section inside a tab (e.g. #part2-4) open that tab.
(function () {
  const links = [...document.querySelectorAll(".sub-tabs a")];
  const panels = [...document.querySelectorAll(".tab-panel")];
  if (!panels.length) return;

  function show(id, scroll) {
    panels.forEach((p) => p.classList.toggle("active", p.id === id));
    links.forEach((a) => a.classList.toggle("current", a.dataset.tab === id));
    if (scroll) document.querySelector(".sub-tabs").scrollIntoView({ behavior: "smooth" });
  }

  function fromHash() {
    const target = location.hash && document.querySelector(location.hash);
    const panel = target && (target.classList.contains("tab-panel") ? target : target.closest(".tab-panel"));
    show(panel ? panel.id : panels[0].id, false);
    if (target && !target.classList.contains("tab-panel")) target.scrollIntoView();
  }

  links.forEach((a) =>
    a.addEventListener("click", (e) => {
      e.preventDefault();
      history.replaceState(null, "", "#" + a.dataset.tab);
      show(a.dataset.tab, true);
    })
  );
  window.addEventListener("hashchange", fromHash);
  document.documentElement.classList.add("tabs-ready");
  fromHash();
})();
