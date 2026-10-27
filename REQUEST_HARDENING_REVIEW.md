# Request and feedback hardening: review evidence

Based on published web commit961ac66 (PR7 and PR8 merged). No duplicate request
endpoint/form. Account removal still uses the prominent manual mailto request,
not Feedback API; automatic deletion stays disabled and no config/key changes.

This PR limits feedback receipts to16KiB BEFORE decoding (including chunked and
truncated bodies), checks category allowlist and254-character email boundary,
and preserves the draft with an explicit retry after malformed responses,
network timeout/outage, HTTP400/429/500. Success still requires exact201 and a
nonblank confirmed receipt. A feedback receipt is NOT operator email delivery
or account deletion confirmation. Client validation is not server anti-spam.

Tests:62 Node PASS,2 Python regeneration/idempotence PASS, diff check PASS.
The9 new tests exercise validation and network/response failures with mocked
fetch only. No real feedback, email, login or account request was submitted.
Published privacy/request pages were independently rechecked HTTPS200; feedback
endpoint GET405 only proves the endpoint responds, not POST/storage/delivery.
Existing320px all-language visual checks are inherited evidence: no HTML/CSS
or layout changes in this PR. No new claim of native-device visual verification.

Not deployed automatically. No mobile build, signature, Beta138 release manifest,
Supabase data, mail configuration or production payments changed. Manual inbox
ownership, end-to-end delivery/spam/outage tests, rate limits, exact retention,
legal operator and managed Supabase staging remain operational release gates.
See app docs/ACCOUNT_DELETION_OPERATIONS.md and docs/STORE_PRIVACY_DRAFT.md.
