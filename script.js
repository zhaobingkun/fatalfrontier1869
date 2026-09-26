const navToggle = document.querySelector('.nav-toggle');
const siteNav = document.querySelector('.site-nav');
const main = document.querySelector('main');

const iconSvg = (body) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${body}</svg>`;

const icons = {
  menu: iconSvg('<path d="M12 3.5l1.15 1.93 2.2.32-.01 2.22 1.6 1.54-1.6 1.55.01 2.21-2.2.33L12 15.5l-1.15-1.9-2.2-.34.01-2.2-1.6-1.55 1.6-1.54-.01-2.22 2.2-.32L12 3.5Z"/><circle cx="12" cy="9.5" r="2.1"/><path d="M4.5 18.5h15M7 21h10"/>'),
  overview: iconSvg('<circle cx="12" cy="12" r="7.5"/><path d="m12 7.5 1.6 3.1 3.4.5-2.5 2.4.6 3.4-3.1-1.6-3.1 1.6.6-3.4L7 11.1l3.4-.5L12 7.5Z"/>'),
  guides: iconSvg('<path d="M5 4.5h10.5A2.5 2.5 0 0 1 18 7v12.5H7a2 2 0 0 1-2-2V4.5Z"/><path d="M18 19.5h1.5M8 8h6M8 11h6M8 14h4"/>'),
  systems: iconSvg('<circle cx="12" cy="12" r="3"/><path d="M12 3.5v2M12 18.5v2M3.5 12h2M18.5 12h2M6 6l1.4 1.4M16.6 16.6 18 18M18 6l-1.4 1.4M7.4 16.6 6 18"/>'),
  pioneers: iconSvg('<circle cx="12" cy="8" r="3"/><path d="M5.5 19c.6-3 2.8-4.5 6.5-4.5s5.9 1.5 6.5 4.5M4 5.5h3M17 5.5h3"/>'),
  updates: iconSvg('<path d="M18.5 8.5A7 7 0 1 0 19 14"/><path d="M18.5 4.5v4h-4M12 8v4l2.5 1.5"/>'),
  gold: iconSvg('<circle cx="12" cy="12" r="7"/><path d="M12 7.5v9M9.5 10c.4-1.3 4.7-1.7 5 0 .3 1.8-4.8 1.2-5 3.1-.2 1.9 4.5 1.8 5 .2"/>'),
  money: iconSvg('<path d="M5 7.5h14v9H5z"/><circle cx="12" cy="12" r="2.3"/><path d="M7.5 10h.01M16.5 14h.01"/>'),
  weapons: iconSvg('<path d="M4 17.5 15.8 5.7l2.5 2.5L6.5 20H4v-2.5Z"/><path d="m13.8 7.7 2.5 2.5M6.5 15l2.5 2.5M16.8 4.7l2.5 2.5"/>'),
  equipment: iconSvg('<path d="M7 8.5V6.8A2.8 2.8 0 0 1 9.8 4h4.4A2.8 2.8 0 0 1 17 6.8v1.7"/><path d="M5 8.5h14v11H5zM9 8.5v11M15 8.5v11M9 13h6"/>'),
  traits: iconSvg('<path d="M12 3.5 14.1 8l4.9.6-3.6 3.3.9 4.8-4.3-2.4-4.3 2.4.9-4.8L5 8.6 9.9 8 12 3.5Z"/><path d="M8 20.5h8"/>'),
  download: iconSvg('<path d="M12 4v10M8.5 10.5 12 14l3.5-3.5M5 18.5h14"/>'),
  official: iconSvg('<circle cx="12" cy="12" r="7.5"/><path d="M9 15.5h6M9.5 12h5M12 8.5v7"/>')
};

const wikiNav = [
  { title: 'Field guide', hub: '/guides/', links: [
    ['Overview', '/', 'overview'],
    ['Guides', '/guides/', 'guides'],
    ['Gameplay', '/guides/gameplay.html', 'overview'],
    ['Quests', '/quests/', 'guides'],
    ['Systems', '/systems/', 'systems'],
    ['Pioneers', '/pioneers/', 'pioneers'],
    ['Updates', '/updates/', 'updates']
  ] },
  { title: 'Reference', links: [
    ['Reviews', '/reviews/', 'overview'],
    ['Is it legit?', '/reviews/is-fatal-frontier-1869-legit.html', 'official'],
    ['Cost & free', '/guides/is-fatal-frontier-1869-free.html', 'money'],
    ['Earn money guide', '/money/how-to-make-money.html', 'gold'],
    ['Gold & loot', '/systems/gold-and-loot.html', 'gold'],
    ['Claims & Skill Check', '/systems/claims-and-skill-check.html', 'gold'],
    ['Greenbacks', '/systems/greenbacks.html', 'money'],
    ['Payout methods', '/money/payout-methods.html', 'money']
  ] },
  { title: 'Gear', links: [
    ['Weapons', '/weapons/', 'weapons'],
    ['Tools & equipment', '/systems/tools-and-equipment.html', 'equipment'],
    ['Traits & loadouts', '/systems/traits-and-loadouts.html', 'traits']
  ] },
  { title: 'Frontier access', links: [
    ['Download & Early Access', '/guides/download-and-early-access.html', 'download'],
    ['Launcher fixes', '/guides/launcher-troubleshooting.html', 'systems'],
    ['About this Wiki', '/about.html', 'official'],
    ['Privacy', '/privacy.html', 'official'],
    ['Contact', '/contact.html', 'official'],
    ['Download the game ↗', 'https://www.fatalfrontier.com/lpdownload', 'download', 'download-link'],
    ['Official site ↗', 'https://www.fatalfrontier.com/', 'official']
  ] }
];

const normalizePath = (path) => {
  if (path === '/index.html' || path === '') return '/';
  return path.replace(/index\.html$/, '');
};

const renderWikiNav = () => {
  if (!siteNav) return;
  const heading = `<div class="nav-heading"><span class="nav-heading-icon">${icons.menu}</span><span><strong>Menu</strong><small>Fatal Frontier Wiki</small></span></div>`;
  siteNav.innerHTML = heading + wikiNav.map((group) => `<div class="nav-group">${group.hub ? `<a class="nav-group-title nav-group-hub" href="${group.hub}" data-view-link><span>${group.title}</span></a>` : `<span class="nav-group-title">${group.title}</span>`}${group.links.map(([label, href, iconName, className = '']) => {
    const external = href.startsWith('http');
    return `<a class="${className}" href="${href}"${external ? ' target="_blank" rel="nofollow noopener"' : ' data-view-link'}><span class="nav-icon">${icons[iconName] || icons.overview}</span><span class="nav-link-text">${label}</span></a>`;
  }).join('')}</div>`).join('');
};

const enhanceIllustrations = () => {
  if (!main) return;
  const article = main.querySelector('.article');
  if (article?.querySelector('#claims') && !article.querySelector('.article-illustration')) {
    const figure = document.createElement('figure');
    figure.className = 'article-illustration';
    figure.innerHTML = '<img src="/assets/frontier-kit.jpg" width="1200" height="800" loading="lazy" decoding="async" alt="Antique frontier field kit with a shotgun, pickaxe, compass and gold pan"><figcaption>Field kit reference: weapons, tools and a gold pan belong to the practical loop of the frontier.</figcaption>';
    article.insertBefore(figure, article.querySelector('#claims'));
  }
  const isPioneerHub = normalizePath(window.location.pathname) === '/pioneers/';
  if (isPioneerHub && !main.querySelector('.roster-illustration')) {
    const section = main.querySelector('.section');
    if (section) {
      const figure = document.createElement('figure');
      figure.className = 'roster-illustration container';
      figure.innerHTML = '<img src="/assets/pioneer-roster.jpg" width="1200" height="800" loading="lazy" decoding="async" alt="Eight anonymous Fatal Frontier 1869 pioneer roles on the frontier"><figcaption>A visual field note for the current Pioneer roster covered by this wiki.</figcaption>';
      section.parentNode.insertBefore(figure, section);
    }
  }
  const articleNav = main.querySelector('.article-nav');
  if (articleNav && pathnameStartsWithGuides(window.location.pathname) && !articleNav.querySelector('.hub-return')) {
    const hubLink = document.createElement('a');
    hubLink.className = 'hub-return';
    hubLink.href = '/guides/';
    hubLink.textContent = '← Back to Guides';
    articleNav.insertBefore(hubLink, articleNav.firstChild);
  }
};

const pathnameStartsWithGuides = (path) => normalizePath(path).startsWith('/guides/');

const setActiveNav = (path = window.location.pathname) => {
  const current = normalizePath(path);
  siteNav?.querySelectorAll('[data-view-link]').forEach((link) => {
    const linkPath = normalizePath(new URL(link.href, window.location.origin).pathname);
    const sectionMatch = linkPath !== '/' && current.startsWith(linkPath);
    if (linkPath === current || sectionMatch) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
};

const updateDocumentMeta = (doc, url) => {
  if (doc.title) document.title = doc.title;
  const description = doc.querySelector('meta[name="description"]');
  const currentDescription = document.querySelector('meta[name="description"]');
  if (description && currentDescription) currentDescription.setAttribute('content', description.content);
  const canonical = document.querySelector('link[rel="canonical"]');
  if (canonical) canonical.href = `${window.location.origin}${url.pathname}`;
};

const loadWikiView = async (url, pushState = true) => {
  if (!main) return;
  const target = new URL(url, window.location.href);
  if (target.origin !== window.location.origin) return;
  if (pushState && target.pathname === window.location.pathname && !target.hash) return;
  main.setAttribute('aria-busy', 'true');
  document.body.classList.add('is-loading-view');
  try {
    const response = await fetch(target.href, { headers: { Accept: 'text/html' } });
    if (!response.ok) throw new Error(`View request failed: ${response.status}`);
    const html = await response.text();
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const nextMain = doc.querySelector('main');
    if (!nextMain) throw new Error('No main content found');
    main.replaceChildren(...Array.from(nextMain.childNodes).map((node) => node.cloneNode(true)));
    updateDocumentMeta(doc, target);
    if (pushState) window.history.pushState({ wikiView: target.pathname }, '', `${target.pathname}${target.search}${target.hash}`);
    enhanceIllustrations();
    setActiveNav(target.pathname);
    window.scrollTo({ top: 0, behavior: 'smooth' });
    siteNav?.classList.remove('is-open');
    navToggle?.setAttribute('aria-expanded', 'false');
  } catch (error) {
    window.location.href = target.href;
  } finally {
    main.removeAttribute('aria-busy');
    document.body.classList.remove('is-loading-view');
  }
};

if (navToggle && siteNav) {
  navToggle.addEventListener('click', () => {
    const open = siteNav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(open));
  });
  renderWikiNav();
  setActiveNav();
  siteNav.addEventListener('click', (event) => {
    const link = event.target.closest('a[data-view-link]');
    if (!link) return;
    event.preventDefault();
    loadWikiView(link.href);
  });
}

enhanceIllustrations();
window.addEventListener('popstate', () => loadWikiView(window.location.href, false));
document.querySelectorAll('[data-year]').forEach((node) => { node.textContent = new Date().getFullYear(); });
