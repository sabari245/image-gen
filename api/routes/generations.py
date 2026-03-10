from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Generation
from ..schemas import GenerationSchema, HistoryResponse
from ..services.storage import delete_generation_files

router = APIRouter()


@router.get("/generations/{generation_id}", response_model=GenerationSchema)
def get_generation(generation_id: int, db: Session = Depends(get_db)):
    """Get a generation by ID."""
    generation = db.query(Generation).filter(Generation.id == generation_id).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    return generation


@router.get("/history", response_model=HistoryResponse)
def get_history(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get paginated generation history."""
    total = db.query(Generation).count()
    offset = (page - 1) * page_size

    items = (
        db.query(Generation)
        .order_by(Generation.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return HistoryResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.delete("/generations/{generation_id}")
def delete_generation(generation_id: int, db: Session = Depends(get_db)):
    """Delete a generation and its files."""
    generation = db.query(Generation).filter(Generation.id == generation_id).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")

    file_paths = [img.file_path for img in generation.images]
    delete_generation_files(file_paths)

    db.delete(generation)
    db.commit()

    return {"status": "deleted"}
