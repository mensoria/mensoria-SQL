(() => {
  const current = document.documentElement.lang;
  const other = current === "zh-CN" ? "en" : "zh-CN";
  const leaf = location.pathname.split("/").pop() || "index.html";
  const link = document.createElement("a");
  link.id = "language-switch";
  const stableAnchor = /^#(?:n\d{3}|c\d{2}|feature-registry)$/.test(location.hash) ? location.hash : "";
  link.href = `../${other}/${leaf}${stableAnchor}`;
  link.hreflang = other;
  link.lang = other;
  link.textContent = other === "en" ? "English" : "简体中文";
  link.setAttribute("aria-label", other === "en" ? "Read this chapter in English" : "阅读本章中文版");
  const target = document.querySelector(".right-buttons") || document.querySelector("#menu-bar");
  if (target) target.prepend(link);
})();
