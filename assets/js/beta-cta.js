// Platform choice stays available through the static #beta fallback without JS.
// Anonymous beta CTA click measurement: no cookies, no IP storage, no identifiers,
// no fingerprinting. The beacon never blocks or delays the download/TestFlight link.
(() => {
  const ANDROID_APK_URL = 'https://github.com/wlada0082/wootrex-web/releases/download/v1.0.0-beta3/Wootrex-Beta3-v1.0.0.apk';
  const IOS_TESTFLIGHT_URL = 'https://testflight.apple.com/join/ztkZN4xV';
  const TRACKING_ENDPOINT = 'https://click.wootrex.cz/e/beta-click';
  const LANGUAGES = ['cs', 'en', 'de', 'sk', 'pl'];
  const SOURCES = ['hero', 'nav', 'platform_section'];

  const deviceType = nav => {
    const ua = (nav && nav.userAgent) || '';
    if (!ua) return 'unknown';
    const platform = (nav && nav.platform) || '';
    if (/iPhone|iPad|iPod/i.test(ua) ||
        ((platform === 'MacIntel' || /Macintosh/i.test(ua)) && (nav.maxTouchPoints || 0) > 1)) return 'ios';
    if (/Android/i.test(ua) || (nav.userAgentData && nav.userAgentData.platform === 'Android')) return 'android';
    return 'desktop';
  };

  const targetOf = href => href === ANDROID_APK_URL ? 'android' :
    href === IOS_TESTFLIGHT_URL ? 'ios' : null;

  // Only whitelisted fields leave the browser; the server re-validates every value.
  const buildEvent = (link, nav, lang) => {
    const platform = targetOf(link.href);
    const cta = link.getAttribute('data-cta');
    if (!platform || !SOURCES.includes(cta)) return null;
    return {
      platform_target: platform,
      language: LANGUAGES.includes(lang) ? lang : 'cs',
      source_cta: cta,
      device_type: deviceType(nav)
    };
  };

  const api = {ANDROID_APK_URL, IOS_TESTFLIGHT_URL, TRACKING_ENDPOINT, LANGUAGES, SOURCES, deviceType, targetOf, buildEvent};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document === 'undefined' || typeof navigator === 'undefined') return;

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

  // Fire-and-forget: no preventDefault, so the APK download / TestFlight page
  // opens immediately even if the beacon fails or the network is slow.
  const send = event => {
    const body = JSON.stringify(event);
    try {
      if (typeof navigator.sendBeacon === 'function' &&
          navigator.sendBeacon(TRACKING_ENDPOINT, new Blob([body], {type: 'text/plain;charset=UTF-8'}))) return;
    } catch (_) {}
    try {
      fetch(TRACKING_ENDPOINT, {method: 'POST', mode: 'no-cors', keepalive: true, credentials: 'omit',
        headers: {'Content-Type': 'text/plain;charset=UTF-8'}, body});
    } catch (_) {}
  };
  const lang = (document.documentElement.lang || '').split('-')[0];
  document.querySelectorAll('a[data-cta]').forEach(link => {
    link.addEventListener('click', () => {
      // Href is resolved at click time so the platform routing above is respected.
      const event = buildEvent(link, navigator, lang);
      if (event) send(event);
    });
  });
})();
