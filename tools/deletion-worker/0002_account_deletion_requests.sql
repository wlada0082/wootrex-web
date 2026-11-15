CREATE TABLE account_deletion_requests (
  email TEXT PRIMARY KEY,
  id TEXT NOT NULL UNIQUE,
  created_at INTEGER NOT NULL,
  next_attempt INTEGER NOT NULL,
  lease TEXT,
  sent_at INTEGER
);
CREATE INDEX account_deletion_requests_pending
  ON account_deletion_requests(next_attempt) WHERE sent_at IS NULL;
