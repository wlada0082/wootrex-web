// Platform choice stays available through the static #beta fallback without JS.
(() => {
  const ua = navigator.userAgent || '';
  const platform = navigator.platform || '';
  const isIOS = /iPhone|iPad|iPod/i.test(ua) ||
    ((platform === 'MacIntel' || /Macintosh/i.test(ua)) && navigator.maxTouchPoints > 1);
  const isAndroid = /Android/i.test(ua) || navigator.userAgentData?.platform === 'Android';
  const selector = !isIOS && isAndroid ? '#beta a[href$=".apk"]' : null;
  const destination = isIOS ? '#ios-beta' :
    selector ? document.querySelector(selector)?.getAttribute('href') : '#beta';
  document.querySelectorAll('[data-beta-cta]').forEach(link => {
    link.setAttribute('href', destination || '#beta');
  });
})();
