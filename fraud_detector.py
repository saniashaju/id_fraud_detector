import cv2
import pytesseract
import numpy as np
from utils import validate_image


def analyze_document(path):

    valid, message = validate_image(path)

    if not valid:
        return {
            "image_valid": False,
            "message": message,
            "risk_score": 100,
            "decision": "Suspicious"
        }

    img = cv2.imread(path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # OCR TEXT DETECTION
    text = pytesseract.image_to_string(gray)

    text_detected = len(text.strip()) > 10

    # BLUR DETECTION
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    # EDGE DETECTION
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges) / edges.size

    risk = 0

    if not text_detected:
        risk += 20

    if blur_score < 100:
        risk += 20

    if edge_density > 0.1:
        risk += 30

    decision = "Likely Genuine"

    if risk > 40:
        decision = "Suspicious"

    report = {
        "image_valid": True,
        "text_detected": text_detected,
        "blur_score": float(blur_score),
        "edge_density": float(edge_density),
        "risk_score": risk,
        "decision": decision
    }

    return report