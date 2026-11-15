import json
from pathlib import Path
import shutil
import sys

assets = Path(__file__).resolve().parent
root = Path(sys.argv[1]).resolve(strict=True)
worker = root / 'src/worker.js'
config = root / 'wrangler.json'
source = worker.read_text(encoding='utf-8')
settings = json.loads(config.read_text(encoding='utf-8'))
if settings['name'] != 'wootrex-feedback-api' or settings['main'] != 'src/worker.js':
    raise SystemExit('Expected existing WOOTREX feedback worker')
route = '    const origin=request.headers.get("Origin");'
entry = 'export default {\n  async fetch(request,env) {'
if source.count(route) != 1 or source.count(entry) != 1 or 'deletionRequest' in source:
    raise SystemExit('Unexpected Worker source or integration already applied')
if settings.get('send_email') or settings.get('triggers') or any(
    limit['namespace_id'] == '10043' for limit in settings['ratelimits']
):
    raise SystemExit('Existing email, schedule or namespace requires review')
source = ("import { deletionRequest, sendPendingRequests } from './account-deletion.mjs';\n"
          + source.replace(entry, 'export default {\n'
            '  async scheduled(_event, env) { await sendPendingRequests(env); },\n'
            '  async fetch(request,env) {')
          .replace(route, '    if (new URL(request.url).pathname === "/account-deletion-requests") {\n'
                           '      return deletionRequest(request, env);\n    }\n' + route))
settings['send_email'] = [{'name': 'DELETION_EMAIL', 'destination_address': 'wootrex@seznam.cz'}]
settings['triggers'] = {'crons': ['*/5 * * * *']}
settings['ratelimits'].append({'name': 'DELETION_RATE_LIMITER', 'namespace_id': '10043',
                               'simple': {'limit': 5, 'period': 60}})
for original, target in [('account-deletion.mjs', 'src/account-deletion.mjs'),
                         ('0002_account_deletion_requests.sql', 'migrations/0002_account_deletion_requests.sql')]:
    if (root / target).exists():
        raise SystemExit(f'Unexpected existing file {target}')
for original, target in [('account-deletion.mjs', 'src/account-deletion.mjs'),
                         ('0002_account_deletion_requests.sql', 'migrations/0002_account_deletion_requests.sql')]:
    shutil.copyfile(assets / original, root / target)
worker.write_text(source, encoding='utf-8')
config.write_text(json.dumps(settings, indent=2) + '\n', encoding='utf-8')
