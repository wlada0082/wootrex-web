# Account deletion website (draft, not activated)

Companion to WOOTREX app PR 40's owner inventory and the new transactional
Supabase deletion PR. No live website deployment or real deletion is performed.

Routes: /delete-account.html redirects to /cs/delete-account.html. Full standalone
forms exist in cs/en/de/sk/pl, linked from localized and legacy privacy pages.
The locale builder and its template preserve discovery links on regeneration.
No third-party scripts/analytics run on these credential forms. CSP permits only
same-origin assets and the exact WOOTREX Supabase project. No form navigation,
credential cookies, localStorage, query-string tokens or arbitrary backend URLs.

The form requires fresh email/password login, typed DELETE and explicit consent.
Password fields are cleared before the request; tokens stay in memory only.
A failure attempts local sign-out of the temporary browser session. Repeated
submits are blocked while busy or after confirmed success. Only the exact server
account_deleted response displays completion; network ambiguity offers retry/support.

assets/account-deletion-config.json deliberately ships enabled=false and an empty
public key. The form, including credential inputs, stays disabled in this state.
Users can request deletion through the established wootrex@seznam.cz contact;
no password should be emailed, and ownership must be verified before any removal.
No mail is sent by this code or its tests.

Activation is blocked pending:
- The companion migration/Edge function's synthetic staging acceptance, including
  managed Auth compatibility, races between PKCE/reset/token refresh/deletion,
  owner isolation, CORS and old JWT rejection. Not just mocked/fixture tests.
- Review of production activation. No production app release is part of this task.
- Configure the PUBLIC sb_publishable_ key (never service-role/secret), enable the
  server feature flag and only then enable the reviewed website config.
- Existing full privacy policy content is still outdated about account availability.
  Align account processing, actual provider retention and store declarations before
  public release. This PR adds truthful deletion scope and policy discovery links;
  it does not invent provider retention periods or complete legal declarations.
- Native in-app initiation and durable owner-scoped local cleanup are not supplied
  by this website. Phone-only history/media/guest data cannot be erased remotely.

Provider operational logs and backups, prior feedback/emails, phone originals and
exports, and store subscriptions are explicitly outside this form's deletion scope.
The form explains those boundaries and does not make cancellation a prerequisite.

Tests:
  npm ci --prefix tools/test-runtime
  npm test --prefix tools/test-runtime
  node --test tools/test/beta-cta.test.cjs tools/test/update-manifest.test.cjs tools/test/training-content.test.cjs

15 new DOM/network tests use only synthetic credentials and mocked responses.
11 existing website regressions passed. Local browser preview verified the disabled
form/support path. No real sign-in, deletion, SMTP, publish or deployment was tested.
