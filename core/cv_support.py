import os
import urllib.request
from pathlib import Path

import cv2


def resolve_haar_cascade_path(filename: str) -> str:
    """Return a usable Haar cascade XML path for this environment.

    Some OpenCV wheels omit the bundled data directory. When that happens,
    this helper falls back to a local repo copy and downloads the XML from the
    upstream OpenCV project if needed.
    """
    candidates = []

    data_dir = getattr(cv2.data, "haarcascades", None)
    if data_dir:
        candidate = os.path.join(data_dir, filename)
        candidates.append(candidate)

    package_dir = Path(cv2.__file__).resolve().parent
    candidates.extend([
        str(package_dir / "data" / filename),
        str(Path(__file__).resolve().parent.parent / "data" / filename),
    ])

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    local_dir = Path(__file__).resolve().parent.parent / "data"
    local_dir.mkdir(parents=True, exist_ok=True)
    local_path = local_dir / filename

    url = (
        "https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/"
        f"{filename}"
    )
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            payload = response.read()
        local_path.write_bytes(payload)
        if local_path.exists():
            return str(local_path)
    except Exception:
        pass

    return ""
