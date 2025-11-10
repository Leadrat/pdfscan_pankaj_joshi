import cv2
import numpy as np
import os

PROCESSED_DIRNAME = "processed"


def ensure_processed_dir(images_root: str) -> str:
    out_dir = os.path.join(images_root, PROCESSED_DIRNAME)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def preprocess_image(path: str) -> np.ndarray:
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Failed to read image: {path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Resize for better OCR if too small
    h, w = gray.shape[:2]
    if max(h, w) < 1024:
        scale = 1024 / max(h, w)
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
    # Denoise
    den = cv2.fastNlMeansDenoising(gray, h=7)
    # Threshold
    thr = cv2.threshold(den, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Morph open
    kernel = np.ones((2, 2), np.uint8)
    morph = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=1)
    # CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    res = clahe.apply(morph)
    return res


def save_processed(image: np.ndarray, images_root: str, filename: str) -> str:
    out_dir = ensure_processed_dir(images_root)
    out_path = os.path.join(out_dir, filename)
    cv2.imwrite(out_path, image)
    return out_path
