(() => {
  // Edit this list to update every header. Set footer: true for footer links.
  const navigationItems = [
    { label: "Home", href: "index.html" },
    { label: "About", href: "about.html", footer: true },
    { label: "Projects", href: "projects.html", footer: true },
    { label: "Team", href: "team.html", footer: true },
    { label: "Contact", href: "contact.html", footer: true },
    { label: "Apps", href: "index.html#apps" },
  ];

  // Resolve from this script, not the page depth or the domain root.
  // This also supports GitHub Pages subpaths and direct HTML file previews.
  const siteRoot = new URL("../", document.currentScript.src);
  const pagePath = (url) => url.pathname.replace(/\/$/, "/index.html");

  document.querySelectorAll("nav[data-navigation]").forEach((nav) => {
    const items = nav.dataset.navigation === "footer"
      ? navigationItems.filter((item) => item.footer)
      : navigationItems;
    const links = items.map((item) => {
      const link = document.createElement("a");
      link.href = new URL(item.href, siteRoot).href;
      link.textContent = item.label;
      return link;
    });
    nav.replaceChildren(...links);
  });

  const updateActiveLink = () => {
    const current = new URL(window.location.href);
    const links = [...document.querySelectorAll('nav[data-navigation="primary"] a')];
    const matchesPage = (link) => pagePath(new URL(link.href)) === pagePath(current);
    // A matching section takes precedence over its containing page.
    const active = links.find((link) => matchesPage(link)
      && new URL(link.href).hash && new URL(link.href).hash === current.hash)
      || links.find((link) => matchesPage(link) && !new URL(link.href).hash);
    links.forEach((link) => {
      if (link === active) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  };

  updateActiveLink();
  window.addEventListener("hashchange", updateActiveLink);
  window.addEventListener("pageshow", updateActiveLink);
})();
