from ultralytics import YOLO
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "weights" / "yolov8n.pt"
model = YOLO(str(MODEL_PATH))

def get_output(image_path: str, save_path: str) -> None:
    """
    Run YOLO inference on an image and save the annotated result.

    Args:
        image_path: Path to the input image.
        save_path: Path to save the output image.
    """
    results = model(image_path)
    for r in results:
        r.save(save_path)