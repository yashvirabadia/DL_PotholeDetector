from ultralytics import YOLO
import cv2
import os
from datetime import datetime

MODEL_PATH = "models/pothole_v1/weights/best.pt"
CONF_THRESHOLD = 0.4
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_model(model_path=MODEL_PATH):
    model = YOLO(model_path)
    return model


def get_severity(box_area, image_area):
    ratio = box_area / image_area
    if ratio < 0.01:
        return "Low"
    elif ratio < 0.05:
        return "Medium"
    else:
        return "High"


def detect_potholes(model, image_path, conf=CONF_THRESHOLD):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    h, w = image.shape[:2]
    image_area = h * w

    results = model.predict(source=image_path, conf=conf, save=False)
    detections = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = round(float(box.conf[0]), 3)
            box_area = (x2 - x1) * (y2 - y1)
            severity = get_severity(box_area, image_area)

            detections.append({
                "bbox": [x1, y1, x2, y2],
                "confidence": confidence,
                "severity": severity,
                "area": box_area
            })

            color = {"Low": (0, 255, 0), "Medium": (0, 165, 255), "High": (0, 0, 255)}[severity]
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            label = f"Pothole {confidence:.2f} [{severity}]"
            cv2.putText(image, label, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_name = f"pred_{timestamp}.jpg"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    cv2.imwrite(out_path, image)

    return detections, out_path


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python inference.py <image_path>")
        sys.exit(1)

    model = load_model()
    detections, out_path = detect_potholes(model, sys.argv[1])
    print(f"Potholes detected: {len(detections)}")
    for i, d in enumerate(detections, 1):
        print(f"  #{i} | Confidence: {d['confidence']} | Severity: {d['severity']}")
    print(f"Saved to: {out_path}")
