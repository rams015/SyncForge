# SyncForge roadmap

- [ ] Replace JSON metadata with SQLAlchemy + PostgreSQL.
- [ ] Stream uploads to avoid loading large files into memory.
- [ ] Add chunk upload sessions and resume tokens.
- [ ] Add content-addressed deduplication with reference counts.
- [ ] Add immutable file versions and restore.
- [ ] Add conflict detection and explicit resolution policies.
- [ ] Add user authentication, authorization and per-user storage isolation.
- [ ] Add integration tests for interrupted uploads and concurrent updates.
- [ ] Add encryption-at-rest strategy and backup/restore tests.
