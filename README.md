# SyncForge — Distributed File Synchronization & Backup System

Starter scaffold for a multi-client file-sync service. This is a foundation, not a production-ready backup product.

## Initial scope
- FastAPI service with client registration placeholder and file upload/download.
- SHA-256 content integrity verification.
- SQLite metadata store for a quick local start (replace with PostgreSQL for deployment).
- Chunk/resumable upload, deduplication, versioning and conflict resolution are planned milestones.

## Run locally
```bash
cd SyncForge
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -e .
uvicorn syncforge.main:app --reload
```
Open `http://127.0.0.1:8000/docs`.

## Current API
- `GET /health`
- `POST /files` — upload a file; server computes SHA-256 and stores it.
- `GET /files` — list stored file metadata.
- `GET /files/{file_id}` — download a stored file.

## Suggested build milestones
1. Implement chunk IDs, chunk upload sessions and resumable upload state.
2. Add content-addressed storage and deduplication.
3. Add file versions and restore endpoints.
4. Add client sync manifests and conflict detection (mtime is not enough; use version/vector metadata).
5. Add authenticated clients, per-user namespaces, quotas and audit logs.
6. Add PostgreSQL, background jobs, tests, metrics and deployment hardening.

## Important
Do not use this as your only backup. Add authentication, authorization, encryption at rest, retention policy, and tested restore procedures before real use.
