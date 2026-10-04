// Click any gallery image to view it enlarged and centered. Click anywhere or press Esc to close.
(function () {
  const overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.innerHTML = '<img alt="" /><p class="lightbox-caption"></p>';
  document.body.appendChild(overlay);

  const big = overlay.querySelector("img");
  const caption = overlay.querySelector(".lightbox-caption");

  function close() {
    overlay.classList.remove("open");
    document.body.style.overflow = "";
  }

  document.querySelectorAll("figure img").forEach((img) => {
    img.addEventListener("click", () => {
      big.src = img.currentSrc || img.src;
      big.alt = img.alt;
      const fc = img.closest("figure").querySelector("figcaption");
      caption.innerHTML = fc ? fc.innerHTML : "";
      overlay.classList.add("open");
      document.body.style.overflow = "hidden";
    });
  });

  overlay.addEventListener("click", close);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });
})();
