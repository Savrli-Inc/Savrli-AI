from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import shutil
import uuid
import os
import json
from typing import List

# Configure storage paths (adjust to your repo layout or config)
DATA_DIR = os.getenv("RESOURCE_DATA_DIR", "data/resources")
INDEX_FILE = os.path.join(DATA_DIR, "index.json")
os.makedirs(DATA_DIR, exist_ok=True)

router = APIRouter(prefix="/api/resources", tags=["resources"])


class ResourceMeta(BaseModel):
    id: str
    filename: str
    content_type: str


def _load_index():
    if not os.path.exists(INDEX_FILE):
        return []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_index(index):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


@router.get("/list", response_model=List[ResourceMeta])
def list_resources():
    index = _load_index()
    return index


@router.post("/upload", response_model=ResourceMeta)
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file and stores metadata in index.json.
    """
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    stored_name = f"{file_id}{ext}"
    dest_path = os.path.join(DATA_DIR, stored_name)

    try:
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    index = _load_index()
    meta = {"id": file_id, "filename": stored_name, "content_type": file.content_type}
    index.append(meta)
    _save_index(index)
    return meta


@router.post("/import")
async def import_json(file: UploadFile = File(...)):
    """
    Import conversations or resources from a JSON file. Expected format: list of resource objects.
    This will save each resource to disk (if present as inline base64 or url) or just register metadata.
    For now, accepts a JSON array and appends as metadata entries.
    """
    if file.content_type not in ("application/json", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Expected a JSON file.")

    content = await file.read()
    try:
        payload = json.loads(content.decode("utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    if not isinstance(payload, list):
        raise HTTPException(status_code=400, detail="Expected a JSON array of resource metadata or conversations.")

    index = _load_index()
    created = []
    for entry in payload:
        # Basic validation: require id or generate one
        file_id = entry.get("id") or str(uuid.uuid4())
        filename = entry.get("filename") or f"{file_id}.json"
        meta = {"id": file_id, "filename": filename, "content_type": entry.get("content_type", "application/json")}
        index.append(meta)
        created.append(meta)

    _save_index(index)
    return {"imported": len(created), "items": created}


@router.get("/export")
def export_index():
    """
    Export the index.json for download.
    """
    if not os.path.exists(INDEX_FILE):
        # Return empty JSON
        return JSONResponse(content=[], status_code=200)

    return FileResponse(INDEX_FILE, media_type="application/json", filename="resources-index.json")


@router.get("/download/{resource_id}")
def download_resource(resource_id: str):
    index = _load_index()
    item = next((i for i in index if i["id"] == resource_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Resource not found")
    path = os.path.join(DATA_DIR, item["filename"])
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Stored file not found")
    return FileResponse(path, media_type=item.get("content_type", "application/octet-stream"), filename=item["filename"])
