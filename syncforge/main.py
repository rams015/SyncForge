from pathlib import Path
from hashlib import sha256
from uuid import uuid4
import json
import mimetypes

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = APP_DIR / "data" / "objects"
META_FILE = APP_DIR / "data" / "metadata.json"
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="SyncForge API", version="0.1.0")


def load_metadata() -> list[dict]:
    if not META_FILE.exists():
        return []
    return json.loads(META_FILE.read_text(encoding="utf-8"))


def save_metadata(items: list[dict]) -> None:
    META_FILE.parent.mkdir(parents=True, exist_ok=True)
    META_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "ok", "service": "syncforge"}


@app.post("/files", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    # Starter implementation buffers one file. Replace with streaming/chunk uploads.
    content = await file.read()
    digest = sha256(content).hexdigest()
    object_path = DATA_DIR / digest

    if not object_path.exists():
        object_path.write_bytes(content)

    items = load_metadata()
    file_id = str(uuid4())
    items.append({
        "id": file_id,
        "filename": Path(file.filename or "upload.bin").name,
        "sha256": digest,
        "size": len(content),
        "content_type": file.content_type or mimetypes.guess_type(file.filename or "")[0],
        "storage_key": digest,
    })
    save_metadata(items)
    return {"id": file_id, "sha256": digest, "size": len(content)}


@app.get("/files")
def list_files():
    return load_metadata()


@app.get("/files/{file_id}")
def download_file(file_id: str):
    record = next((x for x in load_metadata() if x["id"] == file_id), None)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    path = DATA_DIR / record["storage_key"]
    if not path.exists():
        raise HTTPException(status_code=404, detail="Stored object missing")
    return FileResponse(path, filename=record["filename"], media_type=record.get("content_type"))
