
from ultralytics import YOLO

def get_output(image_path: str) -> str:
    """
    Get the output of the model for a given image path.
    Args:
        image_path: The path to the image to run inference on.
    Returns:
        The output of the model for the given image path.
    """
    model = YOLO('weights/yolov8n.pt')

    # Run inference on an image
    results = model(image_path)

    results[0].save("img_output/output.jpg")


get_output('test.jpg')