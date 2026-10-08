const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const api = require(path.join(__dirname, '..', '..', 'assets', 'js', 'beta-cta.js'));
const ROOT = path.resolve(__dirname, '..', '..');

const IOS_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15';
const IPAD_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15';
const ANDROID_UA = 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36';
const DESKTOP_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36';

const link = (href, cta) => ({href, getAttribute: name => (name === 'data-cta' ? cta : null)});

test('device_type detection covers ios, android, desktop and unknown', () => {
  assert.equal(api.deviceType({userAgent: IOS_UA, platform: 'iPhone'}), 'ios');
  assert.equal(api.deviceType({userAgent: IPAD_UA, platform: 'MacIntel', maxTouchPoints: 5}), 'ios');
  assert.equal(api.deviceType({userAgent: ANDROID_UA, platform: 'Linux armv8l'}), 'android');
  assert.equal(api.deviceType({userAgent: DESKTOP_UA, platform: 'Win32'}), 'desktop');
  assert.equal(api.deviceType({userAgent: ''}), 'unknown');
});

test('only the exact APK and TestFlight URLs are measured', () => {
  assert.equal(api.targetOf(api.ANDROID_APK_URL), 'android');
  assert.equal(api.targetOf(api.IOS_TESTFLIGHT_URL), 'ios');
  assert.equal(api.targetOf('https://wootrex.cz/cs/#beta'), null);
  assert.equal(api.targetOf('https://apps.apple.com/app/testflight/id899247664'), null);
  assert.equal(api.targetOf('https://github.com/wlada0082/wootrex-web/releases/tag/v1.0.0-beta2'), null);
});

test('events contain exactly the four whitelisted fields', () => {
  const event = api.buildEvent(link(api.IOS_TESTFLIGHT_URL, 'platform_section'), {userAgent: IOS_UA, platform: 'iPhone'}, 'cs');
  assert.deepEqual(Object.keys(event).sort(), ['device_type', 'language', 'platform_target', 'source_cta']);
  assert.deepEqual(event, {platform_target: 'ios', language: 'cs', source_cta: 'platform_section', device_type: 'ios'});
  const android = api.buildEvent(link(api.ANDROID_APK_URL, 'hero'), {userAgent: ANDROID_UA}, 'de');
  assert.deepEqual(android, {platform_target: 'android', language: 'de', source_cta: 'hero', device_type: 'android'});
});

test('non-install targets, unknown CTA labels and languages are rejected or clamped', () => {
  assert.equal(api.buildEvent(link('#beta', 'hero'), {userAgent: DESKTOP_UA}, 'en'), null);
  assert.equal(api.buildEvent(link('#ios-beta', 'hero'), {userAgent: IOS_UA}, 'en'), null);
  assert.equal(api.buildEvent(link(api.IOS_TESTFLIGHT_URL, 'footer'), {userAgent: IOS_UA}, 'en'), null);
  const clamped = api.buildEvent(link(api.ANDROID_APK_URL, 'nav'), {userAgent: ANDROID_UA}, 'fr');
  assert.equal(clamped.language, 'cs');
});

test('published pages keep the exact beta URLs and CTA labels', () => {
  const pages = ['index.html', 'cs/index.html', 'en/index.html', 'de/index.html', 'sk/index.html', 'pl/index.html',
    'tools/templates/index.html'];
  for (const name of pages) {
    const content = fs.readFileSync(path.join(ROOT, name), 'utf8');
    assert.ok(content.includes(api.ANDROID_APK_URL), name + ' keeps the exact Beta 2 APK URL');
    assert.ok(content.includes(api.IOS_TESTFLIGHT_URL), name + ' keeps the exact TestFlight URL');
    assert.ok(content.includes('data-cta="hero"'), name + ' labels the hero CTA');
    assert.ok(content.includes('data-cta="nav"'), name + ' labels the navigation CTA');
    assert.equal((content.match(/data-cta="platform_section"/g) || []).length, 2, name + ' labels both install links');
    assert.ok(content.includes('assets/js/beta-cta.js'), name + ' loads the beta CTA script');
  }
});
