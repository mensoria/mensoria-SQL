(() => {
  const preferenceKey = "mensoria-docs-language";
  const languages = ["zh-CN", "en"];
  const remember = (language) => {
    try { localStorage.setItem(preferenceKey, language); } catch { /* Storage is optional. */ }
  };

  if (document.documentElement.hasAttribute("data-docs-entry")) {
    let language = "zh-CN";
    try {
      const saved = localStorage.getItem(preferenceKey);
      if (languages.includes(saved)) language = saved;
    } catch { /* The explicit fallback link remains available. */ }
    location.replace(new URL(`${language}/index.html`, location.href).href);
    return;
  }

  const current = document.documentElement.lang;
  if (!languages.includes(current) || document.getElementById("docs-language")) return;
  const leaf = location.pathname.split("/").pop() || "index.html";
  remember(current);
  if (leaf === "index.html" || leaf === "preface.html") {
    document.body.classList.add("docs-home");
    const start = document.querySelector('main > p > a[href="01-purpose.html"]');
    if (start) {
      start.classList.add("start-reading");
      start.parentElement.classList.add("document-actions");
    }
  }

  const title = document.querySelector(".menu-title");
  if (title) {
    const home = document.createElement("a");
    home.href = "index.html";
    home.className = "docs-brand";
    home.textContent = "Mensoria SQL";
    home.setAttribute("aria-label", current === "en" ? "Documentation home" : "文档首页");
    title.replaceChildren(home);
  }

  const target = document.querySelector(".right-buttons");
  if (!target || leaf === "print.html") return;
  const label = document.createElement("label");
  label.className = "docs-language-control";
  label.htmlFor = "docs-language";
  const caption = document.createElement("span");
  caption.className = "visually-hidden";
  caption.textContent = current === "en" ? "Documentation language" : "文档语言";
  const select = document.createElement("select");
  select.id = "docs-language";
  select.name = "language";
  select.setAttribute("aria-label", caption.textContent);
  for (const language of languages) {
    const option = document.createElement("option");
    option.value = language;
    option.textContent = language === "en" ? "English" : "简体中文";
    option.lang = language;
    option.selected = language === current;
    select.append(option);
  }
  select.addEventListener("change", () => {
    const language = select.value;
    if (language === current || !languages.includes(language)) return;
    remember(language);
    const anchor = /^#(?:n\d{3}|c\d{2}|feature-registry)$/.test(location.hash) ? location.hash : "";
    location.assign(`../${language}/${leaf}${anchor}`);
  });
  label.append(caption, select);
  target.prepend(label);
})();
