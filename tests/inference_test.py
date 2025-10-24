import pytest
from unittest.mock import MagicMock, patch

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

import model_inference


def test_model_initialized_with_correct_path(monkeypatch):
    import importlib

    mock_yolo = MagicMock()
    monkeypatch.setitem(sys.modules, "ultralytics", MagicMock(YOLO=mock_yolo))

    importlib.reload(model_inference)
    mock_yolo.assert_called_once_with(str(model_inference.MODEL_PATH))


@patch("model_inference.model")
def test_get_output_calls_model_and_save(mock_model, tmp_path):
    """Test that get_output calls model() and then save() on results."""
    # Arrange
    image_path = tmp_path / "image.jpg"
    save_path = tmp_path / "output.jpg"
    image_path.write_bytes(b"fake_image")

    # Mock model output: model() returns iterable with one result having .save()
    mock_result = MagicMock()
    mock_model.return_value = [mock_result]

    # Act
    model_inference.get_output(str(image_path), str(save_path))

    # Assert
    mock_model.assert_called_once_with(str(image_path))
    mock_result.save.assert_called_once_with(str(save_path))


def test_model_path_exists_type():
    """Ensure MODEL_PATH is a Path and points to yolov8n.pt."""
    assert isinstance(model_inference.MODEL_PATH, type(model_inference.Path()))
    assert model_inference.MODEL_PATH.name == "yolov8n.pt"