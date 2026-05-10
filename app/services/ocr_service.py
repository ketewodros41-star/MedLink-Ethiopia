from __future__ import annotations

import io
from collections import Counter

import cv2
import numpy as np
from PIL import Image

from app.core.metrics import metrics_registry
from app.services.text_utils import normalize_text


def _tokenize(image: np.ndarray) -> list[str]:
    # Deterministic fallback when OCR dependencies are unavailable in local/dev environments.
    mean_brightness = int(float(image.mean()))
    contrast = int(float(image.std()))
    return [f"brightness_{mean_brightness}", f"contrast_{contrast}"]


def process_prescription_image(image_bytes: bytes) -> dict:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    enhanced = cv2.equalizeHist(denoised)

    boxes: list[dict] = []
    extracted_tokens: list[str] = []
    ocr_engine = "fallback"

    try:
        import easyocr  # type: ignore

        reader = easyocr.Reader(["en"], gpu=False)
        ocr_engine = "easyocr"
        for box, text, confidence in reader.readtext(enhanced, detail=1):
            boxes.append(
                {
                    "text": text,
                    "confidence": round(float(confidence), 3),
                    "bounding_box": [[int(x), int(y)] for x, y in box],
                }
            )
            extracted_tokens.extend(text.split())
    except Exception:
        extracted_tokens = _tokenize(enhanced)

    normalized_tokens = [normalize_text(token) for token in extracted_tokens if normalize_text(token)]
    token_counts = Counter(normalized_tokens)
    candidate_medicines = [token for token, count in token_counts.items() if count >= 1][:5]
    review_required = len(boxes) == 0

    metrics_registry.incr("ocr_requests_total")
    if review_required:
        metrics_registry.incr("ocr_review_queue_total")

    return {
        "ocr_engine": ocr_engine,
        "extracted_text": " ".join(extracted_tokens).strip(),
        "bounding_boxes": boxes,
        "candidate_medicines": candidate_medicines,
        "dosage_candidates": [token for token in candidate_medicines if any(char.isdigit() for char in token)],
        "confidence_metrics": {
            "token_count": len(normalized_tokens),
            "mean_box_confidence": round(
                sum(item["confidence"] for item in boxes) / len(boxes),
                3,
            )
            if boxes
            else 0.0,
            "review_required": review_required,
        },
        "preprocessing_metadata": {
            "size": {"width": image.width, "height": image.height},
            "steps": ["rgb_convert", "grayscale", "gaussian_blur", "histogram_equalization"],
        },
        "review_status": "queued" if review_required else "auto_processed",
    }
