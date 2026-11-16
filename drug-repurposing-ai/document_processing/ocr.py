"""OCR pipeline using Tesseract and OpenCV.

Preprocesses medical document images (grayscale, denoise, deskew, binarize)
then runs Tesseract OCR to extract text.
"""

import io
import logging
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# Tesseract command path — set from config at runtime
_tesseract_cmd: Optional[str] = None


def configure_tesseract(tesseract_cmd: str) -> None:
    """Set the Tesseract executable path.

    Args:
        tesseract_cmd: Absolute path to tesseract.exe
    """
    global _tesseract_cmd
    _tesseract_cmd = tesseract_cmd
    try:
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    except ImportError:
        logger.warning("pytesseract not installed — OCR will not be available")


def _load_image(source) -> np.ndarray:
    """Load an image from file path or bytes into OpenCV format.

    Uses cv2.imdecode for Windows Unicode path safety.

    Args:
        source: File path (str/Path) or image bytes.

    Returns:
        OpenCV BGR image array.
    """
    if isinstance(source, (str, Path)):
        # Windows-safe: use numpy fromfile to handle Unicode paths
        img_array = np.fromfile(str(source), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    elif isinstance(source, bytes):
        img_array = np.frombuffer(source, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    else:
        raise ValueError(f"Unsupported source type: {type(source)}")

    if img is None:
        raise ValueError("Could not decode image")

    return img


def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    """Preprocess a medical document image for optimal OCR.

    Pipeline:
    1. Upscale small images (Tesseract works best at ~300 DPI)
    2. Convert to grayscale
    3. Bilateral denoising (removes paper grain while preserving text edges)
    4. CLAHE contrast enhancement
    5. Deskewing
    6. Adaptive binarization

    Args:
        image: OpenCV BGR image.

    Returns:
        Preprocessed binary image ready for OCR.
    """
    h, w = image.shape[:2]

    # 1. Upscale small images (target ~300 DPI equivalent)
    if h < 1000 or w < 1000:
        scale = max(2, 2000 // min(h, w))
        image = cv2.resize(image, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)

    # 2. Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. Bilateral denoising — removes paper texture while keeping text sharp
    denoised = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # 4. CLAHE contrast enhancement — handles uneven illumination
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    # 5. Deskewing — straighten slightly rotated scans
    enhanced = _deskew(enhanced)

    # 6. Adaptive binarization — handles varying backgrounds
    binary = cv2.adaptiveThreshold(
        enhanced, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=15, C=8
    )

    return binary


def _deskew(image: np.ndarray, max_angle: float = 5.0) -> np.ndarray:
    """Deskew a grayscale image if it's slightly rotated.

    Args:
        image: Grayscale image.
        max_angle: Maximum rotation angle to correct (degrees).

    Returns:
        Deskewed image.
    """
    coords = np.column_stack(np.where(image < 200))
    if len(coords) < 100:
        return image

    angle = cv2.minAreaRect(coords)[-1]

    # Normalize angle
    if angle < -45:
        angle = -(90 + angle)
    elif angle > 45:
        angle = 90 - angle
    else:
        angle = -angle

    # Only correct if skew is noticeable but not extreme
    if abs(angle) < 0.5 or abs(angle) > max_angle:
        return image

    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def extract_text_from_image(
    source,
    psm: int = 3,
    preprocess: bool = True,
) -> dict:
    """Extract text from an image using Tesseract OCR.

    Args:
        source: Image file path (str/Path) or image bytes (e.g., from PDF rendering).
        psm: Tesseract Page Segmentation Mode.
             3 = Fully automatic (default, good for full pages)
             6 = Uniform block of text (good for tables/prescriptions)
             11 = Sparse text (good for lab sheets)
        preprocess: Whether to apply preprocessing pipeline.

    Returns:
        Dictionary with extracted text and metadata.
    """
    import pytesseract

    if _tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = _tesseract_cmd

    # Load image
    img = _load_image(source)

    # Preprocess
    if preprocess:
        processed = preprocess_for_ocr(img)
    else:
        processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Run OCR
    custom_config = f"--oem 1 --psm {psm}"
    text = pytesseract.image_to_string(processed, config=custom_config)

    # Get confidence data
    try:
        data = pytesseract.image_to_data(processed, config=custom_config, output_type=pytesseract.Output.DICT)
        confidences = [int(c) for c in data["conf"] if int(c) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    except Exception:
        avg_confidence = 0.0

    return {
        "text": text.strip(),
        "confidence": round(avg_confidence, 2),
        "method": "tesseract_ocr",
        "psm": psm,
        "preprocessed": preprocess,
    }


def is_tesseract_available() -> bool:
    """Check if Tesseract is installed and accessible."""
    try:
        import pytesseract
        if _tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = _tesseract_cmd
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
        return True
    except Exception as e:
        logger.warning(f"Tesseract not available: {e}")
        return False
