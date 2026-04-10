import csv
import os
from datetime import datetime

LOG_FILE = "outputs/prediction_log.csv"


def log_prediction(image_name, pothole_count, detections):
    os.makedirs("outputs", exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Image", "Count", "Severities", "Confidences"])

        severities = [d["severity"] for d in detections]
        confidences = [str(d["confidence"]) for d in detections]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, image_name, pothole_count, "|".join(severities), "|".join(confidences)])


def get_severity_summary(detections):
    summary = {"Low": 0, "Medium": 0, "High": 0}
    for d in detections:
        summary[d["severity"]] += 1
    return summary


def image_to_base64(image_path):
    import base64
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
