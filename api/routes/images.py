from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from ..services.storage import get_image_path

router = APIRouter()


@router.get("/images/{path:path}")
def get_image(path: str):
    """Serve a stored image."""
    file_path = get_image_path(path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    media_type = "image/webp"
    if file_path.suffix.lower() in (".png",):
        media_type = "image/png"
    elif file_path.suffix.lower() in (".jpg", ".jpeg"):
        media_type = "image/jpeg"

    return FileResponse(file_path, media_type=media_type)
