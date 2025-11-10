from fastapi.testclient import TestClient
import os
import json
import tempfile
import sys

# Add parent directory to path to import the API
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set environment variable before importing the app
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

# Import your FastAPI app and router integration here.
# For example, if main app is in api/index.py and includes router, import app
from api.index import app  # adjust if your app path is different

client = TestClient(app)


def test_list_empty():
    r = client.get("/api/resources/list")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_upload_and_download(tmp_path):
    # create a temporary file to upload
    p = tmp_path / "sample.txt"
    p.write_text("hello world")
    with p.open("rb") as f:
        files = {"file": ("sample.txt", f, "text/plain")}
        r = client.post("/api/resources/upload", files=files)
    assert r.status_code == 200
    meta = r.json()
    assert "id" in meta

    # download
    r2 = client.get(f"/api/resources/download/{meta['id']}")
    assert r2.status_code == 200
    assert r2.content == b"hello world"


def test_import_export(tmp_path):
    # create an export file
    data = [{"id": "x1", "filename": "x1.json", "content_type": "application/json"}]
    p = tmp_path / "imp.json"
    p.write_text(json.dumps(data))

    with p.open("rb") as f:
        files = {"file": ("imp.json", f, "application/json")}
        r = client.post("/api/resources/import", files=files)
    assert r.status_code == 200
    assert r.json()["imported"] >= 1

    r2 = client.get("/api/resources/export")
    assert r2.status_code == 200
    # content is JSON
    assert r2.headers["content-type"].startswith("application/json")
