import io
import pytest
from fastapi.testclient import TestClient

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from main import app

client = TestClient(app)

def test_health():
    """Simple health endpoint should return status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_form_page():
    """Root page should render HTML with 200 status."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_upload_image(monkeypatch):
    """Test upload image without real image processing."""

    # Change get_output to not call the real model
    monkeypatch.setattr("main.get_output", lambda a, b: None)

    # Create a fake image (can be any string - the model will not be called)
    file_data = io.BytesIO(b"fake_image_data")
    files = {"file": ("test.png", file_data, "image/png")}

    response = client.post("/upload", files=files)

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "/static/test.png" in response.text
    assert "/static/results/output_test.png" in response.text