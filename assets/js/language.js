/* Language links remain ordinary crawlable links without JavaScript. */
(() => {
  const supported = ['cs', 'en', 'de', 'sk', 'pl'];
  const key = 'wootrex.language';
  document.querySelectorAll('[data-language]').forEach(link => {
    link.addEventListener('click', () => {
      try { localStorage.setItem(key, link.dataset.language); } catch (_) {}
    });
  });
  if (!document.body.hasAttribute('data-language-entry')) return;
  let selected = null;
  try { selected = localStorage.getItem(key); } catch (_) {}
  if (!supported.includes(selected)) {
    selected = (navigator.languages || [navigator.language])
      .map(language => language.toLowerCase().split('-')[0])
      .find(language => supported.includes(language)) || 'cs';
  }
  // Only the root entry redirects; explicit localized URLs never redirect.
  // The storage key holds a language preference only, not a tracking identifier.
  const target = document.querySelector('[data-language="' + selected + '"]');
  if (target) {
    const destination = new URL(target.getAttribute('href'), location.href);
    destination.hash = location.hash;
    location.replace(destination.href);
  }
})();
