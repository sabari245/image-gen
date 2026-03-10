import os
import shutil
from pathlib import Path
from uuid import uuid4

STORAGE_DIR = Path(__file__).parent.parent.parent / "storage"
INPUTS_DIR = STORAGE_DIR / "inputs"
OUTPUTS_DIR = STORAGE_DIR / "outputs"


def ensure_dirs():
    INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def save_input_image(data: bytes, original_filename: str) -> tuple[str, int]:
    """Save an uploaded input image and return (relative_path, file_size)."""
    ensure_dirs()
    ext = Path(original_filename).suffix or ".png"
    filename = f"{uuid4().hex}{ext}"
    file_path = INPUTS_DIR / filename
    file_path.write_bytes(data)
    return f"inputs/{filename}", len(data)


def save_output_image(data: bytes, generation_id: int, index: int) -> tuple[str, int]:
    """Save a generated output image and return (relative_path, file_size)."""
    ensure_dirs()
    filename = f"{generation_id}_{index}.webp"
    file_path = OUTPUTS_DIR / filename
    file_path.write_bytes(data)
    return f"outputs/{filename}", len(data)


def get_image_path(relative_path: str) -> Path:
    """Get absolute path for a stored image."""
    return STORAGE_DIR / relative_path


def delete_image(relative_path: str):
    """Delete an image file."""
    path = get_image_path(relative_path)
    if path.exists():
        path.unlink()


def delete_generation_files(file_paths: list[str]):
    """Delete all files associated with a generation."""
    for path in file_paths:
        delete_image(path)
